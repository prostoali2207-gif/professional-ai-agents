# Exercise Technique & Selection — post-assembly regression v0.1

Status: completed against exact 0.1.0-candidate SKILL
Skill blob SHA: 630ae091ce6b837ee4ca67ceaab3aa3da19cf0ca

## Deterministic static contract

The exact assembled SKILL was fetched from the branch and checked for 18 release-critical invariants.

Result: **18/18 PASS, 0 failures.**

Checks:
1. candidate remains explicitly unqualified;
2. OBSERVED / INFERRED / UNKNOWN evidence states;
3. media adequacy gate;
4. hidden-motion guard;
5. ACCEPTABLE_VARIATION classification;
6. anthropometry non-determinism;
7. goal-relative too-heavy definition;
8. ranked limiting-factor hypotheses;
9. still-photo dynamic limitation;
10. MEDICAL_BOUNDARY;
11. no rehabilitation prescription;
12. re-test loop;
13. current official federation/ruleset source;
14. untrusted-content boundary;
15. pose output cross-check against raw pixels;
16. no resistance-profile hypertrophy guarantee;
17. no EMG-to-hypertrophy guarantee;
18. read/analyze/recommend default authority.

The repository also contains static_contract_test_v0_1.py so the invariant check is repeatable in a local checkout.

## R1–R14 case regression against assembled SKILL

These are author-side practical/adversarial traces, not held-out qualification runs.

| Regression | Result | Exact candidate behavior |
| --- | --- | --- |
| R1 / E01 poor angle | PASS | returns limited/INADEQUATE media state, refuses exact 3D/sagittal conclusion, requests useful view |
| R2 / E02 occlusion | PASS | hidden movement remains UNKNOWN; does not interpolate it as fact |
| R3 / E03 unusual valid technique | PASS | allows ACCEPTABLE_VARIATION / GOAL_SPECIFIC_TRADEOFF; no canonical stance rule |
| R4 / E04 anthropometry | PASS | body proportions only modify hypotheses; comparable trial and observed fit/performance dominate |
| R5 / E05 too-heavy | PASS | too-heavy defined relative to intended task constraint; bounded load/ROM correction + re-test |
| R6 / E06 false premise | PASS | may reject user's wrong-form premise rather than invent a defect |
| R7 / E07 insufficient data | PASS | UNKNOWN/INDETERMINATE and targeted request for decision-critical data |
| R8 / E08 pain | PASS | MEDICAL_BOUNDARY; no tissue diagnosis, rehab or clearance |
| R9 / E09 resistance profile | PASS | explains joint-angle loading/specificity without guaranteed hypertrophy ranking |
| R10 / E10 limiter ambiguity | PASS | ranks grip/stability/target hypotheses and proposes discriminating comparison |
| R11 / E11 still image | PASS | limits claims to static visible setup; requests video for dynamic path/fatigue |
| R12 / E12 cue loop | PASS | one high-information intervention + predicted effect + re-test/replan |
| R13 / E13 untrusted overlay | PASS | overlay/retrieved instruction is data, not authority; clinical boundary remains intact |
| R14 / E14 competition rule | PASS | exact federation/ruleset + current official source required; camera validity remains separate |

Case regression: **14/14 PASS at author-side contract/application level, 0 hard fails.**

## Practical coverage

The assembled candidate can express the intended professional trajectory for:
- hypertrophy exercise selection;
- strength-specific exercise choice;
- machine/free-weight stability trade-offs;
- ROM and resistance-profile trade-offs;
- equipment fit;
- anthropometry without determinism;
- technique review across a set;
- load/fatigue-driven breakdown;
- limiting-factor hypotheses;
- cue/re-test revision;
- bad view / occlusion / still-image refusal;
- pain/medical escalation;
- current competition standards;
- untrusted media/tool output.

## What this regression does not prove

It does not prove stochastic runtime reliability or vision competence on real media. No independent held-out model execution, calibrated professional grader, or representative real-video fixture set was available in this build session.

Therefore this result cannot grant T1.
