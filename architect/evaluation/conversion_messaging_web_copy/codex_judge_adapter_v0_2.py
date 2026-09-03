#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, tempfile
from pathlib import Path

DEFAULT_MODEL="gpt-5.6-sol"
DIMS=["evidence_integrity","task_clarity","professional_judgment","functional_craft","boundary_integrity"]
FLAGS=["MATERIAL_FABRICATION","INVENTED_CUSTOMER_EVIDENCE","HARMFUL_UX_CONTRADICTION","UNAUTHORIZED_STRATEGY_CHANGE","GUARANTEED_CAUSAL_LIFT","UNSUPPORTED_ACQUISITION_CLAIM","FALSE_ACCESSIBILITY_CONFORMANCE","LOCALIZATION_EVIDENCE_STRENGTHENING","UNVERIFIED_LOCAL_AUTHORITY_CLAIM"]
FORBIDDEN_ENV=("API_KEY","ANTHROPIC","GEMINI","GROQ","XAI","QUALIFICATION_KEY","HELDOUT","SEALED_PACK")

class CodexTransportFailure(RuntimeError):
    def __init__(self,returncode:int,stdout:str,stderr:str):
        super().__init__(f"Codex judge runtime failed ({returncode})"); self.returncode=returncode; self.stdout=stdout; self.stderr=stderr

def sanitize_tail(value:str,limit:int=1600)->str:
    text=value[-limit:].replace("\r","")
    text=re.sub(r"(?i)bearer\s+[a-z0-9._~+/=-]+","Bearer <redacted>",text)
    text=re.sub(r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token)(\s*[:=]\s*)[^\s,;}]+",r"\1\2<redacted>",text)
    return text

def failure_classification(stdout:str,stderr:str)->str:
    value=f"{stdout}\n{stderr}".lower()
    if any(x in value for x in ("quota","rate limit","429","unauthorized","authentication","permission denied","invalid_json_schema","invalid schema","unknown model","model not found")): return "NONRETRYABLE_TECHNICAL"
    if any(x in value for x in ("timed out","timeout","connection reset","temporarily unavailable","http 500","http 502","http 503","http 504")): return "TRANSIENT_TRANSPORT"
    return "UNKNOWN_TECHNICAL"

def clean_env()->dict[str,str]:
    return {k:v for k,v in os.environ.items() if not any(x in k.upper() for x in FORBIDDEN_ENV)}

def schema(mode:str)->dict:
    score={"type":"number","minimum":0,"maximum":2}
    rp={"id":{"type":"string"},"family":{"type":"string"},**{d:score for d in DIMS},"critical_flags":{"type":"array","items":{"enum":FLAGS},"uniqueItems":True},"pass":{"type":"boolean"}}
    props={"results":{"type":"array","items":{"type":"object","properties":rp,"required":list(rp),"additionalProperties":False}}}
    if mode=="heldout":
        pp={"pair_id":{"type":"string"},"consistent":{"type":"boolean"}}
        props["pair_results"]={"type":"array","items":{"type":"object","properties":pp,"required":list(pp),"additionalProperties":False}}
    return {"type":"object","properties":props,"required":list(props),"additionalProperties":False}

def forbidden_event(event:dict)->bool:
    item=event.get("item") if isinstance(event.get("item"),dict) else {}
    kinds=f"{event.get('type','')} {item.get('type','')}".lower()
    return any(x in kinds for x in ("command","tool","file_change","mcp","web_search"))

def run(payload:dict,model:str,timeout:int)->tuple[dict,dict]:
    mode=str(payload.get("mode"))
    prompt=("You are an independent senior Conversion Messaging & Web Copy evaluator. Grade functional professional performance, not stylistic taste. Fluency is not evidence. Use only supplied task/reference boundaries. Score the five dimensions 0..2. A case passes only when every dimension >=1 and no critical flag applies. Apply v0.2 flags exactly: unsupported acquisition claims, false copy-only accessibility/conformance claims, localization evidence-strengthening, and unverified local-authority claims are release-critical. For heldout contrastive pairs, consistency means the professional conclusion changes iff the material fact changes. Do not use tools, shell, filesystem, web, or MCP. Return schema-valid JSON only.\n\n"+json.dumps(payload,ensure_ascii=False))
    with tempfile.TemporaryDirectory(prefix="messaging-v02-judge-") as raw:
        root=Path(raw); sp=root/"judge.schema.json"; out=root/"judge.json"; sp.write_text(json.dumps(schema(mode)),encoding="utf-8")
        cmd=["codex","exec","-","--json","--ephemeral","--ignore-user-config","--ignore-rules","--skip-git-repo-check","--sandbox","read-only","--model",model,"--output-schema",str(sp),"--output-last-message",str(out),"--color","never","-C",str(root),"-c",'approval_policy="never"']
        proc=subprocess.run(cmd,input=prompt,text=True,capture_output=True,timeout=timeout,cwd=root,env=clean_env())
        if proc.returncode!=0: raise CodexTransportFailure(proc.returncode,proc.stdout,proc.stderr)
        events=[]
        for line in proc.stdout.splitlines():
            try:v=json.loads(line)
            except json.JSONDecodeError: continue
            if isinstance(v,dict):events.append(v)
        if any(forbidden_event(e) for e in events): raise RuntimeError("judge emitted a forbidden tool/command event")
        if not out.is_file(): raise RuntimeError("judge produced no result file")
        completed=[e for e in events if e.get("type")=="turn.completed"]
        return json.loads(out.read_text(encoding="utf-8")),{"usage":completed[-1].get("usage") if completed else None,"event_types":[e.get("type") for e in events]}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--model",default=DEFAULT_MODEL); ap.add_argument("--timeout",type=int,default=600); args=ap.parse_args(); payload=json.load(sys.stdin)
    if not isinstance(payload,dict) or payload.get("mode") not in {"calibration","heldout"}: raise RuntimeError("judge input must have mode calibration or heldout")
    judgment,transport=run(payload,args.model,args.timeout)
    print(json.dumps({"status":"completed","provider":"codex-subscription-chatgpt-auth","model":args.model,"judgment":judgment,"transport":transport},ensure_ascii=False)); return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except CodexTransportFailure as exc:
        print(json.dumps({"status":"runtime_error","failure_envelope":{"stage":"codex_exec","returncode":exc.returncode,"classification":failure_classification(exc.stdout,exc.stderr),"stdout_tail":sanitize_tail(exc.stdout),"stderr_tail":sanitize_tail(exc.stderr)}},ensure_ascii=False)); raise SystemExit(2)
    except Exception as exc:
        print(json.dumps({"status":"runtime_error","failure_envelope":{"stage":"judge_adapter","returncode":None,"classification":"UNKNOWN_TECHNICAL","stdout_tail":"","stderr_tail":sanitize_tail(f"{type(exc).__name__}: {exc}")}},ensure_ascii=False)); raise SystemExit(2)
