# Field Evidence / Production Feedback Loop

## Purpose

Behavioral qualification proves that a Professional Core or specialization can make required decisions under controlled fixtures. It does **not** prove production effectiveness. Real projects therefore provide a separate evidence class: **field evidence**.

Field evidence must improve professional models without allowing one customer, market, platform, campaign, or lucky outcome to contaminate reusable expertise.

## Evidence classes

Keep these distinct:

1. **Behavioral evaluation evidence** — controlled fixtures, reliability trials, frozen graders.
2. **Field observation** — what actually happened in a consuming project.
3. **Live-context evidence** — current market/platform/regulatory/account facts that may expire.
4. **Organization evidence** — company economics, authority, capacity, CRM and operating process.
5. **Experiment evidence** — one campaign/product/vehicle/test and its outcomes.
6. **Reusable professional evidence** — evidence supporting a transferable competency, judgment policy or failure mode.

A field observation is not reusable professional evidence merely because it occurred in production.

## Required production trace

For a field experiment that may teach the professional model, preserve when available:

### Before action
- decision owner and authority boundary;
- hypothesis and serious alternative explanation;
- known facts, unknowns and assumptions;
- measurement plan and data-quality limitations;
- primary business outcome and proxy metrics;
- expected causal mechanism;
- stop / iterate / scale criteria;
- relevant opportunity cost;
- specialist recommendation and rationale recorded **before** the outcome is known.

### During action
- material decisions and timestamps;
- spend/resource changes;
- measurement or tracking failures;
- inventory/availability changes where relevant;
- operational constraints and handoff failures;
- interventions that can confound interpretation;
- outcome chain at the highest trustworthy resolution available.

### After action
- observed outcome;
- comparison with the pre-action hypothesis and alternatives;
- decision-quality review separate from outcome quality;
- measurement validity review;
- root-cause hypotheses and counterevidence;
- whether the finding is local, live-context, or plausibly reusable;
- unresolved uncertainty.

## Decision quality is not outcome quality

Do not reward a poor decision because it got lucky. Do not punish a sound decision solely because a stochastic outcome was bad.

Review at least:
- whether the decision used the best evidence available at the time;
- whether uncertainty was represented honestly;
- whether measurement was decision-fit;
- whether alternatives were considered;
- whether authority and resource constraints were respected;
- whether the decision policy would remain defensible across repeated comparable cases.

## Promotion gate

A project finding may modify a reusable Professional Core or durable specialization only after this sequence:

`field observation -> evidence validity check -> root-cause analysis -> alternative explanations -> transferability classification -> corroboration -> adversarial eval -> model change -> regression/reliability qualification -> versioned release`

### Default disposition

**KEEP LOCAL** unless promotion is justified.

Possible dispositions:
- `NO_CHANGE` — outcome provides no credible professional-model update;
- `PROJECT_CONTEXT` — organization-specific fact/process/economics;
- `LIVE_CONTEXT` — market/platform/regulatory/account fact requiring freshness control;
- `EXPERIMENT_LEARNING` — useful for future tests but not yet reusable expertise;
- `EVAL_CANDIDATE` — reveals a plausible reusable failure mode; add/strengthen evaluation before changing the model;
- `SPECIALIZATION_CANDIDATE` — evidence supports a domain-transferable judgment delta;
- `CORE_CANDIDATE` — evidence supports a cross-domain professional invariant.

## Promotion evidence standard

One successful or failed production experiment is normally insufficient to create a durable professional rule.

Before promotion, seek the strongest practical corroboration available, such as:
- recurrence across materially different project instances;
- independent authoritative or empirical literature;
- platform-independent mechanism evidence;
- practitioner consensus supported by reasons/evidence rather than popularity;
- controlled or quasi-controlled comparisons;
- an adversarial behavioral fixture reproducing the discovered failure mode.

The required strength increases with blast radius. A Core change requires stronger transferability evidence than a domain-specialization change.

## Causal and measurement guardrails

Do not infer reusable causality from before/after performance alone. Check plausible confounders including creative, offer, price, inventory, audience mix, seasonality, sales follow-up, tracking changes, platform delivery, capacity and external demand.

If the measurement chain is broken, classify the result as measurement-limited rather than inventing a business conclusion.

## Negative and null evidence

Capture failures, null results and stopped experiments. Do not build the learning system only from winners.

A stopped experiment can be high-value evidence when it demonstrates a correct stop-loss, measurement repair, compliance escalation or protection against invalid scale.

## Anti-overfitting rules

Never promote directly from:
- one vehicle, SKU, campaign or customer;
- one country-specific rule;
- one platform UI/mechanic;
- one company's margin, budget or sales process;
- one model response;
- one lucky/unlucky outcome;
- a post-hoc story without pre-action trace;
- vanity metrics without downstream business evidence.

Named experiment instances remain instances. Example: a Toyota Yaris campaign can reveal a candidate failure mode, but it must not create a `Toyota Yaris specialist`.

## Feedback into evaluation

When field evidence reveals a plausible reusable judgment defect, prefer creating an **eval candidate before editing the professional model**.

The new fixture should:
- reproduce the decision structure, not confidential project facts;
- remove irrelevant local details;
- preserve the failure-inducing uncertainty or trade-off;
- include a serious positive control where applicable;
- distinguish construct failure from action-word preference;
- freeze the grader before qualification.

If the current model already passes the new adversarial fixture reliably, do not add redundant rules merely because a production outcome was surprising.

## Model-change gate

If a reusable defect is confirmed:
1. identify the smallest responsible layer: Core vs domain specialization;
2. repair root cause, not the observed wording;
3. preserve parent invariants;
4. run deterministic/static checks first;
5. run the minimal affected behavioral test;
6. for critical stochastic transitions, run reliability trials;
7. run broader regression/release evaluation only after the affected gate passes;
8. version the changed artifact and record provenance from field evidence to eval to repair.

## Resource discipline

Do not replay expensive production/evaluation suites by default.

Use this order:
1. deterministic evidence/schema checks;
2. evidence-quality and transferability review;
3. minimal affected fixture;
4. critical reliability trials if needed;
5. broader regression only when justified.

Field learning is not permission for continuous model churn.

## Red-team questions

Before promotion ask:
- What would explain this result without changing the professional model?
- Is this a market/company/platform fact masquerading as expertise?
- Would the proposed rule survive another country, company and platform?
- Are we learning from decision quality or merely from outcome luck?
- What evidence would falsify the proposed lesson?
- Would a senior practitioner, researcher/teacher and hiring manager all recognize the proposed delta as professional competence?
