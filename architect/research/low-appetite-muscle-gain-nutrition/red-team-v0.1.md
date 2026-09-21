# Low-Appetite Muscle-Gain Nutrition — pre-SKILL red-team v0.1

Status: completed pre-SKILL red-team.
Date: 2026-09-21.

Required question: **What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?**

## Lenses and findings

### 1. Senior sports dietitian / performance nutrition practitioner

**Finding RT-01 — "minimal surplus" can silently become under-fueling.**
A user who values lightness may interpret the strategy as permission to preserve hunger or low energy availability.

Repair:
- profession reconstruction explicitly rejects chronic hunger as the goal;
- applicability gate refuses intentional under-fueling;
- LN-07 and REDs/clinical escalation added;
- candidate must distinguish low food volume from low energy availability.

Status: CORRECTED.

**Finding RT-02 — 0.25–0.5%/week could be misused as a compulsory target.**
Evidence does not establish a universal optimal gain rate, especially in advanced trainees.

Repair:
- decision model labels the range an evidence-informed reference/upper operating context, not a minimum;
- HOLD is correct when a slower positive trend coexists with improving training.

Status: CORRECTED.

**Finding RT-03 — excess protein can be the cause of the appetite problem.**
A generic bodybuilding system might keep 2.2–3.0 g/kg protein and then add calories on top.

Repair:
- ~1.6 g/kg/day is the default sufficiency target;
- ~1.6–2.0 g/kg/day is a working range;
- high protein is deliberately reduced toward sufficiency when it crowds out energy.

Status: CORRECTED.

### 2. Nutrition scientist

**Finding RT-04 — calorie logs and TDEE formulas invite false precision.**
Self-reported intake has systematic/individual error, while maintenance changes with body mass/activity/adaptation.

Repair:
- observed weight trend is a feedback signal;
- intake/TDEE remain ESTIMATED;
- multi-week trend window and provenance classes required.

Status: CORRECTED.

**Finding RT-05 — carbohydrate recommendations are easy to overgeneralize from endurance sport.**
Resistance training evidence does not justify a universal 4–7+ g/kg target.

Repair:
- carbs are allocated after protein/fat based on energy need and actual training demand;
- higher priority only in long/high-volume, fasted, depleted, repeated-session contexts.

Status: CORRECTED.

### 3. Appetite/satiety / diet-behavior lens

**Finding RT-06 — "eat more calorie-dense food" is still too vague.**
The skill needs an ordered intervention mechanism that does not just produce larger meals.

Repair:
- three-level energy-density ladder: densify existing meals -> reduce avoidable satiety burden -> small liquid/semi-solid module;
- smallest-energy-unit controller prevents uncontrolled mass-gainer escalation.

Status: CORRECTED.

**Finding RT-07 — liquids cannot be advertised as universally non-satiating.**
Evidence is heterogeneous.

Repair:
- liquids/shakes are explicitly individualized tolerance tools, not a universal satiety claim.

Status: CORRECTED.

### 4. Clinical / safety reviewer

**Finding RT-08 — low appetite can be a symptom, not a preference.**
New/persistent appetite loss, dysphagia, GI symptoms, medication effects or involuntary weight loss make routine coaching unsafe.

Repair:
- explicit clinical escalation gate;
- NICE/NHS/IOC sources included;
- diagnosis remains outside authority.

Status: CORRECTED.

**Finding RT-09 — protein/supplement advice cannot be universal in clinical populations.**
Kidney/liver disease, pregnancy, minors, medications and tested-sport product purity can change the decision.

Repair:
- supplement and protein boundaries added;
- specific clinical cases escalate rather than receiving generic clearance.

Status: CORRECTED.

### 5. Strength coach / hypertrophy practitioner

**Finding RT-10 — nutrition can be blamed for poor progress caused by inadequate training stimulus.**
Flat performance/muscle gain is not automatically an energy problem.

Repair:
- energy increase requires evidence of insufficient intake rather than plateau alone;
- performance is a supporting signal, not proof of energy deficit;
- candidate must state when training-program quality is an unresolved confound.

Status: CORRECTED.

### 6. Evaluation scientist

**Finding RT-11 — polished plans could pass without correct control behavior.**
Need contrastive/stateful cases, not nutrition trivia.

Repair:
- evaluation plan includes metamorphic pairs, noisy trend cases, prior-change memory, clinical hard-fails and end-to-end work;
- future T1 requires fresh held-out independent fixtures.

Status: CORRECTED.

### 7. Operations/state owner

**Finding RT-12 — repeated chats can stack calories accidentally.**
If a +150 kcal change was made five days ago and forgotten, another increase can be added before its effect is observable.

Repair:
- `active_change`, `previous_changes`, observation window and restart contract are mandatory state;
- state fixture makes double adjustment a hard failure.

Status: CORRECTED.

## Residual uncertainties

Not blockers for candidate assembly, but must remain explicit:
- exact optimal surplus/rate of gain is unresolved;
- exact carbohydrate need is highly training-context dependent;
- liquid-calorie satiety response is individual;
- body-composition proxies such as waist/skinfolds are not direct muscle/fat measurements;
- no internal qualified nutrition core exists, so all domain behavior needs fresh applied evaluation.

## Red-team verdict

**PASS FOR PRE-SKILL GATE after corrections.**

No material finding requires a new generic framework or multi-agent architecture. The remaining uncertainties are represented as uncertainty/boundary behavior rather than hidden assumptions.
