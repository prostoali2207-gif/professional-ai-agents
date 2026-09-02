# Conversion Strategy & Landing Page Architecture — evaluation architecture v0.1

Date: 2026-09-02
Status: pre-candidate evaluation construct; thresholds not yet calibrated/frozen
Issue: #246
Research basis: `architect/research/conversion-strategy-landing-architecture/reuse-decision-2026-09-02.md`

## 1. Evaluation purpose

This suite must distinguish a real conversion strategist from:
- a fluent tactic recommender;
- a long-form sales-page generator;
- a copywriter using strategy vocabulary;
- a generic UX critic;
- a competitor-pattern copier;
- an agent that optimizes clicks/submits while damaging lead quality;
- a cautious agent that says `measure first` even when the evidence is already sufficient.

Passing requires observable professional decisions under realistic ambiguity, not recall of CRO terminology.

## 2. Construct families

### DIAG — Commercial root-cause diagnosis
Tests whether the practitioner:
- identifies the earliest material failure layer;
- distinguishes landing, traffic-message, offer/value, proof/trust, friction, technical, CRM/lead-quality and downstream causes;
- states evidence/confidence and plausible alternatives;
- returns `PAGE CHANGE`, `MEASUREMENT FIRST`, `OUTSIDE LANDING`, or `NO CHANGE` correctly.

Adversarial pattern: a low-conversion page where the supplied stakeholder explanation is wrong.

### ARCH — Decision-information and page architecture
Tests whether the practitioner:
- chooses compact, longer sequential, progressive-disclosure or another justified structure from information need and commitment/trust context;
- treats page length as an output rather than a doctrine;
- protects first-screen relevance and primary-action clarity;
- avoids adding content whose attention cost exceeds decision value.

Contrastive requirement: same surface category, different decision risk/entry context -> different architecture can be correct.

### OFFER — Offer/value versus presentation
Tests whether the practitioner:
- detects when the offer/value is the responsible layer;
- refuses to solve weak/unverified value through claim inflation, urgency, testimonials or visual polish;
- specifies what commercial decision is required upstream.

### PROOF — Proof architecture and evidence integrity
Tests whether the practitioner:
- maps proof to exact claim/objection/risk;
- distinguishes process evidence, capability evidence, result evidence, authority evidence, popularity evidence and current business facts;
- rejects weak proxies, stale evidence, irrelevant logos and overbroad case extrapolation;
- chooses appropriate proof strength, timing, density or omission.

### TRUST — Objection/anxiety/trust/commitment sequencing
Tests whether the practitioner:
- distinguishes friction from anxiety and real offer mismatch;
- prioritizes material objections instead of generic FAQ completeness;
- scales trust requirements with the requested commitment;
- preserves visitor agency.

### COMMIT — CTA, qualification and lead-quality judgment
Tests whether the practitioner:
- chooses the smallest useful next commitment;
- evaluates qualification cost versus downstream utility;
- protects qualified lead rate, CRM actionability, manager load and deeper business outcomes;
- can both remove unnecessary friction and preserve necessary friction.

### TRANSFER — Competitor/reference mechanism transfer
Tests whether the practitioner:
- models the competitor/reference feature as mechanism -> causal hypothesis -> applicability -> evidence -> risk;
- distinguishes inspiration/pattern prevalence from evidence of efficacy;
- returns TAKE / ADAPT / TEST / REJECT appropriately.

### MEASURE — Hypothesis and experimentation handoff
Tests whether the practitioner:
- states evidence-backed problem, mechanism, target behavior, primary outcome and guardrail;
- avoids guaranteed lift;
- does not improvise statistical/causal analysis outside the reused measurement core;
- hands a decision-useful experiment contract to `growth-experimentation-measurement@1.2.0`.

### BOUNDARY — Profession routing and handoff integrity
Tests whether the practitioner preserves the boundaries of:
- Market Intelligence;
- Conversion Messaging;
- UX;
- Visual Design;
- Experimentation/Measurement;
- Sales;
- Frontend/QA;
- Legal/business policy.

The handoff must be specific enough to execute while not taking over the downstream craft.

### INTEGRITY — Non-deceptive persuasion and autonomy
Tests pressure to use:
- fake scarcity/urgency;
- unsupported social proof;
- hidden material terms;
- manipulative defaults;
- deceptive comparison;
- claim implication stronger than evidence.

### E2E — Authentic mixed-evidence strategy work
A full task bundle should include:
- commercial objective and constraints;
- acquisition/entry context;
- current page or structured page description;
- first-party funnel/CRM evidence;
- customer/manager evidence where available;
- competitor/reference examples;
- incomplete/uneven proof;
- organization facts/unknowns.

The practitioner must diagnose, research only material gaps, choose or decline architecture change, produce handoffs and attach measurement only where justified.

## 3. Evidence-centered claim map

| Competency claim | Observable evidence | Task mechanism | Grader/verifier |
|---|---|---|---|
| Diagnoses before prescribing | layer diagnosis + evidence/confidence + alternative cause | misleading stakeholder premise | calibrated strategy judge + structural fields |
| Chooses architecture contextually | architecture changes when mechanism-relevant context changes | blind contrastive pair | pair-consistency judge |
| Uses proof within evidence | proof-to-claim/objection mapping; rejects overclaim | mixed proof packet | judge + hard-fail detector |
| Protects deeper business value | explicit primary outcome + lead-quality/business guardrail | high-submit/low-quality case | deterministic metric consistency + judge |
| Transfers patterns validly | mechanism/applicability record; no prevalence-as-proof | competitor-copy pressure | adversarial judge |
| Knows when not to act | justified NO CHANGE / MEASUREMENT FIRST | attractive but under-evidenced redesign opportunity | judge |
| Preserves professions | exact routing and bounded handoffs | mixed strategy/copy/UX/visual/stats task | structural route checks + judge |
| Avoids deceptive persuasion | refuses/manages fake urgency/proof/hidden terms | stakeholder pressure | zero-tolerance hard-fail |

## 4. Required contrastive pairs

Held-out authoring must include blind pairs for at least:

1. `ARCH`: same offer/category, different commitment/trust/traffic context.
2. `PROOF`: same objection, valid evidence in one case and only weak/irrelevant proxy evidence in the other.
3. `COMMIT`: same apparent field friction, operationally necessary qualification in one case and unnecessary collection in the other.
4. `TRANSFER`: same competitor tactic, compatible context in one case and incompatible mechanism assumptions in the other.
5. `DIAG`: same low conversion symptom, landing responsible in one case and downstream/measurement responsible in the other.

Pair grading evaluates directional judgment consistency, not vocabulary similarity.

## 5. Proposed hard failures

Names are construct-level placeholders until preregistration normalizes identifiers.

- `MATERIAL_FABRICATION`
- `DECEPTIVE_PERSUASION`
- `COMPETITOR_PATTERN_AS_EFFICACY`
- `GUARANTEED_CONVERSION_LIFT`
- `SHALLOW_METRIC_OVERRIDE`
- `UNAUTHORIZED_STRATEGY_SCOPE`
- `EVIDENCE_REQUIRED_BUT_IGNORED`

A weak but truthful architecture choice is normally a P1 professional-quality failure, not automatically a P0 hard failure.

## 6. Grading architecture

### Deterministic / structural grading
Use where mechanically observable:
- decision state and required evidence fields;
- unsupported guaranteed-lift wording;
- explicit fake scarcity/urgency or fabricated evidence when detectable;
- handoff owner/schema presence;
- pair output direction invariants;
- missing primary outcome/guardrail when required.

### Calibrated professional judgment
Required for:
- root-cause quality;
- offer versus presentation distinction;
- page architecture sufficiency;
- proof/objection fit;
- trade-off quality;
- mechanism-transfer applicability;
- appropriateness of NO CHANGE / MEASUREMENT FIRST;
- usefulness and boundedness of handoffs.

A single uncalibrated scalar LLM grader is insufficient. Before scored qualification:
1. create calibration cases with clear PASS, clear P0/P1 FAIL and difficult boundaries;
2. obtain independent reference judgments;
3. run judges blind;
4. inspect disagreement by criterion;
5. revise rubric before judge prompt;
6. retest on held-out calibration cases;
7. freeze judge configuration only after acceptable construct agreement.

For critical subjective families use two independent judges or calibrated comparative judgment where feasible.

## 7. Anti-gaming design

Include:
- polished competitor pages that are inappropriate for target context;
- unattractive pages whose actual failure is traffic/CRM/downstream;
- familiar CRO tactics with insufficient causal evidence;
- style/copy variations preserving the same underlying decision;
- cases where the correct answer is intentionally short and conservative;
- verbose tactic-heavy answers that should fail despite professional language;
- explicit business pressure to optimize raw submits while qualified leads collapse;
- missing decision-critical evidence where the practitioner must stop rather than decorate uncertainty.

E2E grading must verify use of supplied first-party evidence; generic framework recitation cannot pass.

## 8. Development / held-out / practical separation

### Public development
Representative fixtures for every family. Public failures may drive causal candidate repair and targeted regression.

### Independent held-out
Fresh authoring after candidate freeze. Evaluator must be isolated from candidate content and must not reuse public fixture wording. Candidate must never inspect the hidden corpus, expected answers, grader rationale or author prompts as a collection.

### Practical release gate
After held-out semantic PASS, run at least three distinct work samples:
1. automotive part-request landing, Spline-like but not copied from current implementation;
2. service/appointment landing with different trust/proof/commitment structure;
3. higher-consideration information-heavy offer where a longer or progressively disclosed path may be justified.

This is required to detect overfitting to automotive minimalism or infoproduct long-form patterns.

## 9. Calibration before numeric threshold freeze

Do not invent family floors or aggregate thresholds now.

Calibration set must include:
- clear professional passes;
- clear P0/P1 failures;
- genuine professional-disagreement cases;
- concise NO CHANGE answers that should pass strongly;
- verbose tactic catalogs that should fail;
- contrastive pairs whose decision direction is known from case facts.

Only after judge agreement and failure-detection behavior are inspected may counts, floors, pair rules and aggregate threshold be preregistered.

## 10. Candidate repair policy

`FAIL -> classify failure -> root cause -> repair responsible professional layer -> add/target regression -> rerun affected public tests -> only then consider new freeze`.

Do not patch exact fixture phrases into the candidate. If failure is evaluator ambiguity or invalid construct, repair the evaluator rather than the practitioner.

## 11. Release claim ceiling

Qualification may establish only that the exact frozen core demonstrates the tested strategy/judgment behaviors under the qualifying runtime, tools, evidence and authority conditions.

It does **not** establish that any recommended landing change will improve real-world conversion. Actual lift is downstream empirical evidence and must be handled by experimentation/measurement or deployment data.

## 12. Phase 11 red-team before candidate authoring

### Senior practitioner perspective
Risk: the role becomes a checklist-driven CRO auditor.
Repair requirement: every material recommendation must expose mechanism, applicability conditions, competing explanation and evidence needed; architecture may legitimately remain unchanged.

Risk: `short vs long` becomes a false binary.
Repair requirement: include progressive disclosure, sequencing, conditional information and commitment design as alternatives.

Risk: proof architecture becomes "add testimonials".
Repair requirement: evidence type must be claim-scoped; process/capability/result/popularity/authority evidence are not interchangeable.

### Educator / competency-assessor perspective
Risk: candidate can memorize MECLABS/NNG vocabulary and score well.
Repair requirement: use contrastive cases, misleading premises, missing evidence and opposite-decision pairs where terminology does not reveal the answer.

Risk: high aggregate score hides one dangerous persuasion behavior.
Repair requirement: zero-tolerance integrity hard fails and family-level critical gates.

### Hiring-manager perspective
Risk: output sounds strategic but cannot be handed to a real team.
Repair requirement: E2E artifact must contain decision, evidence, must-preserve constraints, exact downstream owner and verification/measurement requirement.

Risk: candidate creates endless research and no decision.
Repair requirement: test research stopping and reversible decision sufficiency; unjustified paralysis is a professional failure.

### Evaluation-science perspective
Risk: graders reward verbosity/style.
Repair requirement: calibration explicitly contains concise expert passes and verbose tactic-heavy failures.

Risk: same judge authors expected answer and grades candidate.
Repair requirement: separate author/reference/judge responsibilities for held-out and use blind evaluation.

### Systems/composition perspective
Risk: strategy overlaps with Messaging, UX, Analytics and Sales, causing duplicate decisions.
Repair requirement: boundary tests and stable handoff schema; reuse qualified research/measurement cores instead of copying their methods.

## 13. Pre-candidate verdict

The construct is sufficiently defined for **candidate authoring to begin**, but no candidate may be frozen or qualified until public development fixtures and calibration materials are created and reviewed.
