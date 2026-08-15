# Research Architecture Benchmark — Final Design Verdict — 2026-08-15

Status: **COMPLETE FOR RESEARCH/DESIGN RECOMMENDATION**.

This artifact does not modify Agent Architect behavior, `architect/SKILL.md`, v1.1 behavioral validation, PR #1, or branch `agent/architect-external-benchmark-2026-08`.

It is not an implementation approval for production research tooling. Remaining limitations are explicitly listed below.

---

## Executive decision

### Architecture decision

**PASS: use a provider-agnostic routed evidence pipeline. Do not use one universal research provider as the authority boundary.**

The benchmark repeatedly showed complementary strengths, provider-specific failure modes, independent verification needs and security boundaries that cannot be safely collapsed into one vendor response.

Recommended logical flow:

```text
trusted request
  -> atomic claim decomposition
  -> claim class / stakes / constraints
  -> evidence-gap + query-budget planning
  -> discovery routing
  -> candidate triage
  -> controlled retrieval / primary inspection
  -> scholarly & identifier verification
  -> provenance + lifecycle normalization
  -> source-lineage graph
  -> methodological/common-cause dependence graph
  -> conflict + comparability adjudication
  -> claim-class-aware evidence aggregation
  -> schema-enforced synthesis
  -> claim + status + citation verification
  -> evidence ledger
  -> stopping / escalation decision
```

No search provider, deep-research provider, MCP server or synthesis model is allowed to certify its own evidence authority.

### Provider recommendation at current evidence level

**Exa — candidate default for authority-sensitive/current/cross-lingual discovery.**

Empirically stronger than Tavily on the tested final-vs-withdrawn authority cases, official cross-lingual discovery and vocabulary-mismatch discovery. This does not establish global recall superiority.

**Tavily — candidate specialist/default fallback for long-document and PDF extraction.**

Empirically stronger on the tested long NIST PDF extraction, preserving useful structure and long content. It should not currently own final authority selection because basic and advanced search both showed lifecycle/authority-ranking weakness in the tested NIST case.

**Direct controlled primary-source retrieval — authority inspection boundary.**

Search ranking, snippets and provider-generated summaries are candidate discovery, not final material evidence. Critical sources should be reopened directly when access permits.

**Crossref — DOI/deposited metadata/correction/retraction verification layer.**

Live testing showed useful DOI and retraction relationships, but also a real record where a bibliographic title field was absent. Therefore it is not a universal complete metadata truth source.

**Semantic Scholar — scholarly discovery/graph/version enrichment layer.**

Useful live enrichment for DOI/title/authors/ACL/arXiv identity, but unauthenticated access exhibited rate limiting. It complements rather than replaces Crossref/publisher/venue verification.

**Publisher/venue/full text — final critical scholarly content/identity check where available.**

**Perplexity Search/Sonar/Deep Research/MCP/API — optional unproven adapter, not current default.**

The benchmark does not establish that Perplexity is worse. It establishes that no observed unresolved capability gap currently justifies paying for it before a controlled route-level test. If tested later, it should be compared against the routed stack on deep decomposition, authoritative-source recovery, citation entailment, conflict handling, latency and total task cost — not vendor marketing claims.

### Buy/not-buy decision

**Do not buy an additional research provider for this architecture yet.**

Current empirical gaps can be handled by specialization among the already tested routes plus direct verification. Paid Perplexity or another deep-research service becomes justified only if a frozen benchmark demonstrates material incremental value above this stack.

---

## What was actually tested

### Retrieval/provider behavior

Paired Exa/Tavily tests covered, among other things:

- current/final authoritative source ranking;
- vocabulary mismatch;
- long PDF extraction;
- scholarly identity / DOI-style discovery;
- counterevidence retrieval;
- cross-lingual official-source discovery;
- final-vs-withdrawn lifecycle traps.

Observed result: provider strengths were materially different, supporting routing rather than universal-provider selection.

### Scholarly verification

Live Crossref/Semantic Scholar checks covered exact DOI identity/enrichment and correction/retraction signals. They demonstrated both complementarity and public-access operational limitations.

### Synthesis and claim integrity

- deterministic integrity fixtures: **PASS 10/10**;
- frozen Gemini synthesis smoke: **PASS 5/5 after deterministic re-adjudication of grader defects**;
- Perturbation A: **semantic PASS 5/5, P0=0**;
- live semantic claim decomposition: **semantic PASS 5/5, P0=0**;
- Perturbation B: **NOT RUN behaviorally** after first request returned 503 and the one allowed retry returned free-tier 429. It remains a registered robustness gap, not a behavioral failure.

The repeated grader defects are themselves an evaluation result: naive lexical checking is not adequate for professional evidence synthesis. Claim text must be interpreted together with polarity, status, scope and citations.

### Security/trust

Established by deterministic and live gates:

- tool-boundary security preflight PASS;
- checkout credentials removed with `persist-credentials: false` in hardened workflows;
- URL/SSRF authorization policy PASS 23/23;
- MCP/tool poisoning + provenance policy PASS 6/6;
- live OWASP hostile-content retrieval confirmed that authoritative sources can contain instruction-like text and therefore source authority must never imply instruction authority;
- no retrieved content or MCP metadata may rewrite the trusted research contract, claim class or stakes.

Not established: complete OS/network process isolation or DNS-rebinding-safe production transport. Those require a controlled fetcher/egress proxy whose checked destination is bound to the actual connection and every redirect is re-authorized.

### Evidence lineage and dependence

Established gates include:

- source lineage / correlated-source detection;
- syndication/live upstream example;
- methodological/common-cause dependence;
- evidence dependence graph structure;
- evidence aggregation and retraction-lineage invalidation.

Important distinction:

```text
many URLs != many independent sources
independent publishers != independent methodologies
different methods != automatically comparable evidence
```

Unknown dependence metadata remains `UNKNOWN`, never silently promoted to independence.

### Claim/stakes and stopping behavior

Established deterministic gates include:

- claim-class + stakes-aware evidence requirements: PASS 9/9;
- trusted claim/stakes routing: PASS 6/6;
- adversarial decomposition completeness contract: PASS 6/6 plus negative controls;
- query-budget/decomposition control: PASS;
- research stopping/evidence-gap policy: PASS 10/10.

The live semantic decomposition test then showed the synthesis model can, on the tested set, separate high-stakes actions from low-stakes product/price questions while preserving material qualifiers.

---

## Required architecture controls

### 1. Trusted control plane

Before retrieval, create a typed `ResearchContract` containing:

- decision/question;
- atomic material claims;
- claim class and stakes;
- jurisdiction, population, language, version and time constraints;
- freshness/lifecycle requirements;
- source classes needed;
- confidentiality constraints;
- cost/latency budget;
- unresolved evidence gaps;
- stopping/escalation conditions.

Retrieved text cannot lower stakes, rewrite the contract or authorize actions.

### 2. Query planning without query explosion

Atomic claims do not imply one paid search per claim.

Classify subclaims as at least:

- `MUST_RESEARCH`;
- shareable under one retrieval route;
- derived after retrieval;
- `CLARIFY_FIRST`;
- no external query required.

Preserve high-stakes recall while minimizing redundant calls.

### 3. Provider routing

Use the cheapest route plausibly sufficient for the claim, then escalate only for a concrete evidence gap.

Examples:

- known official URL -> controlled direct inspection;
- current authority/cross-language discovery -> Exa candidate;
- long PDF extraction -> Tavily candidate;
- DOI/retraction -> Crossref;
- scholarly discovery/enrichment -> Semantic Scholar/other scholarly graph adapter;
- conflict/low authority/no primary -> second discovery route if expected information value justifies it.

### 4. Access-state honesty

Track `FULL`, `PARTIAL`, `METADATA_ONLY`, `SNIPPET_ONLY`, `INACCESSIBLE`.

Never claim full primary inspection from metadata, snippets, search summaries or inaccessible content.

### 5. Provenance and lifecycle

Track canonical identity and relationships such as draft/final, preprint/version-of-record, correction, withdrawal, retraction, supersession, mirror and syndication.

Retracted or withdrawn upstream support invalidates dependent descendants for the affected claim. A superseded source does not create a live conflict with the current source merely because both URLs still exist.

### 6. Independence/dependence model

Store source lineage separately from methodological/common-cause dependence.

Relevant common causes can include dataset, benchmark, measurement pipeline, population/time window, annotators, synthetic-data model and vendor telemetry.

The current numeric dependence weights are heuristic only. Use qualitative flags/routing signals; do not expose pseudo-probabilities such as “72% independent”.

### 7. Conflict and comparability

Before aggregation, establish that evidence addresses the same construct, scope, lifecycle, metric and decision context.

Do not majority-vote:

- syndication descendants;
- shared-dataset pseudo-replications;
- different metrics;
- different populations/domains/languages when the claim requires generalization.

### 8. Claim-class-aware aggregation

Use categorical states such as:

- `SUPPORTED`;
- `PARTIAL`;
- `CONFLICTED`;
- `CONTRADICTED`;
- `UNVERIFIED`;
- `NOT_COMPARABLE` where appropriate.

Do not manufacture numeric confidence without an empirically calibrated probabilistic model.

Evidence requirements differ for legal/regulatory, medical/safety, safety-critical engineering, scientific benchmarking, current product facts and low-stakes hypotheses. Domain-specific expert profiles must refine these scaffolds before high-stakes deployment.

### 9. Schema-enforced synthesis

Machine-consumed synthesis should use enforced structured output where the provider supports it. The empirical run found semantically correct but malformed plain JSON; schema enforcement corrected that failure mode.

### 10. Claim/citation verification

Verify the tuple:

`claim + polarity/status + citations + evidence location + lifecycle/access state`.

A real citation that does not entail the claim is still a failed citation.

### 11. Read-only research security

Research plane is read-only by default and receives no unrelated secrets. Retrieved content, source metadata and MCP descriptions are untrusted data. Write/action tools belong to a separate authorization plane.

Production URL retrieval requires controlled egress, redirect revalidation, private/link-local blocking and DNS-rebinding-safe connection handling.

### 12. Evidence ledger and observability

Persist enough information to audit:

- contract/decomposition;
- queries and provider/model/tool versions;
- raw result ranks;
- opened/rejected sources and reasons;
- access/lifecycle/provenance;
- lineage/dependence decisions;
- transformations/calculations;
- conflicts/comparability;
- synthesis and citation verification;
- security events;
- latency/tokens/API credits/quota/CI cost;
- stopping reason.

### 13. Failure-specific retry rules

Do not treat every error as “retry”. Distinguish at least:

- behavioral/evidence failure;
- authentication/configuration;
- short rate limit;
- daily quota exhaustion;
- transient capacity 503;
- provider outage;
- model/endpoint lifecycle retirement.

Observed examples included all of lifecycle retirement, transient 503 and free-tier quota exhaustion.

### 14. Research stopping

Continue only when the next action targets a concrete unresolved evidence gap with enough expected decision value.

Possible stopping actions include:

- `STOP`;
- `CONTINUE`;
- `CLARIFY_FIRST`;
- `STOP_WITH_LIMITATION`;
- `ESCALATE_OR_DEFER`.

A quota boundary never turns an unresolved high-stakes claim into a supported claim.

---

## Serious alternative considered

The serious alternative was a single universal deep-research/search provider responsible for discovery, extraction, synthesis and citations.

It loses on current evidence because:

1. tested providers showed complementary strengths and different lifecycle/ranking/extraction failures;
2. self-generated citations require independent verification;
3. DOI/retraction identity is a distinct bibliographic problem;
4. primary source inspection is a distinct authority problem;
5. provider outage/quota/model retirement otherwise becomes a correlated single point of failure;
6. trusting provider/MCP metadata as authority expands prompt-injection and provenance risk;
7. one-provider convenience encourages opaque cost and retry behavior.

A multi-layer design costs more engineering complexity, but routing prevents that from becoming “call every provider every time”. Specialization plus stopping rules is the stronger trade-off.

---

## Expert-gap discovery

Question: **What would a strong research engineer / information scientist / professional researcher notice missing even if the user did not ask for it?**

Substantial gaps identified and incorporated during the benchmark:

- source lifecycle, not merely publication date;
- source lineage and syndication correlation;
- methodological/common-cause dependence;
- access-state honesty;
- negative/failed authority-search evidence;
- claim-class/stakes-specific thresholds;
- claim decomposition completeness before retrieval;
- query-explosion prevention;
- explicit abstention states;
- hidden-holdout contamination protection;
- provider health/quota/model lifecycle as routing inputs;
- prompt-injection and MCP provenance boundaries;
- SSRF/redirect/private-network controls;
- citation entailment rather than citation presence;
- research stopping based on evidence gaps and marginal value;
- grader reliability as part of the evaluation target itself.

Still missing or not fully validated:

- calibrated quantitative dependence scoring;
- production-grade DNS-rebinding-safe egress implementation;
- large hidden retrieval corpus sufficient for population-level provider ranking;
- independent external practitioner adjudication;
- domain-specific legal/medical/engineering evidence profiles;
- optimal grouped-vs-split query granularity measured empirically;
- broad license/privacy policy for persistent raw evidence;
- Perturbation B behavioral result due provider capacity/quota block.

---

## Red-team

### Senior researcher

Critique: “The engineering is elaborate, but a small retrieval pilot cannot prove provider superiority or scientific validity.”

Accepted. Provider defaults remain route-specific candidates, not universal rankings. Evidence states preserve scope; large hidden benchmarks and practitioner review remain required before hard defaults or high-stakes deployment.

### Information-retrieval engineer

Critique: “Discovery quality is under-sampled, recall is hard to measure without a judged corpus, and routing can overfit these examples.”

Accepted. The architecture separates durable requirements from provisional provider assignments. A larger judged retrieval set is a future hard-default gate, not a reason to collapse back to one provider now.

### Evaluation scientist

Critique: “You repaired graders after seeing outputs; that can move the goalposts.”

Accepted. Raw outputs and original failures were retained, repairs were limited to demonstrable implementation defects (negation/status/alias coverage), and later tests should freeze graders plus hidden cases before execution. The benchmark explicitly reports these repairs rather than silently converting red runs to green.

### Security engineer

Critique: “Tool-boundary and URL policy tests do not prove process-level containment or DNS-rebinding-safe transport.”

Accepted. Security verdict is scoped: tool/provenance/URL authorization controls have evidence; production egress isolation remains an implementation gate. No claim of complete sandbox security is made.

### Hiring manager / senior practitioner

Critique: “This could become too slow and expensive to use in ordinary work.”

Addressed through risk-based routing, shared retrieval, cheap-first deterministic checks, explicit budgets, manual-only completed CI gates, quota-aware stopping and provider escalation only for concrete gaps. The architecture is intentionally not an ensemble-everything design.

---

## Final gaps and uncertainty

These are not blockers for the design recommendation, but must remain visible:

1. **Perturbation B:** `NOT_RUN / PROVIDER_CAPACITY+QUOTA_BLOCKED`; first attempt 503, one allowed retry 429.
2. **Provider rankings:** small empirical sample; no claim of global Exa/Tavily superiority.
3. **Perplexity:** not empirically head-to-head tested with paid/API access; therefore neither winner nor loser.
4. **OS/network isolation:** actual production egress/DNS rebinding containment not proven.
5. **Dependence weights:** structural graph validated, numeric weights not calibrated.
6. **High-stakes domain rules:** architectural scaffolds only; domain standards/professional expertise remain necessary.
7. **Semantic decomposition:** passed a five-case adversarial batch, not universal completeness proof.
8. **Provider lifecycle/capacity:** current adapters must be live-checked; model names/endpoints cannot be treated as permanent.

---

## Final recommendation

### For the future Agent Architect research layer

Adopt the architecture in this benchmark as the design basis, with provider adapters behind interfaces rather than embedded vendor assumptions.

Use current route candidates:

```text
Exa                -> authority/current/cross-lingual discovery candidate
Tavily             -> long-document/PDF extraction candidate
Direct fetcher     -> primary inspection authority boundary
Crossref           -> DOI/deposited metadata/retraction verification
Semantic Scholar   -> scholarly discovery/graph enrichment
Publisher/venue    -> final critical scholarly verification
LLM synthesis      -> schema-enforced, evidence-normalized, never self-authoritative
Verifier           -> claim/status/citation/lifecycle/access checks
```

Keep Perplexity/deep-research providers as optional adapters until a controlled benchmark demonstrates incremental value.

### Design verdict

**RESEARCH ARCHITECTURE: PASS.**

**MULTI-LAYER ROUTING OVER ONE UNIVERSAL PROVIDER: RECOMMENDED.**

**CURRENT PROVIDER ROUTES: PROVISIONAL, EVIDENCE-BACKED CANDIDATES — NOT GLOBAL WINNERS.**

**ADDITIONAL PAID PROVIDER ACCESS: NOT JUSTIFIED AT THIS STAGE.**

**AGENT ARCHITECT MODIFICATION: OUT OF SCOPE FOR THIS TRACK; NO CHANGE MADE.**

The next phase, if separately authorized, is implementation design/integration of this research layer into Agent Architect with Resource & Cost Engineering controls — not more open-ended provider shopping.
