# Paid Media / Performance Marketing Professional Core Qualification Gate

Frozen candidate: 1.0.0.

Release order:

1. deterministic contract checks, zero model calls;
2. reliability-sensitive PM-S1, PM-S2, PM-S3, PM-S11 and PM-S13: **3/3 independent PASS each, zero application retries**;
3. complete frozen PM-S1..PM-S13 suite on the same behavior-relevant core/runtime: **13/13 PASS, zero application retries**;
4. only then may the exact core artifact digest receive a PASS qualification record and `qualified` lifecycle state.

The semantic runner batches the selected fixtures into one structured model request per independent trial. Hidden expected actions/flags remain grader-side and each case is graded separately. Therefore the release sequence requires **4 model requests** (three critical reliability trials plus one complete release-suite request), rather than 28 one-case requests, while preserving 15 critical case evaluations plus 13 full-suite case evaluations.

Any behavioral failure is REVISE. Infrastructure/credential/quota failure is BLOCKED and is not behavioral PASS or FAIL. Do not rerun a failed stochastic sample until green; repair the root cause, then preregister and run a new candidate.

PM-S2 specifically tests whether a corrupted measurement signal is fit for the requested comparative decision; it does not misuse a causal-incrementality flag as a proxy for measurement validity. PM-S13 provides the positive control that a practitioner must scale when validated downstream economics, marginal return, capacity and delegated authority support a controlled increase.

The fixtures cover business-value vs proxy metrics, lead quality, measurement integrity, attribution vs incrementality, marginal budget allocation, experiment validity, performance diagnosis, sparse data, opportunity cost/stop-loss, automation objective mismatch, privacy signal loss, authority boundaries, vanity metrics, and justified scaling.