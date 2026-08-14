#!/usr/bin/env python3
"""Vendor-neutral runner for Agent Architect behavioral validation.

The runner does not know how a specific model/runtime works. It invokes a candidate
adapter command using a small JSON protocol, verifies frozen fixture hashes, isolates
trials, and writes observable run records. Hidden grader material is never passed to
the candidate adapter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any


class HarnessError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def validate_manifest(manifest: dict[str, Any]) -> None:
    required = [
        "candidate_sha",
        "runner_version",
        "trial_count",
        "fixtures",
        "thresholds",
        "capability_profile",
        "evaluator_class",
    ]
    missing = [key for key in required if key not in manifest]
    if missing:
        raise HarnessError(f"manifest missing required fields: {', '.join(missing)}")
    if not isinstance(manifest["trial_count"], int) or manifest["trial_count"] < 1:
        raise HarnessError("trial_count must be a positive integer")
    if not isinstance(manifest["fixtures"], list) or not manifest["fixtures"]:
        raise HarnessError("fixtures must be a non-empty list")
    for fixture in manifest["fixtures"]:
        for key in ("id", "family", "priority", "path", "sha256"):
            if key not in fixture:
                raise HarnessError(f"fixture missing required field: {key}")


def invoke_candidate(command: str, payload: dict[str, Any], timeout_s: int) -> dict[str, Any]:
    proc = subprocess.run(
        command,
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        shell=True,
        capture_output=True,
        timeout=timeout_s,
        env={**os.environ, "AGENT_ARCHITECT_EVAL": "1"},
    )
    if proc.returncode != 0:
        raise HarnessError(
            f"candidate adapter failed with exit {proc.returncode}: {proc.stderr.strip()}"
        )
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise HarnessError("candidate adapter did not return valid JSON") from exc
    if not isinstance(result, dict):
        raise HarnessError("candidate adapter response must be a JSON object")
    return result


def mechanical_grade(fixture: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Grade only public mechanically-checkable invariants.

    Judgment-heavy or hidden-key grading must be performed by an external grader and
    merged into the run record later. The runner intentionally refuses to invent an
    LLM self-grade.
    """
    grader = fixture.get("mechanical_grader")
    if grader is None:
        return {"status": "PENDING_EXTERNAL_GRADER", "checks": []}

    checks = []
    for check in grader.get("required_equals", []):
        field = check["field"]
        expected = check["value"]
        observed = result.get(field)
        checks.append(
            {
                "type": "required_equals",
                "field": field,
                "expected": expected,
                "observed": observed,
                "pass": observed == expected,
            }
        )

    for check in grader.get("required_absent", []):
        field = check["field"]
        checks.append(
            {
                "type": "required_absent",
                "field": field,
                "pass": field not in result,
            }
        )

    status = "PASS" if checks and all(c["pass"] for c in checks) else "FAIL"
    if not checks:
        status = "PENDING_EXTERNAL_GRADER"
    return {"status": status, "checks": checks}


def run(manifest_path: Path, candidate_command: str, out_dir: Path, timeout_s: int) -> int:
    manifest = read_json(manifest_path)
    validate_manifest(manifest)

    root = manifest_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    records = out_dir / "runs.jsonl"
    summary: list[dict[str, Any]] = []

    for fixture_meta in manifest["fixtures"]:
        fixture_path = (root / fixture_meta["path"]).resolve()
        if not fixture_path.exists():
            raise HarnessError(f"fixture not found: {fixture_path}")
        observed_hash = sha256_file(fixture_path)
        if observed_hash != fixture_meta["sha256"]:
            raise HarnessError(
                f"fixture hash mismatch for {fixture_meta['id']}: "
                f"expected {fixture_meta['sha256']}, got {observed_hash}"
            )
        fixture = read_json(fixture_path)
        candidate_input = fixture.get("candidate_input")
        if candidate_input is None:
            raise HarnessError(f"fixture {fixture_meta['id']} has no candidate_input")

        for trial in range(1, manifest["trial_count"] + 1):
            run_id = f"{fixture_meta['id']}-t{trial}"
            started = time.time()
            with tempfile.TemporaryDirectory(prefix=f"aa-eval-{run_id}-") as tmp:
                run_dir = Path(tmp)
                payload = {
                    "protocol_version": 1,
                    "run_id": run_id,
                    "candidate_sha": manifest["candidate_sha"],
                    "family": fixture_meta["family"],
                    "priority": fixture_meta["priority"],
                    "trial": trial,
                    "capability_profile": manifest["capability_profile"],
                    "input": candidate_input,
                    "workspace": str(run_dir),
                }
                error = None
                result: dict[str, Any] = {}
                grade: dict[str, Any]
                try:
                    result = invoke_candidate(candidate_command, payload, timeout_s)
                    grade = mechanical_grade(fixture, result)
                except (HarnessError, subprocess.TimeoutExpired) as exc:
                    error = str(exc)
                    grade = {"status": "HARNESS_OR_EXECUTION_ERROR", "checks": []}

                artifact_dir = out_dir / "artifacts" / run_id
                artifact_dir.mkdir(parents=True, exist_ok=True)
                for child in run_dir.iterdir():
                    target = artifact_dir / child.name
                    if child.is_dir():
                        shutil.copytree(child, target)
                    else:
                        shutil.copy2(child, target)

                record = {
                    "run_id": run_id,
                    "fixture_id": fixture_meta["id"],
                    "fixture_sha256": observed_hash,
                    "family": fixture_meta["family"],
                    "priority": fixture_meta["priority"],
                    "trial": trial,
                    "candidate_sha": manifest["candidate_sha"],
                    "capability_profile": manifest["capability_profile"],
                    "evaluator_class": manifest["evaluator_class"],
                    "started_unix": started,
                    "duration_s": round(time.time() - started, 6),
                    "result": result,
                    "grade": grade,
                    "error": error,
                    "artifact_dir": str(artifact_dir),
                }
                append_jsonl(records, record)
                summary.append(record)

    summary_path = out_dir / "summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

    any_error = any(r["grade"]["status"] == "HARNESS_OR_EXECUTION_ERROR" for r in summary)
    return 2 if any_error else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--candidate-command", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    try:
        return run(args.manifest, args.candidate_command, args.out, args.timeout)
    except HarnessError as exc:
        print(f"HARNESS ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
