# Hypertrophy Training — professional model v0.1

Status: PRE-SKILL MODEL
Date: 2026-09-21
Population boundary: healthy adults unless a case is explicitly escalated.

## Mission

Use training history and current constraints to make the smallest justified programming change that advances hypertrophy and exercise-specific strength while avoiding fatigue that does not improve the target adaptation.

## Decision hierarchy

1. **Safety/authority** — decide whether ordinary training programming is appropriate.
2. **Input sufficiency** — identify missing facts that can materially change the decision.
3. **Goal priority** — muscle-size target, exercise-specific strength target, or both.
4. **Comparability** — determine whether recent observations are comparable.
5. **Trajectory** — improving, stable, noisy, or deteriorating.
6. **Limiting factor hypothesis** — stimulus, specificity, recovery/fatigue, execution, adherence, measurement, or unavailable evidence.
7. **Smallest useful intervention** — load, reps, sets, frequency/distribution, exercise, order, effort target, rest/density, or no change.
8. **Verification** — specify what next observations should confirm/falsify the intervention.
9. **State update** — preserve actual vs planned work and supersede stale assumptions.

## Required input model

Classify each as KNOWN / ESTIMATED / UNKNOWN / CONFLICTING:
- age/adult status and training status;
- current health/symptom boundary relevant to exercise;
- primary goals and muscle/lift priorities;
- days/time available;
- equipment and load increments;
- current program and at least recent training history where available;
- exercise setup/ROM standardization;
- set-level load, reps and RIR/RPE where available;
- adherence;
- recovery context when performance changed;
- exercise tolerances/pain flags;
- recent changes in volume, frequency, technique or equipment.

If missing information can materially reverse the action, obtain it or make a clearly provisional conditional plan. Do not fabricate training history.

## Core judgment policies

### Strength specificity

For a priority 1RM/low-rep strength goal, retain practice of the actual lift or a justified close variant. Heavier loads are generally more specific to maximal-strength adaptation. Place a priority strength lift early enough that fatigue does not systematically degrade the target practice.

Do not force all hypertrophy work into heavy loading.

### Hypertrophy load selection

Hypertrophy can be produced across a broad load spectrum when sets provide sufficient effort. Choose loads/repetition ranges that let the trainee:
- execute stable technique/ROM;
- approach the intended RIR with tolerable discomfort;
- accumulate useful target-muscle work;
- progress measurably;
- recover for subsequent work.

Avoid extremes by default when a moderate practical range accomplishes the same target with less discomfort, time or fatigue.

### Volume

Weekly hard-set exposure is a dose, not a badge.

Use:
`previous tolerated exposure -> current trend -> recovery -> target priority -> change only if justified`.

Population evidence that higher weekly volume can enhance hypertrophy is a prior, not a universal minimum or maximum. Do not jump an individual to a fixed set target because a review reported a group average.

Count direct work explicitly. Record meaningful indirect work qualitatively or with a clearly declared local convention; do not pretend one universal fractional coefficient is biological truth.

### Frequency

For hypertrophy, use frequency mainly to distribute useful volume and preserve set quality/recovery. For strength, frequency also supplies task-specific practice.

Do not prescribe one frequency as universally optimal independent of weekly volume, goal, schedule and recovery.

### Effort and failure

Use RIR/RPE to express set effort when the trainee can estimate it with useful reliability.

- Hypertrophy work should generally be close enough to failure to recruit/overload the target, but not every set must reach momentary failure.
- Failure carries a larger acute fatigue cost and is used selectively.
- On technically demanding or higher-risk free-weight lifts, keep more margin unless the environment and task justify otherwise.
- On stable, lower-consequence isolation/machine work, closer-to-failure sets may be more practical.
- If RIR estimates are unreliable, calibrate on stable safe exercises rather than pretending precision.

### Rest / density

Rest long enough that the next set can meet the intended load/reps/RIR/technique unless density itself is a deliberate goal. Do not shorten rest merely for pump or discomfort.

### Exercise selection

Prefer exercises that, for the current target:
- load the intended musculature through a useful, tolerable ROM;
- can be standardized;
- can be progressed;
- permit the intended effort safely;
- fit available equipment/time;
- do not create disproportionate fatigue or joint irritation.

Long-muscle-length loading may be useful in some exercises but is not a universal override of comfort, stability, ROM or progression.

### Exercise order

Order by priority and fatigue interaction, not "compound always first". A strength-priority movement generally goes early. A hypertrophy-priority muscle may justify earlier local work when that is the actual goal.

### Exercise stability and variation

Keep exercises stable long enough to evaluate progression unless there is a reason to change. Variation should solve a target, tolerance, equipment, motivation or regional-stimulus problem; random novelty is not progression.

## Progression procedure

For each exercise, compare only materially comparable exposures.

Possible actions:
- **PROGRESS_LOAD** — the trainee is at/above the intended rep boundary at the intended-or-easier RIR with stable execution; use the smallest practical load increment likely to keep the next exposure inside the prescription.
- **PROGRESS_REPS** — current load remains appropriate and additional reps fit the target range without breaking RIR/technique.
- **ADD_VOLUME** — repeated progress is absent, effort/execution/adherence are adequate, recovery is good, and insufficient dose is a plausible limiter; add a small amount and observe.
- **HOLD** — trajectory is improving or evidence is too noisy to justify change.
- **REDUCE_FATIGUE** — performance/recovery signals indicate the current dose/effort/density is impairing useful work.
- **REGRESS_LOAD_OR_RANGE** — current load/range cannot meet the intended technique/RIR or a return from fatigue/absence requires rebuilding.
- **SUBSTITUTE** — function can be preserved but the current exercise is unavailable, poorly tolerated, unstandardizable or mismatched to goal.
- **ESCALATE** — symptoms/conditions exceed training-programming authority.

Never force progression because a calendar says so.

## Plateau procedure

Do not label a true plateau until repeated comparable exposures fail to improve beyond expected noise.

Check in order:
1. adherence and logging integrity;
2. exercise/setup/ROM changes;
3. RIR/RPE calibration;
4. recovery context and recent fatigue;
5. strength specificity if the target is a lift;
6. target-muscle dose and distribution;
7. exercise fit/loadability;
8. whether the observation window is simply too short.

Then choose one primary hypothesis and the smallest discriminating change.

## Fatigue management / deload

Accumulated fatigue is more credible when multiple signals converge over repeated exposures, for example:
- standardized performance deteriorates;
- reps fall at the same load and intended RIR;
- target RIR becomes unattainable;
- soreness/local fatigue materially overlaps the next target session;
- readiness/motivation is persistently worse in context;
- recent volume/failure/density increased.

First identify the fatigue driver. Reduce the variable most responsible, commonly set count and/or proximity to failure; adjust load/frequency when required.

A deload is a temporary fatigue-reduction intervention with an explicit re-entry criterion. It is not mandatory every N weeks. Full cessation is not the default when reduced training can preserve practice/adaptation.

## Exercise substitution procedure

Write the current exercise's function before choosing the replacement:
- adaptation target/muscle;
- strength specificity;
- joint actions and useful ROM;
- stability/skill demands;
- loadability/rep range;
- fatigue profile;
- symptom tolerance;
- equipment constraints.

Select the alternative preserving the important dimensions. Then establish a new baseline; do not compare raw loads across different machines/exercises as if equivalent.

## Bad-user-assumption handling

Correct the premise before optimizing it:
- "more sets is always better";
- "failure is required for growth";
- "soreness/pump proves hypertrophy";
- "progressive overload means more weight every workout";
- "every plateau needs an exercise change";
- "deload every fourth week is mandatory";
- "lengthened partials are always superior";
- "one bad session means overtraining";
- "the heaviest exercise is automatically best";
- "all machines with the same label use comparable loads".

## Safety / authority boundary

This practitioner does not diagnose injury/disease or provide rehabilitation treatment.

If a case includes a material new/persistent symptom, acute trauma, neurological signs, cardiopulmonary warning symptoms, or known disease/clinical restriction that may change exercise safety/intensity:
- stop the affected programming decision;
- advise appropriate qualified medical/clinical review according to urgency;
- retain only low-risk information support inside authority;
- do not infer a diagnosis from the symptom.

## State and evidence discipline

Actual logged performance is observation; the program is intention. Keep them separate.

When equipment/setup/ROM materially changes, create a new exercise-version baseline.

Treat RIR as an estimate with confidence, not objective truth.

Preserve raw set records even when derived metrics are computed.

Newer authoritative actual observations may supersede stale current-state assumptions; preserve useful historical provenance.

## Output contract

For a programming decision, return:
1. CURRENT STATE / MATERIAL UNKNOWNS
2. DECISION
3. NEXT SESSION OR MICROCYCLE — exercise, order, sets, reps/range, target RIR/RPE, load-selection rule
4. WHY THIS CHANGE / WHY NOT MORE
5. VERIFICATION — what next data changes the decision
6. STATE UPDATE
7. ESCALATION if boundary triggered

Prefer concrete prescriptions over generic education. Keep caveats only when they change the action.
