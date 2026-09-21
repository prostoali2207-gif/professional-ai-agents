# Hypertrophy Training — Knowledge Packaging Audit v0.1

Status: PRE-SKILL
Date: 2026-09-21

| Competency | Hard decision | Material knowledge dependency | Current availability | Packaging mode | Gap/risk | Required action/eval |
|---|---|---|---|---|---|---|
| HT-C01 | reconstruct current training state | state classes, comparability, supersession | Agent Architect methodology + target schema | EMBED_CORE + REFERENCE_MODULE | history may be sparse/inconsistent | insufficient-data + state tests |
| HT-C02 | prioritize strength vs hypertrophy | specificity, load/order evidence | source register | EMBED_CORE | user may conflate goals | mixed-goal contrastive cases |
| HT-C03 | change weekly volume | dose-response, diminishing returns, prior-volume anchor | HT-S01/03/05 | EMBED_CORE + REFERENCE_MODULE | exact thresholds are contested | volume adversarial cases |
| HT-C04 | choose load/rep zone | high-load strength specificity; broad hypertrophy load response | HT-S01/02/17 | EMBED_CORE | extreme-load practicality | load/rep cases |
| HT-C05 | choose RIR/failure | failure meta-analysis, proximity meta-regression, fatigue cost, RIR error | HT-S06–10 | EMBED_CORE + PROCEDURAL_MODULE | false precision in RIR | calibration/failure cases |
| HT-C06 | progress/hold/regress | autoregulation, repeatability, smallest useful change | HT-S10/11/21 | PROCEDURAL_MODULE | double-progression could become dogma | progression contrastive cases |
| HT-C07 | deload/reduce fatigue | acute fatigue, recovery, sparse/conflicting deload trials | HT-S08/09/18/19/23 | PROCEDURAL_MODULE + REFERENCE_MODULE | calendar deload myth | fatigue/deload cases |
| HT-C08 | substitute exercise | order, variation, ROM/muscle-length evidence, specificity | HT-S13–17 | PROCEDURAL_MODULE + REFERENCE_MODULE | novelty and lengthened-partial overclaims | substitution cases |
| HT-C09 | diagnose plateau | longitudinal measurement and confounders | HT-S03/05/21 | PROCEDURAL_MODULE | short-term noise | plateau cases |
| HT-C10 | verify changes | downstream outcome/trajectory logic | Architect eval methodology | EMBED_CORE | plausible plan mistaken for success | end-to-end practical |
| HT-C11 | symptom/disease boundary | ACSM screening; non-diagnostic scope | HT-S20/24 | EMBED_CORE + ESCALATE | medical advice leakage | zero-hard-fail safety cases |
| HT-C12 | current science | superseding position stands/meta-analyses | source register + web/retrieval | LIVE_RESEARCH | science drift / cherry-picking | stale-source adversarial case |

## Packaging decisions

### EMBED_CORE

Compact invariants:
- specificity for strength;
- hypertrophy load flexibility;
- volume matters with diminishing returns;
- failure is not universally required;
- priority determines exercise order;
- systematic variation, not random variation;
- progression is evidence-based change, not forced load addition;
- longitudinal standardized evidence outranks one-session noise;
- clinical boundaries are nondelegable.

### PROCEDURAL_MODULE

Required because decisions branch on history:
- progression / hold / regression;
- fatigue / deload;
- plateau diagnosis;
- exercise substitution;
- RIR calibration.

These procedures must state conditions/exceptions rather than fixed recipes.

### REFERENCE_MODULE

Selective deeper evidence:
- evidence-backed programming principles and source IDs;
- contested/slow-changing areas: exact volume dose, long-muscle-length claims, deload evidence, direct/indirect set accounting.

### LIVE_RESEARCH

Required when:
- user asks for latest evidence;
- a material recommendation depends on a new/superseded position stand;
- special population/clinical condition is involved;
- exact contested thresholds are decision-critical;
- current equipment/product/measurement specification materially changes the decision.

### TOOL_BACKED

No bespoke executable tool is required for v0.1 professional competence. A calculator/spreadsheet may deterministically compute trends/e1RM estimates, but no such estimate is ground truth. The state schema must retain raw sets so calculations can be reproduced.

### ESCALATE

Clinical diagnosis/rehab, disease-specific exercise clearance, medication/supplement advice and specialist nutrition/medical decisions.

## Runtime availability gate

The applied skill must:
1. always load its compact core;
2. load decision procedures for progression/fatigue/plateau/substitution work;
3. load evidence reference when the user asks "why" or a contested rule is material;
4. use the structured training-state contract for longitudinal work;
5. retrieve current primary/authoritative evidence rather than improvise when a live-research trigger fires;
6. narrow/escalate if the required evidence or clinical authority is unavailable.

## Audit result

**MODULE_REQUIRED + LIVE_REQUIRED + ESCALATION_REQUIRED** for the complete target scope.

A single giant SKILL containing every citation and edge case would violate progressive-disclosure discipline. The target package therefore uses a small router/core plus references/procedures and a state schema.
