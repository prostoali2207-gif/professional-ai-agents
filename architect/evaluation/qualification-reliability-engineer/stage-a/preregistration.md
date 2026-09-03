# QRE v0.1 Stage A — deterministic evaluator-harness preregistration

Status: **PREREGISTERED BEFORE STAGE-A EXECUTION**
Issue: #269
Date: 2026-09-03

## Execution-chain identity

- frozen candidate: `qualification-reliability-engineer-core` `0.1.0-candidate`
- candidate merge commit: `faafd25b554bcff2c22c30f8edbf76a895f05298`
- freeze-record merge commit: `ed2e69405209813005ef08b1b4f086e011c3b2c8`
- stage: `A_DETERMINISTIC_CANDIDATE_HARNESS_PROOF`
- evaluator cycle: `qre-v01-independent-stage-a-r1`
- evaluator/transport path: `GitHub Actions + Python deterministic evaluator harness; provider/model execution forbidden`
- technical repair consumed: `false`
- eligible technical repair under stop-loss if Stage A itself fails: at most one bounded evaluator-harness repair + exact regression + one final Stage-A retry

This is a fresh qualification stage. It does not reuse candidate-authoring judgments as release evidence and does not authorize Stage B/C/D.

## Frozen identities to verify mechanically

The harness must verify both the frozen source commit and the checked-out files against `candidate-freeze-v0.1.json` for:

- candidate `SKILL.md`;
- professional model;
- readiness-report schema;
- readiness validator;
- supporting guard regression;
- qualification-plan identity.

Any behavior-bearing mismatch is Stage-A FAIL/NOT_EXECUTABLE, not a reason to patch the candidate.

## Stage-A claims and executable evidence

1. **Freeze identity is exact.**
   - verifier: Git object/blob comparison against the freeze record and working-tree `git hash-object`.
2. **Packaged guard is executable without provider/model/network access.**
   - verifier: compile + packaged guard regression + evaluator execution with outbound Python socket/URL functions patched to fail.
3. **Evaluator harness rejects stale/cross-run evidence.**
   - verifier: synthetic evidence envelope with wrong run id, candidate commit, or evaluator cycle must fail closed.
4. **P0/mechanical unsafe `GO` paths fail closed.**
   - verifier: synthetic open-P0, failed artifact identity, unauthorized storage, and exhausted stop-loss cases must be rejected.
5. **The harness discriminates fail-open mutations.**
   - verifier: replace the candidate validator with a deliberately permissive fake; evaluator self-test must detect that unsafe cases were accepted.
6. **The harness does not over-block a valid negative control.**
   - verifier: valid `GO` with no P0 and only accepted P1/P2 backlog remains allowed.

## Resource contract

- candidate/model calls: `0`
- judge/model calls: `0`
- provider API calls: `0`
- metered API calls: `0`
- live canary calls: `0`
- parallel provider-heavy work: prohibited
- Stage-A wall-clock CI limit: 5 minutes per dedicated job

A dependency-download by GitHub Actions is not professional/provider evaluation evidence. The evaluator code path itself must remain network-independent and is tested with outbound Python network calls disabled.

## Stage-A verdict rule

`PASS` only if all frozen-identity checks, packaged regressions, network-disabled execution, stale-identity tests, P0 fail-closed tests, mutation/discrimination tests, and valid-GO negative control pass.

Any failure is classified before repair. Do not spend a model/provider call to diagnose Stage A.

Stage-A `PASS` authorizes only preparation of Stage B calibration/construct-validation with a separately recorded execution-chain budget. It does not qualify the candidate.
