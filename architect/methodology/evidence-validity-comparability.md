# Evidence Validity and Comparability

Status: v0.1.

## Purpose

Prevent a dangerous class of agent failures in which evidence is authoritative, current, and correctly retrieved but still does not support the decision because the observations are not measuring the same construct, population, condition, unit, or outcome.

Source quality is necessary but not sufficient. Professional evidence synthesis requires validity and comparability checks before aggregation or inference.

## 1. Evidence-generating-process map

For every material empirical claim, identify where the evidence came from and what process generated it.

Record as relevant:

- target construct or decision variable;
- population / market / system represented;
- sampling or selection mechanism;
- inclusion and exclusion criteria;
- measurement method;
- unit and denominator;
- time period;
- geography / jurisdiction;
- product, subject, cohort, version, or condition;
- transformations, weighting, normalization, or filtering;
- missingness / nonresponse / censoring;
- known biases and uncertainty.

The agent must not infer comparability from similar labels alone.

## 2. Comparability gate

Before combining, ranking, averaging, benchmarking, or using one observation as a comparator for another, test whether they are sufficiently comparable for the decision.

Ask:

1. Same construct? Are both observations measuring the thing the decision actually requires?
2. Same population or defensible transport? If populations differ, what supports generalization?
3. Same state/condition? Examples: new vs used, retail vs wholesale, export-only vs local-market, production vs preview, observed transaction vs asking price.
4. Same unit and denominator? Gross vs net, per-user vs per-session, nominal vs real, inclusive vs exclusive of taxes/fees.
5. Same temporal regime? Has market, policy, product version, or environment changed materially?
6. Same measurement method? Could instrument, wording, collection mode, logging, or methodology produce systematic differences?
7. Same inclusion criteria? Are hidden exclusions creating selection bias?
8. Same quality threshold? Are duplicates, outliers, low-confidence records, or synthetic observations contaminating one side?

If comparability is partial, preserve the distinction instead of forcing a single estimate.

## 3. Construct validity

A convenient metric is not automatically the decision variable.

Examples:

- listing price is not completed-sale price;
- click-through rate is not customer value;
- test pass rate is not production reliability;
- model preference score is not professional competency;
- response rate alone is not survey validity.

For every proxy, document:

`target construct -> proxy -> causal/empirical justification -> known gaps -> conditions where proxy breaks`.

## 4. Selection and coverage risk

Evidence can be numerically precise while systematically unrepresentative.

Check:

- who or what could enter the dataset;
- who or what could not;
- why observations are missing;
- whether inclusion probability differs in decision-relevant ways;
- whether data availability itself is correlated with the outcome.

Do not use sample size as a substitute for representativeness.

## 5. Measurement and classification error

Inspect whether observations are consistently classified and measured.

Create explicit classification boundaries for categories that materially affect inference. Ambiguous records should be marked uncertain, excluded, or sensitivity-tested rather than silently assigned.

For mixed evidence, require a data dictionary or comparator schema when category ambiguity can change the decision.

## 6. Aggregation discipline

Do not average heterogeneous evidence merely to produce one number.

Preferred sequence:

`classify -> validate -> segment -> compare within segment -> quantify uncertainty -> synthesize only where justified`.

When multiple segments are decision-relevant, present separate estimates or a model that explicitly accounts for segment differences.

## 7. Uncertainty and sensitivity

Where evidence quality or comparability is uncertain:

- identify the uncertain assumption;
- estimate how much the decision changes under plausible alternatives;
- collect additional evidence if the decision is sensitive;
- lower confidence or defer the decision if material uncertainty remains.

A narrow numeric answer with hidden comparability uncertainty is worse than an explicit range or unresolved state.

## 8. Evaluation requirements

Analytical agents must be tested on adversarial evidence sets containing:

- authoritative but non-comparable sources;
- mixed populations or product states;
- duplicate records;
- stale observations;
- proxy/construct mismatch;
- inconsistent units/denominators;
- sample-selection bias;
- mislabeled categories;
- large but biased samples;
- sparse but high-quality evidence;
- a user insisting that heterogeneous data be pooled.

Passing behavior requires detecting the incompatibility, explaining its decision impact, and either segmenting, normalizing with justification, obtaining better evidence, or refusing unsupported synthesis.

## 9. Agent Architect integration

When modeling any profession that consumes empirical evidence, the Architect must determine whether validity/comparability is a core competency, boundary-critical competency, or escalation dependency.

The knowledge architecture is incomplete if it teaches source authority and retrieval without teaching whether the retrieved observations can legitimately answer the professional question.

## Evidence basis

This layer is informed by:

- ISO 20252 requirements for market, opinion, social research, insights and data analytics;
- AAPOR total-survey-error and best-practice guidance on coverage, measurement, nonresponse, sampling, weighting, and transparency;
- occupational descriptions from BLS/O*NET showing that market-research work includes data collection-method design, statistical analysis, competitor/price research, interpretation, and recommendation.

These sources support the general validity discipline; profession-specific comparator rules still require domain evidence and practical evaluation.