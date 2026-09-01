#!/usr/bin/env python3
"""Issue-211 candidate-only isolation and exact unscored canary gate.

No judge, hidden fixture, grader, or scored-run entry point exists here.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from typing import Any

import codex_candidate_adapter_v0_1 as candidate_transport
import codex_canary_gate_v0_1 as prior_gate

MIGRATION_ID = "strategist-v0.1-codex-subscription-migration-2026-08-30"
ISSUE_ID = 211


class CandidateInvocationFailure(RuntimeError):
    def __init__(self, envelope: dict[str, Any]):
        super().__init__("candidate invocation failed")
        self.envelope = sanitize_envelope(envelope)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def run_checked(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(command, text=True, capture_output=True, **kwargs)
    if proc.returncode != 0:
        raise RuntimeError(f"deterministic command failed ({proc.returncode}): {command[0]}")
    return proc


def sanitize_envelope(value: dict[str, Any]) -> dict[str, Any]:
    diagnostics = value.get("stdout_diagnostics") if isinstance(value.get("stdout_diagnostics"), dict) else {}
    summaries = diagnostics.get("error_summaries") if isinstance(diagnostics.get("error_summaries"), list) else []
    clean_summaries = []
    for item in summaries[-4:]:
        if isinstance(item, dict):
            clean_summaries.append({
                str(key)[:80]: candidate_transport.sanitize_diagnostic(str(raw), (), 600)
                for key, raw in item.items()
            })
    return {
        "stage": str(value.get("stage", "unknown"))[:80],
        "returncode": value.get("returncode") if isinstance(value.get("returncode"), int) or value.get("returncode") is None else None,
        "classification": str(value.get("classification", "UNKNOWN_TECHNICAL"))[:80],
        "stdout_diagnostics": {
            "event_types": [str(item)[:80] for item in (diagnostics.get("event_types") or [])[-32:]],
            "error_summaries": clean_summaries,
            "unparsed_line_count": int(diagnostics.get("unparsed_line_count", 0)),
            "unparsed_digest": str(diagnostics.get("unparsed_digest", ""))[:80],
            "byte_count": int(diagnostics.get("byte_count", 0)),
        },
        "stderr_tail": candidate_transport.sanitize_diagnostic(str(value.get("stderr_tail", ""))),
        "stderr_byte_count": int(value.get("stderr_byte_count", 0)),
    }


def invoke_candidate_once(command: list[str], *, cwd: Path, env: dict[str, str], timeout: int) -> dict[str, Any]:
    proc = subprocess.run(command, text=True, capture_output=True, cwd=cwd, env=env, timeout=timeout)
    if proc.returncode != 0:
        try:
            parsed = json.loads(proc.stdout)
        except json.JSONDecodeError:
            parsed = {}
        envelope = parsed.get("failure_envelope") if isinstance(parsed, dict) else None
        if not isinstance(envelope, dict):
            envelope = candidate_transport.candidate_failure_envelope(
                proc.returncode, proc.stdout, proc.stderr, stage="candidate_launcher",
            )
        raise CandidateInvocationFailure(envelope)
    try:
        value = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise CandidateInvocationFailure(candidate_transport.candidate_failure_envelope(
            proc.returncode, proc.stdout, proc.stderr, stage="candidate_launcher_output",
            forced_classification="RUNTIME_OUTPUT",
        )) from exc
    if not isinstance(value, dict) or value.get("status") != "completed":
        raise CandidateInvocationFailure(candidate_transport.candidate_failure_envelope(
            proc.returncode, proc.stdout, proc.stderr, stage="candidate_launcher_status",
            forced_classification="RUNTIME_OUTPUT",
        ))
    return value


def run_candidate_with_bounded_retry(
    command: list[str], *, cwd: Path, env: dict[str, str], retry: dict[str, int],
    attempts: list[dict[str, Any]], timeout: int,
) -> dict[str, Any]:
    attempt = 0
    while True:
        attempt += 1
        try:
            value = invoke_candidate_once(command, cwd=cwd, env=env, timeout=timeout)
        except CandidateInvocationFailure as exc:
            envelope = exc.envelope
            attempts.append({
                "attempt": attempt,
                "outcome": "TECHNICAL_FAILURE",
                "model_call_attempted": envelope["stage"].startswith("codex_exec"),
                "failure_envelope": envelope,
            })
            if envelope["classification"] == "TRANSIENT_TRANSPORT" and retry["remaining"] > 0:
                retry["remaining"] -= 1
                time.sleep(5)
                continue
            raise RuntimeError("candidate canary technical failure") from exc
        attempts.append({"attempt": attempt, "outcome": "COMPLETED", "model_call_attempted": True})
        return value


def verify_reused_judge_evidence(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("freeze_commit") != "d746571fe7f9b658bf24dc8421045753e7199712":
        raise RuntimeError("reused judge evidence freeze identity mismatch")
    if (value.get("calibration") or {}).get("status") != "PASS" or (value.get("judge_isolation") or {}).get("status") != "PASS":
        raise RuntimeError("reused public calibration or judge isolation did not pass")
    return {
        "status": "PASS_REUSED_UNCHANGED_JUDGE_LAYER",
        "evidence_digest": digest_bytes(path.read_bytes()),
        "evidence_freeze_commit": value["freeze_commit"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--candidate-root", required=True)
    parser.add_argument("--deny-root", action="append", required=True)
    parser.add_argument("--profile", default="p211-candidate")
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

    addendum = repo / "architect/evaluation/growth_strategy_experiment_portfolio/qualification-codex-candidate-transport-repair-v0.4.json"
    audit = repo / "architect/evaluation/growth_strategy_experiment_portfolio/qualification-codex-candidate-transport-independent-audit-v0.4.json"
    reused = repo / "architect/evaluation/growth_strategy_experiment_portfolio/qualification-codex-canary-record-v0.3.json"
    adapter = repo / "architect/evaluation/growth_strategy_experiment_portfolio/codex_candidate_adapter_v0_1.py"
    python = Path(args.python).resolve()
    record: dict[str, Any] = {
        "issue": ISSUE_ID,
        "migration_id": MIGRATION_ID,
        "started_utc": now(),
        "freeze_commit": run_checked(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip(),
        "addendum_git_blob": run_checked(["git", "rev-parse", f"HEAD:{addendum.relative_to(repo).as_posix()}"], cwd=repo).stdout.strip(),
        "audit_git_blob": run_checked(["git", "rev-parse", f"HEAD:{audit.relative_to(repo).as_posix()}"], cwd=repo).stdout.strip(),
        "candidate_adapter_git_blob": run_checked(["git", "rev-parse", f"HEAD:{adapter.relative_to(repo).as_posix()}"], cwd=repo).stdout.strip(),
        "provider": "codex-subscription-chatgpt-auth",
        "pre_run_budget": {
            "initial_candidate_canary_calls": 1,
            "transient_transport_retry_reserve": 1,
            "maximum_candidate_model_call_attempts": 2,
            "scored_calls_authorized": 0,
            "separately_billed_api_calls_authorized": 0,
        },
        "retry_policy": {
            "maximum_attempts": 2,
            "eligible_classification": "TRANSIENT_TRANSPORT",
            "backoff_seconds": 5,
            "original_failure_retained": True,
        },
        "denied_roots": [digest_bytes(str(path).encode()) for path in denied_roots],
        "reused_judge_evidence": verify_reused_judge_evidence(reused),
        "FACT": [], "BLOCKER": None, "VERDICT": "RUNNING", "NEXT_ACTION": None,
    }
    principal = prior_gate.sandbox_principal()
    applied: list[Path] = []
    attempts: list[dict[str, Any]] = []
    retry = {"remaining": 1}
    try:
        for path in denied_roots:
            prior_gate.deny_read(path, principal)
            applied.append(path)
        record["candidate_isolation"] = prior_gate.isolation_probe(candidate_root, denied_roots, args.profile)

        child_env = os.environ.copy()
        child_env["STRATEGIST_CODEX_CANDIDATE_ROOT"] = str(candidate_root)
        raw = run_candidate_with_bounded_retry(
            [str(python), str(adapter), "--canary", "--model", "gpt-5.6-terra", "--timeout", "300"],
            cwd=repo, env=child_env, retry=retry, attempts=attempts, timeout=360,
        )
        record["candidate_canary"] = prior_gate.verify_candidate_canary(raw)
        record["FACT"] = ["candidate isolation PASS", "exact unscored candidate canary PASS"]
        record["VERDICT"] = "READY_FOR_SCORED_AUTHORIZATION"
        record["NEXT_ACTION"] = "Obtain separate evaluator authorization before any scored qualification."
    except Exception as exc:
        record["BLOCKER"] = {"error_class": type(exc).__name__, "gate": "candidate isolation" if "candidate_isolation" not in record else "exact unscored candidate canary"}
        record["VERDICT"] = "CANARY_GATE_FAIL_STOPPED"
        record["NEXT_ACTION"] = "Repair only the narrow evidenced blocker under a new frozen addendum; do not retry this run."
        raise
    finally:
        record["candidate_attempts"] = attempts
        record["post_run_accounting"] = {
            "candidate_process_attempts": len(attempts),
            "candidate_model_call_attempts": sum(bool(row.get("model_call_attempted")) for row in attempts),
            "retry_count": 1 - retry["remaining"],
            "completed_candidate_results": sum(row.get("outcome") == "COMPLETED" for row in attempts),
            "scored_calls": 0,
            "separately_billed_api_calls": 0,
        }
        cleanup_errors = []
        for path in reversed(applied):
            try:
                prior_gate.remove_deny(path, principal)
            except Exception as cleanup_exc:
                cleanup_errors.append({"root_digest": digest_bytes(str(path).encode()), "error_class": type(cleanup_exc).__name__})
        record["cleanup"] = "PASS" if not cleanup_errors else {"status": "FAIL", "errors": cleanup_errors}
        record["ended_utc"] = now()
        Path(args.record).write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if record["cleanup"] != "PASS":
        raise RuntimeError("candidate boundary ACL cleanup failed")
    print(json.dumps({"verdict": record["VERDICT"], "record": args.record}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
