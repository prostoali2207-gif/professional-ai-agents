# Growth Experimentation & Measurement — knowledge and computation contract v0.1

Status: research/design artifact; not release-ready.
Date: 2026-08-18.

## Purpose

Define what a reusable Growth Experimentation & Measurement core knows by default, what must come from live experiment context, what must be computed reproducibly, and when the agent must stop instead of guessing.

## Knowledge packaging

### EMBED_CORE — stable professional rules

- freeze the primary KPI and decision rule before outcome inspection;
- attribution is not incrementality;
- missing, delayed, invalid and zero are different states;
- effect size and uncertainty matter more than a favorable percentage alone;
- post-hoc segments are hypotheses unless the design supports valid inference;
- fixed-horizon peeking cannot justify an early winner without a preregistered valid sequential method;
- denominator populations must match the quantity being estimated;
- metric definitions and versions must remain comparable;
- assignment/exposure integrity must be checked before strong causal interpretation;
- selection, survivorship, censoring, contamination and interference can invalidate apparently clean results;
- a positive effect is not automatically economically or operationally scalable;
- `INCONCLUSIVE` is a valid decision when evidence cannot answer the registered question;
- unknown facts are never manufactured.

### PROCEDURAL_MODULE — experiment analysis procedure

1. validate the experiment packet and frozen decision rule;
2. validate data states, IDs, windows and joins;
3. check assignment/exposure integrity when applicable;
4. verify metric definitions and denominators;
5. assess sample and outcome maturity;
6. compute primary effect and uncertainty;
7. inspect guardrails and diagnostics;
8. check selection, censoring, contamination and interference;
9. reconstruct relevant funnel stages;
10. separate attribution evidence from causal evidence;
11. test economics/capacity when SCALE is under consideration;
12. execute the preregistered decision rule or return `INCONCLUSIVE`;
13. state the exact evidence defect or next verification needed.

### REFERENCE_MODULE — deeper material loaded only when needed

- sample-ratio mismatch diagnostics;
- power, MDE and sample-size guidance;
- sparse binary-outcome intervals/tests;
- multiple-testing and segment interpretation;
- sequential/always-valid methods;
- observational/quasi-experimental inference boundaries;
- selection, censoring and maturation patterns;
- metric-quality/OEC failure patterns;
- interaction, interference and carry-over patterns;
- marginal scaling economics and capacity constraints.

### LIVE_CONTEXT — supplied by the current experiment/business/platform

The reusable core must not hard-code:
- current platform metric names or definitions;
- current reporting delays or API/export limitations;
- current experiment IDs, variants, windows and assignment rules;
- current audience/eligibility/exposure conditions;
- current spend, costs, prices, margins or capacity;
- current business definition of a qualified outcome;
- actual leads/users/events/appointments/sales or analogous downstream outcomes;
- current legal/privacy/retention requirements where material.

Every volatile value should carry provenance and observation time where relevant.

### TOOL_BACKED — reproducible computation required

Use deterministic/reproducible computation for:
- counts, rates and absolute/relative deltas;
- expected vs observed allocation diagnostics;
- uncertainty intervals where the method is qualified;
- exact/binomial calculations for sparse binary outcomes when appropriate;
- power/MDE/sample-size calculations when assumptions are supplied;
- deduplication/reconciliation checks over IDs;
- funnel conversions with explicit numerator and denominator;
- cost-per-outcome and other unit-economics arithmetic;
- observation-window alignment and maturity checks;
- deterministic application of preregistered thresholds.

### ESCALATE — do not improvise

Stop or request specialist/human review when:
- required statistical inference depends on unsupported assumptions;
- design includes complex clustering, crossover, interference or repeated measures beyond the qualified toolchain;
- identity resolution is materially ambiguous;
- decision-critical economics are unavailable or unverified;
- live metric definitions are stale or contradictory;
- a legal/privacy conclusion is required beyond analytical data minimization;
- data corruption prevents reconstruction of the intended comparison.

## Minimum reproducible computation contract

Every material calculation must expose:
- `calculation_id`;
- experiment/variant/window identifiers;
- input values and source references;
- input availability states;
- formula or named method;
- method assumptions;
- tool/runtime identifier/version where available;
- output value and unit;
- precision rule;
- warnings/assumption violations;
- timestamp;
- deterministic pass/fail against a preregistered threshold where applicable.

Narrative claims such as “variant B performed significantly better” are not sufficient evidence by themselves.

## Calculation eligibility

### Simple arithmetic

Eligible when inputs are valid and comparable:
- conversion rate = numerator / eligible denominator;
- absolute difference = treatment rate - control rate;
- relative lift = (treatment - control) / control when control is nonzero and interpretation is meaningful;
- cost per outcome = spend / valid outcome count;
- funnel-stage rate = downstream eligible count / upstream eligible count.

Do not manufacture a rate from zero, missing or population-mismatched denominators.

### Allocation / sample-ratio checks

Only apply when an expected allocation exists. Distinguish:
- assigned units;
- exposed units;
- metric-observed units.

If an SRM test is used, record expected ratio, method and assumptions. A material unexplained mismatch blocks strong causal interpretation until resolved.

### Uncertainty and sparse outcomes

- record outcome type and sampling unit;
- use sparse-data-appropriate methods when required;
- avoid unsupported normal approximations;
- report counts and denominators alongside intervals;
- return a blocked state rather than inventing an unsupported interval.

### Power / MDE

Separate:
- business minimum useful effect;
- statistically detectable effect under stated assumptions;
- available sample/traffic and duration.

If these do not align, label the design underpowered for the intended decision.

### Sequential vs fixed horizon

- fixed horizon: judge at registered sample/window except safety/operational failure;
- sequential/always-valid: require the exact qualified method and assumptions;
- no registered sequential method: repeated peeking cannot justify SCALE/KILL.

## Evidence states

Decision-critical fields use:
- `OBSERVED`;
- `MISSING`;
- `NOT_COLLECTED`;
- `DELAYED`;
- `INVALID`;
- `NOT_APPLICABLE`.

`MISSING`, `NOT_COLLECTED`, `DELAYED` and `INVALID` must never be converted to numeric zero.

## Decision-blocking rules

Return `INCONCLUSIVE`/blocked rather than a forced verdict when decision-critical evidence has any of these defects:
- variants are materially incomparable;
- common evaluation window cannot be reconstructed;
- primary KPI or success rule was not frozen before inspection;
- key outcomes are missing/delayed beyond the registered rule;
- attribution identity is too ambiguous for the requested claim;
- metric definitions changed incompatibly;
- unexplained allocation/instrumentation failure could create the observed effect;
- sample cannot resolve the intended business effect and no valid leading metric was preregistered;
- required computation exceeds the qualified toolchain.

## Boundary rule

Industry, geography, platform, CRM, inventory, pricing and company-specific logic belong in specialization/live context, not this reusable core.

## Next gate

1. implement generic public development fixtures;
2. define deterministic graders;
3. develop the reusable candidate without teaching to exact fixture wording;
4. freeze candidate behavior;
5. create fresh sealed held-out qualification cases;
6. package the reusable core only after behavioral PASS.
