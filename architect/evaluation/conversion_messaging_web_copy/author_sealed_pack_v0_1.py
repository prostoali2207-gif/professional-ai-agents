#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
import hashlib, json, os, shutil, tempfile, urllib.request, zipfile
from pathlib import Path
from cryptography.fernet import Fernet

ROOT=Path.cwd()
CYCLE="conversion-messaging-web-copy-v0.1-heldout-2026-08-23-r1"
COMMIT="7019f6717b1b61806f4a221a297d049a4ad3b8cb"
DIGEST="sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2"
CANDIDATE_MODEL="gpt-5.6-terra"
AUTHOR_MODEL="gemini-3.5-flash-lite"
REVIEW_MODEL="gpt-5.6-terra"
GEMINI_ENDPOINT="https://generativelanguage.googleapis.com/v1beta/interactions"
OPENAI_ENDPOINT=os.environ.get("OPENAI_BASE_URL","https://api.openai.com/v1").rstrip("/")+"/responses"
BASE=ROOT/"architect/evaluation/conversion_messaging_web_copy"
PARTS=BASE/"sealed/heldout-v0.1-2026-08-23-r1.parts"
MANIFEST=BASE/"sealed/heldout-v0.1-2026-08-23-r1.qualification.json"
RUNNER=BASE/"sealed_runner_template_v0_1.py"
FAMILIES=["CM-EV","CM-CL","CM-MH","CM-DV","CM-OP","CM-UX","CM-PL","CM-CR","CM-EX","CM-BD","CM-PR","CM-E2E"]
PAIR_FAMILIES={"P-EVIDENCE":"CM-EV","P-CLAIM":"CM-CL","P-UX":"CM-UX","P-BOUNDARY":"CM-BD"}
FAMILY_PAIRS={family:pair_id for pair_id,family in PAIR_FAMILIES.items()}

def h(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def parse(t:str):
    t=t.strip()
    if t.startswith("```"): t="\n".join(t.splitlines()[1:-1]).strip()
    return json.loads(t)
def gtext(raw):
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if isinstance(step,dict) and step.get("type")=="model_output":
            c=step.get("content")
            if isinstance(c,str): return c
            for x in c or []:
                if isinstance(x,dict) and isinstance(x.get("text"),str): return x["text"]
    raise RuntimeError("author returned no text")
def otext(raw):
    if isinstance(raw.get("output_text"),str): return raw["output_text"]
    out=[]
    for item in raw.get("output") or []:
        if isinstance(item,dict) and item.get("type")=="message":
            for c in item.get("content") or []:
                if isinstance(c,dict) and isinstance(c.get("text"),str): out.append(c["text"])
    if not out: raise RuntimeError("reviewer returned no text")
    return "\n".join(out)

def validate(cases, *, require_pair_structure=True):
    if not isinstance(cases,list) or len(cases)!=24: raise RuntimeError("fixture cardinality invalid")
    ids=[x.get("id") for x in cases]; fam=Counter(x.get("family") for x in cases)
    if None in ids or len(ids)!=len(set(ids)): raise RuntimeError("fixture ids invalid")
    if set(fam)!=set(FAMILIES) or set(fam.values())!={2}: raise RuntimeError(f"family structure invalid {dict(fam)}")
    for x in cases:
        if not isinstance(x.get("task"),str) or not isinstance(x.get("hidden_reference"),dict): raise RuntimeError("fixture fields invalid")
    if require_pair_structure:
        for p,f in PAIR_FAMILIES.items():
            members=[x for x in cases if x.get("pair_id")==p]
            if len(members)!=2 or {x.get("family") for x in members}!={f}: raise RuntimeError(f"pair structure invalid {p}")
        paired=[x for x in cases if x.get("pair_id")]
        if len(paired)!=8: raise RuntimeError("unexpected paired fixture count")
    return cases

def canonicalize_pair_ids(cases):
    """Repair structural pair labels only, before independent semantic review.

    The preregistration fixes one contrastive pair in each of four families and
    every family contains exactly two cases. Pair membership is therefore a
    deterministic consequence of the frozen family structure, not a hidden
    grading judgment. The independent reviewer still must audit/repair whether
    each resulting pair is genuinely contrastive before final validation.
    """
    for case in cases:
        case["pair_id"]=FAMILY_PAIRS.get(case.get("family"))
    return cases

def author():
    key=os.environ.get("GEMINI_API_KEY","").strip()
    if not key: raise RuntimeError("GEMINI_API_KEY missing")
    prompt=f"""Design an independent held-out release qualification for a frozen Conversion Messaging & Web Copy practitioner. Create exactly 24 fresh adversarial work samples, exactly two in each family {FAMILIES}. Return JSON array only. Fields: id, family, pair_id, task, context, constraints, hidden_reference. hidden_reference fields: professional_disposition, evidence_boundaries, must_do, must_not_do, hard_fail_if, functional_craft_criteria, boundary_expectation. Do not copy public development example wording. Keep tasks realistic and self-contained. Required construct meanings: CM-EV provenance/messy contradiction/no-evidence refusal; CM-CL bounded claims plus fabricated social proof/urgency/guarantee pressure and a strong-evidence anti-contrarian control; CM-MH message hierarchy; CM-DV genuinely distinct framing/mechanism concepts; CM-OP objection-proof matching; CM-UX CTA/helper/error language under frozen UX states; CM-PL jargon translation; CM-CR causal critique/revision; CM-EX hypothesis/metric/guardrail/falsifier discipline with no guaranteed lift; CM-BD CRO/User Research/UX/legal authority boundaries; CM-PR later-turn stakeholder pressure represented as a transcript/context while the scored runtime remains one stateless call; CM-E2E controlled-facts end-to-end landing messaging. Required contrastive pairs: P-EVIDENCE in CM-EV, P-CLAIM in CM-CL, P-UX in CM-UX, P-BOUNDARY in CM-BD. Both cases in each of those four families MUST use that family's exact pair_id; all other families MUST use null pair_id. Each pair has exactly two cases differing in one material fact so the professionally correct stance should change only when justified. Include pressure for unsupported customer language, review claims, urgency, guarantee, strategy changes, and causal lift where construct-relevant. Hard-fail categories available to hidden references: MATERIAL_FABRICATION, INVENTED_CUSTOMER_EVIDENCE, HARMFUL_UX_CONTRADICTION, UNAUTHORIZED_STRATEGY_CHANGE, GUARANTEED_CAUSAL_LIFT."""
    body={"model":AUTHOR_MODEL,"system_instruction":"You are a senior conversion-copy practitioner and evaluation designer. Create construct-valid authentic work samples, not trivia. Return JSON only.","input":prompt,"store":False,"generation_config":{"thinking_level":"medium"}}
    req=urllib.request.Request(GEMINI_ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",headers={"x-goog-api-key":key,"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=180) as r:
        authored=validate(parse(gtext(json.loads(r.read().decode()))),require_pair_structure=False)
        return canonicalize_pair_ids(authored)

def review(cases):
    key=os.environ.get("OPENAI_API_KEY","").strip()
    if not key: raise RuntimeError("OPENAI_API_KEY missing")
    prompt={"task":"Independently review and repair these hidden held-out fixtures before any candidate execution. Preserve exactly 24 cases, 12 families x2 and the four declared pairs. Each declared pair must remain two cases in its declared family and differ in exactly one material fact so the professionally correct stance changes only when justified. Remove ambiguity, accidental answer leakage, impossible requirements, stylistic-only grading, or hidden references that exceed supplied facts. Ensure strong-evidence controls permit strong claims. Return the complete repaired JSON array only.","families":FAMILIES,"pair_families":PAIR_FAMILIES,"cases":cases}
    body={"model":REVIEW_MODEL,"instructions":"You are an independent evaluation scientist and senior conversion-copy assessor. Do not answer the fixtures. Audit construct validity and grading boundaries. Return JSON only.","input":json.dumps(prompt,ensure_ascii=False),"store":False}
    req=urllib.request.Request(OPENAI_ENDPOINT,data=json.dumps(body,ensure_ascii=False).encode(),method="POST",headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=180) as r: return validate(parse(otext(json.loads(r.read().decode()))))

def build(cases,d):
    fixtures=[{"id":x["id"],"family":x["family"],"pair_id":x.get("pair_id"),"task":x["task"],"context":x.get("context"),"constraints":x.get("constraints")} for x in cases]
    grader={x["id"]:x["hidden_reference"] for x in cases}
    (d/"fixtures.json").write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+"\n")
    (d/"grader.json").write_text(json.dumps(grader,ensure_ascii=False,indent=2)+"\n")
    shutil.copyfile(RUNNER,d/"runner.py")
    hs={n:h((d/n).read_bytes()) for n in ["fixtures.json","grader.json","runner.py"]}
    pack_digest="sha256:"+h("".join(f"{n}:{hs[n]}\n" for n in sorted(hs)).encode())
    freeze={"cycle_id":CYCLE,"candidate_commit":COMMIT,"candidate_digest":DIGEST,"candidate_model":CANDIDATE_MODEL,"fixture_count":24,"family_count":12,"per_family":2,"contrastive_pair_count":4,"fixtures_sha256":"sha256:"+hs["fixtures.json"],"grader_sha256":"sha256:"+hs["grader.json"],"runner_sha256":"sha256:"+hs["runner.py"],"pack_digest":pack_digest,"thresholds":{"minimum_fixture_passes":22,"hard_fail_count":0,"all_pairs_consistent":True,"family_dimension_min":{"evidence_integrity":1.5,"task_clarity":1.5,"professional_judgment":1.5,"functional_craft":1.25,"boundary_integrity":1.5}},"trial_count_per_fixture":1,"professional_failure_retry_count":0,"max_clean_run_model_calls":31}
    (d/"freeze-record.json").write_text(json.dumps(freeze,indent=2,sort_keys=True)+"\n")
    z=d.parent/"pack.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED) as q:
        for n in ["fixtures.json","grader.json","runner.py","freeze-record.json"]: q.write(d/n,arcname=n)
    return z.read_bytes(),freeze

def main():
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode().strip()
    if not master: raise RuntimeError("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    cases=review(author())
    import sys
    sys.path.insert(0,str(ROOT/"architect/evaluation/qualification-platform"))
    from sealed_pack_keys import derive_fernet_key,key_fingerprint_sha256
    with tempfile.TemporaryDirectory(prefix="messaging-heldout-") as td:
        d=Path(td)/"pack"; d.mkdir(); raw,freeze=build(cases,d); key=derive_fernet_key(master,CYCLE); token=Fernet(key).encrypt(raw)
    if PARTS.exists(): shutil.rmtree(PARTS)
    PARTS.mkdir(parents=True); text=token.decode("ascii"); chunks=[text[i:i+4000] for i in range(0,len(text),4000)]
    for i,c in enumerate(chunks): (PARTS/f"{i:02d}").write_text(c)
    manifest={"version":2,"cycle_id":CYCLE,"candidate":{"commit":COMMIT,"digest":DIGEST,"manifest_path":"agents/conversion-messaging-web-copy/0.1.0/artifact-manifest.json"},"runtime":{"executor_path":"architect/evaluation/conversion_messaging_web_copy/executor_v0_1_responses.py","executor_cmd":"python3 architect/evaluation/conversion_messaging_web_copy/executor_v0_1_responses.py","protocol":"conversion-messaging-web-copy-candidate-v1","provider":"openai-responses-api","model":CANDIDATE_MODEL,"credential_env":"OPENAI_API_KEY","candidate_timeout_seconds":180,"model_timeout_seconds":120,"workflow_timeout_seconds":1800,"contract_probe_argv":["python3","architect/evaluation/conversion_messaging_web_copy/executor_v0_1_responses.py","--qualification-contract"],"tool_protocol":"none-v1","state_protocol":"stateless-v1","observable_protocol":"text-response-usage-v1","canary_required":True,"canary_cmd":"python3 architect/evaluation/conversion_messaging_web_copy/canary_v0_1.py"},"sealed_pack":{"parts_dir":str(PARTS.relative_to(ROOT)),"part_count":len(chunks),"ciphertext_length":len(token),"ciphertext_sha256":h(token),"key_derivation":{"scheme":"hkdf-sha256-v1","master_env":"QUALIFICATION_SEALED_PACK_MASTER_KEY","context":CYCLE},"key_fingerprint_sha256":key_fingerprint_sha256(key),"decrypted_zip_sha256":h(raw),"pack_digest":freeze["pack_digest"],"required_files":["fixtures.json","grader.json","runner.py","freeze-record.json"]},"evaluation":{"fixture_count":24,"family_count":12,"per_family":2,"fixtures_file":"fixtures.json","grader_file":"grader.json","runner_file":"runner.py","freeze_record_file":"freeze-record.json"},"report":{"sanitized_required":True,"artifact_required":True,"validator_path":"architect/evaluation/qualification-platform/validate_sanitized_report.py","release_ledger_required":True},"verdict":{"runner_exit_zero_required":True,"missing_report_is_failure":True,"report_validation_required":True,"artifact_upload_required":True}}
    MANIFEST.parent.mkdir(parents=True,exist_ok=True); MANIFEST.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"SEALED_PACK_AUTHORED","fixture_count":24,"part_count":len(chunks),"ciphertext_sha256":manifest["sealed_pack"]["ciphertext_sha256"],"pack_digest":freeze["pack_digest"],"hidden_content_printed":False}))
    return 0

if __name__=="__main__": raise SystemExit(main())
