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
CORE = ROOT / "architect/library/cores/paid-media-performance-marketing/1.0.0/professional-model.md"
OUT = ROOT / ".tmp/paid-media-performance-marketing"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
ACTIONS = ["SCALE", "STOP", "ITERATE", "REPAIR_MEASUREMENT", "EXPERIMENT", "ESCALATE", "HOLD"]
FLAGS = [
    "business_value_over_proxy", "lead_quality_checked", "no_fabricated_business_facts",
    "measurement_validity_first", "dedup_or_event_semantics", "causal_claim_blocked",
    "attribution_not_incrementality", "causal_evidence_required", "marginal_not_average",
    "uncertainty_explicit", "opportunity_cost_considered", "experiment_design_challenged",
    "conversion_lag_considered", "fault_tree_used", "measurement_incident_suspected",
    "discriminating_evidence_requested", "small_reversible_bet", "stop_loss_applied",
    "automation_not_authority", "automation_objective_checked", "privacy_signal_loss_considered",
    "triangulation_required", "authority_boundary_respected", "escalation_required",
    "vanity_metric_rejected"
]


def git_sha() -> str:
    p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True)
    return p.stdout.strip()


def schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ACTIONS},
            "flags": {"type": "array", "items": {"type": "string", "enum": FLAGS}, "uniqueItems": True},
        },
        "required": ["action", "flags"],
        "additionalProperties": False,
    }


def task(case: dict) -> str:
    visible = {"id": case["id"], "title": case["title"], "facts": case["facts"]}
    return (
        "Paid Media / Performance Marketing Professional Core behavioral evaluation. "
        "Apply the supplied professional model. Choose the single primary next action and all policy flags materially required by the case. "
        "Do not invent business facts. Return only schema-valid JSON. Case: " + json.dumps(visible, ensure_ascii=False)
    )


def extract_text(raw: dict) -> str:
    if isinstance(raw.get("output_text"), str):
        return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step, dict) and step.get("type") == "model_output":
            content = step.get("content")
            if isinstance(content, str):
                return content
            for item in content or []:
                if isinstance(item, dict) and item.get("type") == "text":
                    return item["text"]
    raise ValueError("no observable model output")


def call(case: dict, system: str) -> tuple[dict | None, dict]:
    key = os.environ["GEMINI_API_KEY"]
    model = os.environ.get("PAID_MEDIA_MODEL", "gemini-3.5-flash-lite")
    payload = {
        "model": model,
        "input": task(case),
        "system_instruction": system,
        "response_format": {"type": "text", "mime_type": "application/json", "schema": schema()},
        "store": False,
        "generation_config": {"thinking_level": os.environ.get("GEMINI_THINKING_LEVEL", "medium")},
    }
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(), method="POST", headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            raw = json.loads(response.read().decode())
        return json.loads(extract_text(raw).strip()), {"status": "OK", "model": model, "interaction_id": raw.get("id"), "usage": raw.get("usage") or raw.get("usageMetadata")}
    except urllib.error.HTTPError as exc:
        return None, {"status": "INFRA_FAILURE", "http_status": exc.code, "error": exc.read().decode(errors="replace")[:2000], "model": model}
    except Exception as exc:
        return None, {"status": "EVAL_OUTPUT_FAILURE", "error": repr(exc), "model": model}


def grade(case: dict, answer: dict | None, transport: dict, sha: str, trial: int) -> dict:
    if answer is None:
        return {"case_id": case["id"], "trial": trial, "status": transport["status"], "candidate_sha": sha, **transport}
    action = answer.get("action")
    flags = set(answer.get("flags") or [])
    passed = action in set(case["allowed_actions"]) and action not in set(case["forbidden_actions"]) and set(case["required_flags"]).issubset(flags)
    return {
        "case_id": case["id"], "trial": trial, "status": "PASS" if passed else "FAIL",
        "actual_action": action, "allowed_actions": case["allowed_actions"], "forbidden_actions": case["forbidden_actions"],
        "required_flags": case["required_flags"], "actual_flags": sorted(flags), "candidate_sha": sha,
        "model": transport.get("model"), "interaction_id": transport.get("interaction_id"), "usage": transport.get("usage")
    }


def main() -> int:
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY missing; no model calls attempted", file=sys.stderr)
        return 2
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    selected_raw = os.environ.get("PM_CASE_IDS", "").strip()
    if selected_raw:
        wanted = [x.strip() for x in selected_raw.split(",") if x.strip()]
        by_id = {c["id"]: c for c in cases}
        if any(x not in by_id for x in wanted) or len(wanted) != len(set(wanted)):
            raise SystemExit("PM_CASE_IDS contains unknown or duplicate ids")
        cases = [by_id[x] for x in wanted]
    trials = int(os.environ.get("PM_TRIALS", "1"))
    if trials < 1 or trials > 5:
        raise SystemExit("PM_TRIALS must be 1..5")
    system = CORE.read_text(encoding="utf-8")
    sha = git_sha()
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for case in cases:
        for trial in range(1, trials + 1):
            answer, transport = call(case, system)
            result = grade(case, answer, transport, sha, trial)
            results.append(result)
            print(json.dumps(result, ensure_ascii=False))
            if result["status"] in {"INFRA_FAILURE", "EVAL_OUTPUT_FAILURE"}:
                break
        if results[-1]["status"] in {"INFRA_FAILURE", "EVAL_OUTPUT_FAILURE"}:
            break
    planned = len(cases) * trials
    passed = len(results) == planned and all(r["status"] == "PASS" for r in results)
    summary = {
        "candidate_sha": sha,
        "case_ids": [c["id"] for c in cases],
        "trials_per_case": trials,
        "planned_model_calls": planned,
        "application_retries": 0,
        "passes": sum(r["status"] == "PASS" for r in results),
        "release_gate": "PASS" if passed else "REVISE_OR_INFRA_BLOCK",
        "results": results,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
