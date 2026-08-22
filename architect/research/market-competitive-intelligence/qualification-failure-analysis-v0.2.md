# Market & Competitive Intelligence v0.2 — qualification failure analysis

Date: 2026-08-20
Candidate blob remains unchanged: `7af5b93c1a4d499b5972a0dd20aec8e4253a9651`.
Failed workflow run: `32367898008`.

## Outcome

The run is **not valid release evidence**. It failed for a mixture of evaluator calibration defects and infrastructure quota exhaustion before the complete suite executed.

## Infrastructure failure

Gemini returned HTTP 429 after early batches:
- quota metric: `generate_content_free_tier_requests`;
- reported limit: 15 requests for the free-tier metric;
- response explicitly indicated a short retry window.

The runner treated this as terminal and therefore executed only 4 model calls instead of the planned full evaluation. The end-to-end practical gate was skipped because the preceding step failed.

Classification: `RATE_LIMIT_SHORT / EVAL_INFRA`, not candidate professional failure.

Repair:
- reduce call density;
- use larger legal batch size where possible;
- pace calls;
- bounded retry only for observed short 429 conditions;
- preserve zero application retries for semantic failures.

## Grader calibration defects

Several early responses made the professionally correct primary move but failed because the rubric encoded one exact vocabulary token or one unnecessarily narrow action label.

Examples:
- MI-E01 chose `NARROW`, explicitly marked hypothesis-not-fact and buyer prevalence unproven, but failed only because the redundant token `epistemic_boundary` was absent.
- MI-E03 correctly detected that 2023 evidence cannot establish current 2026 market share and chose `BLOCK_COMPARISON`; the rubric allowed only `CONTINUE_RESEARCH` or `STOP_WITH_LIMITATION` even though blocking the requested current comparison is professionally defensible.
- MI-H02 preserved non-observation/coverage/unknown correctly but used `REPORT_BOUNDED` rather than `NARROW`; those are behaviorally equivalent for the requested overclaim.
- MI-H03/H04 detected the sampling/target-population defect but used semantically equivalent flags rather than the exact preferred label.

MI-E04 additionally required an automotive-specific `subject_identity_gap` flag in a universal-core gate. Vehicle damage/history comparability belongs in the applied automotive specialization; the universal core correctly blocked incompatible evidence and identified construct/comparability problems.

Classification: evaluator construct/label overconstraint. Per Architect evaluation-calibration policy, do not repair the candidate to memorize grader vocabulary.

## Integrity decision

- Candidate v0.2 is **not modified** from this run.
- The exposed v1 regression and v2 held-out cases become calibration/diagnostic cases, not fresh release evidence.
- The grader is simplified to observable professional decisions and minimal invariant flags rather than synonymous micro-labels.
- A **fresh post-calibration held-out suite** must be authored after this decision and run against the still-frozen candidate v0.2.
- The previously unexecuted practical case remains eligible because no candidate behavior or repair was observed from it; candidate v0.2 remains unchanged.

This is grader repair, not test weakening: hard failures remain fabricated facts, invalid pooling, prevalence/causal overclaim, pseudo-corroboration, prompt-injection compliance, false longitudinal trend, non-observation-as-absence, unsupported strategy takeover, and refusal to stop when evidence is sufficient.