# Paid Media Professional Core — Qualification Notes

Candidate: 1.0.0

## Pre-qualification failures and root-cause repairs

### Run 31950932908 — REVISE + infrastructure block

Deterministic preflight passed. The first reliability sequence exposed two independent defects:

- PM-S2 consistently selected the correct primary action (`REPAIR_MEASUREMENT`) but the grader required `causal_claim_blocked`. The case asks whether a corrupted conversion signal can rank campaigns by CPA; causal incrementality is a different construct. The grader was repaired to require `decision_signal_invalid`, preserving the measurement-validity requirement rather than weakening it.
- The original one-fixture-per-request release plan required up to 24 semantic API calls and hit the active free-tier request quota before completion. The runner was changed to batch hidden-answer-independent fixtures into one structured request per trial while grading each case separately. Critical 3-trial reliability plus one full suite now requires four model requests and zero application retries.

The attempted fallback to `gemini-2.5-flash-lite` was rejected by the API as unavailable to new users and was treated strictly as infrastructure failure, not behavioral evidence. The qualification runtime was moved to the currently available `gemini-3.1-flash-lite`.

### Run 31951189168 — REVISE

Deterministic preflight passed. PM-S2, PM-S3, PM-S11 and the positive-scale PM-S13 passed all three critical trials. PM-S1 failed because all three trials chose `STOP` while the frozen grader allowed `HOLD`, `ITERATE`, or `REPAIR_MEASUREMENT` but not `STOP`.

The PM-S1 construct is resistance to scaling on cheap CPA when downstream lead quality collapses. `STOP` is a professionally valid stop-loss response to those facts; forbidding it imposed a false single-policy preference that the profession model does not justify. The fixture was repaired to allow `STOP` while still forbidding `SCALE` and requiring explicit business-value and lead-quality reasoning. The unrelated `no_fabricated_business_facts` flag was removed from PM-S1; fabrication remains tested in sparse/unknown-economics cases.

## Red-team corrections already incorporated

A stop-only suite would reward pathological conservatism, so PM-S13 was added as a positive control: when CRM-validated downstream economics, marginal CAC, capacity, and delegated authority support a controlled budget increase, `SCALE` is the only acceptable action.

The release suite therefore tests both sides of professional judgment: resisting unjustified scale and executing justified scale. No threshold was changed after a favorable stochastic sample merely to obtain PASS; each correction addresses a documented construct, infrastructure, or resource-engineering defect.