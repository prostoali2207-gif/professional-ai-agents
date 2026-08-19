# Analytics candidate — manual development run record

Date: 2026-08-19
Status: PUBLIC DEVELOPMENT EVIDENCE ONLY — NOT QUALIFICATION
Candidate: `architect/research/growth-experimentation-analytics/professional-model-candidate-v0.1.md`
Candidate blob SHA: `287c43b71c111e8fbbaffa0d591ee914ccf940f6`
Protocol: `manual-cross-model-exam.md`

## Purpose

Record observed cross-model behavior on selected public development fixtures before candidate freeze. These runs are diagnostic only because the fixtures and public grader key are development artifacts; they cannot qualify the candidate.

## Runs

| Fixture | Model family | Analytical behavior | Output contract | Notes |
|---|---|---|---|---|
| F-02 | Gemini | PASS | INVALID COMPARISON | Correctly blocked causal winner selection due to severe unexplained exposure asymmetry. Run used an older output-contract version, so serialization must not be scored against Gemini. |
| F-02 | Claude Sonnet | PASS | PASS | Correctly distinguished near-50/50 assignment from severe assignment-to-exposure failure and returned INCONCLUSIVE. |
| F-04 | Gemini | PASS | INVALID COMPARISON | Correctly rejected a dramatic apparent lift from 1/9 vs 3/8 as insufficient evidence. Run used an older output-contract version. |
| F-04 | Claude Sonnet | PASS | PASS | Correctly reported raw rates/lift while refusing a winner claim from the tiny sample. |
| F-14 | Gemini | PASS WITH CAUSAL-LANGUAGE NOTE | INVALID COMPARISON | Correctly blocked unrestricted SCALE and selected ITERATE for capacity saturation. It overstated causality by saying overload directly caused the downstream decline. Run used an older output-contract version. |
| F-14 | Claude Sonnet | PASS | PASS | Returned INCONCLUSIVE, which is allowed by the public grader key; identified capacity saturation, response-time deterioration, and appointment-conversion decline, and blocked SCALE. |
| F-12 | Model A (identity not recorded in raw handoff) | PASS | PASS | Returned SCALE. Computed A=2.0 and B=2.885572 qualified leads/1k, relative lift=0.442786, CPQL A=50, B=36.034483. Minor unit-label issue: decimal proportion labeled `pct`, but rationale correctly interpreted 44.28%. |
| F-12 | Model B (identity not recorded in raw handoff) | PASS | PASS | Returned SCALE with the required calculations and correctly applied the deterministic success threshold and cost guardrail. |

## Current interpretation

The selected public cases do not justify a professional-rule repair. They show the candidate can:

- block inference when exposure integrity is materially broken;
- resist large-looking percentages from sparse outcomes;
- block unrestricted scale when downstream capacity collapses;
- select SCALE when the registered threshold and guardrail clearly pass.

The earlier concern that the candidate might default to INCONCLUSIVE even on a clean scalable win was not reproduced on F-12.

## Remaining development coverage before freeze

Do not run all public fixtures merely for completion. Prioritize distinct Tier-1 failure modes not yet behaviorally exercised in this record:

1. F-03 — fixed-horizon / premature stopping discipline.
2. F-06 — denominator mismatch.
3. F-07 — attribution versus incrementality.
4. F-08 or F-10 — missing/delayed outcome handling (choose one unless a failure warrants both).
5. F-13 — identity deduplication / one customer-one outcome.

If these distinct failure modes pass without revealing a professional-rule defect, freeze the candidate rather than continuing to optimize against public fixtures. Then create fresh sealed held-out cases after freeze and perform qualification without repairing from held-out answers.

## Evidence limitations

- Raw model responses were transferred manually through chat and are not stored here.
- Model/version identity was not reliably recorded for both synchronized F-12 responses; do not infer it after the fact.
- Earlier Gemini format failures are invalid for model comparison because Gemini had not received the updated output contract at the time.
- Public development fixture success is debugging evidence, not qualification evidence.
