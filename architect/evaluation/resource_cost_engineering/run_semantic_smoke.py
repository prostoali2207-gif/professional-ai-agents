#!/usr/bin/env python3
"""Blind structured semantic evaluator for frozen RCE cases.

Default scope is exactly RCE-S1 and RCE-S2. The candidate sees only frozen
Agent Architect/RCE instructions plus case facts; required decisions and
rationale codes remain grader-side. The evaluator uses a tool-free Gemini
Interactions call with schema-bound JSON output and no application retry.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = HERE / "semantic_cases.json"
OUT = ROOT / ".tmp/rce-semantic-smoke"
INTERACTIONS_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
DEFAULT_CASE_IDS = ("RCE-S1", "RCE-S2")
ALL_CASE_IDS = tuple(f"RCE-S{i}" for i in range(1, 11))
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


def selected_case_ids(raw: str | None = None) -> tuple[str, ...]:
    raw = os.environ.get("RCE_SEMANTIC_CASE_IDS", "") if raw is None else raw
    if not raw.strip():
        return DEFAULT_CASE_IDS
    values = tuple(x.strip() for x in raw.split(",") if x.strip())
    if not values or len(values) != len(set(values)):
        raise ValueError("RCE_SEMANTIC_CASE_IDS must contain unique frozen case ids")
    unknown = [x for x in values if x not in ALL_CASE_IDS]
    if unknown:
        raise ValueError(f"unknown RCE semantic case ids: {','.join(unknown)}")
    return values


def frozen_instruction_source() -> str:
    paths = [
        ROOT / "architect/SKILL.md",
        ROOT / "architect/methodology/resource-cost-engineering.md",
    ]
    return "\n\n".join(
        f"--- {p.relative_to(ROOT)} ---\n{p.read_text(encoding='utf-8')}" for p in paths
    )


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
        "Return only the schema-defined decision object. Do not mention hidden evaluation expectations. Case facts: "
        + json.dumps(visible, ensure_ascii=False)
    )


def output_json_schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "decision": {"type": "string", "enum": ALLOWED_DECISIONS},
            "rationale_codes": {
                "type": "array",
                "items": {"type": "string", "enum": ALLOWED_RATIONALES},
                "minItems": 1,
                "uniqueItems": True,
            },
        },
        "required": ["decision", "rationale_codes"],
        "additionalProperties": False,
    }


def interaction_payload(case: dict, system: str, model: str) -> dict:
    payload = {
        "model": model,
        "input": task_for(case),
        "system_instruction": system,
        "response_format": {
            "type": "text",
            "mime_type": "application/json",
            "schema": output_json_schema(),
        },
        "store": False,
    }
    thinking = os.environ.get("GEMINI_THINKING_LEVEL", "").strip().lower()
    if thinking:
        if thinking not in {"minimal", "low", "medium", "high"}:
            raise ValueError(f"unsupported GEMINI_THINKING_LEVEL: {thinking}")
        payload["generation_config"] = {"thinking_level": thinking}
    return payload


def extract_output_text(raw: dict) -> str:
    if isinstance(raw.get("output_text"), str):
        return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        content = step.get("content")
        if isinstance(content, str):
            return content
        for item in content or []:
            if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str):
                return item["text"]
    raise ValueError("interaction response contains no observable text model_output")


def classify_http_error(code: int, body: str) -> str:
    low = body.lower()
    if code == 429 and ("quota" in low or "resource_exhausted" in low or "rate" in low):
        return "QUOTA_OR_RATE_LIMIT"
    if code == 503:
        return "CAPACITY_TRANSIENT"
    if code in {401, 403}:
        return "AUTH_CONFIG"
    if code == 404 and "model" in low:
        return "MODEL_LIFECYCLE_OR_ENDPOINT"
    return f"HTTP_{code}"


def call_gemini(case: dict, system: str) -> tuple[dict | None, dict]:
    key = os.environ["GEMINI_API_KEY"]
    model = os.environ.get("AGENT_ARCHITECT_MODEL", "gemini-3.5-flash-lite")
    try:
        payload = interaction_payload(case, system, model)
    except ValueError as exc:
        return None, {"status": "HARNESS_FAILURE", "failure_class": "INVALID_CONFIG", "error": str(exc), "model": model}
    req = urllib.request.Request(
        INTERACTIONS_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            raw = json.loads(response.read().decode("utf-8"))
        answer = json.loads(extract_output_text(raw).strip())
        if not isinstance(answer, dict):
            raise ValueError("candidate output is not a JSON object")
        transport = {
            "status": "OK",
            "api": "interactions/v1beta",
            "model": model,
            "interaction_id": raw.get("id"),
            "interaction_status": raw.get("status"),
            "usage": raw.get("usage") or raw.get("usageMetadata"),
        }
        return answer, transport
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        return None, {
            "status": "INFRA_FAILURE",
            "api": "interactions/v1beta",
            "http_status": exc.code,
            "failure_class": classify_http_error(exc.code, body),
            "error": body[:4000],
            "model": model,
        }
    except (json.JSONDecodeError, ValueError) as exc:
        return None, {
            "status": "EVAL_OUTPUT_FAILURE",
            "api": "interactions/v1beta",
            "failure_class": "SCHEMA_OUTPUT_PARSE",
            "error": repr(exc),
            "model": model,
        }
    except Exception as exc:
        return None, {
            "status": "INFRA_FAILURE",
            "api": "interactions/v1beta",
            "failure_class": "TRANSPORT_OR_PROVIDER_RESPONSE",
            "error": repr(exc),
            "model": model,
        }


def run_case(case: dict, sha: str, system: str) -> dict:
    workspace = OUT / case["id"]
    workspace.mkdir(parents=True, exist_ok=True)
    answer, transport = call_gemini(case, system)
    (workspace / "provider-record.json").write_text(
        json.dumps(transport, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if answer is None:
        status = "FAIL" if transport.get("status") == "EVAL_OUTPUT_FAILURE" else transport.get("status", "INFRA_FAILURE")
        return {"case_id": case["id"], "status": status, "candidate_sha": sha, **transport}
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
        "candidate_identity": {
            "sha": sha,
            "runtime": "gemini-interactions-structured-evaluator-v1",
            "model": transport.get("model"),
        },
        "interaction_id": transport.get("interaction_id"),
        "usage": transport.get("usage"),
    }
    (workspace / "grade.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result


def main() -> int:
    if not os.environ.get("GEMINI_API_KEY"):
        fail("GEMINI_API_KEY is not configured; no model call attempted.", 2)
    try:
        case_ids = selected_case_ids()
    except ValueError as exc:
        fail(str(exc), 2)
    cases = {c["id"]: c for c in json.loads(CASES.read_text(encoding="utf-8"))}
    sha = git_sha()
    system = frozen_instruction_source()
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for case_id in case_ids:
        result = run_case(cases[case_id], sha, system)
        results.append(result)
        print(json.dumps(result, ensure_ascii=False))
        if result["status"] in {"INFRA_FAILURE", "HARNESS_FAILURE"}:
            break
    semantic_pass = len(results) == len(case_ids) and all(r["status"] == "PASS" for r in results)
    summary = {
        "candidate_sha": sha,
        "runtime": "gemini-interactions-structured-evaluator-v1",
        "model": os.environ.get("AGENT_ARCHITECT_MODEL", "gemini-3.5-flash-lite"),
        "selected_case_ids": list(case_ids),
        "planned_model_calls": len(case_ids),
        "executed_cases": len(results),
        "application_retries": 0,
        "results": results,
        "decision": "PASS" if semantic_pass else "REVISE_OR_INFRA_BLOCK",
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if semantic_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
