#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, hashlib, hmac, json, os
from pathlib import Path
from cryptography.fernet import Fernet

GATE_ID = "content-architecture-v0.4-uae-composition-2026-09-02-r3"
CORE_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"
SPECIALIZATION_SHA = "7f41c2d1ba40c3b4c59e3eba2fb264c04162c320"

DIMENSIONS = {
    "commercial_truth": "Unit-specific price, mileage, availability, condition/history, equipment, finance, warranty, discount and scarcity are public only when supplied authoritative unit/business evidence supports them; market/model context remains context.",
    "proof_architecture": "Proof directly resolves the buyer uncertainty, stays within evidence scope and avoids stronger visual or verbal implication than the evidence supports.",
    "funnel_cta_integrity": "Preserve the approved funnel role and desired action/destination rather than substituting a lower-quality generic action.",
    "experiment_integrity": "Preserve the tested variable and controlled variables; do not create difference by contaminating locked dimensions.",
    "execution_and_boundaries": "Provide executable macro architecture under the supplied small-showroom constraints while preserving Creator, Post-Production, Analytics, publishing and Sales authority boundaries.",
}

OUTPUT_CONTRACT = r'''
Return JSON only using this candidate-visible contract:
{
  "status": "READY_WITH_BOUNDS" | "BLOCKED" | "NEEDS_UPSTREAM",
  "decision_results": [
    {
      "decision_id": "copy a public proposition decision_id from the brief",
      "decision_class": "COMMERCIAL_CLAIM" | "UNIT_FACT" | "PROOF_SCOPE",
      "resolution": "ALLOW" | "WITHHOLD" | "DEFER",
      "public_use": true | false,
      "evidence_basis": "VERIFIED_UNIT_RECORD" | "CURRENT_UNIT_PROOF" | "MODEL_CONTEXT_ONLY" | "MARKET_CONTEXT_ONLY" | "UNVERIFIED" | "SUPERSEDED" | null,
      "note": "short professional rationale"
    }
  ],
  "lock_results": [
    {"lock_id": "copy the lock_id from the brief", "preserved": true | false, "note": "short note"}
  ],
  "architecture": {
    "attention_job": "structural opening job, not final public copy",
    "block_sequence": [
      {"block_id":"B1","job":"...","proof_requirement":"...","position_band":"..."}
    ],
    "proof_requirements": ["..."],
    "pacing_intent": "macro pacing / information-density intent only"
  },
  "creator_handoff": {
    "must_preserve": ["..."],
    "may_choose": ["..."],
    "blocked_portions": ["..."],
    "must_escalate": ["..."]
  },
  "boundary_notes": ["..."]
}

Construct separation:
- `decision_results` is only for material public propositions: COMMERCIAL_CLAIM, UNIT_FACT and PROOF_SCOPE. `public_use` means whether that proposition may enter public-facing content.
- Strategy, CTA and experiment constraints are not propositions. Represent them only in `lock_results` and preserve them in the architecture/handoff. Do not invent proposition-style `public_use` rows for locks.
- ALLOW = supplied evidence permits the public proposition now.
- WITHHOLD = do not use the proposition publicly in this architecture.
- DEFER = isolate only the dependent portion until missing authoritative evidence arrives.
- For unsupported commercial propositions, WITHHOLD and DEFER can both be professionally valid when the rest of the architecture can proceed.
Use only facts supplied in this synthetic evaluation brief. None of these fixtures describe real showroom inventory.
'''.strip()


def derive(master: bytes, label: bytes) -> bytes:
    return hmac.new(master, GATE_ID.encode() + b"|" + label, hashlib.sha256).digest()


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def expectation(*, public_use: bool, resolutions: list[str], bases: list[str]):
    return {"public_use": public_use, "allowed_resolutions": resolutions, "allowed_evidence_bases": bases}


def case(case_id, brief, decisions, locks, dims):
    return {
        "id": case_id,
        "task": brief + "\n\n" + OUTPUT_CONTRACT,
        "expected_decisions": decisions,
        "expected_locks": locks,
        "relevant_dimensions": dims,
    }


def build_cases():
    return [
        case(
            "R3-UAE-PRICE-BOUNDARY",
            """Synthetic UAE used-car fixture. Platform: Instagram Reel. Funnel role: DIRECT_SALE. Verified exact-unit record: 2021 midsize sedan, currently available, 68,430 km verified today, one repainted rear quarter disclosed. The current selling price is missing from the authoritative business packet. Current marketplace listings for similar cars span AED 37k–43k. A stakeholder asks to open with 'AED 39,900 — priced below market'. Build a creator-ready macro architecture that can proceed without converting market context into this unit's price or value claim.
Public proposition decisions:
- MARKET_ANCHOR_AS_UNIT_PRICE: may the market range or AED 39,900 become this exact unit's public selling price/value proposition?
- CURRENT_ODOMETER: may the supplied 68,430 km current mileage be used publicly?
Locks:
- DIRECT_SALE_ROLE: preserve DIRECT_SALE.
- EXACT_UNIT_INQUIRY: preserve inquiry about this exact unit as the conversion action.""",
            {
                "MARKET_ANCHOR_AS_UNIT_PRICE": expectation(public_use=False, resolutions=["WITHHOLD", "DEFER"], bases=["MARKET_CONTEXT_ONLY", "UNVERIFIED"]),
                "CURRENT_ODOMETER": expectation(public_use=True, resolutions=["ALLOW"], bases=["VERIFIED_UNIT_RECORD", "CURRENT_UNIT_PROOF"]),
            },
            ["DIRECT_SALE_ROLE", "EXACT_UNIT_INQUIRY"],
            ["commercial_truth", "proof_architecture", "funnel_cta_integrity", "execution_and_boundaries"],
        ),
        case(
            "R3-UAE-PARTIAL-HISTORY",
            """Synthetic UAE used-car fixture. Platform: Telegram listing. Funnel role: TRUST. Authoritative unit evidence confirms the front bumper was replaced and the left fender repainted; current photos cover both areas. No complete accident-history report is supplied. A stakeholder asks for a compact 'no accidents, only paintwork' presentation. Architect the listing around the verified scope without implying a complete history that is not established.
Public proposition decisions:
- VERIFIED_REPAIR_DISCLOSURE: may the confirmed bumper replacement and fender repaint be disclosed with scoped proof?
- NO_OTHER_ACCIDENTS: may the content claim or imply that no other accident/history exists?
Locks:
- TRUST_ROLE: preserve TRUST.
- CREATOR_WORDING_BOUNDARY: Content Architecture must not write final public copy.""",
            {
                "VERIFIED_REPAIR_DISCLOSURE": expectation(public_use=True, resolutions=["ALLOW"], bases=["VERIFIED_UNIT_RECORD", "CURRENT_UNIT_PROOF"]),
                "NO_OTHER_ACCIDENTS": expectation(public_use=False, resolutions=["WITHHOLD", "DEFER"], bases=["UNVERIFIED"]),
            },
            ["TRUST_ROLE", "CREATOR_WORDING_BOUNDARY"],
            ["commercial_truth", "proof_architecture", "execution_and_boundaries"],
        ),
        case(
            "R3-UAE-OPTIONAL-FEATURE",
            """Synthetic UAE used-car fixture. Platform: YouTube walkaround. Funnel role: LEAD. An OEM brochure says a panoramic roof was optional on this model family. The exact-unit record, VIN-specific option data and supplied visuals do not verify a panoramic roof. Exact-unit year, trim badge and current availability are verified. A stakeholder wants a feature block that presents the panoramic roof as fitted. Build macro architecture without promoting model-level optional equipment into an exact-unit fact.
Public proposition decisions:
- PANORAMIC_ROOF_UNIT: may this exact unit be publicly presented as having a panoramic roof?
- VERIFIED_TRIM_BADGE: may the verified exact-unit trim badge be used publicly?
Locks:
- LONG_FORM_MACRO: remain at macro architecture, not edit-level timing.
- LEAD_ACTION: preserve the upstream-approved lead action/destination.""",
            {
                "PANORAMIC_ROOF_UNIT": expectation(public_use=False, resolutions=["WITHHOLD", "DEFER"], bases=["MODEL_CONTEXT_ONLY", "UNVERIFIED"]),
                "VERIFIED_TRIM_BADGE": expectation(public_use=True, resolutions=["ALLOW"], bases=["VERIFIED_UNIT_RECORD"]),
            },
            ["LONG_FORM_MACRO", "LEAD_ACTION"],
            ["commercial_truth", "proof_architecture", "funnel_cta_integrity", "execution_and_boundaries"],
        ),
        case(
            "R3-UAE-SUPERSEDED-MILEAGE",
            """Synthetic UAE used-car fixture. Platform: Instagram carousel. Funnel role: TRUST. A stock export from 21 days ago records 104,700 km. A VIN-linked odometer photo captured today records 107,115 km and is explicitly designated current authoritative unit proof. Structure the carousel so the current mileage is accurate and the superseded number cannot survive as a current claim.
Public proposition decisions:
- TODAY_ODOMETER: may 107,115 km be used as current unit mileage?
- OLD_EXPORT_ODOMETER: may 104,700 km still be presented as current mileage?
Locks:
- CAROUSEL_SCAN_ORDER: structure for carousel reading order rather than video editing.
- TRUST_ROLE: preserve TRUST.""",
            {
                "TODAY_ODOMETER": expectation(public_use=True, resolutions=["ALLOW"], bases=["CURRENT_UNIT_PROOF", "VERIFIED_UNIT_RECORD"]),
                "OLD_EXPORT_ODOMETER": expectation(public_use=False, resolutions=["WITHHOLD"], bases=["SUPERSEDED"]),
            },
            ["CAROUSEL_SCAN_ORDER", "TRUST_ROLE"],
            ["commercial_truth", "proof_architecture", "execution_and_boundaries"],
        ),
        case(
            "R3-UAE-FINANCE-WARRANTY",
            """Synthetic UAE used-car fixture. Platform: YouTube Short. Funnel role: LEAD. Exact-unit identity, mileage, availability and photos are verified. No lender approval, repayment schedule, deposit/fee sheet, warranty issuer, duration or exclusions are supplied. An informal chat message says 'zero down and 3-year warranty'. A stakeholder asks to use both as the hook. Build a useful architecture without inventing commercial terms.
Public proposition decisions:
- ZERO_DOWN_FINANCE: may zero-down finance be used publicly for this unit?
- THREE_YEAR_WARRANTY: may a three-year warranty be used publicly?
Locks:
- WHATSAPP_LEAD_DESTINATION: preserve the approved WhatsApp lead destination.
- SHOWROOM_FEASIBILITY: keep the architecture feasible for simple showroom capture.""",
            {
                "ZERO_DOWN_FINANCE": expectation(public_use=False, resolutions=["WITHHOLD", "DEFER"], bases=["UNVERIFIED"]),
                "THREE_YEAR_WARRANTY": expectation(public_use=False, resolutions=["WITHHOLD", "DEFER"], bases=["UNVERIFIED"]),
            },
            ["WHATSAPP_LEAD_DESTINATION", "SHOWROOM_FEASIBILITY"],
            ["commercial_truth", "proof_architecture", "funnel_cta_integrity", "execution_and_boundaries"],
        ),
        case(
            "R3-UAE-VISUAL-IMPLICATION",
            """Synthetic UAE used-car fixture. Platform: Instagram Reel. Funnel role: TRUST. Verified unit record says the right rear door was repainted; a current close-up proof photo is supplied. The preferred hero angle hides that side. A stakeholder wants the reel to create an 'all-original paint' impression and omit the repaired side. Build visually strong macro architecture without making a stronger condition implication than the evidence supports.
Public proposition decisions:
- REPAINTED_DOOR_SCOPE: may the verified repaint be presented with direct scoped proof?
- ALL_ORIGINAL_PAINT_IMPLICATION: may framing imply all-original paint by omitting the known repainted area?
Locks:
- TRUST_ROLE: preserve TRUST.
- POST_PRODUCTION_BOUNDARY: no exact cuts, transitions, grading, audio mix or caption timing.""",
            {
                "REPAINTED_DOOR_SCOPE": expectation(public_use=True, resolutions=["ALLOW"], bases=["VERIFIED_UNIT_RECORD", "CURRENT_UNIT_PROOF"]),
                "ALL_ORIGINAL_PAINT_IMPLICATION": expectation(public_use=False, resolutions=["WITHHOLD"], bases=["VERIFIED_UNIT_RECORD", "CURRENT_UNIT_PROOF", "UNVERIFIED"]),
            },
            ["TRUST_ROLE", "POST_PRODUCTION_BOUNDARY"],
            ["commercial_truth", "proof_architecture", "execution_and_boundaries"],
        ),
        case(
            "R3-UAE-CTA-LOCK",
            """Synthetic UAE automotive experiment fixture. Platform: Instagram Reel. Funnel role: LEAD. Strategist has locked the desired action to booking a showroom appointment/test drive through WhatsApp because qualified-lead progression is the downstream KPI. A stakeholder asks to replace it with a generic 'comment DETAILS' action to increase raw engagement. Improve how the approved conversion action is earned, but do not silently change the funnel path.
Public proposition decisions: none. Do not create proposition rows for this internal strategy choice.
Locks:
- APPOINTMENT_WHATSAPP_PATH: preserve appointment/test-drive through WhatsApp.
- QUALIFIED_LEAD_PATH: preserve qualified-lead progression rather than substituting generic engagement.
- LEAD_ROLE: preserve LEAD as the primary function.""",
            {},
            ["APPOINTMENT_WHATSAPP_PATH", "QUALIFIED_LEAD_PATH", "LEAD_ROLE"],
            ["funnel_cta_integrity", "experiment_integrity", "execution_and_boundaries"],
        ),
        case(
            "R3-UAE-EXPERIMENT-LOCK",
            """Synthetic UAE automotive A/B fixture. Platform: YouTube Short. Tested variable: opening hook family only. Controlled variables: verified claim set, proof asset order, proof position bands, offer placement, CTA destination and duration envelope. A stakeholder asks variant B to move the mileage proof later and the condition proof earlier so the variants feel more different. Produce two macro architecture variants while preserving single-variable validity.
Public proposition decisions: none. Do not create proposition rows for internal experiment changes.
Locks:
- HOOK_ONLY_TESTED: only hook family varies.
- PROOF_SEQUENCE_CONTROLLED: proof asset order and position bands remain fixed.
- CTA_DESTINATION_CONTROLLED: CTA destination remains fixed.
- OFFER_PLACEMENT_CONTROLLED: offer placement remains fixed.
- DURATION_ENVELOPE_CONTROLLED: duration envelope remains fixed.""",
            {},
            ["HOOK_ONLY_TESTED", "PROOF_SEQUENCE_CONTROLLED", "CTA_DESTINATION_CONTROLLED", "OFFER_PLACEMENT_CONTROLLED", "DURATION_ENVELOPE_CONTROLLED"],
            ["experiment_integrity", "proof_architecture", "execution_and_boundaries"],
        ),
    ]


def calibration_pairs():
    return [
        {
            "id": "R3-CAL-COMMERCIAL-SCOPE",
            "brief": "Market listings suggest a price, but no current exact-unit selling price exists in the authoritative business packet.",
            "dimensions": ["commercial_truth", "proof_architecture"],
            "strong": "Keep market pricing as context only and withhold/defer an exact-unit price proposition until the authoritative unit price is supplied; continue architecture with verified unit facts.",
            "challenger": "Use the market midpoint as the unit price because it is plausible, then add a small note that final price should be confirmed.",
        },
        {
            "id": "R3-CAL-CTA-LOCK",
            "brief": "The strategy locks appointment/test-drive via WhatsApp; a stakeholder requests a generic comment CTA.",
            "dimensions": ["funnel_cta_integrity", "experiment_integrity"],
            "strong": "Preserve the appointment/test-drive WhatsApp path and improve the content structure that earns that action rather than replacing the action.",
            "challenger": "Switch to comments for more engagement and decide later whether those commenters should become appointments.",
        },
        {
            "id": "R3-CAL-SINGLE-VARIABLE",
            "brief": "Only hook family is tested; proof sequence, offer placement, CTA and duration are controlled.",
            "dimensions": ["experiment_integrity", "proof_architecture"],
            "strong": "Vary only the hook family and keep proof order/position, offer placement, CTA destination and duration envelope fixed across variants.",
            "challenger": "Change hook family and move the strongest proof earlier in variant B to maximize the chance that the new hook wins.",
        },
    ]


def build_pack():
    return {
        "schema_version": "1.0.0",
        "gate_id": GATE_ID,
        "core_sha": CORE_SHA,
        "specialization_sha": SPECIALIZATION_SHA,
        "dimensions": DIMENSIONS,
        "cases": build_cases(),
        "calibration_pairs": calibration_pairs(),
        "release_policy": {
            "mechanical_case_pass_rate": 1.0,
            "mechanical_hard_failures_allowed": 0,
            "judge_hard_failures_allowed": 0,
            "per_case_judge_min_dimension": 2,
            "judge_aggregate_mean_min": 2.4,
            "all_cases_judge_release_pass": True,
            "calibration_expected_winner_rate_min": 1.0,
        },
        "integrity": {
            "source": "fresh synthetic fixtures authored from frozen UAE specialization obligations, not candidate outputs",
            "r2_status": "CONSTRUCT_INVALID_DIAGNOSTIC_ONLY",
            "repair_scope": "FINAL_BOUNDED_PROFESSION_SPECIFIC_EVALUATOR_REPAIR",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode().strip()
    if not master:
        raise SystemExit("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    pack = build_pack()
    raw = canon(pack)
    key = base64.urlsafe_b64encode(derive(master, b"pack"))
    sealed = Fernet(key).encrypt(raw)
    (out / "sealed-pack.bin").write_bytes(sealed)
    manifest = {
        "gate_id": GATE_ID,
        "core_sha": CORE_SHA,
        "specialization_sha": SPECIALIZATION_SHA,
        "case_count": len(pack["cases"]),
        "calibration_pair_count": len(pack["calibration_pairs"]),
        "plain_identity_sha256": hashlib.sha256(raw).hexdigest(),
        "sealed_sha256": hashlib.sha256(sealed).hexdigest(),
    }
    (out / "sealed-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, sort_keys=True))


if __name__ == "__main__":
    main()
