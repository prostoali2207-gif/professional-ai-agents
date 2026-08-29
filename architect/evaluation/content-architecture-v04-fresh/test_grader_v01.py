#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUTHOR=HERE/"author_pack_v01.py"
GRADER=HERE/"grader_v01.py"
GATE="content-architecture-v0.4-fresh-heldout-2026-08-29-r1"
SHA="5d440e1bf3e20fbd35c6ab276310a904e36cc06d"

def run(cmd,env):
    return subprocess.run(cmd,text=True,capture_output=True,env=env)

def main():
    env={**os.environ,"QUALIFICATION_SEALED_PACK_MASTER_KEY":"offline-calibration-key-not-production"}
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); packdir=root/"pack"
        r=run(["python",str(AUTHOR),"--out",str(packdir)],env); assert r.returncode==0,r.stderr
        # decrypt via grader module by importing it with the same key
        import importlib.util
        spec=importlib.util.spec_from_file_location("g",GRADER); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
        os.environ["QUALIFICATION_SEALED_PACK_MASTER_KEY"]=env["QUALIFICATION_SEALED_PACK_MASTER_KEY"]
        pack=g.load_pack(packdir/"sealed-pack.bin")
        fixture=pack["fixtures"][0]; fid=fixture["fixture_id"]; exp=pack["expectations"][fid]
        good={}
        for k,v in exp.items():
            if k=="family": continue
            if k.endswith("_contains"): good[k[:-9]]=list(v)
            elif k.endswith("_exact"): good[k[:-6]]=v
            elif k.endswith("_min"): good[k[:-4]]=v
            elif isinstance(v,list): good[k]=v[0]
            else: good[k]=v
        rec={"gate_id":GATE,"candidate_sha":SHA,"fixture_id":fid,"trial_count":fixture.get("trial_count",1),"final_response":json.dumps(good),"terminal_status":"COMPLETED"}
        records=root/"records.jsonl"; records.write_text(json.dumps(rec)+"\n")
        report=root/"report.json"; rr=run(["python",str(GRADER),"--pack",str(packdir/"sealed-pack.bin"),"--records",str(records),"--out",str(report)],env)
        assert rr.returncode==0,rr.stderr
        data=json.loads(report.read_text()); assert data["results"][0]["pass"] is True
        # known fail: remove a required field
        broken=dict(good); broken.pop(next(iter(good)))
        rec["final_response"]=json.dumps(broken); records.write_text(json.dumps(rec)+"\n")
        rr=run(["python",str(GRADER),"--pack",str(packdir/"sealed-pack.bin"),"--records",str(records),"--out",str(report)],env)
        assert rr.returncode==0,rr.stderr
        data=json.loads(report.read_text()); assert data["results"][0]["pass"] is False
        # terminal pending is forbidden
        rec["terminal_status"]="PENDING_EXTERNAL_GRADER"; records.write_text(json.dumps(rec)+"\n")
        rr=run(["python",str(GRADER),"--pack",str(packdir/"sealed-pack.bin"),"--records",str(records),"--out",str(report)],env)
        assert rr.returncode!=0
    print("offline grader calibration: PASS")
if __name__=="__main__": main()
