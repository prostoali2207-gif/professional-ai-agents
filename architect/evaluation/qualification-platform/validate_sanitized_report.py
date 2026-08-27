#!/usr/bin/env python3
from __future__ import annotations

import argparse
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


def completeness_status(report: dict, prereg: dict) -> str:
    expected_tasks = int(prereg["fixture_count"])
    per_family = int(prereg["per_family"])
    expected_families = prereg["families"]

    tasks_attempted = report.get("tasks_attempted", report.get("attempted"))
    if not isinstance(tasks_attempted, int) or tasks_attempted < expected_tasks:
        return "TRUNCATED"

    families = report.get("family_level_aggregate")
    if not isinstance(families, dict) or set(families) != set(expected_families):
        return "TRUNCATED"

    for family in expected_families:
        aggregate = families[family]
        if not isinstance(aggregate, dict):
            return "TRUNCATED"
        attempted = aggregate.get("tasks_attempted", aggregate.get("attempted"))
        if not isinstance(attempted, int) or attempted < per_family:
            return "TRUNCATED"

    if str(report.get("execution_status", "")).lower() == "completed":
        if tasks_attempted < expected_tasks or any(
            families[family].get("tasks_attempted", families[family].get("attempted")) < per_family
            for family in expected_families
        ):
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
