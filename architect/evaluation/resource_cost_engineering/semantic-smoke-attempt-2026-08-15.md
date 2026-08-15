# RCE semantic smoke attempt — 2026-08-15

Candidate branch: `candidate/architect-rce-v1.2`
Frozen candidate SHA tested by workflow: `3d3155c50a9cc2e549d5028cf393fe33cab3e23b`
Workflow run: `31869001377`
Evaluation PR: `#2` (trigger-only; never intended to merge)

## Pre-run budget gate

Scope was deliberately limited to `RCE-S1` and `RCE-S2` only.

Planned model usage:
- model: `gpt-5.4-mini`;
- maximum candidate invocations: 2 total, one per case;
- retries: 0;
- full RCE-S1–S10 suite: forbidden until smoke PASS;
- tool rounds: 0;
- stop condition: stop on infrastructure failure and do not widen/retry.

Official OpenAI pricing was checked live on 2026-08-15 before the attempted run. Exact pricing was not embedded as durable policy knowledge.

## Execution evidence

The pull-request workflow checked out the frozen base candidate SHA exactly: `3d3155c50a9cc2e549d5028cf393fe33cab3e23b`.

Deterministic preflight succeeded:

`Ran 16 tests in 0.002s — OK`

The credential gate then failed with:

`OPENAI_API_KEY is not configured; semantic model calls were not attempted.`

Subsequent OpenAI runtime installation and RCE-S1/S2 execution steps were skipped.

Therefore:
- model/API calls executed: **0**;
- semantic cases executed: **0**;
- semantic PASS/FAIL evidence produced: **none**;
- no API billing was incurred by this attempt;
- only the small GitHub Actions preflight job consumed CI time.

## Decision

`RCE SEMANTIC SMOKE: NOT EXECUTED — INFRASTRUCTURE BLOCKER (MISSING EXISTING BYOK CREDENTIAL)`

This is not a behavioral REVISE and not a PASS. The gate behaved correctly by refusing to infer account access or enable billing automatically.

Do not retry this workflow until an eligible existing credential is deliberately available. When that condition becomes true, rerun the same two-case smoke before widening to RCE-S1–S10.
