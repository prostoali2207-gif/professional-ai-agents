#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import hashlib, json, os, shutil, sys, tempfile, urllib.error, urllib.request, zipfile
from pathlib import Path
from cryptography.fernet import Fernet

ROOT=Path.cwd()
CYCLE="growth-strategy-experiment-portfolio-v0.1-heldout-2026-08-22-clean"
COMMIT="1c042d09695dfe2d4186c21d136474dc9d1fbdd9"
DIGEST="sha256:59dd74cb772f1259a7ed5f6b9da4aa40db7f48be21c380b605bdc044f4dd7b92"
MODEL="gemini-3.5-flash-lite"
ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
FAMILIES=["GS-BV","GS-BD","GS-EV","GS-MH","GS-AS","GS-PP","GS-ED","GS-MB","GS-CH","GS-CF","GS-LI","GS-BA"]
PAIRS={"P-BV-PROXY":"GS-BV","P-EV-COMPARABILITY":"GS-EV","P-MB-MATURITY":"GS-MB","P-PP-CAPACITY":"GS-PP","P-BA-AUTHORITY":"GS-BA","P-MH-CONFIDENCE":"GS-MH","P-LI-WORDING":"GS-LI"}
BASE=ROOT/"architect/evaluation/growth_strategy_experiment_portfolio"
PARTS=BASE/"sealed/heldout-v0.1-2026-08-22-clean.parts"
MANIFEST=BASE/"sealed/heldout-v0.1-2026-08-22-clean.qualification.json"
DESIGN=ROOT/"architect/research/growth-strategy-experiment-portfolio/qualification-design-v0.1.md"
PREREG=BASE/"qualification-preregistration-v0.1.json"
RUNNER=BASE/"sealed_runner_template_v0_1.py"

def h(data:bytes)->str: return hashlib.sha256(data).hexdigest()

def extract(raw:dict)->str:
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            c=step.get("content")
            if isinstance(c,str): return c
            for item in c or []:
                if isinstance(item,dict) and item.get("type")=="text" and isinstance(item.get("text"),str): return item["text"]
    raise RuntimeError("author returned no observable text")

def parse(text:str):
    text=text.strip()
    if text.startswith("```"): text="\n".join(text.splitlines()[1:-1]).strip()
    return json.loads(text)

def author()->list[dict]:
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing before authoring")
    prompt=f"""PUBLIC DESIGN:\n{DESIGN.read_text()}\n\nPREREGISTRATION:\n{PREREG.read_text()}\n\nCreate exactly 24 fresh adversarial fixtures, exactly two per family {FAMILIES}. Return JSON array only. Each object: id, family, pair_id, task, hidden_reference. hidden_reference must contain professional_disposition, required_evidence_or_reasoning, failure_traps, critical_flag_if_triggered, boundary_expectation. For non-paired fixtures pair_id=null. Required pairs: P-BV-PROXY=GS-BV; P-EV-COMPARABILITY=GS-EV; P-MB-MATURITY=GS-MB; P-PP-CAPACITY=GS-PP; P-BA-AUTHORITY=GS-BA; P-MH-CONFIDENCE=GS-MH; P-LI-WORDING=GS-LI. Each required pair has exactly two cases and follows the public contrastive requirement. Do not reveal hidden_reference in task. Include realistic pressure/adversarial cues where construct-relevant."""
    body={"model":MODEL,"system_instruction":"You are an independent senior growth-strategy evaluation designer. Create fresh held-out work samples. Do not copy public examples verbatim. Return JSON only.","input":prompt,"store":False,"generation_config":{"thinking_level":"medium"}}
    req=urllib.request.Request(ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",headers={"Content-Type":"application/json","x-goog-api-key":key})
    try:
        with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
    except urllib.error.HTTPError as e: raise RuntimeError(f"authoring HTTP {e.code}: {e.read().decode(errors='replace')[:1200]}") from e
    cases=parse(extract(raw))
    if not isinstance(cases,list) or len(cases)!=24: raise RuntimeError("authoring cardinality invalid")
    ids=[c.get("id") for c in cases]; fam=Counter(c.get("family") for c in cases)
    if None in ids or len(ids)!=len(set(ids)): raise RuntimeError("fixture IDs invalid")
    if set(fam)!=set(FAMILIES) or set(fam.values())!={2}: raise RuntimeError(f"family structure invalid: {dict(fam)}")
    for p,f in PAIRS.items():
        members=[c for c in cases if c.get("pair_id")==p]
        if len(members)!=2 or {x.get("family") for x in members}!={f}: raise RuntimeError(f"pair structure invalid: {p}")
    for c in cases:
        if not isinstance(c.get("task"),str) or not isinstance(c.get("hidden_reference"),dict): raise RuntimeError("fixture fields invalid")
    return cases

def build(cases:list[dict], d:Path)->tuple[bytes,dict]:
    fixtures=[{"id":c["id"],"family":c["family"],"pair_id":c.get("pair_id"),"task":c["task"]} for c in cases]
    grader={c["id"]:c["hidden_reference"] for c in cases}
    (d/"fixtures.json").write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+"\n")
    (d/"grader.json").write_text(json.dumps(grader,ensure_ascii=False,indent=2)+"\n")
    shutil.copyfile(RUNNER,d/"runner.py")
    hashes={n:h((d/n).read_bytes()) for n in ["fixtures.json","grader.json","runner.py"]}
    canonical="".join(f"{n}:{hashes[n]}\n" for n in sorted(hashes)); pack_digest="sha256:"+h(canonical.encode())
    freeze={"cycle_id":CYCLE,"candidate_commit":COMMIT,"candidate_digest":DIGEST,"model":MODEL,"fixture_count":24,"family_count":12,"per_family":2,"fixtures_sha256":"sha256:"+hashes["fixtures.json"],"grader_sha256":"sha256:"+hashes["grader.json"],"runner_sha256":"sha256:"+hashes["runner.py"],"pack_digest":pack_digest,"trial_count_per_fixture":1,"professional_failure_retry_count":0}
    (d/"freeze-record.json").write_text(json.dumps(freeze,indent=2,sort_keys=True)+"\n")
    z=d.parent/"pack.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED) as q:
        for n in ["fixtures.json","grader.json","runner.py","freeze-record.json"]: q.write(d/n,arcname=n)
    return z.read_bytes(),freeze

def main()->int:
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode().strip()
    if not master: raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing before held-out authoring")
    if not os.environ.get("GEMINI_API_KEY","").strip(): raise RuntimeError("GEMINI_API_KEY missing before held-out authoring")
    sys.path.insert(0,str(ROOT/"architect/evaluation/qualification-platform"))
    from sealed_pack_keys import derive_fernet_key,key_fingerprint_sha256
    cases=author()
    with tempfile.TemporaryDirectory(prefix="strategist-heldout-") as td:
        d=Path(td)/"pack"; d.mkdir(); raw,freeze=build(cases,d); key=derive_fernet_key(master,CYCLE); token=Fernet(key).encrypt(raw)
    if PARTS.exists(): shutil.rmtree(PARTS)
    PARTS.mkdir(parents=True); text=token.decode("ascii"); chunks=[text[i:i+4000] for i in range(0,len(text),4000)]
    for i,c in enumerate(chunks): (PARTS/f"{i:02d}").write_text(c)
    m={"version":2,"cycle_id":CYCLE,
       "candidate":{"commit":COMMIT,"digest":DIGEST,"manifest_path":"architect/research/growth-strategy-experiment-portfolio/candidate-artifact-manifest-v0.1.json"},
       "runtime":{"executor_path":"architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py","executor_cmd":"python3 architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py","protocol":"growth-strategy-experiment-portfolio-candidate-v1","provider":"gemini-interactions-api","model":MODEL,"credential_env":"GEMINI_API_KEY","candidate_timeout_seconds":180,"model_timeout_seconds":120,"workflow_timeout_seconds":1800,"contract_probe_argv":["python3","architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py","--qualification-contract"],"tool_protocol":"none-v1","state_protocol":"stateless-v1","observable_protocol":"final-output-only-v1","canary_required":True,"canary_cmd":"python3 architect/evaluation/growth_strategy_experiment_portfolio/executor_v0_1_gemini.py --canary --model-timeout 120"},
       "sealed_pack":{"parts_dir":str(PARTS.relative_to(ROOT)),"part_count":len(chunks),"ciphertext_length":len(token),"ciphertext_sha256":h(token),"key_derivation":{"scheme":"hkdf-sha256-v1","master_env":"QUALIFICATION_SEALED_PACK_MASTER_KEY","context":CYCLE},"key_fingerprint_sha256":key_fingerprint_sha256(key),"decrypted_zip_sha256":h(raw),"pack_digest":freeze["pack_digest"],"required_files":["fixtures.json","grader.json","runner.py","freeze-record.json"]},
       "evaluation":{"fixture_count":24,"family_count":12,"per_family":2,"fixtures_file":"fixtures.json","grader_file":"grader.json","runner_file":"runner.py","freeze_record_file":"freeze-record.json"},
       "report":{"sanitized_required":True,"artifact_required":True,"validator_path":"architect/evaluation/qualification-platform/validate_sanitized_report.py","release_ledger_required":True},
       "verdict":{"runner_exit_zero_required":True,"missing_report_is_failure":True,"report_validation_required":True,"artifact_upload_required":True}}
    MANIFEST.parent.mkdir(parents=True,exist_ok=True); MANIFEST.write_text(json.dumps(m,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"SEALED_PACK_AUTHORED","fixture_count":24,"part_count":len(chunks),"ciphertext_sha256":m["sealed_pack"]["ciphertext_sha256"],"pack_digest":freeze["pack_digest"],"hidden_content_printed":False}))
    return 0

if __name__=="__main__": raise SystemExit(main())
