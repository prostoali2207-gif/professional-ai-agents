# Paid Media / Performance Marketing Professional Core Qualification Gate

Frozen candidate: 1.0.0.

Release order:

1. deterministic contract checks, zero model calls;
2. reliability-sensitive PM-S1, PM-S2, PM-S3 and PM-S11: **3/3 independent PASS each, zero application retries**;
3. complete frozen PM-S1..PM-S12 suite on the same behavior-relevant core: **12/12 PASS, zero application retries**;
4. only then may the exact core artifact digest receive a PASS qualification record and `qualified` lifecycle state.

Any behavioral failure is REVISE. Infrastructure/credential failure is BLOCKED and is not behavioral PASS or FAIL. Do not rerun a failed stochastic sample until green; repair the root cause, then preregister and run a new candidate.

The fixtures cover business-value vs proxy metrics, lead quality, measurement integrity, attribution vs incrementality, marginal budget allocation, experiment validity, performance diagnosis, sparse data, opportunity cost/stop-loss, automation objective mismatch, privacy signal loss, authority boundaries and vanity metrics.