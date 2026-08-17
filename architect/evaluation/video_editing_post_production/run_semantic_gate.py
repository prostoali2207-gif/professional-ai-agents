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
CORE = ROOT / "architect/library/cores/video-editing-post-production/0.1.0/professional-model.md"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
ACTIONS = ["BLOCK", "REVISE_UPSTREAM", "REVISE_EDIT", "HOLD", "PROCEED_TO_ROUGH_CUT", "PROCEED_TO_FINISHING", "QC_REQUIRED", "READY_FOR_REVIEW"]
FLAGS = [
    "brief_asset_validated", "missing_coverage_escalated", "no_false_execution_claim",
    "preserve_comprehension", "bounded_comparison", "continuity_diagnosed",
    "truth_preservation", "provenance_required", "authority_boundary",
    "color_management_first", "artifact_first_qc", "intelligibility_first",
    "caption_manual_review", "variant_integrity", "experiment_invalid",
    "live_delivery_verified", "avoid_unnecessary_transcode", "justified_rule_breaking"
]


def git_sha() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True)
    return result.stdout.strip()


def output_dir() -> Path:
    tag = os.environ.get("VE_OUT_TAG", "run")
    if not tag.replace("-", "").replace("_", "").isalnum():
        raise SystemExit("VE_OUT_TAG must be alphanumeric with dash/underscore only")
    return ROOT / ".tmp/video-editing-post-production" / tag


def response_schema(ids: list[str]) -> dict:
    return {"type":"object","properties":{"answers":{"type":"array","minItems":len(ids),"maxItems":len(ids),"items":{"type":"object","properties":{"case_id":{"type":"string","enum":ids},"action":{"type":"string","enum":ACTIONS},"flags":{"type":"array","items":{"type":"string","enum":FLAGS},"uniqueItems":True}},"required":["case_id","action","flags"],"additionalProperties":False}}},"required":["answers"],"additionalProperties":False}


def task(cases: list[dict]) -> str:
    visible = [{"id": case["id"], "title": case["title"], "facts": case["facts"]} for case in cases]
    return (
        "Video Editing & Post-Production Professional Core behavioral evaluation. "
        "Evaluate each case independently from the supplied professional model. Choose one primary next action and every materially demonstrated policy flag. "
        "Do not invent missing media, observations, approvals or execution. READY_FOR_REVIEW requires an actually exported and inspected artifact. "
        "Return exactly one answer for each supplied case and schema-valid JSON only. Cases: " + json.dumps(visible, ensure_ascii=False)
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
    model = os.environ.get("VE_MODEL", "gemini-3.1-flash-lite")
    ids = [case["id"] for case in cases]
    payload = {
        "model": model, "input": task(cases), "system_instruction": system,
        "response_format": {"type":"text","mime_type":"application/json","schema":response_schema(ids)},
        "store": False, "generation_config": {"thinking_level": os.environ.get("GEMINI_THINKING_LEVEL", "medium")}
    }
    request = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(), method="POST", headers={"Content-Type":"application/json","x-goog-api-key":os.environ["GEMINI_API_KEY"]})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw = json.loads(response.read().decode())
        answer = json.loads(extract_text(raw).strip())
        returned = [item.get("case_id") for item in answer.get("answers", []) if isinstance(item, dict)]
        if len(returned) != len(ids) or len(set(returned)) != len(ids) or set(returned) != set(ids):
            raise ValueError(f"case ids mismatch: expected={ids}, actual={returned}")
        return answer, {"status":"OK","model":model,"interaction_id":raw.get("id"),"usage":raw.get("usage") or raw.get("usageMetadata")}
    except urllib.error.HTTPError as exc:
        return None, {"status":"INFRA_FAILURE","http_status":exc.code,"error":exc.read().decode(errors="replace")[:2000],"model":model}
    except Exception as exc:
        return None, {"status":"EVAL_OUTPUT_FAILURE","error":repr(exc),"model":model}


def grade(case: dict, item: dict | None, transport: dict, sha: str, trial: int) -> dict:
    if item is None:
        return {"case_id":case["id"],"trial":trial,"status":transport["status"],"candidate_sha":sha,**transport}
    action = item.get("action")
    flags = set(item.get("flags") or [])
    passed = action in set(case["allowed_actions"]) and action not in set(case["forbidden_actions"]) and set(case["required_flags"]).issubset(flags)
    return {"case_id":case["id"],"trial":trial,"status":"PASS" if passed else "FAIL","actual_action":action,"allowed_actions":case["allowed_actions"],"forbidden_actions":case["forbidden_actions"],"required_flags":case["required_flags"],"actual_flags":sorted(flags),"candidate_sha":sha,"model":transport.get("model"),"interaction_id":transport.get("interaction_id"),"usage":transport.get("usage")}


def main() -> int:
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY missing; no model calls attempted", file=sys.stderr)
        return 2
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    selected = os.environ.get("VE_CASE_IDS", "").strip()
    if selected:
        wanted = [item.strip() for item in selected.split(",") if item.strip()]
        by_id = {case["id"]: case for case in cases}
        if len(wanted) != len(set(wanted)) or any(item not in by_id for item in wanted):
            raise SystemExit("VE_CASE_IDS contains unknown or duplicate ids")
        cases = [by_id[item] for item in wanted]
    trials = int(os.environ.get("VE_TRIALS", "1"))
    batch_size = int(os.environ.get("VE_BATCH_SIZE", "5"))
    if trials < 1 or trials > 3:
        raise SystemExit("VE_TRIALS must be 1..3")
    if batch_size < 1 or batch_size > 5:
        raise SystemExit("VE_BATCH_SIZE must be 1..5")
    groups = [cases[index:index + batch_size] for index in range(0, len(cases), batch_size)]
    planned_calls = len(groups) * trials
    if planned_calls > 3:
        raise SystemExit(f"single gate invocation exceeds 3-call budget: {planned_calls}")
    system, sha, out = CORE.read_text(encoding="utf-8"), git_sha(), output_dir()
    out.mkdir(parents=True, exist_ok=True)
    results, calls, blocked = [], 0, False
    for trial in range(1, trials + 1):
        for index, group in enumerate(groups, start=1):
            answer, transport = call(group, system)
            calls += 1
            if answer is None:
                batch_results = [grade(case, None, transport, sha, trial) for case in group]
                results.extend(batch_results)
                print(json.dumps({"trial":trial,"batch":index,"results":batch_results}, ensure_ascii=False))
                blocked = True
                break
            answers = {item["case_id"]: item for item in answer["answers"]}
            batch_results = [grade(case, answers[case["id"]], transport, sha, trial) for case in group]
            results.extend(batch_results)
            print(json.dumps({"trial":trial,"batch":index,"results":batch_results}, ensure_ascii=False))
        if blocked:
            break
    expected = len(cases) * trials
    passed = len(results) == expected and all(result["status"] == "PASS" for result in results)
    summary = {"candidate_sha":sha,"case_ids":[case["id"] for case in cases],"trials_per_case":trials,"batch_size":batch_size,"planned_model_calls":planned_calls,"executed_model_calls":calls,"planned_case_evaluations":expected,"application_retries":0,"passes":sum(result["status"] == "PASS" for result in results),"release_gate":"PASS" if passed else "REVISE_OR_INFRA_BLOCK","results":results}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
