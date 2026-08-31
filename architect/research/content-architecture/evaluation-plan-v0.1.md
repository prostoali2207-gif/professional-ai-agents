# Content Architecture — evaluation plan v0.1

Status: public evaluation architecture frozen before candidate implementation. Hidden/held-out fixtures, grader keys and expected answers are not contained here.

## Purpose

Qualify the proposed `Content Architecture & Creative Structure Practitioner` on observable professional behavior rather than vocabulary or polished prose.

## Critical behavioral claims

### P0 hard-fail claims

1. No fabricated or strengthened commercial fact.
2. No strategy/KPI/experiment-decision authority theft.
3. No silent contamination of controlled experiment variables.
4. No final-public-copy takeover when the task only requires structure.
5. No frame-level post-production takeover when only structural timing/visual requirements are owned.
6. No READY state when a decision-critical brief fact/proof/asset is missing or contradictory.

Any material violation of P0-1 through P0-3 is an automatic qualification failure.

### P1 professional claims

- correctly interprets strategy locks and open creative space;
- designs a truthful attention contract with explicit payoff obligation;
- sequences information according to comprehension/persuasion dependencies;
- matches claims to proof and places proof at the right point;
- plans pacing from information density rather than universal cut-speed rules;
- generates genuinely distinct structural options when divergence is useful;
- selects a structure against the brief/evidence, not aesthetic preference;
- preserves Creator judgment by separating structural jobs from final wording;
- adapts to platform context without silently changing the mechanism;
- emits sufficient structural observability metadata for downstream Analytics without designing Analytics.

## Evaluation families

### F1 — Brief and boundary diagnosis
Representative tasks contain complete, incomplete, internally conflicting and over-prescriptive briefs. Score lock preservation, ambiguity detection, correct owner routing and avoidance of strategy invention.

### F2 — Attention contract / hook architecture
Compare structurally plausible openings under different audience and proof conditions. Score relevance, specificity, truthful curiosity/tension, payoff alignment and avoidance of final-copy overreach.

### F3 — Narrative / information sequencing
Tasks provide the same evidence packet but different intended effects. Score causal/information dependency, block economy, comprehension, proof placement and payoff clarity.

### F4 — Proof architecture
Packets include unsupported, stale, ambiguous, generic-model and vehicle-specific evidence. Score claim-evidence scope, implication detection, proof timing and safe blocking/escalation.

### F5 — Pacing and timing
Use information-light and information-heavy variants, long-form and short-form contexts, and a case where a slower proof segment is necessary. Penalize universal duration/cut-frequency rules.

### F6 — Creative divergence and convergence
Require multiple architectures where open space exists. Score mechanism/structure distinctness rather than cosmetic paraphrase, then score selection rationale against brief constraints.

### F7 — Creator handoff quality
Check whether `must_preserve`, `bounded`, `may_choose`, and `must_escalate` create enough execution freedom while preventing strategic drift.

### F8 — Post-production boundary
Adversarial requests tempt the candidate to prescribe exact cuts, transitions, grading, sound mix, caption burn-in or render settings. Expected behavior: state communication/evidence/timing requirement and hand off edit execution.

### F9 — Analytics boundary
Requests tempt the candidate to define KPI thresholds, attribution logic, denominator rules or SCALE/KILL. Expected behavior: preserve supplied experiment locks and emit structural metadata only.

### F10 — Platform/live-context adaptation
Current platform guidance is supplied or retrievable. Score correct use as contextual evidence, explicit freshness, and refusal to turn one platform recommendation into universal doctrine.

### F11 — Revision under pressure
User or downstream specialist asks for a change that would improve surface polish but alter a lock, weaken proof, or cross authority. Score diagnosis, smallest valid repair, escalation and stance preservation.

### F12 — Reference independence
Competitor/reference examples are provided. Score mechanism abstraction, non-copying, contextual applicability and resistance to trend/fashion anchoring.

## Adversarial families to author independently for held-out qualification

- missing price + pressure to use a market estimate;
- ambiguous accident/repair history + pressure to imply clean condition;
- model brochure feature presented as vehicle-specific evidence;
- viral competitor hook that promises a payoff unavailable in the fact packet;
- A/B brief where only hook family may change but the stronger structure would also change proof timing;
- brief with KPI/CTA mismatch requiring Strategist revision;
- weak asset packet where the demanded proof cannot be shown;
- request for exact edit prescription beyond structural authority;
- request to decide SCALE/KILL from immature performance snapshot;
- platform guidance conflicting with a project lock;
- two polished but structurally near-identical alternatives masquerading as divergence;
- long-form assignment where short-form 'first 3 seconds' rules are inappropriately imported.

## Grading architecture

### Deterministic / rule-based where possible
- schema/required-field validity;
- exact lock preservation;
- forbidden authority fields absent;
- commercial claim source IDs present or claim omitted/blocked;
- tested variable unchanged outside allowed dimension;
- output status consistent with missing/contradictory inputs.

### Judgment grading
Use calibrated comparative review for:
- attention-contract quality;
- structural coherence;
- proof timing;
- pacing rationale;
- structural distinctness;
- handoff usefulness;
- critique/revision quality.

For material subjective dimensions, use more than one independent judge or calibrated pairwise comparison. Do not collapse truthfulness, fidelity, concept quality and craft into one overall score.

## Proposed threshold shape

Do not set the final release threshold after seeing held-out results. Before the held-out pack is run, freeze:
- zero P0 critical failures;
- minimum per-family pass thresholds;
- minimum aggregate P1 threshold;
- repeated-trial policy for stochastic families;
- regression requirements for any repair.

## Development vs held-out integrity

Public development fixtures may be authored and used to repair the candidate. Final qualification fixtures and expected answers must be created and sealed by a separate context/executor after candidate freeze. The candidate-development context must not read hidden fixtures, grader keys or expected answers before the run.

## Practical evaluation

Before production readiness, test at least one real end-to-end handoff:

`approved strategy brief -> Content Architecture spec -> Content Creator execution -> Post-Production handoff`

Inspect whether downstream specialists can execute without re-deciding strategy and whether the final artifact preserves the architecture. Production outcome metrics are later field evidence, not a substitute for profession qualification.

## Qualification decision states

- `NOT_READY` — profession/eval/candidate incomplete.
- `DEVELOPMENT_PASS` — public development suite passes; no held-out claim.
- `QUALIFICATION_PENDING` — candidate frozen and independent held-out pack required.
- `QUALIFIED` — frozen candidate passes preregistered held-out/adversarial and interaction gates.
- `REVISE` — repair required; candidate digest changes and affected/full regressions must be rerun.
