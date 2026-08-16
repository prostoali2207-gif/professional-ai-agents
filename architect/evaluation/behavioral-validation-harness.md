# Behavioral Validation Harness Contract

Status: required infrastructure for critical behavioral release claims.

## Purpose

A behavioral evaluation is not valid merely because a test case is well written. Critical claims about state, memory, tools, security, recovery, portability, or reliability require an execution environment that can expose and grade the relevant behavior.

This contract defines the minimum harness needed for Agent Architect v1.1 and for future applied agents when comparable claims are made.

## Core rule

For every P0/P1 behavioral claim, define:

`claim -> executable fixture -> observable actions/state -> grader -> threshold -> run record`.

If any link is missing, the result is `NOT EXECUTABLE` or `DIAGNOSTIC ONLY`, never PASS.

## Required harness capabilities

The harness must provide, when required by the case:

1. **session isolation** — start a fresh candidate session with explicitly controlled prior state;
2. **persistent-state inspection** — inspect memory/state before and after the run without trusting the candidate's prose report;
3. **checkpoint isolation** — resume from a checkpoint while withholding the original transcript when the test is about checkpoint sufficiency;
4. **controlled tools** — return deterministic, delayed, stale, conflicting, partial-success, or ambiguous results as pre-registered by the fixture;
5. **side-effect ledger** — mechanically record writes/sends/deletes/deploys or other non-idempotent effects so duplicates can be detected;
6. **capability instrumentation** — record which skills/resources/tools were selected or loaded;
7. **capability degradation** — remove a declared capability and rerun an equivalent task;
8. **hidden/held-out fixture support** — keep attack strings, grader keys, or decisive fixture details unavailable to the candidate before execution;
9. **trial isolation** — run repeated equivalent trials without carrying accidental state across trials;
10. **version capture** — record candidate SHA, model/runtime, tool versions, fixture version/hash, grader version, and capability profile.

## Observable run record

Each run record must contain enough external evidence to reconstruct behavior without hidden chain-of-thought:

- run ID and timestamp;
- candidate version/SHA;
- fixture ID and immutable hash or sealed-fixture reference;
- capability profile;
- initial inspectable state;
- user/task inputs visible to the candidate;
- tool calls and tool results;
- state writes/updates/deletions;
- side effects and reconciliation checks;
- capability/resource loads;
- checkpoint artifact when relevant;
- final externally observable state;
- termination reason;
- grader outputs;
- pass/fail and failure class.

## Grader classes

Use the strongest available grader for the claim.

- **mechanical grader** — preferred for duplicates, state contents, tool/resource selection, permissions, end-state invariants, exact structured outputs;
- **environment verifier** — preferred for downstream effects that must exist outside the candidate;
- **independent calibrated evaluator** — needed for judgment-heavy outputs and competence inference;
- **self-evaluation** — diagnostic only for P0/P1 release decisions unless independently corroborated.

A polished explanation from the candidate is never a substitute for inspectable state or side-effect evidence.

## Failure taxonomy

Classify failures at minimum as:

- task-understanding failure;
- state/memory write failure;
- retrieval/use failure;
- supersession/contradiction failure;
- checkpoint/compaction loss;
- progress-detection/replanning failure;
- unsafe retry/idempotency failure;
- authority/trust-boundary failure;
- memory/skill poisoning failure;
- capability-selection/load failure;
- degraded-runtime portability failure;
- evidence-validity/competence-inference failure;
- reliability/variance failure;
- harness/fixture invalidity.

A harness/fixture invalidity blocks conclusion; it is not a candidate PASS or FAIL.

## Repair discipline

On a genuine candidate failure:

`failure -> evidence -> root-cause layer -> repair -> regression -> fresh held-out variant -> coupled critical-family rerun`.

Do not repair by teaching the exact hidden answer or attack string.

On a harness failure:

`invalidate run -> repair harness/fixture -> re-freeze manifest -> rerun candidate`.

Do not score behavior observed under an invalid experimental setup.

## Release rule

No P0/P1 family may be marked PASS unless:

- the relevant harness capability actually existed during execution;
- fixture/version/threshold were frozen before observing the scored output;
- the required external state or action trace was captured;
- the grader type matches the construct being claimed;
- repeated trials were performed where reliability is part of the claim;
- no critical failure was hidden by averaging.

If the current platform cannot supply the required harness capability, narrow the claim or keep release status at REVISE.