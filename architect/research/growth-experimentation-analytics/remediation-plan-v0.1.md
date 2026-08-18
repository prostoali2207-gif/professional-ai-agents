# Growth Experimentation & Measurement — remediation plan v0.1

Status: development plan; no downstream behavior changed yet.
Date: 2026-08-18.

## Purpose

Convert the open development fixtures and competency audit into a bounded upgrade plan for the current `auto-sales-growth-system/agents/analytics.md`. This file does not declare the current agent qualified and does not modify the downstream agent.

## Preserve

The current Analytics Agent already contains strong behavior that should survive the upgrade unless testing disproves it:

- freeze the primary KPI and decision rule before reading results;
- views cannot rescue a lead/sales experiment;
- missing/unknown is not zero;
- attribution is not incrementality;
- fixed-horizon peeking is not a valid stopping rule;
- post-hoc segments are hypotheses, not proof;
- funnel denominators must describe the same eligible population;
- small samples require counts, denominators and uncertainty;
- `INCONCLUSIVE` is a valid result;
- Strategist owns the final portfolio decision.

## Add or strengthen

### R-01 — Assignment / delivery integrity

Add an explicit pre-inference check for randomized experiments:

1. expected assignment ratio;
2. observed assignment ratio;
3. observed eligible exposure by variant;
4. whether imbalance has a documented operational explanation;
5. if material unexplained mismatch exists, block causal winner selection.

Do not mechanically run SRM logic on non-randomized content tests.

### R-02 — Instrumentation sanity

Add a measurement sanity gate that can request A/A or equivalent instrumentation checks when there is evidence of asymmetric tracking, pipeline drift or systematic false positives. Do not require A/A for every automotive experiment.

### R-03 — Sample adequacy / MDE

Require distinction between:

- business minimum useful effect;
- statistically detectable effect under the available sample;
- observed effect.

When the experiment cannot realistically distinguish the business-relevant effect, label it underpowered rather than interpreting a noisy percentage.

### R-04 — Metric quality

Before trusting a primary KPI, check whether it is:

- directionally aligned with business value;
- sensitive enough to the treatment;
- defined consistently across variants;
- protected by downstream guardrails where a proxy can improve while business value worsens.

### R-05 — Selection / censoring / outcome maturity

Explicitly model:

- delayed appointments/sales;
- incomplete follow-up;
- right-censoring from early reads;
- post-treatment inclusion/exclusion changes;
- inventory becoming unavailable during the measurement window.

Missing or immature outcomes must not become observed zeroes.

### R-06 — Duplicate identity / multi-touch handling

Add an explicit identity reconciliation step before counting leads, appointments or sales. Multiple touchpoints may exist for one person, but the business outcome must not be double-counted.

### R-07 — Concurrent experiment contamination

Check whether the same audience, vehicle, WhatsApp destination or time window received other campaigns/treatments that break the intended isolation. Grade contamination and downgrade or block causal interpretation when necessary.

### R-08 — Scale economics

`SCALE` must mean more than "the treatment worked." When spend or operating capacity is decision-relevant, require available evidence on:

- cost per qualified lead / appointment / sale;
- gross profit or other approved unit-economics guardrail when available;
- response/follow-up capacity;
- evidence of diminishing returns risk.

If these data are not required by the preregistered decision rule, do not invent them; bound the recommendation instead.

### R-09 — Reproducible calculations

Every material calculation used to justify a decision must expose:

- inputs;
- formula/method label;
- result;
- unit;
- assumptions or reason calculation is unavailable.

Narrative arithmetic is insufficient for qualification.

### R-10 — Decision output discipline

For every recommendation, output separately:

1. final recommendation;
2. primary KPI result;
3. data-integrity status;
4. uncertainty/sample status;
5. confounder severity;
6. causal-claim ceiling;
7. next evidence/action required.

This makes grading and downstream handoff deterministic enough to audit.

## Open-fixture mapping

- F-01 -> preserve commercial KPI priority; strengthen metric-quality guardrail.
- F-02 -> R-01.
- F-03 -> preserve stopping-rule discipline.
- F-04 -> R-03 + R-09.
- F-05 -> preserve no post-hoc rescue.
- F-06 -> preserve denominator discipline + R-09.
- F-07 -> preserve attribution/incrementality boundary.
- F-08 -> preserve missing-state discipline + R-05.
- F-09 -> R-07.
- F-10 -> R-05.
- F-11 -> preserve metric-definition/version governance.
- F-12 -> R-08 + R-09 while preserving preregistered decision execution.
- F-13 -> R-06.
- F-14 -> R-08 + operational-capacity confounder handling.

## Upgrade boundary

Do not turn the reusable professional core into a Meta/Instagram/WhatsApp-specific prompt. Stable experimentation and measurement behavior belongs in the core. Automotive funnel, vehicle inventory, UAE channel context and showroom economics remain specialization/live context.

Do not modify the downstream Analytics Agent until:

1. the development runner can feed a frozen candidate and parse a structured result;
2. the public fixtures are represented as machine-readable inputs without expected answers in the candidate payload;
3. the grader can deterministically check the most important failure conditions;
4. the first upgraded candidate is versioned separately from the current downstream file.

## Qualification rule

Passing the public fixtures only means `DEVELOPMENT PASS`. It does not qualify the agent.

Final qualification requires a frozen candidate digest and new sealed held-out cases created after freeze. Those held-out cases and expected answers must not be visible to the candidate or used for repair.