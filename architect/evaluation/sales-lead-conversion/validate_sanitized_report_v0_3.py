#!/usr/bin/env python3
"""Validate a Sales 0.3 sanitized qualification report against its own cycle.

The cycle identity and every expected counter are read from the preregistration
of the cycle being validated. Nothing about a specific cycle is a constant in
this file, so a report from r2, r7 or r10 is checked as strictly as r1 was.

What stays strict:

* the top-level field set is closed. A report must match its cycle's declared
  field set exactly -- no extra field, no missing field. When the
  preregistration declares `sanitized_report_schema`, that list is the closed
  set; otherwise the set comes from this file's closed registry of known report
  generations, and a shape that matches no generation is rejected;
* the frozen candidate commit and artifact digest are compared for exact
  equality, and the caller may pin them again on the command line;
* per-family `attempted` is mandatory for every declared family;
* no field carrying case content is accepted. The closed field set already
  excludes it, and a deep scan rejects known sensitive keys anywhere in the
  document as a second barrier.

Report generations
------------------

Two report shapes exist in this repository and both are validated here:

`v1-flat`
    Written by the r1-era runner. Flat `usage`, integer `critical_hard_fails`,
    per-family `{attempted, passed}`, lowercase `completed`, and explicit
    `tasks_attempted` / `tasks_passed`.

`v2-trials`
    Written by `sealed_runner_template_v0_3_r2.py` and every provider wrapper
    layered on it, r2 through r10. Split `usage` (`candidate` / `grader`),
    `critical_hard_fails` as a sorted unique list of hard-fail identifiers,
    per-family `{tasks_passed, tasks_total, trials_attempted, trials_passed}`,
    uppercase `COMPLETED`, and no `tasks_*` top-level fields.

`v2-trials` runners stop the scored loop at the first critical hard fail, which
is preregistered behaviour, so `attempted` is bounded by the cycle's trial
ceiling rather than pinned to it. When no hard fail was recorded the run must
have gone the full distance, and the per-family trial counters must sum to the
top-level counters, so the loose case is bounded from both sides.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

# Keys that must never appear anywhere in a public report, at any depth.
FORBIDDEN_KEYS = {
    "prompt",
    "raw_prompt",
    "hidden_prompt",
    "expected_answer",
    "expected_answers",
    "grader_key",
    "grader_keys",
    "grader_prompt",
    "raw_response",
    "raw_responses",
    "fixture_text",
    "hidden_fixture",
    "hidden_fixtures",
    "fixtures",
    "task",
    "initial_state",
    "observable_candidate_record",
}
# Note: bare "grader" is deliberately NOT forbidden. The v2 usage object splits
# token counters into "candidate" and "grader", which carry no case content.

USAGE_COUNTERS = ("input_tokens", "output_tokens", "total_tokens", "cached_input_tokens")

GENERATIONS: dict[str, dict[str, Any]] = {
    "v1-flat": {
        "fields": frozenset(
            {
                "cycle_id",
                "candidate",
                "execution_status",
                "attempted",
                "passed",
                "tasks_attempted",
                "tasks_passed",
                "critical_hard_fails",
                "family_level_aggregate",
                "usage",
                "verdict",
            }
        ),
        "completed_status": "completed",
        "family_fields": frozenset({"attempted", "passed"}),
        "family_attempted_field": "attempted",
    },
    "v2-trials": {
        "fields": frozenset(
            {
                "cycle_id",
                "candidate",
                "execution_status",
                "attempted",
                "passed",
                "critical_hard_fails",
                "family_level_aggregate",
                "usage",
                "verdict",
            }
        ),
        "completed_status": "COMPLETED",
        "family_fields": frozenset({"tasks_passed", "tasks_total", "trials_attempted", "trials_passed"}),
        "family_attempted_field": "trials_attempted",
    },
}


class ReportInvalid(Exception):
    pass


def fail(message: str) -> None:
    raise ReportInvalid(message)


def load_json(path: Path, what: str) -> Any:
    if not path.is_file():
        fail(f"missing {what}: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {what}: {exc}")


def scan_forbidden(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_KEYS:
                fail(f"forbidden case-content field at {path}.{key}")
            scan_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_forbidden(child, f"{path}[{index}]")


# --------------------------------------------------------------------------
# preregistration reading
# --------------------------------------------------------------------------


class CycleContract:
    """Expected cycle parameters, read from one cycle's preregistration.

    Two preregistration dialects exist in this repository: the r1 records nest
    cardinality under `fixture_design` and name families in
    `construct_families`, while r4-r10 records put them at the top level. Both
    are read here; neither is guessed at.
    """

    def __init__(self, prereg: dict, source: Path):
        self.source = source
        self.cycle_id = self._require(prereg, "cycle_id", str)

        candidate = self._require(prereg, "frozen_candidate", dict)
        self.candidate_commit = self._require(candidate, "commit", str, "frozen_candidate")
        self.candidate_digest = self._require(candidate, "artifact_digest", str, "frozen_candidate")

        design = prereg.get("fixture_design") if isinstance(prereg.get("fixture_design"), dict) else prereg
        self.fixture_count = int(self._require(design, "fixture_count", int, "fixture_count source"))
        self.per_family = int(self._require(design, "per_family", int, "per_family source"))

        families = prereg.get("families")
        if isinstance(families, list) and families:
            self.families = frozenset(str(x) for x in families)
        elif isinstance(prereg.get("construct_families"), dict) and prereg["construct_families"]:
            self.families = frozenset(prereg["construct_families"])
        else:
            fail("preregistration declares no family set")
        declared_family_count = design.get("family_count")
        if isinstance(declared_family_count, int) and declared_family_count != len(self.families):
            fail("preregistration family_count disagrees with its own family set")
        if self.per_family * len(self.families) != self.fixture_count:
            fail("preregistration cardinality is internally inconsistent")

        self.repeat_slots = self._repeat_slots(prereg)
        self.trial_ceiling = self._trial_ceiling(prereg)

        runtime = prereg.get("runtime_contract") if isinstance(prereg.get("runtime_contract"), dict) else {}
        model = runtime.get("candidate_model") or runtime.get("model")
        self.candidate_model = str(model) if isinstance(model, str) and model else None

        schema = prereg.get("sanitized_report_schema")
        if schema is not None and (not isinstance(schema, list) or not all(isinstance(x, str) for x in schema)):
            fail("preregistration sanitized_report_schema must be a list of field names")
        if isinstance(schema, list) and len(schema) != len(set(schema)):
            fail("preregistration sanitized_report_schema contains duplicate field names")
        self.declared_fields = frozenset(schema) if isinstance(schema, list) else None

    @staticmethod
    def _require(node: dict, key: str, kind: type, where: str = "preregistration"):
        if key not in node:
            fail(f"{where} is missing required key: {key}")
        value = node[key]
        if kind is int and isinstance(value, bool):
            fail(f"{where} key {key} must be {kind.__name__}")
        if not isinstance(value, kind):
            fail(f"{where} key {key} must be {kind.__name__}")
        return value

    def _repeat_slots(self, prereg: dict) -> int:
        if isinstance(prereg.get("critical_repeat_slots"), int):
            return int(prereg["critical_repeat_slots"])
        policy = prereg.get("stochastic_retry_policy")
        if isinstance(policy, dict) and isinstance(policy.get("repeated_fixture_ids"), list):
            return len(policy["repeated_fixture_ids"])
        fail("preregistration declares no repeated-fixture count")

    def _trial_ceiling(self, prereg: dict) -> int:
        derived = self.fixture_count + self.repeat_slots
        gate = prereg.get("resource_gate")
        if isinstance(gate, dict) and isinstance(gate.get("candidate_scored_trials_max"), int):
            declared = int(gate["candidate_scored_trials_max"])
            if declared != derived:
                fail(
                    "preregistration candidate_scored_trials_max "
                    f"{declared} disagrees with its own fixture/repeat counts ({derived})"
                )
            return declared
        return derived


# --------------------------------------------------------------------------
# report validation
# --------------------------------------------------------------------------


def select_generation(report: dict, contract: CycleContract, pinned: str | None) -> tuple[str, dict]:
    observed = frozenset(report)
    if pinned:
        if pinned not in GENERATIONS:
            fail(f"unknown report generation: {pinned}")
        generation = GENERATIONS[pinned]
        if observed != generation["fields"]:
            fail("unexpected/missing top-level fields")
        name = pinned
    else:
        matches = [n for n, g in GENERATIONS.items() if g["fields"] == observed]
        if len(matches) != 1:
            fail("unexpected/missing top-level fields")
        name = matches[0]
        generation = GENERATIONS[name]
    if contract.declared_fields is not None and contract.declared_fields != observed:
        fail("report fields do not match the field set declared by the preregistration")
    return name, generation


def check_nonneg_int(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        fail(f"{label} must be a non-negative integer")
    return value


def validate_usage(usage: Any, generation_name: str) -> None:
    def flat(node: Any, label: str) -> None:
        if not isinstance(node, dict):
            fail(f"{label} must be an object")
        for key in USAGE_COUNTERS:
            check_nonneg_int(node.get(key), f"{label}.{key}")
        extra = set(node) - set(USAGE_COUNTERS) - {"api_calls"}
        if extra:
            fail(f"{label} carries unexpected fields: {', '.join(sorted(extra))}")
        if "api_calls" in node:
            check_nonneg_int(node["api_calls"], f"{label}.api_calls")

    if generation_name == "v2-trials":
        if not isinstance(usage, dict) or set(usage) != {"candidate", "grader"}:
            fail("usage must declare exactly candidate and grader")
        flat(usage["candidate"], "usage.candidate")
        flat(usage["grader"], "usage.grader")
    else:
        flat(usage, "usage")


def validate_report(report: Any, contract: CycleContract, pinned: str | None) -> tuple[str, dict]:
    if not isinstance(report, dict):
        fail("report must be a JSON object")
    scan_forbidden(report)
    generation_name, generation = select_generation(report, contract, pinned)

    if report["cycle_id"] != contract.cycle_id:
        fail(
            f"cycle mismatch: report is {report['cycle_id']!r}, "
            f"preregistration {contract.source} is {contract.cycle_id!r}"
        )

    candidate = report["candidate"]
    if not isinstance(candidate, dict):
        fail("candidate must be an object")
    if candidate.get("commit") != contract.candidate_commit:
        fail("candidate mismatch")
    if candidate.get("artifact_digest") != contract.candidate_digest:
        fail("candidate mismatch")
    extra_candidate = set(candidate) - {"commit", "artifact_digest", "model"}
    if extra_candidate:
        fail(f"candidate carries unexpected fields: {', '.join(sorted(extra_candidate))}")
    if contract.candidate_model is not None and "model" in candidate:
        if candidate["model"] != contract.candidate_model:
            fail(
                f"candidate model {candidate['model']!r} differs from the preregistered "
                f"{contract.candidate_model!r}"
            )

    if report["execution_status"] != generation["completed_status"]:
        fail("execution incomplete")
    if report["verdict"] not in {"PASS", "REVISE"}:
        fail("invalid verdict")

    aggregate = report["family_level_aggregate"]
    if not isinstance(aggregate, dict):
        fail("family_level_aggregate must be an object")
    if set(aggregate) != set(contract.families):
        fail("family set mismatch")

    attempted_field = generation["family_attempted_field"]
    family_attempted_total = 0
    family_passed_total = 0
    family_tasks_total = 0
    family_tasks_passed = 0
    for family, entry in sorted(aggregate.items()):
        if not isinstance(entry, dict) or set(entry) != set(generation["family_fields"]):
            fail("family aggregate invalid")
        for key, value in sorted(entry.items()):
            check_nonneg_int(value, f"family_level_aggregate.{family}.{key}")
        if attempted_field not in entry:
            fail(f"family_level_aggregate.{family} is missing mandatory {attempted_field}")
        if generation_name == "v1-flat":
            if entry["attempted"] != contract.per_family:
                fail("family aggregate invalid")
            if entry["passed"] > entry["attempted"]:
                fail("family aggregate invalid")
            family_attempted_total += entry["attempted"]
            family_passed_total += entry["passed"]
        else:
            if entry["tasks_total"] != contract.per_family:
                fail("family aggregate invalid")
            if entry["tasks_passed"] > entry["tasks_total"]:
                fail("family aggregate invalid")
            if entry["trials_passed"] > entry["trials_attempted"]:
                fail("family aggregate invalid")
            if entry["trials_attempted"] < entry["tasks_passed"]:
                fail("family aggregate invalid")
            family_attempted_total += entry["trials_attempted"]
            family_passed_total += entry["trials_passed"]
            family_tasks_total += entry["tasks_total"]
            family_tasks_passed += entry["tasks_passed"]

    attempted = check_nonneg_int(report["attempted"], "attempted")
    passed = check_nonneg_int(report["passed"], "passed")
    if passed > attempted:
        fail("attempt counts invalid")
    if attempted > contract.trial_ceiling:
        fail("attempt counts invalid")

    if generation_name == "v1-flat":
        tasks_attempted = check_nonneg_int(report["tasks_attempted"], "tasks_attempted")
        tasks_passed = check_nonneg_int(report["tasks_passed"], "tasks_passed")
        if tasks_attempted != contract.fixture_count or tasks_passed > tasks_attempted:
            fail("task counts invalid")
        if attempted != contract.trial_ceiling:
            fail("attempt counts invalid")
        if family_attempted_total != tasks_attempted or family_passed_total > tasks_attempted:
            fail("family aggregate does not reconcile with task counts")
        hard_fails = check_nonneg_int(report["critical_hard_fails"], "critical_hard_fails")
    else:
        if family_tasks_total != contract.fixture_count:
            fail("task counts invalid")
        if family_tasks_passed > family_tasks_total:
            fail("task counts invalid")
        if family_attempted_total != attempted or family_passed_total != passed:
            fail("family aggregate does not reconcile with trial counts")
        raw_hard_fails = report["critical_hard_fails"]
        if not isinstance(raw_hard_fails, list) or not all(isinstance(x, str) and x for x in raw_hard_fails):
            fail("critical_hard_fails must be a list of hard-fail identifiers")
        if list(raw_hard_fails) != sorted(set(raw_hard_fails)):
            fail("critical_hard_fails must be sorted and free of duplicates")
        hard_fails = len(raw_hard_fails)
        # The scored loop only stops short of the ceiling on a critical hard
        # fail. With none recorded the cycle must have run every trial.
        if hard_fails == 0 and attempted != contract.trial_ceiling:
            fail("attempt counts invalid")

    if report["verdict"] == "PASS" and hard_fails:
        fail("verdict PASS is inconsistent with recorded critical hard fails")

    validate_usage(report["usage"], generation_name)
    return generation_name, aggregate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("report_positional", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("--report", help="path to the sanitized report JSON")
    parser.add_argument(
        "--preregistration",
        required=True,
        help="path to the preregistration of the cycle that produced the report",
    )
    parser.add_argument(
        "--report-generation",
        choices=sorted(GENERATIONS),
        help="pin the expected report generation instead of matching it by field set",
    )
    parser.add_argument("--candidate-commit", help="additionally pin the frozen candidate commit")
    parser.add_argument("--candidate-digest", help="additionally pin the frozen candidate artifact digest")
    parser.add_argument(
        "--emit-family-aggregate",
        action="store_true",
        help="on success print only family_level_aggregate as JSON",
    )
    args = parser.parse_args(argv)

    report_arg = args.report or args.report_positional or "sanitized-report.json"
    try:
        prereg_path = Path(args.preregistration)
        prereg = load_json(prereg_path, "preregistration")
        if not isinstance(prereg, dict):
            fail("preregistration must be a JSON object")
        contract = CycleContract(prereg, prereg_path)

        if args.candidate_commit and args.candidate_commit != contract.candidate_commit:
            fail("pinned candidate commit differs from the preregistered frozen candidate")
        if args.candidate_digest and args.candidate_digest != contract.candidate_digest:
            fail("pinned candidate digest differs from the preregistered frozen candidate")

        report = load_json(Path(report_arg), "report")
        generation_name, aggregate = validate_report(report, contract, args.report_generation)
    except ReportInvalid as exc:
        print(f"REPORT_INVALID: {exc}", file=sys.stderr)
        return 2

    if args.emit_family_aggregate:
        print(json.dumps(aggregate, indent=2, sort_keys=True))
    else:
        print(f"REPORT_VALID cycle={contract.cycle_id} generation={generation_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
