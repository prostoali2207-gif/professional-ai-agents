# Low-Appetite Muscle-Gain Nutrition — runtime state, memory, control and escalation v0.1

Status: pre-SKILL architecture artifact.

## 1. State model

### User profile state
Persist only when useful and authorized:
- age category (adult vs not);
- dietary constraints/allergies;
- stable food preferences relevant to adherence;
- stable training context if it will be reused.

### Current nutrition cycle
Structured fields:
- `cycle_id`
- `cycle_start_date`
- `body_weight_series[] = {date, kg, conditions, provenance}`
- `weight_trend = {window_days, slope_kg_day, pct_week, confidence_notes}`
- `estimated_intake = {kcal_day, method, days_observed, uncertainty}`
- `protein_g_day`
- `fat_g_day`
- `carb_g_day`
- `meal_pattern`
- `appetite = {score_or_description, worst_windows, limiting_foods, GI_notes}`
- `performance_series[] = {date, exercise_or_session, load_reps_or_metric, RIR_if_known, provenance}`
- `recovery_notes`
- `waist_or_proxy_series[]` when user elects to track it
- `active_change = {date, change, estimated_energy_delta, rationale}`
- `previous_changes[] = {date, change, outcome, disposition}`
- `red_flags[]`
- `status = COLLECT | HOLD | INCREASE | DECREASE | ESCALATE`

## 2. Provenance and uncertainty

Every material value must distinguish:
- directly measured;
- user-reported;
- estimated from food labels/database;
- calculated;
- inferred;
- unknown.

Do not store a TDEE estimate as measured maintenance.

Diet logs have systematic and random error. Preserve the number as an estimate and use observed body-mass response as feedback rather than "correcting" the log by a fixed under-reporting percentage.

## 3. Supersession

Newer authoritative/current measurement can supersede stale state when scope is clear:
- corrected body weight supersedes a typo;
- new food label replaces an old estimate for that food;
- a current training block replaces prior session demand.

Keep useful history as superseded when it matters for trajectory. Do not let stale memory override new observed data.

## 4. Observation/control loop

`measure -> validate comparability -> estimate trend -> classify sufficiency -> choose smallest change -> record -> observe -> hold/adjust/escalate`

Default observation window after a small energy change:
- generally at least 14 days before another change when weight data are noisy but stable;
- extend toward 21 days when adherence/measurement noise is high;
- shorter reaction is allowed for clear adverse symptoms, involuntary loss, or safety concerns.

No unbounded "self-reflection" loops. A new iteration must add data, test an invariant, or escalate.

## 5. Clinical escalation gate

Stop ordinary muscle-gain optimization and recommend appropriate clinician / registered dietitian evaluation when any material condition is present, including:
- persistent or newly reduced appetite with unintentional weight loss;
- continuing weight loss despite attempts to maintain/gain;
- BMI <18.5 kg/m² or other clear malnutrition concern;
- >10% unintentional weight loss over 3–6 months, or BMI <20 with >5% unintentional loss over 3–6 months;
- little or no intake for >5 days or expectation of this pattern;
- dysphagia, repeated vomiting, persistent diarrhea, GI bleeding, major unexplained GI symptoms;
- signs/history suggesting eating disorder or compulsive restriction;
- severe fatigue, recurrent illness/injury, endocrine/menstrual/reproductive concerns or other signs compatible with problematic low energy availability;
- pregnancy, minor status, medically complex disease, renal/hepatic disease, diabetes, or a medication issue that materially changes nutrition safety.

These are escalation indicators, not diagnoses.

For emergency symptoms, direct urgent/emergency care according to local services rather than continuing nutrition coaching.

## 6. Supplement escalation

Do not clear a supplement as "safe for you" when:
- medical history is relevant and unknown;
- prescription medication interaction is plausible;
- pregnancy/breastfeeding/minor status is present;
- product purity/banned status matters for tested sport and has not been verified.

## 7. Privacy / persistence

Body weight, appetite, health symptoms and dietary data can be sensitive. Persist only what has an identified future use and the platform permits. Rejected sensitive payloads must not survive in durable notes under an "excluded" field.

## 8. Resume contract

A safe checkpoint contains:
- goal and scope;
- latest validated trend;
- current protein/macro strategy;
- active nutrition change;
- observation window end;
- unresolved uncertainty;
- red-flag status;
- previous change/outcome history.

After restart, do not make a new calorie adjustment until the active change and its observation window are recovered.
