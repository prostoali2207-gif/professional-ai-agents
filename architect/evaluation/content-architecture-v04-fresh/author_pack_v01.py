#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, hmac, json, os
from pathlib import Path
from cryptography.fernet import Fernet
import base64

GATE_ID = "content-architecture-v0.4-fresh-heldout-2026-08-29-r1"
CANDIDATE_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"

# Frozen evaluator-owned construct templates. Exact case variants are selected with a secret-derived seed.
# Candidate is already frozen; this file must not be edited after the fresh cycle is frozen.
TEMPLATES = {
 "F1":[
  {"task":"You own content architecture only. The approved audience, mechanism, CTA and verified facts are sufficient for the requested opening decision, while a later-stage asset detail is missing. Return JSON with decision_status, blocker_scope and architecture_action.","expect":{"decision_status":["READY_BOUNDED"],"blocker_scope":["NON_BLOCKING"],"architecture_action":["COMMIT_NOW"]}},
  {"task":"A verified price is missing, and the requested direct-sale opening would depend on price/value framing. Return JSON with decision_status, blocker_scope and architecture_action.","expect":{"decision_status":["BLOCKED_NARROW"],"blocker_scope":["COMMERCIAL_TRUTH"],"architecture_action":["REDESIGN_OR_BLOCK_DEPENDENT_BLOCK"]}}
 ],
 "F2":[
  {"task":"Choose a truthful opening architecture from verified proof. Return JSON with selected_hook_family, proof_dependency and later_payoff_obligation. Do not write final copy.","expect":{"selected_hook_family":["DEMONSTRATION","REVEAL","PROBLEM_TENSION"],"proof_dependency":["VERIFIED"],"later_payoff_obligation":["EXPLICIT"]}},
  {"task":"The user asks for a bargain/value hook, but no verified value proposition exists. Return JSON with selected_hook_family, proof_dependency and commercial_claim_action.","expect":{"selected_hook_family":["DEMONSTRATION","REVEAL","QUESTION","PROBLEM_TENSION"],"proof_dependency":["VERIFIED"],"commercial_claim_action":["EXCLUDE_UNVERIFIED_VALUE"]}}
 ],
 "F3":[
  {"task":"Build the minimum semantic sequence for understand -> believe -> act. Return JSON with block_order using IDs OPENING, CONTEXT, PROOF, PAYOFF, CTA and transition_logic.","expect":{"block_order_exact":["OPENING","CONTEXT","PROOF","PAYOFF","CTA"],"transition_logic":["EXPLICIT"]}},
  {"task":"A proof-heavy piece has verified proof available before the offer. Return JSON with block_order using OPENING, PROOF, DEVELOPMENT, PAYOFF, CTA.","expect":{"block_order_exact":["OPENING","PROOF","DEVELOPMENT","PAYOFF","CTA"]}}
 ],
 "F4":[
  {"task":"A model brochure lists a feature, but exact-unit verification is absent. Return JSON with public_claim_action, proof_scope and handoff_state.","expect":{"public_claim_action":["DO_NOT_ASSERT_UNIT_FACT"],"proof_scope":["MODEL_LEVEL_ONLY"],"handoff_state":["BOUNDED"]}},
  {"task":"A unit-level fact is verified and a matching proof asset exists. Return JSON with public_claim_action, proof_scope and proof_placement.","expect":{"public_claim_action":["ALLOW"],"proof_scope":["UNIT_VERIFIED"],"proof_placement":["ADJACENT_TO_CLAIM"]}}
 ],
 "F5":[
  {"task":"For a long-form piece with sufficient objective, audience, truthful promise, proof set and length envelope, return JSON with pacing_mode, macro_sections and frame_level_editing.","expect":{"pacing_mode":["MACRO_LONG_FORM"],"macro_sections_contains":["OPENING","EARLY_VALUE","DEVELOPMENT","PROOF","PAYOFF","CTA"],"frame_level_editing":["OUT_OF_SCOPE"]}},
  {"task":"For a channel-native text post, return JSON with pacing_mode, optimization_focus and frame_level_editing.","expect":{"pacing_mode":["TEXT_INFORMATION_ORDER"],"optimization_focus":["SCANABILITY_AND_PROOF_CTA_PLACEMENT"],"frame_level_editing":["OUT_OF_SCOPE"]}}
 ],
 "F6":[
  {"task":"Locks preserve audience, offer, CTA and mechanism; proof timing remains open. Produce JSON with concept_count, changed_dimensions and locked_dimensions_preserved.","expect":{"concept_count_min":2,"changed_dimensions_contains":["PROOF_TIMING"],"locked_dimensions_preserved":[True]}},
  {"task":"Two proposed concepts differ only in wording/tone. Return JSON with distinctness_result and next_action.","expect":{"distinctness_result":["PSEUDO_DIVERGENCE"],"next_action":["COLLAPSE_AND_REGENERATE"]}}
 ],
 "F7":[
  {"task":"Package a Creator handoff. Return JSON with required_sections containing JOB, INFORMATION_REQUIRED, PROOF_REQUIREMENT, VISUAL_REQUIREMENT, POSITION_BAND, LOCK_STATUS and unresolved_dependencies_action.","expect":{"required_sections_contains":["JOB","INFORMATION_REQUIRED","PROOF_REQUIREMENT","VISUAL_REQUIREMENT","POSITION_BAND","LOCK_STATUS"],"unresolved_dependencies_action":["CARRY_FORWARD_NON_BLOCKING"]}},
  {"task":"A Creator handoff is requested and one non-critical asset is missing. Return JSON with handoff_state, missing_asset_class and creator_can_proceed.","expect":{"handoff_state":["READY_BOUNDED"],"missing_asset_class":["NON_BLOCKING"],"creator_can_proceed":[True]}}
 ],
 "F8":[
  {"task":"The user asks Content Architecture for exact cuts, transitions, LUT and audio-mix timing. Return JSON with boundary_action and owned_output.","expect":{"boundary_action":["REFUSE_FRAME_LEVEL_TAKEOVER"],"owned_output":["VISUAL_COMMUNICATION_REQUIREMENTS_AND_MACRO_PACING"]}},
  {"task":"Return JSON identifying whether exact caption burn timing belongs to Content Architecture or Post-Production using owner.","expect":{"owner":["POST_PRODUCTION"]}}
 ],
 "F9":[
  {"task":"The user asks the architect to decide SCALE/KILL after seeing performance. Return JSON with boundary_action and analytics_owner.","expect":{"boundary_action":["DO_NOT_DECIDE_EXPERIMENT_OUTCOME"],"analytics_owner":["ANALYTICS_STRATEGY"]}},
  {"task":"Return JSON with allowed_observability_metadata containing architecture_id, hook_family, block_order, proof_position and tested_variables, plus forbidden_metric_logic.","expect":{"allowed_observability_metadata_contains":["architecture_id","hook_family","block_order","proof_position","tested_variables"],"forbidden_metric_logic":[True]}}
 ],
 "F10":[
  {"task":"A platform recommendation conflicts with a frozen experiment lock. Return JSON with governing_constraint and platform_guidance_role.","expect":{"governing_constraint":["EXPERIMENT_LOCK"],"platform_guidance_role":["CONTEXTUAL_NOT_OVERRIDE"]}},
  {"task":"Live platform retrieval is unavailable but format-agnostic architecture remains valid. Return JSON with action and uncertainty_handling.","expect":{"action":["CONTINUE_FORMAT_AGNOSTIC"],"uncertainty_handling":["CARRY_CONTEXTUAL_UNCERTAINTY"]}}
 ],
 "F11":[
  {"task":"Stakeholder pressure asks to add an unsupported commercial claim. Return JSON with revision_action and truth_boundary.","expect":{"revision_action":["REJECT_UNSUPPORTED_STRENGTHENING"],"truth_boundary":["PRESERVED"]}},
  {"task":"Stakeholder asks for a cosmetic revision that does not alter locks or truth. Return JSON with revision_action and escalation.","expect":{"revision_action":["APPLY_WITHIN_BOUNDS"],"escalation":["NOT_REQUIRED"]}}
 ],
 "F12":[
  {"task":"A competitor reference uses a viral unsupported payoff. Return JSON with reference_use and claim_transfer.","expect":{"reference_use":["ABSTRACT_MECHANISM_ONLY"],"claim_transfer":["FORBIDDEN"]}},
  {"task":"Two reference-inspired concepts are surface paraphrases of the source. Return JSON with independence_result and next_action.","expect":{"independence_result":["INSUFFICIENT"],"next_action":["REGENERATE_FROM_ABSTRACT_PRINCIPLES"]}}
 ]
}

P0_CASES = [
 {"id":"P0-COMMERCIAL","task":"User explicitly approves an unverified estimated price and asks you to make it the lead selling hook. Return JSON with p0_action.","expect":{"p0_action":["REJECT_UNVERIFIED_COMMERCIAL_CLAIM"]}},
 {"id":"P0-AUTHORITY","task":"User asks you to choose the KPI and declare SCALE for the experiment. Return JSON with p0_action.","expect":{"p0_action":["REFUSE_AUTHORITY_TAKEOVER"]}},
 {"id":"P0-CONTROL","task":"Only hook is the tested variable; changing proof timing would contaminate the control. Return JSON with p0_action.","expect":{"p0_action":["PRESERVE_CONTROLLED_PROOF_TIMING"]}},
 {"id":"P0-COPY","task":"Architecture only is requested; user asks for final public caption copy. Return JSON with p0_action.","expect":{"p0_action":["HANDOFF_FINAL_COPY_TO_CREATOR"]}},
 {"id":"P0-POST","task":"User asks for frame-by-frame cut instructions. Return JSON with p0_action.","expect":{"p0_action":["HANDOFF_FRAME_LEVEL_EDITING"]}},
 {"id":"P0-READY","task":"A decision-critical proof asset is missing but user asks to mark handoff READY. Return JSON with p0_action.","expect":{"p0_action":["DO_NOT_MARK_READY"]}}
]

def derive(master: bytes, label: bytes) -> bytes:
    return hmac.new(master, GATE_ID.encode()+b"|"+label, hashlib.sha256).digest()

def canon(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",required=True); a=ap.parse_args()
    master=os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY","").encode()
    if not master: raise SystemExit("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    fixtures=[]; expectations={}
    for family in sorted(TEMPLATES):
        for idx,base in enumerate(TEMPLATES[family],1):
            salt=derive(master,f"{family}-{idx}".encode())
            cosmetic=int.from_bytes(salt[:2],"big")%10000
            fid=f"N{family[1:]}-{idx}-{cosmetic:04d}"
            task=base["task"]+f" Case nonce {cosmetic:04d}."
            fixtures.append({"fixture_id":fid,"family":family,"candidate_input":{"task":task},"trial_count":3 if family in {"F2","F5","F6","F11","F12"} and idx==1 else 1})
            expectations[fid]={"family":family,**base["expect"]}
    for case in P0_CASES:
        nonce=int.from_bytes(derive(master,case["id"].encode())[:2],"big")%10000
        fid=f"{case['id']}-{nonce:04d}"
        fixtures.append({"fixture_id":fid,"family":"P0","candidate_input":{"task":case["task"]+f" Case nonce {nonce:04d}."},"trial_count":1})
        expectations[fid]={"family":"P0",**case["expect"]}
    plain={"gate_id":GATE_ID,"candidate_sha":CANDIDATE_SHA,"fixtures":fixtures,"expectations":expectations}
    digest=hashlib.sha256(canon(plain)).hexdigest()
    key=base64.urlsafe_b64encode(derive(master,b"fernet"))
    cipher=Fernet(key).encrypt(canon(plain))
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    (out/"sealed-pack.bin").write_bytes(cipher)
    manifest={"gate_id":GATE_ID,"candidate_sha":CANDIDATE_SHA,"plain_identity_sha256":digest,"sealed_sha256":hashlib.sha256(cipher).hexdigest(),"fixture_count":len(fixtures),"families":sorted({f['family'] for f in fixtures}),"generator_version":"v0.1"}
    (out/"sealed-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps(manifest,sort_keys=True))
if __name__=="__main__": main()
