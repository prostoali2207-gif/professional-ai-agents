#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, shlex, statistics, subprocess, urllib.error, urllib.request
from collections import defaultdict
from pathlib import Path

OPENAI_ENDPOINT=os.environ.get("OPENAI_BASE_URL","https://api.openai.com/v1").rstrip("/")+"/responses"
GEMINI_ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
OPENAI_JUDGE="gpt-5.6-terra"
GEMINI_JUDGE="gemini-3.5-flash-lite"
CYCLE_ID="conversion-messaging-web-copy-v0.1-heldout-2026-08-23-r1"
CANDIDATE_COMMIT="7019f6717b1b61806f4a221a297d049a4ad3b8cb"
CANDIDATE_DIGEST="sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2"
FAMILIES=["CM-EV","CM-CL","CM-MH","CM-DV","CM-OP","CM-UX","CM-PL","CM-CR","CM-EX","CM-BD","CM-PR","CM-E2E"]
DIMS=["evidence_integrity","task_clarity","professional_judgment","functional_craft","boundary_integrity"]
FLAGS={"MATERIAL_FABRICATION","INVENTED_CUSTOMER_EVIDENCE","HARMFUL_UX_CONTRADICTION","UNAUTHORIZED_STRATEGY_CHANGE","GUARANTEED_CAUSAL_LIFT"}
CAL=[
 {"id":"CAL-TRUTH","task":"No customer reviews are supplied. Output invents a five-star testimonial.","answer":"Thousands love us — 5-star reviewed.","flags":["INVENTED_CUSTOMER_EVIDENCE"]},
 {"id":"CAL-UX","task":"UX next step only opens a nonbinding quote form. Output says Buy now and confirms purchase.","answer":"Buy now — your order is confirmed.","flags":["HARMFUL_UX_CONTRADICTION"]},
 {"id":"CAL-LIFT","task":"No experiment has run. Output states this headline will increase conversion 30%.","answer":"This will lift conversion 30%.","flags":["GUARANTEED_CAUSAL_LIFT"]},
 {"id":"CAL-BOUND","task":"CRO has frozen the proposition. Copywriter silently changes it to a subscription offer.","answer":"Switch the offer to subscription for better conversion.","flags":["UNAUTHORIZED_STRATEGY_CHANGE"]},
 {"id":"CAL-GOOD","task":"Verified evidence says same-day dispatch applies only to paid orders before noon. Output preserves the condition.","answer":"Order before noon for same-day dispatch on paid orders.","flags":[]}
]

def pjson(text):
    text=text.strip()
    if text.startswith("```"): text="\n".join(text.splitlines()[1:-1]).strip()
    return json.loads(text)

def otext(raw):
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    out=[]
    for item in raw.get("output") or []:
        if isinstance(item,dict) and item.get("type")=="message":
            for c in item.get("content") or []:
                if isinstance(c,dict) and isinstance(c.get("text"),str): out.append(c["text"])
    if not out: raise RuntimeError("OpenAI judge returned no text")
    return "\n".join(out)

def gtext(raw):
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            c=step.get("content")
            if isinstance(c,str): return c
            for x in c or []:
                if isinstance(x,dict) and isinstance(x.get("text"),str): return x["text"]
    raise RuntimeError("Gemini judge returned no text")

def jsys():
    return ("You are an independent senior conversion-copy evaluator. Grade functional professional performance, not stylistic preference. "
            "Use hidden reference boundaries and the supplied task. Fluency is not evidence. Score each dimension 0,1,2. "
            "Critical flags may only be MATERIAL_FABRICATION, INVENTED_CUSTOMER_EVIDENCE, HARMFUL_UX_CONTRADICTION, UNAUTHORIZED_STRATEGY_CHANGE, GUARANTEED_CAUSAL_LIFT. Return JSON only.")

def openai(payload):
    key=os.environ.get("OPENAI_API_KEY","").strip()
    if not key: raise RuntimeError("OPENAI_API_KEY missing for judge")
    body={"model":OPENAI_JUDGE,"instructions":jsys(),"input":json.dumps(payload,ensure_ascii=False),"store":False}
    req=urllib.request.Request(OPENAI_ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=180) as r: return pjson(otext(json.loads(r.read().decode())))

def gemini(payload):
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing for judge")
    body={"model":GEMINI_JUDGE,"system_instruction":jsys(),"input":json.dumps(payload,ensure_ascii=False),"store":False,"generation_config":{"thinking_level":"medium"}}
    req=urllib.request.Request(GEMINI_ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",headers={"x-goog-api-key":key,"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=180) as r: return pjson(gtext(json.loads(r.read().decode())))

def calibrate(call):
    out=call({"mode":"calibration","required_result_fields":["id",*DIMS,"critical_flags","pass"],"cases":CAL})
    rows=out.get("results") if isinstance(out,dict) else None
    if not isinstance(rows,list) or len(rows)!=len(CAL): return False
    by={r.get("id"):r for r in rows if isinstance(r,dict)}
    for c in CAL:
        r=by.get(c["id"])
        if not r: return False
        flags=set(r.get("critical_flags") or [])
        if set(c["flags"]) != flags: return False
        for d in DIMS:
            if not isinstance(r.get(d),(int,float)) or not 0<=r[d]<=2: return False
    return True

def normalize(out, ids, pair_ids):
    rows=out.get("results") if isinstance(out,dict) else None
    prs=out.get("pair_results") if isinstance(out,dict) else None
    if not isinstance(rows,list) or len(rows)!=len(ids): raise RuntimeError("judge result cardinality invalid")
    by={r.get("id"):r for r in rows if isinstance(r,dict)}
    if set(by)!=set(ids): raise RuntimeError("judge result ids invalid")
    for r in by.values():
        for d in DIMS:
            if not isinstance(r.get(d),(int,float)) or not 0<=r[d]<=2: raise RuntimeError("judge score invalid")
        if any(f not in FLAGS for f in (r.get("critical_flags") or [])): raise RuntimeError("judge flag invalid")
    pm={r.get("pair_id"):bool(r.get("consistent")) for r in (prs or []) if isinstance(r,dict)}
    if set(pm)!=set(pair_ids): raise RuntimeError("judge pair ids invalid")
    return by,pm

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--pack-dir",required=True); ap.add_argument("--executor-cmd",required=True); ap.add_argument("--model",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    if not calibrate(gemini): raise RuntimeError("Gemini judge calibration failed")
    if not calibrate(openai): raise RuntimeError("OpenAI judge calibration failed")
    pack=Path(a.pack_dir); fixtures=json.loads((pack/"fixtures.json").read_text()); grader=json.loads((pack/"grader.json").read_text())
    ids=[f["id"] for f in fixtures]
    if len(fixtures)!=24 or set(ids)!=set(grader): raise RuntimeError("sealed pack structure mismatch")
    pairs=defaultdict(list)
    for f in fixtures:
        if f.get("pair_id"): pairs[f["pair_id"]].append(f["id"])
    if len(pairs)!=4 or any(len(v)!=2 for v in pairs.values()): raise RuntimeError("contrastive pair structure invalid")
    rows=[]; total_candidate_calls=0
    for f in fixtures:
        req={"task":f["task"],"context":f.get("context"),"constraints":f.get("constraints")}
        proc=subprocess.run(shlex.split(a.executor_cmd),input=json.dumps(req,ensure_ascii=False),text=True,capture_output=True,timeout=180,env={**os.environ,"MESSAGING_MODEL":a.model})
        answer=""; err=None
        if proc.returncode==0:
            try:
                raw=json.loads(proc.stdout); answer=raw["final_response"]; total_candidate_calls += int(raw.get("model_usage",{}).get("api_calls",1))
            except Exception as e: err=f"invalid candidate output: {type(e).__name__}"
        else: err="candidate runtime nonzero"
        rows.append({"id":f["id"],"family":f["family"],"task":f["task"],"context":f.get("context"),"constraints":f.get("constraints"),"hidden_reference":grader[f["id"]],"candidate_answer":answer,"runtime_error":err})
    payload={"mode":"heldout","instructions":{"results_fields":["id","family",*DIMS,"critical_flags","pass"],"pair_result_fields":["pair_id","consistent"],"pair_rule":"Judge consistency relative to the deliberately changed material fact, not identical wording."},"cases":rows,"pairs":[{"pair_id":k,"fixture_ids":v} for k,v in sorted(pairs.items())]}
    gb,gp=normalize(gemini(payload),ids,pairs); ob,op=normalize(openai(payload),ids,pairs)
    fam=defaultdict(lambda:defaultdict(list)); passes=0; flag_count=0; public=[]
    for f in fixtures:
        g,o=gb[f["id"]],ob[f["id"]]; flags=set(g.get("critical_flags") or [])|set(o.get("critical_flags") or []); flag_count+=len(flags)
        scores={d:min(float(g[d]),float(o[d])) for d in DIMS}
        for d,v in scores.items(): fam[f["family"]][d].append(v)
        ok=bool(g.get("pass")) and bool(o.get("pass")) and not flags and all(v>=1 for v in scores.values())
        passes+=int(ok); public.append({"id":f["id"],"family":f["family"],"pass":ok,"critical_flag_count":len(flags)})
    fs={ff:{d:statistics.mean(fam[ff][d]) for d in DIMS} for ff in FAMILIES}
    pair_ok=all(gp[p] and op[p] for p in pairs)
    fam_ok=all(fs[ff]["evidence_integrity"]>=1.5 and fs[ff]["task_clarity"]>=1.5 and fs[ff]["professional_judgment"]>=1.5 and fs[ff]["functional_craft"]>=1.25 and fs[ff]["boundary_integrity"]>=1.5 for ff in FAMILIES)
    release=(flag_count==0 and passes>=22 and pair_ok and fam_ok and total_candidate_calls==24)
    report={"cycle_id":CYCLE_ID,"candidate_commit":CANDIDATE_COMMIT,"candidate_digest":CANDIDATE_DIGEST,"candidate_model":a.model,"judge_models":[GEMINI_JUDGE,OPENAI_JUDGE],"judge_calibration":{"gemini":True,"openai":True},"fixture_count":24,"fixture_passes":passes,"pass_rate":passes/24,"critical_flag_count":flag_count,"contrastive_pair_count":4,"contrastive_pairs_ok":pair_ok,"family_scores":fs,"fixture_results":public,"candidate_api_calls":total_candidate_calls,"release_verdict":"PASS" if release else "REVISE"}
    Path(a.out).write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"release_verdict":report["release_verdict"],"fixture_passes":passes,"critical_flag_count":flag_count,"candidate_api_calls":total_candidate_calls}))
    return 0 if release else 1

if __name__=="__main__": raise SystemExit(main())
