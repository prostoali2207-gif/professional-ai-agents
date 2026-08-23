#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import hashlib, json, os, shutil, sys, tempfile, urllib.request, zipfile
from pathlib import Path
from cryptography.fernet import Fernet

ROOT=Path.cwd()
CYCLE="growth-strategy-experiment-portfolio-v0.1-heldout-2026-08-23-r2"
COMMIT="1c042d09695dfe2d4186c21d136474dc9d1fbdd9"
DIGEST="sha256:59dd74cb772f1259a7ed5f6b9da4aa40db7f48be21c380b605bdc044f4dd7b92"
MODEL="gemini-3.5-flash-lite"
GROQ_MODEL="qwen/qwen3.6-27b"
FAMILIES=["GS-BV","GS-BD","GS-EV","GS-MH","GS-AS","GS-PP","GS-ED","GS-MB","GS-CH","GS-CF","GS-LI","GS-BA"]
PAIRS={"P-BV-PROXY":"GS-BV","P-EV-COMPARABILITY":"GS-EV","P-MB-MATURITY":"GS-MB","P-PP-CAPACITY":"GS-PP","P-BA-AUTHORITY":"GS-BA","P-MH-CONFIDENCE":"GS-MH","P-LI-WORDING":"GS-LI"}
BASE=ROOT/"architect/evaluation/growth_strategy_experiment_portfolio"
PARTS=BASE/"sealed/heldout-v0.1-2026-08-23-r2.parts"
MANIFEST=BASE/"sealed/heldout-v0.1-2026-08-23-r2.qualification.json"
DESIGN=ROOT/"architect/research/growth-strategy-experiment-portfolio/qualification-design-v0.1.md"
PREREG=BASE/"qualification-preregistration-v0.1.json"
RUNNER=BASE/"sealed_runner_template_v0_1_r2.py"

def h(data:bytes)->str: return hashlib.sha256(data).hexdigest()
def parse(t:str):
    t=t.strip()
    if t.startswith("```"): t="\n".join(t.splitlines()[1:-1]).strip()
    return json.loads(t)
def gtext(raw:dict)->str:
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            c=step.get("content")
            if isinstance(c,str): return c
            if isinstance(c,list):
                z="".join(i.get("text","") for i in c if isinstance(i,dict))
                if z: return z
    raise RuntimeError("Gemini author returned no text")
def validate(cases:list[dict])->list[dict]:
    if not isinstance(cases,list) or len(cases)!=24: raise RuntimeError("fixture cardinality invalid")
    fam=Counter(x.get("family") for x in cases)
    if set(fam)!=set(FAMILIES) or set(fam.values())!={2}: raise RuntimeError("family structure invalid")
    ids=[x.get("id") for x in cases]
    if None in ids or len(ids)!=len(set(ids)): raise RuntimeError("fixture ids invalid")
    for p,f in PAIRS.items():
        m=[x for x in cases if x.get("pair_id")==p]
        if len(m)!=2 or {x.get("family") for x in m}!={f}: raise RuntimeError(f"pair structure invalid: {p}")
    for c in cases:
        if not isinstance(c.get("task"),str) or not isinstance(c.get("hidden_reference"),dict): raise RuntimeError("fixture fields invalid")
    return cases
def author()->list[dict]:
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing")
    prompt=f"PUBLIC DESIGN:\n{DESIGN.read_text()}\n\nPREREGISTRATION:\n{PREREG.read_text()}\n\nCreate exactly 24 fresh adversarial held-out fixtures, two per family {FAMILIES}. Return JSON array only. Fields: id, family, pair_id, task, hidden_reference. hidden_reference fields: professional_disposition, required_evidence_or_reasoning, failure_traps, critical_flag_if_triggered, boundary_expectation. Required pairs: {PAIRS}. Do not reveal hidden_reference in task. Do not copy public examples verbatim."
    body={"model":MODEL,"system_instruction":"You are an independent senior growth-strategy evaluation designer. Create authentic construct-valid work samples. JSON only.","input":prompt,"store":False,"generation_config":{"thinking_level":"medium"}}
    req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/interactions",data=json.dumps(body,ensure_ascii=False).encode(),method="POST",headers={"x-goog-api-key":key,"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=180) as r: return validate(parse(gtext(json.loads(r.read().decode()))))
def review(cases:list[dict])->list[dict]:
    key=os.environ.get("GROQ_API_KEY","").strip()
    if not key: raise RuntimeError("GROQ_API_KEY missing")
    payload={"task":"Audit and repair these hidden fixtures before candidate execution. Preserve exactly 24 cases, 12 families x2 and all declared pairs. Remove ambiguity, leakage, stylistic-only grading, impossible requirements, and hidden references exceeding supplied facts. Preserve the registered constructs, hard-fail semantics and contrastive intent.","families":FAMILIES,"pairs":PAIRS,"cases":cases}
    body={"model":GROQ_MODEL,"messages":[{"role":"system","content":"You are an independent evaluation scientist and senior growth-strategy assessor. Return only a JSON object with key cases."},{"role":"user","content":json.dumps(payload,ensure_ascii=False)}],"temperature":0,"reasoning_format":"hidden","response_format":{"type":"json_object"}}
    req=urllib.request.Request("https://api.groq.com/openai/v1/chat/completions",data=json.dumps(body,ensure_ascii=False).encode(),method="POST",headers={"Authorization":"Bearer "+key,"Content-Type":"application/json","Accept":"application/json","User-Agent":"professional-ai-agents-strategist-r2/1.0"})
    with urllib.request.urlopen(req,timeout=180) as r:
        raw=json.loads(r.read().decode()); obj=json.loads(raw["choices"][0]["message"]["content"]); return validate(obj["cases"])
def build(cases:list[dict],d:Path)->tuple[bytes,dict]:
    fixtures=[{"id":c["id"],"family":c["family"],"pair_id":c.get("pair_id"),"task":c["task"]} for c in cases]
    grader={c["id"]:c["hidden_reference"] for c in cases}
    (d/"fixtures.json").write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+"\n")
    (d/"grader.json").write_text(json.dumps(grader,ensure_ascii=False,indent=2)+"\n")
    shutil.copyfile(RUNNER,d/"runner.py")
    hashes={n:h((d/n).read_bytes()) for n in ["fixtures.json","grader.json","runner.py"]}
    pack_digest="sha256:"+h("".join(f"{n}:{hashes[n]}\n" for n in sorted(hashes)).encode())
    freeze={"cycle_id":CYCLE,"candidate_commit":COMMIT,"candidate_digest":DIGEST,"candidate_model":MODEL,"judge_models":[MODEL,GROQ_MODEL],"fixture_count":24,"family_count":12,"per_family":2,"contrastive_pair_count":7,"fixtures_sha256":"sha256:"+hashes["fixtures.json"],"grader_sha256":"sha256:"+hashes["grader.json"],"runner_sha256":"sha256:"+hashes["runner.py"],"pack_digest":pack_digest,"thresholds":{"minimum_pass_rate":0.90,"hard_fail_count":0,"all_pairs_consistent":True,"family_dimension_min":{"decision_correctness":1.7,"boundary_integrity":1.7,"evidence_calibration":1.5,"mechanism_judgment":1.5}},"trial_count_per_fixture":1,"professional_failure_retry_count":0}
    (d/"freeze-record.json").write_text(json.dumps(freeze,indent=2,sort_keys=True)+"\n")
    z=d.parent/"pack.zip"
    with zipfile.ZipFile(z,"w",zipfile.ZIP_DEFLATED) as q:
        for n in ["fixtures.json","grader.json","runner.py","freeze-record.json"]: q.write(d/n,arcname=n)
    return z.read_bytes(),freeze
def main()->int:
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode().strip()
    if not master: raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    if not os.environ.get("GEMINI_API_KEY","").strip(): raise RuntimeError("GEMINI_API_KEY missing")
    if not os.environ.get("GROQ_API_KEY","").strip(): raise RuntimeError("GROQ_API_KEY missing")
    sys.path.insert(0,str(ROOT/"architect/evaluation/qualification-platform"))
    from sealed_pack_keys import derive_fernet_key,key_fingerprint_sha256
    cases=review(author())
    with tempfile.TemporaryDirectory(prefix="strategist-r2-heldout-") as td:
        d=Path(td)/"pack"; d.mkdir(); raw,freeze=build(cases,d); key=derive_fernet_key(master,CYCLE); token=Fernet(key).encrypt(raw)
    if PARTS.exists(): shutil.rmtree(PARTS)
    PARTS.mkdir(parents=True); text=token.decode("ascii"); chunks=[text[i:i+4000] for i in range(0,len(text),4000)]
    for i,c in enumerate(chunks): (PARTS/f"{i:02d}").write_text(c)
    manifest={"version":2,"cycle_id":CYCLE,"candidate":{"commit":COMMIT,"digest":DIGEST,"manifest_path":"architect/research/growth-strategy-experiment-portfolio/candidate-artifact-manifest-v0.1.json"},"runtime":{"executor_path":"architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py","executor_cmd":"python3 architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py","protocol":"growth-strategy-experiment-portfolio-candidate-v1","provider":"gemini-interactions-api","model":MODEL,"credential_env":"GEMINI_API_KEY","candidate_timeout_seconds":180,"model_timeout_seconds":120,"workflow_timeout_seconds":2100,"contract_probe_argv":["python3","architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py","--qualification-contract"],"tool_protocol":"none-v1","state_protocol":"stateless-v1","observable_protocol":"final-output-only-v1","canary_required":True,"canary_cmd":"python3 architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py --canary --model-timeout 120"},"sealed_pack":{"parts_dir":str(PARTS.relative_to(ROOT)),"part_count":len(chunks),"ciphertext_length":len(token),"ciphertext_sha256":h(token),"key_derivation":{"scheme":"hkdf-sha256-v1","master_env":"QUALIFICATION_SEALED_PACK_MASTER_KEY","context":CYCLE},"key_fingerprint_sha256":key_fingerprint_sha256(key),"decrypted_zip_sha256":h(raw),"pack_digest":freeze["pack_digest"],"required_files":["fixtures.json","grader.json","runner.py","freeze-record.json"]},"evaluation":{"fixture_count":24,"family_count":12,"per_family":2,"fixtures_file":"fixtures.json","grader_file":"grader.json","runner_file":"runner.py","freeze_record_file":"freeze-record.json"},"report":{"sanitized_required":True,"artifact_required":True,"validator_path":"architect/evaluation/qualification-platform/validate_sanitized_report.py","release_ledger_required":True},"verdict":{"runner_exit_zero_required":True,"missing_report_is_failure":True,"report_validation_required":True,"artifact_upload_required":True}}
    MANIFEST.parent.mkdir(parents=True,exist_ok=True); MANIFEST.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"SEALED_PACK_AUTHORED","cycle_id":CYCLE,"fixture_count":24,"part_count":len(chunks),"pack_digest":freeze["pack_digest"],"hidden_content_printed":False}))
    return 0
if __name__=="__main__": raise SystemExit(main())
