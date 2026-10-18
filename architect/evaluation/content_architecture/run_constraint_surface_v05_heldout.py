#!/usr/bin/env python3
from __future__ import annotations
import base64, json, os, re, subprocess, time, urllib.error, urllib.request
from pathlib import Path
from typing import Any

ROOT=Path.cwd()
OUT=ROOT/".tmp/content-architecture-v05-heldout"
OUT.mkdir(parents=True,exist_ok=True)
SAN=OUT/"sanitized-report.json"
FULL=OUT/"full-consumed-evidence.json"

GEMINI_ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
GROQ_ENDPOINT="https://api.groq.com/openai/v1/chat/completions"
GEMINI_CANDIDATE=os.environ.get("CA_V05_CANDIDATE_MODEL","gemini-3.5-flash-lite")
GEMINI_JUDGE=os.environ.get("CA_V05_GEMINI_JUDGE_MODEL","gemini-3.5-flash-lite")
GROQ_MODEL=os.environ.get("CA_V05_GROQ_MODEL","qwen/qwen3.6-27b")

BASELINE_SHA="5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
OVERLAY=ROOT/"architect/research/content-architecture/constraint-surface-overlay-v0.5.md"
PROTO=ROOT/"architect/research/content-architecture/constraint-surface-qualification-protocol-v0.1.md"
OVERLAY_SHA="74942d09593f73d0a9a23be068d3bbf3a0b8c06d"
PROTO_SHA="d90c9daab6256fce3388025db7a656dc06489f1a"

SURFACES={"INTERNAL_ONLY","PUBLIC_MESSAGE_CANDIDATE","PUBLIC_MESSAGE_REQUIRED"}
DIMS=["surface_classification_accuracy","negative_constraint_invisibility","public_message_justification",
"required_disclosure_preservation","handoff_clarity","truth_preservation","brief_fidelity","authority_boundary"]
FLAGS=["INTERNAL_CONSTRAINT_TO_PUBLIC_MESSAGE_LEAK","USER_FEEDBACK_OVERLITERALIZATION",
"REQUIRED_PUBLIC_DISCLOSURE_SUPPRESSED","UNSUPPORTED_CLAIM_STRENGTHENING",
"EXPERIMENT_LOCK_PUBLIC_LEAK","EXPLICIT_PUBLIC_REQUIREMENT_SUPPRESSED"]

CATEGORY_COUNTS={"internal_only":4,"public_candidate":2,"public_required":2,"silent_lock":2,"compatibility":2}

def out_text(raw:dict)->str:
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            c=step.get("content")
            if isinstance(c,str): return c
            for x in c or []:
                if isinstance(x,dict) and x.get("type")=="text" and isinstance(x.get("text"),str): return x["text"]
    return ""

def parse(s:str)->Any:
    s=s.strip()
    if s.startswith("```"):
        s=re.sub(r"^```(?:json)?\s*","",s,flags=re.I); s=re.sub(r"\s*```$","",s)
    try:return json.loads(s)
    except: pass
    for a in [i for i,c in enumerate(s) if c in "[{"]:
        for b in range(len(s),a,-1):
            if s[b-1] not in "]}": continue
            try:return json.loads(s[a:b])
            except: pass
    raise ValueError("invalid JSON")

def gemini(system,prompt,model,format_retry=False):
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing")
    def once(p):
        body={"model":model,"store":False,"system_instruction":system,"input":[{"type":"user_input","content":p}]}
        for attempt in range(2):
            req=urllib.request.Request(GEMINI_ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",
              headers={"x-goog-api-key":key,"Content-Type":"application/json","User-Agent":"ca-v05-heldout/1.0"})
            try:
                with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
                t=out_text(raw)
                if not t: raise RuntimeError("empty Gemini output")
                return t
            except urllib.error.HTTPError as e:
                msg=e.read().decode(errors="replace")
                if e.code in (500,503) and attempt==0:
                    time.sleep(3); continue
                raise RuntimeError(f"Gemini HTTP {e.code}: {msg[:900]}")
    t=once(prompt)
    try:return parse(t)
    except:
        if not format_retry: raise
        return parse(once(prompt+"\nReturn valid JSON only. No markdown."))

def groq(system,prompt,format_retry=False):
    key=os.environ.get("GROQ_API_KEY","").strip()
    if not key: raise RuntimeError("GROQ_API_KEY missing")
    def once(p):
        body={"model":GROQ_MODEL,"messages":[{"role":"system","content":system},{"role":"user","content":p}],
          "temperature":0,"reasoning_format":"hidden","response_format":{"type":"json_object"}}
        req=urllib.request.Request(GROQ_ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",
          headers={"Authorization":"Bearer "+key,"Content-Type":"application/json","Accept":"application/json","User-Agent":"ca-v05-heldout/1.0"})
        try:
            with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
            return raw["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Groq HTTP {e.code}: {e.read().decode(errors='replace')[:900]}")
    t=once(prompt)
    try:return parse(t)
    except:
        if not format_retry: raise
        return parse(once(prompt+"\nReturn valid JSON only. No markdown."))

def github_blob(sha):
    token=os.environ.get("GITHUB_TOKEN","").strip()
    if not token: raise RuntimeError("GITHUB_TOKEN missing")
    req=urllib.request.Request(f"https://api.github.com/repos/prostoali2207-gif/professional-ai-agents/git/blobs/{sha}",
      headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json","User-Agent":"ca-v05-heldout/1.0"})
    with urllib.request.urlopen(req,timeout=30) as r: x=json.loads(r.read().decode())
    return base64.b64decode(x["content"]).decode()

def author_cases():
    plan=[]
    idx=1
    for category,count in CATEGORY_COUNTS.items():
        for _ in range(count):
            plan.append({"id":f"H{idx:02d}","category":category}); idx+=1
    # Pre-assign two contrast pairs so author cannot omit them.
    plan[0]["pair_id"]="PAIR-A"; plan[4]["pair_id"]="PAIR-A"; plan[0]["pair_type"]="audience_job_shift"; plan[4]["pair_type"]="audience_job_shift"
    plan[1]["pair_id"]="PAIR-B"; plan[6]["pair_id"]="PAIR-B"; plan[1]["pair_type"]="high_importance_surface_shift"; plan[6]["pair_type"]="high_importance_surface_shift"

    batches=[]
    for start in range(0,len(plan),4):
        group=plan[start:start+4]
        prompt=json.dumps({
          "task":"Author fresh hidden Content Architecture constraint-surface cases. Each item must contain one primary material constraint/input and enough context to determine whether it belongs in audience-facing semantic architecture. Do not reuse visible examples.",
          "assigned_slots":group,
          "category_rules":{
            "internal_only":"important internal guard/user feedback/negative constraint; expected INTERNAL_ONLY",
            "public_candidate":"truthful explicit audience-message request or audience-relevant proposition requiring validation; expected PUBLIC_MESSAGE_CANDIDATE",
            "public_required":"legal/safety/functional/communication requirement whose omission breaks audience task; expected PUBLIC_MESSAGE_REQUIRED",
            "silent_lock":"experiment/truth/provenance implementation lock that must be preserved but not verbalized; expected INTERNAL_ONLY",
            "compatibility":"broader v0.4 brief/handoff/authority case; choose expected surface from facts and justify it"
          },
          "visible_examples_to_avoid":["landing to CRM dependency","AI as front door","do not invent results","ORIENTATION-01","prior content over-emphasized CRM"],
          "schema":{"cases":[{
            "id":"assigned id","category":"assigned category","pair_id":"assigned or empty","pair_type":"assigned or empty",
            "scenario":"self-contained facts + communication job + constraint",
            "expected_surface_class":"INTERNAL_ONLY|PUBLIC_MESSAGE_CANDIDATE|PUBLIC_MESSAGE_REQUIRED",
            "expected_observables":["..."],"forbidden_behaviors":["..."],"reference_rationale":"evaluator-only"
          }]}
        },ensure_ascii=False)
        got=groq("You are an independent senior Content Architecture evaluation author. Return JSON only.",prompt,True)
        rows=got.get("cases") if isinstance(got,dict) else None
        if not isinstance(rows,list) or len(rows)!=len(group): raise RuntimeError("author batch invalid")
        by={r.get("id"):r for r in rows if isinstance(r,dict)}
        for slot in group:
            r=by.get(slot["id"])
            if not r: raise RuntimeError("missing authored case "+slot["id"])
            if r.get("category")!=slot["category"]: raise RuntimeError("category drift "+slot["id"])
            r["pair_id"]=slot.get("pair_id",""); r["pair_type"]=slot.get("pair_type","")
            if r.get("expected_surface_class") not in SURFACES: raise RuntimeError("bad expected surface")
            batches.append(r)
    return batches

def validate_pack(cases):
    if len(cases)!=12: raise RuntimeError("need 12 cases")
    counts={k:0 for k in CATEGORY_COUNTS}
    for c in cases: counts[c["category"]]+=1
    if counts!=CATEGORY_COUNTS: raise RuntimeError("category counts drift")
    pairs={}
    for c in cases:
        if c.get("pair_id"): pairs.setdefault(c["pair_id"],[]).append(c)
    if set(pairs)!={"PAIR-A","PAIR-B"} or any(len(v)!=2 for v in pairs.values()): raise RuntimeError("pair structure invalid")
    for pid,rows in pairs.items():
        if rows[0]["expected_surface_class"]==rows[1]["expected_surface_class"]:
            raise RuntimeError(pid+" must require different surface classes")

def candidate_outputs(cases,baseline,overlay):
    system=("You are executing exact qualified Content Architecture v0.4 plus the v0.5 Constraint Surface candidate overlay. "
      "v0.5 is CANDIDATE / NOT QUALIFIED. Preserve all v0.4 truth, brief, proof, experiment, authority and handoff requirements. "
      "Architecture is not final copy. Return JSON only.\n---v0.4---\n"+baseline+"\n---v0.5 OVERLAY---\n"+overlay)
    out={}
    for c in cases:
        prompt=json.dumps({"scenario":c["scenario"],
          "task":"Classify the material input surface and produce the architecture/handoff consequence.",
          "schema":{"surface_class":"INTERNAL_ONLY|PUBLIC_MESSAGE_CANDIDATE|PUBLIC_MESSAGE_REQUIRED",
            "communication_job":"concise","information_order":["public semantic blocks only"],"silent_locks":["preserve silently"],
            "handoff":"may/must/must-not verbalize","professional_reason":"concise"}},ensure_ascii=False)
        x=gemini(system,prompt,GEMINI_CANDIDATE,False)
        if x.get("surface_class") not in SURFACES: raise RuntimeError("candidate invalid surface "+c["id"])
        out[c["id"]]=x
    return out

def judge(cases,outputs,provider):
    judged={}
    for start in range(0,len(cases),4):
        group=cases[start:start+4]
        items=[]
        for c in group:
            items.append({"id":c["id"],"scenario":c["scenario"],"expected_surface_class":c["expected_surface_class"],
              "expected_observables":c.get("expected_observables",[]),"forbidden_behaviors":c.get("forbidden_behaviors",[]),
              "reference_rationale":c.get("reference_rationale",""),"candidate_output":outputs[c["id"]]})
        prompt=json.dumps({"task":"Grade candidate architecture. Do not reward meta-explanation; internal guards normally disappear from public information order unless independently required.",
          "dimensions":DIMS,"allowed_flags":FLAGS,
          "schema":{"cases":[{"id":"H01","scores":{d:2 for d in DIMS},"critical_flags":[],"pass":True,"note":"short"}]},
          "cases":items},ensure_ascii=False)
        sys="You are a blinded senior Content Architecture evaluator. Return JSON only."
        got=gemini(sys,prompt,GEMINI_JUDGE,True) if provider=="gemini" else groq(sys,prompt,True)
        rows=got.get("cases") if isinstance(got,dict) else None
        if not isinstance(rows,list): raise RuntimeError("judge batch invalid")
        for r in rows:
            if isinstance(r,dict) and r.get("id"): judged[r["id"]]=r
    if set(judged)!=set(c["id"] for c in cases): raise RuntimeError("judge coverage incomplete")
    return judged

def main():
    try:
        if subprocess.check_output(["git","hash-object",str(OVERLAY)],text=True).strip()!=OVERLAY_SHA: raise RuntimeError("overlay identity mismatch")
        if subprocess.check_output(["git","hash-object",str(PROTO)],text=True).strip()!=PROTO_SHA: raise RuntimeError("protocol identity mismatch")
        cases=author_cases(); validate_pack(cases)
        baseline=github_blob(BASELINE_SHA)
        outputs=candidate_outputs(cases,baseline,OVERLAY.read_text())
        ja=judge(cases,outputs,"gemini"); jb=judge(cases,outputs,"groq")
        results={}; flags=[]
        for c in cases:
            cid=c["id"]; a=ja[cid]; b=jb[cid]
            mechanical=outputs[cid].get("surface_class")==c["expected_surface_class"]
            p=mechanical and bool(a.get("pass")) and bool(b.get("pass")) and not a.get("critical_flags") and not b.get("critical_flags")
            vals=[]
            for d in DIMS:
                av=int((a.get("scores") or {}).get(d,0)); bv=int((b.get("scores") or {}).get(d,0))
                p=p and av>=1 and bv>=1; vals += [av,bv]
            mean=sum(vals)/len(vals)
            p=p and mean>=1.5
            flags += list(a.get("critical_flags") or [])+list(b.get("critical_flags") or [])
            results[cid]={"pass":bool(p),"mechanical_surface_pass":mechanical,"mean":round(mean,3),"judge_a":a,"judge_b":b}
        pair_pass=True
        for pid in ("PAIR-A","PAIR-B"):
            rows=[c for c in cases if c.get("pair_id")==pid]
            observed=[outputs[c["id"]]["surface_class"] for c in rows]
            expected=[c["expected_surface_class"] for c in rows]
            pair_pass=pair_pass and observed==expected and observed[0]!=observed[1]
        overall=all(x["pass"] for x in results.values()) and pair_pass and not flags
        report={"schema_version":"1.0.0","issue":306,
          "candidate":{"baseline_blob":BASELINE_SHA,"overlay_blob":OVERLAY_SHA,"protocol_blob":PROTO_SHA,"status":"CANDIDATE_NOT_QUALIFIED"},
          "providers":{"author":GROQ_MODEL,"candidate":GEMINI_CANDIDATE,"judge_a":GEMINI_JUDGE,"judge_b":GROQ_MODEL},
          "hidden_case_count":12,"hidden_passed":sum(x["pass"] for x in results.values()),"pair_pass":pair_pass,
          "critical_flags":sorted(set(flags)),"overall_pass":overall,"case_results":results,
          "scope_note":"Targeted qualification of constraint-surface revision only; v0.4 prior evidence remains scoped to unchanged constructs."}
        SAN.write_text(json.dumps({k:v for k,v in report.items() if k!="case_results"},ensure_ascii=False,indent=2)+"\n")
        FULL.write_text(json.dumps({"report":report,"hidden_cases":cases,"candidate_outputs":outputs},ensure_ascii=False,indent=2)+"\n")
        print(SAN.read_text())
        return 0 if overall else 1
    except Exception as e:
        report={"schema_version":"1.0.0","issue":306,"status":"NOT_EXECUTABLE","error_class":type(e).__name__,"error":str(e)[:1200]}
        SAN.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
        print(SAN.read_text()); return 2

if __name__=="__main__":
    raise SystemExit(main())
