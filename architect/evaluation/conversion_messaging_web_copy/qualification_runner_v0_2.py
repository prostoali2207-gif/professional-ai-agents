#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json, os, re, subprocess, sys, tempfile
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
PREREG=BASE/"qualification-preregistration-v0.2.json"
CALIBRATION=BASE/"calibration-public-v0.2.json"
CANDIDATE=BASE/"codex_candidate_adapter_v0_2.py"
JUDGE=BASE/"codex_judge_adapter_v0_2.py"
REPORT=BASE/"qualification-report-v0.2.sanitized.json"
PAID_KEYS=("OPENAI_API_KEY","ANTHROPIC_API_KEY","GEMINI_API_KEY","GROQ_API_KEY","XAI_API_KEY")

class GateError(RuntimeError): pass
class CodexFailure(RuntimeError):
    def __init__(self,role:str,returncode:int,stdout:str,stderr:str):
        super().__init__(f"{role} Codex runtime failed ({returncode})"); self.role=role; self.returncode=returncode; self.stdout=stdout; self.stderr=stderr

def redacted(value:str,limit:int=1200)->str:
    text=value[-limit:].replace("\r","")
    text=re.sub(r"(?i)bearer\s+[a-z0-9._~+/=-]+","Bearer <redacted>",text)
    text=re.sub(r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token)(\s*[:=]\s*)[^\s,;}]+",r"\1\2<redacted>",text)
    return text

def classify(stdout:str,stderr:str)->str:
    value=f"{stdout}\n{stderr}".lower()
    if any(x in value for x in ("quota","rate limit","429","unauthorized","authentication","permission denied","invalid schema","unknown model","model not found")): return "NONRETRYABLE_TECHNICAL"
    if any(x in value for x in ("timed out","timeout","connection reset","temporarily unavailable","http 500","http 502","http 503","http 504")): return "TRANSIENT_TRANSPORT"
    return "UNKNOWN_TECHNICAL"

def prereg()->dict:
    p=json.loads(PREREG.read_text(encoding="utf-8"))
    if p.get("status")!="PREREGISTERED_ZERO_MODEL_ONLY": raise GateError("preregistration status invalid")
    return p

def clean_env()->dict[str,str]:
    banned=("API_KEY","ANTHROPIC","GEMINI","GROQ","XAI","QUALIFICATION_KEY","HELDOUT","GRADER","SEALED_PACK","EXPECTED_ANSWER","REFERENCE_ANSWER")
    return {k:v for k,v in os.environ.items() if not any(x in k.upper() for x in banned)}

def cli_facts()->dict:
    for key in PAID_KEYS:
        if os.environ.get(key): raise GateError(f"separately billed API credential present: {key}")
    try:
        version=subprocess.check_output(["codex","--version"],text=True).strip()
        s=subprocess.run(["codex","login","status"],text=True,capture_output=True,check=True)
    except Exception as exc: raise GateError(f"Codex CLI unavailable: {type(exc).__name__}: {exc}") from exc
    login=(s.stdout+s.stderr).strip()
    if "Logged in using ChatGPT" not in login: raise GateError("Codex CLI is not ChatGPT-subscription authenticated")
    return {"version":version,"login":"Logged in using ChatGPT"}

def author_schema(p:dict)->dict:
    families=p["construct"]["families"]
    case_props={
      "id":{"type":"string"},"family":{"enum":families},"pair_id":{"type":["string","null"]},"task":{"type":"string","minLength":20},
      "context":{"type":"object"},"constraints":{"type":"array","items":{"type":"string"}},
      "hidden_reference":{"type":"object","properties":{"required_behaviors":{"type":"array","items":{"type":"string"},"minItems":1},"prohibited_behaviors":{"type":"array","items":{"type":"string"}},"decision_boundary":{"type":"string","minLength":5},"expected_state_facts":{"type":"array","items":{"type":"string"}}},"required":["required_behaviors","prohibited_behaviors","decision_boundary","expected_state_facts"],"additionalProperties":False}
    }
    return {"type":"object","properties":{"cases":{"type":"array","minItems":30,"maxItems":30,"items":{"type":"object","properties":case_props,"required":list(case_props),"additionalProperties":False}}},"required":["cases"],"additionalProperties":False}

def reviewer_schema()->dict:
    return {"type":"object","properties":{"verdict":{"enum":["PASS","FAIL"]},"reasons":{"type":"array","items":{"type":"string"}}},"required":["verdict","reasons"],"additionalProperties":False}

def forbidden_event(event:dict)->bool:
    item=event.get("item") if isinstance(event.get("item"),dict) else {}
    kinds=f"{event.get('type','')} {item.get('type','')}".lower()
    return any(x in kinds for x in ("command","tool","file_change","mcp","web_search"))

def invoke_structured(role:str,model:str,prompt:str,schema:dict,timeout:int)->tuple[dict,dict]:
    with tempfile.TemporaryDirectory(prefix=f"messaging-v02-{role}-") as raw:
        root=Path(raw); sp=root/"schema.json"; out=root/"out.json"; sp.write_text(json.dumps(schema),encoding="utf-8")
        cmd=["codex","exec","-","--json","--ephemeral","--ignore-user-config","--ignore-rules","--skip-git-repo-check","--sandbox","read-only","--model",model,"--output-schema",str(sp),"--output-last-message",str(out),"--color","never","-C",str(root),"-c",'approval_policy="never"']
        proc=subprocess.run(cmd,input=prompt,text=True,capture_output=True,timeout=timeout,cwd=root,env=clean_env())
        if proc.returncode!=0: raise CodexFailure(role,proc.returncode,proc.stdout,proc.stderr)
        events=[]
        for line in proc.stdout.splitlines():
            try:v=json.loads(line)
            except json.JSONDecodeError: continue
            if isinstance(v,dict): events.append(v)
        if any(forbidden_event(e) for e in events): raise GateError(f"{role} emitted forbidden tool/command event")
        if not out.is_file(): raise GateError(f"{role} produced no structured output")
        completed=[e for e in events if e.get("type")=="turn.completed"]
        return json.loads(out.read_text(encoding="utf-8")),{"usage":completed[-1].get("usage") if completed else None,"event_types":[e.get("type") for e in events]}

def author_prompt(p:dict)->str:
    return """You are a blind independent held-out AUTHOR for Conversion Messaging & Web Copy v0.2 qualification. You are not the candidate and must not seek or infer candidate text. Do not use tools, filesystem, web, or MCP. Create exactly 30 fresh adversarial work samples, exactly two per family listed below. Do not copy or reconstruct historical hidden v0.1 cases or development-example wording. Four preserved pairs plus three new pairs are mandatory with the exact pair IDs/families supplied. Each pair must differ by one decision-relevant material fact; conclusions should change only when that fact warrants it. Cases must be realistic professional artifacts, not trivia. Hidden references define required/prohibited behavior and decision boundaries without prescribing one stylistic answer. Include messy/contradictory evidence, pressure, insufficient evidence, strong-evidence controls, and end-to-end work. New v0.2 families must specifically test message-match without unsupported source-claim propagation, accessible wording within frozen UX without copy-only conformance claims, and localization that preserves evidence/commitment and escalates local-authority uncertainty. Return JSON only.\n\nPUBLIC PREREGISTRATION:\n"""+json.dumps({"families":p["construct"]["families"],"pairs":p["construct"]["contrastive_pairs"],"hard_fails":p["construct"]["hard_fails"],"dimensions":p["construct"]["dimensions"]},ensure_ascii=False)

def review_prompt(p:dict,cases:list[dict])->str:
    return """You are the blind independent CONSTRUCT REVIEWER. You are not the candidate. Do not use tools, filesystem, web, or MCP. Review the supplied hidden author corpus only for evaluator validity: exact family coverage/cardinality, contrastive-pair validity, realistic work-sample construct coverage, expected-answer boundaries that allow professionally valid alternatives, no public-example copying, no candidate-specific tailoring, no threshold drift, and explicit coverage of the three v0.2 deltas. Return PASS only if this is release-valid independent held-out evidence. Do not rewrite cases. Return JSON only.\n\nPREREGISTRATION:\n"""+json.dumps({"families":p["construct"]["families"],"pairs":p["construct"]["contrastive_pairs"],"hard_fails":p["construct"]["hard_fails"]},ensure_ascii=False)+"\n\nHIDDEN AUTHOR CORPUS:\n"+json.dumps(cases,ensure_ascii=False)

def validate_cases(cases:list[dict],p:dict)->None:
    if len(cases)!=30: raise GateError("author corpus must contain exactly 30 cases")
    counts=defaultdict(int); ids=set(); pairs=defaultdict(list)
    for case in cases:
        cid=case["id"]
        if cid in ids: raise GateError("duplicate fixture id")
        ids.add(cid); counts[case["family"]]+=1
        if case.get("pair_id") is not None: pairs[case["pair_id"]].append(case)
    if set(counts)!=set(p["construct"]["families"]) or any(counts[f]!=2 for f in p["construct"]["families"]): raise GateError("family cardinality invalid")
    expected=p["construct"]["contrastive_pairs"]
    if set(pairs)!=set(expected): raise GateError("pair ID set invalid")
    for pid,fam in expected.items():
        if len(pairs[pid])!=2 or any(x["family"]!=fam for x in pairs[pid]): raise GateError(f"pair structure invalid: {pid}")

def import_judge():
    spec=importlib.util.spec_from_file_location("messaging_v02_judge",JUDGE)
    if spec is None or spec.loader is None: raise GateError("cannot import judge adapter")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def judge_call(payload:dict,model:str,timeout:int)->dict:
    proc=subprocess.run([sys.executable,str(JUDGE),"--model",model,"--timeout",str(timeout)],input=json.dumps(payload,ensure_ascii=False),text=True,capture_output=True,cwd=ROOT,env=clean_env())
    if proc.returncode!=0:
        try: env=json.loads(proc.stdout)
        except Exception: raise GateError(f"judge adapter failed: {redacted(proc.stderr)}")
        raise GateError(json.dumps(env.get("failure_envelope",{}),ensure_ascii=False))
    out=json.loads(proc.stdout)
    if out.get("status")!="completed": raise GateError("judge did not complete")
    return out["judgment"]

def calibration_payload()->dict:
    data=json.loads(CALIBRATION.read_text(encoding="utf-8"))
    return {"mode":"calibration","cases":[{"id":a["id"],"family":a["family"],"task":a["task"],"candidate_response":a["response"],"reference":a["reference"]} for a in data["anchors"]]}

def validate_calibration(judgment:dict)->None:
    expected={a["id"]:a["reference"] for a in json.loads(CALIBRATION.read_text(encoding="utf-8"))["anchors"]}
    results={r["id"]:r for r in judgment.get("results",[])}
    if set(results)!=set(expected): raise GateError("calibration result IDs mismatch")
    for cid,ref in expected.items():
        r=results[cid]
        if bool(r["pass"])!=bool(ref["expected_pass"]): raise GateError(f"judge calibration mismatch on {cid}")
        if not set(ref["expected_flags"]).issubset(set(r["critical_flags"])): raise GateError(f"judge calibration flag mismatch on {cid}")

def candidate_call(case:dict,timeout:int)->dict:
    visible={k:case[k] for k in ("task","context","constraints")}
    proc=subprocess.run([sys.executable,str(CANDIDATE),"--timeout",str(timeout)],input=json.dumps(visible,ensure_ascii=False),text=True,capture_output=True,cwd=ROOT,env=clean_env())
    if proc.returncode!=0: raise GateError(f"candidate adapter failed: {redacted(proc.stderr)}")
    out=json.loads(proc.stdout)
    if out.get("candidate_identity",{}).get("artifact_digest")!=prereg()["candidate"]["artifact_digest"]: raise GateError("candidate identity drift during scoring")
    return out

def heldout_payload(cases:list[dict],responses:dict[str,dict])->dict:
    return {"mode":"heldout","cases":[{"id":c["id"],"family":c["family"],"pair_id":c["pair_id"],"task":c["task"],"context":c["context"],"constraints":c["constraints"],"candidate_response":responses[c["id"]]["final_response"],"reference":c["hidden_reference"]} for c in cases]}

def verdict(cases:list[dict],ja:dict,jb:dict,p:dict)->dict:
    dims=p["construct"]["dimensions"]; by_a={r["id"]:r for r in ja["results"]}; by_b={r["id"]:r for r in jb["results"]}
    rows=[]; flags=set(); family_values=defaultdict(lambda:{d:[] for d in dims})
    for c in cases:
        a,b=by_a[c["id"]],by_b[c["id"]]
        conservative={d:min(float(a[d]),float(b[d])) for d in dims}; row_flags=sorted(set(a["critical_flags"])|set(b["critical_flags"])); flags.update(row_flags)
        passed=bool(a["pass"] and b["pass"] and not row_flags and all(conservative[d]>=1 for d in dims))
        rows.append({"id":c["id"],"family":c["family"],"pass":passed,"dimensions":conservative,"critical_flags":row_flags})
        for d in dims: family_values[c["family"]][d].append(conservative[d])
    pair_a={x["pair_id"]:x["consistent"] for x in ja.get("pair_results",[])}; pair_b={x["pair_id"]:x["consistent"] for x in jb.get("pair_results",[])}
    pair_ok=set(pair_a)==set(p["construct"]["contrastive_pairs"])==set(pair_b) and all(pair_a[x] and pair_b[x] for x in p["construct"]["contrastive_pairs"])
    floors=p["construct"]["thresholds"]["family_means_min"]; family_means={}; family_ok=True
    for fam,vals in family_values.items():
        family_means[fam]={d:sum(vals[d])/len(vals[d]) for d in dims}
        if any(family_means[fam][d] < float(floors[d]) for d in dims): family_ok=False
    pass_count=sum(1 for r in rows if r["pass"])
    release_pass=(not flags and pass_count>=p["construct"]["thresholds"]["fixture_passes_min"] and pair_ok and family_ok)
    return {"verdict":"PASS" if release_pass else "REVISE","fixture_passes":pass_count,"fixture_count":30,"hard_fails":sorted(flags),"all_pairs_consistent":pair_ok,"family_floors_pass":family_ok,"family_means":family_means,"cases":rows}

def static_preflight()->dict:
    p=prereg(); judge=import_judge()
    if not CALIBRATION.is_file(): raise GateError("public calibration anchors missing")
    if len(json.loads(CALIBRATION.read_text(encoding="utf-8")).get("anchors",[]))!=3: raise GateError("calibration anchor count mismatch")
    a=author_schema(p); r=reviewer_schema()
    if a["properties"]["cases"]["minItems"]!=30 or a["properties"]["cases"]["maxItems"]!=30: raise GateError("author schema cardinality mismatch")
    if reviewer_schema()["properties"]["verdict"]["enum"]!=["PASS","FAIL"]: raise GateError("reviewer schema verdict mismatch")
    if "pair_results" in judge.schema("calibration")["properties"] or "pair_results" not in judge.schema("heldout")["required"]: raise GateError("judge schema mode mismatch")
    contract=json.loads(subprocess.check_output([sys.executable,str(CANDIDATE),"--qualification-contract"],text=True,cwd=ROOT))
    if contract.get("candidate_digest")!=p["candidate"]["artifact_digest"] or contract.get("visible_fields")!=["task","context","constraints"]: raise GateError("candidate contract mismatch")
    return {"status":"PASS","checks":12,"cycle_id":p["cycle_id"],"model_calls":0,"candidate_calls":0,"scored_calls":0,"paid_api_calls":0}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--static-preflight",action="store_true"); ap.add_argument("--runtime-preflight",action="store_true"); ap.add_argument("--execute",action="store_true"); ap.add_argument("--timeout",type=int,default=900); args=ap.parse_args()
    if sum(bool(x) for x in (args.static_preflight,args.runtime_preflight,args.execute))!=1: raise GateError("choose exactly one mode")
    if args.static_preflight:
        print(json.dumps(static_preflight(),sort_keys=True)); return 0
    static_preflight(); facts=cli_facts(); p=prereg()
    if args.runtime_preflight:
        print(json.dumps({"status":"PASS","cycle_id":p["cycle_id"],"codex":facts,"planned_subscription_calls":37,"max_clean_calls":37,"candidate_calls":0,"scored_calls":0,"paid_api_calls":0},sort_keys=True)); return 0

    # Execution begins only after deterministic + runtime prerequisites pass.
    calls=0
    try:
        authored,_=invoke_structured("author",p["evaluation_design"]["author_model"],author_prompt(p),author_schema(p),args.timeout); calls+=1
        cases=authored["cases"]; validate_cases(cases,p)
        reviewed,_=invoke_structured("reviewer",p["evaluation_design"]["reviewer_model"],review_prompt(p,cases),reviewer_schema(),args.timeout); calls+=1
        if reviewed["verdict"]!="PASS":
            print(json.dumps({"status":"EVALUATOR_CONSTRUCT_FAIL","reasons":reviewed["reasons"],"subscription_calls":calls,"candidate_calls":0,"scored_calls":0,"paid_api_calls":0},ensure_ascii=False)); return 3

        cal=calibration_payload()
        for model in p["evaluation_design"]["judges"]:
            validate_calibration(judge_call(cal,model,args.timeout)); calls+=1

        canary=subprocess.run([sys.executable,str(CANDIDATE),"--canary","--timeout",str(args.timeout)],text=True,capture_output=True,cwd=ROOT,env=clean_env())
        calls+=1
        if canary.returncode!=0: raise GateError(f"candidate canary failed: {redacted(canary.stderr)}")

        responses={}
        for case in cases:
            responses[case["id"]]=candidate_call(case,args.timeout); calls+=1
        payload=heldout_payload(cases,responses)
        ja=judge_call(payload,p["evaluation_design"]["judges"][0],args.timeout); calls+=1
        jb=judge_call(payload,p["evaluation_design"]["judges"][1],args.timeout); calls+=1
        result=verdict(cases,ja,jb,p)
        report={"cycle_id":p["cycle_id"],"candidate":p["candidate"],"scope":"FULL","subscription_calls":calls,"paid_api_calls":0,"professional_retries":0,"hidden_fixture_text_published":False,"semantic":result,"practical_gate_required":result["verdict"]=="PASS"}
        REPORT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print(json.dumps({"status":"SEMANTIC_QUALIFICATION_COMPLETE","verdict":result["verdict"],"fixture_passes":result["fixture_passes"],"hard_fails":result["hard_fails"],"subscription_calls":calls,"scored_candidate_calls":30,"paid_api_calls":0,"sanitized_report":str(REPORT.relative_to(ROOT))},ensure_ascii=False)); return 0 if result["verdict"]=="PASS" else 4
    except CodexFailure as exc:
        print(json.dumps({"status":"QUALIFICATION_NOT_EXECUTABLE","stage":exc.role,"classification":classify(exc.stdout,exc.stderr),"subscription_calls_started":calls+1,"candidate_scored_calls_completed":max(0,calls-5),"paid_api_calls":0,"stderr_tail":redacted(exc.stderr)},ensure_ascii=False)); return 2

if __name__=="__main__":
    try: raise SystemExit(main())
    except GateError as exc:
        print(json.dumps({"status":"QUALIFICATION_NOT_EXECUTABLE","classification":"LOCAL_EXECUTION_FAIL","error":redacted(str(exc)),"paid_api_calls":0},ensure_ascii=False)); raise SystemExit(2)
