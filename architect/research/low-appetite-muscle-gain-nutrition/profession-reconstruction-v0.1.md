# Low-Appetite Muscle-Gain Nutrition — profession reconstruction v0.1

Status: pre-SKILL research artifact.
Date: 2026-09-21.

## Target outcome

Design nutrition decision support for a generally healthy adult doing progressive resistance training who wants to gain muscle while minimizing food volume, unnecessary surplus, and the subjective burden of constant fullness.

The target is **not** chronic hunger, aggressive restriction, bodybuilding contest preparation, medical nutrition therapy, or a generic meal-plan generator.

## Reconstructed professional model

The closest real professional model is a **sports/performance nutrition practitioner with resistance-training hypertrophy specialization**, plus bounded competence in:

- energy-balance and weight-gain decisioning;
- protein adequacy for resistance-training adaptation;
- carbohydrate/fat allocation for performance and dietary feasibility;
- appetite/satiety and dietary energy-density engineering;
- longitudinal measurement and uncertainty management;
- supplement evidence appraisal;
- clinical red-flag recognition and escalation.

A general nutrition-science role alone is insufficient because the practitioner must connect diet to resistance-training performance and hypertrophy. A generic bodybuilding coach role is insufficient because unsupported heuristics, supplement culture, and aggressive surplus practices are not acceptable evidence. A clinical dietitian/physician role is **not** reconstructed into the agent; clinical diagnosis and medical nutrition therapy stay outside authority.

## Professional responsibilities

1. Determine whether current intake is plausibly sufficient for muscle gain without treating a calorie calculator as ground truth.
2. Establish a protein intake that is sufficient but not wastefully high when appetite is constrained.
3. Allocate fat and carbohydrate in a way that preserves health, energy density, food preference, and training performance.
4. Reduce meal volume using evidence-compatible energy-density tactics before escalating total eating burden.
5. Use meal frequency/timing only when it improves adherence, protein distribution, or training performance; never as metabolism folklore.
6. Track body-mass trend, intake/adherence, appetite burden, training performance, and relevant side effects over time.
7. Make the smallest justified nutrition change and evaluate it over a sufficient observation window.
8. Resist single-weigh-in reactions and false precision in logged calories or expenditure estimates.
9. Bound supplement use to evidence-supported, legal, non-clinical options; food strategy remains primary.
10. Stop and escalate when poor appetite or weight change may reflect a medical, psychiatric, gastrointestinal, endocrine, swallowing, medication, or malnutrition problem.

## Critical decisions and tacit cues

A strong practitioner notices:

- the user can be eating "clean" and protein-heavy yet unintentionally suppress intake through high-volume, high-fiber, low-energy-density choices;
- a person can meet protein needs but still fail to gain because total energy is insufficient;
- adding more protein after an adequate protein target may worsen satiety without adding meaningful hypertrophy benefit;
- short-term scale changes are dominated by glycogen, water, sodium, bowel contents, and measurement conditions;
- a calculated "surplus" is only an estimate until multi-week body-mass response is observed;
- faster weight gain can produce disproportionately more fat rather than more hypertrophy;
- carbohydrate needs depend on training demand and fed/fasted context rather than a single bodybuilding number;
- liquid or semi-solid energy can be useful for some low-appetite users but is not guaranteed to bypass satiety;
- meal frequency is a tolerance/adherence lever, not a universal anabolic rule;
- low appetite can be a benign trait, but persistent appetite loss with unintentional weight loss or other symptoms changes the task into a clinical one.

## Scope classes

### CORE
- energy sufficiency and rate-of-gain control;
- protein target and practical distribution;
- fat/carbohydrate allocation;
- low-volume/high-energy-density food architecture;
- appetite/satiety trade-offs;
- trend-based adjustment under measurement error;
- adherence-aware minimal-change control loop.

### BOUNDARY-CRITICAL
- micronutrient/fiber/hydration adequacy while increasing energy density;
- supplement evidence and safety boundary;
- clinical red flags, low energy availability, and eating-disorder/malnutrition escalation;
- food allergies/intolerances and medication/symptom conflicts.

### CONTEXTUAL
- cultural/religious food constraints;
- budget, cooking access, schedule, travel;
- specific training time and session volume;
- current body composition goal and tolerance for fat gain.

### ESCALATION
- suspected disease, clinically significant appetite loss, persistent GI symptoms, dysphagia;
- unintentional weight loss or malnutrition risk;
- suspected eating disorder/disordered eating;
- pregnancy, minors, medically complex patients;
- renal/hepatic disease, diabetes or other conditions where protein/energy/supplement advice may require clinician oversight;
- prescription appetite stimulants or medication changes.

### OUT OF SCOPE
- diagnosis or treatment of disease;
- prescription-drug changes;
- contest-prep dehydration;
- anabolic steroids/PED protocols;
- guaranteed rates of muscle gain;
- replacing a registered dietitian/physician for clinical nutrition.

## Architecture implication

A single modular applied skill is sufficient. The domain does not justify a multi-agent system by default. Independent external evidence and later qualification can provide critique without splitting runtime responsibility.

## Professional authority

The skill may provide information, analysis, and bounded recommendations for generally healthy adults. It must not present clinical screening as diagnosis, and it must not continue ordinary mass-gain optimization when an escalation condition is material.
