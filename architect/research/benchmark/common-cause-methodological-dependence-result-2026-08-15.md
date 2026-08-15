# Common-cause methodological dependence result — 2026-08-15

## Verdict

Deterministic gate: **PASS 5/5**.

This gate separates publication/source-lineage independence from methodological independence. Different organizations, domains, and publication lineages may still be correlated evidence if they share a dataset, measurement pipeline, vendor telemetry source, population frame, time window, or method family.

## Required evidence states

For each claim-supported evidence set, research normalization should retain at least:

- lineage root / upstream source;
- dataset or data-generating source;
- measurement / extraction pipeline;
- population and geography;
- funding / vendor ecosystem when materially relevant;
- observation time window;
- method family;
- dependence state and confidence.

Suggested dependence states:

- `DEPENDENT`: shared hard common cause such as the same dataset, measurement pipeline, or vendor ecosystem;
- `PARTIALLY_DEPENDENT`: materially shared population/time/method frame but independent datasets or pipelines;
- `INDEPENDENT`: no material shared dependence found across inspected dimensions;
- `UNKNOWN`: insufficient metadata to adjudicate dependence.

`UNKNOWN` must not be silently promoted to `INDEPENDENT`.

## Tested cases

1. Independent publication lineages using the same dataset -> `DEPENDENT`.
2. Three publications using the same vendor telemetry/SDK/customer population -> `DEPENDENT`.
3. Administrative records, an independent survey, and an experiment across different populations -> `INDEPENDENT`.
4. Publications with missing dataset/pipeline/vendor provenance -> `UNKNOWN`.
5. Different datasets/pipelines but the same narrow population and time frame -> `PARTIALLY_DEPENDENT`.

## Architectural implication

Evidence synthesis must not report confidence using source count alone. At minimum it needs two orthogonal dimensions:

1. **lineage independence** — are publications derived from the same upstream source?
2. **methodological/common-cause independence** — do ostensibly independent sources depend on the same data-generating or measurement process?

A claim supported by ten independent publications using one benchmark dataset is not equivalent to a claim replicated across independent datasets, populations, and methodologies.

## Red-team limitations

This v0.1 model is deliberately conservative but incomplete. It does not yet quantify:

- degree of dataset/population overlap;
- benchmark or train/test contamination;
- shared annotation/labeling artifacts;
- common software instrumentation bias;
- shared model/provider-generated synthetic data;
- causal dependence strength between evidence items;
- undisclosed funding or data-provider relationships;
- temporal autocorrelation across repeated releases of the same dataset.

Therefore the next professional step is a **dependence graph with confidence and overlap**, not a larger list of boolean fields.
