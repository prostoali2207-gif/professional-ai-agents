# Research Benchmark Harness — Expert-Gap & Red-Team Audit v0.1

Status: research-only evaluation artifact. Does not modify `architect/SKILL.md`, Agent Architect v1.1 behavioral validation, or PR #1.

## Audit question

What would a strong research engineer / information scientist / professional researcher notice is missing even though the original requester did not ask for it?

Then:

What would a senior researcher, information-retrieval engineer, evaluation scientist, and security engineer criticize about the current research benchmark architecture?

## Executive finding

The existing harness is directionally strong but was still vulnerable to four classes of false confidence:

1. search-time contamination and benchmark answer leakage;
2. conflating fixed-benchmark performance with expected deployment performance;
3. grader/reference-set error becoming invisible ground truth;
4. provider adoption based on an underpowered or post-hoc comparison.

These are material enough to change provider-selection conclusions. They must be treated as benchmark-design requirements, not reporting footnotes.

---

## 1. Expert-gap discovery

### Gap A — Search-time contamination

A web-enabled research system can search for the benchmark itself, its task wording, published gold answers, discussion pages, or derivative explanations. A provider can therefore score well without demonstrating the intended retrieval/reasoning capability.

This failure differs from ordinary model-training contamination because it occurs at inference time through live search.

Required controls:

- keep provider-selection holdouts private/non-indexed;
- avoid publishing exact gold answers before final provider selection;
- use synthetic-but-professionally-realistic frozen fixtures where appropriate;
- maintain rolling live cases whose gold is created after the tested model/provider release where feasible;
- inspect search trajectories for benchmark-title, task-string, answer-string, or repository leakage;
- mark contaminated runs invalid rather than as successful;
- separate public development cases from hidden selection cases.

Evidence basis: 2026 work on Search-Time Contamination reports that deep-research agents can retrieve benchmark metadata, question context, or explicit answers during evaluation and that this can inflate reported performance.

### Gap B — Benchmark accuracy is not generalized accuracy

A provider can win on this finite case set yet be worse on the broader population of Agent Architect research tasks.

The harness therefore needs an explicit estimand.

For every reported metric state whether it estimates:

- **fixed benchmark performance**: success on exactly these benchmark items; or
- **generalized task-family performance**: expected success over a broader task population represented by sampled items.

If making generalized claims, case families and sampling assumptions must be explicit and uncertainty must reflect item heterogeneity.

Do not report `Provider A is 7% better` without specifying which estimand the 7% belongs to.

### Gap C — Gold-set fallibility

Human-reviewed gold evidence can still be wrong, incomplete, stale, over-narrow, or biased toward the retrieval methods used to construct it.

Mitigations:

- independent second-review of P0/P1 gold labels;
- source/version/date recorded for each gold item;
- acceptable-alternative evidence list rather than one canonical URL where multiple sources are legitimately sufficient;
- adjudication log for reviewer disagreement;
- periodic revalidation of volatile/live gold;
- candidate-provider discoveries may trigger **gold review**, but never automatic retroactive provider credit without blind adjudication.

### Gap D — Pooling heterogeneous cases

One overall success rate can hide severe weaknesses. A provider strong on easy web discovery may compensate numerically for repeated scholarly-identity or authority failures.

Required reporting:

- task-family strata;
- severity strata;
- frozen vs live strata;
- language strata where relevant;
- primary-source vs scholarly vs general-web strata;
- no P0/P1 averaging-away.

### Gap E — Statistical power and stopping rules

Provider comparisons are expensive and stochastic. Without a predeclared stopping rule, evaluators can keep running until the favored provider appears ahead.

Before a paid head-to-head, predeclare:

- primary metrics by layer;
- practically meaningful effect size;
- minimum cases per core family;
- repeat count for stochastic agentic modes;
- uncertainty method;
- tie/inconclusive rule;
- maximum spend/run count;
- adoption threshold.

Do not continue sampling solely because the current result is inconvenient.

### Gap F — Failure correlation and common-mode dependence

A multi-provider architecture is not automatically independent. Two providers may share upstream indexes, cached pages, model families, or the same incorrect source ecosystem.

Measure not only marginal success but **error overlap**:

- which cases both providers miss;
- whether second-provider recall is genuinely complementary;
- whether failures share the same wrong URL/source family;
- incremental evidence recall conditional on the first provider failing.

The value of an ensemble is `new useful evidence / added cost and complexity`, not provider count.

### Gap G — Cost must be normalized by successful evidence outcome

Cheap queries that routinely need retries, fallback retrieval, manual verification, or second providers may be operationally expensive.

Report:

- raw request cost;
- cost per task;
- cost per **P0/P1-safe successful task**;
- marginal cost for incremental required-evidence recall;
- latency to first useful evidence and latency to verified evidence.

### Gap H — Observability quality itself needs a metric

A provider can produce good outcomes but expose too little trace to diagnose failures or verify methodology.

Score whether the system exposes:

- actual queries/subqueries;
- result identities and ranking;
- retrieval timestamps;
- raw/extracted document content;
- cache/live status;
- model/tool-call trace where agentic;
- usage/cost data;
- explicit errors/timeouts.

Opaque success is weaker for a professional research infrastructure than inspectable success, even if top-line quality is similar.

### Gap I — Access/licensing/privacy boundary

Raw-document acquisition can encounter copyrighted, licensed, private, authenticated, or personally sensitive material.

Benchmark and future architecture must distinguish:

- permission to retrieve;
- permission to retain/cache;
- permission to redistribute in fixtures/logs;
- provider data-retention implications;
- whether private context is unnecessarily sent to external research vendors.

Gold fixtures should prefer redistributable/public evidence or store derived minimal excerpts/labels when full redistribution is inappropriate.

### Gap J — Human factors / operator burden

A technically strong provider may impose enough configuration, debugging, quota management, manual disambiguation, or credential burden to reduce real research throughput.

Record operator interventions required for:

- query repair;
- blocked-source recovery;
- authentication;
- malformed extraction;
- citation repair;
- retry/quota recovery.

Do not hide human rescue from provider performance.

---

## 2. Red-team by practitioner perspective

### Senior researcher critique

Likely criticism:

- gold evidence may encode the benchmark author's own literature-search bias;
- case count is initially too small to support broad claims;
- citation correctness alone does not establish evidentiary sufficiency;
- contrary evidence must be actively sought, not merely accepted when encountered;
- research quality includes knowing when the available evidence is insufficient.

Repairs:

- independent gold review;
- sufficiency/completeness probes in addition to citation faithfulness;
- explicit uncertainty/escalation score;
- disconfirmation-search cases as core, not optional.

### Information-retrieval engineer critique

Likely criticism:

- end-to-end answer quality can confound retriever and synthesizer;
- provider result limits and search modes may make comparisons non-equivalent;
- lexical and semantic systems need corpus-controlled evaluation to isolate retrieval;
- one Recall@K value hides query-family variance;
- ensemble value must be measured by complementarity.

Repairs:

- frozen corpus arm;
- common downstream synthesizer when isolating retrieval;
- family-stratified retrieval metrics;
- incremental recall/error-overlap analysis;
- full query/result traces.

### Evaluation scientist critique

Likely criticism:

- benchmark item set may not represent deployment population;
- uncertainty may be miscomputed if items/runs are treated as independent when they are not;
- repeated stochastic runs and task heterogeneity need hierarchical treatment;
- benchmark selection/tuning can overfit to providers;
- no predeclared practical effect size means tiny differences can be overinterpreted.

Repairs:

- explicitly distinguish fixed benchmark vs generalized estimand;
- report raw case-level outcomes, not only means;
- use paired comparisons because providers see the same cases;
- use cluster/bootstrap or hierarchical methods where justified by sample size;
- report intervals and practical effect thresholds;
- hidden holdout + rolling live set;
- pre-registration-style run plan before paid comparison.

### Security engineer critique

Likely criticism:

- prompt-injection tests that only inspect model text are insufficient;
- real risk is privilege crossing and tool execution;
- MCP/tool-return poisoning is a runtime trust problem, not merely a prompt problem;
- a research agent sharing write-capable tools invalidates the threat model;
- logs themselves can leak secrets.

Repairs:

- run research adapters in read-only environment;
- enforce permissions outside the model;
- authorization gate before consequential tool calls;
- structured tool outputs where feasible;
- malicious MCP/tool-response cases;
- redact secrets/PII from traces;
- evaluate attempted unauthorized action separately from completed unauthorized action.

OWASP material on MCP Tool Poisoning supports this architecture: tool descriptions/returns can act as indirect prompt-injection channels, and backend least-privilege controls are required rather than prompt-only restrictions.

---

## 3. Minimum evidence threshold before spending on provider head-to-head

The free baseline is ready for a small paid experiment only when all conditions below hold.

### Harness readiness gate

Required:

- >= 1 debugged gold instance for every core family;
- >= 5 hidden/frozen instances planned for each core provider-selection family before final adoption;
- P0/P1 gold independently reviewed;
- frozen and live task separation established;
- contamination checks defined;
- raw trace schema defined;
- cost/latency capture defined;
- security execution sandbox is read-only;
- provider-specific tuning cases are excluded from final selection holdout;
- adoption rule is written before paid runs.

### Core provider-selection families

1. authority/freshness;
2. scholarly identity/DOI;
3. extraction fidelity;
4. multi-hop/vocabulary mismatch;
5. conflict/comparability;
6. security;
7. rolling live freshness.

---

## 4. Paid-provider adoption rule v0.1

A provider may be adopted as default for a specific layer only if all are true:

1. **Zero observed P0 failures** in the selection set. One P0 blocks default adoption pending root-cause repair and adversarial retest.
2. **No unresolved systematic P1 family failure.** A rare isolated P1 can trigger repair/retest; recurring P1 means the provider is not default-capable for that task family.
3. **Material baseline improvement.** It must improve at least one deployment-relevant primary metric by a predeclared practically meaningful amount, or deliver equivalent quality with materially lower cost/latency/operator burden.
4. **No hidden tradeoff.** Improvement cannot come from materially worse citation correctness, authority selection, extraction fidelity, or security.
5. **Inspectable evidence path.** Failures and source choices must be diagnosable enough for professional use.
6. **Reasonable robustness across live/frozen strata.** A win only on static/public cases is insufficient.
7. **Marginal value exceeds complexity.** For an additional provider in an ensemble, incremental evidence recall or resilience must justify integration/latency/cost.

If results are within uncertainty/practical-equivalence bounds, choose the simpler/cheaper/more observable option rather than declaring a winner.

---

## 5. Recommended first paid experiment — intentionally small

Do not immediately run the entire suite.

### Stage P0 — smoke / integrity

Per provider:

- 1 authority/freshness case;
- 1 scholarly-identity case;
- 1 extraction case;
- 1 hostile-content case;
- 1 multi-hop case.

Goal: detect catastrophic incompatibility before spending further.

### Stage P1 — paired selection pilot

Only providers passing Stage P0:

- same hidden cases across providers;
- at least 5 cases in the high-value discovery/authority family;
- repeated runs for stochastic deep-research modes;
- raw outputs frozen before grading;
- paired case-level comparison.

Purpose: estimate whether differences are large enough to justify full evaluation.

### Stage P2 — full selection benchmark

Run only if pilot shows plausible marginal value.

Expand core families, live cases, security variants, cost/latency measurement, and end-to-end Agent Architect research cases.

This staged design intentionally minimizes paid usage while preserving the ability to reject weak providers early.

---

## 6. Benchmark quality gate after red-team

The harness is sufficiently mature for a **small paid smoke/pilot**, not for a final universal provider ranking.

It is not allowed to claim a global best research provider from this benchmark. Valid conclusions are layer- and task-family-specific, for example:

- `Provider X improved current-web authoritative-source Recall@10 over baseline under these cases.`
- `Provider Y had better PDF structural extraction but worse latency.`
- `Provider Z added little incremental recall after direct web search and therefore did not justify ensemble complexity.`

The future research architecture should select providers by measured role fitness rather than brand-level rank.

## Evidence basis added in this audit

- NIST, *Towards Best Practices for Automated Benchmark Evaluations* (2026): validity, transparency, reproducibility, explicit evaluation objectives and analysis/reporting discipline.
- NIST AI 800-3, *Expanding the AI Evaluation Toolbox with Statistical Models* (2026): distinction between fixed benchmark accuracy and generalized accuracy; explicit assumptions and uncertainty.
- NIST, *Building Evaluation Probes into Agentic AI* (2026): machine-readable audit trails and separate grounding probes for citation faithfulness, completeness and sufficiency.
- Search-Time Contamination in Deep Research Agents (2026): inference-time benchmark leakage through web search can inflate evaluation results.
- LivePI (2026): production-like indirect-prompt-injection evaluation across multiple input surfaces demonstrates that text-only synthetic injection testing is insufficient for agent security claims.
- OWASP MCP Tool Poisoning / MCP Security guidance: tool descriptions and runtime tool outputs are untrusted attack surfaces; privilege isolation and backend enforcement are required.
