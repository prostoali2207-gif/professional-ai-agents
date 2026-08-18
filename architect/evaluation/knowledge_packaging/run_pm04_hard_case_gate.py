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
CASES = HERE / "pm04_experimentation_hard_cases.json"
CORE = ROOT / "architect/library/cores/paid-media-performance-marketing/1.0.0/professional-model.md"
OUT = ROOT / ".tmp/knowledge-packaging/pm04"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"

FINDINGS = [
    "insufficient_power_or_precision", "conversion_lag_not_mature", "no_winner_claim",
    "unit_of_randomization_mismatch", "effective_sample_size_not_sessions", "cluster_aware_analysis_required",
    "interference_risk", "causal_identification_weakened", "redesign_or_specialist_review",
    "optional_stopping_risk", "multiple_testing_or_selection_risk", "analysis_plan_required",
    "practical_significance_required", "economic_value_checked", "do_not_roll_out_on_p_value_alone",
    "baseline_required_for_sample_size", "no_fabricated_precision", "obtain_or_bound_baseline",
    "winner_B", "statistically_proven", "420000_independent_samples", "clean_causal_estimate",
    "ordinary_p_value_valid_as_used", "winner_claim", "significance_implies_rollout", "exact_sample_size_claim"
]


def git_sha() -> str:
    p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True)
    return p.stdout.strip()


def schema(case_ids: list[str]) -> dict:
    return {
        "type": "object",
        "properties": {
            "answers": {
                "type": "array",
                "minItems": len(case_ids),
                "maxItems": len(case_ids),
                "items": {
                    "type": "object",
                    "properties": {
                        "case_id": {"type": "string", "enum": case_ids},
                        "findings": {"type": "array", "items": {"type": "string", "enum": FINDINGS}, "uniqueItems": True}
                    },
                    "required": ["case_id", "findings"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["answers"],
        "additionalProperties": False
    }


def task(cases: list[dict]) -> str:
    visible = [{"id": c["id"], "title": c["title"], "facts": c["facts"]} for c in cases]
    return (
        "Operational-depth evaluation for PM-04 Experimentation and Statistical Judgment. "
        "Use the supplied Paid Media Professional Core only. Evaluate each case independently. "
        "Return the material findings needed to make a professionally defensible decision; do not reward vocabulary without identifying the design defect. "
        "Do not invent baselines, sample sizes, independence, statistical significance, or causal validity. Return only schema-valid JSON. Cases: "
        + json.dumps(visible, ensure_ascii=False)
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


def call(cases: list[dict], system: str) -> tuple[dict | None, dict]:
    key = os.environ["GEMINI_API_KEY"]
    model = os.environ.get("PM04_MODEL", "gemini-3.1-flash-lite")
    ids = [c["id"] for c in cases]
    payload = {
        "model": model,
        "input": task(cases),
        "system_instruction": system,
        "response_format": {"type": "text", "mime_type": "application/json", "schema": schema(ids)},
        "store": False,
        "generation_config": {"thinking_level": os.environ.get("GEMINI_THINKING_LEVEL", "medium")},
    }
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(), method="POST", headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            raw = json.loads(response.read().decode())
        answer = json.loads(extract_text(raw).strip())
        returned = [a.get("case_id") for a in answer.get("answers", [])]
        if len(returned) != len(ids) or len(set(returned)) != len(ids) or set(returned) != set(ids):
            raise ValueError(f"case ids mismatch expected={ids} actual={returned}")
        return answer, {"status": "OK", "model": model, "interaction_id": raw.get("id"), "usage": raw.get("usage") or raw.get("usageMetadata")}
    except urllib.error.HTTPError as exc:
        return None, {"status": "INFRA_FAILURE", "http_status": exc.code, "error": exc.read().decode(errors="replace")[:2000], "model": model}
    except Exception as exc:
        return None, {"status": "EVAL_OUTPUT_FAILURE", "error": repr(exc), "model": model}


def main() -> int:
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY missing; no paid model call attempted", file=sys.stderr)
        return 2
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    system = CORE.read_text(encoding="utf-8")
    answer, transport = call(cases, system)
    OUT.mkdir(parents=True, exist_ok=True)
    sha = git_sha()
    if answer is None:
        summary = {"candidate_sha": sha, "status": transport["status"], "transport": transport, "results": []}
        (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return 1
    by_id = {a["case_id"]: a for a in answer["answers"]}
    results = []
    for case in cases:
        actual = set(by_id[case["id"]]["findings"])
        required = set(case["required_findings"])
        forbidden = set(case["forbidden_findings"])
        passed = required.issubset(actual) and not (forbidden & actual)
        results.append({
            "case_id": case["id"], "status": "PASS" if passed else "FAIL",
            "required_findings": sorted(required), "forbidden_findings": sorted(forbidden), "actual_findings": sorted(actual)
        })
    passed = all(r["status"] == "PASS" for r in results)
    summary = {
        "candidate_sha": sha,
        "status": "PASS" if passed else "FAIL",
        "scope": "Tests whether the current core recognizes experimentation design defects that require operational statistical judgment. A FAIL supports, but does not by itself uniquely determine, a packaging repair.",
        "model": transport.get("model"), "interaction_id": transport.get("interaction_id"), "usage": transport.get("usage"),
        "results": results
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
