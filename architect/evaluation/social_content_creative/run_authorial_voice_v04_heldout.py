#!/usr/bin/env python3
from __future__ import annotations

import base64, json, os, re, time, urllib.error, urllib.request
from pathlib import Path
from typing import Any

ROOT=Path.cwd()
OUT=ROOT/".tmp/authorial-voice-v04-heldout"
OUT.mkdir(parents=True,exist_ok=True)
SAN=OUT/"sanitized-report.json"
FULL=OUT/"full-consumed-evidence.json"

GEMINI_ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
GROQ_ENDPOINT="https://api.groq.com/openai/v1/chat/completions"
GEMINI_CANDIDATE=os.environ.get("AUTHORIAL_VOICE_CANDIDATE_MODEL","gemini-3.5-flash-lite")
GEMINI_JUDGE=os.environ.get("AUTHORIAL_VOICE_GEMINI_JUDGE_MODEL","gemini-3.5-flash-lite")
GROQ_MODEL=os.environ.get("AUTHORIAL_VOICE_GROQ_MODEL","qwen/qwen3.6-27b")

PARENT=ROOT/"architect/library/cores/social-content-creative/0.1.0/professional-model.md"
OVERLAY=ROOT/"architect/research/social-content-creative/professional-model-candidate-v0.4-authorial-voice-overlay.md"
PROTO=ROOT/"architect/research/social-content-creative/authorial-voice-qualification-protocol-v0.2.md"
DEV2=ROOT/"architect/evaluation/social_content_creative/authorial_voice_dev_v0.2.json"

PARENT_SHA="d8eee4c6f9141f362d91a340c37dcae6ad6bfa71"
OVERLAY_SHA="abed0d6762299c82b82e603355beac9f79b4cca2"
PROTO_SHA="c9942aa64cead4f0b55c7949a6a59debbde88356"

PBGS_FAILED="2075489711777214e94e2e6f65863c30fce79419"
PBGS_STRESS="fcaeeb96c8a23213c39adf2dfced4450a8887818"
PBGS_ORIENTATION="6d3141a06a115fb725e7d16d24ef1ff7e3f511eb"

FAMILIES=[
("AV-Q1","generic-to-distinctive"),
("AV-Q2","reference-imitation-trap"),
("AV-Q3","humor-proof-conflict"),
("AV-Q4","correct-no-humor"),
("AV-Q5","profanity-pressure"),
("AV-Q6","persona-continuity"),
("AV-Q7","spoken-naturalness"),
("AV-Q8","anti-template"),
("AV-Q9","multilingual-register"),
("AV-Q10","strategy-boundary"),
("AV-Q11","text-vs-performance-boundary"),
("AV-Q12","reference-diversity"),
("AV-Q13","safe-pedagogic-collapse"),
("AV-Q14","benchmark-to-execution-transfer"),
("AV-Q15","visual-proof-economy"),
("AV-Q16","closure-without-lecture-recap"),
("AV-Q17","fake-spontaneity-trap"),
]

DIMS=[
"truth_preservation","brief_fidelity","authority_boundary","anti_imitation",
"distinctiveness","clarity","speakability","humor_function",
"creator_native_execution","earned_stance_quality","benchmark_transfer_visibility",
"visual_proof_economy","closure_selectivity"
]
FLAGS=[
"MATERIAL_FABRICATION","REFERENCE_CLONING","STRATEGY_BOUNDARY_VIOLATION",
"CANDIDATE_STATUS_STRENGTHENING","SAFE_PEDAGOGIC_COLLAPSE",
"BENCHMARK_WITHOUT_EXECUTION_TRANSFER","VOICE_OVER_EXPLAINS_VISIBLE_PROOF",
"LECTURE_RECAP_CLOSURE","FAKE_SPONTANEITY_REPAIR","PHYSICAL_DELIVERY_OVERCLAIM"
]

def extract_text(raw:dict)->str:
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            c=step.get("content")
            if isinstance(c,str): return c
            for x in c or []:
                if isinstance(x,dict) and x.get("type")=="text" and isinstance(x.get("text"),str): return x["text"]
    return ""

def parse_json(text:str)->Any:
    s=text.strip()
    if s.startswith("```"):
        s=re.sub(r"^```(?:json)?\s*","",s,flags=re.I); s=re.sub(r"\s*```$","",s)
    try:return json.loads(s)
    except: pass
    starts=[i for i,c in enumerate(s) if c in "[{"]
    for a in starts:
        for b in range(len(s),a,-1):
            if s[b-1] not in "]}": continue
            try:return json.loads(s[a:b])
            except: continue
    raise ValueError("invalid JSON")

def gemini(system:str,prompt:str,model:str,format_retry:bool=False)->Any:
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing")
    body={"model":model,"store":False,"system_instruction":system,"input":[{"type":"user_input","content":prompt}]}
    def once(p):
        body["input"]=[{"type":"user_input","content":p}]
        for attempt in range(2):
            req=urllib.request.Request(GEMINI_ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",
              headers={"x-goog-api-key":key,"Content-Type":"application/json","User-Agent":"authorial-voice-heldout/1.0"})
            try:
                with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
                t=extract_text(raw)
                if not t: raise RuntimeError("empty Gemini output")
                return t
            except urllib.error.HTTPError as e:
                msg=e.read().decode(errors="replace")
                if e.code in (500,503) and attempt==0:
                    time.sleep(3); continue
                raise RuntimeError(f"Gemini HTTP {e.code}: {msg[:900]}")
    t=once(prompt)
    try:return parse_json(t)
    except:
        if not format_retry: raise
        return parse_json(once(prompt+"\nReturn valid JSON only. No markdown."))

def groq(system:str,prompt:str,format_retry:bool=False)->Any:
    key=os.environ.get("GROQ_API_KEY","").strip()
    if not key: raise RuntimeError("GROQ_API_KEY missing")
    def once(p):
        body={"model":GROQ_MODEL,"messages":[{"role":"system","content":system},{"role":"user","content":p}],
          "temperature":0,"reasoning_format":"hidden","response_format":{"type":"json_object"}}
        req=urllib.request.Request(GROQ_ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",
          headers={"Authorization":"Bearer "+key,"Content-Type":"application/json","Accept":"application/json","User-Agent":"authorial-voice-heldout/1.0"})
        try:
            with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
            return raw["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Groq HTTP {e.code}: {e.read().decode(errors='replace')[:900]}")
    t=once(prompt)
    try:return parse_json(t)
    except:
        if not format_retry: raise
        return parse_json(once(prompt+"\nReturn valid JSON only. No markdown."))

def github_blob(repo:str,sha:str)->str:
    token=os.environ.get("GITHUB_TOKEN","").strip()
    if not token: raise RuntimeError("GITHUB_TOKEN missing")
    req=urllib.request.Request(f"https://api.github.com/repos/{repo}/git/blobs/{sha}",
      headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json","User-Agent":"authorial-voice-heldout/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r: x=json.loads(r.read().decode())
    return base64.b64decode(x["content"]).decode()

def author_cases()->list[dict]:
    all_cases=[]
    for start in range(0,len(FAMILIES),5):
        group=FAMILIES[start:start+5]
        prompt=json.dumps({
          "task":"Author one fresh hidden professional evaluation case per requested family. Cases must be self-contained and not paraphrase common visible examples. Provide evaluator-only rubric. Exact named creator wording/catchphrases must never be an expected answer.",
          "families":[{"id":a,"name":b} for a,b in group],
          "schema":{"cases":[{
            "id":"family id","scenario":"self-contained task/facts/locks","communication_mode":"creator-practitioner|teaching|mixed as justified",
            "expected_observables":["..."],"forbidden_behaviors":["..."],"material_dimensions":["dimension names"],"reference_answer_notes":"brief evaluator-only rationale"
          }]},
          "dimensions":DIMS,
          "constraints":["No exact visible FleetDesk/landing/BayerCRM cases","No Asati catchphrases","Include enough facts to grade truth","No acoustic performance requirement"]
        },ensure_ascii=False)
        got=groq("You are an independent evaluation author for professional social-content craft. Return JSON only.",prompt,True)
        rows=got.get("cases") if isinstance(got,dict) else None
        if not isinstance(rows,list) or len(rows)!=len(group): raise RuntimeError("author pack shape invalid")
        by={r.get("id"):r for r in rows if isinstance(r,dict)}
        for fid,_ in group:
            if fid not in by: raise RuntimeError("missing authored family "+fid)
            c=by[fid]; c["family"]=fid; all_cases.append(c)
    return all_cases

def candidate_outputs(cases,parent,overlay)->dict:
    system=("You are executing exact Social Content Creative 0.1.0 plus Authorial Voice v0.4 candidate overlay. "
      "Candidate is NOT QUALIFIED. Preserve truth, brief, authority and anti-imitation. "
      "Physical vocal performance is out of scope. Return JSON only.\n---PARENT---\n"+parent+"\n---OVERLAY---\n"+overlay)
    out={}
    for c in cases:
        prompt=json.dumps({"scenario":c["scenario"],"task":"Produce the strongest usable response/artifact for this case.",
          "output_schema":{"diagnosis":"concise","artifact":"actual script/direction/repair","professional_reason":"concise","boundary_notes":"concise"}},ensure_ascii=False)
        out[c["family"]]=gemini(system,prompt,GEMINI_CANDIDATE,False)
    return out

def judge_payload(cases,outputs):
    return [{"family":c["family"],"scenario":c["scenario"],"communication_mode":c.get("communication_mode"),
      "expected_observables":c.get("expected_observables",[]),"forbidden_behaviors":c.get("forbidden_behaviors",[]),
      "material_dimensions":c.get("material_dimensions",[]),"reference_answer_notes":c.get("reference_answer_notes",""),
      "candidate_output":outputs[c["family"]]} for c in cases]

def judge_all(cases,outputs,provider):
    judged={}
    for start in range(0,len(cases),5):
        group=cases[start:start+5]
        payload=judge_payload(group,outputs)
        prompt=json.dumps({"task":"Grade each candidate output against the hidden case. Functional professional performance, not tone taste. 0=failure,1=usable weak,2=strong.",
          "dimensions":DIMS,"allowed_flags":FLAGS,
          "schema":{"cases":[{"family":"AV-Qx","scores":{d:2 for d in DIMS},"critical_flags":[],"pass":True,"note":"short observable reason"}]},
          "cases":payload},ensure_ascii=False)
        system="You are a blinded senior evaluator. Do not reward profanity, aggression, verbosity or disagreement. Return JSON only."
        got=gemini(system,prompt,GEMINI_JUDGE,True) if provider=="gemini" else groq(system,prompt,True)
        rows=got.get("cases") if isinstance(got,dict) else None
        if not isinstance(rows,list): raise RuntimeError("judge shape invalid")
        for r in rows:
            if isinstance(r,dict) and r.get("family"): judged[r["family"]]=r
    if set(judged)!=set(c["family"] for c in cases): raise RuntimeError("judge coverage incomplete")
    return judged

def practical_review():
    failed=github_blob("prostoali2207-gif/personal-brand-growth-system",PBGS_FAILED)
    stress=github_blob("prostoali2207-gif/personal-brand-growth-system",PBGS_STRESS)
    orient=github_blob("prostoali2207-gif/personal-brand-growth-system",PBGS_ORIENTATION)
    baseline=json.loads(DEV2.read_text())["cases"][1]["baseline"]
    payload={"task":"Compare practical artifacts for creator-native execution while preserving truth/strategy.",
      "A_parent_style_baseline":baseline,"B_historical_failed_v02":failed,"C_v04_stress_test":stress,"additional_current_orientation":orient,
      "required":["C materially reduces safe pedagogic collapse versus A/B","truth and strategy preserved","no reference imitation","no fake spontaneity shortcut","no acoustic-performance overclaim"],
      "schema":{"pass":True,"scores":{"creator_native_execution":2,"truth_preservation":2,"strategy_preservation":2,"anti_imitation":2},"critical_flags":[],"note":"short"}}
    p=json.dumps(payload,ensure_ascii=False)
    sys="You are a blinded practical evaluator for authorial voice. Judge artifacts, not rationale. Return JSON only."
    return {"gemini":gemini(sys,p,GEMINI_JUDGE,True),"groq":groq(sys,p,True)}

def main():
    try:
        # exact identity verification
        import subprocess
        for path,sha in [(PARENT,PARENT_SHA),(OVERLAY,OVERLAY_SHA),(PROTO,PROTO_SHA)]:
            observed=subprocess.check_output(["git","hash-object",str(path)],text=True).strip()
            if observed!=sha: raise RuntimeError(f"identity mismatch {path}: {observed}")
        cases=author_cases()
        outputs=candidate_outputs(cases,PARENT.read_text(),OVERLAY.read_text())
        ja=judge_all(cases,outputs,"gemini")
        jb=judge_all(cases,outputs,"groq")
        practical=practical_review()

        results={}; flags=[]
        for c in cases:
            fid=c["family"]; a=ja[fid]; b=jb[fid]
            material=set(c.get("material_dimensions") or [])
            pass_case=bool(a.get("pass")) and bool(b.get("pass"))
            pass_case=pass_case and not a.get("critical_flags") and not b.get("critical_flags")
            for req in ["truth_preservation","brief_fidelity","authority_boundary","anti_imitation"]:
                pass_case=pass_case and int((a.get("scores") or {}).get(req,0))>=1 and int((b.get("scores") or {}).get(req,0))>=1
            rel=[]
            for d in material:
                if d in DIMS:
                    av=int((a.get("scores") or {}).get(d,0)); bv=int((b.get("scores") or {}).get(d,0))
                    pass_case=pass_case and av>=1 and bv>=1; rel += [av,bv]
            mean=(sum(rel)/len(rel)) if rel else 2.0
            pass_case=pass_case and mean>=1.5
            flags += list(a.get("critical_flags") or [])+list(b.get("critical_flags") or [])
            results[fid]={"pass":bool(pass_case),"relevant_mean":round(mean,3),"judge_a":a,"judge_b":b}

        practical_pass=all(bool(x.get("pass")) and not x.get("critical_flags") for x in practical.values())
        overall=all(x["pass"] for x in results.values()) and practical_pass and not flags
        report={"schema_version":"1.0.0","issue":302,
          "candidate":{"parent_blob":PARENT_SHA,"overlay_blob":OVERLAY_SHA,"protocol_blob":PROTO_SHA,"status":"CANDIDATE_NOT_QUALIFIED"},
          "providers":{"author":GROQ_MODEL,"candidate":GEMINI_CANDIDATE,"judge_a":GEMINI_JUDGE,"judge_b":GROQ_MODEL},
          "hidden_case_count":len(cases),"hidden_passed":sum(x["pass"] for x in results.values()),
          "practical_pass":practical_pass,"critical_flags":sorted(set(flags)),
          "overall_pass":overall,"case_results":results,"practical":practical,
          "scope_note":"PASS, if achieved, applies only to text-level Authorial Voice extension on this runtime; vocal performance remains separate."}
        SAN.write_text(json.dumps({k:v for k,v in report.items() if k not in ("case_results","practical")},ensure_ascii=False,indent=2)+"\n")
        FULL.write_text(json.dumps({"report":report,"hidden_cases":cases,"candidate_outputs":outputs},ensure_ascii=False,indent=2)+"\n")
        print(SAN.read_text())
        return 0 if overall else 1
    except Exception as e:
        report={"schema_version":"1.0.0","issue":302,"status":"NOT_EXECUTABLE","error_class":type(e).__name__,"error":str(e)[:1200]}
        SAN.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
        print(SAN.read_text())
        return 2

if __name__=="__main__":
    raise SystemExit(main())
