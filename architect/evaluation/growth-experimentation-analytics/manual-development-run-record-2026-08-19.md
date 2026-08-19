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
| F-03 | Claude Sonnet | PASS | PASS | Correctly returned CONTINUE for an incomplete 14-day fixed-horizon test with no preregistered sequential or early-stop rule. |
| F-03 | Second synchronized runtime | PASS | PASS | Correctly returned CONTINUE and refused to act on interim +38%/+9% reads. Minor terminology note: classified peeking itself as a material confounder, but did not use it to alter the decision. |
| F-06 | Claude Sonnet | PASS | PASS | Correctly rejected denominator mismatch and recomputed appointment/qualified-lead rates, including A=0.25. |
| F-06 | Second synchronized runtime | PASS | PASS | Correctly rejected the apples-to-oranges comparison and recomputed consistent denominators. |
| F-07 | ChatGPT clean chat | PASS | PASS | Correctly separated last-touch attribution from incrementality and rejected the claim that 9 attributed sales were 9 incremental sales. |
| F-07 | Gemini | PASS | PASS | Correctly separated attribution from incrementality. Minor note: suggested additional counterfactual designs beyond the candidate text, without changing the decision. |
| F-07 | Claude Sonnet | PASS | PASS | Correctly bounded the 9/12 attribution read and rejected incremental-causality language without a counterfactual. |
| F-08 | ChatGPT clean chat | PASS | PASS | Returned CONTINUE; correctly treated B's 5-day sales read as immature rather than zero and waited for the 14-day maturation window. |
| F-08 | Gemini | PASS | PASS | Returned INCONCLUSIVE, allowed by the public key; correctly preserved delayed outcomes and rejected the mature-vs-immature comparison. |
| F-08 | Claude Sonnet | PASS | PASS | Returned CONTINUE and correctly identified right-censoring / unequal outcome maturation. |
| F-13 | ChatGPT clean chat | FAIL | PASS | Correctly recognized duplicate identities conceptually but made a counting error: two sale-event rows describing the same underlying purchase represent one unique sale, so one duplicate row should be removed (6 -> 5), not both rows (6 -> 4). |
| F-13 | Gemini | PASS | PASS | Correctly derived 20 unique qualified customers and 5 unique sales; noted the deduplicated rate remains 25% by coincidence. |
| F-13 | Claude Sonnet | PASS | FAIL | Correctly derived 20 unique qualified customers and 5 unique sales, but added an extra `assumptions_warnings` field inside one computation, violating the strict output contract. |

## Current interpretation

The public cases show strong coverage across distinct failure modes, but F-13 revealed a real runtime reliability issue in identity reconciliation arithmetic: one eligible runtime subtracted both duplicate sale-event rows instead of collapsing two rows into one underlying sale.

This is not evidence that the professional invariant is absent — Gemini and Claude executed the same invariant correctly — but it is evidence that the current candidate + runtime boundary does not yet guarantee deterministic deduplication arithmetic across model families.

Therefore do **not** freeze the candidate yet solely on the basis of the current public runs.

## Required repair before freeze

Do not add fixture-specific wording such as "subtract one when two rows are duplicates." Instead strengthen the generic identity-reconciliation procedure so that it operates on equivalence classes / underlying entities:

- customer records -> unique customer entities;
- event records -> unique underlying outcome entities;
- N records proven to represent the same underlying entity collapse to exactly 1 entity, so duplicates removed = N - 1;
- record both raw-row count and reconciled unique-entity count;
- never delete the underlying entity itself when removing duplicate representations.

Also strengthen deterministic computation grading for deduplication so numeric reconciliation is checked directly rather than only by narrative findings.

After this generic repair, rerun F-13 on the runtime that failed and at least one runtime that previously passed. If both pass, freeze the candidate rather than expanding public-test optimization.

## Evidence limitations

- Raw model responses were transferred manually through chat and are not stored here.
- Model/version identity was not reliably recorded for both synchronized F-12 responses; do not infer it after the fact.
- Earlier Gemini format failures are invalid for model comparison because Gemini had not received the updated output contract at the time.
- Public development fixture success is debugging evidence, not qualification evidence.
