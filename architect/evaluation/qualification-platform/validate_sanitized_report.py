#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

FORBIDDEN_KEYS = {
    "prompt", "raw_prompt", "hidden_prompt", "expected_answer", "expected_answers",
    "grader_key", "grader_keys", "grader_prompt", "raw_response", "raw_responses",
    "fixture_text", "hidden_fixture", "hidden_fixtures",
}


def walk(value, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_KEYS:
                raise ValueError(f"forbidden sensitive report field at {path}.{key}")
            walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            walk(child, f"{path}[{i}]")


def fail(message: str) -> int:
    print(f"REPORT_INVALID: {message}", file=sys.stderr)
    return 2


def _expected_trial_count(prereg: dict, expected_tasks: int) -> int:
    fixture_design = prereg.get("fixture_design")
    if not isinstance(fixture_design, dict):
        return expected_tasks
    value = fixture_design.get("expected_candidate_runs_if_full")
    if isinstance(value, int) and value >= expected_tasks:
        return value
    return expected_tasks


def _repeat_counts_by_family(prereg: dict) -> Counter[str]:
    fixture_design = prereg.get("fixture_design")
    if not isinstance(fixture_design, dict):
        return Counter()
    slots = fixture_design.get("repeated_fixture_slots")
    if not isinstance(slots, list):
        return Counter()
    out: Counter[str] = Counter()
    for slot in slots:
        if not isinstance(slot, str) or "-" not in slot:
            continue
        family, _ = slot.split("-", 1)
        if family:
            out[family] += 1
    return out


def _family_tasks_attempted(aggregate: dict) -> int | None:
    # Historical runners used `attempted`; current runners expose base-task
    # completeness as `tasks_total` and trial completeness separately.
    for key in ("tasks_attempted", "attempted", "tasks_total"):
        value = aggregate.get(key)
        if isinstance(value, int):
            return value
    return None


def completeness_status(report: dict, prereg: dict) -> str:
    expected_tasks = int(prereg["fixture_count"])
    per_family = int(prereg["per_family"])
    expected_families = prereg["families"]
    expected_trials = _expected_trial_count(prereg, expected_tasks)
    repeat_counts = _repeat_counts_by_family(prereg)

    trials_attempted = report.get("tasks_attempted", report.get("attempted"))
    if not isinstance(trials_attempted, int) or trials_attempted < expected_trials:
        return "TRUNCATED"

    families = report.get("family_level_aggregate")
    if not isinstance(families, dict) or set(families) != set(expected_families):
        return "TRUNCATED"

    for family in expected_families:
        aggregate = families[family]
        if not isinstance(aggregate, dict):
            return "TRUNCATED"
        task_attempted = _family_tasks_attempted(aggregate)
        if task_attempted is None or task_attempted < per_family:
            return "TRUNCATED"

        expected_family_trials = per_family + repeat_counts.get(family, 0)
        family_trials_attempted = aggregate.get("trials_attempted")
        if repeat_counts.get(family, 0):
            if not isinstance(family_trials_attempted, int) or family_trials_attempted < expected_family_trials:
                return "TRUNCATED"
        elif isinstance(family_trials_attempted, int) and family_trials_attempted < per_family:
            return "TRUNCATED"

    if str(report.get("execution_status", "")).lower() == "completed":
        if trials_attempted < expected_trials:
            return "TRUNCATED"
    return "COMPLETE"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--preregistration", required=True)
    p.add_argument("--cycle-id", required=True)
    p.add_argument("--candidate-commit", required=True)
    p.add_argument("--candidate-digest", required=True)
    p.add_argument("--pack-digest", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--runner-exit-code", required=True, type=int)
    p.add_argument("--ledger-out", required=True)
    args = p.parse_args()

    report_path = Path(args.report)
    prereg_path = Path(args.preregistration)
    if not report_path.is_file() or report_path.stat().st_size == 0:
        return fail("sanitized report missing or empty")
    if not prereg_path.is_file():
        return fail("preregistration missing")
    try:
        report = json.loads(report_path.read_text())
        prereg = json.loads(prereg_path.read_text())
    except Exception as exc:
        return fail(f"invalid JSON input: {exc}")
    if not isinstance(report, dict) or not isinstance(prereg, dict):
        return fail("report and preregistration must be JSON objects")
    try:
        walk(report)
        walk(prereg)
        status = completeness_status(report, prereg)
    except (ValueError, KeyError, TypeError) as exc:
        return fail(str(exc))

    report_sha = hashlib.sha256(report_path.read_bytes()).hexdigest()
    qualification_verdict = report.get("verdict")
    if status == "COMPLETE" and qualification_verdict not in {"PASS", "REVISE"}:
        return fail("missing or invalid qualification verdict")

    ledger = {
        "qualification_release_evidence_version": 2,
        "cycle_id": args.cycle_id,
        "candidate_commit": args.candidate_commit,
        "candidate_digest": args.candidate_digest,
        "pack_digest": args.pack_digest,
        "model": args.model,
        "runner_exit_code": args.runner_exit_code,
        "report_sha256": report_sha,
        "report_sanitization_check": "pass",
        "execution_completeness": status,
    }

    if status == "TRUNCATED":
        Path(args.ledger_out).write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
        print(json.dumps({"status": "TRUNCATED", "report_sha256": report_sha}))
        return 10

    ledger["qualification_verdict"] = qualification_verdict
    Path(args.ledger_out).write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "qualification_verdict": qualification_verdict, "report_sha256": report_sha}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
