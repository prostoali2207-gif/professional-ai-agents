# Knowledge Packaging Audit — Existing Professional Cores

Date: 2026-08-17
Status: initial architecture audit; not a behavioral qualification result.

Purpose: test whether existing Professional Cores retain enough operational knowledge for runtime work, rather than merely documenting what an expert should know.

Method: apply `architect/methodology/knowledge-packaging.md` to CORE and BOUNDARY-CRITICAL competencies. This audit identifies packaging risk; it does not claim a module improves behavior until affected evaluation demonstrates that.

## Paid Media / Performance Marketing 1.0.0

Current artifact inspected: `architect/library/cores/paid-media-performance-marketing/1.0.0/professional-model.md` plus `evidence-and-reuse.md`.

### High-priority findings

| Competency | Hard decision | Material knowledge dependency | Current availability | Packaging mode | Gap/risk | Required action/eval |
|---|---|---|---|---|---|---|
| PM-02 Measurement architecture | Decide whether observed conversion data is fit for optimization | event semantics, deduplication, lag, offline linkage, attribution/configuration, missingness diagnosis | strong principles/checklist in core; platform mechanics intentionally live | EMBED_CORE + PROCEDURAL_MODULE + LIVE_RESEARCH + TOOL_BACKED | diagnosis can become shallow checklist; exact mechanics volatile | design measurement-diagnostics procedure only if hard-case ablation shows core-only insufficiency; live official docs for platform mechanics; tool evidence where account/event data exists |
| PM-03 Attribution/incrementality | Decide whether evidence supports a causal claim | identification assumptions, confounding, experiment/observational boundaries | strong core principle and research evidence | EMBED_CORE + REFERENCE_MODULE + ESCALATE | risk of correct vocabulary but weak identification judgment on novel cases | build compact causal-identification reference only for recurring validated cases; adversarial causal cases; escalate advanced identification |
| PM-04 Experimentation | Design/interpret a decision-relevant experiment | randomization, power/MDE, lag, interference, stopping/analysis | concepts in core; no operational calculation module | EMBED_CORE + PROCEDURAL_MODULE + TOOL_BACKED + REFERENCE_MODULE | material operational-depth gap for power, sample size, sequential/edge-case interpretation | highest-priority candidate: experiment-design procedure + tested calculation helper/reference; novel-case eval and calculation verifier |
| PM-05 Allocation/forecasting | Decide next budget unit under saturation/uncertainty | marginal-return reasoning, response curves, switching/learning cost, forecast uncertainty | stable principles in core; specialist MMM explicitly optional | EMBED_CORE + PROCEDURAL_MODULE + TOOL_BACKED + ESCALATE | may default to qualitative marginal-return language without reproducible allocation method | define bounded allocation procedure for cases supported by available data; use tool/model where calculation is material; escalate MMM/complex optimization |
| PM-06 Auctions/bidding | Diagnose automation failure | stable objective/signal principles plus current platform mechanics | stable principle in core; live boundary explicit | EMBED_CORE + LIVE_RESEARCH | architecture is directionally correct; runtime must actually retrieve current docs | add live-retrieval fixtures for changed/unknown platform mechanics; no static platform encyclopedia |
| PM-08 Creative testing | Preserve learning while selecting variants | hypothesis isolation, sample/lag context, downstream quality, fatigue | good core judgment; limited deep procedure | EMBED_CORE + PROCEDURAL_MODULE | risk of generic testing advice on confounded multi-variable tests | only package a compact test-design/diagnostic procedure if eval demonstrates failure; avoid duplicating PM-04 |
| PM-09 Pacing | Distinguish variance/lag from actionable drift | pacing math, latency, thresholds, forecast ranges | principle only | EMBED_CORE + PROCEDURAL_MODULE + TOOL_BACKED | operational thresholds may be improvised | evaluate realistic pacing cases; package calculator/procedure if repeated errors appear |
| PM-10 Diagnosis | Isolate source of performance drop | discriminating evidence across measurement, auction, creative, funnel, sales, external causes | fault tree embedded | EMBED_CORE + PROCEDURAL_MODULE | fault tree may not encode discriminating tests deeply enough | create hard differential-diagnosis eval before adding module; package only branches where failures are observed |
| PM-12 Privacy/policy | Determine whether current rules constrain measurement/action | current law, consent and platform policy | live boundary explicit | LIVE_RESEARCH + ESCALATE | static knowledge would be unsafe | keep live; require jurisdiction/source verification and legal escalation boundary |

### Paid-media decision

The core is not an empty prompt: substantial stable judgment is already retained. However, operational sufficiency is **UNPROVEN** for several hard decisions. The strongest justified module candidate is PM-04 experimentation because calculation and interpretation are both consequential and reproducible. Measurement diagnosis and pacing are next candidates, but should be admitted only after targeted hard-case evaluation demonstrates a real gap.

Do **not** create one file per PM competency by default. First build discriminating fixtures; then package the minimum knowledge/tooling that repairs demonstrated failures.

## Video Editing & Post-Production 0.1.0

Current artifact inspected: `architect/library/cores/video-editing-post-production/0.1.0/professional-model.md`.

### High-priority findings

| Competency | Hard decision | Material knowledge dependency | Current availability | Packaging mode | Gap/risk | Required action/eval |
|---|---|---|---|---|---|---|
| VE-03 Timing/rhythm/continuity | Choose cut structure that preserves comprehension and intended rhythm | perceptual/editorial cues, continuity patterns, genre/context judgment | expert cues in core | EMBED_CORE + REFERENCE_MODULE | craft depth is partly tacit; text module may induce formulaic editing | prefer calibrated contrastive cases/reference literacy and rendered comparative eval over rigid procedure |
| VE-04 Truth preservation | Decide whether transformation changes evidentiary meaning | provenance, semantic effect of crop/retime/reorder/composite | strong invariant in core | EMBED_CORE + PROCEDURAL_MODULE | edge cases require explicit transformation/provenance review | package a small provenance/truth review procedure if adversarial edit cases expose misses |
| VE-05 Picture finishing | Diagnose color/exposure/artifact problem | color-management concepts, transforms, clipping/artifact diagnosis | principles only | REFERENCE_MODULE + TOOL_BACKED + ESCALATE | base-model terminology can mask inability to inspect/measure real media | require actual scopes/metadata/frame inspection where runtime supports it; compact reference for color pipeline; specialist escalation beyond scope |
| VE-06 Audio | Decide whether mix is intelligible and delivery-safe | loudness/true peak measurement, sync, artifact diagnosis, target-specific requirements | principles plus live-target rule | REFERENCE_MODULE + TOOL_BACKED + LIVE_RESEARCH | measurements cannot be replaced by prose; target values can vary | prioritize tool-backed measurement + target-spec live verification; reference for interpretation, not static universal targets |
| VE-07 Captions/graphics | Validate timed communication | timing/readability, language correctness, safe placement, destination constraints | strong checks in core | PROCEDURAL_MODULE + TOOL_BACKED + LIVE_RESEARCH | manual/model review can miss timing/occlusion | use render/timeline inspection and current destination constraints; procedure may coordinate checks |
| VE-09 Conform/versioning | Preserve variant identity and reproducibility | hashes, asset/timeline IDs, transforms, export settings | explicit in core | PROCEDURAL_MODULE + TOOL_BACKED | prose alone does not create lineage | tool-backed manifest/ledger is preferable to more instructions |
| VE-10 Delivery | Produce technically valid destination master | codec/container/color/audio/platform specifications | live boundary explicit | LIVE_RESEARCH + TOOL_BACKED + REFERENCE_MODULE | static export recipes will decay | keep platform specs live; tool-backed media probe/validation; stable codec/color concepts may live in reference |
| VE-11 Artifact-first QC | Determine whether exported artifact actually passes | decode/metadata/frame/audio/perceptual inspection | strong workflow in core | PROCEDURAL_MODULE + TOOL_BACKED | core correctly demands observation, but runtime capability may be absent | highest-priority runtime capability: deterministic media QC + perceptual inspection contract; hard fail if artifact not observable |

### Video-editing decision

The principal gap is not "more editing facts." It is the bridge between craft knowledge and observable media. VE-11, VE-05, VE-06 and VE-10 are strongly **TOOL_BACKED**. Adding prose without decode/frame/audio/metadata observability would create false confidence. For VE-03, contrastive examples and calibrated comparative review are more defensible than a rigid pacing recipe.

## Cross-core architecture findings

1. Existing cores already separate stable vs live knowledge reasonably well; do not replace this with a document dump.
2. The missing layer is selective **operational depth + runtime availability proof**, not generic source collection.
3. Knowledge packaging must be evaluation-led. The existence of a plausible missing module is a hypothesis until hard-case/ablation evidence shows material benefit.
4. Deterministic/tool-backed knowledge should not be rewritten as prose merely to fit a skill format.
5. Creative/tacit knowledge often needs contrastive cases, direct artifact inspection and calibrated human/expert judgment rather than more rules.
6. Volatile platform/legal/specification knowledge should remain live with freshness and authority gates.

## Red-team

### Senior practitioner

Likely criticism: the architecture could become academically neat but operationally slow, with agents loading modules instead of solving work. Repair: require each module to earn context/coordination cost through observed capability benefit and progressive disclosure.

### Educator / competency assessor

Likely criticism: a module inventory does not prove competence and can encourage teaching-to-the-test. Repair: novel work samples, ablation, holdouts, and graders tied to observable decisions rather than module vocabulary.

### Hiring manager

Likely criticism: an agent may cite the right framework but still fail on messy data, incomplete assets, deadlines and tool failures. Repair: evaluations must include degraded inputs, missing dependencies, conflicting evidence, real artifacts, and recovery/escalation behavior.

## Next implementation order

1. Integrate Knowledge Packaging Audit into Agent Architect workflow — done in `architect/SKILL.md`.
2. Treat existing cores as `UNPROVEN` for operational-depth claims not already behaviorally demonstrated; do not revoke unrelated qualification claims without evidence.
3. Build the first targeted hard-case eval around Paid Media PM-04 experimentation and Video Editing VE-11 artifact-first QC.
4. Only after an observed failure or clear executable dependency, add the minimum procedural/reference/tool package needed.
5. Re-run affected regression and compare against core-only behavior; reject modules that add cost without material gain.
