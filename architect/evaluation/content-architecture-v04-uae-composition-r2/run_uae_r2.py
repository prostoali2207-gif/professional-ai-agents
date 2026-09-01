#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, hashlib, hmac, json, os, subprocess, sys, time
from pathlib import Path
from cryptography.fernet import Fernet

GATE_ID="content-architecture-v0.4-uae-composition-2026-09-01-r2"
CORE_SHA="5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
SPECIALIZATION_SHA="7f41c2d1ba40c3b4c59e3eba2fb264c04162c320"
JUDGE_SHA="669cdfcd0195d0507637d377b48f2650b4a870dd"
ADAPTER=Path("architect/evaluation/harness/adapters/codex_frozen_artifact_adapter.py")
ASSEMBLY_VERSION="content-architecture-uae-composition-v1"
DECISION_CLASSES={"COMMERCIAL_CLAIM","UNIT_FACT","PROOF_SCOPE","STRATEGY_LOCK","EXPERIMENT_LOCK"}
RESOLUTIONS={"ALLOW","WITHHOLD","DEFER"}
EVIDENCE_BASES={"VERIFIED_UNIT_RECORD","CURRENT_UNIT_PROOF","MODEL_CONTEXT_ONLY","MARKET_CONTEXT_ONLY","UNVERIFIED","SUPERSEDED",None}


def derive(master:bytes,label:bytes)->bytes:
    return hmac.new(master,GATE_ID.encode()+b"|"+label,hashlib.sha256).digest()

def canon(obj)->bytes:
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()

def parse_json(text:str)->dict:
    text=(text or "").strip()
    if text.startswith("```"):
        lines=text.splitlines(); text="\n".join(lines[1:-1]).strip()
    try: obj=json.loads(text)
    except Exception:
        s=text.find("{"); e=text.rfind("}")
        if s<0 or e<=s: raise ValueError("no JSON object")
        obj=json.loads(text[s:e+1])
    if not isinstance(obj,dict): raise ValueError("JSON output is not an object")
    return obj

def git_blob(sha:str)->str:
    k=subprocess.run(["git","cat-file","-t",sha],capture_output=True,text=True)
    if k.returncode!=0 or k.stdout.strip()!="blob": raise RuntimeError(f"missing blob {sha}")
    p=subprocess.run(["git","cat-file","-p",sha],capture_output=True,text=False)
    if p.returncode!=0: raise RuntimeError(f"cannot read blob {sha}")
    return p.stdout.decode("utf-8")

def assemble_composed_blob()->tuple[str,str]:
    text=(git_blob(CORE_SHA).rstrip()+"\n\n--- BEGIN APPLIED UAE AUTOMOTIVE SPECIALIZATION ---\n"+git_blob(SPECIALIZATION_SHA).rstrip()+"\n--- END APPLIED UAE AUTOMOTIVE SPECIALIZATION ---\n")
    p=subprocess.run(["git","hash-object","-w","--stdin"],input=text.encode(),capture_output=True)
    if p.returncode!=0: raise RuntimeError("cannot materialize composed blob")
    sha=p.stdout.decode().strip(); ident=hashlib.sha256((ASSEMBLY_VERSION+"|"+CORE_SHA+"|"+SPECIALIZATION_SHA+"|"+sha).encode()).hexdigest()
    return sha,ident

def load_pack(path:Path)->dict:
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode().strip()
    if not master: raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    raw=Fernet(base64.urlsafe_b64encode(derive(master,b"pack"))).decrypt(path.read_bytes()); pack=json.loads(raw)
    if pack.get("gate_id")!=GATE_ID or pack.get("core_sha")!=CORE_SHA or pack.get("specialization_sha")!=SPECIALIZATION_SHA: raise RuntimeError("sealed pack identity mismatch")
    return pack

def call_artifact(sha:str,task:str,workspace:Path,timeout:int)->dict:
    workspace.mkdir(parents=True,exist_ok=True)
    payload={"protocol_version":2,"candidate_sha":sha,"workspace":str(workspace.resolve()),"input":{"task":task,"allowed_resources":[],"fixture_tools":{},"max_tool_rounds":2}}
    p=subprocess.run([sys.executable,str(ADAPTER)],input=json.dumps(payload),capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=timeout+30)
    if p.returncode!=0: raise RuntimeError("artifact runtime failed: "+((p.stdout or "")+"\n"+(p.stderr or ""))[-1400:])
    raw=parse_json(p.stdout)
    if raw.get("status")!="completed": raise RuntimeError("artifact runtime did not complete")
    if (raw.get("candidate_identity") or {}).get("sha")!=sha: raise RuntimeError("artifact identity mismatch")
    return raw

def validate_candidate_shape(obj:dict)->list[str]:
    f=[]
    if obj.get("status") not in {"READY_WITH_BOUNDS","BLOCKED","NEEDS_UPSTREAM"}: f.append("invalid status")
    ds=obj.get("decision_results")
    if not isinstance(ds,list): f.append("decision_results missing"); ds=[]
    for i,row in enumerate(ds):
        if not isinstance(row,dict): f.append(f"decision_results[{i}] not object"); continue
        if not isinstance(row.get("decision_id"),str): f.append(f"decision_results[{i}].decision_id")
        if row.get("decision_class") not in DECISION_CLASSES: f.append(f"decision_results[{i}].decision_class")
        if row.get("resolution") not in RESOLUTIONS: f.append(f"decision_results[{i}].resolution")
        if not isinstance(row.get("public_use"),bool): f.append(f"decision_results[{i}].public_use")
        if row.get("evidence_basis") not in EVIDENCE_BASES: f.append(f"decision_results[{i}].evidence_basis")
    ls=obj.get("lock_results")
    if not isinstance(ls,list): f.append("lock_results missing")
    arch=obj.get("architecture")
    if not isinstance(arch,dict): f.append("architecture missing"); arch={}
    for k in ["attention_job","block_sequence","proof_requirements","pacing_intent"]:
        if k not in arch: f.append(f"architecture.{k} missing")
    h=obj.get("creator_handoff")
    if not isinstance(h,dict): f.append("creator_handoff missing"); h={}
    for k in ["must_preserve","may_choose","blocked_portions","must_escalate"]:
        if not isinstance(h.get(k),list): f.append(f"creator_handoff.{k}")
    if not isinstance(obj.get("boundary_notes"),list): f.append("boundary_notes missing")
    return f

def mechanical_case(case:dict,obj:dict)->dict:
    failures=validate_candidate_shape(obj); hard=[]
    decisions={r.get("decision_id"):r for r in (obj.get("decision_results") or []) if isinstance(r,dict) and isinstance(r.get("decision_id"),str)}
    for did,exp in case["expected_decisions"].items():
        row=decisions.get(did)
        if not row: failures.append(f"missing decision {did}"); continue
        if row.get("public_use") is not exp["public_use"]:
            failures.append(f"{did} public_use")
            if exp["public_use"] is False and row.get("public_use") is True: hard.append(f"unsafe public use {did}")
        if row.get("resolution") not in exp["allowed_resolutions"]: failures.append(f"{did} resolution")
        if exp["evidence_required"]:
            if row.get("evidence_basis") not in exp["allowed_evidence_bases"]: failures.append(f"{did} evidence_basis")
    locks={r.get("lock_id"):r for r in (obj.get("lock_results") or []) if isinstance(r,dict) and isinstance(r.get("lock_id"),str)}
    for lid in case["expected_locks"]:
        row=locks.get(lid)
        if not row: failures.append(f"missing lock {lid}")
        elif row.get("preserved") is not True: failures.append(f"lock not preserved {lid}"); hard.append(f"lock breach {lid}")
    return {"pass":not failures,"failures":failures,"hard_failures":hard}

def calibration_task(pair:dict,dimensions:dict,a:str,b:str)->str:
    rel={k:dimensions[k] for k in pair["dimensions"]}
    return "MODE: CALIBRATE\n\nBrief:\n"+pair["brief"]+"\n\nRelevant dimensions:\n"+json.dumps(rel,ensure_ascii=False,indent=2)+"\n\nArtifact A:\n"+a+"\n\nArtifact B:\n"+b+"\n\nChoose the professionally stronger artifact. Return only calibration JSON."

def assess_task(case:dict,dimensions:dict,artifact:str)->str:
    rel={k:dimensions[k] for k in case["relevant_dimensions"]}
    return "MODE: ASSESS\n\nSynthetic evaluation brief:\n"+case["task"]+"\n\nRelevant dimensions:\n"+json.dumps(rel,ensure_ascii=False,indent=2)+"\n\nSubmitted architecture:\n"+artifact+"\n\nAssess only this architecture against the brief and rubric. Return only assessment JSON."

def validate_assessment(obj:dict,dims:list[str])->list[str]:
    f=[]
    if not isinstance(obj.get("hard_failures"),list): f.append("hard_failures not list")
    scores=obj.get("scores")
    if not isinstance(scores,dict): f.append("scores not object"); scores={}
    for d in dims:
        v=scores.get(d)
        if not isinstance(v,int) or isinstance(v,bool) or not 0<=v<=3: f.append(f"bad score {d}")
    if set(scores)-set(dims): f.append("unexpected score dimension")
    if obj.get("release_recommendation") not in {"PASS","FAIL"}: f.append("bad release_recommendation")
    return f

def run_calibrate(pack:dict,out:Path,timeout:int)->int:
    correct=0
    for pair in pack["calibration_pairs"]:
        swap=int(hashlib.sha256(f"{GATE_ID}|{pair['id']}".encode()).hexdigest()[:2],16)%2==1
        a,b=(pair["challenger"],pair["strong"]) if swap else (pair["strong"],pair["challenger"]); expected="B" if swap else "A"
        raw=call_artifact(JUDGE_SHA,calibration_task(pair,pack["dimensions"],a,b),out/"judge-calibration"/pair["id"],timeout); winner=parse_json(raw.get("final_output","")).get("winner")
        if winner not in {"A","B"}: raise RuntimeError("invalid calibration output")
        correct+=int(winner==expected)
    rate=correct/len(pack["calibration_pairs"]); passed=rate>=pack["release_policy"]["calibration_expected_winner_rate_min"]
    report={"gate_id":GATE_ID,"status":"CALIBRATION_PASS" if passed else "CALIBRATION_FAIL","candidate_calls":0,"judge_calls":len(pack["calibration_pairs"]),"expected_winner_rate":rate,"policy":pack["release_policy"]["calibration_expected_winner_rate_min"]}
    out.mkdir(parents=True,exist_ok=True); (out/"calibration-report.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(report,sort_keys=True)); return 0 if passed else 10

def run_score(pack:dict,out:Path,timeout:int)->int:
    composed_sha,composed_identity=assemble_composed_blob(); out.mkdir(parents=True,exist_ok=True)
    sanitized=[]; records=[]; scores_all=[]; mech_hard=judge_hard=0; all_judge_pass=True
    for case in pack["cases"]:
        t=time.time(); raw=call_artifact(composed_sha,case["task"],out/"candidate-work"/case["id"],timeout); artifact=raw.get("final_output",""); obj=parse_json(artifact); mech=mechanical_case(case,obj); mech_hard+=len(mech["hard_failures"])
        jr=call_artifact(JUDGE_SHA,assess_task(case,pack["dimensions"],artifact),out/"judge-work"/case["id"],timeout); assessment=parse_json(jr.get("final_output","")); shape=validate_assessment(assessment,case["relevant_dimensions"])
        if shape: raise RuntimeError(f"invalid judge assessment: {shape}")
        scores=assessment["scores"]; scores_all.extend(scores[d] for d in case["relevant_dimensions"]); hc=len(assessment["hard_failures"]); judge_hard+=hc
        jpass=assessment["release_recommendation"]=="PASS" and hc==0 and all(scores[d]>=pack["release_policy"]["per_case_judge_min_dimension"] for d in case["relevant_dimensions"]); all_judge_pass=all_judge_pass and jpass
        sanitized.append({"id":case["id"],"mechanical_pass":mech["pass"],"mechanical_failure_count":len(mech["failures"]),"mechanical_hard_failure_count":len(mech["hard_failures"]),"judge_scores":scores,"judge_hard_failure_count":hc,"judge_release_recommendation":assessment["release_recommendation"]})
        records.append({"id":case["id"],"candidate_output":artifact,"candidate_identity":raw.get("candidate_identity"),"candidate_transport":raw.get("transport"),"mechanical":mech,"judge":assessment,"duration_s":round(time.time()-t,3)})
    pol=pack["release_policy"]; mech_rate=sum(c["mechanical_pass"] for c in sanitized)/len(sanitized); mean=sum(scores_all)/len(scores_all) if scores_all else 0.0
    passed=mech_rate>=pol["mechanical_case_pass_rate"] and mech_hard<=pol["mechanical_hard_failures_allowed"] and judge_hard<=pol["judge_hard_failures_allowed"] and all_judge_pass and mean>=pol["judge_aggregate_mean_min"]
    verdict="PASS" if passed else "REVISE"
    report={"gate_id":GATE_ID,"verdict":verdict,"core_sha":CORE_SHA,"specialization_sha":SPECIALIZATION_SHA,"assembly_version":ASSEMBLY_VERSION,"composed_blob_sha":composed_sha,"composed_identity_sha256":composed_identity,"case_count":len(sanitized),"candidate_calls":len(sanitized),"judge_calls":len(sanitized),"mechanical_case_pass_rate":mech_rate,"mechanical_hard_failure_count":mech_hard,"judge_hard_failure_count":judge_hard,"all_cases_judge_release_pass":all_judge_pass,"judge_aggregate_mean":mean,"policy":pol,"cases":sanitized,"prior_evidence":{"universal_release_run_id":33501449175,"universal_release_verdict":"PASS","r1_composition_status":"CONSTRUCT_INVALID_DIAGNOSTIC_ONLY"}}
    (out/"qualification-report.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode().strip(); rr=canon(records); key=base64.urlsafe_b64encode(derive(master,b"run-records")); sealed=Fernet(key).encrypt(rr); (out/"sealed-run-records.bin").write_bytes(sealed); (out/"run-records-manifest.json").write_text(json.dumps({"identity_sha256":hashlib.sha256(rr).hexdigest(),"sealed_sha256":hashlib.sha256(sealed).hexdigest(),"record_count":len(records)},indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"gate_id":GATE_ID,"verdict":verdict,"case_count":len(sanitized),"mechanical_case_pass_rate":mech_rate,"mechanical_hard_failure_count":mech_hard,"judge_hard_failure_count":judge_hard,"judge_aggregate_mean":mean},sort_keys=True)); return 0 if passed else 20

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=["calibrate","score"],required=True); ap.add_argument("--pack",required=True); ap.add_argument("--out",required=True); ap.add_argument("--timeout",type=int,default=300); a=ap.parse_args()
    try:
        pack=load_pack(Path(a.pack)); return run_calibrate(pack,Path(a.out),a.timeout) if a.mode=="calibrate" else run_score(pack,Path(a.out),a.timeout)
    except Exception as exc:
        out=Path(a.out); out.mkdir(parents=True,exist_ok=True); report={"gate_id":GATE_ID,"status":"NOT_EXECUTABLE","error_type":type(exc).__name__,"error":str(exc)[:1200]}; (out/"runtime-failure.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps(report,sort_keys=True)); return 1

if __name__=="__main__": raise SystemExit(main())
