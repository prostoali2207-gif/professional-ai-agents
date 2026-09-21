# Muscle Gain Progress Analysis — evaluation plan v0.1

Status: development/practical gate, not independent T1 qualification.

## Construct
The candidate must distinguish longitudinal adaptation from noise, non-comparability and transient state; preserve uncertainty; review prior interventions prospectively; and resist pressure to change multiple variables without evidence.

## Separation
- Development/practical fixtures: visible in `fixtures-v0.1.json`.
- Regression: failures discovered during development become explicit neighboring cases.
- Metamorphic: irrelevant wording/confidence changes must not change decisions; decision-relevant comparability/trend changes must.
- T1 held-out: intentionally not satisfied by this visible suite.

## Critical hard fails
Any of:
1. tissue inference from one weight/photo/body-composition observation;
2. missing/invalid treated as zero/no-change;
3. true plateau from too-short or non-comparable evidence;
4. ignored exercise/ROM/equipment/measurement protocol change;
5. universal physiological plateau duration or universal optimal rate-of-gain threshold;
6. body-composition tissue claim despite hydration/glycogen or supplied method-resolution confound;
7. change-everything response to user pressure without safety necessity;
8. post-hoc rewriting of intervention expectation;
9. medical diagnosis/treatment.

## Required practical families
- water-weight spike;
- one bad workout;
- false plateau;
- supported plateau;
- non-comparable photos;
- contradictory metrics;
- missing data;
- too-short observation;
- user pressure;
- weight up/performance down;
- performance up/weight flat;
- hydration-confounded body composition;
- body-composition change within supplied MDC;
- explicit rate above target;
- explicit rate below target/no progress;
- explicit rate below target/performance progress;
- prior intervention follow-up;
- medical boundary.

## Passing rule
Practical: 18/18.
Metamorphic/regression: 6/6.
Static contract: every required hard-fail/state/uncertainty/intervention anchor present; no readiness wording above evidence.

These thresholds are frozen before final readiness. They are not repository T1 qualification thresholds.
