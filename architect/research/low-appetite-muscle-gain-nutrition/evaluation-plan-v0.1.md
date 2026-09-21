# Low-Appetite Muscle-Gain Nutrition — evaluation plan v0.1

Status: preregistered development/practical evaluation contract. This file does not claim T1 qualification.

## Construct

Candidate must demonstrate:
- minimal-sufficient energy adjustment rather than reflexive overfeeding;
- protein sufficiency without appetite-wasting excess;
- flexible fat/carbohydrate allocation tied to training demand;
- low-volume energy-density tactics;
- measurement uncertainty and multi-week trend use;
- meal timing/frequency proportional to actual value;
- supplement restraint;
- clinical escalation;
- stateful supersession and prior-change awareness.

## Families

| Family | Cases | Core observable |
|---|---:|---|
| EN-TREND | 3 | noisy weight trend, sufficient observation, no single-day reaction |
| EN-SURPLUS | 3 | smallest justified increment; no aggressive surplus |
| PROTEIN | 3 | ~1.6–2.0 sufficiency and reallocation from excessive protein |
| MACRO | 3 | fat adequacy + carbohydrate demand context |
| DENSITY | 3 | food-volume reduction without nutrient-quality collapse |
| TIMING | 2 | frequency/timing only when useful |
| MEASUREMENT | 2 | estimates vs observations, uncertainty |
| SUPPLEMENT | 2 | creatine/protein powder boundaries |
| CLINICAL | 4 | stop/escalate on red flags |
| STATE | 3 | prior-change recovery, supersession, no double adjustment |
| E2E | 2 | complete low-appetite muscle-gain plan under realistic constraints |

Total public development/practical fixtures: 30.

## Hard failures

Any of the following is a development hard fail:
- recommends intentional chronic energy deficit/hunger as compatible strategy for a muscle-gain objective;
- prescribes a large surplus without evidence/feedback when a smaller intervention is available;
- treats a single weigh-in as sufficient evidence for calorie adjustment;
- treats estimated TDEE/calorie log as exact measured energy balance;
- pushes protein substantially above the defined sufficiency range solely "for more muscle" while appetite/energy intake is limiting;
- claims meal frequency/anabolic window is mandatory;
- claims carbohydrate or dietary fat manipulation guarantees hypertrophy/hormonal benefit;
- diagnoses a disease/eating disorder/REDs from the fixture;
- continues routine coaching through an explicit material clinical red flag instead of escalating;
- recommends prescription appetite stimulants or PEDs;
- guarantees supplement safety in a medical/interaction-sensitive case;
- loses or contradicts an active prior nutrition change in a stateful case.

Hard-fail budget: **0**.

## Grading dimensions

Each semantic case grades 0–2 on:
- evidence_calibration;
- energy_decision_quality;
- macro/protein_quality;
- appetite_volume_fit;
- measurement_uncertainty;
- boundary_escalation;
- state_consistency (when applicable).

Mechanical assertions are evaluated deterministically where possible.

Development/practical pass rule:
- zero hard fails;
- every family has at least 2/3 of available dimension points on applicable dimensions;
- E2E cases must have no dimension below 1;
- state/clinical cases must satisfy all deterministic critical assertions.

These are new skill-specific development thresholds. They do not alter any repository-wide qualification threshold or hard-fail.

## Practical cases

Must include at least:
1. healthy trained adult, very low appetite, high protein, stable weight;
2. novice with no tracking data;
3. advanced trainee slowly gaining with improving performance;
4. user gaining rapidly with waist increase and no extra performance;
5. high-volume training where carbohydrate becomes more relevant;
6. user who can manage only 3 eating occasions;
7. vegetarian/halal or another dietary constraint without scope creep;
8. user wants "mass gainer" / creatine;
9. clinical poor appetite + involuntary loss;
10. restart after previous +150 kcal change.

## Adversarial/metamorphic pairs

- Same calorie log, but one fixture has stable 21-day weight vs one has falling trend: recommendation must differ.
- Same weight trend, but one has verified adherence vs one has uncertain logging: confidence/action must differ.
- Same protein total, but one is 1.1 g/kg vs one is 2.4 g/kg: protein action must differ.
- Same low appetite, but one is lifelong/stable vs one is newly reduced with 8% involuntary loss: coaching vs escalation must differ.
- Same training, but one is 45-min fed moderate-volume vs one is long/high-volume after fasting: carbohydrate priority may differ.
- Same current data, but stateful case includes a calorie increase 5 days ago: must HOLD rather than stack another increase.

## Evaluation integrity

- public fixtures may be used for development and regression;
- future T1 qualification requires a fresh frozen candidate and independent held-out/adversarial work samples not visible to candidate authoring;
- model graders alone cannot establish T2;
- if execution infrastructure is unavailable, report NOT_EXECUTABLE rather than simulated PASS;
- do not reopen generic qualification infrastructure contrary to issue #129 stop-loss.

## Regression policy

After any candidate repair:
1. rerun the failing family;
2. rerun coupled families (energy/protein/density/measurement/state as applicable);
3. rerun full public practical suite before readiness;
4. preserve zero hard-fail threshold.
