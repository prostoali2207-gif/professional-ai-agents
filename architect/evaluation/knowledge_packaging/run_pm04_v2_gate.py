#!/usr/bin/env python3
from __future__ import annotations

import json, math, os, subprocess, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = HERE / "pm04_v2_cases.json"
CORE = ROOT / "architect/library/cores/paid-media-performance-marketing/1.0.0/professional-model.md"
OUT = ROOT / ".tmp/knowledge-packaging/pm04-v2"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"

SCHEMA = {
  "type":"object",
  "properties":{"answers":{"type":"array","items":{"type":"object","properties":{
    "case_id":{"type":"string"}, "decision":{"type":"string"},
    "numeric_answer":{"type":["number","null"]},
    "reasoning_points":{"type":"array","items":{"type":"string"}},
    "next_action":{"type":"string"}
  },"required":["case_id","decision","numeric_answer","reasoning_points","next_action"],"additionalProperties":False}}},
  "required":["answers"],"additionalProperties":False
}

def call_model(cases, system):
    key=os.environ["GEMINI_API_KEY"]
    visible=[{"id":c["id"],"task":c["task"]} for c in cases]
    prompt=("Act as the Paid Media Professional Core. Solve each task as actual professional work. "
            "Show concise decision-relevant reasoning. For numeric tasks put the requested result in numeric_answer. "
            "Do not invent missing inputs. Return JSON only. Tasks: "+json.dumps(visible,ensure_ascii=False))
    payload={"model":os.environ.get("PM04_MODEL","gemini-3.1-flash-lite"),"input":prompt,"system_instruction":system,
             "response_format":{"type":"text","mime_type":"application/json","schema":SCHEMA},"store":False,
             "generation_config":{"thinking_level":os.environ.get("GEMINI_THINKING_LEVEL","medium")}}
    req=urllib.request.Request(ENDPOINT,data=json.dumps(payload).encode(),method="POST",headers={"Content-Type":"application/json","x-goog-api-key":key})
    with urllib.request.urlopen(req,timeout=120) as r: raw=json.loads(r.read().decode())
    text=raw.get("output_text")
    if not text:
        for step in reversed(raw.get("steps") or []):
            if isinstance(step,dict) and step.get("type")=="model_output":
                content=step.get("content")
                if isinstance(content,str): text=content; break
                for item in content or []:
                    if isinstance(item,dict) and item.get("type")=="text": text=item["text"]; break
                if text: break
    if not text: raise ValueError("no model output")
    return json.loads(text), raw

def txt(a): return " ".join([a.get("decision","")+" "+a.get("next_action","")]+a.get("reasoning_points",[])).lower()
def any_term(s, terms): return any(x.lower() in s for x in terms)

def grade(case,a):
    g=case["grade"]; t=txt(a); typ=g["type"]; checks={}
    if typ=="numeric_sample_size":
        n=a.get("numeric_answer")
        checks["numeric"] = isinstance(n,(int,float)) and abs(n-g["expected"])/g["expected"] <= g["tolerance_fraction"]
        # The task already states equal random assignment; do not require parroting the premise.
        checks["independence/interference"] = any_term(t,["independ", "interference", "spillover", "sutva"])
        checks["precommitment"] = any_term(t,["pre-register", "preregister", "pre-specified", "prespecified", "stopping rule", "fixed horizon", "analysis plan"])
        checks["no_guarantee"] = not any_term(t,["guarantees winner","guaranteed winner"])
    elif typ=="cluster_design":
        checks["reject_session_independence"] = any_term(t,["unit of randomization is the city","randomization unit is the city","intra-city correlation","session-level testing","sessions are not independent","pseudoreplication","pseudo-replication"])
        checks["recognize_eight_clusters"] = a.get("numeric_answer")==8 or any_term(t,["n=8","8 cities","eight cities","only 8","only eight"])
        checks["cluster_appropriate_analysis"] = any_term(t,["city-level","city level","cluster-level","cluster level","permutation test","difference-in-differences","did regression"])
        checks["few_clusters_uncertainty"] = any_term(t,["low power","small sample","few clusters","only 8","only eight","uncertainty"])
    elif typ=="stopping_multiple_testing":
        checks["reject_naive"] = any_term(t,["not valid","invalid","not defensible"])
        checks["optional_stopping"] = any_term(t,["optional stopping","peeking","continuous monitoring","sequential"])
        checks["multiple_testing"] = any_term(t,["multiple testing","multiplicity","false positive","primary outcome"])
        checks["valid_strategy"] = any_term(t,["pre-register","preregister","fixed-horizon","fixed horizon","sequential testing boundary","o'brien-fleming","obrien-fleming","pocock","alpha spending","correction","adjust"])
    elif typ=="economic_significance":
        n=a.get("numeric_answer")
        checks["no_rollout"] = any_term(t,["do not roll","no rollout","should not roll","reject rollout","do not implement","negative roi"])
        checks["cost_margin"] = any_term(t,["350,000","350000"]) and any_term(t,["40,000","40000"])
        checks["negative_net"] = (isinstance(n,(int,float)) and abs(n + 310000) <= 1) or any_term(t,["-310,000","-310000","-310k","310,000 loss","310000 loss","net loss"])
    elif typ=="missing_baseline":
        checks["refuse_exact"] = any_term(t,["cannot give an exact","can't give an exact","cannot provide a single exact","not possible to give exact","no exact sample","without the baseline"])
        checks["need_or_bound_baseline"] = any_term(t,["baseline","scenario","bound","range"])
        checks["no_numeric_fabrication"] = a.get("numeric_answer") is None
    elif typ=="interference":
        checks["identify_interference"] = any_term(t,["interference","spillover","contamination","cross-border","sutva"])
        checks["reject_clean_causal"] = any_term(t,["not justified","cannot support","not clean","invalid causal","weakened causal","biased and unreliable"])
        checks["next_step"] = any_term(t,["redesign","separate geographies","buffer","switchback","synthetic control","alternative method","review"])
    return checks, all(checks.values())

def main():
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY missing",file=__import__('sys').stderr); return 2
    cases=json.loads(CASES.read_text()); ans,raw=call_model(cases,CORE.read_text()); by={x["case_id"]:x for x in ans["answers"]}
    results=[]
    for c in cases:
        a=by[c["id"]]; checks,p=grade(c,a); results.append({"case_id":c["id"],"status":"PASS" if p else "FAIL","checks":checks,"answer":a})
    status="PASS" if all(x["status"]=="PASS" for x in results) else "FAIL"
    sha=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
    summary={"candidate_sha":sha,"status":status,"scope":"PM-04 v2 authentic-work evaluation: design, calculation, diagnosis, stopping/multiplicity, economics, missing inputs, interference.","model":os.environ.get("PM04_MODEL","gemini-3.1-flash-lite"),"usage":raw.get("usage") or raw.get("usageMetadata"),"results":results}
    OUT.mkdir(parents=True,exist_ok=True); (OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)); print(json.dumps(summary,ensure_ascii=False,indent=2)); return 0 if status=="PASS" else 1

if __name__=="__main__": raise SystemExit(main())
