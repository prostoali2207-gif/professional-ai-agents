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
CASES = HERE / "semantic-cases.json"
CANDIDATE = HERE / "candidate" / "SKILL.md"
MODEL = HERE / "professional-model-extension-candidate-v0.1.md"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"

ACTIONS = [
    "REVISE_SOUND_STRUCTURE","ESCALATE_EDITORIAL","BLOCK_TRUTH_RISK",
    "PROCEED_WITH_CONCEPT","FILL_ALL_SILENCE","PROCEED_WITH_BOUNDED_LAYERING",
    "REPLACE_WITH_UNRELATED_HERO_SOUND","REVISE_SOUND_FIT","REVISE_MIX",
    "QC_REQUIRED","READY_FOR_REAL_MEDIA_REVIEW"
]
FLAGS = [
    "sonic_concept_first","macro_coherence","remove_nonessential_sfx",
    "upstream_edit_check","no_sound_bandage","truth_preserving_sound",
    "avoid_false_product_property","intentional_negative_space","hero_event_hierarchy",
    "transition_restraint","preserve_attention_hierarchy","layer_roles_defined",
    "retain_authentic_anchor","perspective_fit","sync_not_sufficient",
    "playback_context_qc","creative_mix_hierarchy","meters_not_sufficient",
    "artifact_listen_required","no_false_qc_claim","macro_emotional_arc",
    "event_hierarchy"
]


def candidate_sha() -> str:
    frozen = os.environ.get("CSD_CANDIDATE_SHA")
    if frozen:
        return frozen
    return subprocess.run(["git","rev-parse","HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()


def response_schema(ids: list[str]) -> dict:
    return {
        "type":"object",
        "properties":{"answers":{
            "type":"array","minItems":len(ids),"maxItems":len(ids),
            "items":{"type":"object","properties":{
                "case_id":{"type":"string","enum":ids},
                "action":{"type":"string","enum":ACTIONS},
                "flags":{"type":"array","items":{"type":"string","enum":FLAGS},"uniqueItems":True},
                "rationale":{"type":"string"}
            },"required":["case_id","action","flags","rationale"],"additionalProperties":False}
        }},
        "required":["answers"],"additionalProperties":False
    }


def call(batch: list[dict], system: str) -> tuple[dict | None, dict]:
    ids=[c["id"] for c in batch]
    visible=[{"id":c["id"],"title":c["title"],"facts":c["facts"]} for c in batch]
    payload={
        "model":os.environ.get("CSD_MODEL","gemini-3.1-flash-lite"),
        "input":"Evaluate each Commercial Sound Design case independently. Choose the professionally correct next action and only directly implicated flags. Do not infer real-media PASS from a text case. Return schema-valid JSON only. Cases: "+json.dumps(visible,ensure_ascii=False),
        "system_instruction":system,
        "response_format":{"type":"text","mime_type":"application/json","schema":response_schema(ids)},
        "store":False,
        "generation_config":{"thinking_level":os.environ.get("GEMINI_THINKING_LEVEL","medium")}
    }
    req=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),method="POST",headers={"Content-Type":"application/json","x-goog-api-key":os.environ["GEMINI_API_KEY"]})
    try:
        with urllib.request.urlopen(req,timeout=120) as r:
            raw=json.loads(r.read().decode())
        txt=raw.get("output_text")
        if not isinstance(txt,str):
            for step in reversed(raw.get("steps") or []):
                if isinstance(step,dict) and step.get("type")=="model_output":
                    content=step.get("content")
                    if isinstance(content,str):
                        txt=content
                        break
                    for item in content or []:
                        if isinstance(item,dict) and item.get("type")=="text":
                            txt=item.get("text")
                            break
                    if isinstance(txt,str):
                        break
        if not isinstance(txt,str):
            raise ValueError("no observable model output")
        answer=json.loads(txt.strip())
        returned=[x.get("case_id") for x in answer.get("answers",[]) if isinstance(x,dict)]
        if len(returned)!=len(ids) or len(set(returned))!=len(ids) or set(returned)!=set(ids):
            raise ValueError(f"case id mismatch expected={ids} actual={returned}")
        return answer,{"status":"OK","usage":raw.get("usage") or raw.get("usageMetadata")}
    except urllib.error.HTTPError as exc:
        return None,{"status":"PROVIDER_RUNTIME_FAIL","http_status":exc.code,"error":exc.read().decode(errors="replace")[:2000]}
    except Exception as exc:
        return None,{"status":"EVAL_OUTPUT_FAILURE","error":repr(exc)}


def grade(case: dict, item: dict | None, transport: dict, sha: str, trial: int) -> dict:
    if item is None:
        return {"case_id":case["id"],"trial":trial,"status":transport["status"],"candidate_sha":sha,**transport}
    flags=set(item.get("flags") or [])
    action=item.get("action")
    ok=action in set(case["allowed_actions"]) and action not in set(case["forbidden_actions"]) and set(case["required_flags"]).issubset(flags)
    supporting=set(case.get("supporting_flags") or [])
    return {
        "case_id":case["id"],"trial":trial,"status":"PASS" if ok else "FAIL",
        "actual_action":action,"actual_flags":sorted(flags),
        "required_flags":case["required_flags"],"observed_supporting_flags":sorted(flags & supporting),
        "candidate_sha":sha
    }


def main() -> int:
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY missing; no model calls attempted",file=sys.stderr)
        return 2

    cases=json.loads(CASES.read_text(encoding="utf-8"))
    selected=os.environ.get("CSD_CASE_IDS","").strip()
    if selected:
        ids=[x.strip() for x in selected.split(",") if x.strip()]
        by={c["id"]:c for c in cases}
        if len(ids)!=len(set(ids)) or any(x not in by for x in ids):
            raise SystemExit("CSD_CASE_IDS contains unknown or duplicate ids")
        cases=[by[x] for x in ids]

    trials=int(os.environ.get("CSD_TRIALS","1"))
    batch=int(os.environ.get("CSD_BATCH_SIZE","4"))
    if trials<1 or trials>3 or batch<1 or batch>4:
        raise SystemExit("trials and batch must be 1..3")
    groups=[cases[i:i+batch] for i in range(0,len(cases),batch)]
    if len(groups)*trials>3:
        raise SystemExit("single invocation exceeds 3-call budget")

    system=CANDIDATE.read_text(encoding="utf-8")+"\n\n"+MODEL.read_text(encoding="utf-8")
    sha=candidate_sha()
    results=[]
    calls=0
    for trial in range(1,trials+1):
        for group in groups:
            answer,transport=call(group,system)
            calls+=1
            if answer is None:
                results.extend(grade(c,None,transport,sha,trial) for c in group)
                summary={"candidate_sha":sha,"executed_model_calls":calls,"application_retries":0,"release_gate":"NOT_EXECUTABLE","results":results}
                print(json.dumps(summary,ensure_ascii=False,indent=2))
                return 1
            by={x["case_id"]:x for x in answer["answers"]}
            results.extend(grade(c,by[c["id"]],transport,sha,trial) for c in group)

    expected=len(cases)*trials
    passed=len(results)==expected and all(x["status"]=="PASS" for x in results)
    summary={"candidate_sha":sha,"case_ids":[c["id"] for c in cases],"trials_per_case":trials,"executed_model_calls":calls,"application_retries":0,"release_gate":"PASS_DEVELOPMENT_ONLY" if passed else "REVISE","results":results}
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0 if passed else 1


if __name__=="__main__":
    raise SystemExit(main())
