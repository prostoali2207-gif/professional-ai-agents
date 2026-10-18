#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, time, urllib.error, urllib.request
from pathlib import Path

ROOT=Path.cwd()
BASE=ROOT/"architect/evaluation/social_content_creative"
V1=BASE/"authorial_voice_dev_v0.1.json"
V2=BASE/"authorial_voice_dev_v0.2.json"
PARENT=ROOT/"architect/library/cores/social-content-creative/0.1.0/professional-model.md"
OVERLAY=ROOT/"architect/research/social-content-creative/professional-model-candidate-v0.4-authorial-voice-overlay.md"
OUT=ROOT/".tmp/authorial-voice-v04-targeted-development.json"
ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
CANDIDATE_MODEL=os.environ.get("AUTHORIAL_VOICE_CANDIDATE_MODEL","gemini-3.5-flash-lite")
JUDGE_MODEL=os.environ.get("AUTHORIAL_VOICE_JUDGE_MODEL","gemini-3.5-flash-lite")

NEW_DIMS=["creator_native_execution","earned_stance_quality","benchmark_transfer_visibility","visual_proof_economy","closure_selectivity"]
BASE_DIMS=["truth_preservation","brief_fidelity","authority_boundary","anti_imitation","speakability","distinctiveness","clarity"]

def text(raw):
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            c=step.get("content")
            if isinstance(c,str): return c
            for x in c or []:
                if isinstance(x,dict) and x.get("type")=="text" and isinstance(x.get("text"),str): return x["text"]
    return ""

def parse(s):
    s=s.strip()
    if s.startswith("```"):
        s=re.sub(r"^```(?:json)?\s*","",s,flags=re.I); s=re.sub(r"\s*```$","",s)
    try:return json.loads(s)
    except: pass
    a=min([i for i,c in enumerate(s) if c in "[{"] or [0])
    for b in range(len(s),a,-1):
        if s[b-1] not in "]}": continue
        try:return json.loads(s[a:b])
        except: continue
    raise ValueError("invalid JSON")

def call(system,prompt,model):
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing")
    body={"model":model,"store":False,"system_instruction":system,"input":[{"type":"user_input","content":prompt}]}
    for attempt in range(2):
        req=urllib.request.Request(ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",
            headers={"x-goog-api-key":key,"Content-Type":"application/json","User-Agent":"authorial-voice-v04-dev/1.0"})
        try:
            with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
            t=text(raw)
            if not t: raise RuntimeError("empty model output")
            return parse(t)
        except urllib.error.HTTPError as e:
            b=e.read().decode(errors="replace")
            if e.code in (500,503) and attempt==0:
                time.sleep(3); continue
            raise RuntimeError(f"Gemini HTTP {e.code}: {b[:700]}")
    raise RuntimeError("provider retry exhausted")

def main():
    parent=PARENT.read_text()
    overlay=OVERLAY.read_text()
    suites=[json.loads(V1.read_text()),json.loads(V2.read_text())]
    cases=suites[0]["cases"]+suites[1]["cases"]
    system="""You are executing Social Content Creative 0.1.0 with the frozen Authorial Voice v0.4 candidate overlay.
Candidate status is CANDIDATE / NOT QUALIFIED. Do not claim qualification.
Preserve truth, brief, experiment, authority and anti-imitation controls.
Physical vocal performance is outside scope.
Return only valid JSON.
--- QUALIFIED PARENT ---
%s
--- v0.4 CANDIDATE OVERLAY ---
%s"""%(parent,overlay)

    outputs={}
    for start in range(0,len(cases),6):
        batch=cases[start:start+6]
        prompt={"task":"Execute each visible development fixture independently. Give the actual usable artifact/direction, not only a critique. Do not reuse surface wording across unrelated cases.",
                "output_schema":{"cases":[{"id":"exact id","diagnosis":"concise","artifact":"actual answer/script/direction","professional_reason":"concise","boundary_notes":"concise"}]},
                "cases":batch}
        got=call(system,json.dumps(prompt,ensure_ascii=False),CANDIDATE_MODEL)
        rows=got.get("cases") if isinstance(got,dict) else None
        if not isinstance(rows,list): raise RuntimeError("candidate batch missing cases")
        for row in rows:
            if isinstance(row,dict) and row.get("id"): outputs[row["id"]]=row

    missing=[c["id"] for c in cases if c["id"] not in outputs]
    if missing: raise RuntimeError("candidate missing: "+",".join(missing))

    judge_system="""You are a senior Social Content Creative evaluator. Grade professional behavior, not verbosity or taste.
This is a visible development gate, not qualification.
A polished but teacherly mini-lesson must fail creator-native fixtures.
Do not reward profanity, slang, fake spontaneity, reference imitation or unsupported claims.
Return only valid JSON."""
    grades={}
    for start in range(0,len(cases),6):
        batch=cases[start:start+6]
        payload=[]
        for c in batch: payload.append({"fixture":c,"candidate_output":outputs[c["id"]]})
        prompt={"task":"Grade each case against its visible expected observables and critical fails.",
                "dimensions":BASE_DIMS+NEW_DIMS,
                "scoring":"0 material failure; 1 usable but weak; 2 professionally strong. For dimensions not materially applicable, use 2 if no violation is present.",
                "hard_rules":["any explicit critical_fail_if trigger => FAIL","any unsupported factual/commercial claim => FAIL","reference cloning => FAIL","strategy/CTA boundary violation => FAIL","for AV-DEV2-01..05 no new dimension may be 0"],
                "output_schema":{"cases":[{"id":"exact id","scores":{d:2 for d in BASE_DIMS+NEW_DIMS},"critical_flags":[],"pass":True,"note":"observable reason"}]},
                "cases":payload}
        got=call(judge_system,json.dumps(prompt,ensure_ascii=False),JUDGE_MODEL)
        rows=got.get("cases") if isinstance(got,dict) else None
        if not isinstance(rows,list): raise RuntimeError("judge batch missing cases")
        for row in rows:
            if isinstance(row,dict) and row.get("id"): grades[row["id"]]=row

    missing=[c["id"] for c in cases if c["id"] not in grades]
    if missing: raise RuntimeError("judge missing: "+",".join(missing))

    results={}
    overall=True
    for c in cases:
        cid=c["id"]; g=grades[cid]
        scores=g.get("scores") or {}
        critical=g.get("critical_flags") or []
        p=bool(g.get("pass")) and not critical
        if cid.startswith("AV-DEV2-"):
            p=p and all(int(scores.get(d,0))>0 for d in NEW_DIMS)
        p=p and int(scores.get("truth_preservation",0))>0 and int(scores.get("brief_fidelity",0))>0 and int(scores.get("authority_boundary",0))>0 and int(scores.get("anti_imitation",0))>0
        overall=overall and p
        results[cid]={"family":c.get("family"),"pass":p,"scores":scores,"critical_flags":critical,"note":g.get("note",""),"candidate_output":outputs[cid]}

    report={"schema_version":"1.0.0","issue":302,"candidate":"social-content-creative-authorial-voice-v0.4","candidate_status":"CANDIDATE_NOT_QUALIFIED","suite":"TARGETED_DEVELOPMENT_EVALUATION_V0_2","models":{"candidate":CANDIDATE_MODEL,"judge":JUDGE_MODEL},"case_count":len(cases),"passed":sum(1 for x in results.values() if x["pass"]),"failed":sum(1 for x in results.values() if not x["pass"]),"overall_pass":overall,"results":results,"scope_note":"Visible development evidence only; cannot qualify candidate."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k!="results"},ensure_ascii=False,indent=2))
    if not overall:
        print(json.dumps({"failed_cases":[k for k,v in results.items() if not v["pass"]]},ensure_ascii=False))
    return 0 if overall else 1

if __name__=="__main__":
    raise SystemExit(main())
