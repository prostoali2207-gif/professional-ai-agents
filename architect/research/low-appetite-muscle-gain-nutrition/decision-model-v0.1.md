# Low-Appetite Muscle-Gain Nutrition — decision model v0.1

Status: pre-SKILL professional decision architecture.

## 1. Applicability gate

Proceed with ordinary mass-gain decision support only when:
- adult;
- goal is muscle/strength gain alongside resistance training;
- no material clinical red flag is present;
- user is not asking to preserve chronic hunger or intentional under-fueling;
- no condition/medication/pregnancy/minor status makes individualized medical nutrition the controlling problem.

Otherwise enter escalation policy in `runtime-state-and-escalation-v0.1.md`.

## 2. Minimum input model

Classify each item as OBSERVED, USER-REPORTED, ESTIMATED, UNKNOWN, or SUPERSEDED.

Decision-critical inputs:
- current body mass and available recent body-mass series;
- weighing conditions;
- recent estimated intake and logging method, if available;
- protein estimate;
- training frequency, approximate session demand, and at least one performance trend;
- appetite burden/tolerance;
- recent unintentional weight loss or appetite change;
- relevant GI/swallowing symptoms;
- dietary restrictions/allergies;
- supplements/medications when they materially affect appetite, GI tolerance, or safety.

Useful but non-mandatory:
- waist or other repeatable body-composition proxy;
- meal schedule;
- sleep/recovery notes;
- current food pattern.

A calorie calculator or wearable may initialize a prior. It never converts estimated maintenance into observed maintenance.

## 3. Weight-trend model

Preferred measurement:
- repeated morning weights under reasonably similar conditions;
- use a 7-day rolling mean/median for display;
- estimate directional slope over at least 14 days when feasible, preferably 21 days when noise/adherence is high;
- compute weekly relative rate as `(kg/day slope * 7 / representative body mass) * 100`.

Do not adjust intake from one isolated weight.

Short-term confounders include hydration, sodium, carbohydrate/glycogen, bowel contents, travel, illness, and scale/measurement conditions.

## 4. Energy-balance controller

### A. Insufficient evidence
If there is <14 days of reasonably comparable weight data and no clear involuntary loss:
- do not infer exact maintenance;
- establish a tolerable baseline intake and measurement routine;
- avoid large pre-emptive surplus.

### B. Likely insufficient intake
If for >=14 days:
- body-mass trend is flat/down;
- intake adherence is reasonably established;
- resistance training is being performed;
- protein is already adequate or close;
then add the **smallest practical energy unit**.

Default energy unit is an operational heuristic, not a physiological law:
- about 5% of current estimated intake, often roughly 100–200 kcal/day;
- prefer increasing energy density rather than meal volume;
- do not add protein if protein is already sufficient unless food architecture requires it.

Reobserve before another increase unless there is a clear safety reason to escalate.

### C. Adequate response
If body mass trends upward and training performance/recovery is stable or improving:
- HOLD intake;
- do not add calories solely because the gain rate is below a bodybuilding heuristic.

### D. Excessive response
If a sustained trend is clearly rapid, or waist/skinfold proxy rises disproportionately without corresponding training benefit:
- first verify measurement/adherence;
- then remove one small energy unit rather than making a large cut.

## 5. Rate-of-gain interpretation

Evidence supports avoiding aggressive gain, but not one universal optimum.

Use `~0.25–0.5% body mass/week` only as an **evidence-informed reference band / upper operating context**, scaled downward with training experience. It is not a mandatory minimum.

For an advanced or strongly low-appetite user:
- a slower positive trend can be acceptable if training adaptation is occurring;
- the system's objective is the lowest intake that supports useful adaptation, not hitting a scale-speed quota.

Never promise that a given surplus or rate will produce a particular amount of muscle.

## 6. Protein decision

Default for generally healthy resistance-training adults:
- aim around **1.6 g/kg/day**;
- working range **~1.6–2.0 g/kg/day** when practical;
- do not push toward the upper end merely because more is mathematically possible.

When appetite is constrained and intake is already >~2.0 g/kg/day:
- consider reducing toward sufficiency and reallocating energy to carbohydrate/fat;
- preserve total calories and training support.

Distribution:
- daily total has priority;
- use roughly 3–4 protein opportunities when convenient;
- a practical per-opportunity range around ~0.3–0.4 g/kg can be used, but failure to hit perfectly even distribution is not a reason to increase food burden;
- pre/post-workout timing is flexible inside the day; no narrow anabolic-window rule.

If actual-body-weight multiplication produces implausibly high targets because of very high adiposity or a clinical context, do not mechanically apply it; escalate or use a professionally justified alternative basis.

## 7. Fat and carbohydrate decision

### Fat
- ordinarily keep within health-compatible athlete guidance, roughly **20–35% of total energy**;
- with low appetite, the middle/upper part of that range can be useful for energy density when tolerated;
- favor a varied pattern containing essential fats; do not make a low-fat diet a virtue;
- do not claim higher fat intake is a testosterone/hypertrophy hack.

### Carbohydrate
- after protein and fat adequacy, carbohydrate can take the remaining energy according to preference and training demand;
- ordinary fed resistance training does not require endurance-style carbohydrate numbers;
- increase carbohydrate priority for long/high-volume sessions, repeated sessions, glycogen depletion, fasted training, or when performance clearly responds to it;
- do not claim more carbohydrate independently guarantees more hypertrophy.

## 8. Low-volume/high-energy-density ladder

Use the least disruptive level that solves the intake gap.

### Level 1 — densify existing meals
Examples when appropriate:
- full-fat instead of low-fat dairy;
- add olive oil, tahini, nut/seed butter, cheese, avocado, sauces;
- choose denser starches/breads/cereals rather than very bulky low-calorie substitutes;
- use dried fruit or juice as additions where nutritionally appropriate.

### Level 2 — reduce avoidable satiety burden
Without removing diet quality:
- move very large raw-vegetable/fiber-heavy portions away from hardest eating windows if they suppress intake;
- prefer cooked/compact produce when better tolerated;
- avoid turning every meal into a high-protein/high-fiber "diet food" meal.

### Level 3 — small liquid/semi-solid module
If individually better tolerated:
- milk/yogurt-based shake, protein powder only as needed, fruit, nut butter, honey or other tolerated ingredients;
- use a deliberately sized energy module rather than an uncontrolled "mass gainer".

Liquid calories are an option, not a claim that liquids are universally less satiating.

## 9. Meal timing/frequency

Use timing only for:
- tolerance/appetite;
- distributing sufficient protein;
- avoiding training while uncomfortably full;
- supporting unusually long/high-volume training;
- convenience/adherence.

Do not require six meals/day. Three meals, or another workable frequency, can be valid if the total target is achieved and the person tolerates it.

## 10. Food-quality adequacy

Energy density must not collapse the diet into oils/sugar/protein powder.

Preserve:
- sufficient micronutrient diversity;
- fruit/vegetable and fiber intake compatible with current reference values and GI tolerance;
- hydration and sodium appropriate to conditions;
- a meaningful proportion of minimally processed/nutrient-dense foods.

Retrieve current age/sex/jurisdiction-specific reference values live when exact micronutrient/fiber requirements materially affect the decision.

## 11. Supplement boundary

Default hierarchy:
1. food architecture;
2. protein powder only as a convenience tool when useful;
3. creatine monohydrate may be offered as an optional evidence-supported ergogenic aid for appropriate healthy adults, commonly 3–5 g/day;
4. no supplement is allowed to substitute for adequate energy/protein/training.

Do not:
- create broad supplement stacks by default;
- recommend prescription appetite stimulants;
- guarantee supplement safety for kidney/liver disease, pregnancy, minors, medication interactions, or other clinical contexts;
- treat creatine-associated scale changes as muscle tissue without qualification.

## 12. Change discipline

Prefer one primary nutrition change per observation cycle when practical.

Every change record should include:
- why change is needed;
- exact small change;
- expected signal;
- observation window;
- what would trigger HOLD / INCREASE / DECREASE / ESCALATE.

This is a feedback controller, not a static diet prescription.
