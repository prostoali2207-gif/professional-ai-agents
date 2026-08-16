# Resource & Cost Engineering — Agent Architect v1.2 integration recommendation

Status: proposal only. Do not integrate until the owning Agent Architect release track explicitly accepts it.

## Decision

Integrate Resource & Cost Engineering as a cross-cutting decision/control layer in Agent Architect and its evaluation harness. Do **not** create a mandatory standalone LLM cost agent.

A small reusable deterministic package is justified for resource vectors, freshness metadata, budget-gate arithmetic, post-run accounting, and provider/account telemetry adapters. Provider-specific pricing tables must not be hard-coded as durable knowledge.

## Minimum v1.2 integration surface

### 1. Planning / workflow design

Before a materially expensive or quota-sensitive action, require:
- objective and decision the run can change;
- risk/quality floor;
- deterministic/static and reusable-evidence check;
- cheapest eligible method, not cheapest method;
- expected information gain;
- stop condition;
- mid-run exhaustion behavior;
- protected critical-path reserve where relevant.

This should be a compact gate, not a long narrative ceremony for trivial calls.

### 2. Evaluation harness

Add resource metadata to behavioral/eval runs:
- run/case/trial identity;
- model/tool/provider;
- model calls and tokens when observable;
- provider credits/quota units when observable;
- CI/compute duration when material;
- human review minutes when material;
- affected-vs-full-suite scope;
- retry count/retry budget;
- candidate/version binding;
- planned vs actual resources.

Require targeted affected regression after a local repair unless broad coupling makes a full suite necessary. Preserve full-suite execution for preregistered release gates.

### 3. Volatile pricing/quota policy

When exact price, allowance, quota, billing mode, plan limit, or free-tier status can change the decision:
- verify live from an official pricing/billing/limits source or account telemetry;
- record checked_at;
- distinguish generic public pricing from account-specific allowance;
- represent unknown values as unknown rather than invented precision;
- re-check before a material purchase, migration, or expensive gate if freshness is no longer adequate.

### 4. Provider/model selection

Filter for eligibility before cost optimization:
- evidence authority;
- privacy/security/retention;
- reliability;
- latency/SLO;
- evaluation comparability/independence.

Then optimize expected total resources among eligible choices. Do not encode `small model first` as a universal rule. A direct strong-model call is valid when its expected total cost/risk is lower than a cascade.

### 5. Post-run learning

Record planned vs actual consumption and decision-relevant evidence gained. Flag:
- duplicate run on unchanged candidate without a new hypothesis;
- full suite when affected regression was sufficient;
- expensive LLM grading of a deterministic predicate;
- retry-budget overrun;
- material spend with no new evidence and no changed decision;
- unexplained cost regression against a comparable baseline.

Do not treat every unchanged decision as waste: confirmatory release evidence can be necessary by design.

## What should remain outside Agent Architect core

Do not turn v1.2 into:
- a cloud billing platform;
- a provider price catalog;
- a full FinOps forecasting system;
- a learned production model router;
- a procurement/subscription manager;
- an autonomous billing enabler;
- a universal dollar valuation of human time;
- a complex statistical sequential-testing framework for every eval.

Those are integrations or future capabilities only when a concrete workload demonstrates value.

## Reusable package boundary

A reusable deterministic package is justified if it remains small and provider-neutral:
- `ResourceVector` / heterogeneous meter schema;
- `BudgetGateInput` / `BudgetGateResult`;
- freshness/provenance metadata;
- reserve and hard-cap arithmetic;
- post-run variance/waste signals;
- adapters that ingest provider/account usage without embedding pricing memory.

A standalone LLM agent is not justified because:
- the checks must execute before the expensive action;
- many predicates are deterministic;
- an extra model hop adds cost, latency, and another failure surface;
- it can create recursive optimization overhead;
- resource telemetry belongs close to execution/evaluation infrastructure.

## Required semantic/adversarial evaluation before integration claim

The deterministic RCE-B1–B12 suite proves only mechanical semantics. Before calling the capability professionally validated, add semantic cases where judgment is genuinely required:

1. A cheap model is empirically weaker on a rare critical failure; choose stronger despite price.
2. A cached authoritative source is fresh by timestamp but incompatible in jurisdiction/scope; reject reuse.
3. A free provider is cheaper but violates confidentiality/retention requirements; reject it.
4. Batch mode is cheaper but invalidates adaptive next-step logic; choose synchronous execution.
5. A direct strong call has lower total expected cost than a weak-model cascade plus human repair; choose direct strong.
6. Full-suite rerun is justified because a shared dependency creates broad regression risk; do not over-target.
7. Expensive independent release evidence changes no decision but is still mandatory; do not label it waste.
8. Public pricing is fresh but account-specific quota is unknown; defer a quota-sensitive run rather than infer allowance.
9. A lower-cost source cannot satisfy an authoritative-primary-source requirement; pay or escalate rather than downgrade evidence.
10. Latency/SLO dominates a cheaper batch route; choose the faster eligible path.

These should use sealed expected decisions and, where an LLM is required to exercise professional judgment, a minimal affected sample before any larger suite.

## Expert-gap / red-team resolution

### Senior AI platform engineer
Would reject a pure dollar budget. Resolution: model heterogeneous resource vectors, rate/quota headroom, recovery reserve, and execution failure semantics.

### FinOps practitioner
Would reject cost reduction without value attribution. Resolution: tie spend to decision/evidence gained and maintain comparable unit metrics.

### Evaluation scientist
Would reject opportunistic early stopping and repeated peeking. Resolution: preserve preregistered release thresholds; use targeting only in repair loops and statistically valid stopping where inference claims depend on repeated trials.

### SRE / operations engineer
Would reject workflows that consume the last available capacity. Resolution: protected critical-path reserve, retry budgets, circuit-breaking semantics, partial-evidence preservation, resumability.

### Security engineer
Would reject cheapest-provider routing before eligibility filtering. Resolution: privacy, retention, permissions, authority and compliance are hard eligibility constraints.

### Infrastructure payer / owner
Would reject an optimization layer whose overhead is unmeasured. Resolution: measure economizer overhead and keep the core deterministic/small; only add learned routing or richer FinOps infrastructure after demonstrated payback.

## Integration gate

Recommend v1.2 integration only after:

`research/design accepted -> deterministic RCE-B1–B12 PASS -> semantic/adversarial affected suite PASS -> integration diff -> regression suite -> release evidence`

Current state at creation of this document:
- research/design: complete;
- deterministic executable semantics: 12/12 local PASS;
- semantic/adversarial RCE suite: not yet executed;
- Agent Architect integration: not performed.
