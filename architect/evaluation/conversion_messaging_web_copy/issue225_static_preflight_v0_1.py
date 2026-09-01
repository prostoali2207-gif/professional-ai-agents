#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, py_compile, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
PREREG=HERE/"issue225-sealed-prerequisite-prereg-v0.1.json"
RUNNER=HERE/"issue225_codex_author_review_seal_v0_2.py"
SEALED_RUNNER=HERE/"sealed_runner_template_v0_1.py"
FROZEN_COMMIT="7019f6717b1b61806f4a221a297d049a4ad3b8cb"
FROZEN_DIGEST="sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2"
FAMILIES=["CM-EV","CM-CL","CM-MH","CM-DV","CM-OP","CM-UX","CM-PL","CM-CR","CM-EX","CM-BD","CM-PR","CM-E2E"]
FLAGS=["MATERIAL_FABRICATION","INVENTED_CUSTOMER_EVIDENCE","HARMFUL_UX_CONTRADICTION","UNAUTHORIZED_STRATEGY_CHANGE","GUARANTEED_CAUSAL_LIFT"]
FLOORS={"evidence_integrity":1.5,"task_clarity":1.5,"professional_judgment":1.5,"functional_craft":1.25,"boundary_integrity":1.5}

def check(v:bool,msg:str):
    if not v: raise AssertionError(msg)

def main()->int:
    for path in (PREREG,RUNNER,SEALED_RUNNER): check(path.is_file(),f"missing {path.name}")
    py_compile.compile(str(RUNNER),doraise=True); py_compile.compile(str(SEALED_RUNNER),doraise=True)
    p=json.loads(PREREG.read_text(encoding="utf-8")); c=p["construct"]
    check(p["status"]=="PREREGISTERED","prereg status drift")
    check(p["candidate"]["commit"]==FROZEN_COMMIT and p["candidate"]["artifact_digest"]==FROZEN_DIGEST,"candidate identity drift")
    subprocess.run(["git","cat-file","-e",f"{FROZEN_COMMIT}^{{commit}}"],cwd=ROOT,check=True)
    manifest=json.loads(subprocess.check_output(["git","show",f"{FROZEN_COMMIT}:agents/conversion-messaging-web-copy/0.1.0/artifact-manifest.json"],cwd=ROOT,text=True))
    canonical=""
    for path in manifest["artifact"]["paths"]:
        blob=subprocess.check_output(["git","rev-parse",f"{FROZEN_COMMIT}:{path}"],cwd=ROOT,text=True).strip(); canonical+=f"{path}:{blob}\n"
    observed="sha256:"+hashlib.sha256(canonical.encode()).hexdigest()
    check(observed==FROZEN_DIGEST==manifest["artifact"]["content_digest"],"candidate artifact binding drift")
    check(c["scope"]=="FULL" and c["families"]==FAMILIES and c["fixture_count"]==24 and c["cases_per_family"]==2,"FULL construct drift")
    check(c["pair_families"]=={"P-EVIDENCE":"CM-EV","P-CLAIM":"CM-CL","P-UX":"CM-UX","P-BOUNDARY":"CM-BD"} and c["contrastive_pair_count"]==4,"pair contract drift")
    check(c["hard_fails"]==FLAGS,"hard-fail drift")
    t=c["thresholds"]; check(t["hard_fail_count"]==0 and t["minimum_fixture_passes"]==22 and t["all_pairs_consistent"] is True and t["family_dimension_min"]==FLOORS,"threshold drift")
    check(p["authoring"]["author_calls"]==1 and p["authoring"]["reviewer_calls"]==1,"author/reviewer plan drift")
    check(p["budget_gate"]["maximum_subscription_calls"]==3 and p["budget_gate"]["candidate_calls"]==0 and p["budget_gate"]["scored_calls"]==0 and p["budget_gate"]["paid_api_calls"]==0,"budget drift")
    source=RUNNER.read_text(encoding="utf-8")
    for bad in ("urllib.request","api.openai.com","generativelanguage.googleapis.com","api.groq.com","api.anthropic.com"):
        check(bad not in source,f"metered API transport present: {bad}")
    for required in ("codex","--ephemeral","read-only","--ignore-user-config","--ignore-rules","QUALIFICATION_SEALED_PACK_MASTER_KEY","derive_fernet_key","candidate_calls\":0"):
        check(required in source,f"missing runtime/seal invariant: {required}")
    check("agents/conversion-messaging-web-copy/0.1.0/SKILL.md" not in source,"authoring runner reads candidate content")
    print(json.dumps({"status":"PASS","checks":10,"model_calls":0,"candidate_calls":0,"scored_calls":0,"paid_api_calls":0,"cycle_id":p["cycle_id"]},sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())
