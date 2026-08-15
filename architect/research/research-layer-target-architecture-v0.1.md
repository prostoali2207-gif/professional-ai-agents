# Research Layer Target Architecture v0.1

Status: research/design artifact only. Does not modify `architect/SKILL.md`, Agent Architect v1.1 behavior, or PR #1.

## Decision

Use a **provider-agnostic routed evidence pipeline**, not one universal research provider.

Target flow:

`ResearchContract -> Decomposition -> Discovery Router -> Candidate Triage -> Primary Retrieval -> Scholarly/Identifier Verification -> Evidence Normalization -> Lineage/Conflict/Comparability -> Synthesis -> Claim/Citation Verification -> Evidence Ledger`

A provider may be default for a route only after route-specific empirical evidence. No provider owns the authority boundary.

## Why this architecture is stronger than one-provider research

A universal provider creates correlated failure across discovery, extraction, synthesis, citation generation, pricing, availability, security, and lifecycle changes. The empirical pilot already shows complementary strengths: Exa was stronger on authority-sensitive/current-source and cross-lingual discovery; Tavily was stronger on long PDF extraction. Direct primary inspection and bibliographic registries solve different problems again. Therefore provider specialization is not accidental complexity; it is evidence-backed separation of concerns.

## Layer 0 — Research contract

Every research job starts with a typed contract:

- decision/question to support;
- material claims that require evidence;
- stakes/risk class;
- freshness requirement;
- jurisdiction/version/population constraints;
- source classes allowed/preferred;
- minimum evidence strength;
- confidentiality/data handling constraints;
- latency/cost budget;
- stopping and escalation criteria.

The contract is the control plane. Retrieved content can never rewrite it.

## Layer 1 — Decomposition

Generate evidence-seeking subqueries across distinct purposes, not paraphrase spam:

- terminology/profession map;
- official/primary authority;
- empirical evidence;
- counterevidence;
- lifecycle/current-version checks;
- practitioner/tacit knowledge;
- failure/incident evidence;
- scholarly citation-chain expansion.

Each query carries a reason and expected source class.

## Layer 2 — Discovery router

The router selects the cheapest plausible route that meets the contract.

### Default candidate routing based on current evidence

- **Authority-sensitive/current web discovery:** Exa candidate default.
- **Long-document/PDF extraction:** Tavily candidate default/fallback.
- **Known official URL:** direct browser/HTTP inspection first.
- **Scholarly discovery:** Semantic Scholar/OpenAlex-style graph adapters as discovery only.
- **DOI/bibliographic identity:** Crossref/publisher/identifier authority.
- **Exploratory deep research:** optional adapter only; output treated as candidate synthesis, never final evidence.

These are provisional route defaults, not universal winners.

### Escalation

Escalate to a second discovery mode when any of the following holds:

- high-stakes material claim;
- weak authority in top results;
- current/supersession ambiguity;
- cross-lingual or vocabulary mismatch;
- suspected counterevidence;
- low recall / no authoritative hit;
- provider failure or quota block.

Do not ensemble every provider on trivial queries.

## Layer 3 — Candidate triage

Every candidate receives explicit metadata:

- source class;
- authority basis;
- apparent lifecycle state;
- canonical identity confidence;
- access state;
- language/jurisdiction;
- likely relevance;
- provider/rank;
- security flags.

SERP snippets and provider summaries are discovery evidence only; they cannot directly satisfy a material claim.

## Layer 4 — Primary retrieval and inspection

Access states are first-class:

`FULL -> PARTIAL -> METADATA_ONLY -> SNIPPET_ONLY -> INACCESSIBLE`

For inspected material capture:

- canonical URL/identifier;
- title/author/organization;
- publication/update/version date;
- source location/page/section;
- raw extract/observation;
- extraction mechanism;
- retrieval timestamp;
- extraction confidence/errors.

A system may never convert `METADATA_ONLY`, `SNIPPET_ONLY`, or `INACCESSIBLE` into a claim that the primary source was read.

## Layer 5 — Source identity, lineage and scholarly verification

Normalize source identity before counting evidence.

Track relationships such as:

- draft -> final;
- preprint -> accepted -> version of record;
- correction -> corrected version;
- withdrawn/retracted -> replacement/current;
- press release -> downstream reporting;
- mirror/syndication -> canonical source.

For scholarly claims, verify identifiers and bibliographic fields independently. Crossref/publisher records are identity checks, not substitutes for full-text evidence.

## Layer 6 — Evidence object model

```text
EvidenceRecord
- evidence_id
- claim_id
- source_identity_id
- source_url
- canonical_identifiers[]
- source_class
- authority_basis
- lifecycle_state
- access_state
- raw_excerpt_or_observation
- source_location
- publication_date
- update_version_date
- retrieval_timestamp
- jurisdiction_population_language
- construct_measurement_method
- extraction_method
- freshness_class
- confidence
- lineage_edges[]
- conflict_edges[]
- security_flags[]
- transformations[]
```

Derived summaries are stored separately from raw evidence.

## Layer 7 — Conflict and comparability engine

Before synthesis or aggregation, evaluate:

- same construct/claim?;
- same version/lifecycle?;
- same jurisdiction/population/language?;
- same metric/measurement?;
- same methodology/protocol?;
- independent evidence or correlated upstream source?;
- actual contradiction or merely different scope?;

Possible result states:

`SUPPORTED`, `PARTIAL`, `CONFLICTED`, `UNVERIFIED`, `NOT_COMPARABLE`.

Never majority-vote across non-independent or non-comparable sources.

## Layer 8 — Synthesis

The synthesis model consumes normalized evidence plus unresolved gaps, not raw arbitrary web pages where avoidable.

Required behaviors empirically validated in the frozen smoke:

- abstain on inaccessible-primary claims;
- preserve material scope conflicts;
- reject unsupported global extrapolation;
- treat retrieved instructions as untrusted data;
- refuse rankings based on incomparable metrics.

Use schema-enforced structured output for machine-consumed synthesis. The pilot found plain JSON prompting can still produce malformed structured output even when semantics are correct.

## Layer 9 — Claim/citation verifier

For every material claim, verify the tuple:

`claim text + claim status + citation(s) + evidence location`

This is critical. The pilot exposed a grader failure when claim text was evaluated without its status: a hypothesis explicitly marked `CONFLICTED` or `UNVERIFIED` was falsely treated as an affirmative claim.

Verification outcomes:

- `SUPPORTS`;
- `PARTIAL_SUPPORT`;
- `CONTRADICTS`;
- `IRRELEVANT`;
- `INACCESSIBLE`;
- `LIFECYCLE_INVALID`.

Critical claims fail closed when they cannot be reopened or verified.

## Layer 10 — Evidence ledger / observability

Persist enough state to reproduce and audit:

- research contract;
- decomposition/subqueries;
- provider/tool/model/version;
- query/result ranks;
- opened/rejected sources and reasons;
- source lineage;
- access/extraction failures;
- normalized evidence;
- conflicts/comparability decisions;
- synthesis output;
- citation verification;
- security events;
- latency/tokens/API credits/CI cost;
- quota/capacity/lifecycle failures.

## Failure taxonomy and retry policy

Do not collapse all non-success into `retry`.

### Behavioral/evidence failures

- fabricated source/DOI;
- false primary inspection claim;
- unsupported citation entailment;
- lifecycle-invalid authority;
- loss of material qualifier;
- false conflict resolution;
- incomparable aggregation;
- prompt-injection effect.

These require architecture/prompt/grader repair, not blind retry.

### Provider operational failures

- `CAPACITY_TRANSIENT` (for example HTTP 503 high demand): one bounded retry if budget allows;
- `RATE_LIMIT_SHORT` (retry-after seconds/minutes): delay only when useful;
- `DAILY_QUOTA_EXHAUSTED`: stop, do not rotate keys merely to bypass budget policy;
- `AUTH_CONFIG`: fix credentials/configuration;
- `MODEL_LIFECYCLE`: migrate adapter/model, do not retry obsolete endpoint;
- `PROVIDER_OUTAGE`: route fallback if claim value justifies it.

This taxonomy is directly supported by the pilot: GitHub Models produced a lifecycle-retirement failure, Gemini produced temporary 503 capacity failure, and later a daily free-tier quota exhaustion.

## Security / trust boundaries

### Non-negotiable

1. Research plane is read-only by default.
2. Retrieved documents and MCP/tool metadata are untrusted data.
3. Broad web research receives no unrelated secrets/private context.
4. Research credentials are least-privilege and provider-specific.
5. Write/action plane is separate and requires explicit authorization.
6. Citation verification reopens evidence independently.
7. Redirects, mirrors, source replacement and embedded instructions are security-relevant events.
8. No provider-generated answer can certify its own citation correctness.

## Cost and stopping policy

Use marginal evidence value, not maximum search depth.

Stop when:

- all material claims meet their evidence threshold; and
- high-risk gaps are resolved or explicitly escalated; and
- additional searches yield low novel evidence; or
- budget boundary is reached and remaining uncertainty is disclosed.

Spend more only on claims where the expected decision value of more evidence exceeds cost/latency/risk.

## Current empirical evidence carried into this architecture

### Exa vs Tavily

Observed in controlled paired pilots:

- Exa: stronger authority-sensitive/current-source ranking and cross-lingual authoritative discovery on tested cases;
- Tavily: stronger long-PDF extraction fidelity on tested NIST document;
- both: capable of finding counterevidence in a BM25-vs-semantic retrieval case;
- Tavily advanced retry did not repair the tested draft/final authority-ranking weakness.

This evidence supports routing rather than a single provider.

### Synthesis integrity

Deterministic integrity fixtures passed 10/10. Gemini frozen synthesis smoke, after correcting grader defects and enforcing structured schema, was adjudicated PASS 5/5 with zero P0/content P1 findings on the registered set.

This proves capability on that small frozen set only; it does not establish generalized robustness. Two controlled perturbations remain required.

### Operational reliability lessons

- provider/model lifecycle must be checked live;
- schema enforcement materially improves structured-output reliability;
- graders must be status-aware and should not use naive phrase matching;
- 503 capacity failures and quota exhaustion must not be mislabeled behavioral failures;
- repeated retries can consume the entire free quota without increasing evidence quality.

## Expert-gap discovery after empirical work

A strong practitioner would additionally demand:

- source independence/provenance graph, not citation counts;
- lifecycle invalidation propagation when a source is superseded/retracted;
- negative-search logs for meaningful failed authority searches;
- benchmark contamination controls and truly hidden holdouts;
- calibration of abstention, not only answer accuracy;
- cross-language canonical-identity checks;
- robust structured-output validation before downstream execution;
- provider-health and quota state as router inputs;
- privacy/license policy for durable evidence storage;
- human escalation rules for high-stakes unresolved conflicts.

## Red-team

### Senior researcher critique

Risk: architecture becomes a search-engine orchestration system rather than a research method.

Response: contract-first claims, source lineage, comparability, stopping criteria and explicit uncertainty are mandatory; provider count is secondary.

### Information-retrieval engineer critique

Risk: tiny pilot overfits routing decisions and lacks frozen recall benchmarks.

Response: current provider defaults remain provisional; larger frozen retrieval-only benchmark is still required before hard defaulting.

### Evaluation scientist critique

Risk: grader repair after seeing outputs can silently move goalposts.

Response: distinguish genuine pre-registered criteria from discovered grader implementation bugs; preserve raw runs, change logs, hashes and deterministic re-adjudication. Future hidden perturbations must freeze graders before execution.

### Security engineer critique

Risk: an LLM that safely summarizes injection text may still be unsafe when real write-capable tools exist.

Response: current B4 validates synthesis behavior only. A separate tool-boundary security test must use sandboxed canary tools/credentials and prove zero unauthorized side effects.

### Hiring-manager / practitioner critique

Risk: architecture is elegant but too expensive/slow for daily use.

Response: route by claim risk and expected information value; direct cheap path first; multi-provider escalation only when material uncertainty remains.

## Implementation gate

Do **not** modify Agent Architect yet.

Before implementation, complete at minimum:

1. Perturbation A after free quota reset;
2. Perturbation B only after A has no P0;
3. sandboxed real-tool prompt-injection boundary test;
4. larger frozen retrieval set sufficient to justify hard provider defaults;
5. reconcile this architecture with Resource & Cost Engineering so budgets/quotas are first-class router inputs.

If those gates pass, this document can become the design basis for a future research-layer implementation proposal.