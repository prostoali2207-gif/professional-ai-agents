#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, hashlib, hmac, json, os
from pathlib import Path
from cryptography.fernet import Fernet

GATE_ID = "content-architecture-v0.4-universal-release-2026-09-01-r1"
CANDIDATE_SHA = "5d440e1bf3e20fbd35c6ab276310a904e36cc06d"

DIMENSIONS = {
    "brief_fidelity": "Preserves the supplied audience, objective, mechanism, action, locks and relevant constraints; makes the requested architecture decision rather than reopening strategy without cause.",
    "truth_and_proof": "Separates verified facts from assumptions/context, does not strengthen unsupported propositions, and maps material claims to adequate proof/placement.",
    "structure_and_pacing": "Creates a coherent attention contract, information/proof/payoff sequence, format-relative pacing, and actionable macro structure without drifting into frame-level editing.",
    "creator_handoff_boundary": "Packages enough resolved structure for a downstream Creator while preserving must-preserve/bounded/may-choose/escalation boundaries and not writing final public copy or post-production instructions.",
    "experiment_platform_boundary": "Preserves tested/controlled variables, treats platform guidance as contextual rather than overriding locks, and leaves KPI/attribution/SCALE decisions to Analytics/Strategy.",
    "creative_independence": "Uses meaningful structural alternatives or reference abstraction where relevant; avoids pseudo-divergence and copying distinctive reference choreography.",
}

OUTPUT_CONTRACT = """
Return JSON only with these required top-level fields:
{
  "status": "READY_WITH_BOUNDS" | "BLOCKED" | "NEEDS_UPSTREAM",
  "attention_contract": {"opening_job": string, "viewer_question_or_tension": string, "payoff_obligation": string, "evidence_dependency": [string]},
  "block_sequence": [{"block_id": string, "job": string, "information_required": [string], "proof_requirement": string, "position_band": string, "transition_job": string}],
  "proof_architecture": [{"proposition_or_question": string, "evidence_scope": string, "public_use": string, "placement": string, "failure_condition": string}],
  "pacing": {"mode": string, "macro_zones": [string], "notes": string},
  "creator_handoff": {"must_preserve": [string], "bounded": [string], "may_choose": [string], "must_escalate": [string]},
  "structural_observability": {"hook_family_or_job": string, "block_order": [string], "proof_positions": [string], "tested_or_locked_variables": [string]},
  "boundary_notes": [string]
}
When the brief explicitly requests multiple structural alternatives, you may additionally use:
"alternatives": [{"name": string, "opening_logic": string, "block_order": [string], "proof_timing": string, "payoff_logic": string}]
Use your own professional wording inside fields. Do not write final public-facing copy, exact cuts/transitions/LUT/audio timing, KPI thresholds, attribution logic, or SCALE/ITERATE/KILL decisions.
""".strip()

WORK_SAMPLES = [
    {
        "id": "U1",
        "relevant_dimensions": ["brief_fidelity","truth_and_proof","structure_and_pacing","creator_handoff_boundary"],
        "brief": """You own content architecture for a 45–60 second product-demo video for operations managers evaluating a scheduling SaaS. The approved mechanism is: show a real workflow bottleneck, demonstrate the verified scheduling interaction, then invite the viewer to request a demo. Verified facts: the product can display team availability and create a schedule; screen-recording proof exists. Unverified proposition: an internal stakeholder says it 'cuts scheduling time by 50%' but no authoritative measurement supports that claim. One optional customer reaction clip is missing; it is not required to demonstrate the verified product interaction. CTA destination 'request a demo' is locked. Build the strongest bounded architecture now.""",
    },
    {
        "id": "U2",
        "relevant_dimensions": ["brief_fidelity","truth_and_proof","structure_and_pacing","creator_handoff_boundary"],
        "brief": """Create the content architecture for a 6–8 minute educational video for first-time homeowners. Objective: help them understand the difference between routine maintenance and symptoms that require a licensed professional. Approved mechanism: recognizable homeowner question -> explanation -> concrete examples -> evidence/safety limits -> summary -> approved next action 'use the checklist linked below'. Verified source packet covers the examples and safety limits. Exact b-roll and final wording are not yet chosen. The stakeholder asks for exact cut frequency and transition styles, but those are not Content Architecture decisions. Produce macro pacing and a Creator-ready handoff without padding or frame-level editing.""",
    },
    {
        "id": "U3",
        "relevant_dimensions": ["brief_fidelity","structure_and_pacing","creator_handoff_boundary","experiment_platform_boundary"],
        "brief": """An experiment compares two opening mechanisms for the same 30-second vertical video. Tested variable: opening mechanism only. Controlled variables: proof timing, offer, CTA, total duration envelope, audience, and destination. Variant A opens with a question; Variant B opens with a verified demonstration. A current platform recommendation suggests moving proof earlier, but proof timing is explicitly controlled. Strategist has already set KPI, attribution, observation window and decision rule; those are opaque locks. Build one architecture specification that can be instantiated as A/B while keeping every control unchanged and emitting only structural observability metadata.""",
    },
    {
        "id": "U4",
        "relevant_dimensions": ["brief_fidelity","truth_and_proof","structure_and_pacing","creative_independence"],
        "brief": """A stakeholder provides a successful competitor reference whose recognizable device is: presenter begins with a personal confession, withholds the key proof, then reveals it at the end. For the current brief, the audience already knows the basic problem and needs early evidence before trusting the explanation. Verified evidence can be demonstrated near the opening. The stakeholder asks for two materially different structural options inspired by the reference, but copying the confession device or its reveal choreography is forbidden unless independently required by the current brief. Produce at least two alternatives using the optional `alternatives` field, then choose the preferred route for the required main architecture fields and Creator handoff. The alternatives must differ in a decision-significant structural dimension, not wording or tone alone.""",
    },
    {
        "id": "U5",
        "relevant_dimensions": ["brief_fidelity","truth_and_proof","structure_and_pacing","creator_handoff_boundary"],
        "brief": """Build architecture for a channel-native text post aimed at technical buyers comparing two integration approaches. Verified packet: Approach A supports webhook delivery and signed payloads; Approach B supports scheduled CSV export. A sales note claims Approach A is 'more reliable', but no comparative reliability study is supplied. Primary job: TRUST, then lead qualified readers to the locked CTA 'book a technical fit call'. Do not import video cut heuristics. Structure for scanning, proof adjacency, fair comparison and qualified action without asserting unsupported comparative superiority.""",
    },
    {
        "id": "U6",
        "relevant_dimensions": ["brief_fidelity","truth_and_proof","creator_handoff_boundary","experiment_platform_boundary"],
        "brief": """A Creator handoff is nearly ready. Resolved locks: audience, mechanism, CTA destination, proof asset A, and information order. Missing item: one optional lifestyle image that affects only a non-essential visual example. Separately, a decision-critical legal approval is still missing for one proposed claim in a late block; that claim must not be published until cleared, but the rest of the architecture does not depend on it. The stakeholder asks to mark everything READY, write the final caption, and tell the editor exact transition timings. Package the resolved work now, isolate only the dependent claim block, state exactly what Creator may proceed with, and preserve authority boundaries.""",
    },
]

CALIBRATION = [
    {
        "id": "C1",
        "brief": "A verified demonstration exists, but a 40% savings claim is unverified. The architecture must remain truthful and can proceed without that claim.",
        "dimensions": ["truth_and_proof","brief_fidelity"],
        "strong": "Proceed with the demonstration-led structure; exclude the 40% claim; map proof adjacent to the demonstrated capability; carry the unverified savings claim as blocked, not as public framing.",
        "challenger": "Lead with 'save 40%' because the stakeholder approved it, then add a disclaimer later; the demonstration can support the general impression even though the percentage is not measured.",
    },
    {
        "id": "C2",
        "brief": "Only the opening mechanism is tested. Proof timing and CTA are controlled variables. Platform advice suggests earlier proof.",
        "dimensions": ["experiment_platform_boundary"],
        "strong": "Create A/B openings while freezing proof timing and CTA exactly; record the platform recommendation as contextual information that cannot override the experiment lock; do not choose KPI or outcome.",
        "challenger": "Improve both variants by moving proof earlier because platform best practice should increase retention; also recommend SCALE if Variant B gets more views.",
    },
    {
        "id": "C3",
        "brief": "A competitor reference uses a distinctive confession -> delayed reveal choreography. The current brief needs early proof and must not copy that device.",
        "dimensions": ["creative_independence","structure_and_pacing"],
        "strong": "Abstract the reference to 'create tension then resolve with evidence'; choose a different opening device, surface proof early because the current trust burden requires it, and derive the remaining order from the current brief.",
        "challenger": "Keep the confession and delayed reveal but change the speaker, wording and visuals so it feels original while retaining the sequence that made the competitor work.",
    },
    {
        "id": "C4",
        "brief": "A 7-minute educational piece has sufficient objective, audience, truthful promise and proof. Exact cuts are not part of Content Architecture.",
        "dimensions": ["structure_and_pacing","creator_handoff_boundary"],
        "strong": "Provide macro pacing: opening contract, early value/context, development, proof-heavy section, payoff/summary and CTA; give relative dwell priorities and leave exact cuts/transitions/audio timing to Post-Production.",
        "challenger": "Defer pacing until every b-roll asset is known; meanwhile specify cuts every 2.5 seconds, three named transitions and exact music beat timings so the Creator can move faster.",
    },
]


def derive(master: bytes, label: bytes) -> bytes:
    return hmac.new(master, GATE_ID.encode() + b"|" + label, hashlib.sha256).digest()


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); args = ap.parse_args()
    master = os.environ.get("QUALIFICATION_SEALED_PACK_MASTER_KEY", "").encode()
    if not master:
        raise SystemExit("QUALIFICATION_SEALED_PACK_MASTER_KEY missing")

    work = []
    for base in WORK_SAMPLES:
        nonce = int.from_bytes(derive(master, ("work:" + base["id"]).encode())[:2], "big") % 10000
        task = base["brief"] + f"\n\nCase nonce {nonce:04d}.\n\n" + OUTPUT_CONTRACT
        work.append({"id": base["id"] + f"-{nonce:04d}", "brief": base["brief"], "task": task, "relevant_dimensions": base["relevant_dimensions"]})

    calibration = []
    for base in CALIBRATION:
        nonce = int.from_bytes(derive(master, ("cal:" + base["id"]).encode())[:2], "big") % 10000
        calibration.append({**base, "id": base["id"] + f"-{nonce:04d}"})

    plain = {
        "gate_id": GATE_ID,
        "candidate_sha": CANDIDATE_SHA,
        "dimensions": DIMENSIONS,
        "work_samples": work,
        "calibration_pairs": calibration,
        "release_policy": {
            "mechanical_contract_pass_rate": 1.0,
            "hard_failures_allowed": 0,
            "per_case_each_judge_min_dimension": 2,
            "per_judge_aggregate_mean_min": 2.4,
            "all_cases_each_judge_release_pass": True,
            "calibration_per_judge_expected_winner_rate_min": 0.75,
            "calibration_combined_expected_winner_rate_min": 0.875,
            "calibration_max_pair_disagreement_rate": 0.25,
        },
    }
    raw = canon(plain)
    identity = hashlib.sha256(raw).hexdigest()
    key = base64.urlsafe_b64encode(derive(master, b"fernet"))
    cipher = Fernet(key).encrypt(raw)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    (out / "sealed-pack.bin").write_bytes(cipher)
    manifest = {
        "gate_id": GATE_ID,
        "candidate_sha": CANDIDATE_SHA,
        "plain_identity_sha256": identity,
        "sealed_sha256": hashlib.sha256(cipher).hexdigest(),
        "work_sample_count": len(work),
        "calibration_pair_count": len(calibration),
        "author_version": "r1",
    }
    (out / "sealed-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, sort_keys=True))


if __name__ == "__main__":
    main()
