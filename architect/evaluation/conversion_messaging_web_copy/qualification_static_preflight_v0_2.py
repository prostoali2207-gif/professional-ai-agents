#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"architect/evaluation/conversion_messaging_web_copy"
PREREG=BASE/"qualification-preregistration-v0.2.json"
CANDIDATE=BASE/"codex_candidate_adapter_v0_2.py"
JUDGE=BASE/"codex_judge_adapter_v0_2.py"
SKILL=ROOT/"agents/conversion-messaging-web-copy/0.2.0/SKILL.md"
MANIFEST=ROOT/"agents/conversion-messaging-web-copy/0.2.0/artifact-manifest.json"
EXPECTED_DIGEST="sha256:627b7ee68bd4bb77e70abc8018856dc91f36f29a0eb187185992341a103d2173"
EXPECTED_COMMIT="22ee4c3e8b9d3d850d037d95bd83f2b3669a7896"
FAMILIES=["CM-EV","CM-CL","CM-MH","CM-DV","CM-OP","CM-UX","CM-PL","CM-CR","CM-EX","CM-BD","CM-PR","CM-E2E","CM-MM","CM-A11Y","CM-L10N"]
PAIRS={"P-EVIDENCE":"CM-EV","P-CLAIM":"CM-CL","P-UX":"CM-UX","P-BOUNDARY":"CM-BD","P-MESSAGE-MATCH":"CM-MM","P-A11Y":"CM-A11Y","P-L10N":"CM-L10N"}
DIMS=["evidence_integrity","task_clarity","professional_judgment","functional_craft","boundary_integrity"]
FLAGS=["MATERIAL_FABRICATION","INVENTED_CUSTOMER_EVIDENCE","HARMFUL_UX_CONTRADICTION","UNAUTHORIZED_STRATEGY_CHANGE","GUARANTEED_CAUSAL_LIFT","UNSUPPORTED_ACQUISITION_CLAIM","FALSE_ACCESSIBILITY_CONFORMANCE","LOCALIZATION_EVIDENCE_STRENGTHENING","UNVERIFIED_LOCAL_AUTHORITY_CLAIM"]
PAID_KEYS=["OPENAI_API_KEY","ANTHROPIC_API_KEY","GEMINI_API_KEY","GROQ_API_KEY","XAI_API_KEY"]

def fail(msg:str)->None: raise SystemExit(msg)

def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: fail(f"cannot import {path.name}")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

for path in (PREREG,CANDIDATE,JUDGE,SKILL,MANIFEST):
    if not path.is_file(): fail(f"missing required file: {path.relative_to(ROOT)}")

p=json.loads(PREREG.read_text(encoding="utf-8")); manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
if p.get("status")!="PREREGISTERED_ZERO_MODEL_ONLY": fail("prereg status mismatch")
if p.get("scope")!="FULL": fail("v0.2 release scope must be FULL")
if p["candidate"].get("freeze_commit")!=EXPECTED_COMMIT or p["candidate"].get("artifact_digest")!=EXPECTED_DIGEST: fail("candidate freeze binding mismatch")
raw=SKILL.read_bytes(); observed="sha256:"+hashlib.sha256(raw).hexdigest()
if observed!=EXPECTED_DIGEST or len(raw)!=15859: fail("candidate bytes/digest mismatch")
if manifest.get("artifact",{}).get("content_digest")!=EXPECTED_DIGEST: fail("artifact manifest digest mismatch")
if manifest.get("candidate",{}).get("qualification_status")!="UNQUALIFIED_CANDIDATE": fail("candidate must remain unqualified before scored release evidence")

c=p["construct"]
if c.get("families")!=FAMILIES or c.get("fixture_count")!=30 or c.get("per_family")!=2: fail("family/cardinality drift")
if c.get("contrastive_pairs")!=PAIRS: fail("contrastive pair drift")
if c.get("dimensions")!=DIMS or c.get("hard_fails")!=FLAGS: fail("grader construct drift")
t=c["thresholds"]
if t.get("fixture_passes_min")!=28 or t.get("fixture_count")!=30 or not t.get("zero_hard_fails") or not t.get("all_pairs_consistent_both_judges"): fail("release threshold drift")
if t.get("family_means_min")!={"evidence_integrity":1.5,"task_clarity":1.5,"professional_judgment":1.5,"functional_craft":1.25,"boundary_integrity":1.5}: fail("family floor drift")

if p["evaluation_design"].get("hidden_transport")!="ephemeral-evaluator-memory-v1" or p["evaluation_design"].get("sealed_pack_required") is not False: fail("hidden transport contract mismatch")
if p["evaluation_design"].get("candidate_visible_fields")!=["task","context","constraints"]: fail("candidate visible-field boundary drift")
if p["routing"].get("provider")!="codex-subscription-chatgpt-auth" or p["routing"].get("paid_api_fallback")!="FORBIDDEN": fail("routing drift")
if p["budget"].get("clean_subscription_calls")!=37 or p["budget"].get("scored_candidate")!=30 or p["budget"].get("paid_api_calls")!=0: fail("budget arithmetic drift")
if sum(p["budget"][k] for k in ("author","reviewer","judge_calibration","candidate_canary","scored_candidate","hidden_judge_batches"))!=37: fail("clean-call budget does not add to 37")

for key in PAID_KEYS:
    if os.environ.get(key): fail(f"paid API credential present in zero-model gate: {key}")
text=(CANDIDATE.read_text(encoding="utf-8")+JUDGE.read_text(encoding="utf-8")).lower()
for token in ("api.openai.com","generativelanguage.googleapis.com","api.groq.com","anthropic.com/v1"):
    if token in text: fail(f"metered API transport token found: {token}")

candidate_contract=json.loads(subprocess.check_output([sys.executable,str(CANDIDATE),"--qualification-contract"],text=True,cwd=ROOT))
if candidate_contract.get("candidate_commit")!=EXPECTED_COMMIT or candidate_contract.get("candidate_digest")!=EXPECTED_DIGEST or candidate_contract.get("visible_fields")!=["task","context","constraints"]: fail("candidate adapter contract mismatch")
judge=load_module(JUDGE,"messaging_v02_judge")
cal=judge.schema("calibration"); held=judge.schema("heldout")
if "pair_results" in cal.get("properties",{}) or "pair_results" in cal.get("required",[]): fail("calibration schema incorrectly requires pair_results")
if "pair_results" not in held.get("properties",{}) or "pair_results" not in held.get("required",[]): fail("heldout schema missing pair_results")
if judge.DIMS!=DIMS or judge.FLAGS!=FLAGS: fail("judge adapter enum drift")

print(json.dumps({"status":"PASS","checks":25,"cycle_id":p["cycle_id"],"scope":"FULL","families":15,"fixtures":30,"pairs":7,"fixture_passes_min":28,"hidden_transport":"ephemeral-evaluator-memory-v1","model_calls":0,"candidate_calls":0,"scored_calls":0,"paid_api_calls":0},sort_keys=True))
