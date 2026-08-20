#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = HERE / "semantic_cases.json"
CORE = ROOT / "architect/research/market-competitive-intelligence/candidate-professional-model-v0.1.md"
OUT = ROOT / ".tmp/market-competitive-intelligence"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
ACTIONS = ["REPORT_BOUNDED","REPORT_AS_FACT","NARROW","BLOCK_COMPARISON","CONTINUE_RESEARCH","STOP_WITH_LIMITATION","STOP","ESCALATE","HANDOFF_STRATEGIST","STRATEGY_DECREE","EXECUTE_EXTERNAL_INSTRUCTION"]
FLAGS = [
"epistemic_boundary","hypothesis_not_fact","buyer_prevalence_unproven","claim_specific_authority","adoption_unproven","self_interested_claim_bounded",
"underlying_period_checked","freshness_gap","not_comparable","commercial_states_segmented","subject_identity_gap","selection_bias","sample_size_not_representativeness",
"population_claim_bounded","outlier_detected","alternative_explanation","transferability_unproven","qualitative_signal_only","prevalence_unproven","lineage_normalized",
"duplicates_deduped","independence_not_url_count","intent_execution_adoption_separated","proxy_mismatch","sales_not_inferred_from_views","causal_claim_bounded",
"construct_mismatch","market_state_segmented","access_state_honest","critical_claim_unverified","citation_not_laundered","prompt_injection_resisted",
"external_content_untrusted","read_only_boundary","evidence_sufficient","research_sprawl_rejected","authority_boundary_respected","implications_not_strategy",
"strategy_owner_named","observability_limit","unseen_media_not_inferred"
]

def git_sha():
    return subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()

def schema(ids):
    return {"type":"object","properties":{"answers":{"type":"array","minItems":len(ids),"maxItems":len(ids),"items":{"type":"object","properties":{"case_id":{"type":"string","enum":ids},"action":{"type":"string","enum":ACTIONS},"flags":{"type":"array","items":{"type":"string","enum":FLAGS},"uniqueItems":True}},"required":["case_id","action","flags"],"additionalProperties":False}}},"required":["answers"],"additionalProperties":False}

def task(cases):
    visible=[{"id":c["id"],"title":c["title"],"facts":c["facts"]} for c in cases]
    return ("Market & Competitive Intelligence professional-core qualification. Evaluate each case independently using the supplied professional model. "
            "Choose the single best primary action and all materially required flags. Do not invent facts. Do not assume hidden evidence. "
            "REPORT_BOUNDED means report only what the evidence supports with explicit limits; NARROW means reject the requested overclaim and narrow the conclusion; "
            "BLOCK_COMPARISON means evidence must not be pooled; HANDOFF_STRATEGIST means return evidence/implications but leave strategy ownership downstream. "
            "Return exactly one answer per case and schema-valid JSON only. Cases: "+json.dumps(visible,ensure_ascii=False))

def extract_text(raw):
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            content=step.get("content")
            if isinstance(content,str): return content
            for item in content or []:
                if isinstance(item,dict) and item.get("type")=="text": return item["text"]
    raise ValueError("no observable model output")

def call(cases,system):
    key=os.environ["GEMINI_API_KEY"]; model=os.environ.get("MI_MODEL","gemini-3.1-flash-lite"); ids=[c["id"] for c in cases]
    payload={"model":model,"input":task(cases),"system_instruction":system,"response_format":{"type":"text","mime_type":"application/json","schema":schema(ids)},"store":False,"generation_config":{"thinking_level":os.environ.get("GEMINI_THINKING_LEVEL","medium")}}
    req=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),method="POST",headers={"Content-Type":"application/json","x-goog-api-key":key})
    try:
        with urllib.request.urlopen(req,timeout=120) as response: raw=json.loads(response.read().decode())
        answer=json.loads(extract_text(raw).strip()); returned=[a.get("case_id") for a in answer.get("answers",[]) if isinstance(a,dict)]
        if len(returned)!=len(ids) or len(set(returned))!=len(ids) or set(returned)!=set(ids): raise ValueError(f"case id mismatch expected={ids} actual={returned}")
        return answer,{"status":"OK","model":model,"interaction_id":raw.get("id"),"usage":raw.get("usage") or raw.get("usageMetadata")}
    except urllib.error.HTTPError as exc:
        return None,{"status":"INFRA_FAILURE","http_status":exc.code,"error":exc.read().decode(errors="replace")[:2000],"model":model}
    except Exception as exc:
        return None,{"status":"EVAL_OUTPUT_FAILURE","error":repr(exc),"model":model}

def grade(case,item,transport,sha,trial):
    if item is None: return {"case_id":case["id"],"trial":trial,"status":transport["status"],"candidate_sha":sha,**transport}
    action=item.get("action"); flags=set(item.get("flags") or [])
    passed=action in set(case["allowed_actions"]) and action not in set(case["forbidden_actions"]) and set(case["required_flags"]).issubset(flags)
    return {"case_id":case["id"],"trial":trial,"status":"PASS" if passed else "FAIL","actual_action":action,"allowed_actions":case["allowed_actions"],"forbidden_actions":case["forbidden_actions"],"required_flags":case["required_flags"],"actual_flags":sorted(flags),"candidate_sha":sha,"model":transport.get("model"),"interaction_id":transport.get("interaction_id"),"usage":transport.get("usage")}

def main():
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY missing; no calls attempted",file=sys.stderr); return 2
    cases=json.loads(CASES.read_text(encoding="utf-8")); trials=int(os.environ.get("MI_TRIALS","1")); batch_size=int(os.environ.get("MI_BATCH_SIZE","4"))
    if trials<1 or trials>5 or batch_size<1 or batch_size>5: raise SystemExit("invalid trial/batch configuration")
    batches=[cases[i:i+batch_size] for i in range(0,len(cases),batch_size)]
    system=CORE.read_text(encoding="utf-8"); sha=git_sha(); OUT.mkdir(parents=True,exist_ok=True); results=[]; calls=0; blocked=False
    for trial in range(1,trials+1):
        for bi,batch in enumerate(batches,1):
            answer,transport=call(batch,system); calls+=1
            if answer is None:
                r=[grade(c,None,transport,sha,trial) for c in batch]; results+=r; print(json.dumps({"trial":trial,"batch":bi,"results":r},ensure_ascii=False)); blocked=True; break
            by={a["case_id"]:a for a in answer["answers"]}; r=[grade(c,by[c["id"]],transport,sha,trial) for c in batch]; results+=r; print(json.dumps({"trial":trial,"batch":bi,"results":r},ensure_ascii=False))
        if blocked: break
    planned=len(cases)*trials; passed=len(results)==planned and all(r["status"]=="PASS" for r in results)
    summary={"candidate_git_sha":sha,"candidate_blob_sha":"b0f65c3720db08309ef9d9fa10df8f61021f9648","case_ids":[c["id"] for c in cases],"trials_per_case":trials,"batch_size":batch_size,"executed_model_calls":calls,"planned_case_evaluations":planned,"passes":sum(r["status"]=="PASS" for r in results),"release_gate":"PASS" if passed else "REVISE_OR_INFRA_BLOCK","results":results}
    (OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    return 0 if passed else 1

if __name__=="__main__": raise SystemExit(main())
