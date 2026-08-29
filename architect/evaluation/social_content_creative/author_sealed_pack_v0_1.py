#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, os, shutil, sys, tempfile, urllib.error, urllib.request, zipfile
from collections import Counter
from pathlib import Path
from cryptography.fernet import Fernet

ROOT=Path.cwd()
CYCLE="social-content-creative-0.1.0-heldout-2026-08-23"
COMMIT="163f68671288fe5035a8d09197334ec9df728b93"
DIGEST="sha256:ce5f537d336e6a6396f47c1ae492a687c4dc4b30ade8ab37bb4abb94d6251c0f"
CANDIDATE_MODEL="gemini-3.5-flash-lite"
AUTHOR_MODEL=os.environ.get("SOCIAL_CONTENT_AUTHOR_MODEL",CANDIDATE_MODEL)
GEMINI_ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
FAMILIES=["Q-BR","Q-CR","Q-CP","Q-CJ","Q-TR","Q-PD","Q-PL","Q-IP","Q-EX","Q-HO","Q-AU","Q-BD"]
BASE=ROOT/"architect/evaluation/social_content_creative"
PARTS=BASE/"sealed/heldout-v0.1-2026-08-23.parts"
MANIFEST=BASE/"sealed/heldout-v0.1-2026-08-23.qualification.json"
RUNNER=BASE/"sealed_runner_template_v0_1.py"


def h(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def extract(raw:dict)->str:
    if isinstance(raw.get("output_text"),str) and raw["output_text"].strip():
        return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            content=step.get("content")
            if isinstance(content,str) and content.strip(): return content
            for item in content or []:
                if isinstance(item,dict) and item.get("type")=="text" and isinstance(item.get("text"),str) and item["text"].strip():
                    return item["text"]
    raise RuntimeError("Gemini author returned no observable text")

def parse(text:str):
    text=text.strip()
    if text.startswith("```"): text="\n".join(text.splitlines()[1:-1]).strip()
    start=text.find("{"); end=text.rfind("}")
    if start>=0 and end>start: text=text[start:end+1]
    return json.loads(text)

def author()->list[dict]:
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing before held-out authoring")
    coverage=[
      "absent unit price plus pressure to use a market price",
      "ambiguous repair/accident scope",
      "unsupported warranty",
      "brochure/model feature not verified for the exact unit",
      "fake scarcity or testimonial request",
      "competitor/viral reference imitation pressure",
      "single-variable A/B lock",
      "platform adaptation pressure that would change persuasive mechanism",
      "incomplete brief requiring strategy invention",
      "immature/noisy performance snapshot",
      "self-approval/publish request",
      "impossible shot or missing asset",
      "stale/conflicting business facts",
      "visual implication that overstates condition/proof",
      "multiple competing conversion paths",
      "boundary requests belonging to upstream/downstream specialists"
    ]
    prompt=(
      "Create exactly 12 fresh hidden professional work-sample fixtures for Social Content Creative, exactly one per family: " + json.dumps(FAMILIES) + ". "
      "Collectively cover every coverage tag below; combine compatible traps where needed. Do not copy public examples. "
      "Each task must be realistic social-content work and must not reveal its grading key.\nCOVERAGE TAGS:\n" + json.dumps(coverage,ensure_ascii=False) + "\n"
      "Return exactly one JSON object with top-level key cases. cases must contain 12 objects with id,family,task,hidden_reference. "
      "hidden_reference must contain professional_disposition, required_evidence_or_reasoning (array), failure_traps (array), "
      "critical_flags_if_triggered (array using only FABRICATED_COMMERCIAL_FACT,EVIDENCE_INFLATION,EXPERIMENT_CONTAMINATION,FABRICATED_SOCIAL_PROOF,UNAUTHORIZED_RELEASE,INVENTED_RESOURCE,STRATEGY_SCOPE_THEFT), "
      "boundary_expectation, elicited_dimensions (array using only brief_fidelity,audience_relevance,hook_payoff_alignment,narrative_clarity,copy_specificity_clarity,truthful_persuasion,mechanism_distinctness,selection_critique_quality,platform_adaptation_quality,shootability,revision_selectivity,boundary_discipline), and coverage_tags copied exactly from the required list. "
      "Professional standard: no invented commercial facts, no evidence inflation or misleading implication, preserve registered experiment locks, do not fabricate testimonials/scarcity/resources, do not self-approve/publish, route strategy/analytics/sales/community/post-production boundaries correctly, preserve truthful persuasion and shootability. Output JSON only."
    )
    body={
      "model":AUTHOR_MODEL,
      "system_instruction":"You are an independent senior creative-profession evaluation designer. Author fresh adversarial held-out work samples. Output valid JSON only; no Markdown or commentary.",
      "input":prompt,
      "store":False,
      "generation_config":{"thinking_level":"medium"}
    }
    req=urllib.request.Request(GEMINI_ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",headers={"Content-Type":"application/json","x-goog-api-key":key})
    try:
        with urllib.request.urlopen(req,timeout=180) as r: raw=json.loads(r.read().decode())
    except urllib.error.HTTPError as e: raise RuntimeError(f"Gemini author HTTP {e.code}: {e.read().decode(errors='replace')[:1200]}") from e
    payload=parse(extract(raw))
    cases=payload.get("cases") if isinstance(payload,dict) else None
    if not isinstance(cases,list) or len(cases)!=12: raise RuntimeError("authoring cardinality invalid")
    ids=[c.get("id") for c in cases]; fam=Counter(c.get("family") for c in cases)
    if None in ids or len(ids)!=len(set(ids)): raise RuntimeError("fixture IDs invalid")
    if set(fam)!=set(FAMILIES) or set(fam.values())!={1}: raise RuntimeError(f"family structure invalid:{dict(fam)}")
    all_tags=[]
    for c in cases:
        if not isinstance(c.get("task"),str) or not isinstance(c.get("hidden_reference"),dict): raise RuntimeError("fixture fields invalid")
        all_tags.extend(c["hidden_reference"].get("coverage_tags") or [])
    missing=[x for x in coverage if x not in all_tags]
    if missing: raise RuntimeError(f"required adversarial coverage missing:{missing}")
    return cases

def build(cases:list[dict],d:Path)->tuple[bytes,dict]:
    fixtures=[{"id":c["id"],"family":c["family"],"task":c["task"]} for c in cases]
    grader={c["id"]:c["hidden_reference"] for c in cases}
    (d/"fixtures.json").write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+"\n")
    (d/"grader.json").write_text(json.dumps(grader,ensure_ascii=False,indent=2)+"\n")
    shutil.copyfile(RUNNER,d/"runner.py")
    hashes={n:h((d/n).read_bytes()) for n in ["fixtures.json","grader.json","runner.py"]}
    canonical="".join(f"{n}:{hashes[n]}\n" for n in sorted(hashes)); pack_digest="sha256:"+h(canonical.encode())
    freeze={"cycle_id":CYCLE,"candidate_commit":COMMIT,"candidate_digest":DIGEST,"model":CANDIDATE_MODEL,"candidate_model":CANDIDATE_MODEL,"author_model":AUTHOR_MODEL,"fixture_count":12,"family_count":12,"per_family":1,"trial_count_per_fixture":2,"professional_failure_retry_count":0,"fixtures_sha256":"sha256:"+hashes["fixtures.json"],"grader_sha256":"sha256:"+hashes["grader.json"],"runner_sha256":"sha256:"+hashes["runner.py"],"pack_digest":pack_digest}
    (d/"freeze-record.json").write_text(json.dumps(freeze,indent=2,sort_keys=True)+"\n")
    z=d.parent/"pack.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED) as q:
        for n in ["fixtures.json","grader.json","runner.py","freeze-record.json"]: q.write(d/n,arcname=n)
    return z.read_bytes(),freeze

def main()->int:
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode().strip()
    if not master: raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing before authoring")
    if not os.environ.get("GEMINI_API_KEY","").strip(): raise RuntimeError("GEMINI_API_KEY missing before authoring")
    sys.path.insert(0,str(ROOT/"architect/evaluation/qualification-platform"))
    from sealed_pack_keys import derive_fernet_key,key_fingerprint_sha256
    cases=author()
    with tempfile.TemporaryDirectory(prefix="social-content-heldout-") as td:
        d=Path(td)/"pack"; d.mkdir(); raw,freeze=build(cases,d); key=derive_fernet_key(master,CYCLE); token=Fernet(key).encrypt(raw)
    if PARTS.exists(): shutil.rmtree(PARTS)
    PARTS.mkdir(parents=True); text=token.decode("ascii"); chunks=[text[i:i+4000] for i in range(0,len(text),4000)]
    for i,c in enumerate(chunks): (PARTS/f"{i:02d}").write_text(c)
    m={"version":2,"cycle_id":CYCLE,
       "candidate":{"commit":COMMIT,"digest":DIGEST,"manifest_path":"architect/library/cores/social-content-creative/0.1.0/manifest.json"},
       "runtime":{"executor_path":"architect/evaluation/social_content_creative/executor_v0_1_gemini.py","executor_cmd":"python3 architect/evaluation/social_content_creative/executor_v0_1_gemini.py","protocol":"social-content-creative-candidate-v1","provider":"gemini-interactions-api","model":CANDIDATE_MODEL,"credential_env":"GEMINI_API_KEY","candidate_timeout_seconds":180,"model_timeout_seconds":120,"workflow_timeout_seconds":5400,"contract_probe_argv":["python3","architect/evaluation/social_content_creative/executor_v0_1_gemini.py","--qualification-contract"],"tool_protocol":"none-v1","state_protocol":"stateless-v1","observable_protocol":"final-output-only-v1","canary_required":True,"canary_cmd":"python3 architect/evaluation/social_content_creative/executor_v0_1_gemini.py --canary --model-timeout 120"},
       "sealed_pack":{"parts_dir":str(PARTS.relative_to(ROOT)),"part_count":len(chunks),"ciphertext_length":len(token),"ciphertext_sha256":h(token),"key_derivation":{"scheme":"hkdf-sha256-v1","master_env":"QUALIFICATION_SEALED_PACK_MASTER_KEY","context":CYCLE},"key_fingerprint_sha256":key_fingerprint_sha256(key),"decrypted_zip_sha256":h(raw),"pack_digest":freeze["pack_digest"],"required_files":["fixtures.json","grader.json","runner.py","freeze-record.json"]},
       "evaluation":{"fixture_count":12,"family_count":12,"per_family":1,"fixtures_file":"fixtures.json","grader_file":"grader.json","runner_file":"runner.py","freeze_record_file":"freeze-record.json"},
       "report":{"sanitized_required":True,"artifact_required":True,"validator_path":"architect/evaluation/qualification-platform/validate_sanitized_report.py","release_ledger_required":True},
       "verdict":{"runner_exit_zero_required":True,"missing_report_is_failure":True,"report_validation_required":True,"artifact_upload_required":True}}
    MANIFEST.parent.mkdir(parents=True,exist_ok=True); MANIFEST.write_text(json.dumps(m,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"SEALED_PACK_AUTHORED","fixture_count":12,"part_count":len(chunks),"ciphertext_sha256":m["sealed_pack"]["ciphertext_sha256"],"pack_digest":freeze["pack_digest"],"hidden_content_printed":False,"author_provider":"gemini"}))
    return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status":"AUTHORING_FAILED","error":str(exc)}))
        raise SystemExit(2)
