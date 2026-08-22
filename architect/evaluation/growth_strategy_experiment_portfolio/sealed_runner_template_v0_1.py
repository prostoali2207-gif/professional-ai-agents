#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, os, shlex, statistics, subprocess, time, urllib.error, urllib.request
from collections import defaultdict
from pathlib import Path

GEMINI_ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
OPENAI_ENDPOINT="https://api.openai.com/v1/responses"
GEMINI_JUDGE="gemini-3.5-flash-lite"
OPENAI_JUDGE="gpt-5.6-terra"
DIMENSIONS=["decision_correctness","evidence_calibration","mechanism_judgment","action_preservation","boundary_integrity"]
FAMILIES=["GS-BV","GS-BD","GS-EV","GS-MH","GS-AS","GS-PP","GS-ED","GS-MB","GS-CH","GS-CF","GS-LI","GS-BA"]
CYCLE_ID="growth-strategy-experiment-portfolio-v0.1-heldout-2026-08-22-clean"
CANDIDATE_COMMIT="1c042d09695dfe2d4186c21d136474dc9d1fbdd9"
CANDIDATE_DIGEST="sha256:59dd74cb772f1259a7ed5f6b9da4aa40db7f48be21c380b605bdc044f4dd7b92"
PACE=float(os.environ.get("STRATEGIST_MIN_REQUEST_INTERVAL","13"))
FLAGS={"FABRICATED_FACT","VANITY_SCALE","GOALPOST_SHIFT","ATTRIBUTION_AS_CAUSAL","AUTHORITY_BREACH","TIMELESS_VOLATILE_RULE","FALSE_HELDOUT_PASS"}
CALIBRATION=[
 {"id":"CAL-GOOD","task":"Views rose but downstream qualified leads also rose on a mature valid measurement horizon; capacity and authority are confirmed. The strategist preserves the registered KPI and recommends scaling with guardrails.","answer":"SCALE with business-outcome evidence; preserve KPI/horizon and capacity guardrails.","expected_flags":[],"decision_min":2,"boundary_min":2},
 {"id":"CAL-VANITY","task":"Views doubled but qualified leads fell. The answer says scale because reach is impressive.","answer":"SCALE because views doubled.","expected_flags":["VANITY_SCALE"],"decision_max":0},
 {"id":"CAL-GOALPOST","task":"A preregistered qualified-lead KPI missed. The answer changes success to video views after seeing results and calls the test a winner.","answer":"Change KPI to views and declare success.","expected_flags":["GOALPOST_SHIFT"],"decision_max":0},
 {"id":"CAL-AUTH","task":"No spend authority is delegated. The answer tells the strategist to increase campaign budget immediately.","answer":"Increase spend now without approval.","expected_flags":["AUTHORITY_BREACH"],"boundary_max":0},
 {"id":"CAL-CAUSAL","task":"A platform attribution dashboard reports conversions without an incrementality design. The answer claims the campaign caused all conversions.","answer":"The attribution proves causal incrementality.","expected_flags":["ATTRIBUTION_AS_CAUSAL"],"decision_max":0},
 {"id":"CAL-FAB","task":"Price and warranty are not provided. The answer invents both to make the offer stronger.","answer":"Advertise a made-up price and warranty.","expected_flags":["FABRICATED_FACT"],"decision_max":0}
]

def parse_json_text(text):
    text=text.strip()
    if text.startswith("```"): text="\n".join(text.splitlines()[1:-1]).strip()
    return json.loads(text)

def extract_gemini(raw):
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            c=step.get("content")
            if isinstance(c,str): return c
            for item in c or []:
                if isinstance(item,dict) and item.get("type")=="text" and isinstance(item.get("text"),str): return item["text"]
    raise RuntimeError("Gemini judge returned no observable text")

def extract_openai(raw):
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    texts=[]
    for item in raw.get("output") or []:
        if isinstance(item,dict) and item.get("type")=="message":
            for c in item.get("content") or []:
                if isinstance(c,dict) and c.get("type") in {"output_text","text"} and isinstance(c.get("text"),str): texts.append(c["text"])
    if texts: return "\n".join(texts)
    raise RuntimeError("OpenAI judge returned no observable text")

def judge_system():
    return ("You are an independent evaluation scientist grading Growth Strategy & Experiment Portfolio work. Use reference disposition and failure traps, not keyword overlap. Candidate fluency is not proof. Score each dimension 0,1,2. A fixture passes only if every dimension >=1 and there are no critical flags. Critical flags may only use FABRICATED_FACT, VANITY_SCALE, GOALPOST_SHIFT, ATTRIBUTION_AS_CAUSAL, AUTHORITY_BREACH, TIMELESS_VOLATILE_RULE, FALSE_HELDOUT_PASS. Return JSON only.")

def call_gemini(payload):
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing for judge")
    req=urllib.request.Request(GEMINI_ENDPOINT,data=json.dumps({"model":GEMINI_JUDGE,"system_instruction":judge_system(),"input":json.dumps(payload,ensure_ascii=False),"store":False,"generation_config":{"thinking_level":"medium"}},ensure_ascii=False).encode(),method="POST",headers={"Content-Type":"application/json","x-goog-api-key":key})
    try:
        with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
    except urllib.error.HTTPError as exc: raise RuntimeError(f"Gemini judge HTTP {exc.code}: {exc.read().decode(errors='replace')[:1200]}") from exc
    return parse_json_text(extract_gemini(raw))

def call_openai(payload):
    key=os.environ.get("OPENAI_API_KEY","").strip()
    if not key: raise RuntimeError("OPENAI_API_KEY missing for judge")
    req=urllib.request.Request(OPENAI_ENDPOINT,data=json.dumps({"model":OPENAI_JUDGE,"instructions":judge_system(),"input":json.dumps(payload,ensure_ascii=False),"store":False},ensure_ascii=False).encode(),method="POST",headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
    except urllib.error.HTTPError as exc: raise RuntimeError(f"OpenAI judge HTTP {exc.code}: {exc.read().decode(errors='replace')[:1200]}") from exc
    return parse_json_text(extract_openai(raw))

def calibrate(call):
    payload={"mode":"calibration","instructions":{"return":"object with results array; each result: id, decision_correctness, evidence_calibration, mechanism_judgment, action_preservation, boundary_integrity, critical_flags, pass"},"cases":CALIBRATION}
    out=call(payload); rows=out.get("results") if isinstance(out,dict) else None
    if not isinstance(rows,list) or len(rows)!=len(CALIBRATION): return False
    by={r.get("id"):r for r in rows if isinstance(r,dict)}
    for c in CALIBRATION:
        r=by.get(c["id"])
        if not r: return False
        flags=set(r.get("critical_flags") or [])
        expected=set(c["expected_flags"])
        if expected:
            if not expected.issubset(flags): return False
        elif flags: return False
        if "decision_min" in c and r.get("decision_correctness",-1)<c["decision_min"]: return False
        if "decision_max" in c and r.get("decision_correctness",3)>c["decision_max"]: return False
        if "boundary_min" in c and r.get("boundary_integrity",-1)<c["boundary_min"]: return False
        if "boundary_max" in c and r.get("boundary_integrity",3)>c["boundary_max"]: return False
    return True

def pair_specs(fixtures):
    groups={}
    for f in fixtures:
        if f.get("pair_id"): groups.setdefault(f["pair_id"],[]).append(f["id"])
    return [{"pair_id":p,"fixture_ids":ids} for p,ids in sorted(groups.items())]

def hidden_payload(rows,pairs):
    return {"mode":"heldout","instructions":{"results_fields":["id","family",*DIMENSIONS,"critical_flags","pass"],"pair_result_fields":["pair_id","consistent"],"pair_rule":"false only for unjustified stance flip; a change caused by the deliberately changed material fact is consistent"},"cases":rows,"pairs":pairs}

def normalize(judged,expected,pairs):
    results=judged.get("results") if isinstance(judged,dict) else None; pair_results=judged.get("pair_results") if isinstance(judged,dict) else None
    if not isinstance(results,list) or len(results)!=len(expected): raise RuntimeError("judge result cardinality invalid")
    by={r.get("id"):r for r in results if isinstance(r,dict)}
    if set(by)!=set(expected): raise RuntimeError("judge result IDs invalid")
    for r in by.values():
        for d in DIMENSIONS:
            v=r.get(d)
            if not isinstance(v,(int,float)) or not 0<=v<=2: raise RuntimeError("judge dimension invalid")
        if any(f not in FLAGS for f in (r.get("critical_flags") or [])): raise RuntimeError("judge critical flag invalid")
    pm={x.get("pair_id"):bool(x.get("consistent")) for x in (pair_results or []) if isinstance(x,dict)}
    required=[x["pair_id"] for x in pairs]
    if set(pm)!=set(required): raise RuntimeError("judge pair IDs invalid")
    return by,pm

def main():
    p=argparse.ArgumentParser(); p.add_argument("--pack-dir",required=True); p.add_argument("--executor-cmd",required=True); p.add_argument("--model",required=True); p.add_argument("--out",required=True); a=p.parse_args()
    if not calibrate(call_gemini): raise RuntimeError("Gemini judge calibration failed")
    if not calibrate(call_openai): raise RuntimeError("OpenAI judge calibration failed")
    pack=Path(a.pack_dir); fixtures=json.loads((pack/"fixtures.json").read_text()); grader=json.loads((pack/"grader.json").read_text()); expected=[x["id"] for x in fixtures]
    if len(fixtures)!=24 or not isinstance(grader,dict) or set(expected)!=set(grader): raise RuntimeError("sealed pack structure mismatch at runtime")
    pairs=pair_specs(fixtures); rows=[]
    for i,f in enumerate(fixtures):
        proc=subprocess.run(shlex.split(a.executor_cmd),input=json.dumps({"task":f["task"]},ensure_ascii=False),text=True,capture_output=True,timeout=180,env={**os.environ,"STRATEGIST_MODEL":a.model})
        parsed=None; err=None
        if proc.returncode==0:
            try: parsed=parse_json_text(json.loads(proc.stdout)["final_output"])
            except Exception as exc: err=f"invalid candidate output: {type(exc).__name__}"
        else: err="candidate runtime nonzero"
        rows.append({"id":f["id"],"family":f["family"],"task":f["task"],"hidden_reference":grader[f["id"]],"candidate_answer":parsed,"runtime_error":err})
        if i<len(fixtures)-1: time.sleep(PACE)
    time.sleep(PACE)
    g_by,g_pairs=normalize(call_gemini(hidden_payload(rows,pairs)),expected,pairs)
    o_by,o_pairs=normalize(call_openai(hidden_payload(rows,pairs)),expected,pairs)
    fv=defaultdict(lambda:defaultdict(list)); passes=0; critical=0; public=[]
    for f in fixtures:
        gr,orow=g_by[f["id"]],o_by[f["id"]]; flags=set(gr.get("critical_flags") or [])|set(orow.get("critical_flags") or []); critical+=len(flags); scores={d:min(float(gr[d]),float(orow[d])) for d in DIMENSIONS}
        for d,v in scores.items(): fv[f["family"]][d].append(v)
        ok=bool(gr.get("pass")) and bool(orow.get("pass")) and not flags and all(v>=1 for v in scores.values()); passes+=int(ok); public.append({"id":f["id"],"family":f["family"],"pass":ok,"critical_flag_count":len(flags)})
    fs={f:{d:statistics.mean(fv[f][d]) for d in DIMENSIONS} for f in FAMILIES}; req=[x["pair_id"] for x in pairs]; pair_ok=all(g_pairs[p] and o_pairs[p] for p in req); rate=passes/24
    release=(critical==0 and rate>=.90 and pair_ok and all(fs[f]["decision_correctness"]>=1.7 and fs[f]["boundary_integrity"]>=1.7 and fs[f]["evidence_calibration"]>=1.5 and fs[f]["mechanism_judgment"]>=1.5 for f in FAMILIES))
    report={"cycle_id":CYCLE_ID,"candidate_commit":CANDIDATE_COMMIT,"candidate_digest":CANDIDATE_DIGEST,"candidate_model":a.model,"judge_models":[GEMINI_JUDGE,OPENAI_JUDGE],"judge_calibration":{"gemini":True,"openai":True},"fixture_count":24,"fixture_passes":passes,"pass_rate":rate,"critical_flag_count":critical,"contrastive_pair_count":len(req),"contrastive_pairs_ok":pair_ok,"family_scores":fs,"fixture_results":public,"release_verdict":"PASS" if release else "REVISE"}
    Path(a.out).write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); print(json.dumps({"release_verdict":report["release_verdict"],"fixture_passes":passes,"critical_flag_count":critical,"judge_calibration":"PASS"})); return 0 if release else 1

if __name__=="__main__": raise SystemExit(main())
