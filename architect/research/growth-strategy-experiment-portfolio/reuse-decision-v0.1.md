# Growth Strategy & Experiment Portfolio — reuse decision v0.1

Status: pre-qualification
Date: 2026-08-20

## Target profession

`Growth Strategy & Experiment Portfolio Practitioner`

Target stable responsibility: diagnose the highest-value growth decision under uncertainty, prioritize a bounded portfolio of mechanism-level experiments, define decision contracts, and update strategy from evidence without optimizing proxy metrics or doing downstream specialist work.

## Candidate 1 — Growth Experimentation & Measurement Practitioner 1.0.0

Decision: **EXTEND AS DEPENDENCY, NOT REUSE AS THE TARGET CORE**.

### Compatibility evidence retained

Applicable unchanged invariants:

- preregistration and fixed decision logic;
- measurement/denominator integrity;
- delayed outcome handling;
- attribution vs incrementality discipline;
- bounded `CONTINUE / ITERATE / SCALE / KILL / INCONCLUSIVE` decisions;
- reproducible calculation preference;
- authority/escalation around missing business facts and unsupported causal methods.

### Material gaps

The manifest explicitly excludes campaign strategy and does not own:

- bottleneck/opportunity selection before an experiment exists;
- audience/problem/offer mechanism selection;
- alternative generation;
- cross-channel journey role allocation;
- portfolio prioritization and opportunity cost across candidate bets;
- strategic non-priorities;
- upstream research requests and downstream strategic handoffs.

### Transfer obligations

Retain qualification evidence only for unchanged measurement invariants. Add interaction evals for strategist -> measurement handoff, especially when Strategist attempts to overrule an `INCONCLUSIVE`, repair a denominator post hoc, change horizon, or reinterpret attribution as causality.

## Candidate 2 — Paid Media / Performance Marketing Practitioner 1.0.0

Decision: **ADAPT/REUSE ONLY FOR PAID-MEDIA SUBTASKS; REJECT AS THE GENERAL STRATEGIST CORE**.

### Compatibility evidence retained

Applicable principles:

- business-value precedence;
- measurement-before-optimization;
- causal distinction;
- audience/creative learning;
- diagnosis before expensive changes;
- opportunity-cost/resource discipline;
- spend authority separation.

### Material incompatibility

Its profession is specifically paid-media investment under auctions, budgets, bidding and media allocation. The target Strategist owns organic/owned/paid cross-channel choice and experiment portfolio decisions even when no media spend exists.

Using it as the top-level strategist would create paid-media framing bias and role collision with the existing Paid Media specialist capability.

### Transfer obligations

When a strategy experiment materially uses paid media, hand off spend/media design and execution to the qualified paid-media core. Add boundary tests for double-ownership and unauthorized spend changes.

## Candidate 3 — current applied `auto-sales-growth-system/agents/strategist.md`

Decision: **REJECT AS REUSABLE CORE; RETAIN ONLY AS TARGET-context evidence and regression source**.

Rationale:

- no library manifest;
- no independent qualification record;
- mixed stable profession logic with UAE automotive/platform/business-specific policy;
- contains implementation decisions (platform roles, automotive pricing gate) that must not be promoted into a universal core;
- useful observed design patterns do not constitute professional qualification.

The file should remain untouched until the new core passes qualification. Its strong behaviors should become development/regression requirements, not inherited truth.

## Candidate 4 — public growth-agent / skill repositories

Sources inspected as examples include public growth-marketer, A/B-testing, experimentation and growth-decision repositories surfaced through GitHub search.

Decision: **REJECT FOR CORE REUSE**.

Reasons:

- author-defined role descriptions are not independent profession evidence;
- no compatible qualification provenance for material professional claims;
- common use of universal frameworks or fixed thresholds (for example AARRR/ICE and canned LTV:CAC or conversion benchmarks) can create context-insensitive decisions;
- repository popularity/stars are not construct-valid qualification evidence.

Useful transferable artifacts are limited to non-authoritative patterns such as explicit hypothesis records, guardrails, experiment history and tool-supported documentation.

## Alternatives considered

1. **REUSE Growth Experimentation core as Strategist** — rejected because pre-experiment strategic opportunity selection is outside scope.
2. **REUSE Paid Media core as Strategist** — rejected because it creates channel-specific framing bias.
3. **Composite only: Experimentation + Paid Media with no new core** — rejected because neither owns the missing strategic portfolio/journey judgment; an orchestrator would be forced to fill professional gaps.
4. **BUILD NEW Growth Strategy core with explicit dependencies** — current preferred option.

## Lifecycle/resource trade-off

A new core adds research and qualification cost, but avoids duplicated bespoke strategist prompts across domains and creates a coherent home for portfolio judgment that is currently unowned. Reusing the two existing cores for their qualified sub-boundaries reduces duplicated evaluation and knowledge while preserving their profession boundaries.

## Decision

**BUILD NEW** `growth-strategy-experiment-portfolio` professional core.

Composition:

`Growth Strategy core -> qualified Growth Experimentation & Measurement dependency for measurement adjudication -> qualified Paid Media dependency when spend/media mechanics are material -> domain specialization -> market/live context -> organization/project context`.

## Evidence retained for unchanged invariants

- Growth Experimentation & Measurement 1.0.0 qualification evidence remains supporting evidence only for its unchanged, exact artifact boundary.
- Paid Media / Performance Marketing 1.0.0 qualification evidence remains supporting evidence only for paid-media sub-decisions within its declared scope.

No PASS is transferred to the new strategist core.

## Required new regressions / interaction evals

- vanity metric vs downstream business outcome conflict;
- largest funnel drop vs highest-value actionable bottleneck;
- competitor virality vs local causal evidence;
- numeric prioritization score vs gating constraint/opportunity cost;
- user pressure to launch with unverified commercial facts;
- too-many-variable experiment vs discriminating experiment;
- post-result pressure to change KPI/horizon/denominator;
- channel-fashion pressure to use every platform;
- paid-media strategy routed without unauthorized spend execution;
- Analytics returns `INCONCLUSIVE` and Strategist must not manufacture a winner;
- strong top-of-funnel signal with poor qualified-lead/sales quality;
- low-volume business where formal A/B power is unavailable and another learning design is required;
- capacity/inventory constraint makes a superficially successful strategy non-scalable.
