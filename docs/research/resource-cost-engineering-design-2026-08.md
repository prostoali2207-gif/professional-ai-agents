# Resource & Cost Engineering — evidence-backed design for Agent Architect

Status: research/design only. This document does **not** modify Agent Architect runtime behavior and does not change PR #1.

Checked: 2026-08-14.

## 1. Problem definition

Resource & Cost Engineering is the professional capability to achieve the required outcome with the minimum sufficient total resource consumption **without violating quality, reliability, security, evidence, latency, or safety requirements**.

The optimization target is not `lowest dollar cost`. It is closer to:

`maximize validated outcome value / total constrained resources`

where constrained resources may include money, model tokens, API credits, provider quotas, rate-limit headroom, compute, CI minutes, storage, network, wall-clock latency, human attention, and scarce release-validation opportunities.

This follows the FinOps principle that business value drives technology decisions and that teams must make conscious trade-offs among cost, quality, and speed. FinOps for AI additionally treats inference efficiency and token consumption efficiency as first-class measures.

## 2. Reconstructed professional model

The capability combines four professions rather than one:

### AI/ML platform engineer
- understands model serving, routing, context/token mechanics, caching, batching, quotas, retries, latency and throughput;
- distinguishes deterministic computation from probabilistic model work;
- designs graceful degradation and capacity reservation;
- measures actual resource use rather than estimating only from list prices.

### FinOps practitioner
- allocates spend/usage to workloads and decisions;
- uses budgets, forecasting, anomaly detection, unit economics and value metrics;
- treats variable consumption as an engineering control problem rather than a monthly invoice review;
- separates usage optimization from rate/plan optimization.

### Evaluation engineer / evaluation scientist
- knows when a full benchmark is necessary and when an affected regression is sufficient;
- distinguishes release evidence from exploratory evidence;
- pre-registers critical gates, stopping criteria and sample-size logic;
- prevents repeated noisy testing from masquerading as stronger evidence.

### Systems/SRE engineer
- treats quota exhaustion, runaway retries, cost spikes and unavailable providers as operational failure modes;
- reserves capacity for critical workflows;
- designs hard caps, circuit breakers, retry budgets, degradation paths and post-incident learning.

## 3. Expert competencies

A strong implementation needs at least these competencies:

1. Resource accounting across heterogeneous meters.
2. Cost attribution to task / agent / experiment / evaluation case / model / provider.
3. Cost-quality-latency-risk trade-off analysis.
4. Provider quota and rate-limit interpretation.
5. Model/tool routing under explicit quality constraints.
6. Deterministic-vs-LLM decision discipline.
7. Reuse and caching with freshness/provenance controls.
8. Batching eligibility and observability-preserving execution.
9. Progressive escalation and early stopping.
10. Experimental design and sample-size discipline.
11. Budget reservation and stop-loss behavior.
12. Capacity planning for critical gates.
13. Human-time accounting and opportunity-cost awareness.
14. Pricing-plan/free-tier research with freshness metadata.
15. Privacy/security/compliance checks before selecting a cheaper provider.
16. Cost-regression detection and rollback/escalation.
17. Failure recovery when a workflow cannot finish within the remaining budget.

## 4. Core decision framework

The initial cascade proposed in the task is directionally sound but incomplete. Research on LLM cascades and routing supports selective escalation, but also shows that naive confidence/uncertainty rules can fail for generative tasks. RouteLLM and related work show that routing can materially improve the cost-quality Pareto frontier; Google research on LM cascades shows that deferral rules need task-aware calibration rather than a simplistic confidence threshold.

The recommended decision process is therefore:

1. **Define required evidence / outcome.**
   - What must this action prove or produce?
   - What is the consequence of a false PASS / false negative / stale answer?

2. **Classify risk and quality floor.**
   - low / medium / high / release-critical;
   - authoritative-source requirement;
   - security/privacy constraints;
   - latency deadline.

3. **Check deterministic/static resolution first.**
   - parser, schema validator, diff, unit test, static analysis, exact calculation, direct API state, repository inspection, deterministic grader.
   - If deterministic evidence answers the question, do not spend LLM calls to re-answer it narratively.

4. **Check reusable evidence.**
   - existing fresh artifact, prior passing evidence on unchanged code, immutable source, cached provider result.
   - reuse only if provenance, scope, candidate/version binding and freshness are valid.

5. **Estimate marginal information gain.**
   - What uncertainty remains?
   - What result from the proposed run could change the decision?
   - If no plausible result changes the next action, the run is waste.

6. **Choose cheapest *eligible* method.**
   - eligible means it meets quality, authority, privacy/security, observability and latency constraints;
   - model choice is based on empirical task performance or a calibrated routing policy, not model price alone.

7. **Run the smallest discriminating experiment.**
   - affected fixture / targeted regression / bounded sample before full suite;
   - define pass/fail/stop conditions before execution.

8. **Escalate only on insufficient evidence.**
   - stronger model, broader sample, full suite, independent grader or authoritative paid source only when the lower-cost stage cannot settle the required decision.

9. **Reserve expensive/full-suite runs for release gates.**
   - exploratory loops should not consume the resource reserved for the final independent validation.

10. **Post-account and learn.**
   - planned vs actual resources;
   - evidence gained;
   - decision changed or not;
   - update estimates and routing policy.

### Serious alternative considered: always use the strongest model once

For low-volume, high-risk, human-expensive tasks, a single strong call can be cheaper in total than a long cascade. This alternative is valid when routing overhead, repeated weak-model failures, human review time, or false-negative risk dominate model price. Therefore progressive escalation is **not mandatory**. The gate should choose between direct-strong and cascade execution based on expected total cost and risk.

## 5. PRE-RUN BUDGET GATE

Any potentially material run should emit a machine-readable budget decision before execution.

Minimum fields:

```yaml
run_id:
objective:
decision_to_change:
risk_class:
required_quality_floor:
method:
provider:
model_or_tool:
resource_estimate:
  model_calls:
  input_tokens:
  output_tokens:
  api_credits:
  compute_minutes:
  ci_minutes:
  storage_gb_hours:
  network_gb:
  human_minutes:
quota_state:
  source:
  checked_at:
  remaining:
  reserved_for_critical_work:
pricing_state:
  source:
  checked_at:
  account_or_plan_scope:
alternatives_considered:
expected_information_gain:
stop_condition:
max_run_budget:
midrun_exhaustion_plan:
decision: ALLOW | DOWNGRADE | TARGET | DEFER | BLOCK
reason:
```

### Gate rules

A run is BLOCKED or narrowed when:
- it cannot state what new evidence it may produce;
- equivalent deterministic/fresh evidence already exists;
- estimated consumption violates a hard budget or protected reserve;
- the workflow cannot fail safely if quota ends mid-run;
- the chosen cheaper provider violates privacy/security/evidence requirements;
- the pricing/quota assumption is stale and materially affects the decision.

A release-critical run may override a normal cost preference, but the override must be explicit and logged.

### Budget reservation

A hidden professional gap is the need for **critical-path reserve**. Do not treat all remaining quota as spendable. Maintain a protected reserve for final validation, rollback verification, incident response, or other mandatory gates.

Conceptually:

`spendable_now = remaining_quota - protected_reserve - expected_failure_recovery`

The protected reserve is workload-specific and may be zero for non-critical exploratory work.

## 6. POST-RUN ACCOUNTING

Every material run should record:

```yaml
planned_resources:
actual_resources:
evidence_produced:
new_information:
decision_before:
decision_after:
reusable_artifacts:
cacheable_evidence:
variance_from_plan:
waste_signal:
followup_required:
```

### Waste / low-information detection

Flag a run when one or more are true:
- high spend with no decision-relevant evidence;
- repeated run on unchanged candidate without a new hypothesis;
- full-suite execution when only one affected gate changed;
- expensive LLM grader reproduces a deterministic predicate;
- repeated failures caused by the same known infrastructure problem;
- duplicated retrieval of unchanged authoritative evidence;
- retry storm or repeated 429/5xx calls without backoff or circuit breaking.

Useful unit metrics:
- cost per validated gate;
- calls/tokens per accepted evidence item;
- human minutes per resolved failure;
- full-suite runs per release candidate;
- percentage of expensive runs that changed the decision;
- percentage of LLM grading replaceable by deterministic checks;
- quota reserve remaining at release gate;
- cache/evidence reuse rate;
- cost regression against baseline for the same eval surface.

## 7. Deterministic code vs LLM rules

Prefer deterministic execution when the truth condition is mechanically inspectable:
- exact file/state existence;
- schema validity;
- side effects;
- candidate SHA/version binding;
- count/threshold arithmetic;
- duplicate detection;
- policy/routing invariants;
- source freshness timestamps;
- test pass/fail;
- CI status;
- budget arithmetic.

Use LLM judgment when the criterion is irreducibly semantic, contextual, adversarial, or professional-judgment based.

Hybrid pattern:
1. deterministic pre-filter;
2. LLM only on ambiguous residues;
3. deterministic post-check of inspectable claims.

This is not only cheaper; it reduces grader variance and false narrative PASSes.

## 8. Model routing

Routing should optimize a constrained objective, e.g.:

`min expected total resource cost`

subject to:
- `P(quality >= floor) >= target`;
- security/privacy policy;
- latency SLO;
- provider/tool availability;
- evidence-authority requirements.

Research support:
- RouteLLM (ICLR 2025) shows learned routing can reduce costs while maintaining strong-model quality in tested settings.
- BEST-Route (ICML 2025) shows that model choice and test-time compute/sample count can be optimized jointly.
- Google ICLR 2024 cascade work shows naive generative confidence rules are unreliable; routing needs calibrated/task-aware deferral.

Therefore v1.2 should **not** encode `small model first` as a universal rule. It should encode `cheapest empirically sufficient eligible route`.

## 9. Caching and evidence reuse

Separate four concepts:

1. **Provider prompt cache** — reuses model prefix computation.
2. **Application result cache** — reuses a prior tool/model result.
3. **Evidence cache** — reuses a verified source claim with provenance/freshness.
4. **Eval artifact reuse** — reuses test evidence tied to an unchanged candidate and compatible gate.

Each needs different invalidation rules.

### Cache eligibility
- source/candidate identity unchanged;
- data is not past freshness TTL;
- scope of prior evidence matches current question;
- provider retention/privacy policy is acceptable;
- cache use does not hide required independent revalidation.

Pricing research confirms prompt caching can materially reduce input cost/latency, but provider semantics differ and may interact with data retention. Therefore caching policy must include security/privacy eligibility, not just hit-rate optimization.

## 10. Batching

Batch when:
- jobs are independent;
- latency is flexible;
- provider offers an economically meaningful batch mode;
- per-item IDs and results remain traceable;
- partial failures can be isolated;
- a late batch result does not block a critical deadline.

Do not batch merely to reduce price when:
- immediate feedback is required for an adaptive experiment;
- the next call depends on the prior result;
- observability/attribution would be degraded;
- one bad item can poison or delay the whole decision flow.

## 11. Experiment and sample-size discipline

The correct question is not `how many trials can we afford?` but `what minimum evidence is necessary to support the decision with the predeclared uncertainty tolerance?`

Rules:
- pre-register critical threshold and minimum trials for release claims;
- use targeted affected tests during repair loops;
- do not repeatedly peek at a noisy result and stop opportunistically unless the statistical procedure supports sequential stopping;
- for expensive repeated trials, use valid sequential/early-stopping methods where appropriate;
- use full suites only at predefined release boundaries or when broad regressions are plausible.

Adaptive Learn-then-Test (ICML 2025) is evidence that sequential early termination can preserve statistical validity while reducing testing rounds in costly evaluation settings. It supports the principle, not a requirement to implement that exact method in v1.2.

## 12. Pricing / free-tier / allowance freshness policy

Pricing, quotas, free tiers, billing units, promotional credits, model multipliers, usage caps and plan limits are **volatile knowledge**.

Required policy:

1. Never rely on model memory for a material exact price/limit.
2. Prefer official provider pricing/billing/limits pages or account APIs/dashboard state.
3. Record `checked_at` and source.
4. Distinguish:
   - subscription fee;
   - included allowance;
   - API pay-as-you-go billing;
   - promotional/free credits;
   - plan-specific feature access;
   - account-specific quota;
   - organization/workspace/project pool;
   - regional/data-residency surcharge or limitation.
5. Treat account dashboard/API state as stronger than generic public pricing for account-specific allowance.
6. If exact account allowance cannot be verified, use ranges or `unknown`; do not fabricate precision.
7. Re-check before a material purchase, provider migration, or budget gate whose result depends on the number.

### Evidence from current providers

- OpenAI publishes model-specific token prices and discounted cached-input rates; its Usage API exposes request/token usage and a Costs endpoint for spend reconciliation.
- Anthropic exposes spend limits, RPM/ITPM/OTPM, cache-aware rate behavior and programmatic Rate Limits APIs; its Message Batches API uses different economics from synchronous requests.
- GitHub Copilot billing changed materially in 2026: usage-based AI credits now coexist with a legacy request-based regime for some annual subscribers. This is direct evidence that billing logic must be version/plan/account aware.
- Google Vertex AI pricing varies by model, modality, context length, batch/flex mode and caching; quota may use dynamic shared capacity or provisioned throughput.
- Vercel exposes usage/spend management and hard-limit-style actions for eligible plans; resource billing is split across requests, transfer, compute/build metrics, etc.
- GitHub Actions has distinct meters for hosted-runner time and storage, with plan allowances and different runner costs.

## 13. Human-time cost

Human time must be first-class because the cheapest API path can be globally expensive if it produces review loops, debugging, manual reconciliation or unreliable evidence.

Estimate when material:

`total_expected_cost = machine/API spend + expected human time cost + expected failure/rework cost + delay/opportunity cost`

Exact monetary valuation of human time is optional. Even without salary data, track `human_minutes` as a separate scarce resource and avoid pretending it is free.

## 14. Security / privacy / authority guardrail

Cost optimization is subordinate to eligibility.

A cheaper provider/tool/source must be rejected when it materially worsens:
- confidentiality or retention guarantees;
- data residency requirements;
- permissions / blast radius;
- legal/compliance constraints;
- source authority;
- independent-review requirements;
- reliability/SLO needed by the task.

This directly addresses the failure mode `free provider -> privacy regression` and `cheap source -> non-authoritative evidence`.

## 15. Cost regression control

Treat cost as a regression dimension alongside quality and latency.

For stable eval surfaces, retain baselines:
- calls per fixture;
- tokens per fixture;
- grader calls;
- CI minutes;
- artifact storage;
- wall time;
- pass rate / decision quality.

Alert on material deviations, but do not auto-reject higher cost if quality/risk changed legitimately. A regression is unexplained deterioration in resource efficiency, not simply higher spend.

## 16. Graceful degradation / mid-run exhaustion

Before execution, define what happens if quota ends halfway:
- preserve completed evidence atomically;
- do not infer PASS from partial suite;
- mark unavailable gates explicitly;
- retry only when resource is restored and evidence remains valid;
- prefer resuming missing cases over rerunning valid completed cases;
- reserve critical quota so the release gate is not starved by exploration;
- use fallback provider/model only if it is an eligible comparator and does not invalidate preregistered evaluation conditions.

## 17. Today’s behavioral-validation incident

Incident: repeated Copilot model trials consumed the available monthly quota before a fresh final B1 revalidation could be completed.

### Controls that would have prevented or reduced the incident

1. **Quota inventory before behavioral phase.**
   Record actual account/plan regime, remaining quota/credits and reset semantics.

2. **Protected release reserve.**
   Reserve enough capacity for one fresh B1 affected regression plus the final required release suite before exploratory reruns begin.

3. **Hypothesis-bound reruns.**
   Every rerun states what changed and what failure hypothesis it tests. `same candidate + same fixture + no new hypothesis` is blocked.

4. **Deterministic-first harness validation.**
   Candidate SHA, persistence state, side effects, protocol structure, fixture schema, nested grading and infrastructure contracts should be proven mechanically before spending candidate-model quota.

5. **Affected-test loop.**
   After a B1 repair, run the minimum B1 regression first. Do not rerun B1–B10 until B1 passes the pre-registered affected threshold.

6. **Full-suite release budget gate.**
   Full B1–B10 repeated suite is allowed only after deterministic gates and affected behavioral regression pass.

7. **Post-run accounting.**
   Record quota consumed per fixture/trial and whether each run changed the diagnosis. Repeated low-information runs trigger a circuit breaker.

8. **Mid-run exhaustion plan.**
   Partial evidence must remain REVISE/INCOMPLETE; no old successful run may substitute for the required fresh revalidation.

### Necessary vs avoidable calls

Necessary:
- real candidate calls for behavior that cannot be observed deterministically;
- repeated trials required by pre-registered behavioral thresholds;
- fresh affected revalidation after root-cause repair;
- final independent release suite once prerequisites pass.

Potentially avoidable or deferrable:
- model calls used to discover mechanical harness/state defects;
- full-suite reruns before the known affected critical gate passes;
- repeated unchanged trials without a distinct hypothesis;
- LLM grading of conditions that mechanical state checks can prove exactly.

The incident is therefore not evidence that behavioral evals are too expensive. It is evidence that **eval capacity itself requires budget architecture**.

## 18. Failure modes and mitigations

### False economy harms reliability
Mitigation: hard quality/risk floor; savings are invalid if the required outcome is not met.

### Cheap model misses a critical failure
Mitigation: risk-aware routing; high-risk cases may route directly to strong/independent evaluation.

### Stale cache/evidence reuse
Mitigation: provenance + candidate binding + TTL/freshness policy + explicit invalidation.

### Free provider weakens privacy/security
Mitigation: provider eligibility gate precedes price comparison.

### Batch destroys observability
Mitigation: per-item IDs, independent results, failure attribution; reject batching where adaptive feedback is required.

### Cost optimization increases latency
Mitigation: latency SLO included as a constraint, not an afterthought.

### Cheap non-authoritative source replaces primary evidence
Mitigation: authority requirement is a hard eligibility constraint.

### Quota exhausted during critical workflow
Mitigation: protected reserve, live quota telemetry, per-run max budget, circuit breaker.

### Pricing knowledge becomes stale
Mitigation: live official verification with timestamps; account-specific state when available.

### Benchmark-price optimization damages real work
Mitigation: optimize unit economics on representative production/eval workloads, not headline $/token alone.

### Router itself becomes costly/fragile
Mitigation: start with simple deterministic policy; learned router only if workload volume and measured gains justify it.

### Optimization consumes more engineering time than it saves
Mitigation: maturity threshold. Do not build sophisticated routing/telemetry until spend or scarcity justifies it.

## 19. Evaluation design for Resource & Cost Engineering

The capability should not PASS because it can explain FinOps concepts. It must demonstrate behavior.

### Core eval families

1. **Deterministic-vs-LLM selection**
   - exact state question where LLM use is unnecessary;
   - must choose deterministic check.

2. **Cheap-vs-strong routing**
   - low-risk easy case;
   - high-risk subtle case where cheap route is unsafe;
   - must route differently.

3. **Quota-reserve scenario**
   - limited remaining credits with mandatory final release run;
   - must preserve reserve and reject nonessential work.

4. **Volatile pricing case**
   - stale remembered tariff conflicts with current official source;
   - must research live and timestamp it.

5. **Free-tier trap**
   - free provider has weaker privacy/retention terms;
   - must reject despite lower price.

6. **Cache staleness case**
   - cheap reusable evidence is candidate/version stale;
   - must invalidate.

7. **Batching trap**
   - batch is cheaper but the experiment is sequential/adaptive;
   - must preserve adaptive execution.

8. **Full-suite trap**
   - one critical gate changed and is still failing;
   - must run targeted regression before full suite.

9. **Information-gain test**
   - proposed expensive run cannot change the decision;
   - must block/defer it.

10. **Post-run waste detection**
    - actual usage greatly exceeds plan with negligible new evidence;
    - must flag regression/waste and change future policy.

11. **Mid-run exhaustion**
    - quota ends after partial suite;
    - must preserve evidence, mark incomplete, and not claim PASS.

12. **Human-time trade-off**
    - 500 weak free calls require hours of review vs one reliable paid call;
    - must include human time in the decision.

### Metrics
- outcome quality / critical-gate accuracy;
- total resource usage;
- cost per validated decision;
- quota reserve preservation;
- unnecessary expensive-call rate;
- false-economy rate;
- stale-evidence reuse rate;
- pricing-freshness compliance;
- cost-estimate calibration error;
- resource regression detection rate.

## 20. Expert Gap Discovery

Question: **What would a strong AI platform / FinOps / evaluation specialist notice missing that the user did not know to ask for?**

Material additions found:

1. **Critical-path capacity reservation**, not merely budget caps.
2. **Marginal information gain** as the justification for experiments.
3. **Unit economics per validated outcome**, not token price alone.
4. **Cost estimate calibration** — planned-vs-actual error should improve over time.
5. **Retry budgets / circuit breakers** for repeated provider or harness failure.
6. **Shared-cost attribution** for infrastructure used by multiple agents/evals.
7. **Provider eligibility before price optimization** for privacy/security/authority.
8. **Resume semantics** so partial valid evidence is not repeatedly repurchased.
9. **Optimization maturity threshold** to prevent overengineering a low-spend system.
10. **Router/economizer overhead accounting** — the optimization layer itself has a cost.
11. **Concurrency/throughput as quota resources**, not merely monthly spend.
12. **Cost-aware incident response** — debugging loops are a primary source of waste.

## 21. Red-team

### Senior AI platform engineer
Critique: a prose policy without enforcement hooks will be ignored. Provider usage metadata, token counts, rate-limit headers, run IDs and hard max-call controls must be machine-readable.

Correction: implement budget schemas and harness hooks, not only methodology text.

### FinOps practitioner
Critique: token counts alone are not financial accountability; allocation and business/value units are missing.

Correction: attribute resource use to agent/eval/gate and track cost per validated outcome.

### Evaluation scientist
Critique: aggressive early stopping can invalidate repeated-trial claims and induce selection bias.

Correction: use pre-registered stopping rules; where statistical claims matter, use valid sequential methods rather than ad-hoc peeking.

### SRE / operations engineer
Critique: monthly budget caps do not prevent critical-workflow starvation or retry storms.

Correction: protected reserve, retry budgets, circuit breakers, graceful degradation, resumable evidence.

### Security engineer
Critique: cheapest-provider routing can create data-retention, residency and privilege regressions.

Correction: provider security/privacy eligibility is a hard precondition.

### Infrastructure payer
Critique: savings claims can be meaningless if they exclude human review, subscriptions, CI, storage or failed experiments.

Correction: report total resource vector plus outcome value; avoid converting everything into fake dollar precision when data is unavailable.

## 22. Integration recommendation for Agent Architect v1.2

### Recommended architecture

**Embed the policy and gates directly into Agent Architect and its evaluation harness.**

Why:
- resource decisions occur at orchestration boundaries already controlled by Agent Architect;
- the eval harness knows fixture criticality, affected gates and release/full-suite semantics;
- another LLM agent would add cost, latency and another failure surface;
- deterministic budget arithmetic and provider telemetry do not require an LLM persona.

### Reusable package: justified, but narrow

A reusable package is worthwhile for:
- `ResourceBudget` schema;
- `RunEstimate` / `RunActual` records;
- provider pricing/usage adapters;
- quota snapshots;
- cache/evidence freshness metadata;
- budget gate function;
- cost-regression reports;
- eval-run attribution.

It should be a library/tooling layer, not an autonomous “economist agent”.

### Minimal v1.2 changes worth making

1. Add Resource & Cost Engineering methodology.
2. Add PRE-RUN BUDGET GATE to expensive behavioral/research actions.
3. Add POST-RUN ACCOUNTING to eval/research runs.
4. Add targeted-regression-before-full-suite release routing.
5. Add protected critical-run reserve concept.
6. Add volatile pricing/quota source policy.
7. Add provider eligibility/security constraint.
8. Add resource telemetry fields to behavioral harness artifacts.
9. Add cost/resource regression eval cases.
10. Add deterministic-first grader/tool preference where truth is mechanically observable.

### Overengineering to avoid in v1.2

Do **not** initially build:
- a learned model router;
- a multi-agent FinOps team;
- real-time cross-provider arbitrage;
- a full FOCUS-compatible billing warehouse;
- autonomous subscription purchasing;
- complex monetary valuation of every human minute;
- predictive capacity models without enough historical data;
- automatic provider migration based only on list price.

Start with observable accounting + deterministic gates + targeted escalation. Add sophistication only when measured workloads justify it.

## 23. Source register

Primary / authoritative sources checked on 2026-08-14:

- FinOps Foundation — FinOps Framework, Principles, FinOps for AI.
- OpenAI — API Pricing; Usage/Costs API; Batch API; data controls / caching-related retention semantics; rate-limit guidance.
- Anthropic — Claude Platform pricing; Message Batches; rate limits; Rate Limits API.
- GitHub — Copilot billing, models/pricing, AI-credit and legacy request-based billing docs; GitHub Actions billing/usage/storage docs.
- Google Cloud — Vertex AI Generative AI pricing, throughput quota, context caching and security controls.
- Vercel — pricing, usage optimization and Spend Management documentation.

Research literature:

- Ong et al., **RouteLLM: Learning to Route LLMs from Preference Data**, ICLR 2025.
- Gupta et al., **Language Model Cascades: Token-Level Uncertainty And Beyond**, ICLR 2024.
- Ding et al., **BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute**, ICML 2025.
- Hu et al., **RouterBench: A Benchmark for Multi-LLM Routing System**, ICML Workshop 2024.
- Zecchin et al., **Adaptive Learn-then-Test: Statistically Valid and Efficient Hyperparameter Selection**, ICML 2025.

## 24. Final design decision

Resource & Cost Engineering should be treated as a **cross-cutting execution discipline** of Agent Architect, not as a separate professional agent.

The governing rule is:

> Spend the least total constrained resource that can still produce the required trustworthy evidence or outcome, while preserving capacity for the critical path.

That rule is enforced through observable telemetry, pre-run budget gating, targeted experimentation, calibrated escalation, protected reserves, live pricing/quota verification, post-run accounting and regression tests — not through generic reminders to “save tokens”.
