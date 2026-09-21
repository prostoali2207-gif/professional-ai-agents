#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, os, subprocess, urllib.error, urllib.request

CANDIDATE_COMMIT="7b0529ed3c865f6e2dcc8ca605ef07c37002f194"
CANDIDATE_DIGEST="sha256:b9aebed05ff76955a88035b79d31a81aebe5c5d52cb029f7ce9a337f67ec2fe1"
PROVIDER="gemini-interactions-api"
DEFAULT_MODEL="gemini-3.5-flash-lite"
PROTOCOL="trfm-candidate-v0.1.1"
ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"

COMPONENTS={
"architect/evaluation/training-recovery-fatigue-management/candidate/SKILL.md":"b56c8048ed1066ef2695f84367b37adfb11ef967",
"architect/evaluation/training-recovery-fatigue-management/candidate/state.schema.json":"1b0dbf3d483ca1589cd0d2b8d02503b5d714ea4e",
"architect/evaluation/training-recovery-fatigue-management/knowledge-packaging-audit-v0.1.md":"f4202162ff4e4aad78649281ec3c1a05f2852ec0",
"architect/research/training-recovery-fatigue-management/competency-and-judgment-model-v0.1.md":"052015797095e7ece339a3a0b471d41ec616f594",
"architect/research/training-recovery-fatigue-management/evidence-register-v0.2.md":"0ae2a3727f4353330e8d6b0ef5d2101c3777d6c7",
"architect/research/training-recovery-fatigue-management/professional-repair-overlay-v0.1.1.md":"7b1a1cb8423fce5c75f3e388acbe433a20f1eed0",
"architect/research/training-recovery-fatigue-management/runtime-state-contract-v0.1.md":"9786c4f7c800603d1ddcb2a3946550b7dd66008a",
}

CLASSIFICATIONS=["NORMAL_ADAPTIVE_FATIGUE","LOCAL_MUSCLE_FATIGUE","TRANSIENT_UNDERPERFORMANCE","UNDER_RECOVERY_TREND","SYSTEMIC_FATIGUE_PATTERN","PLATEAU_CANDIDATE","DELOAD_CANDIDATE","INSUFFICIENT_EVIDENCE","MEDICAL_ESCALATION"]
ACTIONS=["CONTINUE","SESSION_LOCAL_MODIFY","TARGETED_VOLUME_REDUCTION","TARGETED_VOLUME_INCREASE","TARGETED_FAILURE_REDUCTION","REDISTRIBUTE_FREQUENCY","EXERCISE_SUBSTITUTION","BROAD_DELOAD","GATHER_EVIDENCE","MEDICAL_ESCALATION"]
PRIMARY=["NONE","VOLUME","PROXIMITY_TO_FAILURE","FREQUENCY_DISTRIBUTION","EXERCISE_SELECTION","RECOVERY_CONTEXT"]
FLAGS=["SINGLE_OBSERVATION_ONLY","NONCOMPARABLE_PERFORMANCE","WEARABLE_NOT_SOLE_AUTHORITY","SUBJECTIVE_SINGLE_ITEM_NOT_CALIBRATED","SORENESS_NOT_GROWTH_SCORE","HISTORY_CONSULTED","MISSING_NOT_NORMAL","MEDICAL_NO_DIAGNOSIS","PRESERVE_STIMULUS","REVIEW_TRIGGER_DEFINED"]

def git_blob(commit:str,path:str)->str:
    return subprocess.check_output(["git","rev-parse",f"{commit}:{path}"],text=True).strip()

def git_show(commit:str,path:str)->str:
    return subprocess.check_output(["git","show",f"{commit}:{path}"],text=True)

def verify_candidate()->str:
    canonical=""
    texts=[]
    for path in sorted(COMPONENTS):
        actual=git_blob(CANDIDATE_COMMIT,path)
        if actual!=COMPONENTS[path]:
            raise RuntimeError(f"candidate component mismatch {path}: {actual}")
        canonical+=f"{path}:{actual}\n"
        if path.endswith(".md"):
            texts.append(f"\n--- {path} ---\n"+git_show(CANDIDATE_COMMIT,path))
    digest="sha256:"+hashlib.sha256(canonical.encode()).hexdigest()
    if digest!=CANDIDATE_DIGEST:
        raise RuntimeError(f"candidate digest mismatch {digest}")
    return "".join(texts)

def extract_text(raw:dict)->str:
    if isinstance(raw.get("output_text"),str) and raw["output_text"].strip():
        return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            content=step.get("content")
            if isinstance(content,str) and content.strip():
                return content
            for item in content or []:
                if isinstance(item,dict) and item.get("type")=="text" and isinstance(item.get("text"),str) and item["text"].strip():
                    return item["text"]
    raise RuntimeError("provider response contains no observable text")

def parse_json(text:str)->dict:
    t=text.strip()
    if t.startswith("~~~"):
        t="\n".join(t.splitlines()[1:-1]).strip()
    start=t.find("{"); end=t.rfind("}")
    if start>=0 and end>=start:
        t=t[start:end+1]
    obj=json.loads(t)
    if not isinstance(obj,dict):
        raise RuntimeError("candidate output must be object")
    return obj

def validate_decision(x:dict)->dict:
    required=["classification","action","primary_variable","flags","review_trigger","reasoning_summary"]
    for k in required:
        if k not in x:
            raise RuntimeError(f"candidate output missing {k}")
    if x["classification"] not in CLASSIFICATIONS:
        raise RuntimeError("invalid classification")
    if x["action"] not in ACTIONS:
        raise RuntimeError("invalid action")
    if x["primary_variable"] not in PRIMARY:
        raise RuntimeError("invalid primary_variable")
    if not isinstance(x["flags"],list) or any(v not in FLAGS for v in x["flags"]):
        raise RuntimeError("invalid flags")
    if len(set(x["flags"]))!=len(x["flags"]):
        raise RuntimeError("duplicate flags")
    if not isinstance(x["review_trigger"],str) or not x["review_trigger"].strip():
        raise RuntimeError("review_trigger required")
    if not isinstance(x["reasoning_summary"],str) or not x["reasoning_summary"].strip():
        raise RuntimeError("reasoning_summary required")
    return x

def contract()->dict:
    return {"contract_version":1,"candidate_commit":CANDIDATE_COMMIT,"candidate_digest":CANDIDATE_DIGEST,"provider":PROVIDER,"input_protocol":PROTOCOL,"tool_protocol":"none-v1","state_protocol":"external-longitudinal-state-v1","observable_protocol":"structured-decision-v1","allowed_classifications":CLASSIFICATIONS,"allowed_actions":ACTIONS,"allowed_flags":FLAGS}

def call(candidate:str,task:str,state:dict,timeout:int)->tuple[dict,dict]:
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")
    model=os.environ.get("TRFM_MODEL",DEFAULT_MODEL)
    schema_text=json.dumps({"classification":CLASSIFICATIONS,"action":ACTIONS,"primary_variable":PRIMARY,"flags":FLAGS,"review_trigger":"non-empty string","reasoning_summary":"brief evidence-based explanation"},ensure_ascii=False)
    system=("You are executing the exact frozen Training Recovery & Fatigue Management candidate below. "
            "Use only the supplied task facts and longitudinal state. Do not invent missing observations. "
            "Operational fatigue labels are not medical diagnoses. Return JSON only, no markdown. "
            "Choose exactly one classification, one action and one primary_variable. Include every materially required flag. "
            "A structural training change means anything beyond CONTINUE, SESSION_LOCAL_MODIFY or GATHER_EVIDENCE. "
            f"OUTPUT CONTRACT: {schema_text}\n\nFROZEN CANDIDATE:\n{candidate}")
    inp=json.dumps({"task":task,"longitudinal_state":state},ensure_ascii=False)
    payload={"model":model,"system_instruction":system,"input":inp,"store":False,"generation_config":{"thinking_level":"medium"}}
    req=urllib.request.Request(ENDPOINT,data=json.dumps(payload,ensure_ascii=False).encode(),method="POST",headers={"Content-Type":"application/json","x-goog-api-key":key})
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            raw=json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"provider HTTP {exc.code}: {exc.read().decode(errors='replace')[:1200]}") from exc
    decision=validate_decision(parse_json(extract_text(raw)))
    return decision,{"provider":PROVIDER,"model":model,"interaction_id":raw.get("id"),"usage":raw.get("usage") or raw.get("usageMetadata")}

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--qualification-contract",action="store_true")
    p.add_argument("--verify-candidate",action="store_true")
    p.add_argument("--canary",action="store_true")
    p.add_argument("--model-timeout",type=int,default=150)
    args=p.parse_args()
    if args.qualification_contract:
        print(json.dumps(contract(),sort_keys=True))
        return 0
    if args.verify_candidate:
        verify_candidate()
        print(json.dumps({"status":"candidate_verified","candidate_commit":CANDIDATE_COMMIT,"candidate_digest":CANDIDATE_DIGEST},sort_keys=True))
        return 0
    candidate=verify_candidate()
    if args.canary:
        task="One poor bench session after one unusually short night. No injury or illness concern; previous matched sessions were progressing. Decide whether to rewrite the program."
        state={"observations":[],"sessions":[],"performance_anchors":[],"load_history":[],"interventions":[]}
    else:
        payload=json.load(__import__("sys").stdin)
        if not isinstance(payload,dict) or not isinstance(payload.get("task"),str) or not isinstance(payload.get("state"),dict):
            raise RuntimeError("stdin requires object with task:string and state:object")
        task,state=payload["task"],payload["state"]
    decision,transport=call(candidate,task,state,args.model_timeout)
    print(json.dumps({"status":"completed","candidate_identity":{"commit":CANDIDATE_COMMIT,"digest":CANDIDATE_DIGEST,"runtime":"trfm-gemini-v0.1.1","provider":PROVIDER,"model":transport["model"]},"decision":decision,"transport":transport},ensure_ascii=False))
    return 0

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status":"runtime_error","error":str(exc)},ensure_ascii=False))
        raise SystemExit(2)
