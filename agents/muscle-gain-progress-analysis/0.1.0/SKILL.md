# Muscle Gain Progress Analysis

Version: 0.1.0-candidate
Status: development candidate; local practical/regression gate passed; not T1-qualified

## Mission

Turn longitudinal muscle-gain and resistance-training data into evidence-bounded progress decisions. Distinguish real adaptation from measurement noise, transient state and non-comparable observations. Track prior interventions and determine whether they produced the expected effect before proposing further changes.

This is an analysis/decision-support skill for healthy-adult hypertrophy and strength goals. It is not a medical, rehabilitation, diagnostic or clinical-nutrition system.

## Architecture and provenance

Profession/reuse decision:
`architect/research/muscle-gain-progress-analysis/architecture-v0.1.md#profession-reconstruction-and-reuse-decision`

Evidence:
`architect/research/muscle-gain-progress-analysis/architecture-v0.1.md#authoritative-evidence--source-register`

Competency map:
`architect/research/muscle-gain-progress-analysis/architecture-v0.1.md#competency--evidence-map`

Judgment:
`architect/research/muscle-gain-progress-analysis/architecture-v0.1.md#judgment-and-decision-model`

State:
`architect/research/muscle-gain-progress-analysis/architecture-v0.1.md#longitudinal-state--memory-architecture`
and `schemas/longitudinal-state.schema.json`

Procedures:
`architect/research/muscle-gain-progress-analysis/architecture-v0.1.md#procedural-capabilities`
and `procedures/decision_reference.py` as a narrow executable critical-invariant reference, not a complete physiology model.

Reuse decision: adapt qualified measurement-integrity/decision-sufficiency patterns from `growth-experimentation-measurement@1.2.0`, comparability/provenance patterns from `market-competitive-intelligence@1.0.0`, and Agent Architect state methodology. Do **not** inherit their domain qualification. The sports/training domain model is new.

## Required inputs

Accept whatever is available, but explicitly mark missingness:
- body mass observations with dates and weighing conditions when known;
- training log: exercise/variant, equipment, load, reps, sets, ROM/technique constraints when relevant;
- RIR/RPE or other effort measures;
- training volume/frequency and recent program changes;
- body measurements/body-composition results with method/protocol;
- progress photos and capture conditions;
- nutrition/adherence context;
- recovery/sleep/stress/illness/travel context;
- subjective state;
- prior period summaries, interventions, expected effects and unresolved uncertainties.

Missing inputs are not zero and do not authorize a fabricated conclusion.

## Evidence states

Raw observation state:
`OBSERVED | MISSING | INVALID | NONCOMPARABLE | ESTIMATED | USER_REPORTED`

Interpretation state:
`SUPPORTED | PLAUSIBLE | WEAK | UNKNOWN | CONTESTED`

Comparability:
`COMPARABLE | PARTIAL | NONCOMPARABLE | UNKNOWN`

Primary verdict:
`PROGRESS | NO_MATERIAL_CHANGE | FALSE_PLATEAU | PLATEAU_SUPPORTED | CONFLICTING_SIGNALS | INSUFFICIENT_DATA | ESCALATE`

Action:
`HOLD | GATHER_DATA | CHANGE_ONE_VARIABLE | REVIEW_PROGRAM | ESCALATE`

## Core workflow

1. **Load longitudinal state.** Retrieve the current goal, previous relevant period, active intervention, expected effect, protocol versions and open uncertainties. If state is unavailable, say so; do not invent history.
2. **Ingest without flattening.** Preserve source, timestamp, units, method, exercise identity, missingness and protocol.
3. **Audit comparability first.** Identify measurement/exercise/protocol changes before looking for a trend.
4. **Separate inputs from outcomes.** Volume/calories/frequency are exposures; performance/body trend/standardized dimensions are outcomes; RIR/RPE/recovery are context; hydration/glycogen/method changes can confound.
5. **Construct each signal independently.** Use repeated standardized observations. Report raw variation and trend; never make tissue claims from one point.
6. **Synthesize without voting.** Weight valid/comparable outcome signals more heavily than input proxies or non-comparable evidence. Explain conflicts.
7. **Classify plateau/rate only at the supported claim ceiling.** A flat latest value is not a plateau. No universal plateau duration is assumed.
8. **Review prior intervention.** Compare its preregistered expected effect to observed data; mark `SUPPORTED`, `NOT_SUPPORTED` or `INCONCLUSIVE`.
9. **Choose the smallest justified action.** Default to one key variable at a time when a change is warranted.
10. **Write state deliberately.** Persist only validated period summaries, decisions, interventions, expectations and explicit uncertainties; preserve history and supersession.
11. **Set next review condition.** Specify what evidence would confirm/refute the current hypothesis.

## Professional judgment rules

### A. Body mass: trend before story

A daily scale reading is a noisy observation, not a tissue measurement. Hydration, glycogen, gut content, recent carbohydrate/sodium changes, creatine use, travel and training can alter short-term mass.

- Never infer muscle or fat change from one scale point.
- Prefer repeated standardized observations and an aggregate/trend.
- Annotate suspected transient causes; do not silently delete data.
- A valid upward trend supports **body-mass gain**, not its composition.

When a user calls one flat week/day a plateau, compare the current aggregate/trend with prior comparable periods before accepting the premise.

### B. Performance: like with like

Compare resistance-training performance only when the underlying task is comparable enough:
- same exercise/meaningfully equivalent variant;
- same equipment/machine where equipment affects mechanics;
- same ROM and important technique constraints;
- load/repetition target interpreted with effort context;
- no material program-phase or fatigue confound left unmentioned.

Load/repetitions improving at similar effort is a useful strength/performance signal. One poor session is normally weak evidence. Volume load is an input proxy and cannot prove adaptation by itself.

Do not turn strength progress into proof of hypertrophy: neural, technical and skill adaptations can contribute.

### C. RIR/RPE: useful, noisy

Use RIR/RPE to contextualize performance and dose, but treat them as subjective/context-sensitive. Never let one RIR/RPE value overrule a repeated objective pattern without a reason. Do not fabricate exact accuracy.

### D. Body measurements and body composition

Before interpreting change:
- verify the same method/protocol;
- check pre-measurement conditions;
- use method/operator-specific reliability, TEM, precision or minimal-detectable-change information when available;
- if no relevant error estimate exists, do not invent one;
- do not compare BIA, DXA, tape, skinfold, ultrasound or 3D outputs as interchangeable.

Hydration/glycogen/creatine and measurement preparation can materially alter apparent lean-mass/body-composition estimates. When a change may sit inside method error or protocol drift, the verdict is bounded/insufficient, not “lean mass gained.”

### E. Photos: comparability gate

Before using progress photos, check:
- lighting;
- pose/flexion;
- camera height and angle;
- distance/focal/framing;
- pump/time/context;
- clothing/visibility.

Material mismatch makes photos `NONCOMPARABLE` for fine longitudinal change. Do not estimate kilos, body-fat percentage or muscle gain from visual impression.

### F. Conflicting indicators

Do not average disagreement away.

Examples:
- weight ↑ + performance ↓: not automatic successful gaining. Verify persistence/comparability, recovery/fatigue, training-dose changes, illness/travel and measurement context. Return conflict/uncertainty when unresolved.
- performance ↑ + weight ≈ flat: record performance progress; hypertrophy remains unresolved unless independently corroborated.
- circumference ↑ + non-standardized photos disagree: prioritize standardized data and downgrade photos, not vice versa.
- body-composition “lean mass” jump after hydration/glycogen/creatine change: downgrade the scan interpretation until protocol/error is resolved.

### G. Plateau

`PLATEAU_SUPPORTED` requires multiple comparable longitudinal observations and no meaningful positive signal in the relevant outcomes, with adequate program exposure/adherence and no unresolved transient or measurement confounder.

`FALSE_PLATEAU` applies when:
- latest raw values are flat but aggregate trend is positive;
- valid performance/measurement progress contradicts the “no progress” premise;
- a measurement/protocol artifact explains the apparent stall.

`INSUFFICIENT_DATA` applies when duration, coverage, comparability or measurement quality cannot support the claim.

Do not encode or invent a universal physiological plateau duration.

### H. Rate of gain

Use an explicit target range when it exists and record its provenance/owner.

If no target exists, a bodybuilding-specific literature reference of roughly 0.25–0.5% bodyweight/week for novice/intermediate natural bodybuilders may be presented only as a **qualified contextual reference**, with advanced trainees generally needing a more conservative target. Do not present it as a universal optimum: the evidence base has not validated one “sweet spot” for all resistance-trained people.

Never infer “too much fat” or “no muscle” from rate alone. Integrate valid performance and standardized physique/body-composition evidence.

### I. Causal uncertainty and changes

Before changing a key variable, create an intervention contract:
- exact variable;
- hypothesis/rationale;
- expected direction in named metrics;
- what key variables stay fixed;
- review condition;
- confounders;
- rollback/escalation condition.

Default to one key causal variable at a time. If several must change for safety or unavoidable operational reasons, log the multi-variable change and explicitly lower later causal attribution.

At follow-up, compare expected vs observed before suggesting the next change. Do not rewrite the expectation after seeing results.

User pressure such as “change everything now” does not lower evidence requirements.

## State/memory contract

Longitudinal state is required for full behavior. Use `schemas/longitudinal-state.schema.json` or a behavior-equivalent structured store.

Must preserve:
- current and superseded measurement protocols;
- period summaries and comparability;
- prior decisions;
- active/past interventions;
- expected effects fixed at intervention time;
- hypotheses with evidence for/against;
- unresolved uncertainties;
- next review condition.

New data may supersede an erroneous value but must not erase useful history. A new measurement protocol can break comparability with earlier periods. External raw records remain source of truth when available.

If persistent structured state is unavailable, operate in bounded single-session mode and state that longitudinal follow-up/attribution is unsupported.

## Tools

Prefer deterministic tools for:
- unit conversion;
- aggregation/trend arithmetic;
- data coverage/missingness;
- exact exercise/variant grouping;
- state schema validation;
- comparison of expected versus observed intervention effects.

Use live research when device-specific validity/error, current consensus or a material threshold is not already supported by the source register.

Use image inspection for progress photos only after the comparability gate and only within the visual claim ceiling.

The bundled `procedures/decision_reference.py` is an executable reference for critical branches used in evaluation. It does not estimate physiology and must not be presented as a validated predictive model.

## Output contract

For a material review return:

1. **DATA QUALITY / COMPARABILITY**
2. **CURRENT VS PRIOR PERIOD**
3. **SIGNALS**
   - body-mass trend
   - performance
   - training dose/effort
   - measurements/body composition
   - photos
   - nutrition/recovery/context
4. **CONFLICTS / UNCERTAINTY**
5. **VERDICT**
6. **ACTION**
7. **PRIOR INTERVENTION REVIEW** when applicable
8. **INTERVENTION CONTRACT** only when changing something
9. **STATE UPDATE**
10. **NEXT REVIEW CONDITION**

Use concise language. A correct `INSUFFICIENT_DATA` or `CONFLICTING_SIGNALS` verdict is preferable to false precision.

## Hard failures

- infer muscle/fat gain or loss from one weight reading, one photo, or one body-composition result;
- treat a daily water/glycogen fluctuation as tissue adaptation;
- call a true plateau from an explicitly too-short or non-comparable period;
- treat missing/invalid data as zero or no change;
- ignore a material exercise/ROM/equipment/measurement-protocol change;
- treat volume or calories alone as proof of adaptation;
- treat RIR/RPE as error-free ground truth;
- quantify photo-derived muscle/fat change without validated measurement;
- apply a universal plateau duration or universal optimal rate-of-gain threshold without evidence;
- claim causality after several key variables changed or material confounders remain;
- change multiple key variables merely because the user demands urgency;
- overwrite prior intervention expectation after seeing outcome;
- claim a prior change worked without retrieving/observing the relevant follow-up data;
- diagnose or treat a medical condition;
- claim T1/T2/T3 readiness beyond recorded evaluation evidence.

## Escalation

Escalate rather than diagnose when the request or data involve medical/clinical questions, severe/persistent unexplained symptoms, injury/rehabilitation, disordered-eating indicators, drug/PED use, or other issues outside this skill’s validated authority.

## Self-check before final decision

- Did I inspect the previous relevant period and active intervention?
- Are the compared observations actually comparable?
- Did I separate outcomes from inputs and context?
- Am I reacting to one reading/session?
- Could hydration/glycogen, protocol or measurement error explain the change?
- Did I preserve disagreement instead of averaging it away?
- Is the claim stronger than the evidence?
- If I recommend change, why this one variable first?
- Is the expected effect recorded prospectively?
- What evidence at the next review would change the decision?
- Did I cross a medical/rehabilitation boundary?

## Qualification boundary

Local v0.1 practical/regression evidence is recorded under `architect/evaluation/muscle_gain_progress_analysis/evaluation-v0.1.md` and machine-readable evidence in `evaluation-evidence-v0.1.json`.

That evidence supports only a development-level practical gate for the explicit critical branches tested. It does **not** establish repository T1 qualification, cross-runtime reliability, strong-practitioner equivalence, or production proof.

T1 requires fresh independent held-out evaluation of the exact assembled candidate/runtime under repository rules. T2 requires independent strong-practitioner validation and calibration for judgment-heavy cases. T3 requires representative monitored field evidence.

Do not weaken hard fails, scope or evaluator independence to obtain a higher label.
