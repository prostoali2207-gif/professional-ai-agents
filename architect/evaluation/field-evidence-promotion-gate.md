# Field Evidence Promotion Gate

Use this gate when a consuming project reports a production observation that may justify changing a Professional Core or durable specialization.

## Gate 0 — provenance

REVISE if the observation lacks enough provenance to distinguish what was known before action from what was learned afterward.

Record:
- source project and experiment identifier;
- observation date/window;
- specialist/model artifact versions used;
- pre-action recommendation/hypothesis when available;
- measurement sources and known limitations;
- material interventions/confounders.

## Gate 1 — evidence validity

Ask whether the claimed observation is actually supported by trustworthy measurement.

REVISE or classify `MEASUREMENT_LIMITED` when:
- conversion/outcome tracking is materially broken;
- attribution is treated as incrementality without justification;
- inventory/price/offer changed without accounting for it;
- downstream outcomes are unavailable but proxy metrics are presented as business truth;
- key timestamps or decision provenance are missing.

## Gate 2 — alternative explanations

Require at least one serious alternative explanation for a material finding.

Examples: offer, creative, audience composition, inventory, price, seasonality, follow-up quality, capacity, platform delivery, measurement changes, external demand.

A post-hoc narrative with no alternative is not promotion evidence.

## Gate 3 — classification

Choose exactly one primary disposition:

- `NO_CHANGE`
- `PROJECT_CONTEXT`
- `LIVE_CONTEXT`
- `EXPERIMENT_LEARNING`
- `EVAL_CANDIDATE`
- `SPECIALIZATION_CANDIDATE`
- `CORE_CANDIDATE`

Default to the least reusable justified class.

## Gate 4 — transferability

For `SPECIALIZATION_CANDIDATE` or `CORE_CANDIDATE`, require explicit answers:
- What mechanism makes this transferable?
- What materially different contexts should still exhibit it?
- What evidence argues against transferability?
- What corroboration exists beyond this one project instance?

One production experiment alone normally cannot PASS this gate for a durable model change.

## Gate 5 — adversarial evaluation before model edit

When a plausible reusable failure mode exists, create or strengthen a behavioral eval **before** changing the professional model.

The fixture must abstract away confidential/local facts while preserving the decision structure that exposed the problem.

REVISE if the proposed model edit has no falsifiable behavioral test.

## Gate 6 — root-cause repair

Only if the current professional artifact fails the new valid eval:
- identify Core vs specialization ownership;
- repair the smallest responsible professional policy;
- do not encode project names, country/platform facts or experiment-specific numbers;
- do not weaken grader thresholds to obtain PASS.

## Gate 7 — requalification

Order:
1. deterministic/static checks;
2. minimal affected behavioral test;
3. critical reliability trials when stochastic behavior affects a critical transition;
4. broader regression/release suite after affected PASS.

Record exact artifact revision/digest and evidence provenance.

## Gate 8 — feedback closure

The consuming project should receive the disposition:
- what stayed local;
- what became live context;
- what became an eval;
- whether the professional model changed;
- qualified version/digest if changed;
- remaining uncertainty.

## Anti-patterns

Automatic REVISE:
- `campaign won -> add rule`;
- `campaign lost -> agent was wrong`;
- optimizing the reusable model to one customer;
- turning current platform behavior into durable professional knowledge;
- promoting a vehicle/SKU/product into its own specialist;
- changing prompts before reproducing the suspected defect;
- ignoring null/negative/stopped experiments;
- using self-report as proof of production effectiveness.
