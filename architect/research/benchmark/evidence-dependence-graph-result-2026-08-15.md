# Evidence Dependence Graph v0.1 — Result

Date: 2026-08-15

## Verdict

STRUCTURAL PASS / QUANTITATIVE CALIBRATION NOT VALIDATED.

The deterministic graph gate passed all registered checks. It correctly represents pairwise evidence dependence with explicit shared causes, qualitative strength, and metadata confidence, while preserving UNKNOWN when dependence-relevant metadata is missing.

## What is proven

- lineage independence and methodological dependence are separate concepts;
- shared datasets, measurement pipelines, benchmarks, synthetic-data generators, populations/time windows, and annotators can be represented as dependence edges;
- partial dependence is distinct from high common-cause dependence;
- missing dependence metadata is UNKNOWN rather than automatically independent;
- two otherwise separate studies can remain strongly correlated through a shared benchmark or synthetic-data model.

## Important limitation

The numeric field weights and normalized overlap values in v0.1 are heuristic test scaffolding. They are not empirically calibrated probabilities or validated causal-effect estimates. They MUST NOT be presented to an Agent Architect or end user as statements such as “72% independent” or used as a statistical correction factor.

Until calibration exists, production use should rely on:

1. explicit dependence causes;
2. categorical state (DEPENDENT / PARTIALLY_DEPENDENT / NO_COMMON_CAUSE_OBSERVED / UNKNOWN);
3. metadata-coverage confidence;
4. human-readable rationale.

## Red-team findings

A senior evaluation scientist would still ask for adjudicated real-world pairs, partial population-overlap representation, benchmark contamination lineage, shared labeling artifacts, time-series/autocorrelation structure, shared pretrained-model ancestry, and sensitivity analysis showing that routing decisions do not depend on arbitrary field weights.

A causal-inference specialist would additionally object that an observed shared factor does not by itself quantify covariance or causal dependence. The current graph is a provenance/dependence warning system, not a causal estimator.

## Architecture consequence

Evidence aggregation must operate on an evidence-dependence graph, not raw source count. Confidence should be reduced or marked unresolved when apparently independent sources share strong common causes, while UNKNOWN dependence must remain visible rather than silently treated as replication.

## Cost control

The workflow was changed to manual-only after the successful gate so ordinary research commits do not consume additional GitHub Actions minutes.
