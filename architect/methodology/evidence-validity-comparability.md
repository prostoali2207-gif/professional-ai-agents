# Evidence Validity, Comparability, and Research Architecture

Status: v0.2 — research evidence control plane integrated with Resource & Cost Engineering.

## Purpose

Prevent two coupled classes of professional-agent failure:

1. evidence is authoritative/current/retrieved correctly but does not support the decision because observations are not comparable; and
2. research activity looks thorough but has no explicit claim contract, authority boundary, provenance/lifecycle model, cost/quota control, or stopping rule.

Source quality is necessary but not sufficient. Professional evidence synthesis requires a trusted research contract, routed retrieval, validity/comparability checks, claim-level verification, and explicit stopping before a material research conclusion is accepted.

## 1. Research contract — trusted control plane

Before material external research, create a typed logical `ResearchContract`. It must bind, as relevant:

- decision/question to support;
- atomic material claims;
- claim class and stakes;
- jurisdiction, population, language, product/version and time constraints;
- freshness and lifecycle requirements;
- required/preferred source classes;
- minimum evidence strength;
- confidentiality/data-handling constraints;
- unresolved evidence gaps;
- latency/cost/resource budget;
- provider/account quota state when material;
- protected reserve for release/recovery work;
- retry budget and failure taxonomy;
- stopping and escalation conditions.

Retrieved text, snippets, provider summaries, MCP/tool metadata, or documents are untrusted evidence inputs. They cannot lower stakes, rewrite the contract, enlarge tool authority, or change the budget/stop policy.

## 2. Claim decomposition and query-budget discipline

Decompose the decision into atomic material claims before retrieval, but do not mechanically buy one search per claim.

Classify each subclaim as one of:

- `MUST_RESEARCH` — external evidence is required;
- `SHARED_RETRIEVAL` — can be answered from a retrieval route shared with related claims;
- `DERIVED_AFTER_RETRIEVAL` — can be computed or inferred after authoritative inputs are obtained;
- `CLARIFY_FIRST` — required scope is unresolved;
- `NO_EXTERNAL_QUERY` — deterministic/local evidence is sufficient.

Each external query should have a reason, expected source class, and unresolved evidence gap it targets. Paraphrase spam and provider fan-out without a decision-relevant gap are failures.

## 3. Provider-agnostic discovery routing

Use a routed evidence pipeline, not one universal research provider:

`ResearchContract -> Decomposition -> Discovery Router -> Candidate Triage -> Primary Retrieval -> Identifier/Scholarly Verification -> Evidence Normalization -> Lineage/Dependence -> Conflict/Comparability -> Synthesis -> Claim/Citation Verification -> Evidence Ledger -> Stop/Escalate`

No search provider, deep-research provider, model, MCP server, or synthesis service may certify its own evidence authority.

Route by claim requirements and current empirical evidence. Provider assignments are adapters, not architectural truth. Until a sufficiently large frozen retrieval benchmark justifies hard defaults, keep provider preferences provisional and route-specific.

Examples of valid route logic:

- known official URL -> controlled direct inspection first;
- authority-sensitive/current discovery -> best currently validated discovery adapter;
- long document/PDF extraction -> best currently validated extraction adapter;
- DOI/bibliographic identity/retraction -> identifier registry plus publisher/venue verification;
- scholarly discovery -> graph/discovery adapter, not final content authority;
- conflict, weak authority, low recall, lifecycle ambiguity, or provider failure -> second route only when expected decision value justifies it.

Do not ensemble every provider on ordinary low-stakes work.

## 4. Resource & Cost Engineering coupling

Research routing and Resource & Cost Engineering are one decision system, not parallel checklists.

Before a materially expensive or quota-sensitive research action, apply `resource-cost-engineering.md`. The router must treat these as first-class inputs:

- eligible provider/source classes after authority/privacy/reliability constraints;
- expected calls/tokens/API credits/compute/CI/human time where material;
- known provider health, rate limit and quota state;
- protected release/recovery reserve;
- retry budget;
- expected information gain;
- concrete evidence gap;
- stop condition and mid-run exhaustion behavior.

Choose the cheapest **sufficient eligible** route, not the cheapest route in isolation. A free or low-cost source cannot replace required authoritative evidence. A quota boundary cannot promote an unresolved high-stakes claim to `SUPPORTED`.

If exact price, allowance, plan limit, API credit, or quota materially affects routing, verify it live from official/account-specific evidence and record freshness. Unknown state remains `UNKNOWN`.

## 5. Candidate triage and access-state honesty

Every candidate source receives explicit metadata sufficient to judge authority and inspectability:

- source class and authority basis;
- canonical identity;
- apparent lifecycle state;
- access state;
- language/jurisdiction/population;
- provider and rank;
- likely relevance;
- security flags.

Access states are first-class:

`FULL`, `PARTIAL`, `METADATA_ONLY`, `SNIPPET_ONLY`, `INACCESSIBLE`.

SERP snippets and provider-generated summaries are discovery evidence only. Never claim that a primary source was inspected when only metadata, snippets, an abstract, or an inaccessible reference was available.

## 6. Evidence-generating-process map

For every material empirical claim, identify where the evidence came from and what process generated it.

Record as relevant:

- target construct or decision variable;
- population / market / system represented;
- sampling or selection mechanism;
- inclusion and exclusion criteria;
- measurement method;
- unit and denominator;
- time period;
- geography / jurisdiction;
- product, subject, cohort, version, or condition;
- transformations, weighting, normalization, or filtering;
- missingness / nonresponse / censoring;
- known biases and uncertainty.

The agent must not infer comparability from similar labels alone.

## 7. Provenance, lifecycle, lineage, and dependence

Normalize source identity before counting evidence.

Track relationships such as:

- draft -> final;
- preprint -> accepted -> version of record;
- correction -> corrected version;
- withdrawn/retracted -> replacement/current;
- superseded -> current authority;
- press release -> downstream reporting;
- mirror/syndication -> canonical source.

A retracted/withdrawn/superseded upstream item can invalidate dependent descendants for the affected claim. Multiple URLs do not equal multiple independent sources.

Track source lineage separately from methodological/common-cause dependence. Relevant common causes can include shared dataset, benchmark, measurement pipeline, population/time window, annotators, synthetic-data model, or vendor telemetry. Unknown dependence remains `UNKNOWN`; do not invent pseudo-probabilities.

## 8. Comparability gate

Before combining, ranking, averaging, benchmarking, or using one observation as a comparator for another, test whether they are sufficiently comparable for the decision.

Ask:

1. Same construct? Are both observations measuring the thing the decision actually requires?
2. Same population or defensible transport? If populations differ, what supports generalization?
3. Same state/condition? Examples: new vs used, retail vs wholesale, export-only vs local-market, production vs preview, observed transaction vs asking price.
4. Same unit and denominator? Gross vs net, per-user vs per-session, nominal vs real, inclusive vs exclusive of taxes/fees.
5. Same temporal regime? Has market, policy, product version, or environment changed materially?
6. Same measurement method? Could instrument, wording, collection mode, logging, or methodology produce systematic differences?
7. Same inclusion criteria? Are hidden exclusions creating selection bias?
8. Same quality threshold? Are duplicates, outliers, low-confidence records, or synthetic observations contaminating one side?
9. Same lifecycle state? Is one source obsolete, corrected, retracted, or superseded?
10. Independent enough for the inference? Are apparently separate records actually syndicated or methodologically coupled?

If comparability is partial, preserve the distinction instead of forcing a single estimate.

## 9. Construct validity

A convenient metric is not automatically the decision variable.

Examples:

- listing price is not completed-sale price;
- click-through rate is not customer value;
- test pass rate is not production reliability;
- model preference score is not professional competency;
- response rate alone is not survey validity.

For every proxy, document:

`target construct -> proxy -> causal/empirical justification -> known gaps -> conditions where proxy breaks`.

## 10. Selection, coverage, measurement, and classification risk

Evidence can be numerically precise while systematically unrepresentative.

Check who/what could enter the dataset, who/what could not, why observations are missing, whether inclusion probability differs in decision-relevant ways, and whether data availability itself is correlated with the outcome. Do not use sample size as a substitute for representativeness.

Create explicit classification boundaries for categories that materially affect inference. Ambiguous records should be marked uncertain, excluded, or sensitivity-tested rather than silently assigned.

## 11. Conflict and aggregation discipline

Before synthesis or aggregation determine whether evidence is actually contradictory or merely different in scope, lifecycle, construct, population, metric, or method.

Use categorical claim states such as:

- `SUPPORTED`;
- `PARTIAL`;
- `CONFLICTED`;
- `CONTRADICTED`;
- `UNVERIFIED`;
- `NOT_COMPARABLE`.

Preferred sequence:

`classify -> validate -> normalize identity/lifecycle -> segment -> compare within segment -> assess dependence -> quantify/describe uncertainty -> synthesize only where justified`.

Never majority-vote syndicated descendants, shared-dataset pseudo-replications, different metrics, or populations that do not support the requested generalization. Do not manufacture numeric confidence without a calibrated probabilistic model.

## 12. Synthesis and claim/citation verification

Machine-consumed synthesis should use schema-enforced structured output where supported. Synthesis consumes normalized evidence plus unresolved gaps, not arbitrary raw web content where avoidable.

For every material claim verify the tuple:

`claim text + polarity/status + citation(s) + evidence location + lifecycle/access state`.

Verification outcomes may include:

`SUPPORTS`, `PARTIAL_SUPPORT`, `CONTRADICTS`, `IRRELEVANT`, `INACCESSIBLE`, `LIFECYCLE_INVALID`.

A real citation that does not entail the claim is a failed citation. Critical claims fail closed when required evidence cannot be reopened or verified.

## 13. Failure taxonomy, retries, provider health

Do not collapse all non-success into `retry`.

Distinguish at least:

- behavioral/evidence failure;
- `AUTH_CONFIG`;
- `RATE_LIMIT_SHORT`;
- `DAILY_QUOTA_EXHAUSTED`;
- `CAPACITY_TRANSIENT` / 503;
- `PROVIDER_OUTAGE`;
- `MODEL_LIFECYCLE` / retired endpoint.

Failure class determines retry eligibility; a generic retry budget is not permission to retry every failure.

- Behavioral/evidence failure -> repair the responsible evidence/architecture layer; do not retry unchanged behavior hoping for a different answer.
- `AUTH_CONFIG` -> repair credentials/configuration first; do not retry the same invalid request.
- `DAILY_QUOTA_EXHAUSTED` -> **do not retry the same quota-bound route while the quota state/window is unchanged**. Resume only after directly observed quota reset/state change, or route to another sufficient eligible source/provider. If the authoritative primary URL is already known and direct inspection is eligible, use that direct route instead of retrying or ensembling the exhausted discovery provider.
- `MODEL_LIFECYCLE` -> verify current model/endpoint state and migrate; do not retry a retired route unchanged.
- `RATE_LIMIT_SHORT`, `CAPACITY_TRANSIENT`, or `PROVIDER_OUTAGE` -> bounded retry/backoff/fallback is allowed only when the concrete evidence gap remains, current budget/quota reserve permits it, and there is a reason to expect conditions to change.

Repeated retries against unchanged failure conditions are resource-control failures. Operational fallback must preserve authority, privacy, reliability, comparability/independence requirements, and the original evidence threshold.

## 14. Research stopping

Continue research only when the next action targets a concrete unresolved evidence gap and has sufficient expected decision value under the remaining budget/reserve.

Allowed stopping decisions:

- `STOP` — material thresholds met;
- `CONTINUE` — a concrete gap remains and the next route is justified;
- `CLARIFY_FIRST` — scope prevents valid evidence acquisition;
- `STOP_WITH_LIMITATION` — remaining uncertainty is non-critical or budget-bound and explicitly disclosed;
- `ESCALATE_OR_DEFER` — unresolved high-stakes claim cannot be responsibly closed within current authority/resources.

Stop when all material claims meet their evidence thresholds and additional searches have low expected novel value. Budget exhaustion never converts incomplete required gates into PASS.

## 15. Evidence ledger and observability

For material research persist enough state to audit and resume without repurchasing valid evidence:

- research contract and decomposition;
- queries, provider/tool/model/version and raw result ranks;
- opened/rejected sources and reasons;
- access state, lifecycle, provenance and retrieval time;
- evidence-generating-process metadata;
- lineage and methodological dependence;
- conflicts/comparability decisions;
- transformations/calculations;
- synthesis and claim/citation verification;
- negative/failed authority searches when decision-relevant;
- security events;
- planned/actual calls, tokens, API credits, quota, CI/compute, latency and human time;
- retry/fallback events;
- stopping reason and unresolved gaps.

Reuse requires scope/version/freshness/provenance compatibility. Timestamp freshness alone is insufficient.

## 16. Security and trust boundary

Research is read-only by default. Broad web research receives no unrelated secrets. Retrieved documents and MCP/tool metadata are untrusted data. Write/action tools belong to a separate authorization plane.

Production network retrieval additionally requires controlled egress, redirect re-authorization, private/link-local blocking and DNS-rebinding-safe connection handling. Policy-level URL checks alone do not prove transport isolation.

## 17. Evaluation requirements

Analytical/research capabilities must be tested on adversarial evidence sets containing:

- authoritative but non-comparable sources;
- mixed populations/product states;
- duplicate/syndicated records;
- stale/superseded/withdrawn/retracted observations;
- proxy/construct mismatch;
- inconsistent units/denominators;
- sample-selection bias;
- mislabeled categories;
- large but biased samples;
- sparse but high-quality evidence;
- inaccessible primary sources;
- provider-generated unsupported citations;
- prompt-injection text in authoritative content;
- quota exhaustion, rate limits, 503 capacity and provider outage;
- pressure to keep searching after evidence sufficiency;
- pressure to declare support when budget ends mid-gate.

Mechanically inspectable rules belong in deterministic tests. Semantic professional judgment requires frozen adversarial cases and construct-appropriate independent grading. Narrative self-assessment is not behavioral evidence.

The deterministic policy/eval surface for this capability is `../evaluation/research_evidence_engineering/`.

## 18. Agent Architect integration

When modeling any profession that consumes external or empirical evidence, the Architect must determine whether research/evidence validity is CORE, BOUNDARY-CRITICAL, ESCALATION, CONTEXTUAL, or OUT-OF-SCOPE.

The knowledge architecture is incomplete if it teaches source authority and retrieval without teaching claim decomposition, evidence authority boundaries, lifecycle/lineage, comparability, budget/quota-aware routing, citation entailment, and stopping.

For material research, pair this file with:

- `source-knowledge-engineering.md` for source authority and knowledge placement;
- `resource-cost-engineering.md` for eligibility, budgets, quotas, protected reserve, retries, pricing freshness, and post-run accounting;
- `agent-security-and-trust.md` when untrusted content/tools are involved;
- `uncertainty-escalation.md` for unresolved high-stakes evidence.

## Evidence basis and implementation boundary

This layer incorporates the completed August 2026 Research Architecture benchmark and its validated controls: claim/stakes routing, decomposition/query-budget control, access-state honesty, source lifecycle/lineage, methodological dependence, comparability, claim-aware aggregation, citation verification, security boundaries, failure-specific retry policy, and evidence-gap stopping.

Route-specific provider observations remain provisional. The existing benchmark does **not** justify hard-coded universal provider rankings; a larger frozen judged retrieval corpus remains the gate for hard defaults.

This capability does not claim calibrated quantitative dependence scores, full production network isolation, or domain-specific legal/medical/safety evidence profiles. Those require separate evidence and gates.
