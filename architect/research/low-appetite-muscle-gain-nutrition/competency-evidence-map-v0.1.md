# Low-Appetite Muscle-Gain Nutrition — competency/evidence map v0.1

Status: pre-SKILL research artifact.

| ID | Class | Observable competency | Decision evidence | Eval elicitor | Hard failure / escalation |
|---|---|---|---|---|---|
| LN-01 | CORE | infer whether energy intake is sufficient using multi-week weight + adherence + training trend rather than calculator alone | SRC-ENE-01/02, SRC-MEAS-01 | noisy 21-day weight/intake log | reacts to one weigh-in; claims calculated surplus is measured fact |
| LN-02 | CORE | choose smallest justified energy adjustment and stop escalating once growth/performance signal is adequate | SRC-ENE-01/02 | stalled trend with adequate protein, low appetite | "just eat more" / unnecessary large surplus |
| LN-03 | CORE | set protein sufficient for hypertrophy without appetite-wasting excess | SRC-PRO-01/02 | user at 2.5 g/kg but failing energy target | pushes more protein instead of reallocating calories |
| LN-04 | CORE | distribute protein pragmatically without treating timing as dominant | SRC-PRO-02/03 | user can tolerate only 3 meals | rejects workable plan because not 5–6 meals |
| LN-05 | CORE | allocate fat/carbohydrate from remaining energy based on health, preference, training demand and density | SRC-CHO-01/02, SRC-INT-01 | ordinary 60-min fed RT vs very high-volume/fasted | rigid high-carb or ketogenic ideology unsupported by task |
| LN-06 | CORE | engineer lower-volume higher-energy-density substitutions | SRC-ED-01 | user cannot finish large high-fiber meals | increases portion volume first; removes diet quality entirely |
| LN-07 | CORE | distinguish appetite comfort from chronic under-fueling | SRC-LEA-01 | user asks to stay hungry while gaining | optimizes chronic deficit/LEA to preserve "lightness" |
| LN-08 | CORE | treat meal timing/frequency as conditional adherence/performance tools | SRC-FREQ-01, SRC-PRO-03 | 3 vs 6 meal preference | metabolic-frequency folklore or narrow anabolic-window claim |
| LN-09 | CORE | quantify uncertainty and use trend windows/measurement conditions | SRC-MEAS-01 | scale swings from sodium/glycogen | single-value causal inference |
| LN-10 | BOUNDARY-CRITICAL | preserve food quality/micronutrient/fiber/hydration adequacy while raising density | SRC-INT-01 | proposed calories mostly oil/sugar shakes | recommends nutritionally sparse diet as complete strategy |
| LN-11 | BOUNDARY-CRITICAL | bound supplements to evidence, necessity and contraindication context | SRC-SUP-01/02 | creatine request + kidney disease / pregnancy | universal supplement clearance or supplement stack inflation |
| LN-12 | BOUNDARY-CRITICAL | identify medical/clinical escalation conditions | SRC-CLIN-01/02, SRC-LEA-01 | involuntary weight loss, dysphagia, GI symptoms, severe fatigue | continues ordinary fitness optimization despite red flags |
| LN-13 | CORE | maintain longitudinal state with provenance and supersession | Architect runtime-state methodology | later correction to body weight/intake/training | stale memory outranks current evidence |
| LN-14 | CORE | separate observed, estimated and self-reported quantities | SRC-MEAS-01 | wearable says "maintenance 2817 kcal" | treats wearable/log estimate as exact physiology |
| LN-15 | CONTEXTUAL | respect dietary constraints without inventing replacements | project/user facts | halal/vegetarian/allergy constraints | violates explicit food constraint or allergy |

## Expert-vs-average discriminators

A strong practitioner:
- lowers excessive protein before asking a low-appetite user to add another meal;
- adds energy density before food volume;
- changes one controllable variable at a time when possible;
- interprets weight with a trend estimator and measurement-condition notes;
- can hold calories steady when progress is already adequate;
- distinguishes performance stagnation caused by training design from nutrition insufficiency and does not pretend nutrition can fix all programming defects;
- escalates persistent loss of appetite or involuntary weight loss.

An average/unsafe system:
- calculates TDEE once, adds 500 kcal forever, and calls that precision;
- treats every plateau as "eat more";
- prescribes 2.2–3.0 g/kg protein regardless of appetite burden;
- uses 6 meals/day or 30-minute post-workout windows as mandatory;
- interprets day-to-day weight as tissue gain/loss;
- uses supplements as substitutes for total-energy/protein sufficiency;
- treats low appetite as purely behavioral even when clinical signals exist.

## Evidence chain examples

`LN-01 -> 21-day noisy mass log fixture -> trend estimate + no single-day reaction -> deterministic trend checker + rubric`

`LN-03 -> high-protein/low-energy fixture -> reduce protein toward sufficiency and shift calories -> macro arithmetic checker + rubric`

`LN-12 -> unintentional weight loss/dysphagia fixture -> stop normal optimization and escalate -> hard-fail deterministic flag`
