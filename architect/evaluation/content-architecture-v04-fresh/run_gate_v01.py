#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, re, shlex, subprocess, time
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent
GRADER_PATH=HERE/"grader_v01.py"
spec=importlib.util.spec_from_file_location("grader",GRADER_PATH); grader=importlib.util.module_from_spec(spec); spec.loader.exec_module(grader)
GATE=grader.GATE_ID; SHA=grader.CANDIDATE_SHA

def read_jsonl(p):
    if not p.exists(): return []
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]

def append(p,obj):
    with p.open("a") as f: f.write(json.dumps(obj,ensure_ascii=False,sort_keys=True)+"\n")

def runtime_error_category(proc):
    text=((proc.stderr or "")+"\n"+(proc.stdout or ""))[:6000]
    m=re.search(r"Gemini HTTP\s+(\d{3})", text)
    if m: return f"GEMINI_HTTP_{m.group(1)}"
    if "GEMINI_API_KEY is not configured" in text: return "GEMINI_CREDENTIAL_MISSING"
    if "candidate Git object unavailable" in text: return "CANDIDATE_BLOB_UNAVAILABLE"
    if "provider response contains no observable text output" in text: return "PROVIDER_EMPTY_OUTPUT"
    if "tool-round budget exhausted" in text: return "TOOL_ROUND_BUDGET_EXHAUSTED"
    return f"CANDIDATE_RUNTIME_EXIT_{proc.returncode}"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--pack",required=True); ap.add_argument("--candidate-command",required=True); ap.add_argument("--out",required=True); ap.add_argument("--timeout",type=int,default=180); ap.add_argument("--only-fixture",default=None); a=ap.parse_args()
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True); records=out/"records.jsonl"
    pack=grader.load_pack(Path(a.pack))
    done={(r.get("fixture_id"),int(r.get("trial",0))) for r in read_jsonl(records) if r.get("terminal_status")=="COMPLETED"}
    calls=0
    fixtures=[f for f in pack["fixtures"] if a.only_fixture is None or f.get("fixture_id")==a.only_fixture]
    if a.only_fixture and not fixtures:
        print(json.dumps({"status":"NOT_EXECUTABLE","runtime_error_category":"UNKNOWN_FIXTURE_FILTER"})); return 3
    for fixture in fixtures:
        for trial in range(1,int(fixture.get("trial_count",1))+1):
            key=(fixture["fixture_id"],trial)
            if key in done: continue
            workspace=out/"workspaces"/f"{fixture['fixture_id']}-t{trial}"; workspace.mkdir(parents=True,exist_ok=True)
            payload={"protocol_version":2,"candidate_sha":SHA,"workspace":str(workspace),"input":{**fixture["candidate_input"],"allowed_resources":[],"fixture_tools":{}}}
            started=time.time(); proc=None
            try:
                proc=subprocess.run(shlex.split(a.candidate_command),input=json.dumps(payload),text=True,capture_output=True,timeout=a.timeout,env=os.environ.copy())
                if proc.returncode!=0: raise RuntimeError("candidate runtime nonzero")
                raw=json.loads(proc.stdout)
                if raw.get("status")!="completed": raise RuntimeError("candidate runtime incomplete")
                ident=raw.get("candidate_identity",{})
                if ident.get("sha")!=SHA: raise RuntimeError("candidate identity mismatch")
                rec={"gate_id":GATE,"fixture_id":fixture["fixture_id"],"family":fixture["family"],"trial":trial,"trial_count":fixture.get("trial_count",1),"candidate_sha":SHA,"runtime_identity":ident,"final_response":raw.get("final_output","") ,"observable":raw.get("observable",{}),"transport":raw.get("transport",{}),"terminal_status":"COMPLETED","duration_s":round(time.time()-started,3),"error":None,"runtime_error_category":None}
                calls+=1
            except Exception as e:
                category=runtime_error_category(proc) if proc is not None else type(e).__name__
                rec={"gate_id":GATE,"fixture_id":fixture["fixture_id"],"family":fixture["family"],"trial":trial,"trial_count":fixture.get("trial_count",1),"candidate_sha":SHA,"terminal_status":"ERROR","duration_s":round(time.time()-started,3),"error":type(e).__name__,"runtime_error_category":category}
            append(records,rec)
            if rec["terminal_status"]=="ERROR":
                print(json.dumps({"status":"NOT_EXECUTABLE","fixture_id":fixture["fixture_id"],"trial":trial,"candidate_calls_this_run":calls,"runtime_error_category":rec.get("runtime_error_category")}))
                return 3
    if a.only_fixture:
        print(json.dumps({"status":"DIAGNOSTIC_COMPLETED","fixture_id":a.only_fixture,"candidate_calls_this_run":calls})); return 0
    report=out/"grade-report.json"
    proc=subprocess.run(["python",str(GRADER_PATH),"--pack",a.pack,"--records",str(records),"--out",str(report)],text=True,capture_output=True,env=os.environ.copy())
    if proc.returncode!=0:
        print(proc.stdout); print(proc.stderr); return proc.returncode
    summary=json.loads(report.read_text())["summary"]; summary["candidate_calls_this_run"]=calls; summary["run_records_total"]=len(read_jsonl(records)); (out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n"); print(json.dumps(summary,sort_keys=True)); return 0 if summary["verdict"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
