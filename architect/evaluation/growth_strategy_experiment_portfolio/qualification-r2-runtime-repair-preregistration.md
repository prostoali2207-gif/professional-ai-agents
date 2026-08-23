# Strategist v0.1 qualification r2 — runtime repair preregistration

Status: preregistered before r2 hidden authoring.

## Reason

The prior sealed qualification reached static preflight PASS, sealed transport PASS, exact-runtime canary PASS, then stopped before candidate fixture execution because the second independent OpenAI judge returned `credit_balance_exhausted` during calibration. This is an evaluator-runtime availability failure, not professional evidence about the candidate.

## Frozen invariants

- Candidate commit: `1c042d09695dfe2d4186c21d136474dc9d1fbdd9`.
- Candidate digest: `sha256:59dd74cb772f1259a7ed5f6b9da4aa40db7f48be21c380b605bdc044f4dd7b92`.
- Candidate model/runtime: Gemini `gemini-3.5-flash-lite`, stateless, no tools.
- Same 12 competency families and two fixtures per family.
- Same seven contrastive/metamorphic pair constructs.
- Same critical hard-fail flag set.
- Same family dimension thresholds and overall pass-rate threshold.
- One trial per fixture; zero professional-failure retries.

## Evaluator repair

Replace only the unavailable second judge transport:

`OpenAI judge -> Groq qwen/qwen3.6-27b judge`.

Retain Gemini as the first judge. Both judges must pass public calibration before hidden grading. Aggregation remains conservative: minimum dimension score across judges, union of critical flags, and both judges required for pair consistency.

The r2 hidden pack must be freshly authored after this preregistration, independently reviewed by Groq before sealing, encrypted with the repository-wide qualification master key, and frozen before scored candidate execution.

## Resource gate

OpenAI is not used. The workflow must fail closed on missing Gemini/Groq credentials, quota/rate failure, calibration failure, invalid pack structure, missing sanitized report, or nonzero qualification verdict. No blind reruns are permitted; after an infrastructure failure, reuse the already-frozen r2 pack when possible instead of re-authoring it.
