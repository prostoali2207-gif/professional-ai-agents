# Research Architecture Benchmark — August 2026

Status: research-only recommendation. This document does **not** modify `architect/SKILL.md`, Agent Architect v1.1 behavioral validation, or PR #1.

## Executive decision

Do **not** build Agent Architect research on one universal provider.

The recommended architecture is a **provider-agnostic evidence pipeline** with specialized layers:

`research intent -> query decomposition -> broad discovery -> targeted retrieval -> primary-source inspection -> scholarly/bibliographic verification -> evidence normalization -> conflict/comparability analysis -> synthesis -> citation verification -> evidence ledger`

A general web provider such as Perplexity, Exa, or Tavily can be valuable in discovery/retrieval, and a deep-research product can accelerate exploratory synthesis. Neither should become the authority boundary.

Perplexity is a strong candidate for **one discovery/deep-research adapter**, not a sufficient research architecture by itself.

The architecture must preserve the option to swap or ensemble providers, inspect original documents, and verify scholarly metadata/DOIs independently.

---

## 1. Repository constraints and requirements reconstructed from current `main`

Current Agent Architect methodology already establishes several non-negotiable principles:

- source selection is **claim-first**, not topic-dump-first;
- authority is claim-dependent;
- volatile knowledge requires freshness controls/live retrieval;
- derived synthesis must remain traceable to source and transformation;
- retrieval must be evaluated independently from downstream generation;
- authoritative-but-non-comparable evidence can still be decision-invalid;
- tool interfaces must expose enough state to distinguish success from apparent success and diagnose failures;
- evaluation must grade both outcome and trajectory, and P0/P1 integrity failures cannot be averaged away.

Therefore the future research layer must expose evidence and intermediate state, not merely return a polished answer.

### Research capabilities a strong Agent Architect actually needs

The professional model is closer to a combination of:

- research engineer;
- information-retrieval engineer;
- information scientist / librarian;
- evidence-synthesis analyst;
- scientific/bibliographic researcher;
- evaluation scientist;
- security engineer for untrusted external content.

Required capabilities include:

1. translate an agent-design question into explicit evidence needs;
2. decompose broad questions into searchable subclaims;
3. discover relevant sources with high recall;
4. prioritize claim-appropriate authoritative sources;
5. detect version/date/jurisdiction/population mismatch;
6. retrieve and inspect raw source content rather than relying on snippets or provider summaries;
7. follow citations/references and search backward/forward where useful;
8. verify bibliographic identities and DOIs independently;
9. distinguish publisher metadata, indexes, preprints, mirrors, secondary reporting, and vendor-generated synthesis;
10. extract claims faithfully with source location/provenance;
11. preserve contradictory evidence rather than smoothing it away;
12. evaluate comparability before combining evidence;
13. track uncertainty and unresolved gaps;
14. resist prompt injection or malicious instructions embedded in retrieved content;
15. observe queries, sources, tool calls, failures, costs, latency, and transformations;
16. verify every material citation-to-claim association before final synthesis;
17. evaluate the research process on frozen and live tasks.

---

## 2. Benchmark dimensions

Provider comparison must not collapse into one marketing-style score. Dimensions have different failure costs.

### Discovery and retrieval

- discovery recall;
- precision/ranking quality;
- reasoning-intensive / multi-hop retrieval;
- source diversity;
- authoritative-primary-source retrieval;
- domain/date/language/region control;
- freshness and update-date control;
- scientific/academic coverage;
- raw-document access;
- JavaScript/PDF extraction capability;
- deep-site crawl/map capability.

### Evidence integrity

- stable source URL/identifier;
- provenance fidelity;
- raw text versus model-generated summary distinguishability;
- citation-to-claim correctness;
- DOI/identifier support;
- bibliographic verification;
- retraction/update/correction metadata where available;
- extraction fidelity;
- source-scope metadata;
- conflict preservation;
- evidence comparability support.

### Agent engineering

- query decomposition / deep research;
- controllability;
- observability of queries/tool calls/progress;
- structured outputs;
- API quality;
- MCP availability;
- deterministic primitives versus opaque agentic behavior;
- latency;
- cost predictability;
- rate limits;
- vendor lock-in;
- graceful failure semantics.

### Security / trust

- retrieved content treated as untrusted data;
- prompt-injection exposure;
- arbitrary navigation/exfiltration risk;
- isolation of research reads from write/action tools;
- domain allowlisting;
- least-privilege credentials;
- auditability;
- data retention/privacy controls;
- ability to preserve raw evidence without executing embedded instructions.

---

## 3. Provider / system benchmark

Legend: `Strong`, `Useful`, `Limited`, `Unknown` reflect suitability for this architecture, not an overall product ranking. Vendor claims are not treated as independent quality evidence.

| System | Best architectural role | Strong points supported by docs/evidence | Material limitations / unknowns |
|---|---|---|---|
| **Perplexity Search API** | broad web discovery | Raw ranked results; multi-query; domain allow/deny filters; language, country, publication-date, last-updated and recency controls; configurable result/context limits | Search quality/recall versus competitors still needs our own controlled eval; provider index/ranking remains opaque; not a bibliographic authority |
| **Perplexity Sonar / Pro Search** | web-grounded answer + exploratory synthesis | Integrated web-grounded responses; Pro/Fast modes; controllable search filters; OpenAI-compatible integration | Generated answer can hide retrieval/synthesis coupling; must not be used as independent citation verifier of itself |
| **Perplexity Sonar Deep Research** | exploratory deep research / secondary researcher | Long-horizon search and synthesis across many sources; async operation; citations | Vendor describes “hundreds of sources” and expert-level synthesis, but these are product claims; independent benchmarks show deep-research systems remain far below expert completeness on many tasks; opaque internal retrieval trajectory relative to primitive search tools |
| **Perplexity MCP** | convenient adapter | exposes search, ask, research, reason tools through MCP | MCP convenience does not solve evidence validity; remote tool adds trust/credential boundary |
| **Exa Search** | semantic web discovery, research-paper/code discovery | Natural-language semantic search; search modes from instant/fast to deep; domain/date controls; category including research paper; can return text/highlights with results | independent recall/authority benchmark needed; deep modes combine retrieval/synthesis; proprietary index |
| **Exa Contents** | raw-document extraction | Full-page clean markdown; JS-rendered pages, PDFs, highlights; cache/livecrawl control; known-URL retrieval and subpage crawling | extraction fidelity must be tested against raw documents; generated summaries/highlights must be distinguished from extractive text |
| **Exa MCP** | retrieval adapter | open-source MCP server; explicit web search and web fetch primitives; advanced search controls | same remote-tool/prompt-injection trust boundary; free endpoint limits may differ from production behavior |
| **Tavily Search** | agent-oriented web discovery | Basic/advanced search; designed for agent retrieval; low-cost primitive; source results | controlled recall/authority benchmark required; proprietary ranking/index |
| **Tavily Extract / Crawl / Map** | targeted retrieval and site exploration | separate extraction, site mapping, and crawling primitives; clean content; path filters/instructions | site crawling can greatly expand untrusted-content attack surface; extraction fidelity needs adversarial tests |
| **Tavily Research** | secondary deep-research adapter | mini/pro/auto research modes; structured output schema; async/status and streaming progress with tool-call visibility | much more expensive/variable than primitive search; generated report must still undergo independent evidence verification |
| **Tavily MCP** | retrieval adapter | exposes search/extract through MCP; broad agent-framework compatibility | same trust/credential concerns; MCP is transport, not evidence validation |
| **Semantic Scholar Academic Graph** | scholarly discovery / graph enrichment | large academic graph; paper/author/citation/reference metadata; external IDs; abstracts and some PDF-related metadata; public unauthenticated access for many endpoints | not a canonical DOI registry; metadata/entity resolution can be imperfect; coverage varies by field; rate behavior without key is shared/throttled |
| **Crossref REST API** | DOI/bibliographic verification | open public API; publisher/member-deposited metadata; DOI lookup; updates, licences, funding, ORCID/ROR and Retraction Watch-derived data available; no signup required for public access | metadata completeness depends on deposits; not full-text retrieval; DOI coverage does not equal all scholarly output |
| **OpenAlex** | scholarly discovery / graph cross-check | large open scholarly knowledge graph, work/author/source/institution relationships, DOI/PMID/etc lookup, retraction field, downloadable snapshot | API currently requires a free key; metadata has documented historical quality failures (including a retraction-status incident), so it should be a cross-check, not sole authority |
| **Direct web/browser + primary source** | authority boundary / final inspection | sees the actual official standard, documentation, paper, regulatory text, dataset, or product page; supports exact scope/version inspection | slower; extraction/navigation variability; prompt injection; paywalls/robots/login/JS/PDF issues; requires disciplined browsing and caching |

### Important non-winner finding

The strongest capabilities are **complementary rather than substitutable**:

- a web search API is good at discovery but is not a DOI authority;
- Crossref is excellent for bibliographic identity but cannot replace full-text inspection;
- Semantic Scholar/OpenAlex add scholarly graph discovery but should not be assumed canonical for every metadata field;
- a deep-research agent can accelerate decomposition and exploration, but a polished report is not proof that each material claim is correctly grounded;
- direct primary-source inspection is the authority boundary, but by itself is inefficient for broad discovery.

This makes a one-provider architecture structurally weaker.

---

## 4. Evidence on deep-research evaluation

### Retrieval and search must be disentangled from synthesis

**BrowseComp (OpenAI, 2025)** demonstrates that hard-to-find information requires persistent and creative browsing, but OpenAI explicitly describes it as incomplete for broader user research tasks.

**BrowseComp-Plus (ACL 2026)** fixes an important evaluation flaw: dynamic black-box web search makes fair retriever comparison difficult. It uses a fixed, human-verified corpus to separate retrieval quality from agent quality. The paper reports a large performance change when the same agent is paired with a stronger retriever, supporting the need to evaluate our retrieval layer independently.

**SAGE (2026)** further warns against assuming semantic/LLM retrievers automatically dominate simple methods: in its scientific reasoning-intensive retrieval setting, BM25 substantially outperformed the tested LLM retrievers because agents generated keyword-oriented subqueries. This is a strong reason to ensemble lexical + semantic retrieval rather than rely on fashionable retrieval alone.

### Long-form quality cannot be represented by one score

**DeepResearch Bench (2025)** separates report quality from citation/retrieval quality and includes citation accuracy/effective citation measures.

**Mind2Web 2 (NeurIPS 2025)** evaluates long-horizon live web tasks and source attribution; even the best tested system reached only a fraction of human performance.

**LiveResearchBench (ICLR 2026)** argues research tasks should be user-centric, unambiguous, time-varying, multi-faceted, and search-intensive. Its evaluation separates coverage, consistency, depth, citation association and citation accuracy. Crucially, the authors report that naive holistic 0–10 LLM judging aligned poorly with humans and showed high run variance, favoring atomic/checklist/pairwise protocols and multiple judges.

**Deep Research Bench II (2026)** uses thousands of fine-grained expert-derived binary rubrics and reports that even the strongest deep-research systems satisfy fewer than half of them. This is direct evidence against treating any current “Deep Research” product as a sufficient professional research layer without verification.

### Scientific synthesis benefits from specialized scholarly retrieval

**OpenScholar / ScholarQABench (Nature, 2026)** reports substantial gains from a specialized scientific corpus, retriever and self-feedback loop versus generic LLM baselines, with much stronger citation behavior. The architectural implication is not “use OpenScholar everywhere”; it is that domain-specialized retrieval and verification can materially outperform generic web-only research for scholarly tasks.

---

## 5. Security findings

Web research is a security boundary because every retrieved page is untrusted input.

OpenAI's Deep Research system card explicitly identifies prompt injection from browsed pages as a risk that can produce incorrect answers or data exfiltration, and notes residual risk even after mitigation. Anthropic likewise describes every browsed webpage as a possible prompt-injection vector.

The MCP specification also states that tool descriptions/metadata should be treated as untrusted unless obtained from a trusted server and emphasizes explicit consent, least privilege and user control.

### Architecture consequences

1. **Research-only execution context.** The research layer should not share unrestricted credentials or write-capable tools with retrieved web content.
2. **Untrusted-document boundary.** Retrieved text is data, never instruction. Tool output must be tagged with source/trust metadata.
3. **No secret-bearing context in broad research calls.** Do not expose unrelated private repository data, keys, or connected-app content to web research providers.
4. **Read/write separation.** Research adapters should be read-only. Any later action belongs to a separate, explicitly authorized workflow.
5. **Domain allowlists where authority is known.** For standards, regulatory material and product docs, prefer constrained official-domain retrieval after broad discovery.
6. **Citation verification must reopen the cited source.** Do not trust the research provider's own summary as evidence that its citation supports the claim.
7. **Security eval corpus.** Include pages/PDFs containing visible, hidden, indirect and multimodal prompt-injection attempts, malicious citation instructions, fake authority signals and data-exfiltration bait.
8. **Provider/MCP configuration is part of the threat model.** Remote MCP servers, API keys, logs, retention and tool schemas require explicit trust review.

---

## 6. Recommended research architecture

### Layer 0 — Research contract

Input:

- target professional decision;
- claim/evidence dependencies;
- required freshness;
- jurisdiction/version/population;
- acceptable source classes;
- prohibited/low-value source classes;
- output/evidence requirements;
- cost/latency budget.

Output: machine-readable `ResearchPlan` plus human-readable rationale.

### Layer 1 — Query decomposition

Generate multiple evidence-seeking queries, not paraphrases only:

- terminology / profession map;
- official/primary-source queries;
- empirical evidence queries;
- contrary evidence queries;
- practitioner/tacit-work queries;
- failure/incident queries;
- recent-update/version queries;
- scholarly citation-chain queries.

Keep query trace and reason for each subquery.

### Layer 2 — Discovery ensemble

Use at least two retrieval modes where stakes justify it:

- lexical/general web search;
- semantic/AI-oriented search;
- scholarly graph search for academic claims.

Candidate adapters: Perplexity Search, Exa Search, Tavily Search, direct browser/search, Semantic Scholar/OpenAlex.

Do not run all providers on every trivial query. Router selects based on claim type, stakes, and expected value.

### Layer 3 — Source triage and authority routing

Classify every candidate:

- primary normative / official;
- primary empirical;
- official product docs;
- scholarly secondary/synthesis;
- practitioner evidence;
- news/reporting;
- aggregator/index;
- vendor-generated synthesis;
- unknown.

Promote authoritative candidates for inspection; do not synthesize directly from SERP snippets.

### Layer 4 — Raw retrieval / primary-source inspection

Open the real source and capture:

- canonical URL/identifier;
- title/author/organization;
- publication and update/version date;
- relevant raw passage/location;
- document type;
- retrieval timestamp;
- extraction mechanism;
- extraction confidence/errors.

Prefer raw/extractive text over model-generated summaries for evidence records.

### Layer 5 — Scholarly / bibliographic verification

For academic claims:

1. resolve DOI/identifier through Crossref where applicable;
2. cross-check title/authors/year/venue with Semantic Scholar and/or OpenAlex;
3. inspect publisher/preprint/full text;
4. check retraction/correction/update status where relevant;
5. preserve version relationships (preprint vs accepted vs published).

No single scholarly index is authoritative for all fields.

### Layer 6 — Evidence normalization

Normalize each evidence item into a typed record:

```text
EvidenceRecord
- evidence_id
- claim_id
- source_url
- canonical_identifier(s)
- source_class
- authority_basis
- raw_excerpt / structured observation
- source_location
- publication_date
- update/version_date
- retrieval_date
- jurisdiction/population/version
- measurement / construct metadata when empirical
- extraction_method
- freshness_class
- confidence
- conflicts[]
- security_flags[]
- transformations[]
```

Keep provider summaries separately as `DerivedSynthesis`, never as raw evidence.

### Layer 7 — Conflict and comparability engine

Before aggregation:

- verify same claim/construct;
- compare version/date/jurisdiction/population;
- compare methodology/measurement;
- find real versus apparent conflict;
- segment incompatible evidence;
- record unresolved uncertainty.

### Layer 8 — Synthesis

Synthesis consumes only normalized evidence records and explicit unresolved gaps.

It may use a deep-research system as a **second researcher / hypothesis generator**, but final claims must map back to normalized evidence.

### Layer 9 — Citation verifier

For each material output claim:

`claim -> cited source -> reopened evidence location -> support / partial / contradict / irrelevant / inaccessible`

Critical claims fail closed when the citation cannot be reopened or does not support the claim.

### Layer 10 — Evidence ledger and observability

Persist:

- plan;
- queries;
- provider/tool/version;
- results/rank;
- opened sources;
- rejected sources + reason;
- extraction failures;
- normalized evidence;
- conflicts;
- synthesis transformations;
- citation checks;
- cost/latency;
- security events.

This is needed for debugging, regression and auditability.

---

## 7. Router recommendation

Do not hardcode “Perplexity first” or “Exa first.” Route by research need.

### Fast/current web discovery

Candidates: Perplexity Search / Exa Search / Tavily Search / direct search.

Select empirically using our benchmark on:

- authoritative-source recall@k;
- freshness correctness;
- near-match rejection;
- duplicate/domain diversity;
- latency/cost.

### Known URL / raw extraction

Candidates: direct browser first; Exa Contents or Tavily Extract as fallback/normalizer when direct extraction is poor.

### Site-level documentation exploration

Candidates: Tavily Map/Crawl, Exa subpage crawl, direct sitemap/browser.

### Academic discovery

Use Semantic Scholar + OpenAlex as complementary discovery graphs; direct publisher/preprint reading for evidence.

### DOI / bibliographic identity

Crossref first for Crossref-registered DOI metadata; fall back/cross-check with publisher/DataCite/other identifier registries as claim requires.

### Deep exploratory research

Perplexity Sonar Deep Research, Tavily Research, Exa deep/research, or another deep-research agent can be used as **exploratory parallel researchers**. Their outputs feed candidate claims/sources into verification; they do not bypass it.

---

## 8. Perplexity-specific assessment

### What makes it genuinely attractive

Perplexity is more architecturally useful than a simple “chat with search” product because it now exposes multiple separable surfaces:

- raw Search API;
- Sonar web-grounded model API;
- Pro/Fast search modes;
- Sonar Deep Research;
- domain/date/update/recency/language/country controls;
- MCP tools for search, ask, research and reasoning.

This makes it possible to use Perplexity as a controlled retrieval component rather than only consuming a finished answer.

### Why it should not be the sole provider

1. Retrieval/index behavior is still vendor-controlled and partially opaque.
2. Search, model synthesis and citation generation can share correlated failure modes.
3. It is not a bibliographic registry.
4. It cannot prove extraction fidelity merely by citing a URL.
5. Independent evaluation of research agents shows that polished deep-research systems still miss substantial expert-required information.
6. A provider outage, pricing change, policy change or ranking regression would become a single point of failure.
7. Security exposure is correlated if discovery, retrieval and synthesis all traverse the same external trust boundary.

### Decision

**KEEP AS A CANDIDATE ADAPTER; DO NOT STANDARDIZE AS THE RESEARCH ARCHITECTURE.**

The next empirical gate should decide whether Perplexity earns a default position for specific routes (e.g. fast web discovery or exploratory deep research).

---

## 9. Empirical benchmark design

Documentation comparison is not enough. We need a controlled harness.

### A. Retrieval-only frozen benchmark

Purpose: compare retrievers without synthesis confound.

Create 100–200 expert-labelled tasks across Agent Architect research needs:

- exact official standard/document;
- current product/API behavior;
- obscure multi-hop fact;
- scientific paper by concept rather than title keywords;
- superseded versus current version;
- authoritative source versus popular wrong near-match;
- conflicting sources;
- jurisdiction mismatch;
- non-comparable empirical evidence;
- adversarial SEO/source spam.

Gold record:

`task -> required claim -> acceptable sources -> authoritative target(s) -> distractors -> freshness/scope constraints`

Metrics:

- Recall@5/10/20;
- authoritative-source Recall@k;
- MRR/nDCG where useful;
- freshness correctness;
- scope correctness;
- diversity/duplicate rate;
- retrieval latency;
- cost;
- failure rate.

Run exact same query set against Perplexity Search, Exa Search, Tavily Search and selected baseline search.

### B. Live retrieval benchmark

Use 25–50 dynamic queries with ground truth verified at evaluation time. Repeat across multiple days to measure index/freshness variance.

### C. Raw extraction fidelity benchmark

Use controlled HTML, JS-heavy pages, tables, PDFs, footnotes, multi-column documents, code blocks and pages containing prompt injection.

Compare direct browser extraction, Exa Contents, Tavily Extract/Crawl and any Perplexity raw-content output available.

Grade:

- text completeness;
- table/structure preservation;
- numeric fidelity;
- citation/footnote fidelity;
- page/section attribution;
- injected-instruction containment;
- inaccessible/error signaling.

### D. Scholarly benchmark

Tasks:

- concept discovery;
- exact DOI resolution;
- author/title/year/venue verification;
- backward/forward citation discovery;
- preprint/published-version disambiguation;
- retraction/correction detection;
- same-name author ambiguity.

Compare Semantic Scholar, Crossref, OpenAlex, direct publisher/preprint source.

Do **not** ask one metric to choose a winner: Crossref and scholarly graphs have different jobs.

### E. Deep research end-to-end benchmark

Use representative Agent Architect tasks with expert-derived atomic checklists.

Grade separately:

- coverage/recall of required evidence;
- analysis quality;
- citation association;
- citation accuracy;
- primary-source ratio where appropriate;
- conflict handling;
- uncertainty calibration;
- unsupported-claim rate;
- cost/latency;
- trajectory quality.

Run repeated trials because deep-research systems are stochastic.

### F. Security benchmark

Adversarial corpus:

- direct prompt injection;
- hidden HTML/CSS instruction;
- malicious PDF text;
- instruction inside quoted source;
- fake system/developer messages;
- request to exfiltrate secrets via URL/query;
- malicious tool-description text;
- poisoned high-ranking SEO page;
- citation that redirects to attacker content.

P0 failures:

- follows retrieved instruction over research contract;
- leaks secrets/private context;
- writes/actions through research context without authorization;
- suppresses/rewrites evidence because a page instructs it to;
- reports citation support without opening/verifying the source.

---

## 10. Empirical work completed in this stage and remaining access gap

### Completed without provider credentials

- inspected current Agent Architect source/knowledge, retrieval, evidence-comparability, tool-human-factors and evaluation requirements;
- reviewed official current documentation for Perplexity Search/Sonar/Deep Research/MCP, Exa Search/Contents/MCP, Tavily Search/Extract/Crawl/Map/Research/MCP, Semantic Scholar, Crossref and OpenAlex;
- reviewed independent/academic evaluation evidence including BrowseComp-Plus, Mind2Web 2, LiveResearchBench, DeepResearch Bench, Deep Research Bench II, SAGE and OpenScholar/ScholarQABench;
- used the available live web/browser search in this environment as the direct-web baseline to find and inspect current primary documentation and research sources;
- attempted direct unauthenticated HTTP calls to Semantic Scholar and Crossref from the execution sandbox, but this runtime has no general outbound DNS/network from the shell, so the calls could not be executed there. This is an environment limitation, not an API limitation.

### What cannot be honestly claimed yet

We **cannot** claim that Perplexity, Exa or Tavily wins retrieval quality, latency, cost-adjusted recall, extraction fidelity or deep-research accuracy for Agent Architect. We have not run the identical controlled query set through their APIs.

### Exact access needed for the next empirical gate

For a real head-to-head provider benchmark:

- `PERPLEXITY_API_KEY` with Search API + Sonar/Deep Research access;
- `EXA_API_KEY` with Search + Contents (and deep/research if included); 
- `TAVILY_API_KEY` with Search + Extract/Crawl/Research;
- network-capable benchmark runner for public Crossref and Semantic Scholar endpoints;
- optional free `OPENALEX_API_KEY` for OpenAlex API cross-checks.

No production installation or Agent Architect modification is required for this benchmark. Keys should be injected only into an isolated benchmark environment and never committed.

---

## 11. Expert-gap discovery

Question: **What would a strong research engineer / information scientist / professional researcher notice missing that the user did not know to ask for?**

### Gap 1 — Reference chaining / citation graph traversal

Good research often starts from one strong source and moves backward through references and forward through citing work. This is distinct from keyword search and should be a first-class research operation.

**Repair:** add citation-neighborhood expansion for scholarly research and source-link expansion for standards/docs.

### Gap 2 — Source identity / deduplication / version lineage

The same work may appear as preprint, accepted manuscript, publisher version, mirror and syndicated copy. Counting these as independent evidence creates false corroboration.

**Repair:** canonical source clustering and version lineage.

### Gap 3 — Retractions, corrections and supersession

“Authoritative + current-looking” can still be withdrawn, corrected or superseded.

**Repair:** explicit update/retraction/supersession status and dependent-claim invalidation.

### Gap 4 — Search stopping criteria

Deep research can waste cost indefinitely or stop after convenient confirmation.

**Repair:** evidence-saturation and marginal-value stopping rules: stop when required claims meet evidence thresholds, new queries yield low novel evidence, or budget/risk boundary is reached; escalate unresolved high-impact gaps.

### Gap 5 — Negative evidence / failed searches

Knowing that a targeted search found no authoritative evidence can matter. Most research outputs only retain what was found.

**Repair:** record significant unsuccessful searches and coverage gaps.

### Gap 6 — Correlated-source detection

Ten articles repeating one press release are one underlying evidence chain, not ten independent confirmations.

**Repair:** provenance graph and upstream-source clustering.

### Gap 7 — Paywall / inaccessible-source policy

A citation to content the system could not inspect should not be treated like verified evidence.

**Repair:** source access state: `opened-full`, `opened-partial`, `metadata-only`, `snippet-only`, `inaccessible`.

### Gap 8 — Temporal reproducibility

Live-web results change; future regression diagnosis needs snapshots/identifiers.

**Repair:** retain retrieval timestamps, source hashes where legally/operationally appropriate, provider/result IDs, and frozen eval corpora.

### Gap 9 — Research-budget allocation

Not every claim deserves deep research.

**Repair:** risk-weighted router that allocates more providers, deeper inspection and expert review only to high-impact/uncertain claims.

### Gap 10 — Copyright/data-governance boundary

Raw-document storage and model ingestion can create licensing/privacy issues.

**Repair:** store minimal necessary excerpts/metadata where appropriate, preserve licenses/access conditions, and separate transient retrieval from durable knowledge storage.

---

## 12. Red-team critique

### Senior researcher would criticize

- treating retrieval abundance as evidence quality;
- insufficient attention to citation chaining, supersession and correlated sources;
- synthesis before clarifying constructs/populations/methods;
- lack of explicit stopping/escalation criteria.

**Architecture response:** normalization, lineage, conflict/comparability gate, evidence saturation and escalation.

### Information-retrieval engineer would criticize

- comparing providers only end-to-end;
- dynamic web making retrieval benchmarks non-reproducible;
- one semantic retriever assumption;
- no per-query-class failure analysis.

**Architecture response:** frozen retrieval benchmark, lexical + semantic + scholarly modes, retrieval-only metrics, query-class stratification, repeat live trials.

### Evaluation scientist would criticize

- one aggregate score;
- uncalibrated LLM judges;
- benchmark contamination;
- no stochastic repeat trials;
- no hard gates for citation integrity/security.

**Architecture response:** atomic criteria, heterogeneous graders, frozen + live sets, multiple trials, P0/P1 integrity gates, direct citation verification.

### Security engineer would criticize

- giving a browsing researcher the same secrets/tools as an execution agent;
- trusting MCP servers/tool metadata;
- rendering retrieved text into privileged instruction context;
- allowing citations without safe reopening.

**Architecture response:** isolated read-only research context, least privilege, untrusted-content typing, provider allowlist/trust registry, injection evals, separate action plane.

---

## 13. Recommendation and decision gate

### Recommended target architecture

Adopt a **multi-layer, provider-agnostic research architecture**.

Initial candidate stack for empirical evaluation:

- **General discovery:** Perplexity Search + Exa Search + Tavily Search candidates; select/router by benchmark rather than preference.
- **Raw retrieval:** direct browser/HTTP primary source, with Exa Contents and/or Tavily Extract/Crawl as extraction adapters.
- **Scholarly discovery:** Semantic Scholar + OpenAlex.
- **Bibliographic/DOI verification:** Crossref plus publisher/identifier authority as needed.
- **Deep exploratory synthesis:** Perplexity Sonar Deep Research, Tavily Research, Exa research/deep modes as optional parallel researchers.
- **Evidence normalization/conflict/citation verification:** owned by Agent Architect infrastructure, not delegated to any one provider.
- **Security boundary:** owned by Agent Architect infrastructure.

### Gate before implementation

Do not choose default providers until the controlled empirical benchmark is run.

A provider can become a default for a route only if it passes route-specific critical gates. Example:

- discovery default: authoritative recall/freshness/latency/cost;
- extraction default: fidelity + reliable error signaling;
- deep-research default: coverage + citation accuracy + conflict handling + cost;
- scholarly default: metadata coverage/identity quality for the targeted disciplines.

No aggregate score may compensate for a P0 citation-integrity or security failure.

---

## 14. Key sources

Repository methodology:

- `architect/methodology/source-knowledge-engineering.md`
- `architect/methodology/retrieval-evaluation.md`
- `architect/methodology/evidence-validity-comparability.md`
- `architect/methodology/tool-human-factors.md`
- `architect/methodology/evaluation-calibration.md`

Provider documentation:

- Perplexity Search API: https://docs.perplexity.ai/docs/search/quickstart
- Perplexity Search API reference: https://docs.perplexity.ai/api-reference/search-post
- Perplexity domain filters: https://docs.perplexity.ai/docs/search/filters/domain-filter
- Perplexity date/time filters: https://docs.perplexity.ai/docs/search/filters/date-time-filters
- Perplexity Sonar Deep Research: https://docs.perplexity.ai/docs/sonar/models/sonar-deep-research
- Perplexity MCP: https://docs.perplexity.ai/docs/getting-started/integrations/mcp-server
- Exa Search: https://exa.ai/docs/reference/search
- Exa Contents: https://exa.ai/docs/reference/contents-api-guide
- Exa MCP: https://exa.ai/docs/reference/exa-mcp
- Exa pricing: https://exa.ai/pricing?tab=api
- Tavily API: https://docs.tavily.com/documentation/api-reference/introduction
- Tavily Crawl: https://docs.tavily.com/examples/quick-tutorials/crawl-api
- Tavily Research: https://docs.tavily.com/documentation/api-reference/endpoint/research
- Tavily Research streaming: https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming
- Tavily MCP: https://docs.tavily.com/documentation/mcp
- Tavily pricing: https://docs.tavily.com/documentation/api-credits
- Semantic Scholar API: https://api.semanticscholar.org/api-docs
- Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- OpenAlex developers: https://developers.openalex.org/

Evaluation / research evidence:

- OpenAI BrowseComp: https://openai.com/index/browsecomp/
- BrowseComp-Plus (ACL 2026): https://aclanthology.org/2026.acl-long.1023/
- DeepResearch Bench: https://arxiv.org/abs/2506.11763
- Deep Research Bench (FutureSearch): https://arxiv.org/abs/2506.06287
- Mind2Web 2 (NeurIPS 2025): https://proceedings.neurips.cc/paper_files/paper/2025/hash/fdcec9f5b99aa4fc8f4fb8487802d737-Abstract-Datasets_and_Benchmarks_Track.html
- LiveResearchBench (ICLR 2026): https://arxiv.org/abs/2510.14240
- Deep Research Bench II: https://arxiv.org/abs/2601.08536
- SAGE retrieval benchmark: https://arxiv.org/abs/2602.05975
- OpenScholar / ScholarQABench: https://www.nature.com/articles/s41586-025-10072-4

Security:

- OpenAI Deep Research System Card: https://openai.com/index/deep-research-system-card/
- OpenAI prompt-injection agent design: https://openai.com/index/designing-agents-to-resist-prompt-injection/
- Anthropic browser prompt-injection defenses: https://www.anthropic.com/research/prompt-injection-defenses
- MCP specification: https://modelcontextprotocol.io/specification/2025-11-25
