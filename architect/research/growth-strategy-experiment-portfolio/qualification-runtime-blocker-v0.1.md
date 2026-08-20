# Strategist qualification runtime blocker v0.1

Date: 2026-08-20
Candidate: `architect/research/growth-strategy-experiment-portfolio/candidate-professional-model-v0.1.md`
Frozen candidate Git blob: `b22bac7a4deed11c466c014f41960f5e2deec2d1`
Status: `BLOCKED_BY_EVAL_RUNTIME`

## What was attempted

### Runtime A — GitHub Copilot SDK

Result: infrastructure failure before fixture generation.

Observed error: monthly Copilot request quota exceeded on the first evaluator request.

Qualification implication:

- no hidden fixture was generated;
- the candidate did not receive a task;
- no professional PASS/FAIL evidence exists from this run;
- candidate remains uncontaminated by generated held-out fixtures.

### Runtime B — existing OpenAI BYOK path

The repository already contains an OpenAI Responses evaluation adapter/workflow pattern.

Result: infrastructure failure before fixture generation because repository secret `OPENAI_API_KEY` is not configured.

Qualification implication:

- no hidden fixture was generated;
- no candidate run occurred;
- this is not a candidate failure.

## Integrity decision

Do not:

- call the candidate qualified;
- call the candidate professionally failed;
- replace held-out execution with same-session self-grading;
- inspect or tune against any future held-out task before its round closes;
- promote the candidate to Professional Core Library or replace the applied UAE Strategist before independent qualification.

## Resume condition

Resume the frozen qualification unchanged when either:

1. GitHub Copilot evaluation quota becomes available; or
2. `OPENAI_API_KEY` is configured for the repository's existing BYOK evaluation path; or
3. another independently controlled model runtime satisfying the same secrecy/run-record requirements is connected.

The frozen candidate blob and public qualification design should remain unchanged for the first valid held-out round unless new profession evidence materially invalidates the model before that round.

## Clean-session fallback if CI runtime cannot be restored

Use three independent clean model sessions with no access to each other's hidden material:

1. **Fixture author** receives only `qualification-design-v0.1.md`, creates fresh adversarial fixtures plus private expected dispositions/grading notes, and does not expose grading notes to the candidate session.
2. **Candidate executor** receives the exact frozen candidate blob plus only fixture task text and returns the declared JSON contract.
3. **Independent grader** receives the public design, task, private grading notes and candidate answer; it scores the frozen rubric and hard-fail flags.

Required evidence record: candidate blob SHA, model/runtime identities, fresh fixture IDs, outputs, grader version, per-dimension scores, critical flags, aggregate threshold result and confirmation that the candidate session never saw hidden grading material.

A same-chat simulation is explicitly non-qualifying.
