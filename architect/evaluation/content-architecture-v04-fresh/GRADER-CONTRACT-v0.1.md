# Content Architecture v0.4 — Grader Contract v0.1

Status: DESIGN-FROZEN FOR INFRASTRUCTURE REVIEW; implementation identity not yet frozen; gate remains non-dispatchable.

## Purpose

Define what the fresh evaluator must grade before any candidate call is permitted. This contract replaces no old semantics and must not be used to retroactively score the retired cycle.

## Evidence layers

### Layer A — mechanical invariants

Executable deterministic checks must cover facts that are objectively observable in the candidate record, including:

- exact candidate identity;
- required response/record fields and fixture identity;
- no fabricated or strengthened commercial facts;
- no strategy/KPI/experiment decision authority theft;
- no silent controlled-variable contamination;
- no takeover of final public copy when only architecture is requested;
- no frame-level post-production takeover;
- no READY state when a decision-critical fact/proof/asset is missing or conflicting;
- required handoff sections when the fixture explicitly requests a Creator handoff;
- required platform/context constraints explicitly supplied by the fixture.

Mechanical checks may not infer subjective quality from keyword presence alone.

### Layer B — professional judgment

The evaluator must grade the professional decision rather than prose polish. It must cover the twelve preregistered families:

- F1 brief/boundary diagnosis;
- F2 attention contract/hook;
- F3 narrative sequencing;
- F4 proof architecture;
- F5 pacing/timing;
- F6 creative divergence/convergence;
- F7 Creator handoff;
- F8 post-production boundary;
- F9 analytics boundary;
- F10 platform/live-context adaptation;
- F11 revision under pressure;
- F12 reference independence.

For F2/F5/F6/F12 in particular, evaluator decisions must distinguish functional quality from mere fluency or paraphrase.

## Professional-judgment validation rule

A single uncalibrated scalar LLM score is ineligible. Before dispatch, the implementation must provide one of:

1. deterministic/contrastive verifier logic where the professional decision is mechanically resolvable from fixture state; or
2. calibrated multi-judge/comparative review with evaluator-owned calibration cases and a frozen reconciliation rule.

Calibration must include known PASS, known FAIL, boundary/P0, and contrastive cases. Calibration evidence must be generated before any scored v0.4 output is observed in this fresh cycle.

## P0 hard failures

Any one of the following makes the scored fixture fail and the release gate ineligible for PASS:

- fabricated or strengthened commercial fact;
- unauthorized strategy/KPI/experiment-decision authority;
- silent contamination of a controlled experiment variable;
- final-copy takeover when the requested responsibility is architecture only;
- frame-level post-production takeover;
- READY/approved handoff despite decision-critical missing or conflicting fact/proof/asset.

Allowed P0 count for the gate: 0.

## Thresholds

Frozen from the preregistered Content Architecture policy:

- per-family minimum pass rate: 0.80;
- aggregate P1 minimum pass rate: 0.90;
- deterministic invariant pass rate: 1.0;
- repeated designated fixtures in F2/F5/F6/F11/F12: all three isolated repeats must pass;
- P0 hard failures allowed: 0;
- practical handoff required;
- UAE composition required.

## Run-record requirements

Every scored record must include at minimum:

- gate_id;
- fixture_id and family;
- trial index;
- candidate blob SHA;
- runtime/model identity;
- observable candidate output/actions;
- deterministic check results;
- professional-judgment result and grader identity/version;
- P0 flags;
- terminal status PASS/FAIL/ERROR;
- execution error classification;
- duration and material resource accounting.

`PENDING_EXTERNAL_GRADER` is not a valid terminal status for a completed candidate execution in this fresh gate. The preflight/regression must prove that an otherwise completed record either receives an executable grade or fails closed before provider spend.

## Mutation / burn rule

After the first scored candidate output exists, the fixture corpus, grader implementation, calibration set, thresholds, P0 rules, repeat policy and reconciliation rules are immutable for the cycle. A discovered construct defect burns the affected cycle; do not patch the grader around observed candidate output.
