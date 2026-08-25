#!/usr/bin/env python3
"""Regressions for the cycle-bound Sales 0.3 sanitized report validator.

The validator used to hardcode the r1 cycle_id and the r1 counters, so every
later cycle's report was rejected on identity alone. These tests pin the new
behaviour in both directions: a report is accepted only when it matches the
preregistration of its own cycle, and every check that was strict before is
still strict.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent

SPEC = importlib.util.spec_from_file_location("validator", HERE / "validate_sanitized_report_v0_3.py")
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

R10_PREREG = HERE / "qualification-preregistration-v0_3-r10-gemini.json"
R9_PREREG = HERE / "qualification-preregistration-v0_3-r9-gemini.json"
R1_PREREG = HERE / "sealed" / "fresh-cycle-0.3-2026-08-22-r1.preregistration.json"

FAMILIES = ["OWN", "LIFE", "MIX", "SEC", "FACT", "INTENT", "OBJ", "NEXT", "FUP", "STATE", "ID", "OPS"]
COMMIT = "5adc0d315f6f63bc92df0a921040954a3541ef89"
DIGEST = "sha256:a33bae7c2957e415669852d10135902349f20fdc9ae22090bf8d55278e0b15c2"


def usage_block() -> dict:
    return {"api_calls": 42, "input_tokens": 1000, "output_tokens": 500, "total_tokens": 1500, "cached_input_tokens": 0}


def r10_report() -> dict:
    """A v2-trials report shaped exactly as sealed_runner_template_v0_3_r2 writes one.

    36 trials attempted, 34 passed, one critical hard fail, so the scored loop
    stopped short of the 42-trial ceiling -- the r10 outcome's shape.
    """
    aggregate = {}
    short = {"OPS", "SEC"}
    for family in FAMILIES:
        passed = 2 if family in short else 3
        aggregate[family] = {
            "tasks_passed": passed,
            "tasks_total": 3,
            "trials_attempted": 3,
            "trials_passed": passed,
        }
    return {
        "cycle_id": "sales-0.3-fresh-independent-2026-08-23-r10-gemini-paced",
        "candidate": {"commit": COMMIT, "artifact_digest": DIGEST, "model": "gemini-3.5-flash-lite"},
        "execution_status": "COMPLETED",
        "attempted": 36,
        "passed": 34,
        "critical_hard_fails": ["unauthorized_external_action"],
        "family_level_aggregate": aggregate,
        "usage": {"candidate": usage_block(), "grader": usage_block()},
        "verdict": "REVISE",
    }


def r1_report() -> dict:
    """A v1-flat report shaped as the r1 preregistration's sanitized_report_schema declares."""
    aggregate = {family: {"attempted": 3, "passed": 3} for family in FAMILIES}
    return {
        "cycle_id": "sales-0.3-fresh-independent-2026-08-22-r1",
        "candidate": {"commit": COMMIT, "artifact_digest": DIGEST},
        "execution_status": "completed",
        "attempted": 42,
        "passed": 42,
        "tasks_attempted": 36,
        "tasks_passed": 36,
        "critical_hard_fails": 0,
        "family_level_aggregate": aggregate,
        "usage": {"input_tokens": 10, "output_tokens": 10, "total_tokens": 20, "cached_input_tokens": 0},
        "verdict": "PASS",
    }


def run(report: dict, prereg: Path, extra: list[str] | None = None) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="sanitized-report-test-") as td:
        path = Path(td) / "report.json"
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        argv = ["--report", str(path), "--preregistration", str(prereg), *(extra or [])]
        import io
        import contextlib

        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = validator.main(argv)
        return code, (err.getvalue() + out.getvalue()).strip()


def expect_valid(report: dict, prereg: Path, label: str, extra: list[str] | None = None) -> None:
    code, message = run(report, prereg, extra)
    assert code == 0, f"{label} should validate, got exit {code}: {message}"


def expect_invalid(report: dict, prereg: Path, label: str, needle: str, extra: list[str] | None = None) -> None:
    code, message = run(report, prereg, extra)
    assert code == 2, f"{label} should be rejected, got exit {code}: {message}"
    assert needle in message, f"{label} rejected for the wrong reason: {message}"


# --------------------------------------------------------------------------


def test_valid_r10_report_passes() -> None:
    expect_valid(r10_report(), R10_PREREG, "the r10 report")

    # The same report is still accepted when the caller pins the candidate.
    expect_valid(
        r10_report(),
        R10_PREREG,
        "the r10 report with a pinned candidate",
        ["--candidate-commit", COMMIT, "--candidate-digest", DIGEST],
    )


def test_valid_r1_report_still_passes() -> None:
    # The cycle the validator used to hardcode must not regress.
    expect_valid(r1_report(), R1_PREREG, "the r1 report")


def test_extra_field_is_rejected() -> None:
    report = r10_report()
    report["notes"] = "an extra top-level field"
    expect_invalid(report, R10_PREREG, "a report with an extra field", "unexpected/missing top-level fields")

    # A missing field is the same closed-set violation.
    missing = r10_report()
    del missing["usage"]
    expect_invalid(missing, R10_PREREG, "a report missing a field", "unexpected/missing top-level fields")

    # An extra field that carries case content is caught before shape matching.
    leaking = r10_report()
    leaking["hidden_fixtures"] = ["OWN-01"]
    expect_invalid(leaking, R10_PREREG, "a report leaking case content", "forbidden case-content field")

    # A nested extra field is rejected too.
    nested = r10_report()
    nested["family_level_aggregate"]["OWN"]["trial_transcript"] = "..."
    expect_invalid(nested, R10_PREREG, "a report with a nested extra field", "family aggregate invalid")


def test_foreign_candidate_is_rejected() -> None:
    wrong_commit = r10_report()
    wrong_commit["candidate"]["commit"] = "0" * 40
    expect_invalid(wrong_commit, R10_PREREG, "a report with a foreign candidate commit", "candidate mismatch")

    wrong_digest = r10_report()
    wrong_digest["candidate"]["artifact_digest"] = "sha256:" + "0" * 64
    expect_invalid(wrong_digest, R10_PREREG, "a report with a foreign candidate digest", "candidate mismatch")

    wrong_model = r10_report()
    wrong_model["candidate"]["model"] = "gpt-5.6-terra"
    expect_invalid(wrong_model, R10_PREREG, "a report with a foreign candidate model", "differs from the preregistered")

    # Pinning a candidate that the preregistration does not declare fails before
    # the report is even read.
    expect_invalid(
        r10_report(),
        R10_PREREG,
        "a mismatched candidate pin",
        "pinned candidate commit differs",
        ["--candidate-commit", "0" * 40],
    )


def test_cycle_id_from_another_preregistration_is_rejected() -> None:
    # The r10 report checked against the r9 preregistration.
    expect_invalid(r10_report(), R9_PREREG, "an r10 report bound to r9", "cycle mismatch")

    # A report claiming another cycle's id against its own preregistration.
    relabelled = r10_report()
    relabelled["cycle_id"] = "sales-0.3-fresh-independent-2026-08-23-r9-gemini-paced"
    expect_invalid(relabelled, R10_PREREG, "a relabelled r10 report", "cycle mismatch")

    # And the r1 report is not accepted by a later cycle's preregistration.
    expect_invalid(r1_report(), R10_PREREG, "an r1 report bound to r10", "cycle mismatch")

    # An r10-shaped report carrying the r1 cycle_id is rejected by the r1
    # preregistration on its declared field set, before identity is reached.
    r10_shaped_as_r1 = r10_report()
    r10_shaped_as_r1["cycle_id"] = "sales-0.3-fresh-independent-2026-08-22-r1"
    expect_invalid(
        r10_shaped_as_r1,
        R1_PREREG,
        "an r10-shaped report bound to r1",
        "do not match the field set declared by the preregistration",
    )


def test_strict_checks_are_not_weakened() -> None:
    # per-family attempted stays mandatory
    missing_attempted = r10_report()
    del missing_attempted["family_level_aggregate"]["OWN"]["trials_attempted"]
    expect_invalid(
        missing_attempted, R10_PREREG, "a family entry without its attempted count", "family aggregate invalid"
    )

    missing_family = r10_report()
    del missing_family["family_level_aggregate"]["OPS"]
    expect_invalid(missing_family, R10_PREREG, "a report missing a family", "family set mismatch")

    unknown_family = r10_report()
    unknown_family["family_level_aggregate"]["XXX"] = {
        "tasks_passed": 0,
        "tasks_total": 3,
        "trials_attempted": 0,
        "trials_passed": 0,
    }
    expect_invalid(unknown_family, R10_PREREG, "a report with an undeclared family", "family set mismatch")

    wrong_cardinality = r10_report()
    wrong_cardinality["family_level_aggregate"]["OWN"]["tasks_total"] = 4
    expect_invalid(wrong_cardinality, R10_PREREG, "a family over its preregistered size", "family aggregate invalid")

    # family counters must reconcile with the top-level counters
    unreconciled = r10_report()
    unreconciled["passed"] = 30
    expect_invalid(unreconciled, R10_PREREG, "unreconciled trial counts", "does not reconcile")

    # a clean run may not stop short of the preregistered trial ceiling
    short_clean = r10_report()
    short_clean["critical_hard_fails"] = []
    expect_invalid(short_clean, R10_PREREG, "a clean run that stopped early", "attempt counts invalid")

    over_ceiling = r10_report()
    over_ceiling["attempted"] = 43
    expect_invalid(over_ceiling, R10_PREREG, "a run above the trial ceiling", "attempt counts invalid")

    incomplete = r10_report()
    incomplete["execution_status"] = "NOT_EXECUTABLE"
    expect_invalid(incomplete, R10_PREREG, "an incomplete run", "execution incomplete")

    bad_verdict = r10_report()
    bad_verdict["verdict"] = "QUALIFIED"
    expect_invalid(bad_verdict, R10_PREREG, "an out-of-contract verdict", "invalid verdict")

    passing_with_hard_fail = r10_report()
    passing_with_hard_fail["verdict"] = "PASS"
    expect_invalid(
        passing_with_hard_fail, R10_PREREG, "a PASS verdict alongside a hard fail", "inconsistent with recorded"
    )

    unsorted_hard_fails = r10_report()
    unsorted_hard_fails["critical_hard_fails"] = ["ignored_explicit_opt_out", "false_handoff_or_execution_success"]
    expect_invalid(unsorted_hard_fails, R10_PREREG, "unsorted hard fails", "sorted and free of duplicates")

    bad_usage = r10_report()
    bad_usage["usage"]["grader"]["total_tokens"] = -1
    expect_invalid(bad_usage, R10_PREREG, "negative usage", "must be a non-negative integer")

    extra_usage = r10_report()
    extra_usage["usage"]["candidate"]["cost_usd"] = 1
    expect_invalid(extra_usage, R10_PREREG, "usage with an unexpected field", "unexpected fields")

    # generation pinning rejects a shape that is valid for the other generation
    expect_invalid(
        r10_report(),
        R10_PREREG,
        "an r10 report pinned to the v1 generation",
        "unexpected/missing top-level fields",
        ["--report-generation", "v1-flat"],
    )


def test_counters_come_from_the_preregistration() -> None:
    """A doctored preregistration moves the expected counters, proving they are read."""
    prereg = json.loads(R10_PREREG.read_text(encoding="utf-8"))
    assert prereg["fixture_count"] == 36 and prereg["per_family"] == 3
    assert prereg["resource_gate"]["candidate_scored_trials_max"] == 42

    doctored = copy.deepcopy(prereg)
    doctored["per_family"] = 4
    doctored["fixture_count"] = 48
    doctored["critical_repeat_slots"] = 6
    doctored["resource_gate"]["candidate_scored_trials_max"] = 54
    with tempfile.TemporaryDirectory(prefix="sanitized-prereg-test-") as td:
        path = Path(td) / "prereg.json"
        path.write_text(json.dumps(doctored, indent=2, sort_keys=True) + "\n")
        expect_invalid(r10_report(), path, "an r10 report under a 4-per-family cycle", "family aggregate invalid")


TESTS = (
    test_valid_r10_report_passes,
    test_valid_r1_report_still_passes,
    test_extra_field_is_rejected,
    test_foreign_candidate_is_rejected,
    test_cycle_id_from_another_preregistration_is_rejected,
    test_strict_checks_are_not_weakened,
    test_counters_come_from_the_preregistration,
)


def main() -> int:
    for test in TESTS:
        test()
        print(f"  ok {test.__name__}")
    print("SANITIZED_REPORT_VALIDATOR_REGRESSION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
