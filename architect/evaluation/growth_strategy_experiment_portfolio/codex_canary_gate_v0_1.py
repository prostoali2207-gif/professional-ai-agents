#!/usr/bin/env python3
"""Run the frozen, unscored issue-198 isolation/calibration/candidate canary gates.

This script never opens the sealed pack and has no scored-run entry point.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

import codex_judge_adapter_v0_1 as judge_transport
import sealed_runner_codex_v0_1 as runner

MIGRATION_ID = "strategist-v0.1-codex-subscription-migration-2026-08-30"
EXPECTED_CANDIDATE_COMMIT = "1c042d09695dfe2d4186c21d136474dc9d1fbdd9"
EXPECTED_CANDIDATE_DIGEST = "sha256:59dd74cb772f1259a7ed5f6b9da4aa40db7f48be21c380b605bdc044f4dd7b92"
ALLOWED_CANARY_DECISIONS = {"TEST", "RESEARCH_REQUIRED", "BLOCKED", "CONTINUE", "INCONCLUSIVE", "HANDOFF"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def run_checked(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(command, text=True, capture_output=True, **kwargs)
    if proc.returncode != 0:
        raise RuntimeError(f"command failed ({proc.returncode}): {command[0]}: {proc.stderr[-1200:]}")
    return proc


def sandbox_principal() -> str:
    domain = os.environ.get("USERDOMAIN", "").strip()
    if not domain:
        raise RuntimeError("USERDOMAIN is unavailable")
    return f"{domain}\\CodexSandboxOffline"


def acl_text(path: Path) -> str:
    return run_checked(["icacls", str(path)]).stdout


def deny_read(path: Path, principal: str) -> None:
    before = acl_text(path).lower()
    if principal.lower() in before and "(deny)" in before:
        raise RuntimeError(f"pre-existing deny ACE for sandbox principal at {path}")
    run_checked(["icacls", str(path), "/deny", f"{principal}:(OI)(CI)(RX)"])


def remove_deny(path: Path, principal: str) -> None:
    run_checked(["icacls", str(path), "/remove:d", principal])


def quote_ps(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def isolation_probe(candidate_root: Path, denied_roots: list[Path], profile: str) -> dict[str, Any]:
    checks = []
    for index, path in enumerate(denied_roots):
        checks.append(
            f"$r{index}=try{{Get-ChildItem -LiteralPath {quote_ps(str(path))} -ErrorAction Stop|Select-Object -First 1|Out-Null;'READABLE'}}catch{{'DENIED'}}"
        )
    properties = ";".join(f"root_{i}=$r{i}" for i in range(len(denied_roots)))
    script = (
        f"$inside=try{{Get-ChildItem -LiteralPath {quote_ps(str(candidate_root))} -ErrorAction Stop|Out-Null;'READABLE'}}catch{{'DENIED'}};"
        + ";".join(checks)
        + f";[Console]::Out.Write((@{{inside=$inside;{properties}}}|ConvertTo-Json -Compress))"
    )
    proc = run_checked([
        "codex", "sandbox", "-p", profile, "-P", "candidate", "-C", str(candidate_root),
        "powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script,
    ])
    observed = json.loads(proc.stdout)
    if observed.get("inside") != "READABLE":
        raise RuntimeError("candidate workspace is not readable to the sandbox")
    if any(observed.get(f"root_{i}") != "DENIED" for i in range(len(denied_roots))):
        raise RuntimeError(f"candidate boundary denial failed: {observed}")
    return {"status": "PASS", "observed": observed, "sandbox_principal": sandbox_principal()}


def judge_command(python: Path, adapter: Path, model: str) -> str:
    return f"{python.as_posix()} {adapter.as_posix()} --model {model} --timeout 600"


def sanitized_envelope(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": str(value.get("stage", "unknown"))[:80],
        "returncode": value.get("returncode"),
        "classification": str(value.get("classification", "UNKNOWN_TECHNICAL"))[:80],
        "stdout_tail": judge_transport.sanitize_tail(str(value.get("stdout_tail", ""))),
        "stderr_tail": judge_transport.sanitize_tail(str(value.get("stderr_tail", ""))),
    }


def calibrate_with_bounded_retry(command: str, model: str, retry: dict[str, int], attempts: list[dict[str, Any]]) -> None:
    attempt = 0
    while True:
        attempt += 1
        try:
            passed = runner.calibrate(command, model)
        except runner.IsolatedRuntimeError as exc:
            envelope = sanitized_envelope(exc.envelope)
            attempts.append({"model": model, "attempt": attempt, "outcome": "TECHNICAL_FAILURE", "failure_envelope": envelope})
            if envelope["classification"] == "TRANSIENT_TRANSPORT" and retry["remaining"] > 0:
                retry["remaining"] -= 1
                time.sleep(5)
                continue
            raise RuntimeError(f"calibration technical failure: {model}") from exc
        attempts.append({"model": model, "attempt": attempt, "outcome": "PASS" if passed else "CALIBRATION_MISMATCH"})
        if not passed:
            raise RuntimeError(f"public calibration mismatch: {model}")
        return


def verify_judge_isolation(transports: list[dict[str, Any]]) -> dict[str, Any]:
    if len(transports) != 2:
        raise RuntimeError("judge isolation requires exactly two successful calibration transports")
    expected = {"gpt-5.6-sol", "gpt-5.6-terra"}
    if {row.get("model") for row in transports} != expected or any(row.get("mode") != "calibration" for row in transports):
        raise RuntimeError("judge identity or calibration-mode isolation mismatch")
    details = [row.get("transport") or {} for row in transports]
    threads = [row.get("thread_id") for row in details]
    workspaces = [row.get("workspace_digest") for row in details]
    if any(not value for value in threads + workspaces) or len(set(threads)) != 2 or len(set(workspaces)) != 2:
        raise RuntimeError("judges did not use distinct ephemeral threads and workspaces")
    for transport in details:
        event_types = transport.get("event_types") or []
        if any("tool" in str(kind).lower() or "command" in str(kind).lower() or "file_change" in str(kind).lower() for kind in event_types):
            raise RuntimeError("judge isolation observed a forbidden event")
    return {"status": "PASS", "distinct_threads": 2, "distinct_ephemeral_workspaces": 2, "tool_free": True}


def verify_candidate_canary(raw: dict[str, Any]) -> dict[str, Any]:
    identity = raw.get("candidate_identity") or {}
    if raw.get("status") != "completed":
        raise RuntimeError("candidate canary did not complete")
    if identity.get("commit") != EXPECTED_CANDIDATE_COMMIT or identity.get("digest") != EXPECTED_CANDIDATE_DIGEST:
        raise RuntimeError("candidate canary identity mismatch")
    answer = json.loads(raw["final_output"])
    if answer.get("decision") not in ALLOWED_CANARY_DECISIONS:
        raise RuntimeError(f"canary made unsafe decision {answer.get('decision')!r}")
    statuses = {item.get("status") for item in answer.get("evidence", []) if isinstance(item, dict)}
    if not statuses or not statuses.issubset({"FACT", "OBSERVATION", "INFERENCE", "HYPOTHESIS", "UNRESOLVED"}):
        raise RuntimeError("candidate evidence contract is invalid")
    observable = raw.get("observable") or {}
    if any(observable.get(key) for key in ("tool_calls", "state_events", "side_effects")):
        raise RuntimeError("candidate canary was not stateless/tool-free")
    transport = raw.get("transport") or {}
    if any("tool" in str(kind).lower() or "command" in str(kind).lower() for kind in transport.get("event_types", [])):
        raise RuntimeError("candidate transport contains a forbidden tool event")
    return {
        "status": "PASS",
        "decision": answer["decision"],
        "output_digest": digest_bytes(json.dumps(answer, ensure_ascii=False, sort_keys=True).encode()),
        "transport": transport,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--candidate-root", required=True)
    parser.add_argument("--deny-root", action="append", required=True)
    parser.add_argument("--profile", default="p198-candidate")
    parser.add_argument("--python", required=True)
    parser.add_argument("--record", required=True)
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    candidate_root = Path(args.candidate_root).resolve()
    denied_roots = [Path(value).resolve() for value in args.deny_root]
    if not candidate_root.is_dir() or any(not path.exists() for path in denied_roots):
        raise RuntimeError("candidate or denied root is unavailable")
    if any(candidate_root == path or candidate_root.is_relative_to(path) for path in denied_roots):
        raise RuntimeError("candidate root overlaps a denied root")

    addendum = repo / "architect/evaluation/growth_strategy_experiment_portfolio/qualification-codex-migration-schema-repair-v0.3.json"
    candidate_adapter = repo / "architect/evaluation/growth_strategy_experiment_portfolio/codex_candidate_adapter_v0_1.py"
    judge_adapter = repo / "architect/evaluation/growth_strategy_experiment_portfolio/codex_judge_adapter_v0_1.py"
    python = Path(args.python).resolve()
    record: dict[str, Any] = {
        "migration_id": MIGRATION_ID,
        "started_utc": now(),
        "freeze_commit": run_checked(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip(),
        "repair_addendum_git_blob": run_checked(["git", "rev-parse", f"HEAD:{addendum.relative_to(repo).as_posix()}"], cwd=repo).stdout.strip(),
        "codex_cli_version": run_checked(["codex", "--version"]).stdout.strip(),
        "provider": "codex-subscription-chatgpt-auth",
        "pre_run_budget": {"maximum_model_calls": 4, "judge_calibration_initial_batches": 2, "shared_transient_transport_retry": 1, "candidate_canary": 1, "scored_calls_authorized": 0, "on_quota_or_nonretryable_failure": "STOP"},
        "retry_policy": {"shared_retry_budget": 1, "eligible_classification": "TRANSIENT_TRANSPORT", "backoff_seconds": 5, "candidate_retry_budget": 0, "professional_or_calibration_mismatch_retry_budget": 0},
        "denied_roots": [digest_bytes(str(path).encode()) for path in denied_roots],
    }
    principal = sandbox_principal()
    applied: list[Path] = []
    try:
        runner.JUDGE_TRANSPORTS.clear()
        retry = {"remaining": 1}
        attempts: list[dict[str, Any]] = []
        calibrate_with_bounded_retry(judge_command(python, judge_adapter, "gpt-5.6-sol"), "gpt-5.6-sol", retry, attempts)
        calibrate_with_bounded_retry(judge_command(python, judge_adapter, "gpt-5.6-terra"), "gpt-5.6-terra", retry, attempts)
        record["calibration"] = {"status": "PASS", "attempts": attempts, "shared_retry_used": 1 - retry["remaining"], "transports": runner.JUDGE_TRANSPORTS.copy()}
        record["judge_isolation"] = verify_judge_isolation(runner.JUDGE_TRANSPORTS)

        for path in denied_roots:
            deny_read(path, principal)
            applied.append(path)
        record["isolation_canary"] = isolation_probe(candidate_root, denied_roots, args.profile)

        child_env = os.environ.copy()
        child_env["STRATEGIST_CODEX_CANDIDATE_ROOT"] = str(candidate_root)
        proc = run_checked([str(python), str(candidate_adapter), "--canary", "--model", "gpt-5.6-terra", "--timeout", "300"], cwd=repo, env=child_env, timeout=360)
        record["candidate_canary"] = verify_candidate_canary(json.loads(proc.stdout))
        record["verdict"] = "READY_FOR_SCORED_AUTHORIZATION"
    except Exception as exc:
        record["verdict"] = "CANARY_GATE_FAIL_STOPPED"
        record["error_class"] = type(exc).__name__
        if "attempts" in locals() and "calibration" not in record:
            record["calibration"] = {"status": "FAIL", "attempts": attempts, "shared_retry_used": 1 - retry["remaining"]}
        raise
    finally:
        cleanup_errors = []
        for path in reversed(applied):
            try:
                remove_deny(path, principal)
            except Exception as cleanup_exc:
                cleanup_errors.append(f"{path}: {type(cleanup_exc).__name__}")
        record["acl_cleanup"] = ("PASS" if applied else "NOT_APPLICABLE") if not cleanup_errors else {"status": "FAIL", "errors": cleanup_errors}
        record["ended_utc"] = now()
        Path(args.record).write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if record["acl_cleanup"] != "PASS":
        raise RuntimeError("candidate boundary ACL cleanup failed")
    print(json.dumps({"verdict": record["verdict"], "record": args.record}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
