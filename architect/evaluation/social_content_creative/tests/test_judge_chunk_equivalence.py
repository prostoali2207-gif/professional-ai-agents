"""Offline proof that grouping the judge requests cannot change the verdict.
Zero provider calls. The stub judge answers per case from a fixed verdict table,
so batched and chunked transports must produce identical scoring."""
import importlib.util, json, random, sys
from pathlib import Path

RUNNER=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("r",RUNNER)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.PACE=0.0; m.GROQ_JUDGE_PACE=0.0

random.seed(1729)
def make_rows(n=12, size=1):
    return [{"id":f"F{i:02d}","family":m.FAMILIES[i],"task":"t"*(300*size),
             "hidden_reference":{"h":"r"*(500*size)},"candidate_answer":"a"*(1200*size),
             "runtime_error":None} for i in range(n)]

BASE={"mode":"heldout","trial":1,"dimensions":m.DIMS,"allowed_flags":sorted(m.FLAGS),
      "return":"x","cases":None}

def verdict_table(rows):
    """One fixed verdict per case id, independent of how cases are grouped."""
    t={}
    for i,r in enumerate(rows):
        t[r["id"]]={"scores":{d:random.choice([0,1,2,None]) for d in m.DIMS},
                    "critical_flags":(["EVIDENCE_INFLATION"] if i==5 else []),
                    "pass": i!=5, "reason_code":"stub"}
    return t

def stub(table, calls):
    def call(payload):
        calls.append(len(payload["cases"]))
        return {"results":[{"id":c["id"],"family":c["family"],**table[c["id"]]} for c in payload["cases"]]}
    return call

fails=0
for size,label in [(1,"lean"),(2,"typical"),(4,"rich")]:
    rows=make_rows(size=size); ids=[r["id"] for r in rows]
    table=verdict_table(rows)

    batched_calls=[]; chunked_calls=[]
    batched=m.normalize(stub(table,batched_calls)({**BASE,"cases":rows}), ids)
    chunked=m.judge_heldout(stub(table,chunked_calls), BASE, rows, ids, 0.0)

    same = json.dumps(batched,sort_keys=True)==json.dumps(chunked,sort_keys=True)
    overhead=m.approx_tokens({k:v for k,v in BASE.items() if k!="cases"})+m.approx_tokens(m.judge_system())
    groups=m.chunk_cases(rows,overhead,m.JUDGE_INPUT_BUDGET)
    sizes=[overhead+sum(m.approx_tokens(r) for r in g) for g in groups]
    worst=0
    for g in groups:
        p=dict(BASE); p['cases']=g
        worst=max(worst, m.approx_tokens(p)+m.approx_tokens(m.judge_system())+m.groq_completion_budget(p))
    fits = worst<=8000
    covered = sorted(x["id"] for g in groups for x in g)==sorted(ids)
    once = len([x for g in groups for x in g])==12

    ok = same and fits and covered and once
    fails += (not ok)
    print(f"[{label}] groups={len(groups)} sizes={sizes} worst_request={worst}tok "
          f"| identical={same} fits_8000TPM={fits} every_case_once={covered and once} -> {'PASS' if ok else 'FAIL'}")

# a case bigger than the budget must still be graded, in its own request
big=[{"id":"F00","family":m.FAMILIES[0],"task":"t"*40000,"hidden_reference":{},"candidate_answer":"","runtime_error":None}]
g=m.chunk_cases(big,100,m.JUDGE_INPUT_BUDGET)
print(f"[oversized single case] groups={len(g)} cases={[c['id'] for grp in g for c in grp]} -> {'PASS' if len(g)==1 else 'FAIL'}")
fails += (len(g)!=1)

# incomplete judge coverage must be a hard error, never a silent pass
rows=make_rows(); ids=[r["id"] for r in rows]; table=verdict_table(rows)
def dropping(payload):
    cs=payload["cases"][:-1] if len(payload["cases"])>1 else payload["cases"]
    return {"results":[{"id":c["id"],"family":c["family"],**table[c["id"]]} for c in cs]}
try:
    m.judge_heldout(dropping,BASE,rows,ids,0.0); print("[dropped case] FAIL - accepted"); fails+=1
except RuntimeError as e:
    print(f"[dropped case] PASS - rejected ({e})")

print("\nRESULT:", "ALL PASS" if fails==0 else f"{fails} FAILURES")
sys.exit(1 if fails else 0)
