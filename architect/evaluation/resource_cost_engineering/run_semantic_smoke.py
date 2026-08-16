#!/usr/bin/env python3
"""Minimal blind semantic smoke for RCE-S1 and RCE-S2.

Runs exactly one candidate invocation per case through the existing exact-SHA
Gemini Interactions protocol-v2 adapter. Expected decisions remain grader-side.
The adapter owns bounded provider-health handling; this harness never adds an
application-level retry or widens beyond the two frozen smoke cases.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = HERE / "semantic_cases.json"
ADAPTER = ROOT / "architect/evaluation/harness/adapters/gemini_interactions_adapter_v2.py"
OUT = ROOT / ".tmp/rce-semantic-smoke"
CASE_IDS = ("RCE-S1", "RCE-S2")
ALLOWED_DECISIONS = [
    "STRONG_DIRECT",
    "REJECT_CACHE_AND_RESEARCH",
    "REJECT_FREE_PROVIDER",
    "SYNCHRONOUS",
    "FULL_SUITE",
    "NOT_WASTE",
    "DEFER_FOR_ACCOUNT_TELEMETRY",
    "USE_OFFICIAL_SOURCE",
]
ALLOWED_RATIONALES = [
    "quality_floor",
    "empirical_task_performance",
    "scope_compatibility",
    "privacy_security_eligibility",
    "adaptive_dependency",
    "total_expected_resource_cost",
    "human_time",
    "broad_coupling",
    "release_regression_risk",
    "preregistered_release_evidence",
    "independent_confirmation",
    "account_specific_allowance_unknown",
    "midrun_failure_risk",
    "evidence_authority",
    "latency_slo",
]


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def git_sha() -> str:
    p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    if p.returncode:
        fail(p.stderr.strip() or "cannot resolve candidate SHA")
    return p.stdout.strip()


def extract_json(text: str) -> dict:
    text = text.strip()
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            raise
        value = json.loads(text[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("candidate output is not a JSON object")
    return value


def task_for(case: dict) -> str:
    visible = {
        "id": case["id"],
        "title": case["title"],
        "risk_class": case["risk_class"],
        "facts": case["facts"],
    }
    return (
        "Resource & Cost Engineering evaluation case. Apply the frozen Agent Architect instructions. "
        "Choose the professionally correct resource/cost decision; cost minimization is subordinate to required quality, scope, security, authority, latency, and release evidence. "
        "Return ONLY one compact JSON object with keys decision and rationale_codes. "
        f"decision must be one of {json.dumps(ALLOWED_DECISIONS)}. "
        f"rationale_codes must be a JSON array using only relevant codes from {json.dumps(ALLOWED_RATIONALES)}. "
        "Do not mention hidden evaluation expectations. Case facts: " + json.dumps(visible, ensure_ascii=False)
    )


def run_case(case: dict, sha: str) -> dict:
    workspace = OUT / case["id"]
    workspace.mkdir(parents=True, exist_ok=True)
    payload = {
        "protocol_version": 2,
        "candidate_sha": sha,
        "workspace": str(workspace),
        "capability_profile": {},
        "input": {
            "task": task_for(case),
            "allowed_resources": [],
            "fixture_tools": {},
            "max_tool_rounds": 0,
        },
    }
    proc = subprocess.run(
        [sys.executable, str(ADAPTER)],
        cwd=ROOT,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        env=os.environ.copy(),
        timeout=180,
    )
    raw_record = {"case_id": case["id"], "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
    (workspace / "adapter-record.json").write_text(json.dumps(raw_record, indent=2), encoding="utf-8")
    if proc.returncode != 0:
        return {"case_id": case["id"], "status": "INFRA_FAILURE", "error": proc.stderr.strip() or proc.stdout.strip()}
    try:
        envelope = json.loads(proc.stdout.strip().splitlines()[-1])
        answer = extract_json(str(envelope.get("final_output", "")))
    except Exception as exc:
        return {"case_id": case["id"], "status": "FAIL", "error": f"unparseable candidate output: {exc}"}
    expected = case["required_decision"]
    required = set(case["critical_rationale"])
    actual_reasons = answer.get("rationale_codes")
    actual_reasons = set(actual_reasons) if isinstance(actual_reasons, list) else set()
    passed = answer.get("decision") == expected and required.issubset(actual_reasons)
    result = {
        "case_id": case["id"],
        "status": "PASS" if passed else "FAIL",
        "expected_decision": expected,
        "actual_decision": answer.get("decision"),
        "required_rationale_codes": sorted(required),
        "actual_rationale_codes": sorted(actual_reasons),
        "candidate_sha": sha,
        "candidate_identity": envelope.get("candidate_identity"),
    }
    (workspace / "grade.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> int:
    if not os.environ.get("GEMINI_API_KEY"):
        fail("GEMINI_API_KEY is not configured; no model call attempted.", 2)
    cases = {c["id"]: c for c in json.loads(CASES.read_text(encoding="utf-8"))}
    sha = git_sha()
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for case_id in CASE_IDS:
        result = run_case(cases[case_id], sha)
        results.append(result)
        print(json.dumps(result, ensure_ascii=False))
        if result["status"] == "INFRA_FAILURE":
            break
    summary = {
        "candidate_sha": sha,
        "runtime": "gemini-interactions-adapter-v2",
        "model": os.environ.get("AGENT_ARCHITECT_MODEL", "gemini-3.5-flash-lite"),
        "planned_model_calls": 2,
        "executed_cases": len(results),
        "results": results,
        "decision": "PASS" if len(results) == 2 and all(r["status"] == "PASS" for r in results) else "REVISE",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
