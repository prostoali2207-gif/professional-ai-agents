# Hypertrophy Training — decision procedures v0.1

Version: 0.1

These procedures operationalize recurring decisions. They are not unconditional recipes.

## P1 — session/history normalization

For every exercise exposure capture:
- exercise_id + exercise_version;
- date/session;
- load;
- reps;
- RIR/RPE and confidence if available;
- set completion;
- ROM/technique deviation;
- rest deviation if material;
- symptom flag;
- equipment/setup change.

Before comparing sessions, mark exposures NON_COMPARABLE when material equipment, ROM, technique standard or exercise version changed.

## P2 — progression / hold / regression

For each comparable exercise series:

1. Check safety boundary.
2. Check whether the current prescription was actually followed.
3. Check trajectory across repeated exposures.
4. Classify:
   - improving at target effort -> HOLD or advance the least disruptive variable;
   - top of rep target reached at intended/easier RIR with stable technique -> smallest practical load increase;
   - load appropriate but rep target not yet exhausted -> progress repetitions;
   - repeated lack of progress + good recovery/effort/adherence -> diagnose plateau before adding sets;
   - deteriorating performance + fatigue context -> reduce fatigue, not "push harder";
   - exercise unavailable/poorly tolerated/unstandardizable -> substitute by function.
5. Write the observation that would reverse the decision.

Do not interpret "progressive overload" as "add weight every workout".

## P3 — RIR calibration

Use RIR as an estimate.

Calibration triggers:
- novice or unfamiliar exercise;
- repeated mismatch between predicted RIR and achieved repetitions;
- large session-to-session RIR inconsistency at stable load/setup;
- user reports every set with identical RIR despite large rep drop.

Action:
- choose a stable, low-consequence exercise;
- on a planned calibration set, approach safe technical failure closely enough to compare predicted vs actual reserve;
- update confidence, not just the numeric RIR;
- avoid calibration-to-failure on a high-risk lift without appropriate safety setup.

## P4 — volume change

ADD a small amount of target-muscle work only when:
- the target is important;
- repeated comparable performance is not improving enough for the goal;
- effort and technique are adequate;
- adherence is high;
- recovery is acceptable;
- exercise selection is reasonable;
- insufficient dose is a plausible primary limiter.

HOLD volume when progress is occurring or evidence is ambiguous.

REDUCE volume when:
- a recent dose increase is followed by persistent performance degradation and recovery overlap; or
- the current number of hard sets prevents later sets/sessions from meeting intended quality.

After a volume change, keep other variables as stable as practical and define a review window.

## P5 — fatigue / deload

1. Look for converging repeated signals, not one bad day.
2. Identify the likely fatigue driver: sets, failure proximity, density, load, exercise choice, schedule, external stress/illness.
3. Reduce the responsible driver first.
4. Preserve priority-lift practice when safe and useful.
5. Define re-entry: e.g. standardized performance/readiness returns toward prior baseline and target RIR is again feasible.
6. If symptoms imply illness/injury/clinical concern, escalate instead of calling it "fatigue".

A deload can be several reduced sessions or a reduced microcycle. No calendar interval is mandatory.

## P6 — plateau diagnosis

A plateau requires repeated comparable non-progression beyond ordinary noise.

Check:
A. logging/adherence;
B. setup/ROM/equipment;
C. RIR calibration;
D. recovery/fatigue;
E. goal specificity;
F. weekly dose/distribution;
G. exercise loadability/target fit;
H. observation window.

Choose one primary hypothesis and one discriminating intervention. Do not change load + sets + exercise + frequency simultaneously unless an external constraint forces a rebuild.

## P7 — exercise substitution

Describe the original exercise function:
- primary adaptation target;
- strength-specificity role;
- muscles/joint actions;
- useful ROM;
- stability/skill;
- loadability/rep zone;
- fatigue cost;
- symptom tolerance;
- equipment/time.

Choose a replacement that preserves the dimensions that matter for this goal.

Then:
- create a new exercise_version;
- establish a new baseline;
- do not compare absolute machine weights across versions;
- keep surrounding program stable enough to interpret the substitution.

## P8 — mixed hypertrophy + strength goal

For a priority strength lift plus muscle growth:
- place the priority lift early;
- include heavy-enough specific practice;
- stop most strength-practice sets with useful technical margin unless a specific test demands otherwise;
- add hypertrophy work with loads/reps that are efficient and recoverable;
- prevent accessory volume from degrading repeated priority-lift practice;
- use separate progression criteria for the lift and for target-muscle accessories.

## P9 — insufficient data

If history is absent:
- do not invent a baseline;
- collect the minimum high-sensitivity inputs;
- when a usable provisional program is still possible, label it PROVISIONAL and start conservatively enough to observe response;
- define exactly what data to log next session;
- avoid aggressive volume/failure/loading decisions until response is observable.

If a missing fact can reverse a safety decision, stop and obtain/escalate rather than provide a provisional answer.

## P10 — downstream review

After the next exposure/block:
- compare planned vs actual;
- verify whether technique/setup remained comparable;
- inspect progression and fatigue signals;
- mark the prior hypothesis SUPPORTED / NOT SUPPORTED / UNRESOLVED;
- keep, reverse or revise the intervention;
- persist only future-useful state.
