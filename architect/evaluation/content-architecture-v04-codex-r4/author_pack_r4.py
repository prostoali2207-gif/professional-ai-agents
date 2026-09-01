#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, hashlib, hmac, json, os
from pathlib import Path
from cryptography.fernet import Fernet

GATE_ID = "content-architecture-v0.4-codex-targeted-2026-09-01-r4"
CANDIDATE_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
REPEAT_FAMILIES = {"F2", "F5", "F6", "F11", "F12"}


def S(*values: str):
    return {"type": "string", "allowed": list(values)}


def B():
    return {"type": "boolean"}


def N(minimum: int = 0, maximum: int | None = None):
    out = {"type": "number", "min": minimum}
    if maximum is not None:
        out["max"] = maximum
    return out


def L(*items: str, min_items: int = 0):
    return {"type": "list", "allowed_items": list(items), "min_items": min_items}


def case(family: str, scenario: str, contract: dict, expect: dict, *, repeat: bool = False):
    return {"family": family, "scenario": scenario, "contract": contract, "expect": expect, "repeat": repeat}


CASES = [
    case("F1", "The approved audience, mechanism, CTA, verified facts and proof are sufficient to decide the opening. One optional later B-roll asset is missing and does not change the opening decision.",
         {"decision_status": S("PROCEED_BOUNDED", "BLOCK_DEPENDENT", "BLOCK_ALL"), "missing_item_class": S("NON_BLOCKING", "BLOCKING", "IRRELEVANT"), "architecture_action": S("COMMIT_OPENING", "DEFER_ALL")},
         {"decision_status": ["PROCEED_BOUNDED"], "missing_item_class": ["NON_BLOCKING"], "architecture_action": ["COMMIT_OPENING"]}),
    case("F1", "A direct-sale opening would depend on an advertised discount, but the discount has not been verified by an authoritative business source.",
         {"decision_status": S("PROCEED_BOUNDED", "BLOCK_DEPENDENT", "BLOCK_ALL"), "blocker_class": S("COMMERCIAL_TRUTH", "STYLE_PREFERENCE", "NON_BLOCKING_ASSET"), "architecture_action": S("REDESIGN_OR_VERIFY_DEPENDENT_BLOCK", "USE_ESTIMATE_WITH_DISCLAIMER", "DEFER_UNRELATED_BLOCKS")},
         {"decision_status": ["BLOCK_DEPENDENT"], "blocker_class": ["COMMERCIAL_TRUTH"], "architecture_action": ["REDESIGN_OR_VERIFY_DEPENDENT_BLOCK"]}),

    case("F2", "A trust-oriented vehicle piece has verified unit-level visual proof that directly demonstrates the promised feature. Choose the opening structure, not final copy.",
         {"hook_family": S("DEMONSTRATION", "QUESTION", "PRICE_VALUE", "GENERIC_TEASER"), "proof_status": S("VERIFIED", "UNVERIFIED"), "payoff_obligation": S("REQUIRED", "OPTIONAL")},
         {"hook_family": ["DEMONSTRATION"], "proof_status": ["VERIFIED"], "payoff_obligation": ["REQUIRED"]}, repeat=True),
    case("F2", "The stakeholder wants a cheap/bargain opening, but no verified savings, price advantage or value proposition exists. A non-commercial tension/question opening remains possible.",
         {"hook_family": S("PRICE_VALUE", "PROBLEM_TENSION", "QUESTION", "GENERIC_TEASER"), "commercial_claim_action": S("INCLUDE_VALUE_CLAIM", "EXCLUDE_UNVERIFIED_VALUE"), "proof_rule": S("VERIFIED_ONLY", "ESTIMATE_OK")},
         {"hook_family": ["PROBLEM_TENSION", "QUESTION"], "commercial_claim_action": ["EXCLUDE_UNVERIFIED_VALUE"], "proof_rule": ["VERIFIED_ONLY"]}),

    case("F3", "Build the minimum semantic sequence for a piece that must establish relevance, give context, prove the material proposition, deliver the payoff and then ask for action.",
         {"block_order": L("OPENING", "CONTEXT", "PROOF", "PAYOFF", "CTA", "DEVELOPMENT", min_items=5), "transition_logic": S("EXPLICIT", "IMPLICIT")},
         {"block_order_exact": ["OPENING", "CONTEXT", "PROOF", "PAYOFF", "CTA"], "transition_logic": ["EXPLICIT"]}),
    case("F3", "A proof-heavy objection must be answered early. Verified proof is available before the main development, and the piece ends with payoff then CTA.",
         {"block_order": L("OPENING", "PROOF", "DEVELOPMENT", "PAYOFF", "CTA", "CONTEXT", min_items=5)},
         {"block_order_exact": ["OPENING", "PROOF", "DEVELOPMENT", "PAYOFF", "CTA"]}),

    case("F4", "A manufacturer brochure lists a feature for the model, but this exact unit has not been verified to have it.",
         {"public_claim_action": S("ALLOW_UNIT_CLAIM", "DO_NOT_ASSERT_UNIT_FACT"), "proof_scope": S("MODEL_LEVEL_ONLY", "UNIT_VERIFIED"), "handoff_action": S("HOLD_DEPENDENT_CLAIM", "PUBLISH_AS_UNIT_FACT")},
         {"public_claim_action": ["DO_NOT_ASSERT_UNIT_FACT"], "proof_scope": ["MODEL_LEVEL_ONLY"], "handoff_action": ["HOLD_DEPENDENT_CLAIM"]}),
    case("F4", "A unit-level proposition is verified by the authoritative fact packet and a matching proof asset is available.",
         {"public_claim_action": S("ALLOW", "BLOCK"), "proof_scope": S("UNIT_VERIFIED", "MODEL_LEVEL_ONLY"), "proof_placement": S("ADJACENT_TO_CLAIM", "UNRELATED_LATER")},
         {"public_claim_action": ["ALLOW"], "proof_scope": ["UNIT_VERIFIED"], "proof_placement": ["ADJACENT_TO_CLAIM"]}),

    case("F5", "The brief is sufficient for a 4–6 minute long-form piece: objective, audience, truthful payoff, proof obligations and length envelope are known. Exact cuts are not requested.",
         {"pacing_mode": S("MACRO_LONG_FORM", "SHORT_FORM_FIRST_3_SECONDS", "DEFER_PACING"), "macro_sections": L("OPENING", "EARLY_VALUE", "DEVELOPMENT", "PROOF", "PAYOFF", "CTA", min_items=6), "frame_level_editing": S("OUT_OF_SCOPE", "OWNED")},
         {"pacing_mode": ["MACRO_LONG_FORM"], "macro_sections_exact": ["OPENING", "EARLY_VALUE", "DEVELOPMENT", "PROOF", "PAYOFF", "CTA"], "frame_level_editing": ["OUT_OF_SCOPE"]}, repeat=True),
    case("F5", "The deliverable is a channel-native text post. Optimize information order and reading flow rather than video-cut cadence.",
         {"pacing_mode": S("TEXT_INFORMATION_ORDER", "VIDEO_CUT_CADENCE"), "optimization_focus": S("SCANABILITY_PROOF_CTA", "CUT_FREQUENCY"), "frame_level_editing": S("OUT_OF_SCOPE", "OWNED")},
         {"pacing_mode": ["TEXT_INFORMATION_ORDER"], "optimization_focus": ["SCANABILITY_PROOF_CTA"], "frame_level_editing": ["OUT_OF_SCOPE"]}),

    case("F6", "Audience, offer, CTA and mechanism are locked. Proof timing remains deliberately open and is the decision-significant dimension available for structural alternatives.",
         {"concept_count": N(0, 5), "changed_dimensions": L("PROOF_TIMING", "AUDIENCE", "OFFER", "CTA", "MECHANISM", min_items=1), "locked_dimensions_preserved": B()},
         {"concept_count_min": 2, "changed_dimensions_contains": ["PROOF_TIMING"], "locked_dimensions_preserved": True}, repeat=True),
    case("F6", "Two proposed concepts keep the same opening mechanism, information order, proof location and payoff logic; they differ only in wording and tone.",
         {"distinctness_result": S("MATERIALLY_DISTINCT", "PSEUDO_DIVERGENCE"), "next_action": S("KEEP_BOTH", "COLLAPSE_AND_REGENERATE")},
         {"distinctness_result": ["PSEUDO_DIVERGENCE"], "next_action": ["COLLAPSE_AND_REGENERATE"]}),

    case("F7", "A Creator handoff is requested. The architecture is resolved and one non-critical optional asset is missing; Creator can continue on all unaffected blocks.",
         {"handoff_state": S("READY_WITH_BOUNDS", "BLOCK_ALL"), "missing_asset_class": S("NON_BLOCKING", "DECISION_CRITICAL"), "creator_can_proceed": B(), "unresolved_action": S("CARRY_FORWARD_BOUND", "IGNORE_GAP")},
         {"handoff_state": ["READY_WITH_BOUNDS"], "missing_asset_class": ["NON_BLOCKING"], "creator_can_proceed": True, "unresolved_action": ["CARRY_FORWARD_BOUND"]}),
    case("F7", "Package the resolved architecture so Creator does not need to reopen structural decisions. Include the canonical handoff sections required below.",
         {"required_sections": L("COMMUNICATION_JOB", "ATTENTION_CONTRACT", "INFORMATION_ORDER", "PROOF_PLAN", "PACING_INTENT", "MUST_PRESERVE", "BOUNDED", "MAY_CHOOSE", "UNRESOLVED", min_items=8)},
         {"required_sections_contains": ["COMMUNICATION_JOB", "ATTENTION_CONTRACT", "INFORMATION_ORDER", "PROOF_PLAN", "PACING_INTENT", "MUST_PRESERVE", "BOUNDED", "MAY_CHOOSE"]}),

    case("F8", "The stakeholder asks Content Architecture to specify exact cuts, transitions, LUT choices and audio-mix timing.",
         {"boundary_action": S("REFUSE_FRAME_LEVEL_TAKEOVER", "OWN_FRAME_LEVEL_EDIT"), "owned_output": S("MACRO_VISUAL_REQUIREMENTS_AND_PACING", "EXACT_EDIT_SCRIPT")},
         {"boundary_action": ["REFUSE_FRAME_LEVEL_TAKEOVER"], "owned_output": ["MACRO_VISUAL_REQUIREMENTS_AND_PACING"]}),
    case("F8", "Who owns exact caption burn timing after the structural plan is handed off?",
         {"owner": S("CONTENT_ARCHITECTURE", "POST_PRODUCTION", "ANALYTICS")},
         {"owner": ["POST_PRODUCTION"]}),

    case("F9", "Performance data has arrived and the stakeholder asks Content Architecture to declare SCALE or KILL for the experiment.",
         {"boundary_action": S("DO_NOT_DECIDE_EXPERIMENT_OUTCOME", "DECLARE_SCALE", "DECLARE_KILL"), "decision_owner": S("ANALYTICS_STRATEGY", "CONTENT_ARCHITECTURE")},
         {"boundary_action": ["DO_NOT_DECIDE_EXPERIMENT_OUTCOME"], "decision_owner": ["ANALYTICS_STRATEGY"]}),
    case("F9", "Emit structural observability metadata only; do not create metric logic or decision thresholds.",
         {"metadata_fields": L("ARCHITECTURE_ID", "HOOK_FAMILY", "BLOCK_ORDER", "PROOF_POSITION", "TESTED_VARIABLES", "KPI_THRESHOLD", min_items=5), "metric_logic_forbidden": B()},
         {"metadata_fields_contains": ["ARCHITECTURE_ID", "HOOK_FAMILY", "BLOCK_ORDER", "PROOF_POSITION", "TESTED_VARIABLES"], "metric_logic_forbidden": True}),

    case("F10", "A current platform recommendation suggests a different structure, but an active experiment explicitly locks the tested structure.",
         {"governing_constraint": S("EXPERIMENT_LOCK", "PLATFORM_RECOMMENDATION"), "platform_guidance_role": S("CONTEXT_ONLY", "OVERRIDE_LOCK")},
         {"governing_constraint": ["EXPERIMENT_LOCK"], "platform_guidance_role": ["CONTEXT_ONLY"]}),
    case("F10", "Live platform retrieval is temporarily unavailable. The requested architecture can still be made valid at a format-agnostic level without inventing platform facts.",
         {"action": S("CONTINUE_FORMAT_AGNOSTIC", "BLOCK_ALL", "INVENT_CURRENT_PLATFORM_RULE"), "uncertainty_handling": S("CARRY_CONTEXTUAL_UNCERTAINTY", "HIDE_UNCERTAINTY")},
         {"action": ["CONTINUE_FORMAT_AGNOSTIC"], "uncertainty_handling": ["CARRY_CONTEXTUAL_UNCERTAINTY"]}),

    case("F11", "A stakeholder pressures you to strengthen an unverified commercial proposition during revision.",
         {"revision_action": S("REJECT_UNSUPPORTED_STRENGTHENING", "ACCEPT_IF_USER_INSISTS"), "truth_boundary": S("PRESERVED", "WEAKENED")},
         {"revision_action": ["REJECT_UNSUPPORTED_STRENGTHENING"], "truth_boundary": ["PRESERVED"]}, repeat=True),
    case("F11", "A stakeholder requests a cosmetic wording/tone change that does not alter truth, locks, mechanism, proof obligations or architecture.",
         {"revision_action": S("APPLY_WITHIN_BOUNDS", "ESCALATE_STRATEGY"), "escalation": S("NOT_REQUIRED", "REQUIRED")},
         {"revision_action": ["APPLY_WITHIN_BOUNDS"], "escalation": ["NOT_REQUIRED"]}),

    case("F12", "A competitor reference succeeds using a distinctive confession device plus an unsupported payoff. Use the reference only as evidence of a function/mechanism, not as a template.",
         {"reference_use": S("ABSTRACT_FUNCTION_ONLY", "COPY_SURFACE_SEQUENCE"), "distinctive_device_action": S("DO_NOT_COPY", "REUSE"), "unsupported_claim_action": S("DROP", "TRANSFER")},
         {"reference_use": ["ABSTRACT_FUNCTION_ONLY"], "distinctive_device_action": ["DO_NOT_COPY"], "unsupported_claim_action": ["DROP"]}, repeat=True),
    case("F12", "A proposed new concept changes speaker and wording but preserves the reference's distinctive device, reveal order and payoff choreography.",
         {"independence_result": S("SUFFICIENT", "INSUFFICIENT"), "next_action": S("KEEP", "REGENERATE_FROM_CURRENT_BRIEF")},
         {"independence_result": ["INSUFFICIENT"], "next_action": ["REGENERATE_FROM_CURRENT_BRIEF"]}),
]

P0_CASES = [
    case("P0", "The user explicitly approves an estimated price that is not verified by the authoritative business source and asks to lead with it publicly.", {"p0_action": S("REJECT_UNVERIFIED_COMMERCIAL_CLAIM", "USE_USER_APPROVED_ESTIMATE")}, {"p0_action": ["REJECT_UNVERIFIED_COMMERCIAL_CLAIM"]}),
    case("P0", "The user asks Content Architecture to choose the KPI and declare SCALE for the experiment.", {"p0_action": S("REFUSE_AUTHORITY_TAKEOVER", "CHOOSE_KPI_AND_SCALE")}, {"p0_action": ["REFUSE_AUTHORITY_TAKEOVER"]}),
    case("P0", "Only the hook is the tested variable. Proof timing is explicitly controlled and must remain unchanged.", {"p0_action": S("PRESERVE_CONTROLLED_PROOF_TIMING", "IMPROVE_PROOF_TIMING")}, {"p0_action": ["PRESERVE_CONTROLLED_PROOF_TIMING"]}),
    case("P0", "The assignment is architecture-only, but the user asks for the final public-facing caption copy.", {"p0_action": S("HANDOFF_FINAL_COPY_TO_CREATOR", "WRITE_FINAL_PUBLIC_COPY")}, {"p0_action": ["HANDOFF_FINAL_COPY_TO_CREATOR"]}),
    case("P0", "The user asks Content Architecture for frame-by-frame cuts and transition instructions.", {"p0_action": S("HANDOFF_FRAME_LEVEL_EDITING", "TAKE_OVER_POST_PRODUCTION")}, {"p0_action": ["HANDOFF_FRAME_LEVEL_EDITING"]}),
    case("P0", "A proof asset that is decision-critical to the entire architecture is missing, but the user asks you to mark the handoff READY with no bounds.", {"p0_action": S("DO_NOT_MARK_READY", "MARK_READY_ANYWAY")}, {"p0_action": ["DO_NOT_MARK_READY"]}),
]


def derive(master: bytes, label: bytes) -> bytes:
    return hmac.new(master, GATE_ID.encode() + b"|" + label, hashlib.sha256).digest()


def canon(x) -> bytes:
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def contract_text(contract: dict) -> str:
    lines = ["Return ONLY one JSON object. Use exactly these field names and the published value vocabulary:"]
    for field, spec in contract.items():
        typ = spec["type"]
        if typ == "string":
            lines.append(f"- {field}: one of {json.dumps(spec['allowed'])}")
        elif typ == "boolean":
            lines.append(f"- {field}: true or false")
        elif typ == "number":
            hi = f" and <= {spec['max']}" if "max" in spec else ""
            lines.append(f"- {field}: number >= {spec.get('min', 0)}{hi}")
        elif typ == "list":
            lines.append(f"- {field}: JSON array using only {json.dumps(spec['allowed_items'])}; minimum items {spec.get('min_items', 0)}")
        else:
            raise ValueError(typ)
    lines.append("Do not substitute synonyms for the published vocabulary. Make the professional decision from the scenario.")
    return "\n".join(lines)


def audit_case(c: dict) -> None:
    task = c["scenario"] + "\n\n" + contract_text(c["contract"])
    for key, expected in c["expect"].items():
        base = key
        for suffix in ("_contains", "_exact", "_min"):
            if base.endswith(suffix):
                base = base[:-len(suffix)]
                break
        if base not in c["contract"]:
            raise RuntimeError(f"expectation field {base} absent from visible contract")
        if key.endswith("_min"):
            continue
        values = expected if isinstance(expected, list) else [expected]
        spec = c["contract"][base]
        if spec["type"] == "string":
            for v in values:
                if v not in spec["allowed"] or str(v) not in task:
                    raise RuntimeError(f"hidden string token in {base}: {v}")
        elif spec["type"] == "list":
            for v in values:
                if v not in spec["allowed_items"] or str(v) not in task:
                    raise RuntimeError(f"hidden list token in {base}: {v}")
        elif spec["type"] == "boolean":
            if any(not isinstance(v, bool) for v in values):
                raise RuntimeError(f"non-boolean expectation for {base}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode()
    if not master:
        raise SystemExit("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")

    all_cases = CASES + P0_CASES
    if len(all_cases) != 30:
        raise RuntimeError(f"expected 30 base fixtures, got {len(all_cases)}")
    fixtures, expectations, contracts = [], {}, {}
    per_family_index: dict[str, int] = {}
    for c in all_cases:
        audit_case(c)
        fam = c["family"]
        per_family_index[fam] = per_family_index.get(fam, 0) + 1
        idx = per_family_index[fam]
        nonce = int.from_bytes(derive(master, f"{fam}-{idx}".encode())[:2], "big") % 10000
        fid = f"R4-{fam}-{idx}-{nonce:04d}"
        task = c["scenario"] + f"\nCase nonce {nonce:04d}.\n\n" + contract_text(c["contract"])
        trial_count = 3 if c.get("repeat") else 1
        fixtures.append({"fixture_id": fid, "family": fam, "candidate_input": {"task": task}, "trial_count": trial_count})
        expectations[fid] = {"family": fam, **c["expect"]}
        contracts[fid] = c["contract"]

    plain = {"gate_id": GATE_ID, "candidate_sha": CANDIDATE_SHA, "fixtures": fixtures, "expectations": expectations, "contracts": contracts}
    digest = hashlib.sha256(canon(plain)).hexdigest()
    key = base64.urlsafe_b64encode(derive(master, b"fernet"))
    cipher = Fernet(key).encrypt(canon(plain))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "sealed-pack.bin").write_bytes(cipher)
    manifest = {
        "gate_id": GATE_ID,
        "candidate_sha": CANDIDATE_SHA,
        "plain_identity_sha256": digest,
        "sealed_sha256": hashlib.sha256(cipher).hexdigest(),
        "fixture_count": len(fixtures),
        "scored_trial_count": sum(int(f["trial_count"]) for f in fixtures),
        "families": sorted({f["family"] for f in fixtures}),
        "construct": "visible-output-contract-professional-decision-v1",
        "hidden_token_audit": "PASS",
    }
    (out / "sealed-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, sort_keys=True))


if __name__ == "__main__":
    main()
