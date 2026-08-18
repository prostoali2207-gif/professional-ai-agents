# PM-04 v2 Authentic-Work Results — 2026-08-18

Status: professional-result review; deterministic grader implementation requires repair.

Targeted GitHub Actions run: `32110165071`, job `paid-media-pm04-v2`, Gemini 3.1 Flash Lite.

## Plain result

The current Paid Media Professional Core demonstrated the intended PM-04 professional behavior on all six authentic-work cases. The job's aggregate `FAIL` is not a defensible capability failure because the string-matching grader rejected substantively correct answers for wording/representation differences.

### PM04V2-01 — power/sample size

Agent answer: approximately **8,150 users per arm**. Independent reference calculation used by the fixture: approximately **8,158 per arm** under the stated normal approximation. Numeric check passed. The answer also stated independence/no-interference assumptions and recommended a pre-registered sample size. Grader falsely failed because it searched for the literal token `random...` and a narrow analysis-plan phrase rather than accepting the explicit task premise plus `pre-registered sample size`.

Professional judgment: PASS for the tested slice.

### PM04V2-02 — cluster randomization

Agent correctly stated that city is the randomization unit, session-level testing is invalid because it ignores intra-city correlation, N=8 cities is a small/low-power cluster sample, and city-level/cluster-appropriate analysis is required. It proposed aggregation and permutation/DiD approaches.

Grader falsely failed because it expected narrow exact phrases such as `not independent` / `cluster-aware` and numeric_answer=8 even though the response said the same thing in professional language.

Professional judgment: PASS for diagnosis; specific choice among DiD/permutation/synthetic-control still depends on design/data assumptions and should not be made universal.

### PM04V2-03 — optional stopping and multiplicity

Agent correctly rejected ordinary fixed-horizon inference under daily peeking, identified inflated false positives and multiple-testing bias, and proposed proper sequential boundaries (O'Brien-Fleming/Pocock) or pre-registered fixed-horizon analysis.

Grader falsely failed because its valid-strategy keyword list did not include the explicit phrase `sequential testing boundary` or named valid methods.

Professional judgment: PASS.

### PM04V2-04 — economic significance

Agent decision: **do not roll out**. It explicitly compared 40,000 AED incremental annual margin with 350,000 AED implementation cost and calculated **−310,000 AED net annual impact**.

Grader falsely failed because it only searched the text field for `-310,000`, while the exact `numeric_answer` was `-310000` and the prose used `-310k`.

Professional judgment: PASS.

### PM04V2-05 — unknown baseline

Agent explicitly said it **cannot provide a single exact sample size without the baseline conversion rate**, refused numeric fabrication, and proposed historical-data estimation / bounded baseline scenarios.

Grader falsely failed because its phrase matcher accepted `cannot give an exact` but not `cannot provide a single exact sample size`.

Professional judgment: PASS.

### PM04V2-06 — interference

Agent correctly rejected a clean causal interpretation, identified SUTVA/interference violation from commuting/media/cross-border behavior, and proposed moving to a switchback design or another design/model that addresses spillover/correlation.

Grader falsely failed because its `next_step` matcher did not include `switchback` or `synthetic control`.

Professional judgment: PASS for recognizing the identification failure and need to change design/method; whether switchback or synthetic control is appropriate remains context-dependent.

## Resource accounting

The PM-04 v2 run consumed 5,193 total model tokens: 3,285 input, 1,069 output, 839 thought tokens. No further model call is justified merely to make the brittle string grader turn green; the raw observable answers are already sufficient to diagnose the grader defect.

## Architecture decision

Current evidence does **not** justify adding a PM-04 procedural/reference knowledge module solely because of experimentation/statistical judgment. The existing core plus base model demonstrated:

- correct approximate sample-size calculation;
- unit-of-randomization/pseudoreplication diagnosis;
- optional-stopping/multiplicity judgment;
- statistical-vs-economic significance distinction;
- refusal to fabricate sample size without baseline;
- interference/causal-identification diagnosis.

Therefore PM-04 remains `SUFFICIENT_CORE_FOR_TESTED_SLICE`, not `MODULE_REQUIRED`.

This does not prove expert-level statistics universally. Future packaging should be triggered by a demonstrated failure on materially harder work: complex clustered power, heterogeneous treatment effects, sequential-design calculation, variance-reduction methods, interference modeling, or other tasks outside the tested slice.

## Evaluation repair

Repair the PM-04 v2 grader before using it as a release gate. Prefer structured semantic/decision fields and deterministic numeric checks over brittle substring matching. Do not weaken professional requirements; improve construct validity.

## Expert-gap / red-team

Senior practitioner: the main missing proof is deeper quantitative execution, not more terminology. Test complex design choices only when they are part of the role's real responsibility.

Educator/assessment specialist: current raw work samples are much more construct-valid than v1 label classification, but grader implementation must score meaning rather than exact wording.

Hiring manager: these six cases establish a useful floor, not mastery. The next meaningful evidence would be performance on messy real campaign data with incomplete telemetry and business constraints.
