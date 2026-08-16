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
OUT = ROOT / ".tmp/professional-core-reuse"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
DECISIONS = ["REUSE", "ADAPT", "EXTEND", "FORK", "BUILD_NEW", "REJECT"]
FLAGS = [
    "compatibility_checked",
    "title_similarity_not_sufficient",
    "refresh_volatile_claims",
    "preserve_stable_core",
    "delta_research",
    "separate_project_context",
    "block_library_admission",
    "no_pass_inheritance",
    "targeted_or_new_regression",
    "composition_eval",
    "reuse_existing_evidence",
    "quality_before_cost",
    "provenance_required",
    "evaluation_required",
]


def git_sha() -> str:
    p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True)
    return p.stdout.strip()


def frozen_system() -> str:
    paths = [ROOT / "architect/SKILL.md", ROOT / "architect/methodology/professional-core-reuse.md"]
    return "\n\n".join(f"--- {p.relative_to(ROOT)} ---\n{p.read_text(encoding='utf-8')}" for p in paths)


def schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "decision": {"type": "string", "enum": DECISIONS},
            "flags": {"type": "array", "items": {"type": "string", "enum": FLAGS}, "uniqueItems": True},
        },
        "required": ["decision", "flags"],
        "additionalProperties": False,
    }


def selected_cases(all_cases: list[dict]) -> list[dict]:
    raw = os.environ.get("PCR_CASE_IDS", "").strip()
    if not raw:
        return all_cases
    wanted = [x.strip() for x in raw.split(",") if x.strip()]
    by_id = {c["id"]: c for c in all_cases}
    if len(wanted) != len(set(wanted)) or any(x not in by_id for x in wanted):
        raise ValueError("PCR_CASE_IDS must contain unique frozen case ids")
    return [by_id[x] for x in wanted]


def trial_count() -> int:
    raw = os.environ.get("PCR_TRIALS", "1")
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError("PCR_TRIALS must be an integer") from exc
    if value < 1 or value > 5:
        raise ValueError("PCR_TRIALS must be between 1 and 5")
    return value


def task(case: dict) -> str:
    visible = {"id": case["id"], "title": case["title"], "facts": case["facts"]}
    return (
        "Professional Core Reuse behavioral evaluation. Apply the frozen Agent Architect instructions. "
        "Choose one reuse classification and observable policy flags. BUILD_NEW means BUILD NEW. "
        "composition_eval means evaluating material interactions in the composed inherited+local system. "
        "Return only schema-valid JSON. Case facts: " + json.dumps(visible, ensure_ascii=False)
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
    model = os.environ.get("AGENT_ARCHITECT_MODEL", "gemini-3.5-flash-lite")
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
    decision = answer.get("decision")
    flags = set(answer.get("flags") or [])
    passed = decision in set(case["allowed_decisions"]) and decision not in set(case["forbidden_decisions"]) and set(case["required_flags"]).issubset(flags)
    return {
        "case_id": case["id"], "trial": trial, "status": "PASS" if passed else "FAIL", "actual_decision": decision,
        "allowed_decisions": case["allowed_decisions"], "forbidden_decisions": case["forbidden_decisions"],
        "required_flags": case["required_flags"], "actual_flags": sorted(flags), "candidate_sha": sha,
        "model": transport.get("model"), "interaction_id": transport.get("interaction_id"), "usage": transport.get("usage"),
    }


def main() -> int:
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY missing; no model calls attempted", file=sys.stderr)
        return 2
    all_cases = json.loads(CASES.read_text(encoding="utf-8"))
    try:
        cases = selected_cases(all_cases)
        trials = trial_count()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    system = frozen_system()
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
        if results and results[-1]["status"] in {"INFRA_FAILURE", "EVAL_OUTPUT_FAILURE"}:
            break
    planned = len(cases) * trials
    passed = len(results) == planned and all(r["status"] == "PASS" for r in results)
    per_case = {}
    for case in cases:
        case_results = [r for r in results if r["case_id"] == case["id"]]
        per_case[case["id"]] = {
            "passes": sum(r["status"] == "PASS" for r in case_results),
            "trials": len(case_results),
            "required_trials": trials,
        }
    summary = {
        "candidate_sha": sha,
        "case_ids": [c["id"] for c in cases],
        "trials_per_case": trials,
        "planned_model_calls": planned,
        "executed_cases": len(results),
        "application_retries": 0,
        "passes": sum(r["status"] == "PASS" for r in results),
        "per_case": per_case,
        "release_gate": "PASS" if passed else "REVISE_OR_INFRA_BLOCK",
        "results": results,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
