#!/usr/bin/env python3
from __future__ import annotations

import json, math, os, re, subprocess, sys, urllib.request, urllib.error
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
    "case_id":{"type":"string"},
    "decision":{"type":"string"},
    "numeric_answer":{"type":["number","null"]},
    "reasoning_points":{"type":"array","items":{"type":"string"}},
    "next_action":{"type":"string"}
  },"required":["case_id","decision","numeric_answer","reasoning_points","next_action"],"additionalProperties":False}}},
  "required":["answers"],"additionalProperties":False
}

def call_model(cases, system):
    key=os.environ["GEMINI_API_KEY"]
    visible=[{"id":c["id"],"task":c["task"]} for c in cases]
    prompt=("Act as the Paid Media Professional Core. Solve each task as actual professional work, not as label classification. "
            "Show concise decision-relevant reasoning in reasoning_points. For numeric tasks put the requested numeric result in numeric_answer. "
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
def has_any(s, terms): return any(t.lower() in s for t in terms)

def grade(case,a):
    g=case["grade"]; t=txt(a); typ=g["type"]; checks={}
    if typ=="numeric_sample_size":
        n=a.get("numeric_answer")
        checks["numeric"] = isinstance(n,(int,float)) and abs(n-g["expected"])/g["expected"] <= g["tolerance_fraction"]
        checks["randomization"] = has_any(t,["random", "randomization"])
        checks["independence/interference"] = has_any(t,["independ", "interference", "spillover"])
        checks["analysis_plan"] = has_any(t,["primary outcome","analysis plan","fixed horizon","stopping rule"])
        checks["no_guarantee"] = not has_any(t,["guarantees winner","guaranteed winner"])
    elif typ=="cluster_design":
        checks["reject_sessions"] = has_any(t,["not independent","pseudo-replication","pseudoreplication","cannot treat 420,000","sessions are not independent"])
        checks["eight_units"] = a.get("numeric_answer")==8 or has_any(t,["8 cities","eight cities","8 independent"])
        checks["cluster_aware"] = has_any(t,["cluster-aware","cluster aware","cluster-level","cluster level"])
        checks["few_clusters_uncertainty"] = has_any(t,["few clusters","low cluster","only 8","only eight","uncertainty"])
    elif typ=="stopping_multiple_testing":
        checks["reject_naive"] = has_any(t,["not valid","invalid","not defensible"])
        checks["optional_stopping"] = has_any(t,["optional stopping","peeking","sequential"])
        checks["multiple_testing"] = has_any(t,["multiple testing","multiplicity","family-wise","false discovery"])
        checks["valid_strategy"] = has_any(t,["pre-spec","preregister","sequential design","alpha spending","correction","adjust"])
    elif typ=="economic_significance":
        checks["no_rollout"] = has_any(t,["do not roll","no rollout","should not roll","reject rollout"])
        checks["cost_margin"] = has_any(t,["350,000","350000"]) and has_any(t,["40,000","40000"])
        checks["negative_net"] = has_any(t,["-310,000","-310000","310,000 loss","310000 loss","net loss"])
    elif typ=="missing_baseline":
        checks["refuse_exact"] = has_any(t,["cannot give an exact","can't give an exact","not possible to give exact","no exact sample"])
        checks["need_or_bound_baseline"] = has_any(t,["baseline","scenario","bound","range"])
        checks["no_numeric_fabrication"] = a.get("numeric_answer") is None
    elif typ=="interference":
        checks["identify_interference"] = has_any(t,["interference","spillover","contamination","cross-border"])
        checks["reject_clean_causal"] = has_any(t,["not justified","cannot support","not clean","invalid causal","weakened causal"])
        checks["next_step"] = has_any(t,["redesign","separate geographies","buffer","specialist","review"])
    return checks, all(checks.values())

def main():
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY missing",file=sys.stderr); return 2
    cases=json.loads(CASES.read_text())
    ans,raw=call_model(cases,CORE.read_text())
    by={x["case_id"]:x for x in ans["answers"]}
    results=[]
    for c in cases:
        a=by[c["id"]]; checks,p=grade(c,a)
        results.append({"case_id":c["id"],"status":"PASS" if p else "FAIL","checks":checks,"answer":a})
    status="PASS" if all(x["status"]=="PASS" for x in results) else "FAIL"
    sha=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
    summary={"candidate_sha":sha,"status":status,"scope":"PM-04 v2 authentic-work evaluation: design, calculation, diagnosis, stopping/multiplicity, economics, missing inputs, interference.","model":os.environ.get("PM04_MODEL","gemini-3.1-flash-lite"),"usage":raw.get("usage") or raw.get("usageMetadata"),"results":results}
    OUT.mkdir(parents=True,exist_ok=True); (OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print(json.dumps(summary,ensure_ascii=False,indent=2)); return 0 if status=="PASS" else 1

if __name__=="__main__": raise SystemExit(main())
