#!/usr/bin/env python3
"""Vendor-neutral runner for Agent Architect behavioral validation.

Protocol v2 adds multi-step/session orchestration and mechanical inspection of
workspace artifacts. The runner never treats a candidate's prose claim about state
or side effects as mechanical proof.
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


RUNNER_VERSION = "2"


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
    if str(manifest["runner_version"]) != RUNNER_VERSION:
        raise HarnessError(
            f"manifest runner_version={manifest['runner_version']} does not match runner {RUNNER_VERSION}"
        )
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


def deep_get(value: Any, dotted_path: str) -> tuple[bool, Any]:
    current = value
    for part in dotted_path.split(".") if dotted_path else []:
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return False, None
    return True, current


def normalized_steps(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    if "steps" in fixture:
        steps = fixture["steps"]
        if not isinstance(steps, list) or not steps:
            raise HarnessError("fixture steps must be a non-empty list")
        seen: set[str] = set()
        for index, step in enumerate(steps, 1):
            if not isinstance(step, dict):
                raise HarnessError("each fixture step must be an object")
            step_id = step.get("id", f"step-{index}")
            if step_id in seen:
                raise HarnessError(f"duplicate step id: {step_id}")
            seen.add(step_id)
            step.setdefault("id", step_id)
            if "input" not in step:
                raise HarnessError(f"step {step_id} has no input")
        return steps
    if "candidate_input" in fixture:
        return [{"id": "main", "session_id": "session-1", "input": fixture["candidate_input"]}]
    raise HarnessError("fixture has neither steps nor candidate_input")


def merge_capabilities(base: dict[str, Any], override: Any) -> dict[str, Any]:
    merged = dict(base)
    if override is not None:
        if not isinstance(override, dict):
            raise HarnessError("step capability_profile must be an object")
        merged.update(override)
    return merged


def artifact_json_get(workspace: Path, relative_path: str, json_path: str) -> tuple[bool, Any]:
    target = (workspace / relative_path).resolve()
    root = workspace.resolve()
    if root not in target.parents and target != root:
        raise HarnessError("artifact grader path escapes workspace")
    if not target.exists() or not target.is_file():
        return False, None
    try:
        data = read_json(target)
    except (json.JSONDecodeError, OSError):
        return False, None
    return deep_get(data, json_path)


def mechanical_grade(
    fixture: dict[str, Any], step_results: dict[str, Any], workspace: Path
) -> dict[str, Any]:
    """Grade public mechanically checkable invariants only.

    Hidden-key or professional-judgment grading remains external. For state/side-effect
    claims, prefer artifact checks over candidate-reported fields.
    """
    grader = fixture.get("mechanical_grader")
    if grader is None:
        return {"status": "PENDING_EXTERNAL_GRADER", "checks": []}

    context = {"steps": step_results}
    checks: list[dict[str, Any]] = []

    for check in grader.get("required_equals", []):
        field = check["field"]
        expected = check["value"]
        exists, observed = deep_get(context, field)
        checks.append(
            {
                "type": "required_equals",
                "field": field,
                "expected": expected,
                "observed": observed if exists else None,
                "pass": exists and observed == expected,
            }
        )

    for check in grader.get("required_absent", []):
        field = check["field"]
        exists, observed = deep_get(context, field)
        checks.append(
            {
                "type": "required_absent",
                "field": field,
                "observed": observed if exists else None,
                "pass": not exists,
            }
        )

    for check in grader.get("required_contains", []):
        field = check["field"]
        needle = check["value"]
        exists, observed = deep_get(context, field)
        passed = False
        if exists and isinstance(observed, (list, str, dict)):
            passed = needle in observed
        checks.append(
            {
                "type": "required_contains",
                "field": field,
                "expected_member": needle,
                "observed": observed if exists else None,
                "pass": passed,
            }
        )

    for check in grader.get("artifact_exists", []):
        rel = check["path"]
        target = (workspace / rel).resolve()
        root = workspace.resolve()
        if root not in target.parents and target != root:
            raise HarnessError("artifact_exists path escapes workspace")
        passed = target.exists()
        checks.append({"type": "artifact_exists", "path": rel, "pass": passed})

    for check in grader.get("artifact_json_equals", []):
        rel = check["path"]
        jpath = check.get("json_path", "")
        expected = check["value"]
        exists, observed = artifact_json_get(workspace, rel, jpath)
        checks.append(
            {
                "type": "artifact_json_equals",
                "path": rel,
                "json_path": jpath,
                "expected": expected,
                "observed": observed if exists else None,
                "pass": exists and observed == expected,
            }
        )

    if not checks:
        return {"status": "PENDING_EXTERNAL_GRADER", "checks": []}
    return {"status": "PASS" if all(c["pass"] for c in checks) else "FAIL", "checks": checks}


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
        steps = normalized_steps(fixture)

        per_fixture_trials = int(fixture_meta.get("trial_count", manifest["trial_count"]))
        if per_fixture_trials < 1:
            raise HarnessError("fixture trial_count must be positive")

        for trial in range(1, per_fixture_trials + 1):
            run_id = f"{fixture_meta['id']}-t{trial}"
            started = time.time()
            error = None
            step_results: dict[str, Any] = {}

            with tempfile.TemporaryDirectory(prefix=f"aa-eval-{run_id}-") as tmp:
                workspace = Path(tmp)
                try:
                    for step_index, step in enumerate(steps, 1):
                        step_id = step["id"]
                        session_id = step.get("session_id", f"session-{step_index}")
                        payload = {
                            "protocol_version": 2,
                            "operation": step.get("operation", "run"),
                            "run_id": run_id,
                            "step_id": step_id,
                            "candidate_sha": manifest["candidate_sha"],
                            "family": fixture_meta["family"],
                            "priority": fixture_meta["priority"],
                            "trial": trial,
                            "session_id": session_id,
                            "reset_session": bool(step.get("reset_session", False)),
                            "capability_profile": merge_capabilities(
                                manifest["capability_profile"], step.get("capability_profile")
                            ),
                            "input": step["input"],
                            "workspace": str(workspace),
                        }
                        result = invoke_candidate(candidate_command, payload, timeout_s)
                        identity = result.get("candidate_identity", {})
                        if identity.get("sha") != manifest["candidate_sha"]:
                            raise HarnessError(
                                f"step {step_id} did not verify candidate SHA: "
                                f"expected {manifest['candidate_sha']}, observed {identity.get('sha')}"
                            )
                        step_results[step_id] = result

                    grade = mechanical_grade(fixture, step_results, workspace)
                except (HarnessError, subprocess.TimeoutExpired) as exc:
                    error = str(exc)
                    grade = {"status": "HARNESS_OR_EXECUTION_ERROR", "checks": []}

                artifact_dir = out_dir / "artifacts" / run_id
                artifact_dir.mkdir(parents=True, exist_ok=True)
                for child in workspace.iterdir():
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
                    "steps": step_results,
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
    any_fail = any(r["grade"]["status"] == "FAIL" for r in summary)
    if any_error:
        return 2
    if any_fail:
        return 1
    return 0


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
