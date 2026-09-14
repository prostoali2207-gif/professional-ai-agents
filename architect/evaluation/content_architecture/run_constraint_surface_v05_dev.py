#!/usr/bin/env python3
from __future__ import annotations
import base64, json, os, re, time, urllib.error, urllib.request
from pathlib import Path

ROOT=Path.cwd()
DEV=ROOT/"architect/evaluation/content_architecture/constraint_surface_dev_v0.1.json"
OVERLAY=ROOT/"architect/research/content-architecture/constraint-surface-overlay-v0.5.md"
OUT=ROOT/".tmp/content-architecture-v05-constraint-surface-dev.json"
ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
BASELINE_BLOB="5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
CANDIDATE_MODEL=os.environ.get("CA_V05_CANDIDATE_MODEL","gemini-3.5-flash-lite")
JUDGE_MODEL=os.environ.get("CA_V05_JUDGE_MODEL","gemini-3.5-flash-lite")

DIMS=[
 "surface_classification_accuracy",
 "negative_constraint_invisibility",
 "public_message_justification",
 "required_disclosure_preservation",
 "handoff_clarity",
 "truth_preservation",
 "brief_fidelity",
 "authority_boundary"
]

def out_text(raw):
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    for s in reversed(raw.get("steps") or []):
        if isinstance(s,dict) and s.get("type")=="model_output":
            c=s.get("content")
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
    starts=[i for i,c in enumerate(s) if c in "[{"]
    for a in starts:
        for b in range(len(s),a,-1):
            if s[b-1] not in "]}": continue
            try:return json.loads(s[a:b])
            except: pass
    raise ValueError("invalid JSON")

def call(system,prompt,model):
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing")
    body={"model":model,"store":False,"system_instruction":system,"input":[{"type":"user_input","content":prompt}]}
    for attempt in range(2):
        req=urllib.request.Request(ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",
          headers={"x-goog-api-key":key,"Content-Type":"application/json","User-Agent":"ca-v05-constraint-surface-dev/1.0"})
        try:
            with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
            t=out_text(raw)
            if not t: raise RuntimeError("empty output")
            return parse(t)
        except urllib.error.HTTPError as e:
            b=e.read().decode(errors="replace")
            if e.code in (500,503) and attempt==0:
                time.sleep(3); continue
            raise RuntimeError(f"Gemini HTTP {e.code}: {b[:700]}")
    raise RuntimeError("provider retry exhausted")

def blob(sha):
    token=os.environ.get("GITHUB_TOKEN","").strip()
    if not token: raise RuntimeError("GITHUB_TOKEN missing")
    req=urllib.request.Request(
      f"https://api.github.com/repos/prostoali2207-gif/professional-ai-agents/git/blobs/{sha}",
      headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json","User-Agent":"ca-v05-dev/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r: x=json.loads(r.read().decode())
    return base64.b64decode(x["content"]).decode()

def cases():
    target=json.loads(DEV.read_text())["cases"]
    practical={
      "id":"CA-PRACTICAL-ORIENTATION-01",
      "input":"Communication job: a new ordinary-business viewer should understand what Ali does. Verified service range: Website/Landing, CRM, Automation/Integrations, Custom Systems. Internal guard: these categories are modular and must not be implied as a mandatory sequence. AI is not the buyer-facing front door. No prices, guarantees, result claims or CTA are approved.",
      "expected":"Architecture communicates the service range and real-work promise. Modularity and AI-secondary remain INTERNAL_ONLY unless independently needed. No disclaimer about 'not everything at once' and no anti-AI block.",
      "hard_fail":"Turns modularity or AI-secondary guard into audience-facing explanation solely because the internal guard exists."
    }
    compat=[
      {"id":"CA-COMPAT-01","input":"A verified case study has one supported result metric and three unsupported result claims proposed by a stakeholder.","expected":"Supported metric may be used if relevant; unsupported claims stay out. Truth locks remain active and are not turned into a defensive public disclaimer.","hard_fail":"Invents/strengthens unsupported claims or creates irrelevant meta-disclaimer."},
      {"id":"CA-COMPAT-02","input":"The approved communication job explicitly requires viewers to know a critical eligibility condition before acting.","expected":"Condition is PUBLIC_MESSAGE_REQUIRED and placed before the action.","hard_fail":"Hides it as internal-only or moves it after the action."},
      {"id":"CA-COMPAT-03","input":"User says 'I personally hate long intros' but the approved brief for this educational asset requires a 10-second setup to make the proof understandable.","expected":"Preference is not promoted above the approved communication requirement; architecture keeps necessary setup while minimizing waste.","hard_fail":"Treats preference as hard public architecture law and damages comprehension."},
      {"id":"CA-COMPAT-04","input":"Experiment lock says variant B must keep the same CTA as variant A; the audience does not need to know this lock exists.","expected":"CTA is preserved silently; experiment lock is INTERNAL_ONLY.","hard_fail":"Adds audience-facing copy explaining that the CTA was kept the same for the experiment."}
    ]
    return target+[practical]+compat

def main():
    base=blob(BASELINE_BLOB)
    overlay=OVERLAY.read_text()
    all_cases=cases()
    system="""You are executing exact qualified Content Architecture v0.4 plus the v0.5 Constraint Surface candidate overlay.
v0.5 is CANDIDATE / NOT QUALIFIED.
Preserve all v0.4 truth, brief, proof, experiment, authority and handoff requirements.
Your output is architecture, not final copy.
Return JSON only.
--- QUALIFIED v0.4 ---
%s
--- v0.5 CANDIDATE OVERLAY ---
%s"""%(base,overlay)
    prompt={"task":"Execute every case independently. For each, classify the material input surface and provide the public architecture/handoff consequence.",
      "output_schema":{"cases":[{"id":"exact","surface_class":"INTERNAL_ONLY|PUBLIC_MESSAGE_CANDIDATE|PUBLIC_MESSAGE_REQUIRED|MIXED","communication_job":"concise","information_order":["public semantic blocks only"],"silent_locks":["internal constraints preserved silently"],"handoff":"what creator may/must/must-not verbalize","reason":"concise"}]},
      "cases":all_cases}
    got=call(system,json.dumps(prompt,ensure_ascii=False),CANDIDATE_MODEL)
    rows=got.get("cases") if isinstance(got,dict) else None
    if not isinstance(rows,list): raise RuntimeError("candidate missing cases")
    outputs={r.get("id"):r for r in rows if isinstance(r,dict) and r.get("id")}
    missing=[c["id"] for c in all_cases if c["id"] not in outputs]
    if missing: raise RuntimeError("candidate missing "+",".join(missing))

    judge_system="""You are a senior Content Architecture evaluator.
This is visible development/regression evidence, not qualification.
The key construct is that internal constraint importance does not imply audience-message importance.
Required disclosures must still surface. Preserve the qualified v0.4 boundaries.
Return JSON only."""
    jprompt={"task":"Grade each candidate architecture against expected behavior and hard fail.",
      "dimensions":DIMS,
      "scoring":"0 material failure, 1 usable but weak/ambiguous, 2 professionally strong",
      "hard_rules":["any hard_fail triggered => fail","INTERNAL_ONLY guard appearing in information_order solely as meta-explanation => fail","required disclosure suppressed => fail","unsupported claim strengthening => fail"],
      "output_schema":{"cases":[{"id":"exact","scores":{d:2 for d in DIMS},"critical_flags":[],"pass":True,"note":"observable reason"}]},
      "cases":[{"fixture":c,"candidate_output":outputs[c["id"]]} for c in all_cases]}
    grades_raw=call(judge_system,json.dumps(jprompt,ensure_ascii=False),JUDGE_MODEL)
    rows=grades_raw.get("cases") if isinstance(grades_raw,dict) else None
    if not isinstance(rows,list): raise RuntimeError("judge missing cases")
    grades={r.get("id"):r for r in rows if isinstance(r,dict) and r.get("id")}
    missing=[c["id"] for c in all_cases if c["id"] not in grades]
    if missing: raise RuntimeError("judge missing "+",".join(missing))

    results={}; overall=True
    for c in all_cases:
        g=grades[c["id"]]; sc=g.get("scores") or {}; flags=g.get("critical_flags") or []
        p=bool(g.get("pass")) and not flags and all(int(sc.get(d,0))>0 for d in DIMS)
        results[c["id"]]={"pass":p,"scores":sc,"critical_flags":flags,"note":g.get("note",""),"candidate_output":outputs[c["id"]]}
        overall=overall and p
    report={"schema_version":"1.0.0","issue":306,"candidate":"content-architecture-v0.5-constraint-surface-overlay","candidate_status":"CANDIDATE_NOT_QUALIFIED","baseline_blob":BASELINE_BLOB,"candidate_overlay_blob":"74942d09593f73d0a9a23be068d3bbf3a0b8c06d","case_count":len(all_cases),"passed":sum(x["pass"] for x in results.values()),"failed":sum(not x["pass"] for x in results.values()),"overall_pass":overall,"models":{"candidate":CANDIDATE_MODEL,"judge":JUDGE_MODEL},"results":results,"scope_note":"Visible targeted development + compatibility + PBGS practical only; not qualification."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k!="results"},ensure_ascii=False,indent=2))
    if not overall: print(json.dumps({"failed_cases":[k for k,v in results.items() if not v["pass"]]},ensure_ascii=False))
    return 0 if overall else 1

if __name__=="__main__":
    raise SystemExit(main())
