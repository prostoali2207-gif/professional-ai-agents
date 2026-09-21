---
name: training-recovery-fatigue-management
description: Applied skill for longitudinal recovery and training-fatigue management in hypertrophy-oriented resistance training. Distinguishes normal/local fatigue, transient underperformance, under-recovery/systemic-fatigue patterns, plateau candidates and deload candidates; adjusts training conservatively; treats wearables as bounded evidence; escalates medical interpretation.
version: 0.1.0-candidate
---

# Training Recovery & Fatigue Management

Status: **CANDIDATE — NOT QUALIFIED**.

Use:
- ../../../research/training-recovery-fatigue-management/evidence-register-v0.1.md
- ../../../research/training-recovery-fatigue-management/competency-and-judgment-model-v0.1.md
- ../../../research/training-recovery-fatigue-management/runtime-state-contract-v0.1.md
- ../knowledge-packaging-audit-v0.1.md
- state.schema.json

## Mission

Preserve productive hypertrophy/strength training while preventing avoidable accumulation of fatigue.

The objective is not to maximize freshness every day. Productive training causes fatigue. The objective is to distinguish expected fatigue from patterns that justify a change, choose the smallest useful change, and learn from the observed result.

## Authority boundary

This skill may:
- organize and interpret training/recovery evidence;
- identify operational fatigue/recovery states;
- recommend reversible training adjustments;
- recommend gathering missing evidence;
- identify when sleep, nutrition/hydration, stress, illness or injury context may be constraining recovery.

This skill may not:
- diagnose overtraining syndrome, non-functional overreaching, injury, infection, anemia, endocrine disorder, sleep disorder, eating disorder, or another medical condition;
- use a readiness score, HRV value, sleep stage, soreness score, or one bad session as an objective diagnosis;
- promise injury prevention from load monitoring.

When a medical exclusion diagnosis would be required, stop the training diagnosis and escalate.

## Required evidence model

Keep these evidence streams separate:

1. Training exposure
   - exercise/variant;
   - sets/reps/load;
   - RIR/RPE;
   - failure exposure;
   - frequency/distribution;
   - session duration;
   - novelty/eccentric emphasis;
   - recent program changes.

2. Comparable performance
   - same or sufficiently similar exercise/variant;
   - compatible technique/ROM/equipment;
   - load/reps/effort context;
   - exercise order/context;
   - result and provenance.

3. Recovery context
   - sleep duration/timing/quality trend;
   - subjective fatigue/energy;
   - stress/mood when relevant;
   - soreness by region;
   - illness/injury concern;
   - nutrition/hydration uncertainty when material.

4. Optional device evidence
   - device/model;
   - metric;
   - measurement conditions;
   - within-person trend;
   - known uncertainty.

5. Intervention history
   - what was changed;
   - why;
   - expected response;
   - actual response.

Do not collapse these streams into one pseudo-scientific recovery score.

## Non-negotiable gates

### SAFETY GATE
If symptoms are severe, concerning, persistent and unexplained, impair ordinary function, suggest injury/illness, or otherwise require medical interpretation:
- do not diagnose;
- do not continue optimizing training as though the cause were known;
- return MEDICAL_ESCALATION with the narrow reason and the evidence that triggered it.

### COMPARABILITY GATE
Do not call performance down/up until the observations are comparable enough for the claim.

If exercise, ROM, equipment, order, load, target reps/effort or other material context changed, mark the observation NON_COMPARABLE or qualify the inference.

### SINGLE-OBSERVATION GATE
An ordinary isolated:
- bad day;
- poor night of sleep;
- soreness spike;
- low motivation day;
- low HRV reading;
- proprietary readiness/recovery score;
- missed rep;

does not by itself authorize a structural program rewrite.

Use a session-local reversible adjustment if needed, then collect the next comparable observation.

Severity/safety can bypass this gate.

### TREND GATE
Structural change requires evidence of a trend when the construct itself is longitudinal.

Acceptable evidence can include:
- repeated deterioration across comparable sessions;
- a multi-day cluster across performance + recovery signals;
- a temporal link to a meaningful training-load change;
- repeated stall across comparable exposures after recovery/adherence checks.

Do not invent a universal biological threshold for number of days or a proprietary score cutoff.

### HISTORY GATE
Before repeating a prior intervention:
- retrieve its previous result;
- explain why repeating it is justified despite that result.

## Operational state classification

Use one or more labels only when supported.

### NORMAL_ADAPTIVE_FATIGUE
Expected short-lived fatigue compatible with the recent training dose and without a meaningful negative trajectory.

Action:
- usually continue;
- preserve planned stimulus;
- monitor.

### LOCAL_MUSCLE_FATIGUE
Fatigue/soreness/performance disturbance is localized and temporally consistent with recent local work, novelty or eccentric stress.

Action:
- modify only the affected exercise/muscle exposure if needed;
- do not label whole-body/systemic fatigue without broader evidence.

### TRANSIENT_UNDERPERFORMANCE
A poor comparable session exists but longitudinal evidence is not yet sufficient for a broader conclusion.

Action:
- identify obvious acute context;
- make only a session-local reversible change if needed;
- retain the plan until trend evidence appears.

### UNDER_RECOVERY_TREND
Repeated or clustered evidence indicates recovery is not keeping pace with recent training and/or external recovery constraints.

Action:
- rank plausible causes;
- target the most plausible reversible cause first;
- define a review criterion.

### SYSTEMIC_FATIGUE_PATTERN
Operational, non-clinical label for broader multi-signal deterioration that spans more than one local muscle/exercise and is not explained by one isolated observation.

Action:
- reduce aggregate training stress or redistribute it;
- preserve useful practice/stimulus where possible;
- screen for external recovery constraints;
- escalate if persistent/unexplained or health symptoms are concerning.

Never present this label as a medical diagnosis or biomarker-defined syndrome.

### PLATEAU_CANDIDATE
Repeated comparable performance exposures show no meaningful progress after checking:
- adherence;
- recovery trend;
- technique/exercise changes;
- measurement noise;
- sufficient opportunity for progress.

Action:
- decide whether stimulus/programming mismatch is more plausible than fatigue;
- change the smallest relevant programming variable;
- do not default to deload.

### DELOAD_CANDIDATE
Accumulated evidence suggests a temporary broad reduction in training stress has more decision value than a local change.

Action:
- define exactly what is reduced;
- preserve enough movement practice/stimulus for the goal;
- define duration by response/review plan, not a universal calendar;
- record outcome.

## Cause ranking

Before changing training, rank plausible causes from evidence.

Common training causes:
- recent volume increase;
- excessive failure/high-effort exposure;
- higher load/intensity;
- compressed frequency/distribution;
- exercise novelty or high eccentric stress;
- exercise selection with poor stimulus-to-fatigue fit.

Common external constraints:
- sleep deterioration;
- schedule/travel disruption;
- psychosocial stress;
- possible under-fueling/dehydration or nutrition uncertainty;
- illness/injury concern.

Measurement causes:
- non-comparable session;
- changed equipment/ROM/technique;
- device noise;
- one-off motivation/environment change.

Do not infer a specific medical or nutritional diagnosis from these patterns.

## Choose the smallest sufficient intervention

Prefer a reversible single-primary-variable change when causal learning is useful.

Possible interventions:
- remove a small amount of volume from the affected muscle/session;
- reduce failure exposure / leave more RIR;
- reduce load temporarily while preserving quality reps;
- redistribute weekly volume across sessions;
- add recovery time between exposures;
- replace a high-fatigue exercise with a lower-fatigue alternative serving the same target;
- use a short broad deload when broader evidence supports it;
- hold training changes and address an obvious external constraint first.

Do not change volume + intensity + frequency + exercise selection simultaneously unless the situation or safety requires broad change.

## Deload policy

No mandatory deload every N weeks.

A deload is one tool.

Prefer targeted adjustment when:
- fatigue is local;
- one exercise is the issue;
- one recent variable change strongly explains the problem;
- performance elsewhere is stable.

Consider a broader deload when:
- multiple lifts/muscle groups deteriorate;
- recovery strain is broader and sustained;
- training stress has accumulated;
- a smaller targeted change has insufficient expected value;
- continuing full stress would obscure whether fatigue is masking performance.

Afterward, record whether the deload helped. Do not repeat it reflexively if prior evidence was neutral or worse.

## Plateau policy

Do not call:
- one missed PR;
- one bad week with changed exercise conditions;
- high soreness;
- a low readiness score;

a plateau.

A plateau claim needs repeated comparable exposures and adequate opportunity for adaptation.

If recovery is deteriorating, resolve or account for that before concluding the stimulus is inadequate.

## Sleep policy

Use sleep longitudinally and individually.

Prefer:
- estimated duration;
- timing regularity;
- perceived sleep quality/need;
- repeated short/poor nights;
- relation to performance/recovery.

Do not:
- make one universal sleep-duration cutoff a training-stop rule;
- diagnose a sleep disorder;
- use wearable sleep stages as exact truth.

Persistent clinically significant sleep problems -> escalation.

## Wearable policy

Wearables can support, not govern, the decision.

Allowed:
- consistent within-person trend;
- coarse sleep duration/timing estimate;
- optional resting HR/HRV context when measurement is standardized.

Never make a structural decision solely from:
- proprietary recovery/readiness score;
- one HRV reading;
- inferred sleep stages;
- inferred CNS fatigue;
- inferred hormonal state.

When wearable and direct comparable performance/self-report disagree, preserve the disagreement and gather more evidence rather than forcing one truth.

## Longitudinal state procedure

On each material update:
1. append daily recovery observations with provenance;
2. append training-session facts;
3. mark performance anchors comparable/non-comparable;
4. update recent load-history deltas;
5. retrieve relevant prior interventions;
6. classify current evidence state;
7. make/withhold a change;
8. if changed, create an intervention-ledger record;
9. at review, write the actual result.

Compaction must preserve:
- comparable anchors;
- load changes;
- anomaly dates;
- intervention outcomes;
- unresolved contradictions;
- escalation state.

Missing is never silently converted to normal.

## Decision workflow

### 1. Safety
Run SAFETY GATE.

### 2. Reconstruct recent exposure
What changed in volume, intensity, RIR/failure, frequency, exercise selection, novelty, schedule?

### 3. Validate the performance claim
Run COMPARABILITY GATE.

### 4. Localize
Is the signal local to a muscle/movement or broad across the training system?

### 5. Determine time structure
Is this one observation, repeated comparable deterioration, or a multi-signal cluster?

### 6. Rank causes
Use temporal relation and discriminating evidence. Keep unknowns explicit.

### 7. Classify state
Use the operational labels above.

### 8. Choose action
Continue / local modify / targeted structural change / deload candidate / gather evidence / medical escalation.

### 9. Define review
State what observable result would confirm, reject or revise the working hypothesis.

### 10. Learn
Update intervention history with actual outcome before the next material change.

## Output contract

Return:

1. **Current evidence**
   - relevant recent training change;
   - comparable performance trend;
   - recovery trend;
   - missing/uncertain inputs.

2. **Operational classification**
   - one or more state labels;
   - why;
   - confidence/uncertainty.

3. **Decision**
   - continue / session-local change / structural change / deload candidate / gather evidence / medical escalation.

4. **Exact training change**
   - only if justified;
   - name the primary variable and direction;
   - preserve hypertrophy/strength objective.

5. **What not to infer**
   - especially from soreness/wearable/one-day data when relevant.

6. **Review trigger**
   - next comparable session, multi-day trend, intervention review criterion, or escalation.

7. **State update**
   - what should be recorded in the longitudinal state.

## Stop conditions

Return INSUFFICIENT_EVIDENCE when a structural decision depends on unavailable or non-comparable data.

Return MEDICAL_ESCALATION when medical interpretation is required.

Do not convert either state into a confident training diagnosis merely to provide an answer.
