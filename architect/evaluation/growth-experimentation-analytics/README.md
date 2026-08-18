# Growth Experimentation & Measurement — evaluation harness

Status: development harness specification; not release-ready.

## Goal

Provide a reusable execution and grading boundary for Growth Experimentation & Measurement candidates without depending on one business, repository, model provider, or chat product.

The harness must:

1. accept one candidate-facing experiment fixture;
2. execute one externally supplied frozen candidate;
3. require one structured decision result;
4. run deterministic checks before any residual judgment;
5. record candidate version, fixture version and runtime metadata;
6. fail closed when the candidate cannot produce a valid result.

## Repository boundary

This repository stores only reusable evaluation infrastructure, generic development fixtures, schemas and qualification rules.

It must not store:
- manifests that identify one downstream business candidate;
- customer or project experiment data;
- provider credentials;
- project-specific remediation reports;
- sealed held-out qualification material intended to remain private.

A downstream project supplies its own frozen candidate manifest at execution time through `ANALYTICS_CANDIDATE_MANIFEST`.

## Directory contract

- `fixtures/` — generic public development cases.
- `schemas/` — candidate-facing input/output contracts.
- `runner.py` — executes a candidate adapter against fixtures.
- `grader.py` — deterministic development grader.
- `adapters/` — provider-neutral execution boundaries.
- `runs/` — generated local artifacts only; never commit secrets, customer PII or sealed exam content.

## Candidate interface

The runner passes one fixture to an adapter. The adapter loads an externally supplied frozen candidate manifest and invokes an eligible runtime.

Minimum output fields:
- `fixture_id`;
- `recommendation`: `CONTINUE | ITERATE | SCALE | KILL | INCONCLUSIVE`;
- `data_integrity_findings[]`;
- `computations[]`;
- `claim_boundaries[]`;
- `confounders[]`;
- `rationale`;
- `next_action`.

Each material computation exposes inputs, method and result. Unsupported narrative arithmetic is not sufficient when the decision depends on the calculation.

## Grading order

1. schema validity;
2. deterministic arithmetic/state checks;
3. forbidden decision/claim checks;
4. required decision-state checks;
5. claim-boundary checks;
6. only residual judgment that cannot be made deterministically may use a separate reviewer.

## Development vs qualification — hard separation

Public fixtures and any fixture whose expected behavior or grader rule is visible during implementation are development/regression tests only.

They may find defects, verify repairs and prevent regressions. They must not be presented as final qualification, even if another model family executes them.

## Final qualification protocol

Final qualification requires:

1. freeze the assembled candidate and record its digest/version;
2. create fresh held-out cases after freeze;
3. keep held-out cases and grading keys outside candidate/developer context until execution;
4. execute without repair between held-out cases;
5. keep grader material separate from candidate execution;
6. preserve reproducible run metadata;
7. burn any held-out case that becomes visible and is then used for repair.

Manual execution in a clean external chat can be used as transport when API execution is unavailable, but this does not weaken the separation rules.

## Next gate

Keep this harness generic. Candidate-specific baselines, remediation notes and business integration belong in the downstream project. Package a reusable professional core only after development behavior is stable and sealed qualification passes.
