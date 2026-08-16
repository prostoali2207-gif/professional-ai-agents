#!/usr/bin/env python3
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
OUT = ROOT / ".tmp/research-rce-semantic-smoke"
INTERACTIONS_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
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


def selected_case_ids(raw: str | None = None) -> tuple[str, ...]:
    raw = os.environ.get("SEMANTIC_CASE_IDS", "") if raw is None else raw
    if not raw.strip():
        return CASE_IDS
    requested = tuple(x.strip() for x in raw.split(",") if x.strip())
    if not requested or len(set(requested)) != len(requested):
        raise ValueError("SEMANTIC_CASE_IDS must contain unique frozen case ids")
    unknown = [x for x in requested if x not in CASE_IDS]
    if unknown:
        raise ValueError(f"unknown semantic case ids: {','.join(unknown)}")
    return requested


def extract_json(text: str) -> dict:
    value = json.loads(text.strip())
    if not isinstance(value, dict):
        raise ValueError("candidate output is not a JSON object")
    return value


def frozen_instruction_source() -> str:
    paths = [
        ROOT / "architect/SKILL.md",
        ROOT / "architect/methodology/evidence-validity-comparability.md",
        ROOT / "architect/methodology/resource-cost-engineering.md",
    ]
    return "\n\n".join(f"--- {p.relative_to(ROOT)} ---\n{p.read_text(encoding='utf-8')}" for p in paths)


def task_for(case: dict) -> str:
    visible = {"id": case["id"], "title": case["title"], "facts": case["facts"]}
    return (
        "Research Evidence Engineering + Resource & Cost Engineering evaluation case. "
        "Apply the frozen Agent Architect instructions. Evidence quality and high-stakes thresholds must not be weakened because budget or quota is exhausted. "
        "Return only the schema-defined decision object. Do not mention hidden expectations. Case facts: "
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
            },
        },
        "required": ["decision", "rationale_codes"],
        "additionalProperties": False,
    }


def response_format() -> dict:
    return {"type": "text", "mime_type": "application/json", "schema": output_json_schema()}


def interaction_payload(case: dict, system: str, model: str) -> dict:
    return {
        "model": model,
        "input": task_for(case),
        "system_instruction": system,
        "response_format": response_format(),
        "store": False,
    }


def extract_interaction_output_text(raw: dict) -> str:
    for step in reversed(raw.get("steps") or []):
        if step.get("type") != "model_output":
            continue
        for item in step.get("content") or []:
            if item.get("type") == "text" and isinstance(item.get("text"), str):
                return item["text"]
    if isinstance(raw.get("output_text"), str):
        return raw["output_text"]
    raise ValueError("interaction response contains no observable text model_output")


def classify_http_error(code: int, body: str) -> str:
    low = body.lower()
    if code == 429 and ("quota" in low or "resource_exhausted" in low):
        return "DAILY_QUOTA_OR_RATE_LIMIT"
    if code == 503:
        return "CAPACITY_TRANSIENT"
    if code in {401, 403}:
        return "AUTH_CONFIG"
    if code == 404 and "model" in low:
        return "MODEL_LIFECYCLE_OR_ENDPOINT"
    return f"HTTP_{code}"


def call_gemini(case: dict, system: str) -> tuple[dict | None, dict]:
    key = os.environ["GEMINI_API_KEY"]
    model = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
    payload = interaction_payload(case, system, model)
    req = urllib.request.Request(
        INTERACTIONS_ENDPOINT,
        data=json.dumps(payload).encode(),
        method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            raw = json.loads(response.read().decode())
        text = extract_interaction_output_text(raw)
        answer = extract_json(text)
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
        return None, {"status": "INFRA_FAILURE", "api": "interactions/v1beta", "http_status": exc.code, "failure_class": classify_http_error(exc.code, body), "error": body, "model": model}
    except json.JSONDecodeError as exc:
        return None, {"status": "EVAL_OUTPUT_FAILURE", "api": "interactions/v1beta", "failure_class": "SCHEMA_OUTPUT_PARSE", "error": repr(exc), "model": model}
    except Exception as exc:
        return None, {"status": "INFRA_FAILURE", "api": "interactions/v1beta", "failure_class": "TRANSPORT_OR_PROVIDER_RESPONSE", "error": repr(exc), "model": model}


def run_case(case: dict, sha: str, system: str) -> dict:
    workspace = OUT / case["id"]
    workspace.mkdir(parents=True, exist_ok=True)
    answer, transport = call_gemini(case, system)
    (workspace / "provider-record.json").write_text(json.dumps(transport, ensure_ascii=False, indent=2), encoding="utf-8")
    if answer is None:
        status = "FAIL" if transport.get("status") == "EVAL_OUTPUT_FAILURE" else "INFRA_FAILURE"
        return {"case_id": case["id"], "status": status, "candidate_sha": sha, **transport}
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
        "provider": "Google Gemini API",
        "api": transport.get("api"),
        "model": transport.get("model"),
        "interaction_id": transport.get("interaction_id"),
        "usage": transport.get("usage"),
    }
    (workspace / "grade.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> int:
    if not os.environ.get("GEMINI_API_KEY"):
        fail("GEMINI_API_KEY is not configured; no model call attempted.", 2)
    cases = {c["id"]: c for c in json.loads(CASES.read_text(encoding="utf-8"))}
    try:
        case_ids = selected_case_ids()
    except ValueError as exc:
        fail(str(exc), 2)
    sha = git_sha()
    system = frozen_instruction_source()
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for case_id in case_ids:
        result = run_case(cases[case_id], sha, system)
        results.append(result)
        print(json.dumps(result, ensure_ascii=False))
        if result["status"] == "INFRA_FAILURE":
            break
    semantic_pass = len(results) == len(case_ids) and all(r["status"] == "PASS" for r in results)
    summary = {
        "candidate_sha": sha,
        "provider": "Google Gemini API",
        "api": "interactions/v1beta",
        "model": os.environ.get("GEMINI_MODEL", "gemini-3.6-flash"),
        "selected_case_ids": list(case_ids),
        "planned_model_calls": len(case_ids),
        "executed_cases": len(results),
        "results": results,
        "decision": "PASS" if semantic_pass else "REVISE_OR_INFRA_BLOCK",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if semantic_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
