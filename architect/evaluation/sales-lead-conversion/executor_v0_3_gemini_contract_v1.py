#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys

BASE='architect/evaluation/sales-lead-conversion/executor_v0_3_gemini.py'

def main():
    if len(sys.argv)==2 and sys.argv[1]=='--qualification-contract':
        raw=subprocess.check_output(['python',BASE,'--qualification-contract'],text=True)
        c=json.loads(raw); c['contract_version']=1
        json.dump(c,sys.stdout,sort_keys=True); sys.stdout.write('\n'); return 0
    p=subprocess.run(['python',BASE,*sys.argv[1:]],stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr,env=os.environ.copy())
    return p.returncode

if __name__=='__main__': raise SystemExit(main())
