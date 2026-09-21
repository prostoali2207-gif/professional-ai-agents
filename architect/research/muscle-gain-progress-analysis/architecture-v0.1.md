# Muscle Gain Progress Analysis — architecture v0.1

Status: pre-SKILL architecture and evidence record.

## Profession reconstruction and reuse decision

### Real professional model
The target is not a weight tracker. It is a longitudinal resistance-training progress analyst combining:
- resistance-training / strength-and-conditioning monitoring;
- hypertrophy and strength adaptation interpretation;
- longitudinal measurement and trend analysis;
- body-measurement / body-composition measurement interpretation;
- uncertainty-aware intervention review.

The accountable output is a bounded decision: what changed, how certain that conclusion is, whether a plateau is supported, whether a previous intervention worked, and whether any single variable should change now.

### Boundaries
Included: healthy-adult muscle-gain and strength progress analysis, longitudinal signal construction, measurement-comparability audit, intervention review, decision support.
Excluded: medical diagnosis/treatment, rehabilitation, injury management, eating-disorder treatment, PED/drug guidance, clinical nutrition, autonomous modification of external records.

### Inventory
Repository Professional Core Library candidates inspected:
- growth-experimentation-measurement@1.2.0;
- market-competitive-intelligence@1.0.0;
- paid-media-performance-marketing@1.0.0;
- all other catalog entries.

No sports-science, strength-and-conditioning, hypertrophy-monitoring or body-composition professional core exists in the current catalog.

### Formal reuse decision
**growth-experimentation-measurement@1.2.0 — ADAPT capability, REJECT whole-core reuse.**
Reusable invariants: measurement integrity before inference, missing/invalid state separation, fixed decision question, causal-vs-operational distinction, bounded inconclusive verdict. Gap: its qualified construct concerns controlled growth experiments, not human training adaptation.

**market-competitive-intelligence@1.0.0 — ADAPT capability, REJECT whole-core reuse.**
Reusable invariants: comparability, provenance, longitudinal collection-drift control, non-observation discipline. Gap: market evidence is not physiological/performance monitoring.

**Agent Architect runtime-state-memory-context — REUSE methodology.**
The state lifecycle, provenance, supersession and checkpoint rules transfer because they are domain-independent architecture.

**Sports/training domain — BUILD NEW applied domain skill.**
A new generic framework is not created. Domain judgment remains local to this applied skill.

Inherited qualification does not transfer. The assembled skill requires its own practical, adversarial and later independent qualification evidence.

## Authoritative evidence / source base

Material evidence is maintained in `source-register-v0.1.md`. Main evidence classes:
- current ACSM resistance-training position stand for healthy adults;
- peer-reviewed resistance-training monitoring literature;
- RIR accuracy/reliability evidence;
- DXA/hydration/glycogen body-composition measurement evidence;
- physique/body-composition measurement reliability literature;
- energy-surplus / off-season bodybuilding reviews for qualified rate-of-gain context only.

No source supports treating a single weight, single workout, single photo or single body-composition result as proof of tissue adaptation.

## Competency / evidence map

| ID | Competency | Observable capability | Critical cues | Failure | Verification |
|---|---|---|---|---|---|
| PA-01 | Longitudinal state reconstruction | Retrieves prior comparable period, active intervention and expected effect | time, protocol, supersession | invents history | stateful fixtures |
| PA-02 | Measurement integrity | Separates observed/missing/invalid/noncomparable | protocol, method, units, hydration | missing=zero | deterministic cases |
| PA-03 | Body-mass signal | Distinguishes daily noise from trend | repeated standardized weights, water/glycogen context | tissue claim from one point | water-spike/metamorphic cases |
| PA-04 | Performance signal | Compares like with like | exercise, machine, ROM, effort, phase | false comparison | variant/ROM fixtures |
| PA-05 | Effort interpretation | Uses RIR/RPE as contextual noisy measure | load, rep range, proximity to failure | treats estimate as exact | RIR adversarial case |
| PA-06 | Anthropometry/body composition | Applies protocol/method/error gate | method, operator, hydration, MDC/TEM | cross-method overclaim | hydration/MDC fixtures |
| PA-07 | Photo interpretation | Gates on lighting/pose/angle/distance | capture protocol | visual kilos/bodyfat estimate | bad-photo fixture |
| PA-08 | Multi-signal synthesis | Preserves conflicts and claim ceilings | independent outcomes vs proxies | averages conflict away | contradictory metrics |
| PA-09 | Plateau judgment | Distinguishes false vs supported plateau | duration, trend, comparable outcomes, adherence | one flat week=plateau | plateau pair |
| PA-10 | Rate-of-gain judgment | Uses explicit target first; contextual literature second | target provenance, trend, training age | universal optimum | rate fixtures |
| PA-11 | Intervention causality | Freezes hypothesis/expected effect and reviews later | prior change, controlled variables | post-hoc story | stateful intervention fixture |
| PA-12 | Minimal-change decision | Changes one key variable unless necessary | uncertainty, reversibility | change everything | pressure fixture |
| PA-13 | Boundary/escalation | Stops at medical/rehab boundary | symptoms, injury, disordered eating, PED | diagnosis | boundary fixture |

## Knowledge packaging

EMBED_CORE:
- signal-vs-noise invariants;
- comparability rules;
- plateau/rate claim ceilings;
- intervention-review logic;
- medical boundary.

PROCEDURAL_MODULE:
- `procedures/decision_reference.py` for critical deterministic branches.

REFERENCE_MODULE:
- this architecture record and source register.

TOOL_BACKED:
- arithmetic/trends;
- schema validation;
- exact exercise grouping;
- photo metadata/inspection when available.

LIVE_RESEARCH:
- device/method-specific measurement error or validity;
- material current consensus changes;
- thresholds not already established in the source register.

ESCALATE:
- medical/rehabilitation/clinical/PED issues.

## Judgment and decision model

### Signal construction
Do not collapse data into one score. Build independent channels:
1. body-mass trend;
2. comparable performance trend;
3. standardized anthropometry/body composition;
4. standardized visual evidence;
5. training dose/effort;
6. nutrition/recovery/context.

Outcome channels outrank exposure proxies for claims of adaptation.

### Evidence hierarchy inside a case
1. repeated comparable direct outcome observations;
2. repeated standardized proxy/measurement observations with known limitations;
3. subjective/context measures;
4. isolated/noncomparable observations.

This is not a universal scientific hierarchy; it is a decision rule for this skill's longitudinal task.

### Plateau
A plateau is an inference, not a flat data point.
- FALSE_PLATEAU when the current raw observation looks flat but comparable aggregate trend or another valid relevant outcome remains positive, or a measurement artifact explains the stall.
- PLATEAU_SUPPORTED only when repeated comparable relevant outcomes show no meaningful positive signal after adequate exposure/adherence and unresolved transient/measurement confounding is absent.
- INSUFFICIENT_DATA when duration/coverage/comparability cannot support the inference.
No universal physiological duration threshold is encoded.

### Rate of gain
1. Prefer an explicit user/program target with provenance.
2. If none exists, a 0.25–0.5% bodyweight/week reference may be discussed only as a bodybuilding-specific contextual reference for novice/intermediate natural bodybuilders, with more conservative gain for advanced athletes.
3. Do not convert that reference into a universal hard threshold or infer tissue composition from rate alone.

### Conflicting indicators
Conflicts lower the claim ceiling rather than being averaged away.
- weight up + performance down -> CONFLICTING_SIGNALS unless a resolved explanation supports a narrower conclusion;
- performance up + weight flat -> performance progress is supported; hypertrophy remains unresolved;
- nonstandardized photos cannot overrule standardized measures;
- hydration-confounded body-composition change is downgraded.

### Causal attribution
Before intervention, freeze:
`variable -> rationale -> expected metric direction -> controlled variables -> review condition -> confounders -> rollback/escalation`.

After intervention, compare expected to observed. Do not rewrite the expected outcome after seeing data.

## Longitudinal state / memory architecture

Required state classes:
- working context: current decision packet;
- session state: current analysis progress and unresolved checks;
- episodic memory: period summaries and intervention outcomes;
- semantic memory: stable user-specific measurement protocols/targets only when validated and useful;
- procedural memory: this skill and procedures;
- external source of truth: raw training/weight/measurement records.

Persistent write gate requires provenance, confidence, scope, expected future use and contradiction check.

Durable state:
- goal/target and provenance;
- protocol versions and supersession;
- period summaries;
- intervention contracts;
- expected effects frozen at intervention time;
- observed follow-up;
- uncertainties;
- next review condition.

Never persist an inferred diagnosis or convert one anecdote into durable fact.

Contradiction handling:
- explicit authoritative correction supersedes current state while preserving useful history;
- protocol change creates a new comparability segment;
- unresolved conflicting sources remain contested, not silently overwritten.

Checkpoint/resume must preserve objective, current period, active intervention, prior expectations, unresolved uncertainty and next decision condition.

If structured persistent state is unavailable, the skill must declare bounded single-session behavior and not claim longitudinal attribution.

## Procedural capabilities

P1 ingest/normalize -> preserve units, timestamps, method, exercise identity, missingness.
P2 comparability audit -> segment protocol/exercise changes before trend inference.
P3 trend construction -> aggregate repeated observations and retain raw dispersion.
P4 performance normalization -> compare exact/meaningfully equivalent tasks with effort context.
P5 measurement-error gate -> apply supplied/verified TEM/MDC/reliability where available; never invent.
P6 photo comparability gate -> lighting/pose/angle/distance/pump/clothing.
P7 multi-signal synthesis -> preserve disagreement.
P8 intervention review -> expected vs observed.
P9 minimal-change proposal -> one key variable by default.
P10 state write/checkpoint -> validated summary + uncertainty + next review.

## Evaluation design

Development/practical cases are preregistered in `architect/evaluation/muscle_gain_progress_analysis/fixtures-v0.1.json`.
Critical hard fails:
- tissue inference from one observation;
- false plateau from too-short/noncomparable evidence;
- missing=zero;
- ignored measurement/exercise protocol change;
- universal rate/plateau threshold;
- body-composition overclaim despite hydration/method-error confound;
- multiple key changes from user pressure;
- post-hoc rewriting of intervention expectation;
- medical diagnosis.

Required user-requested cases:
water-weight spike; single bad workout; false plateau; real plateau; bad photos; contradictory metrics; missing data; too-short period; pressure to change everything; weight up/performance down; performance up/weight flat.

Additional cases:
hydration-confounded DXA; change below method resolution; explicit rate above target; rate below target/no performance progress; rate below target/performance progress; intervention follow-up; medical boundary.

Metamorphic checks hold the decision constant under irrelevant wording/confidence changes and flip only decision-relevant comparability/trend facts.

## Red-team and pre-SKILL gate

Question asked exactly:
**What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?**

Senior-practitioner findings and repairs:
- missing exercise comparability -> added machine/ROM/variant gate;
- volume-load overinterpretation -> explicitly classified as input proxy;
- body-composition hydration confound -> added protocol/error gate and executable regression;
- intervention history without expected-effect freeze -> added prospective contract.

Educator/assessor:
- “knows trends” was not observable -> competencies rewritten as elicitable decisions;
- plateau lacked contrastive cases -> added false/real/short-window cases.

Hiring-manager:
- skill could create churn by changing many variables -> one-variable default + pressure hard-fail;
- output lacked next evidence -> next-review condition required.

Evaluation scientist:
- same visible fixture set cannot support independent qualification -> readiness ceiling kept below T1;
- exact-string static checks can misclassify equivalent behavior -> static checks test semantic anchors, not one arbitrary phrase.

State/security:
- stale protocol could contaminate later comparison -> protocol version/supersession required;
- missing state could be hallucinated -> bounded single-session fallback.

Pre-SKILL gate: PASS for construction. Profession, evidence, competencies, judgment, procedures, state, boundaries, eval design, red-team and production-learning path exist before final SKILL assembly.

## Production learning

Capture:
- user/practitioner substantive corrections;
- false plateau/false progress decisions;
- intervention changes that fail expected effects;
- measurement/protocol surprises;
- state corruption/supersession failures;
- boundary misses.

A confirmed new failure class becomes a regression before durable rule change. T2/T3 claims require the repository's professional-trust-validation gates.
