#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = HERE / "semantic_cases.json"
ADAPTER = ROOT / "architect/evaluation/harness/adapters/openai_responses_adapter_v2.py"
OUT = ROOT / ".tmp/research-rce-semantic-smoke"
CASE_IDS = ("RES-RCE-S1", "RES-RCE-S2")
ALLOWED_DECISIONS = ["ESCALATE_OR_DEFER", "DIRECT_PRIMARY_INSPECTION", "CONTINUE", "STOP_WITH_LIMITATION", "SUPPORTED"]
ALLOWED_RATIONALES = [
    "unknown_dependence_not_independence",
    "protected_reserve",
    "no_false_support",
    "known_official_url",
    "cheapest_sufficient_eligible_route",
    "no_blind_retry",
    "provider_health_or_quota",
    "citation_entailment",
    "high_stakes_threshold",
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
    visible = {"id": case["id"], "title": case["title"], "facts": case["facts"]}
    return (
        "Research Evidence Engineering + Resource & Cost Engineering evaluation case. "
        "Apply the frozen Agent Architect instructions and available methodology resources. "
        "Evidence quality and high-stakes thresholds must not be weakened because budget or quota is exhausted. "
        "Return ONLY one compact JSON object with keys decision and rationale_codes. "
        f"decision must be one of {json.dumps(ALLOWED_DECISIONS)}. "
        f"rationale_codes must be a JSON array using only relevant codes from {json.dumps(ALLOWED_RATIONALES)}. "
        "Do not mention hidden expectations. Case facts: " + json.dumps(visible, ensure_ascii=False)
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
            "allowed_resources": [
                "architect/methodology/evidence-validity-comparability.md",
                "architect/methodology/resource-cost-engineering.md"
            ],
            "fixture_tools": {},
            "max_tool_rounds": 4,
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
    raw = {"case_id": case["id"], "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
    (workspace / "adapter-record.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
    if proc.returncode != 0:
        return {"case_id": case["id"], "status": "INFRA_FAILURE", "error": proc.stderr.strip() or proc.stdout.strip()}
    try:
        envelope = json.loads(proc.stdout.strip().splitlines()[-1])
        answer = extract_json(str(envelope.get("final_output", "")))
    except Exception as exc:
        return {"case_id": case["id"], "status": "FAIL", "error": f"unparseable candidate output: {exc}"}
    required = set(case["critical_rationale"])
    reasons = answer.get("rationale_codes")
    reasons = set(reasons) if isinstance(reasons, list) else set()
    passed = answer.get("decision") == case["required_decision"] and required.issubset(reasons)
    result = {
        "case_id": case["id"],
        "status": "PASS" if passed else "FAIL",
        "expected_decision": case["required_decision"],
        "actual_decision": answer.get("decision"),
        "required_rationale_codes": sorted(required),
        "actual_rationale_codes": sorted(reasons),
        "candidate_sha": sha,
        "candidate_identity": envelope.get("candidate_identity"),
    }
    (workspace / "grade.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        fail("OPENAI_API_KEY is not configured; no model call attempted.", 2)
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
        "model": os.environ.get("AGENT_ARCHITECT_MODEL", "gpt-5.4-mini"),
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
