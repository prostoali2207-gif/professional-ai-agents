# Growth Experimentation & Measurement — Evidence and Reuse

## Reconstruction and development evidence

The profession was reconstructed in `architect/research/growth-experimentation-analytics/` before admission. Public development coverage included exposure integrity, fixed-horizon stopping, sparse samples, denominator mismatch, attribution versus incrementality, delayed outcomes, identity deduplication, downstream capacity, and clean SCALE behavior.

A real duplicate-cluster defect was repaired before the first freeze: `n` records proven to represent one real entity contribute one canonical entity and therefore `n-1` duplicates.

Candidate v0.1 later failed qualification because a runtime proposed replacing a corrupted registered denominator with an assigned-user diagnostic denominator as the future primary comparison. That failure was recorded without repairing the frozen candidate.

Candidate v0.2 added the profession-general registered-estimand-preservation rule, passed the public regression `R-01-v0.2`, and was frozen as the exact base-plus-overlay assembly with composite digest `sha256:729d8de82480135ec64509a56cb8c143dbca6e392ffb9614312f3ddfa19b353f`.

## Held-out qualification

Fresh held-out cases were created only after the v0.2 freeze.

- Q-09: completed horizon with unrecoverable registered denominator — PASS on ChatGPT, Gemini, Claude.
- Q-10: burned as construct-invalid because the grader required an unsupported matured-cohort linkage not stated in the fixture; it is not candidate failure evidence.
- Q-11: replacement delayed-conversion case with explicit matured-cohort linkage — PASS on ChatGPT, Gemini, Claude.

The candidate was not changed between Q-09 and Q-11.

Qualification record source:
`architect/evaluation/growth-experimentation-analytics/qualification-result-v0.2.json`

Freeze source:
`architect/evaluation/growth-experimentation-analytics/candidate-freeze-v0.2.json`

Q-10 invalidation/Q-11 preregistration source:
`architect/evaluation/growth-experimentation-analytics/q10-invalidation-and-q11-preregistration-v0.2.json`

## Reuse boundary

Stable reusable behavior belongs in this core. Domain, organization, platform, legal, price, margin, inventory, capacity, and current metric-definition facts remain external context.

Specializations may add domain-specific measurement definitions and operating constraints but may not weaken the core invariants, silently change registered estimands, or convert attribution into incrementality.

Any behavior-relevant change to the frozen professional model, a repeated production failure class, materially changed runtime behavior, or new evidence invalidating a critical policy triggers revalidation or requalification.
