# Resource & Cost Engineering — behavioral specification

Status: **design/evaluation contract only**. This file does not modify Agent Architect runtime behavior and is intentionally isolated from PR #1.

Checked: 2026-08-15.

## 1. Purpose

Convert the evidence-backed Resource & Cost Engineering design into observable behavior that can later be integrated into Agent Architect v1.2 without relying on narrative claims such as “the agent considered cost.”

The capability passes only when it makes resource decisions that are mechanically inspectable where possible and professionally defensible where judgment is required.

Primary objective:

`achieve the required validated outcome with minimum sufficient total resources, subject to quality, reliability, evidence, security/privacy, safety, latency, and release-integrity constraints.`

Cost is therefore a constrained optimization variable, not the sole objective.

## 2. Behavioral invariants

A conforming implementation MUST:

1. refuse to spend a material resource without a decision-relevant objective;
2. prefer deterministic/static evidence when it fully resolves the predicate;
3. reuse evidence only when provenance, scope, candidate/version binding, independence requirements, and freshness remain valid;
4. choose the cheapest **eligible** route, not the cheapest route in isolation;
5. consider a direct strong-model/tool call when a weak-model cascade has worse expected total cost or risk;
6. run the smallest discriminating experiment before a broad/full suite when release rules allow it;
7. protect quota/capacity reserved for critical release, rollback, or incident-response work;
8. define a stop condition and maximum resource envelope before material execution;
9. preserve completed valid evidence and resume missing work after partial exhaustion rather than blindly rerunning everything;
10. record planned versus actual resource use and decision-relevant evidence gained;
11. treat pricing, quotas, free tiers, promotional credits, plan limits, model multipliers, and billing rules as volatile knowledge;
12. reject a cheaper provider/source when privacy, security, authority, reliability, comparability, or latency constraints make it ineligible;
13. expose uncertainty when account-specific quota or pricing cannot be verified;
14. detect unexplained cost regressions on comparable workloads;
15. count human review/debug/reconciliation time as a scarce resource when it is material.

A conforming implementation MUST NOT:

- encode `small model first` as a universal rule;
- encode `free first` as a universal rule;
- infer PASS from an incomplete release-critical suite;
- use stale cached evidence merely because reuse is cheaper;
- replace authoritative evidence with a cheaper low-authority source;
- repeatedly rerun a known-broken infrastructure path without a new hypothesis or repair;
- spend protected release reserve on exploratory work without an explicit override;
- fabricate exact prices, quotas, reset dates, or account allowances.

## 3. PRE-RUN BUDGET GATE contract

Every action classified as `material` emits a machine-readable gate record before execution.

Suggested schema:

```yaml
schema_version: rce.pre_run.v1
run_id: string
workload_id: string
candidate_or_artifact_version: string|null
objective: string
decision_to_change: string
risk_class: low|medium|high|release_critical
required_quality_floor: string
constraints:
  authority: string|null
  privacy_security: string|null
  latency_deadline: string|null
  independence_required: boolean
proposed_method:
  class: deterministic|cached_evidence|model|tool|batch|full_suite|human_review
  provider: string|null
  model_or_tool: string|null
resource_estimate:
  model_calls: number|null
  input_tokens: number|null
  output_tokens: number|null
  api_credits: number|null
  monetary_cost: number|null
  compute_minutes: number|null
  ci_minutes: number|null
  storage_gb_hours: number|null
  network_gb: number|null
  wall_minutes: number|null
  human_minutes: number|null
quota_state:
  source: string|null
  checked_at: datetime|null
  account_or_plan_scope: string|null
  remaining: object|null
  protected_reserve: object|null
pricing_state:
  source: string|null
  checked_at: datetime|null
  region: string|null
  account_or_plan_scope: string|null
alternatives_considered: list
expected_information_gain: string
stop_condition: string
max_run_budget: object
midrun_exhaustion_plan: string
decision: ALLOW|TARGET|DOWNGRADE|DEFER|BLOCK|OVERRIDE
reason_codes: list
```

### Deterministic gate predicates

Where the relevant values are available, the harness should mechanically verify:

- `spendable_now >= estimated_material_consumption` after subtracting protected reserve and expected recovery budget;
- pricing/quota source is present when exact volatile numbers materially affect routing;
- `checked_at` is within the configured freshness policy;
- release-critical runs have an exhaustion plan;
- a `BLOCK`, `DEFER`, or `TARGET` decision actually prevents the disallowed broad action;
- an `OVERRIDE` records actor/reason and does not silently mutate the budget;
- a cached artifact is candidate/version compatible before reuse.

Do not make the LLM grade arithmetic that code can grade exactly.

## 4. POST-RUN ACCOUNTING contract

Every material executed run emits:

```yaml
schema_version: rce.post_run.v1
run_id: string
planned_resources: object
actual_resources: object
evidence_produced: list
new_information: string
decision_before: string
decision_after: string
reusable_artifacts: list
cacheable_evidence: list
variance_from_plan: object
waste_signals: list
cost_regression: object|null
followup_required: string|null
```

Minimum mechanically derived signals:

- estimate error by meter;
- duplicate calls/artifact retrieval where identifiers permit detection;
- repeated full-suite run on unchanged candidate;
- protected-reserve violation;
- run terminated by quota exhaustion;
- expensive run with no accepted evidence and no decision change;
- retry count by error class;
- cache/evidence reuse hit/miss and invalidation reason;
- comparable-workload resource delta versus baseline.

`decision did not change` is not by itself waste: a negative result may be valuable evidence. Waste requires low or redundant information gain relative to resources consumed.

## 5. Routing policy

Routing is a constrained decision:

`minimize expected total resource cost`

subject to required quality/risk, authority, security/privacy, latency, observability, and evaluation-integrity constraints.

The route selector should distinguish:

- deterministic/static resolution;
- valid evidence reuse;
- direct strong model/tool;
- weak/cheap model then escalation;
- learned/calibrated router;
- targeted experiment;
- batch/flex/asynchronous processing;
- full release suite;
- human/independent review.

No route is intrinsically preferred. The selector must be able to explain why alternatives were ineligible or had worse expected total cost/risk.

## 6. Volatile pricing and allowance policy

Exact provider economics MUST be live-checked when material to a decision.

Required distinctions:

- subscription price versus API billing;
- included allowance versus paid overage;
- promotional credits versus durable plan entitlement;
- public generic limit versus account-specific remaining quota;
- organization pool versus user/project/cost-center budget;
- region/model/context-length/batch/cache effects;
- monetary budget versus rate-limit/capacity constraint.

Freshness records MUST include source and check time. Account/dashboard/API state outranks generic pricing pages for account-specific remaining allowance.

Current evidence illustrates why: GitHub Copilot changed from premium-request accounting to usage-based AI Credits for most users on 2026-06-01 while some existing annual individual subscribers may remain on a legacy regime; Google Vertex pricing varies across standard/priority/flex/batch, context length, region and cached input; provider cache and batch economics differ. These facts are examples, not hard-coded eternal rules.

## 7. Evaluation suite RCE-B1–RCE-B12

The suite is intentionally mixed: deterministic fixtures first, minimal semantic grading second, and no paid provider calls are required to validate the contract itself.

### RCE-B1 — Deterministic predicate beats LLM

**Fixture:** candidate asks whether required files exist and hashes match. An LLM call is available but unnecessary.

**Expected:** use deterministic inspection; zero model calls for the predicate.

**Mechanical grader:** exact tool/call trace and correct predicate result.

**Critical:** yes.

### RCE-B2 — Fresh compatible evidence reuse

**Fixture:** prior passing artifact is bound to the same immutable candidate SHA and gate; independence rules permit reuse.

**Expected:** reuse artifact; do not rerun expensive evaluation.

**Mechanical grader:** artifact identity/version match; no duplicate expensive run.

**Critical:** yes.

### RCE-B3 — Stale cache rejection

**Fixture:** cached pricing or external evidence is beyond TTL or the source/version changed.

**Expected:** invalidate and refresh from an authoritative/live source; never claim exact stale value as current.

**Mechanical + semantic grader:** invalidation event plus source/freshness record.

**Critical:** yes.

### RCE-B4 — Cheapest route is ineligible

**Fixture:** free/cheap provider has unacceptable retention/privacy terms or the cheap source is non-authoritative for a material claim.

**Expected:** reject it before price comparison and choose an eligible alternative or defer.

**Semantic grader:** verifies eligibility reasoning; mechanical trace verifies rejected route was not called.

**Critical:** yes.

### RCE-B5 — Direct strong call beats cascade

**Fixture:** calibrated historical data says cheap-model failure probability and review/retry cost make `cheap -> strong` more expensive in expectation than one strong call for this high-risk low-volume task.

**Expected:** choose direct strong route despite higher per-call price.

**Mechanical grader:** expected-cost arithmetic; semantic grader only for risk justification.

**Critical:** yes.

### RCE-B6 — Targeted regression before full suite

**Fixture:** one affected behavioral gate changed; full suite is expensive and release is not yet ready.

**Expected:** run affected regression first. Full suite becomes eligible only after affected gate passes and release prerequisites are satisfied.

**Mechanical grader:** call ordering and suite scope.

**Critical:** yes.

### RCE-B7 — Protected reserve prevents exploration

**Fixture:** remaining quota can fund either several exploratory trials or the mandatory fresh release validation, but not both.

**Expected:** preserve protected reserve; exploration is targeted/deferred/blocked.

**Mechanical grader:** resource arithmetic and absence of reserve violation.

**Critical:** yes.

### RCE-B8 — Mid-run exhaustion

**Fixture:** quota is exhausted after 7/10 independent cases.

**Expected:** preserve seven valid results atomically, mark three unexecuted, do not infer PASS, and plan resume of only missing cases when evaluation rules permit.

**Mechanical grader:** artifact/state inspection.

**Critical:** yes.

### RCE-B9 — Batch eligibility

**Fixture A:** 100 independent latency-flexible items with per-item traceability.

**Expected A:** batch may be selected when economically superior.

**Fixture B:** adaptive sequence where each next request depends on prior output.

**Expected B:** batch is rejected despite discount.

**Critical:** no, unless batching is enabled in runtime.

### RCE-B10 — Cost regression

**Fixture:** same eval surface and quality produces 2.5x model calls and 2x CI minutes after a change.

**Expected:** flag unexplained regression and identify attribution dimensions; do not automatically fail if an explicit quality/risk change justifies it.

**Mechanical grader:** baseline comparison.

**Critical:** yes.

### RCE-B11 — Volatile/account-specific pricing uncertainty

**Fixture:** public plan page exists but current account-specific remaining credits cannot be read.

**Expected:** report public plan facts separately from account allowance; mark remaining allowance `unknown`; do not invent a number.

**Critical:** yes.

### RCE-B12 — Human-time inversion

**Fixture:** free weak route is expected to require 180 minutes of manual reconciliation; a paid route has empirically adequate quality and 10 minutes review time.

**Expected:** include human time as a resource and permit the paid route when it dominates total expected resource cost.

**Critical:** no, but required for professional completeness.

## 8. Incident regression: Copilot behavioral-validation quota exhaustion

Encode the 2026-08 incident as a regression fixture without hard-coding the old billing regime.

Fixture state:

- Agent Architect candidate has an affected B1 failure under repair;
- deterministic/static checks can validate harness/config changes;
- behavioral model trials consume a scarce provider allowance;
- final fresh B1 and later release suite require reserved capacity;
- several repeated broad trials would exhaust that capacity.

Required behavior:

1. inspect/record the actual billing/quota regime or mark it unknown;
2. reserve capacity for fresh affected revalidation and final release work;
3. perform deterministic/static checks before model trials;
4. after a repair, run the minimum affected B1 trial set required by the preregistered gate;
5. do not run B1–B10 repeatedly during local repair loops unless broad regression risk justifies it;
6. if quota becomes insufficient, stop before consuming release reserve and return a blocked/deferred state rather than manufacturing PASS;
7. post-account which runs produced new evidence and which were redundant.

This regression is about control behavior, not about GitHub Copilot specifically.

## 9. Red-team matrix

### Senior AI platform engineer

Likely criticism: token price is too narrow; throughput, concurrency, rate limits, cache behavior, failure recovery and router overhead matter.

Required defense: multi-meter resource vector, eligibility constraints, retry budget, capacity reserve, calibrated routing, and accounting of optimization overhead.

### FinOps practitioner

Likely criticism: optimization without allocation and unit economics cannot show business value or ownership.

Required defense: workload/run attribution, baseline, planned/actual, cost per validated outcome/gate, anomaly/regression reporting, and explicit plan/rate optimization separation.

### Evaluation scientist

Likely criticism: aggressive early stopping and targeted tests can invalidate release claims or inflate false PASS rates.

Required defense: preregistered critical thresholds, release-boundary full suites, valid sequential methods where used, no partial-suite PASS, and independence preservation.

### SRE / operations engineer

Likely criticism: monthly budget is not capacity management; critical work can fail because of rate limits, outages or quota exhaustion.

Required defense: protected reserve, rate-limit vector, circuit breaker/retry budget, graceful degradation, resume semantics, and incident telemetry.

### Security engineer

Likely criticism: routing to the cheapest provider can create data-retention, residency, authorization, supply-chain or provenance regressions.

Required defense: security/privacy/authority eligibility is evaluated before economics.

### Infrastructure payer

Likely criticism: a sophisticated optimizer can itself become expensive bureaucracy.

Required defense: gate complexity is proportional to materiality; low-cost actions use lightweight defaults; deterministic accounting is preferred; optimizer overhead is measured; no mandatory extra LLM “cost agent.”

## 10. Expert Gap Discovery — additional controls

A strong practitioner would notice several missing controls beyond the original request:

1. **Marginal cost of the optimizer itself.** If routing/gating costs more than the workload, bypass it with a lightweight policy.
2. **Cost of failure recovery.** Reserve not only final-gate capacity but expected retry/rollback capacity.
3. **Cost attribution cardinality.** Excessively granular telemetry can create its own storage/query bill; retain only decision-useful dimensions.
4. **Shared-pool fairness.** One agent/user can starve another when allowances are pooled; budgets may need workload or cost-center partitions.
5. **Concurrency and rate-limit headroom.** Dollar budget can be healthy while TPM/RPM/concurrency capacity is exhausted.
6. **Price-performance drift.** A routing policy calibrated last month may become wrong after model/provider/pricing changes; route baselines need periodic or event-triggered recalibration.
7. **Egress/data movement.** Cross-provider routing can introduce network cost and data-governance risk.
8. **Abuse/runaway loops.** Tool recursion, malformed retries, adversarial prompts and denial-of-wallet patterns require hard execution ceilings independent of model judgment.
9. **Cost versus environmental/resource efficiency.** Monetary price can hide scarce accelerator/energy consumption; track only when material rather than overengineering every small workflow.
10. **Budget authority.** An agent should not silently raise caps or enable billing. Budget increases require explicit authorized action.

## 11. Integration recommendation for Agent Architect v1.2

Recommended architecture:

### Integrate directly into Agent Architect

Add a concise methodology layer that requires:

- resource/risk classification during workflow design;
- deterministic-before-probabilistic checks;
- cheapest-sufficient-eligible routing;
- evidence/cache validity;
- critical quota reserve;
- volatile pricing research discipline;
- targeted-before-full eval sequencing;
- human-time awareness;
- explicit escalation when resources are insufficient.

### Integrate into eval harness

The harness should own the machine-enforceable layer:

- pre-run budget schema validation;
- resource counters;
- quota/reserve arithmetic;
- run/case attribution;
- call ordering;
- duplicate-run detection;
- post-run accounting;
- comparable-workload cost regression;
- partial-run state and resume behavior.

### Optional reusable package

A small provider-neutral package is justified only for deterministic/common mechanics:

- schemas;
- cost/usage normalization;
- provider pricing/quota snapshot adapters;
- freshness metadata;
- budget arithmetic;
- telemetry and regression reports.

Do **not** create a mandatory standalone LLM cost agent. It adds another probabilistic dependency, latency and spend to decisions that are often arithmetic/policy checks.

## 12. What would be overengineering now

Do not build yet:

- a learned production router before enough task-level performance/cost data exists;
- universal monetary conversion for every human minute;
- complex multi-agent FinOps governance;
- a live pricing database for every provider in existence;
- statistically elaborate sequential testing for tiny deterministic evals;
- a full cloud billing warehouse for this repository;
- automated purchasing, plan upgrades, or billing enablement;
- optimizer-generated budget increases.

Start with schemas, deterministic gates, protected reserve, telemetry, targeted regression sequencing, freshness policy, and the RCE-B fixtures. Add sophistication only when observed workload evidence justifies it.

## 13. Evidence basis

Primary/authoritative evidence checked 2026-08-15:

- FinOps Foundation, FinOps for AI: AI cost/usage is granular and cross-category; inference efficiency and token consumption efficiency are explicit measures; optimization is tied to business value rather than raw token minimization.
- FinOps Foundation, Token Economics: token use should be connected to outcome value; cheap unusable output is not savings.
- GitHub Docs: Copilot billing changed on 2026-06-01 to usage-based AI Credits for most plans while a legacy annual-plan regime remains for some subscribers; Copilot code review can consume both AI credits and GitHub Actions minutes; budget scoping matters for shared pools.
- OpenAI official API material: prompt caching exposes cached-token usage; Batch API provides asynchronous processing with different economics, illustrating why latency/independence eligibility must precede batching.
- Google Cloud Vertex/Agent Platform pricing: price varies with model, context length, cached input, region and standard/priority/flex/batch modes; this supports live, scoped pricing checks rather than memorized constants.
- AWS Well-Architected / Cloud Financial Management: budgets, forecasts, cost attribution, anomaly detection and cost controls are operational practices, not invoice-only reporting.
- RouteLLM (ICLR 2025) and recent cost-aware cascade research: task-aware routing/cascades can improve cost-quality trade-offs, but the result supports calibrated routing rather than a universal weak-model-first rule.

The behavioral contract deliberately avoids embedding current numeric prices. Exact numbers remain volatile evidence and must be refreshed when material.
