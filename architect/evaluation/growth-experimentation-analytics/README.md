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

## Qualification boundary

Public fixtures are for development and regression only. They cannot qualify the candidate because the candidate developer can see them.

Final qualification requires:

- frozen candidate digest;
- sealed held-out fixtures created after freeze;
- grader separated from candidate implementation;
- reproducible execution record;
- no repair using held-out answers.

## Immediate next action

Implement the JSON fixture/output schemas and deterministic runner/grader skeleton, then bind a real candidate adapter. Until an adapter can actually execute the frozen Analytics behavior, no claim of a behavioral PASS is permitted.