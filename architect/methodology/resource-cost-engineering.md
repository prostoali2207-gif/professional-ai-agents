# Resource & Cost Engineering

## Purpose

Resource & Cost Engineering makes resource use a first-class architectural constraint without turning cost minimization into the objective. The goal is to achieve the required professional outcome with the minimum sufficient total resources while preserving quality, reliability, security, evidence authority, latency requirements, and release integrity.

Optimize neither `free`, `cheap`, nor `fewest tokens` in isolation. Optimize expected validated value under explicit constraints.

## Resource model

Treat resources as a heterogeneous vector, not one dollar number. Relevant meters may include:

- model/tool calls;
- input/output/cached tokens;
- provider credits and account-specific quota;
- request/rate-limit headroom;
- compute and CI minutes;
- storage and network transfer;
- latency and wall-clock time;
- human review/debugging time;
- protected capacity for release, rollback, or incident recovery.

Do not collapse incomparable meters into money unless the conversion is decision-relevant and supportable.

## Eligibility before optimization

Before comparing cost, remove methods/providers/sources that fail a hard requirement. Eligibility can depend on:

- minimum empirical quality for the task;
- evidence authority and source requirements;
- privacy, retention, residency, compliance, permissions, and blast radius;
- reliability and availability;
- latency/SLO;
- evaluation independence/comparability;
- required observability and auditability.

A cheaper ineligible option is not an optimization candidate.

## Deterministic-first discipline

Before using an LLM or paid external tool, ask whether the required truth condition is mechanically observable through direct state inspection, parsing, schema validation, diffing, arithmetic, static analysis, deterministic tests, exact API state, or deterministic grading.

If deterministic evidence settles the decision, do not buy a probabilistic re-answer merely for narrative confirmation.

Use a hybrid pattern when only part of the problem is mechanical:

`deterministic pre-filter -> semantic judgment on residue -> deterministic post-check of observable claims`.

## Evidence reuse and cache discipline

Before a new run, test whether existing evidence can validly answer the current decision. Reuse requires compatible:

- source/candidate/version identity;
- task scope and jurisdiction;
- evidence-generating conditions;
- freshness;
- provenance;
- independence requirements;
- privacy/retention policy.

Freshness by timestamp is not sufficient when scope, population, jurisdiction, authority, or candidate binding differs.

Distinguish provider prompt cache, application-result cache, evidence cache, and eval-artifact reuse. They require different invalidation rules.

## Pre-run budget gate

Apply a compact gate before a materially expensive, quota-sensitive, latency-sensitive, or human-expensive action. Trivial inexpensive actions do not require ceremony.

The gate must establish, as applicable:

1. **Objective** — what must this run produce or prove?
2. **Decision impact** — what plausible result could change the next action?
3. **Risk/quality floor** — what failure consequence or release criticality applies?
4. **Alternatives** — can deterministic/static verification or valid reusable evidence settle it?
5. **Eligible route** — which methods meet quality, authority, security, reliability, latency, observability, and independence constraints?
6. **Resource estimate** — expected calls/tokens/credits/compute/CI/human time where material.
7. **Quota state** — known remaining capacity and rate-limit constraints where observable.
8. **Protected reserve** — capacity that must remain available for release, rollback, recovery, or other critical work.
9. **Pricing/allowance freshness** — if exact cost/allowance materially changes the decision, verify live from an official or account-specific source.
10. **Stop condition** — when to stop because sufficient evidence exists or the hypothesis has failed.
11. **Mid-run exhaustion plan** — how partial evidence is preserved and how PASS is prevented when required gates are incomplete.
12. **Maximum run budget** — a hard or soft cap appropriate to the workload.

The result may be `ALLOW`, `TARGET`, `DOWNGRADE`, `DEFER`, or `BLOCK`.

### Protected reserve

Do not treat all remaining quota as spendable. When a future release/recovery gate is mandatory, conceptually reserve:

`spendable_now = remaining_capacity - protected_critical_reserve - expected_failure_recovery`

Exploration must not consume the reserve without an explicit release-critical override.

## Cheapest sufficient eligible route

Do not encode `small model first` as a universal rule.

Progressive escalation is useful when lower-cost stages can reliably eliminate uncertainty, but it is not mandatory. A single stronger model/tool may have lower expected total cost when weak-model failures create retries, human repair, latency, or critical false-negative risk.

Choose the route that minimizes expected total constrained resources **subject to the quality/risk floor**. Use empirical task evidence or calibrated routing evidence where available; do not route by list price alone.

## Targeted experiment before broad execution

During repair/development loops, prefer the smallest discriminating experiment that can test the changed hypothesis. After a local repair, run the affected regression before a full suite unless shared coupling makes broad regression plausible.

Full suites remain justified when:

- the change touches shared infrastructure or cross-cutting behavior;
- the release protocol preregisters a full suite;
- the affected surface is genuinely unknown;
- independence or reliability claims require repeated/broad evidence.

Do not optimize away mandatory independent release evidence merely because it is expensive or confirms the same decision.

## Early stopping and sampling

Predeclare thresholds and stopping conditions for release claims. Do not repeatedly peek at noisy outcomes and stop opportunistically. Use statistically valid sequential procedures when inference depends on repeated trials and early stopping matters.

For deterministic failures, stop immediately once the failure conclusively invalidates the run and further calls cannot add decision-relevant evidence.

## Batching

Batch only when jobs are independent, latency is flexible, item-level attribution remains observable, partial failures can be isolated, and batch semantics do not alter the experiment.

Do not batch adaptive workflows where the next action depends on the prior result, or where batch execution degrades observability, deadline reliability, or attribution.

## Volatile pricing, quotas, and free tiers

Treat exact prices, quotas, free tiers, promotional credits, plan limits, model multipliers, billing units, and allowance rules as volatile knowledge.

When such a value materially affects a decision:

- verify live rather than relying on model memory;
- prefer official pricing/billing/limits documentation and account telemetry;
- record the verification date/time and source;
- distinguish subscription fees, included allowance, API billing, promotional credits, plan-specific access, organization/project pools, and account-specific quota;
- represent unknown values as `unknown` rather than inventing precision;
- re-check when freshness is no longer adequate for the decision.

Generic public pricing does not prove account-specific remaining quota.

## Human-time and delay cost

Human review, debugging, reconciliation, and rework are resources even when no monetary valuation is available. Track `human_minutes` separately when material.

A free weak route can be globally more expensive than one paid call if it creates hours of repair or materially higher error risk.

## Retry and failure controls

A retry budget is an upper bound, not permission to retry every failure. Classify the failure before spending another call.

- Behavioral/evidence failure -> repair the responsible layer; do not retry unchanged behavior hoping for a different answer.
- Authentication/configuration failure -> repair configuration before another request.
- Daily/project quota exhaustion -> **do not retry the same quota-bound route while the quota state or quota window is unchanged**. Resume only after directly observed capacity restoration, or use another sufficient eligible route. When the required authoritative primary source is already known and direct inspection is eligible, prefer that route over retrying or ensembling an exhausted discovery provider.
- Retired/unsupported model or endpoint -> verify lifecycle and migrate; do not retry the obsolete route unchanged.
- Short rate limit, transient capacity/503, or provider outage -> bounded retry/backoff/fallback is allowed only when there is a concrete unresolved gap, a reason to expect conditions to change, and sufficient budget/quota reserve.

Retries require a bounded retry budget, backoff where appropriate, and a new reason to expect success. Stop retry storms against unchanged infrastructure/provider failures.

If a workflow exhausts quota or budget mid-run:

- preserve completed valid evidence atomically;
- mark incomplete required gates explicitly;
- never infer PASS from partial completion;
- resume missing compatible work rather than repurchasing valid completed evidence;
- use a fallback provider/model only when it remains eligible and does not invalidate preregistered comparability/independence.

## Post-run accounting

For material runs compare planned and actual resource use with decision-relevant information gained. Record as applicable:

- planned vs actual calls/tokens/credits/compute/CI/human time;
- evidence produced;
- genuinely new information;
- decision before vs after;
- reusable artifacts;
- estimate variance;
- retry count;
- waste/cost-regression signal.

Flag investigation when there is high spend with little decision-relevant evidence, duplicate execution on an unchanged candidate without a new hypothesis, full-suite execution where a targeted regression was sufficient, an expensive LLM grader reproducing a deterministic predicate, retry-budget overrun, or unexplained resource growth on a comparable eval surface.

Do **not** classify an unchanged decision as waste by itself. Independent confirmatory release evidence can be required by design.

## Cost regression

For stable workloads keep comparable baselines such as calls per fixture, tokens per fixture, grader calls, CI minutes, wall time, storage, human review time, and quality/pass outcomes.

A cost regression is unexplained deterioration in resource efficiency under comparable requirements, not simply higher spend. Higher cost can be legitimate when quality, risk, workload, or evidence requirements changed.

## Observability and attribution

Where material, attribute consumption to task/agent/experiment/eval case/trial/model/provider/candidate version. If attribution is impossible, avoid making precise optimization claims.

Separate estimated consumption from actual provider/account telemetry.

## Integration boundary

Agent Architect should own the decision rules and evaluation discipline, but should not become a cloud billing platform, provider price catalog, procurement manager, universal human-cost calculator, or production learned router.

Keep provider-specific billing adapters and deterministic resource schemas modular. Add richer FinOps infrastructure only when a concrete workload demonstrates value beyond its own overhead.

## Failure modes to red-team

Explicitly test for:

- false economy that lowers reliability or safety;
- cheap model missing a critical failure;
- stale or scope-incompatible cache reuse;
- free provider violating privacy/retention/compliance;
- batch mode destroying adaptive semantics or observability;
- cost optimization violating latency/SLO;
- cheaper secondary source replacing required authoritative evidence;
- critical workflow starvation after exploration consumes quota;
- stale pricing/plan assumptions;
- optimizing benchmark price while worsening real human/rework cost;
- optimization-layer overhead exceeding savings;
- mandatory release evidence incorrectly labeled waste.

## Evidence and evaluation

Mechanically inspectable rules belong in deterministic tests. Professional trade-off judgment requires sealed adversarial cases with frozen expected decision properties and independent grading.

Use `../evaluation/resource_cost_engineering/` for the current RCE fixtures and contracts. Do not count narrative self-assessment as semantic PASS.
