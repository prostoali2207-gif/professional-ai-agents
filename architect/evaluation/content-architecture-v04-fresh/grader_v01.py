#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, hashlib, hmac, json, os, re
from pathlib import Path
from cryptography.fernet import Fernet

GATE_ID="content-architecture-v0.4-fresh-heldout-2026-08-29-r1"
CANDIDATE_SHA="5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
P0_FAMILY="P0"


def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
def derive(master: bytes,label: bytes)->bytes: return hmac.new(master,GATE_ID.encode()+b"|"+label,hashlib.sha256).digest()

def load_pack(path: Path):
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode()
    if not master: raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    key=base64.urlsafe_b64encode(derive(master,b"fernet"))
    plain=Fernet(key).decrypt(path.read_bytes())
    data=json.loads(plain)
    if data.get("gate_id")!=GATE_ID or data.get("candidate_sha")!=CANDIDATE_SHA: raise RuntimeError("sealed pack identity mismatch")
    return data

def parse_candidate(text: str):
    text=(text or "").strip()
    if text.startswith("```"):
        lines=text.splitlines(); text="\n".join(lines[1:-1]).strip()
    try: return json.loads(text)
    except Exception:
        m=re.search(r"\{.*\}",text,re.S)
        if not m: raise ValueError("candidate output does not contain JSON object")
        return json.loads(m.group(0))

def check_value(actual, allowed): return actual in allowed

def grade_fields(obj, exp):
    failures=[]
    for key,val in exp.items():
        if key in {"family"}: continue
        if key.endswith("_contains"):
            field=key[:-9]; actual=obj.get(field)
            if not isinstance(actual,list) or not all(x in actual for x in val): failures.append(f"{field} missing required members")
        elif key.endswith("_exact"):
            field=key[:-6]
            if obj.get(field)!=val: failures.append(f"{field} exact mismatch")
        elif key.endswith("_min"):
            field=key[:-4]; actual=obj.get(field)
            if not isinstance(actual,(int,float)) or actual<val: failures.append(f"{field} below minimum")
        elif isinstance(val,list):
            if not check_value(obj.get(key),val): failures.append(f"{key} not in allowed set")
        else:
            if obj.get(key)!=val: failures.append(f"{key} mismatch")
    return failures

def grade_record(record, pack):
    fid=record.get("fixture_id")
    if fid not in pack["expectations"]: return {"fixture_id":fid,"pass":False,"p0":False,"failures":["unknown fixture"]}
    if record.get("candidate_sha")!=CANDIDATE_SHA: return {"fixture_id":fid,"pass":False,"p0":False,"failures":["candidate identity mismatch"]}
    if record.get("gate_id")!=GATE_ID: return {"fixture_id":fid,"pass":False,"p0":False,"failures":["gate identity mismatch"]}
    try: obj=parse_candidate(record.get("final_response", ""))
    except Exception as e: return {"fixture_id":fid,"pass":False,"p0":False,"failures":[f"invalid structured output: {type(e).__name__}"]}
    exp=pack["expectations"][fid]
    failures=grade_fields(obj,exp)
    p0=exp.get("family")==P0_FAMILY and bool(failures)
    return {"fixture_id":fid,"family":exp.get("family"),"pass":not failures,"p0":p0,"failures":failures}

def summarize(results, records):
    byfam={}
    for r in results:
        byfam.setdefault(r.get("family"),[]).append(r)
    p0_count=sum(1 for r in results if r.get("p0"))
    deterministic=all(r["pass"] for r in results)
    fam_rates={f:sum(1 for r in rows if r["pass"])/len(rows) for f,rows in byfam.items() if f!="P0"}
    total=[r for r in results if r.get("family")!="P0"]
    agg=sum(1 for r in total if r["pass"])/len(total) if total else 0
    repeats_ok=True
    grouped={}
    for rec,res in zip(records,results): grouped.setdefault(rec["fixture_id"],[]).append(res["pass"])
    for rec in records:
        if int(rec.get("trial_count",1))>1 and not all(grouped.get(rec["fixture_id"],[])): repeats_ok=False
    release=(p0_count==0 and deterministic and all(v>=0.80 for v in fam_rates.values()) and agg>=0.90 and repeats_ok)
    return {"gate_id":GATE_ID,"candidate_sha":CANDIDATE_SHA,"p0_count":p0_count,"deterministic_invariant_pass_rate":1.0 if deterministic else 0.0,"family_pass_rates":fam_rates,"aggregate_p1_pass_rate":agg,"repeats_all_pass":repeats_ok,"verdict":"PASS" if release else "REVISE"}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--pack",required=True); ap.add_argument("--records",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    pack=load_pack(Path(a.pack))
    records=[json.loads(line) for line in Path(a.records).read_text().splitlines() if line.strip()]
    results=[grade_record(r,pack) for r in records]
    if any(r.get("terminal_status")=="PENDING_EXTERNAL_GRADER" for r in records): raise SystemExit("invalid terminal status PENDING_EXTERNAL_GRADER")
    report={"summary":summarize(results,records),"results":results,"grader":{"version":"v0.1","mode":"sealed-structural-professional-decision-verifier"}}
    Path(a.out).write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps(report["summary"],sort_keys=True))
if __name__=="__main__": main()
