#!/usr/bin/env python3
import json,sys
from pathlib import Path
ALLOWED={"cycle_id","candidate","execution_status","attempted","passed","tasks_attempted","tasks_passed","critical_hard_fails","family_level_aggregate","usage","verdict"}
FAMS={"OWN","LIFE","MIX","SEC","FACT","INTENT","OBJ","NEXT","FUP","STATE","ID","OPS"}
def fail(m): print("REPORT_INVALID: "+m,file=sys.stderr); raise SystemExit(2)
p=Path(sys.argv[1] if len(sys.argv)>1 else "sanitized-report.json")
if not p.is_file(): fail("missing report")
try: r=json.loads(p.read_text())
except Exception: fail("invalid json")
if set(r)!=ALLOWED: fail("unexpected/missing top-level fields")
if r["cycle_id"]!="sales-0.3-fresh-independent-2026-08-22-r1": fail("cycle mismatch")
c=r["candidate"]
if c.get("commit")!="5adc0d315f6f63bc92df0a921040954a3541ef89" or c.get("artifact_digest")!="sha256:a33bae7c2957e415669852d10135902349f20fdc9ae22090bf8d55278e0b15c2": fail("candidate mismatch")
if r["execution_status"]!="completed": fail("execution incomplete")
if r["verdict"] not in {"PASS","REVISE"}: fail("invalid verdict")
if set(r["family_level_aggregate"])!=FAMS: fail("family set mismatch")
for v in r["family_level_aggregate"].values():
    if set(v)!={"attempted","passed"} or v["attempted"]!=3 or not (0<=v["passed"]<=3): fail("family aggregate invalid")
if r["tasks_attempted"]!=36 or not (0<=r["tasks_passed"]<=36): fail("task counts invalid")
if r["attempted"]!=42 or not (0<=r["passed"]<=42): fail("attempt counts invalid")
if not isinstance(r["critical_hard_fails"],int) or r["critical_hard_fails"]<0: fail("critical count invalid")
u=r["usage"]
for k in ("input_tokens","output_tokens","total_tokens","cached_input_tokens"):
    if not isinstance(u.get(k),int) or u[k]<0: fail("usage invalid")
print("REPORT_VALID")
