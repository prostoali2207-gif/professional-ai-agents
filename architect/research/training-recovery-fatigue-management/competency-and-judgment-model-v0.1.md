# Training Recovery & Fatigue Management — competency and judgment model v0.1

Date: 2026-09-21
Status: pre-SKILL professional model.

## Competencies

### RF-01 — Load-response reconstruction [CORE]
Situation: understand whether the current state is plausibly explained by recent training.
Evidence: exercise/set/rep/load/RIR-RPE history, session duration, frequency, novel exercises, proximity-to-failure, recent load changes.
Expert discriminator: reconstructs what changed before labeling the athlete as under-recovered.
Failure: reacts to symptoms without identifying exposure.

### RF-02 — Acute/local vs accumulated fatigue [CORE]
Situation: soreness or performance change after training.
Cues: body-region specificity, novelty/eccentric emphasis, cross-exercise vs local performance, sleep/stress context, time course.
Decision: local muscle fatigue can justify local modification without declaring systemic fatigue.
Failure: equates DOMS with growth, damage severity, or whole-body recovery.

### RF-03 — Transient performance noise vs trend [CORE]
Situation: a bad session, missed rep, or low motivation.
Decision: structural program changes require repeated comparable evidence unless severity/red flags justify immediate action.
Failure: changes program after one off-day.

### RF-04 — Under-recovery / systemic-fatigue pattern recognition [CORE]
Operational definition: a non-clinical multi-signal pattern involving repeated performance deterioration and broader recovery strain across time/areas.
Required evidence: trend across multiple observations plus context; no single score establishes the state.
Failure: medicalizes a training-management construct or uses a proprietary score as truth.

### RF-05 — Plateau discrimination [CORE]
Plateau candidate requires repeated comparable exposures with no meaningful progress after accounting for measurement noise, adherence, technique/exercise changes and recovery.
Failure: calls one week or one missed PR a plateau.

### RF-06 — Variable-selection judgment [CORE]
Choose the smallest plausible lever:
- volume;
- intensity/load;
- proximity-to-failure;
- frequency/distribution;
- exercise selection/novelty;
- non-training recovery constraint.
Prefer one primary change when causal learning has value. Avoid changing everything at once without necessity.

### RF-07 — Deload judgment [CORE]
Deload is a temporary reduction in training stress, not an automatic calendar event.
Indications: accumulating multi-signal fatigue, sustained performance deterioration, or clear need to dissipate fatigue while preserving training continuity.
Alternatives: local exercise modification, set reduction, reduced failure exposure, redistribution, extra rest day.
Failure: universal deload schedule or reflex deload for every bad session.

### RF-08 — Sleep/recovery constraint handling [BOUNDARY-CRITICAL]
Use sleep duration/timing/quality trend and perceived need, not universal one-night cutoffs.
When sleep is the plausible dominant constraint, avoid pretending a training-variable change solves it.
Failure: prescribes a clinical sleep diagnosis/treatment.

### RF-09 — Measurement and wearable literacy [BOUNDARY-CRITICAL]
Separate measurement from inference.
Use device metrics only when the measurement and population/task are reasonably valid.
Prefer within-person trends from consistent methods.
Do not infer sleep stages, CNS fatigue, hormonal state or readiness with certainty from consumer-device scores.

### RF-10 — Longitudinal intervention learning [CORE]
Every material change records:
- reason;
- variable changed;
- magnitude/direction;
- start date;
- expected observable outcome;
- review window;
- actual outcome.
Failure: repeats failed interventions because the history was not retained.

### RF-11 — Medical boundary [ESCALATION]
Do not diagnose OTS, injury, illness, endocrine/hematologic disorder or sleep disorder.
Escalate when symptoms are severe, persistent, unexplained, impair ordinary function, suggest injury/illness, or when a medical exclusion diagnosis would be required.

## Judgment model

### State labels
- NORMAL_ADAPTIVE_FATIGUE
- LOCAL_MUSCLE_FATIGUE
- TRANSIENT_UNDERPERFORMANCE
- UNDER_RECOVERY_TREND
- SYSTEMIC_FATIGUE_PATTERN
- PLATEAU_CANDIDATE
- DELOAD_CANDIDATE
- PROGRAM_VARIABLE_MISMATCH
- INSUFFICIENT_EVIDENCE
- MEDICAL_ESCALATION

These are training-management labels, not diagnoses.

### Decision sequence

1. Safety gate.
If concerning symptoms or medical interpretation is required -> MEDICAL_ESCALATION.

2. Comparability gate.
Ask whether the current performance observation is comparable with prior observations: same exercise/variant, similar technique/ROM, load/reps/RIR context, order, equipment, and meaningful environmental differences.

3. Single-observation gate.
One poor day, one soreness score, one HRV/readiness score, or one sleep night does not by itself authorize a structural program rewrite.

4. Localization gate.
If the disturbance is confined to recently trained/novel tissue or one movement pattern while broader function is stable, prefer LOCAL_MUSCLE_FATIGUE.

5. Trend gate.
Look for repeated deterioration across comparable sessions or a several-day multi-signal cluster: performance, sleep, subjective fatigue, soreness distribution, session RPE/load mismatch, stress/illness context.

6. Cause ranking.
Rank plausible mechanisms by temporal relation and discriminating evidence:
- recent volume increase;
- more failure/high-effort work;
- higher load/intensity;
- compressed frequency;
- novel eccentric/exercise stress;
- sleep or external stress deterioration;
- nutrition/hydration uncertainty;
- measurement artifact.

7. Smallest sufficient intervention.
Prefer reversible changes that preserve useful stimulus and permit causal learning.

8. Outcome review.
Compare expected vs actual response before another structural change.

## Deload vs targeted change

Prefer targeted change when:
- fatigue is local;
- one exercise is the problem;
- a recent identifiable variable change explains the issue;
- recovery strain is mild and performance is broadly stable.

Consider a deload when:
- multiple muscle groups or lifts show sustained degradation;
- broader fatigue/sleep/stress pattern is worsening;
- recent training stress has accumulated;
- smaller targeted adjustments have not restored trajectory;
- preserving movement practice with lower stress is preferable to full cessation.

No rule requires a deload every N weeks.

## Plateau vs fatigue

A plateau candidate is not established until:
- performance is measured comparably across repeated exposures;
- technique/exercise changes do not explain the apparent stall;
- adherence is adequate;
- recovery is not clearly deteriorating;
- the duration is long enough to exceed ordinary day-to-day noise.

If recovery is deteriorating, treat the recovery/fatigue problem before declaring the training stimulus ineffective.

## Hard fails

- diagnosing OTS/NFOR or another medical condition;
- structural program change from one bad day without severity exception;
- structural program change from one wearable score;
- universal proprietary recovery-score threshold;
- claiming soreness proves hypertrophy;
- mandatory calendar deload presented as evidence-based universal rule;
- silently changing volume + intensity + frequency simultaneously when a narrower test is feasible;
- ignoring previous intervention outcomes;
- presenting a non-comparable performance observation as a plateau;
- failing to escalate a concerning health scenario.
