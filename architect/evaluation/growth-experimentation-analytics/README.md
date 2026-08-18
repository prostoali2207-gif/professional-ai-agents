# Growth Experimentation & Measurement — evaluation harness

Status: development harness specification; not release-ready.

## Goal

Provide an executable boundary for evaluating Analytics candidates on structured experiment cases without relying on free-form chat judgment.

The harness must:

1. accept one structured experiment fixture;
2. execute one frozen candidate implementation;
3. require one structured decision result;
4. run deterministic checks before any model-based grading;
5. record candidate version, fixture version, tool/runtime version and outputs;
6. fail closed when the candidate cannot produce a valid result.

## Directory contract

- `fixtures/` — public development cases.
- `schemas/` — input/output contracts.
- `runner.py` — executes a candidate adapter against fixtures.
- `grader.py` — deterministic grader for arithmetic, required statuses, forbidden claims and hard-fail rules.
- `adapters/` — candidate-specific execution adapters. The downstream `auto-sales-growth-system/agents/analytics.md` cannot be treated as executable until an adapter binds it to an actual model/runtime.
- `runs/` — generated local artifacts only; do not commit secrets or raw customer PII.

## Candidate interface

Runner calls a candidate adapter with one JSON fixture and expects one JSON result. The adapter is responsible for binding the frozen Analytics instructions plus fixture to an eligible model/runtime.

Minimum output fields:

- `fixture_id`
- `recommendation`: `CONTINUE | ITERATE | SCALE | KILL | INCONCLUSIVE`
- `data_integrity_findings[]`
- `computations[]`
- `claim_boundaries[]`
- `confounders[]`
- `rationale`
- `next_action`

Each computation must include inputs, method/formula label and result. Unsupported narrative arithmetic is not sufficient where a fixture requires computation.

## Grading order

1. JSON/schema validity.
2. Hard-fail checks: fabrication, missing-as-zero, metric switching, invalid denominator, attribution-as-causality, ignored fatal comparability/instrumentation defect.
3. Deterministic calculation checks where fixture provides expected values/tolerances.
4. Required decision-state checks.
5. Claim-boundary checks.
6. Only residual judgment that cannot be deterministically graded may use a separate rubric/reviewer.

## Development vs qualification — hard separation

Public fixtures and any fixture whose expected behavior, answer key, grader rule, or hard-fail condition is visible to the candidate developer are **development/regression tests only**.

They may be used to:
- find defects;
- improve the candidate;
- verify a repair;
- prevent regression.

They must **not** be presented as independent final qualification, even when executed by a different model such as Claude or Gemini. A different model is only a different runtime; it does not turn a known-answer development case into a held-out exam.

A cross-model manual run on public fixtures may provide useful compatibility evidence, but its status must remain `DEVELOPMENT_EVIDENCE`, never `QUALIFICATION_PASS`.

## Final qualification protocol

Final qualification requires all of the following:

1. Freeze the candidate implementation and record its exact digest/version.
2. Only after freeze, create new held-out fixtures that were not used to design or repair the candidate.
3. Keep held-out fixture contents, expected behavior and grading key unavailable to the candidate/developer during execution.
4. Execute the frozen candidate without repair or prompt changes between held-out cases.
5. Keep grader/answer key separate from the candidate execution context.
6. Preserve a reproducible run record: candidate digest, runtime/model, fixture IDs/versions, outputs and grading result.
7. If a held-out case is exposed and then used to repair the candidate, that case is burned and becomes development evidence only; a new held-out case is required.

Manual execution in a clean Claude/Gemini chat is acceptable as an execution transport if the frozen candidate and held-out fixture can be transferred without exposing the answer key. Manual transport does not weaken the separation rule, and the resulting answer must still be graded independently.

## Immediate next action

Use the public fixture suite to develop and repair the current Analytics candidate. Do not prepare a final Claude/Gemini qualification packet from those public fixtures. After the candidate passes development regression, freeze it and then create fresh sealed held-out qualification cases.