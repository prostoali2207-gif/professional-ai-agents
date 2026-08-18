# Growth Experimentation & Measurement — knowledge and computation contract v0.1

Status: research/design artifact; not release-ready.
Date: 2026-08-18.

## Purpose

Define what the future professional core must know by default, what must be retrieved from the current experiment or platform, what must be calculated deterministically, and when the agent must stop instead of guessing.

## 1. Knowledge packaging

### EMBED_CORE — stable professional rules

These belong in the reusable professional core because they are stable principles of trustworthy experimentation and measurement:

- freeze the primary KPI and decision rule before outcome inspection;
- attribution is not incrementality;
- missing, delayed, invalid and zero are different states;
- effect size and uncertainty matter more than a favorable percentage alone;
- post-hoc segments are hypotheses unless the design explicitly permits valid inference;
- fixed-horizon peeking must not trigger an early winner unless a valid sequential method was preregistered;
- denominator populations must match the quantity being estimated;
- metric definitions and versions must remain comparable across variants and windows;
- randomization or exposure integrity must be checked before strong causal interpretation;
- selection, survivorship, censoring and contamination can invalidate apparently clean results;
- a positive effect is not automatically economically scalable;
- INCONCLUSIVE is an acceptable professional decision when evidence cannot answer the registered question;
- unknown facts are never manufactured to complete an analysis.

### PROCEDURAL_MODULE — load when running an experiment analysis

The analysis procedure should be a dedicated module rather than always-loaded prose:

1. validate experiment packet and frozen decision rule;
2. validate data states, IDs, time windows and joins;
3. check assignment/exposure integrity when applicable;
4. verify metric definitions and denominators;
5. test sample/maturity adequacy;
6. compute primary effect and uncertainty;
7. inspect guardrails and secondary diagnostics;
8. check selection/censoring and contamination;
9. reconstruct the commercial funnel;
10. separate attribution evidence from causal evidence;
11. test economics and operational capacity when SCALE is possible;
12. execute the preregistered decision rule or return INCONCLUSIVE;
13. state the exact evidence defect or next verification needed.

### REFERENCE_MODULE — deeper professional material

Load only when the case requires it:

- sample-ratio mismatch diagnostics and thresholds;
- power, MDE and sample-size guidance;
- sparse binary-outcome intervals/tests;
- multiple-testing/segment interpretation;
- sequential/always-valid methods;
- quasi-experiment/observational inference boundaries;
- selection, censoring and maturation patterns;
- metric-quality/OEC failure patterns;
- interaction, interference and carry-over patterns;
- marginal scaling economics and capacity constraints.

These references should contain operational rules and assumptions, not copied textbooks.

### LIVE_CONTEXT — must come from current sources or the experiment packet

The reusable core must not hard-code these:

- current Meta/Instagram/YouTube/Telegram metric names and definitions;
- current platform reporting delays or API/export limitations;
- campaign objective, optimization and attribution-window settings;
- current business definition of a qualified lead;
- current vehicle availability, price, gross margin and inventory status;
- current sales-team response capacity and appointment capacity;
- current experiment IDs, variants, start/end times and spend;
- actual placement, audience, delivery and creative execution;
- actual leads, appointments, sales and delayed outcomes;
- current legal/privacy/retention rules where material.

Every volatile value must carry source/provenance and observation time where relevant.

### TOOL_BACKED — deterministic computation required

Use reproducible computation rather than narrative arithmetic for:

- counts, rates and absolute/relative deltas;
- expected vs observed allocation and sample-ratio diagnostics;
- confidence/credible intervals where the chosen method is supported;
- exact/binomial calculations for sparse binary outcomes when appropriate;
- power/MDE/sample-size calculations when assumptions are supplied;
- deduplication/reconciliation checks over IDs;
- funnel conversion calculations with explicit numerator and denominator;
- cost per qualified lead/appointment/sale and gross-profit arithmetic;
- observation-window alignment and maturity checks;
- deterministic application of preregistered thresholds/decision rules.

### ESCALATE — do not improvise

The agent must stop or request specialist/human review when:

- the requested statistical inference depends on assumptions that are not supplied or cannot be justified;
- the test design has complex interference, clustering, crossover or repeated-measure structure beyond the qualified toolchain;
- identity resolution is materially ambiguous and would affect attribution or sales outcome counts;
- business economics such as gross margin are unverified or restricted;
- platform definitions are stale/contradictory and the decision depends on them;
- a legal/privacy conclusion is required rather than an analytical data-minimization decision;
- data corruption or experiment integrity failure prevents reconstruction of the intended comparison.

## 2. Minimum reproducible computation contract

Every material calculation must produce a record with:

- `calculation_id`;
- `experiment_id` and variant/window identifiers;
- input values and their source references;
- input availability states;
- formula or named statistical method;
- method assumptions;
- tool/runtime identifier and version where available;
- output value and unit;
- rounding/precision rule;
- warnings or assumption violations;
- timestamp;
- deterministic pass/fail against a preregistered threshold when applicable.

A prose sentence such as "B performed significantly better" is not sufficient evidence by itself.

## 3. Calculation eligibility rules

### Simple deterministic arithmetic

Eligible whenever all inputs are valid and comparable:

- conversion rate = numerator / eligible denominator;
- absolute difference = treatment rate - control rate;
- relative lift = (treatment - control) / control, only when control is nonzero and the interpretation is meaningful;
- cost per outcome = spend / valid outcome count;
- funnel-stage rate = downstream eligible count / upstream eligible count.

If the denominator is zero, missing or represents a different population, do not manufacture the rate.

### Allocation / sample-ratio checks

Only apply when an expected assignment/allocation ratio exists.

The tool record must distinguish:

- assigned units;
- exposed/reached units;
- metric-observed units.

A mismatch at one level must not be silently interpreted as a mismatch at another.

If a statistical SRM test is used, the expected ratio and test method must be recorded. A material unexplained mismatch blocks strong causal interpretation until resolved.

### Uncertainty and sparse outcomes

The agent must not choose a statistical method only because it is convenient.

Required behavior:

- record outcome type and sampling unit;
- prefer exact/binomial-compatible approaches for very sparse binary outcomes when appropriate;
- avoid normal approximations when assumptions are visibly poor;
- report counts and denominators alongside intervals;
- if the qualified runtime does not support the required method, return `BLOCKED_STATISTICAL_METHOD` rather than inventing a confidence interval.

### Power / MDE

Before claiming a design is capable of answering its question, separate:

- business minimum useful effect;
- statistical detectable effect under stated assumptions;
- available sample/traffic and test duration.

If these do not align, label the design underpowered for the intended decision. Do not hide this by extending the test indefinitely after observing results.

### Sequential vs fixed horizon

The computation layer must know which stopping regime was preregistered.

- fixed horizon: evaluate at the registered sample/window except safety/operational failure;
- sequential/always-valid: require the exact qualified method and its assumptions;
- no registered sequential method: repeated peeking cannot justify SCALE/KILL.

## 4. Evidence states

Every decision-critical field must use one of:

- `OBSERVED` — valid current observation;
- `MISSING` — expected but absent;
- `NOT_COLLECTED` — collection was not implemented;
- `DELAYED` — outcome may still mature;
- `INVALID` — collected but unusable;
- `NOT_APPLICABLE` — legitimately irrelevant.

`MISSING`, `NOT_COLLECTED`, `DELAYED` and `INVALID` must never be converted to numeric zero.

## 5. Decision blocking rules

Analytics must return INCONCLUSIVE/BLOCKED rather than a forced business verdict when any of these is decision-critical:

- A and B are not comparable on the registered variable because material uncontrolled changes exist;
- common evaluation window cannot be reconstructed;
- primary KPI or success rule was not frozen before result inspection;
- key outcome data is missing/delayed beyond what the registered rule can tolerate;
- attribution identity is too ambiguous for the requested claim;
- metric definitions changed incompatibly between variants/windows;
- unexplained allocation/instrumentation failure can plausibly produce the observed effect;
- sample is incapable of resolving the intended business effect and no valid leading metric was preregistered;
- required calculation exceeds the qualified toolchain.

## 6. Automotive specialization boundary

The reusable professional core should know how to reason about experiments and measurement. The automotive specialization should add domain-specific commercial structure such as:

- vehicle-level inventory identity;
- qualified buyer definitions;
- appointment/test-drive/reservation/sale states;
- sold-elsewhere and inventory-availability censoring;
- price/condition/vehicle-desirability confounding;
- gross profit, time-to-sale and inventory-age economics;
- salesperson response/follow-up as an operational confounder.

UAE/Meta/WhatsApp details remain live context, not permanent core knowledge.

## 7. Immediate A/B field requirement

For the current automotive creative test, the future analyzer must receive or reconstruct at minimum:

- exact common comparison start from the moment both variants were live;
- exact common observation maturity when results are compared;
- spend and delivery by A/B over that same window;
- actual audience, geography, placements, optimization and attribution settings for each variant;
- proof that the intended creative difference is the only material controlled difference, or an explicit deviation record;
- qualified inquiry counts by variant where attribution supports them;
- appointment/test-drive/sale outcomes with delayed/missing states preserved;
- any concurrent campaign or operational event that could contaminate the result.

This requirement does not predetermine which variant wins. It protects the experiment from a false conclusion.

## 8. Next gate

1. implement public development fixtures covering the competency matrix;
2. define deterministic graders for calculations, state handling and decisions;
3. run the current downstream Analytics behavior against those fixtures as a baseline;
4. repair the professional model rather than teaching to individual fixture wording;
5. freeze candidate behavior;
6. create sealed held-out qualification cases;
7. package a reusable core only after behavioral PASS.