# Content Architecture v0.4 Codex r3 — construct invalid

Status: CLOSED / CONSTRUCT_INVALID. Do not use the r3 `REVISE` verdict as professional evidence about candidate v0.4.

## What completed

- Exact candidate blob: `5d440e1bf3e20fbd35c6ab276310a904e36cc06d`.
- Codex runtime identity and subscription auth were verified.
- 40/40 scored trials completed after checkpoint continuation.
- No provider API key was used.

## Why the verdict is invalid

The r3 grader inherited the r1 exact-token verifier. Several tasks asked for JSON fields but did not publish the canonical enum vocabulary that the grader later required. Professionally equivalent decisions expressed with different but valid labels were therefore counted as failures. This makes the measurement depend on guessing hidden evaluator tokens rather than the underlying professional judgment.

A second implementation defect made `deterministic_invariant_pass_rate` equal to `all professional decisions passed`, which unintentionally converted the preregistered 0.80 per-family / 0.90 aggregate thresholds into an effective 1.00 all-cases threshold.

These are evaluator construct defects, not candidate failures. Because the defects were discovered after scored r3 outputs existed, r3 is burned rather than patched.

## Integrity disposition

- Candidate v0.4 remains frozen and unchanged.
- r3 records remain diagnostic only.
- No r3 result may be reused as scored r4 evidence.
- r4 must use fresh evaluator-owned cases.
- r4 must publish all response vocabulary required for deterministic grading inside each candidate-visible task.
- r4 deterministic invariants must measure mechanical contract/identity compliance, while professional correctness is governed by the unchanged P0, per-family, aggregate and repeat thresholds.
