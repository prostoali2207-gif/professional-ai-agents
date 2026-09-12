#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, sys, time, urllib.error, urllib.request
from pathlib import Path

ROOT=Path.cwd()
ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
CANDIDATE_MODEL="gemini-3.5-flash-lite"
JUDGE_MODEL="gemini-3.5-flash"
REPORT=ROOT/"operational-product-ux-ui-b0-development-report.json"

CORES={
 "operational_product_ux":{
  "skill":"architect/evaluation/operational-product-ux/candidate/SKILL.md",
  "knowledge":[
   "architect/evaluation/operational-product-ux/candidate/knowledge/operational-interaction.md",
   "architect/evaluation/operational-product-ux/candidate/knowledge/mobile-accessibility-rtl.md",
   "architect/evaluation/operational-product-ux/candidate/knowledge/rendered-ux-review.md"],
  "fixtures":"architect/evaluation/operational-product-ux/fixtures-v0.1.json",
  "ids":["UX04_RECOVERABLE_FAILURE_DATA_PRESERVATION","UX07_SELECT_ALL_SCOPE_TRAP","UX08_CONSEQUENTIAL_GENERIC_CONFIRMATION","UX10_COLLAPSED_DESKTOP_MOBILE","UX13_BOUNDARY_DOMAIN_RULE_TRAP"]},
 "product_interface_design":{
  "skill":"architect/evaluation/product-interface-design/candidate/SKILL.md",
  "knowledge":[
   "architect/evaluation/product-interface-design/candidate/knowledge/system-foundations.md",
   "architect/evaluation/product-interface-design/candidate/knowledge/operational-components-responsive.md",
   "architect/evaluation/product-interface-design/candidate/knowledge/rendered-system-review.md"],
  "fixtures":"architect/evaluation/product-interface-design/fixtures-v0.1.json",
  "ids":["UI04_SEMANTIC_COLOR_DRIFT","UI08_COMPONENT_STATE_INCONSISTENCY","UI12_COLLAPSED_DESKTOP_RESPONSIVE","UI16_UNAUTHORIZED_UX_CHANGE","UI17_FAKE_OPERATIONAL_STATUS"]}
}

def sha(s): return hashlib.sha256(s.encode()).hexdigest()

def extract(raw):
 if isinstance(raw.get("output_text"),str) and raw["output_text"].strip(): return raw["output_text"].strip()
 for step in reversed(raw.get("steps") or []):
  if isinstance(step,dict) and step.get("type")=="model_output":
   c=step.get("content")
   if isinstance(c,str) and c.strip(): return c.strip()
   for x in c or []:
    if isinstance(x,dict) and isinstance(x.get("text"),str) and x["text"].strip(): return x["text"].strip()
 raise RuntimeError("provider returned no observable text")

def parse_obj(text):
 t=text.strip()
 if t.startswith("json"): t=t[4:].strip()
 if t.startswith("'''"): t="\n".join(t.splitlines()[1:-1]).strip()
 if not t.startswith("{"):
  a,b=t.find("{"),t.rfind("}")
  if a<0 or b<=a: raise RuntimeError("judge returned invalid JSON")
  t=t[a:b+1]
 out=json.loads(t)
 if not isinstance(out,dict): raise RuntimeError("judge JSON must be object")
 return out

def call(model,system,payload):
 key=os.environ.get("GEMINI_API_KEY","").strip()
 if not key: raise RuntimeError("GEMINI_API_KEY missing")
 body={"model":model,"system_instruction":system,"input":payload,"store":False,"generation_config":{"thinking_level":"medium"}}
 req=urllib.request.Request(ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",headers={"Content-Type":"application/json","x-goog-api-key":key})
 for attempt in range(2):
  try:
   with urllib.request.urlopen(req,timeout=180) as r:
    raw=json.loads(r.read().decode()); return extract(raw),raw
  except urllib.error.HTTPError as e:
   detail=e.read().decode("utf-8","replace")[-1000:]
   if 500<=e.code<600 and attempt==0: time.sleep(15); continue
   raise RuntimeError(f"Gemini HTTP {e.code}: {detail}") from None

def load(spec):
 skill=(ROOT/spec["skill"]).read_text()
 knowledge="\n\n".join((ROOT/p).read_text() for p in spec["knowledge"])
 rows=json.loads((ROOT/spec["fixtures"]).read_text())["families"]
 by={x["id"]:x for x in rows}
 for cid in spec["ids"]:
  if cid not in by or by[cid].get("criticality")!="P0": raise RuntimeError(f"invalid B0 fixture {cid}")
 return skill+"\n\n--- PACKAGED KNOWLEDGE ---\n"+knowledge,by

def candidate(contract,case):
 system="Execute the supplied professional candidate as the complete role contract. Respond as the practitioner, not as an evaluator. Do not mention testing or grading. Use packaged knowledge when relevant. Never claim evidence not supplied.\n\n--- CONTRACT ---\n"+contract
 payload=json.dumps({"work_situation":case["prompt"],"instruction":"Handle this situation professionally with concrete decisions."},ensure_ascii=False)
 return call(CANDIDATE_MODEL,system,payload)

def judge(core,case,output):
 system="You are a strict independent senior assessor for a DEVELOPMENT-ONLY P0 agent test. Judge observable behavior, not style. A required safeguard must be explicit enough to control the recommendation. Return JSON only."
 payload=json.dumps({
  "core":core,"work_situation":case["prompt"],
  "must_observe":case["must_observe"],"must_not_observe":case["must_not_observe"],
  "candidate_output":output,
  "schema":{"verdict":"PASS|FAIL","p0_triggered":"boolean","missing_required":[],"forbidden_observed":[],"reason":"string"}
 },ensure_ascii=False)
 text,raw=call(JUDGE_MODEL,system,payload); out=parse_obj(text)
 if out.get("verdict") not in ("PASS","FAIL"): raise RuntimeError("invalid judge verdict")
 if not isinstance(out.get("p0_triggered"),bool): raise RuntimeError("invalid p0 flag")
 for k in ("missing_required","forbidden_observed"):
  if not isinstance(out.get(k),list) or not all(isinstance(x,str) for x in out[k]): raise RuntimeError(f"invalid {k}")
 if not isinstance(out.get("reason"),str) or not out["reason"].strip(): raise RuntimeError("invalid judge reason")
 if out["verdict"]=="PASS" and (out["p0_triggered"] or out["missing_required"] or out["forbidden_observed"]): raise RuntimeError("inconsistent judge PASS")
 if out["verdict"]=="FAIL" and not out["p0_triggered"]: raise RuntimeError("B0 FAIL without P0")
 return out,raw

def write(report): REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")

def main():
 report={"stage":"B0_DEVELOPMENT_ONLY","release_evidence":False,"heldout_evidence":False,"candidate_model":CANDIDATE_MODEL,"judge_model":JUDGE_MODEL,"max_generation_calls":20,"generation_calls":0,"cores":{},"status":"IN_PROGRESS"}
 try:
  for name,spec in CORES.items():
   contract,fixtures=load(spec)
   cr={"contract_sha256":sha(contract),"cases":[],"status":"IN_PROGRESS"}; report["cores"][name]=cr
   for cid in spec["ids"]:
    if report["generation_calls"]+2>20: raise RuntimeError("generation call budget exhausted")
    output,craw=candidate(contract,fixtures[cid]); report["generation_calls"]+=1
    verdict,jraw=judge(name,fixtures[cid],output); report["generation_calls"]+=1
    cr["cases"].append({"id":cid,**verdict,"candidate_output_sha256":sha(output),"candidate_output_excerpt":output[:1800],"candidate_usage":craw.get("usage") or craw.get("usageMetadata"),"judge_usage":jraw.get("usage") or jraw.get("usageMetadata")})
    if verdict["verdict"]=="FAIL": cr["status"]="B0_REVISE_P0"; break
   if cr["status"]=="IN_PROGRESS": cr["status"]="B0_PASS"
  if any(x["status"]=="B0_REVISE_P0" for x in report["cores"].values()): report["status"]="B0_REVISE"; code=20
  elif all(x["status"]=="B0_PASS" for x in report["cores"].values()): report["status"]="B0_PASS"; code=0
  else: report["status"]="DEVELOPMENT_NOT_EXECUTABLE"; code=30
  write(report)
  print(json.dumps({"status":report["status"],"generation_calls":report["generation_calls"],"cores":{k:{"status":v["status"],"cases_executed":len(v["cases"]),"failed_case":next((c["id"] for c in v["cases"] if c["verdict"]=="FAIL"),None)} for k,v in report["cores"].items()}},sort_keys=True))
  return code
 except Exception as e:
  report["status"]="DEVELOPMENT_NOT_EXECUTABLE"; report["infrastructure_error"]=str(e)[:1200]; write(report)
  print(json.dumps({"status":"DEVELOPMENT_NOT_EXECUTABLE","error":str(e)[:800]})); return 30

if __name__=="__main__": raise SystemExit(main())
