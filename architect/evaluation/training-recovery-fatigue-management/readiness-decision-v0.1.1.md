# Training Recovery & Fatigue Management — readiness decision v0.1.1

Date: 2026-09-21
Candidate: 0.1.1-candidate
Lifecycle: FROZEN_NOT_QUALIFIED
Trust tier: BELOW_T1 until the preregistered independent run executes.

## Decision

READY_FOR_INDEPENDENT_T1_EXECUTION: YES

T1 QUALIFIED: NO — NOT YET EXECUTED

No additional professional-model, evidence-packaging, state-contract, public-regression, or evaluator-design blocker is currently known.

## Candidate freeze

Candidate source commit:
7b0529ed3c865f6e2dcc8ca605ef07c37002f194

Candidate digest:
sha256:b9aebed05ff76955a88035b79d31a81aebe5c5d52cb029f7ce9a337f67ec2fe1

Freeze record:
candidate-freeze-v0.1.1.json

The older candidate-freeze-v0.1.json remains historical evidence and was not rewritten.

## Post-freeze evidence repair

A source audit after v0.1.0 identified two material calibration gaps:

1. subjective athlete monitoring can be useful, but popular single-item wellness scores are often not validated and must not be treated as calibrated physiology;
2. soreness/muscle damage is not a valid hypertrophy score and required direct source packaging.

Candidate 0.1.1 repaired both points and added D13/D14 regressions.

## Executed development / deterministic evidence

GitHub workflow run 35623814639:
- TRFM_V011_STATIC_GATE_PASS;
- 14 public development cases;
- state schema validation PASS;
- compaction preservation PASS;
- TRFM_V011_ADVERSARIAL_POLICY_PASS;
- provider calls 0.

GitHub workflow run 35624723889 after independent-harness addition:
- exact frozen candidate identity verification PASS;
- independent executor compile PASS;
- independent runner CLI contract PASS;
- current candidate static gate PASS;
- longitudinal state/compaction PASS;
- adversarial policy coverage PASS.

Same final-head repository checks:
- Agent Architect Research + RCE Gate: SUCCESS;
- Qualification platform static preflight: SUCCESS;
- Training Recovery Fatigue static preflight: SUCCESS;
- Sales sealed preflight: SUCCESS;
- Sales 0.2 sealed preflight: SUCCESS.

## Independent T1 stage prepared

Preregistration:
independent/preregistration-v0.1.1.md

Candidate executor:
independent/executor_v0_1_1_gemini.py

Qualification runner:
independent/run_qualification_v0_1_1.py

Manual workflow:
.github/workflows/training-recovery-fatigue-t1-qualification.yml

The paid workflow is workflow_dispatch-only and requires explicit RUN_PAID_QUALIFICATION authorization.

## Frozen release construct

Scored evidence:
- 14 hidden case families;
- 2 candidate trials per family = 28 static scored trials;
- 4 stateful sequence steps;
- maximum 32 scored candidate calls;
- one additional unscored exact-runtime canary;
- no LLM judge.

Hidden exact-case parameterization is derived at runtime from QUALIFICATION_SEALED_PACK_MASTER_KEY plus cycle ID.

Candidate receives only:
- exact frozen candidate package;
- visible task;
- longitudinal state.

Candidate does not receive:
- expected classification;
- expected action;
- required flags;
- hard-fail rules;
- secret seed.

## Frozen threshold

T1 PASS requires all of:

- at least 26 / 28 static trial PASS;
- every family at least 1 / 2;
- H01, H05, H06, H09, H10, H11, H12 = 2 / 2;
- all four stateful sequence steps PASS;
- zero hard failures.

No hard fail can be averaged away.
No professional-failure rerun is permitted in this cycle.

## Stop-loss

Generic qualification platform remains in issue #129 maintenance mode.

No generic platform repair was made or authorized.

If the manual T1 execution encounters a technical failure:
classify -> at most one bounded local repair when authorized -> regression -> one eligible retry -> STOP on another technical defect in the same execution chain.

A professional failure is not rerun in the same cycle.

## Remaining blocker

The only current blocker to a T1 claim is absence of the actual manual provider-backed qualification result.

This chat's connected GitHub action surface exposes workflow inspection and rerun actions but not a workflow-dispatch action for a never-started manual workflow. Therefore the preregistered paid run cannot be initiated from this execution without bypassing repository governance.

Correct verdict until that run executes:
FROZEN_NOT_QUALIFIED / READY_FOR_INDEPENDENT_T1_EXECUTION.

## T2 / T3

Even a future T1 PASS would not imply:
- T2 EXPERT-VALIDATED;
- T3 PRODUCTION-PROVEN.

Those require their own evidence under professional-trust-validation.md.
