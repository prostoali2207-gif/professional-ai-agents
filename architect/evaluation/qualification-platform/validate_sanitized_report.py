#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

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
}


def walk(value, path="$"):
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_KEYS:
                raise ValueError(f"forbidden sensitive report field at {path}.{key}")
            walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            walk(child, f"{path}[{i}]")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--cycle-id", required=True)
    p.add_argument("--candidate-commit", required=True)
    p.add_argument("--candidate-digest", required=True)
    p.add_argument("--pack-digest", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--runner-exit-code", required=True, type=int)
    p.add_argument("--ledger-out", required=True)
    args = p.parse_args()

    report_path = Path(args.report)
    if not report_path.is_file() or report_path.stat().st_size == 0:
        print("sanitized report missing or empty", file=sys.stderr)
        return 2
    try:
        report = json.loads(report_path.read_text())
    except Exception as exc:
        print(f"sanitized report is not valid JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(report, dict):
        print("sanitized report must be a JSON object", file=sys.stderr)
        return 2
    try:
        walk(report)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    report_sha = hashlib.sha256(report_path.read_bytes()).hexdigest()
    ledger = {
        "qualification_release_evidence_version": 1,
        "cycle_id": args.cycle_id,
        "candidate_commit": args.candidate_commit,
        "candidate_digest": args.candidate_digest,
        "pack_digest": args.pack_digest,
        "model": args.model,
        "runner_exit_code": args.runner_exit_code,
        "report_sha256": report_sha,
        "report_sanitization_check": "pass",
    }
    Path(args.ledger_out).write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "report_sha256": report_sha}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
