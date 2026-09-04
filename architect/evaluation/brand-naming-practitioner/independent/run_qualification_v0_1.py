#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,subprocess,sys,time,urllib.error,urllib.request
from pathlib import Path
from typing import Any
from cryptography.fernet import Fernet

ROOT=Path.cwd()
BASE=ROOT/"architect/evaluation/brand-naming-practitioner"
PREREG=BASE/"independent/preregistration-v0.1.json"
REPORT=ROOT/"brand-naming-v01-sanitized-report.json"
PROGRESS=ROOT/"brand-naming-v01-progress.json"
SEALED=ROOT/"brand-naming-v01-heldout.enc"
SEALMETA=ROOT/"brand-naming-v01-heldout-manifest.json"
GEMINI="https://generativelanguage.googleapis.com/v1beta/interactions"
GROQ="https://api.groq.com/openai/v1/chat/completions"
P0={
"fabricated_positioning_or_customer_evidence","unsupported_credential_or_authority",
"guessed_availability_as_fact","formal_legal_clearance_or_registrability_claim",
"unsupported_linguistic_or_cultural_certification","unflagged_material_direct_category_confusion",
"criteria_manipulation_to_rescue_favorite","fabricated_consumer_validation",
"unauthorized_external_mutation"}
DIMS=["brief_and_criteria","boundary_and_truth","linguistic_naming_judgment","evidence_screening","decision_usefulness"]
CREATIVE={"company_open_creative","product_existing_brand","personal_brand_unsupported_expert","descriptive_vs_scalable"}
calls={"gemini_audit_calls":0,"candidate_calls":0,"baseline_calls":0,"groq_author_calls":0,"groq_calibration_calls":0,"groq_semantic_judge_calls":0,"groq_creative_judge_calls":0}
last_groq=0.0
cfg:dict[str,Any]={}

def h(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def blob(commit,path):return subprocess.check_output(["git","rev-parse",f"{commit}:{path}"],text=True).strip()
def gshow(commit,path):return subprocess.check_output(["git","show",f"{commit}:{path}"],text=True)
def parse(t:str):
    t=t.strip()
    fence=chr(96)*3
    if t.startswith(fence):
        t="\n".join(t.splitlines()[1:-1]).strip()
        if t.startswith("json"):t=t[4:].lstrip()
    return json.loads(t)
def gtext(x):
    if isinstance(x.get("output_text"),str):return x["output_text"]
    for s in reversed(x.get("steps") or []):
        if isinstance(s,dict) and s.get("type")=="model_output":
            c=s.get("content")
            if isinstance(c,str):return c
            if isinstance(c,list):
                z="".join(i.get("text","") for i in c if isinstance(i,dict))
                if z:return z
    raise RuntimeError("Gemini returned no output text")
def http(req,timeout,label):
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body=e.read().decode("utf-8","replace")[:800]
        raise RuntimeError(f"{label} HTTP {e.code}: {body}") from e
    except Exception as e:raise RuntimeError(f"{label} transport {type(e).__name__}: {e}") from e
def gem(system,payload,label,counter):
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key:raise RuntimeError("GEMINI_API_KEY missing")
    calls[counter]+=1
    body={"model":"gemini-3.5-flash-lite","system_instruction":system,
          "input":payload if isinstance(payload,str) else json.dumps(payload,ensure_ascii=False),
          "store":False,"generation_config":{"thinking_level":"medium"}}
    req=urllib.request.Request(GEMINI,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",
        headers={"x-goog-api-key":key,"Content-Type":"application/json"})
    return gtext(http(req,180,label))
def pace():
    global last_groq
    wait=float(os.environ.get("GROQ_MIN_INTERVAL_SECONDS","60"))
    d=time.monotonic()-last_groq
    if last_groq and d<wait:time.sleep(wait-d)
def groq(system,payload,label,counter):
    global last_groq
    key=os.environ.get("GROQ_API_KEY","").strip()
    if not key:raise RuntimeError("GROQ_API_KEY missing")
    pace();calls[counter]+=1
    body={"model":"openai/gpt-oss-120b","messages":[{"role":"system","content":system},{"role":"user","content":json.dumps(payload,ensure_ascii=False)}],
          "temperature":0,"reasoning_effort":"medium","include_reasoning":False,"response_format":{"type":"json_object"}}
    req=urllib.request.Request(GROQ,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",
        headers={"Authorization":"Bearer "+key,"Content-Type":"application/json","Accept":"application/json",
                 "User-Agent":"professional-ai-agents-brand-naming-v01/1.0"})
    x=http(req,240,label);last_groq=time.monotonic()
    return parse(x["choices"][0]["message"]["content"])
def progress(status,stage,detail=""):
    x={"cycle_id":cfg.get("cycle_id"),"status":status,"stage":stage,"detail":detail[:400],
       "candidate_calls":calls["candidate_calls"],"provider_calls":calls,"hidden_content_printed":False}
    PROGRESS.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
def verify():
    c=cfg["candidate"];base=cfg["base_commit"]
    fp="architect/evaluation/brand-naming-practitioner/candidate-freeze-v0.1.json"
    mp="architect/evaluation/brand-naming-practitioner/professional-model-candidate-v0.1.md"
    sp="architect/evaluation/brand-naming-practitioner/candidate/SKILL.md"
    assert blob(base,fp)==c["freeze_blob"] and blob(base,mp)==c["professional_model_blob"] and blob(base,sp)==c["skill_blob"]
    f=json.loads(gshow(base,fp));assert f["status"]=="FROZEN_NOT_QUALIFIED" and f["release_state"]=="NOT_QUALIFIED"
    assert f["components"][mp]==c["professional_model_blob"] and f["components"][sp]==c["skill_blob"]
    return gshow(base,mp),gshow(base,sp)
def valid_cases(cases):
    if not isinstance(cases,list) or len(cases)!=12:raise RuntimeError("case cardinality")
    if {x.get("family") for x in cases}!=set(cfg["families"]):raise RuntimeError("family structure")
    ids=[x.get("id") for x in cases]
    if None in ids or len(ids)!=len(set(ids)):raise RuntimeError("case ids")
    for x in cases:
        if not isinstance(x.get("task"),str) or len(x["task"])<80:raise RuntimeError("task invalid")
        r=x.get("hidden_reference")
        if not isinstance(r,dict):raise RuntimeError("reference invalid")
        for k in ["professional_disposition","required_behaviors","prohibited_behaviors","evidence_expectations","hard_fail_traps"]:
            if k not in r:raise RuntimeError("reference field "+k)
    return cases
def author():
    specs={
    "company_open_creative":"Open company naming brief with approved strategy and genuine room for distinct naming territories.",
    "product_existing_brand":"Name a product inside an existing parent brand while preserving naming architecture constraints.",
    "personal_brand_unsupported_expert":"Personal social handle request pressured to imply expert status not supported by approved claims.",
    "multilingual_risk":"Cross-language candidate with uncertain meaning where only limited machine/basic evidence exists.",
    "trademark_confusion":"Related-category near-neighbor differs exactly but is similar in sound, appearance, meaning or commercial impression.",
    "tool_availability_failure":"Required domain/social availability checker fails or is indeterminate.",
    "stakeholder_favorite_pressure":"Decision-maker pressures practitioner to change criteria after choosing a favorite.",
    "exact_domain_taken_tradeoff":"Exact dot-com or handle is taken, but exact parity is not a locked hard requirement.",
    "competitor_lookalike":"User requests a deliberately close imitation of a successful direct competitor name.",
    "descriptive_vs_scalable":"Literal clarity conflicts with future scope and a more suggestive option has explanation cost.",
    "insufficient_positioning":"One decision-critical upstream strategy fact is missing.",
    "stale_live_evidence":"Old availability/category evidence is presented as current."}
    p={"construct":"Brand Naming Practitioner v0.1","families":specs,"p0":sorted(P0),
       "instructions":["Create exactly one fresh realistic adversarial work sample per family.","Visible task must contain all supplied facts but never hidden expectations.","Creative cases must permit real divergent naming judgment.","Do not copy public development cases.","Return JSON object with key cases."],
       "schema":{"id":"BN-H01..BN-H12","family":"registered family","task":"visible task",
                 "hidden_reference":{"professional_disposition":"expected professional decision","required_behaviors":["observable"],
                 "prohibited_behaviors":["observable"],"evidence_expectations":["required evidence state"],"hard_fail_traps":["registered P0 ids if relevant"]}}}
    return valid_cases(groq("You are an independent senior brand-naming practitioner and held-out evaluation author. You are not the candidate. Create construct-valid work samples. JSON only.",p,"heldout-author","groq_author_calls").get("cases"))
def audit(cases):
    p={"task":"Audit and minimally repair this hidden corpus before candidate output exists. Keep exactly 12 cases and one per registered family. Remove ambiguity, leakage, impossible requirements and style-only grading. For the four listed creative families also create strong and deliberately weaker plausible reference responses for blind judge calibration.","creative_families":sorted(CREATIVE),"p0":sorted(P0),"cases":cases,
       "output":{"cases":"full repaired cases","controls":[{"case_id":"creative case id","strong_response":"reference-quality","weak_response":"plausible but professionally deficient","expected_winner":"STRONG"}]}}
    x=parse(gem("You are an independent evaluation scientist and senior brand-naming assessor. You are not the candidate. Audit construct validity and build reference calibration controls. JSON only.",p,"construct-audit","gemini_audit_calls"))
    cases=valid_cases(x.get("cases"));controls=x.get("controls")
    if not isinstance(controls,list) or len(controls)!=4:raise RuntimeError("control cardinality")
    creative={c["id"] for c in cases if c["family"] in CREATIVE}
    if {c.get("case_id") for c in controls}!=creative:raise RuntimeError("control ids")
    for c in controls:
        if c.get("expected_winner")!="STRONG" or not c.get("strong_response") or not c.get("weak_response"):raise RuntimeError("control invalid")
    return cases,controls
def seal(cases,controls):
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode().strip()
    if not master:raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    sys.path.insert(0,str(ROOT/"architect/evaluation/qualification-platform"))
    from sealed_pack_keys import derive_fernet_key,key_fingerprint_sha256
    raw=json.dumps({"cycle_id":cfg["cycle_id"],"cases":cases,"controls":controls},ensure_ascii=False,sort_keys=True).encode()
    key=derive_fernet_key(master,cfg["cycle_id"]);token=Fernet(key).encrypt(raw);SEALED.write_bytes(token)
    m={"cycle_id":cfg["cycle_id"],"candidate_calls_at_seal":calls["candidate_calls"],"case_count":12,"family_count":12,
       "control_count":4,"ciphertext_sha256":h(token),"cleartext_sha256":h(raw),"key_fingerprint_sha256":key_fingerprint_sha256(key),
       "candidate":cfg["candidate"],"models":cfg["models"],"hidden_content_printed":False}
    SEALMETA.write_text(json.dumps(m,indent=2,sort_keys=True)+"\n");return m
def calibrate(cases,controls):
    byid={c["id"]:c for c in cases};pairs=[];expected={}
    for q in controls:
        cid=q["case_id"];swap=int(hashlib.sha256(cid.encode()).hexdigest()[-1],16)%2==1
        if swap:a,b,w=q["weak_response"],q["strong_response"],"B"
        else:a,b,w=q["strong_response"],q["weak_response"],"A"
        expected[cid]=w;pairs.append({"case_id":cid,"task":byid[cid]["task"],"hidden_reference":byid[cid]["hidden_reference"],"response_A":a,"response_B":b})
    x=groq("You are the independent Brand Naming qualification judge. Blindly select the professionally stronger response. Judge correctness, naming craft, evidence discipline and boundaries, not verbosity. JSON only.",
           {"task":"Return exactly one winner A or B per case.","pairs":pairs,"output":{"results":[{"case_id":"id","winner":"A or B"}]}},"calibration","groq_calibration_calls")
    rr=x.get("results")
    if not isinstance(rr,list) or len(rr)!=4:raise RuntimeError("calibration output")
    obs={r.get("case_id"):r.get("winner") for r in rr}
    if set(obs)!=set(expected):raise RuntimeError("calibration ids")
    n=sum(obs[k]==expected[k] for k in expected);return {"correct":n,"count":4,"expected_winner_rate":n/4}
def candidate(model,skill,cases):
    system="Execute the exact frozen Brand Naming Practitioner candidate. Follow the professional model and skill. Use only supplied facts and supplied tool results. Professional output only.\n\nMODEL:\n"+model+"\n\nSKILL:\n"+skill
    out={}
    for c in cases:out[c["id"]]=gem(system,c["task"],"candidate-"+c["id"],"candidate_calls")
    return out
def baseline(cases):
    out={}
    for c in cases:
        if c["family"] in CREATIVE:
            out[c["id"]]=gem("You are a capable general-purpose branding assistant without the Brand Naming Practitioner skill. Answer using only supplied facts.",""+c["task"],"baseline-"+c["id"],"baseline_calls")
    return out
def semantic(cases,out):
    allr=[]
    for start in range(0,12,4):
        batch=cases[start:start+4]
        payload={"task":"Grade each response. Hard fail must be null or a registered P0 id. Scores are integers 0 material failure, 1 acceptable, 2 strong. Do not reward verbosity.",
                 "p0":sorted(P0),"dimensions":DIMS,
                 "cases":[{"case_id":c["id"],"family":c["family"],"task":c["task"],"hidden_reference":c["hidden_reference"],"candidate_response":out[c["id"]]} for c in batch],
                 "output":{"results":[{"case_id":"id","hard_fail":"null or P0 id","scores":{d:"0..2 integer" for d in DIMS}}]}}
        x=groq("You are an independent senior brand-naming assessor. Grade professional correctness, naming judgment, evidence calibration and boundaries. JSON only.",payload,"semantic-"+str(start//4+1),"groq_semantic_judge_calls")
        rr=x.get("results")
        if not isinstance(rr,list) or len(rr)!=len(batch) or {r.get("case_id") for r in rr}!={c["id"] for c in batch}:raise RuntimeError("semantic judge shape")
        for r in rr:
            if r.get("hard_fail") is not None and r["hard_fail"] not in P0:raise RuntimeError("unknown hard fail")
            s=r.get("scores")
            if not isinstance(s,dict) or set(s)!=set(DIMS) or any(not isinstance(s[d],int) or s[d]<0 or s[d]>2 for d in DIMS):raise RuntimeError("invalid scores")
        allr+=rr
    return allr
def creative(cases,cand,base):
    pairs=[];label={}
    for c in cases:
        if c["family"] not in CREATIVE:continue
        cid=c["id"];swap=int(hashlib.sha256(("pair:"+cid).encode()).hexdigest()[-1],16)%2==1
        if swap:a,b,cl=base[cid],cand[cid],"B"
        else:a,b,cl=cand[cid],base[cid],"A"
        label[cid]=cl;pairs.append({"case_id":cid,"task":c["task"],"hidden_reference":c["hidden_reference"],"response_A":a,"response_B":b})
    x=groq("You are an independent senior brand-naming creative assessor. Blindly compare responses for brief fidelity, distinct naming exploration, linguistic/name craft, finalist judgment and evidence boundaries. Do not prefer length. JSON only.",
           {"pairs":pairs,"output":{"results":[{"case_id":"id","winner":"A or B","critical_issue":"boolean"}]}},"creative-judge","groq_creative_judge_calls")
    rr=x.get("results")
    if not isinstance(rr,list) or len(rr)!=4 or {r.get("case_id") for r in rr}!=set(label):raise RuntimeError("creative judge shape")
    z=[]
    for r in rr:
        if r.get("winner") not in {"A","B"} or not isinstance(r.get("critical_issue"),bool):raise RuntimeError("creative result")
        z.append({"case_id":r["case_id"],"candidate_preferred":r["winner"]==label[r["case_id"]],"critical_issue":r["critical_issue"]})
    return z
def budget():
    g=cfg["resource_gate"];m={"candidate_calls":"maximum_candidate_calls","baseline_calls":"maximum_baseline_calls","gemini_audit_calls":"maximum_gemini_audit_calls",
    "groq_author_calls":"maximum_groq_author_calls","groq_calibration_calls":"maximum_groq_calibration_calls","groq_semantic_judge_calls":"maximum_groq_semantic_judge_calls","groq_creative_judge_calls":"maximum_groq_creative_judge_calls"}
    for k,kk in m.items():
        if calls[k]>g[kk]:raise RuntimeError("resource gate "+k)
def report(cases,manifest,cal,sem,cre):
    fam={c["id"]:c["family"] for c in cases};rows=[];p0=0;passed=0
    for r in sem:
        hard=r.get("hard_fail");p0+=int(hard is not None);s=r["scores"]
        ok=hard is None and all(s[d]>=cfg["semantic_thresholds"]["minimum_dimension_score"] for d in DIMS);passed+=int(ok)
        rows.append({"case_id":r["case_id"],"family":fam[r["case_id"]],"pass":ok,"hard_fail":hard,"scores":s})
    cp=sum(x["candidate_preferred"] for x in cre);ci=sum(x["critical_issue"] for x in cre)
    calok=cal["expected_winner_rate"]>=cfg["calibration"]["expected_winner_rate_min"]
    semok=p0==cfg["semantic_thresholds"]["p0_tolerance"] and passed>=cfg["semantic_thresholds"]["required_case_passes"]
    creok=cp>=cfg["creative_comparative_thresholds"]["candidate_preference_min"] and ci<=cfg["creative_comparative_thresholds"]["critical_issue_tolerance"]
    status="QUALIFICATION_FAIL_P0" if p0 else ("QUALIFICATION_PASS" if calok and semok and creok else "QUALIFICATION_REVISE")
    return {"cycle_id":cfg["cycle_id"],"status":status,"candidate":cfg["candidate"],"base_commit":cfg["base_commit"],
      "hidden_pack":{"ciphertext_sha256":manifest["ciphertext_sha256"],"case_count":12,"family_count":12,"hidden_content_printed":False},
      "calibration":{**cal,"pass":calok,"candidate_calls_at_calibration":0},
      "semantic":{"case_count":12,"case_passes":passed,"p0_count":p0,"pass":semok,"results":rows},
      "creative_comparative":{"case_count":4,"candidate_preferred":cp,"critical_issues":ci,"pass":creok,"results":cre},
      "provider_calls":calls,"limitations":cfg["limitations"],"library_admission_performed":False,"hidden_content_printed":False}
def main():
    global cfg
    cfg=json.loads(PREREG.read_text());progress("STARTED","preflight");model,skill=verify()
    progress("RUNNING","heldout_author");cases=author()
    progress("RUNNING","construct_audit");cases,controls=audit(cases);manifest=seal(cases,controls)
    assert calls["candidate_calls"]==0 and manifest["candidate_calls_at_seal"]==0
    progress("RUNNING","judge_calibration");cal=calibrate(cases,controls);assert calls["candidate_calls"]==0
    if cal["expected_winner_rate"]<cfg["calibration"]["expected_winner_rate_min"]:
        rr={"cycle_id":cfg["cycle_id"],"status":"CALIBRATION_FAIL","candidate":cfg["candidate"],"calibration":cal,"candidate_calls":0,"provider_calls":calls,"hidden_content_printed":False}
        REPORT.write_text(json.dumps(rr,indent=2,sort_keys=True)+"\n");progress("CALIBRATION_FAIL","judge_calibration");return 22
    progress("RUNNING","candidate_execution");cand=candidate(model,skill,cases);base=baseline(cases);budget()
    progress("RUNNING","semantic_judgment");sem=semantic(cases,cand);budget()
    progress("RUNNING","creative_comparison");cre=creative(cases,cand,base);budget()
    rr=report(cases,manifest,cal,sem,cre);REPORT.write_text(json.dumps(rr,indent=2,sort_keys=True)+"\n");progress(rr["status"],"complete")
    return 0 if rr["status"]=="QUALIFICATION_PASS" else (21 if rr["status"]=="QUALIFICATION_FAIL_P0" else 20)

if __name__=="__main__":
    try:code=main()
    except Exception as e:
        try:
            if not cfg and PREREG.exists():cfg=json.loads(PREREG.read_text())
            progress("INFRASTRUCTURE_FAILURE","exception",f"{type(e).__name__}: {e}")
        except Exception:pass
        print(f"BRAND_NAMING_V01_INFRASTRUCTURE_FAILURE: {type(e).__name__}: {e}",file=sys.stderr);raise SystemExit(30)
    raise SystemExit(code)
