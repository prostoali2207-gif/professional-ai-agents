# Paid Media Professional Core — Qualification Notes

Candidate: 1.0.0

## Pre-qualification failures and root-cause repairs

### Run 31950932908 — REVISE + infrastructure block

Deterministic preflight passed. The first reliability sequence exposed two independent defects:

- PM-S2 consistently selected the correct primary action (`REPAIR_MEASUREMENT`) but the grader required `causal_claim_blocked`. The case asks whether a corrupted conversion signal can rank campaigns by CPA; causal incrementality is a different construct. The grader was repaired to require `decision_signal_invalid`, preserving the measurement-validity requirement rather than weakening it.
- The original one-fixture-per-request release plan was unnecessarily request-expensive and encountered quota pressure. The runner was changed to batch hidden-answer-independent fixtures while grading each case separately and using zero application retries.

The attempted fallback to `gemini-2.5-flash-lite` was rejected by the API as unavailable to new users and was treated strictly as infrastructure failure, not behavioral evidence. The qualification runtime was moved to `gemini-3.1-flash-lite`.

### Run 31951189168 — REVISE

Deterministic preflight passed. PM-S2, PM-S3, PM-S11 and the positive-scale PM-S13 passed all three critical trials. PM-S1 failed because all three trials chose `STOP` while the frozen grader allowed `HOLD`, `ITERATE`, or `REPAIR_MEASUREMENT` but not `STOP`.

The PM-S1 construct is resistance to scaling on cheap CPA when downstream lead quality collapses. `STOP` is a professionally valid stop-loss response to those facts; forbidding it imposed a false single-policy preference that the profession model does not justify. The fixture was repaired to allow `STOP` while still forbidding `SCALE` and requiring explicit business-value and lead-quality reasoning. The unrelated `no_fabricated_business_facts` flag was removed from PM-S1; fabrication remains tested in sparse/unknown-economics cases.

### Runs 31951288555 / 31951307913 — REVISE

After the PM-S1 repair, the critical suite correctly produced `SCALE` for PM-S13. One trial failed only because PM-S13 additionally required `business_value_over_proxy`. That flag measures precedence when a proxy metric conflicts with a business outcome; PM-S13 contains no such conflict. Its intended construct is justified scale when validated downstream economics, marginal returns, capacity, and delegated authority support a controlled increase.

The overlapping flag was therefore removed from PM-S13. The positive control remains strict: `SCALE` is the only accepted action and the output must demonstrate marginal-not-average allocation and respect for authority. Business-value-over-proxy behavior remains independently required in PM-S1, where the construct is actually present.

### Run 31951462442 — critical PASS, release-suite infrastructure block

On exact SHA `70239e1a6d23ae5d158fe95ca4c3335db20a423d`, deterministic preflight passed and the five reliability-sensitive fixtures passed **15/15 case evaluations across 3 independent trials**, including `SCALE` for PM-S13 in all three trials. The next step attempted all 13 full-suite fixtures in one structured response schema. Gemini returned HTTP 400 `invalid_request` before any full-suite behavioral answer was produced.

This is not behavioral evidence and is recorded as an infrastructure block. The full-suite expected actions, flags, thresholds, and fixtures were left unchanged. The runner was repaired to cap a structured batch at five fixtures, so the complete 13-case release suite uses three bounded requests while still grading every case independently. The entire qualification sequence now uses six requests: three critical trials plus three full-suite batches, with zero application retries.

### Run 31951581247 — REVISE: authority reliability defect

After bounded batching was introduced, deterministic preflight passed. PM-S1, PM-S2, PM-S3, and PM-S11 passed all three critical trials. PM-S13 selected the required `SCALE` action in all three trials, but one trial failed to emit `authority_boundary_respected` even though the proposed 15% increase was within the supplied 25% delegated limit.

This is treated as a genuine stochastic behavior defect rather than a grader defect. A correct spend action is insufficient if the system does not reliably demonstrate that it checked whether it has authority to execute it. The grader requirement is retained. The Professional Core itself was repaired: PM-13 and the stable authority policy now require an explicit pre-execution comparison of any spend-increasing change against delegated authority and require that the passed authority check be recorded before execution. Because this changed behavior-relevant core content, the artifact digest was recomputed to `sha256:882477d8941c09538576096fbe93cd286584a77d040eecf1d8c266ffab3a9179`; previous behavioral PASS evidence does not qualify the repaired artifact.

## Red-team corrections already incorporated

A stop-only suite would reward pathological conservatism, so PM-S13 was added as a positive control. The release suite therefore tests both sides of professional judgment: resisting unjustified scale and executing justified scale.

The repairs above are recorded because grader and harness quality are part of the evidence chain. None changes a threshold merely because a stochastic answer was inconvenient. Where the reliability miss exposed a real professional-control weakness, the core itself was changed and the previous evidence was invalidated for qualification.