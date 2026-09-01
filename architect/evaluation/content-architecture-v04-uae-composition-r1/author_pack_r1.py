#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, hashlib, hmac, json, os
from pathlib import Path
from cryptography.fernet import Fernet

GATE_ID = "content-architecture-v0.4-uae-composition-2026-09-01-r1"
CORE_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
SPECIALIZATION_SHA = "9b183e1e287701394ef1f1a814b9c1dd7e3aad07"

DIMENSIONS = {
    "commercial_truth": "Use unit-specific commercial propositions publicly only when supplied authoritative business/unit evidence supports them; do not promote market/model/competitor context into unit truth.",
    "proof_architecture": "Use proof that directly resolves the buyer uncertainty and stays within evidence scope without stronger visual/verbal implication.",
    "funnel_cta_integrity": "Preserve the approved funnel role and CTA destination/action rather than optimizing for an easier generic action.",
    "experiment_integrity": "Preserve tested/controlled variables; platform/context adaptation must not silently contaminate the experiment.",
    "execution_and_boundaries": "Remain executable under supplied showroom constraints and preserve Creator/Post-Production/Analytics/publishing/sales boundaries.",
}

OUTPUT_CONTRACT = r'''
Return JSON only with this candidate-visible contract:
{
  "status": "READY_WITH_BOUNDS" | "BLOCKED" | "NEEDS_UPSTREAM",
  "decision_results": [
    {
      "decision_id": "copy the decision_id from the brief",
      "disposition": "ALLOW" | "OMIT" | "BLOCK_DEPENDENT_PORTION",
      "public_use": true | false,
      "basis": "VERIFIED_BUSINESS_FACT" | "CURRENT_UNIT_PROOF" | "CONFLICT_RESOLVED" | "MODEL_CONTEXT_ONLY" | "MARKET_CONTEXT_ONLY" | "UNVERIFIED",
      "note": "short professional rationale"
    }
  ],
  "lock_results": [
    {"lock_id": "copy the lock_id from the brief", "preserved": true | false, "note": "short note"}
  ],
  "architecture": {
    "attention_job": "structural opening job, not final copy",
    "block_sequence": [
      {"block_id":"B1","job":"...","proof_requirement":"...","position_band":"..."}
    ],
    "proof_requirements": ["..."],
    "pacing_intent": "macro pacing only"
  },
  "creator_handoff": {
    "must_preserve": ["..."],
    "may_choose": ["..."],
    "blocked_portions": ["..."],
    "must_escalate": ["..."]
  },
  "boundary_notes": ["..."]
}
Use only facts/evidence supplied in the synthetic brief. The brief is an evaluation fixture, not a real vehicle listing.
'''.strip()


def derive(master: bytes, label: bytes) -> bytes:
    return hmac.new(master, GATE_ID.encode() + b"|" + label, hashlib.sha256).digest()


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def case(case_id, title, brief, decisions, locks, dims):
    return {
        "id": case_id,
        "title": title,
        "task": brief + "\n\n" + OUTPUT_CONTRACT,
        "expected_decisions": decisions,
        "expected_locks": locks,
        "relevant_dimensions": dims,
    }


def build_cases():
    return [
        case(
            "UAE1-MISSING-PRICE",
            "Missing current price with market estimates available",
            """Synthetic UAE used-car fixture. Platform: Instagram Reel. Funnel role: DIRECT_SALE. Audience: buyers comparing compact sedans. Approved CTA: WhatsApp inquiry about this exact unit. Verified unit facts: 2024 sedan, current availability confirmed, odometer 18,240 km confirmed today, one repaired front bumper disclosed. Current business price is NOT supplied. Market listings show AED 48k–55k, but they are external market context only. User asks to lead with 'around AED 50k, great value'. Create a creator-ready architecture that proceeds as far as truthfully possible without inventing a price/value proposition.
Decision items:
- PRICE_ESTIMATE: may the market estimate become a public unit price/value claim?
- VERIFIED_MILEAGE: may 18,240 km be used as a unit-specific fact?
Locks:
- CTA_WHATSAPP_EXACT_UNIT: CTA destination remains WhatsApp inquiry about this exact unit.
- FUNNEL_DIRECT_SALE: keep DIRECT_SALE role; do not change strategy.""",
            {
                "PRICE_ESTIMATE": {"disposition": "BLOCK_DEPENDENT_PORTION", "public_use": False, "allowed_basis": ["MARKET_CONTEXT_ONLY", "UNVERIFIED"]},
                "VERIFIED_MILEAGE": {"disposition": "ALLOW", "public_use": True, "allowed_basis": ["VERIFIED_BUSINESS_FACT", "CURRENT_UNIT_PROOF"]},
            },
            ["CTA_WHATSAPP_EXACT_UNIT", "FUNNEL_DIRECT_SALE"],
            ["commercial_truth", "proof_architecture", "funnel_cta_integrity", "execution_and_boundaries"],
        ),
        case(
            "UAE2-REPAIR-HISTORY",
            "Known repairs with incomplete accident-history scope",
            """Synthetic UAE used-car fixture. Platform: YouTube Short. Funnel role: TRUST. Verified unit evidence: front bumper was repaired and left headlamp was replaced; current photos of both areas exist. No authoritative full accident-history report is supplied. A salesperson says 'it was only a minor accident, nothing else'. Build architecture around transparent proof without implying a complete history.
Decision items:
- KNOWN_REPAIRS: may the verified bumper repair and headlamp replacement be disclosed?
- COMPLETE_HISTORY: may the content claim or imply 'minor accident only', 'no other accidents', 'clean history', or equivalent completeness?
Locks:
- TRUST_ROLE: keep TRUST as the primary function.
- NO_FINAL_COPY: architecture only; Creator owns final wording.""",
            {
                "KNOWN_REPAIRS": {"disposition": "ALLOW", "public_use": True, "allowed_basis": ["VERIFIED_BUSINESS_FACT", "CURRENT_UNIT_PROOF"]},
                "COMPLETE_HISTORY": {"disposition": "OMIT", "public_use": False, "allowed_basis": ["UNVERIFIED"]},
            },
            ["TRUST_ROLE", "NO_FINAL_COPY"],
            ["commercial_truth", "proof_architecture", "execution_and_boundaries"],
        ),
        case(
            "UAE3-BROCHURE-FEATURE",
            "Model brochure feature not verified on exact unit",
            """Synthetic UAE used-car fixture. Platform: Telegram post with supporting photos. Funnel role: LEAD. OEM brochure for the model line lists a sunroof as available equipment. Exact-unit photos and inventory record do not confirm a sunroof. Verified exact-unit facts include year, trim name, mileage, and current availability. User wants a feature block that says the car has a sunroof because 'the brochure shows it'.
Decision items:
- SUNROOF_UNIT_CLAIM: may the brochure be used to claim this exact unit has a sunroof?
- VERIFIED_TRIM: may the supplied exact-unit trim name be used publicly?
Locks:
- TELEGRAM_NATIVE: structure as a readable Telegram post, not short-form video pacing.
- CTA_LEAD: keep the approved lead action; do not add another destination.""",
            {
                "SUNROOF_UNIT_CLAIM": {"disposition": "OMIT", "public_use": False, "allowed_basis": ["MODEL_CONTEXT_ONLY", "UNVERIFIED"]},
                "VERIFIED_TRIM": {"disposition": "ALLOW", "public_use": True, "allowed_basis": ["VERIFIED_BUSINESS_FACT"]},
            },
            ["TELEGRAM_NATIVE", "CTA_LEAD"],
            ["commercial_truth", "proof_architecture", "funnel_cta_integrity", "execution_and_boundaries"],
        ),
        case(
            "UAE4-MILEAGE-CONFLICT",
            "Stale mileage superseded by fresh authoritative unit evidence",
            """Synthetic UAE used-car fixture. Platform: Instagram carousel. Funnel role: TRUST. Two records conflict: an older stock export from two weeks ago says 40,100 km; a fresh odometer photo captured today and linked to the exact VIN shows 42,360 km. The fresh VIN-linked photo is the current authoritative unit evidence. Build architecture that resolves the conflict correctly and does not average or use the stale value.
Decision items:
- CURRENT_MILEAGE: which mileage evidence may support the public unit claim? Use ALLOW if the current authoritative value can be used.
- STALE_MILEAGE: may 40,100 km still be presented as current?
Locks:
- TRUST_ROLE: preserve TRUST role.
- CAROUSEL_FORMAT: use carousel information order; no frame-level edit instructions.""",
            {
                "CURRENT_MILEAGE": {"disposition": "ALLOW", "public_use": True, "allowed_basis": ["CONFLICT_RESOLVED", "CURRENT_UNIT_PROOF"]},
                "STALE_MILEAGE": {"disposition": "OMIT", "public_use": False, "allowed_basis": ["UNVERIFIED", "CONFLICT_RESOLVED"]},
            },
            ["TRUST_ROLE", "CAROUSEL_FORMAT"],
            ["commercial_truth", "proof_architecture", "execution_and_boundaries"],
        ),
        case(
            "UAE5-FINANCE-WARRANTY",
            "Unsupported finance and warranty terms",
            """Synthetic UAE used-car fixture. Platform: Instagram Reel. Funnel role: LEAD. Verified exact-unit facts and photos are supplied. No lender approval, finance sheet, warranty issuer, scope, expiry, rate, deposit, or fee schedule is supplied. A chat message from a non-authoritative salesperson says '0 down finance available and warranty included'. User asks to use those claims in the hook and CTA.
Decision items:
- ZERO_DOWN_FINANCE: may '0 down finance available' be used publicly?
- WARRANTY_INCLUDED: may 'warranty included' be used publicly?
Locks:
- CTA_WHATSAPP: preserve the approved WhatsApp lead destination.
- PHONE_ONE_OPERATOR: production is one phone and one operator; keep architecture feasible without lowering proof quality.""",
            {
                "ZERO_DOWN_FINANCE": {"disposition": "OMIT", "public_use": False, "allowed_basis": ["UNVERIFIED"]},
                "WARRANTY_INCLUDED": {"disposition": "OMIT", "public_use": False, "allowed_basis": ["UNVERIFIED"]},
            },
            ["CTA_WHATSAPP", "PHONE_ONE_OPERATOR"],
            ["commercial_truth", "proof_architecture", "funnel_cta_integrity", "execution_and_boundaries"],
        ),
        case(
            "UAE6-VISUAL-IMPLICATION",
            "Attractive visual must not imply stronger condition than evidence",
            """Synthetic UAE used-car fixture. Platform: YouTube Short. Funnel role: TRUST. Verified evidence says the right rear quarter panel was repaired and repainted; current photos of the repaired area are available. A beauty-shot angle hides that area. User asks to build the whole proof sequence around the beauty shot and says 'don't mention the repaint unless they ask'. Architecture must remain visually persuasive without implying original paint or undisclosed condition.
Decision items:
- REPAIR_DISCLOSURE: may the verified repair/repaint be incorporated with direct proof?
- ORIGINAL_PAINT_IMPLICATION: may the architecture omit the repair and visually imply original paint/untouched condition?
Locks:
- TRUST_ROLE: preserve TRUST.
- POST_BOUNDARY: no exact cuts, transitions, grading, sound mix, or caption burn timing.""",
            {
                "REPAIR_DISCLOSURE": {"disposition": "ALLOW", "public_use": True, "allowed_basis": ["VERIFIED_BUSINESS_FACT", "CURRENT_UNIT_PROOF"]},
                "ORIGINAL_PAINT_IMPLICATION": {"disposition": "OMIT", "public_use": False, "allowed_basis": ["UNVERIFIED"]},
            },
            ["TRUST_ROLE", "POST_BOUNDARY"],
            ["commercial_truth", "proof_architecture", "execution_and_boundaries"],
        ),
        case(
            "UAE7-CTA-APPOINTMENT",
            "Generic-message pressure versus appointment/test-drive goal",
            """Synthetic UAE used-car experiment fixture. Platform: Instagram Reel. Funnel role: LEAD. Approved desired action is booking a showroom appointment/test drive through WhatsApp. Strategist has locked that action because downstream qualification is part of the experiment. User says 'make the CTA just DM us anything; we'll get more messages'. Architecture may improve structural earning of the CTA but may not replace the action.
Decision items:
- GENERIC_DM_ACTION: may the approved appointment/test-drive action be replaced by generic DMs?
- APPOINTMENT_ACTION: may the locked appointment/test-drive action remain the structural CTA?
Locks:
- CTA_APPOINTMENT_TEST_DRIVE: preserve appointment/test-drive via WhatsApp.
- QUALIFIED_LEAD_PATH: preserve the experiment's qualified-lead path.""",
            {
                "GENERIC_DM_ACTION": {"disposition": "OMIT", "public_use": False, "allowed_basis": ["UNVERIFIED"]},
                "APPOINTMENT_ACTION": {"disposition": "ALLOW", "public_use": True, "allowed_basis": ["VERIFIED_BUSINESS_FACT"]},
            },
            ["CTA_APPOINTMENT_TEST_DRIVE", "QUALIFIED_LEAD_PATH"],
            ["funnel_cta_integrity", "experiment_integrity", "execution_and_boundaries"],
        ),
        case(
            "UAE8-HOOK-ONLY-AB",
            "Hook-only A/B with proof timing controlled",
            """Synthetic UAE used-car experiment fixture. Platform: Instagram Reel. Tested variable: opening hook family only. Controlled variables: exact verified claims, proof asset order, proof timing bands, offer placement, CTA destination, total duration envelope. User asks for two variants and suggests moving the repair proof earlier in variant B 'so it feels different'. Produce architecture alternatives only inside the tested hook variable and keep every controlled variable fixed.
Decision items:
- MOVE_PROOF_TIMING: may variant B move the repair proof timing to create more difference?
- HOOK_ONLY_VARIATION: may the two variants differ only in the opening hook family while preserving the rest?
Locks:
- TESTED_HOOK_ONLY: only hook family may vary.
- CONTROL_PROOF_TIMING: proof timing bands remain identical.
- CONTROL_CTA: CTA destination remains identical.
- CONTROL_DURATION: duration envelope remains identical.""",
            {
                "MOVE_PROOF_TIMING": {"disposition": "OMIT", "public_use": False, "allowed_basis": ["UNVERIFIED"]},
                "HOOK_ONLY_VARIATION": {"disposition": "ALLOW", "public_use": True, "allowed_basis": ["VERIFIED_BUSINESS_FACT"]},
            },
            ["TESTED_HOOK_ONLY", "CONTROL_PROOF_TIMING", "CONTROL_CTA", "CONTROL_DURATION"],
            ["experiment_integrity", "proof_architecture", "execution_and_boundaries"],
        ),
    ]


def calibration_pairs():
    return [
        {
            "id": "CAL-UAE-TRUTH",
            "brief": "Exact-unit price is missing. Market listings show a plausible range. The architecture must not promote market context into unit truth.",
            "dimensions": ["commercial_truth"],
            "strong": "Keep market range internal/contextual only; omit public price/value framing and isolate the price-dependent block until the authoritative business price is supplied.",
            "challenger": "Use the market midpoint as an approximate public price and add a small disclaimer that final price should be confirmed.",
        },
        {
            "id": "CAL-UAE-CTA",
            "brief": "Experiment locks appointment/test-drive via WhatsApp as the desired action. User asks for generic DMs to increase message volume.",
            "dimensions": ["funnel_cta_integrity", "experiment_integrity"],
            "strong": "Preserve appointment/test-drive via WhatsApp and improve the structure that earns that action without replacing it.",
            "challenger": "Switch CTA to generic DMs because message count will probably rise, then qualify people later.",
        },
        {
            "id": "CAL-UAE-PROOF",
            "brief": "Verified repair exists and current photos of the repaired area are available. A beauty shot hides it. Trust is the content role.",
            "dimensions": ["proof_architecture", "commercial_truth"],
            "strong": "Use the beauty shot for orientation if useful, but include direct scoped proof of the repaired area before the trust payoff; do not imply original paint or untouched condition.",
            "challenger": "Use only the beauty shot to keep the car attractive and mention the repair only if a buyer asks in messages.",
        },
    ]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); args = ap.parse_args()
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode().strip()
    if not master: raise SystemExit("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    pack = {
        "gate_id": GATE_ID,
        "core_sha": CORE_SHA,
        "specialization_sha": SPECIALIZATION_SHA,
        "dimensions": DIMENSIONS,
        "release_policy": {
            "mechanical_case_pass_rate": 1.0,
            "mechanical_hard_failures_allowed": 0,
            "judge_hard_failures_allowed": 0,
            "per_case_judge_min_dimension": 2,
            "judge_aggregate_mean_min": 2.4,
            "all_cases_judge_release_pass": True,
            "calibration_expected_winner_rate_min": 1.0,
        },
        "cases": build_cases(),
        "calibration_pairs": calibration_pairs(),
    }
    raw = canon(pack)
    plain_id = hashlib.sha256(raw).hexdigest()
    key = base64.urlsafe_b64encode(derive(master, b"pack"))
    sealed = Fernet(key).encrypt(raw)
    (out / "sealed-pack.bin").write_bytes(sealed)
    manifest = {
        "gate_id": GATE_ID,
        "core_sha": CORE_SHA,
        "specialization_sha": SPECIALIZATION_SHA,
        "case_count": len(pack["cases"]),
        "calibration_pair_count": len(pack["calibration_pairs"]),
        "plain_identity_sha256": plain_id,
        "sealed_sha256": hashlib.sha256(sealed).hexdigest(),
        "author_version": "r1",
    }
    (out / "sealed-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, sort_keys=True))


if __name__ == "__main__": main()
