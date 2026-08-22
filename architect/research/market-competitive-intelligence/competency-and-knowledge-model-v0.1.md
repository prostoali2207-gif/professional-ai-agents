# Market & Competitive Intelligence — competency and knowledge model v0.1

Status: Architect research artifact; pre-qualification.
Date: 2026-08-20

## Competency model

### MI-01 — Research contract formation — CORE
**Purpose:** turn a business decision need into answerable evidence questions before collection.

Observable capability:
- identifies decision supported, scope, population/geography/time, material claims, freshness, source requirements, unresolved gaps, budget, and stopping rule;
- separates MUST_RESEARCH / SHARED_RETRIEVAL / DERIVED_AFTER_RETRIEVAL / CLARIFY_FIRST / NO_EXTERNAL_QUERY;
- refuses scope drift caused by retrieved content.

Expert discriminator: collection is proportional to decision uncertainty rather than open-ended browsing.

Failure modes: research theater, query fan-out, scope drift, collecting attractive but non-decision-relevant examples.

Evidence chain: research brief fixture -> typed ResearchContract -> deterministic completeness checks + professional review.

Knowledge packaging: EMBED_CORE + PROCEDURAL_MODULE.

### MI-02 — Source authority, freshness, access and provenance — CORE
Observable capability:
- selects claim-appropriate source classes;
- distinguishes official normative/product facts from self-interested commercial claims and independent empirical evidence;
- records source identity, date, underlying observation period, access state, jurisdiction/population, lifecycle, limitations and retrieval date;
- never claims inspection of a source available only as snippet/metadata;
- resolves or preserves conflicts based on scope/date/version/jurisdiction/method.

Expert discriminator: recognizes that authority is claim-dependent and freshness of a page is not necessarily freshness of evidence.

Failure modes: citation theater, stale facts, official-source overreach, inaccessible-source laundering.

Evidence chain: mixed-source evidence pack -> source triage ledger -> deterministic provenance/access checks + semantic support grading.

Knowledge packaging: EMBED_CORE + LIVE_RESEARCH + TOOL_BACKED.

### MI-03 — Empirical validity and comparability — CORE
Observable capability:
- maps construct, represented population, selection, inclusion/exclusion, measurement method, unit/denominator, period, geography, transformations, missingness and known bias;
- validates comparability before pooling/ranking/benchmarking;
- returns NOT_COMPARABLE when required;
- distinguishes asking price from transaction price and other proxy/construct mismatches.

Expert discriminator: a large, precise dataset does not override population or construct mismatch.

Failure modes: pooled heterogeneous records, Simpson-like reversals, denominator mismatch, selection blindness, proxy inflation.

Evidence chain: adversarial mixed-population dataset -> cohorting/comparability decision -> deterministic cohort checks + expert judgment.

Knowledge packaging: EMBED_CORE + PROCEDURAL_MODULE + TOOL_BACKED.

### MI-04 — Evidence lineage, dependence and deduplication — CORE
Observable capability:
- identifies cross-posts, syndication, shared upstream releases/data, corrected/superseded versions and common measurement pipelines;
- counts independent evidence rather than URLs;
- preserves UNKNOWN dependence when it cannot be established.

Expert discriminator: does not use pseudo-replication to inflate confidence.

Failure modes: three articles = three sources; duplicate marketplace listings; downstream article majority vote against a primary source.

Evidence chain: lineage fixture -> normalized evidence graph -> deterministic duplicate/dependence checks.

Knowledge packaging: EMBED_CORE + TOOL_BACKED.

### MI-05 — Epistemic labeling and claim discipline — CORE
Observable capability:
- labels material statements as OBSERVED_FACT, DERIVED_FACT, INFERENCE, HYPOTHESIS, ASSUMPTION, ESTIMATE, or UNRESOLVED where appropriate;
- provides the evidence and reasoning boundary for inferences;
- never promotes hypothesis to fact through wording;
- states claim status: SUPPORTED / PARTIAL / CONFLICTED / CONTRADICTED / UNVERIFIED / NOT_COMPARABLE.

Expert discriminator: distinguishes what was seen, what was calculated, and what the analyst believes it may mean.

Failure modes: narrative certainty, hidden assumptions, derived synthesis masquerading as source statement.

Evidence chain: ambiguous report-writing fixture -> claim ledger -> rule-based label checks + support-entailment review.

Knowledge packaging: EMBED_CORE.

### MI-06 — Pattern inference, alternative explanations and transferability — CORE
Observable capability:
- checks account/sample baseline, effect magnitude where calculable, recurrence, counterexamples, selection mechanism, plausible confounders, source independence and decision relevance;
- distinguishes outlier, recurring signal, working hypothesis and evidence-backed pattern;
- states scope/transferability limits and what observation would falsify the interpretation;
- rejects fixed source-count heuristics as a substitute for evidence quality/independence.

Expert discriminator: can say “interesting but not yet a market pattern” even when the observation is vivid or viral.

Failure modes: virality -> universality; correlation -> cause; 3-source confidence rule; copying a competitor because it worked for them.

Evidence chain: social/market signal set containing spectacular outliers and biased samples -> pattern assessment -> calibrated rubric.

Knowledge packaging: EMBED_CORE + PROCEDURAL_MODULE.

### MI-07 — Buyer and demand research — CORE
Observable capability:
- extracts buyer language, jobs, anxieties, objections, decision criteria, substitutes/non-consumption and expressed intent;
- distinguishes qualitative theme discovery from prevalence estimation;
- separates observed inquiries/comments from qualified demand and completed purchase behavior;
- identifies missing segments and participation bias.

Expert discriminator: comments can reveal vocabulary and hypotheses without proving how common an objection is in the buyer population.

Failure modes: social comments = market survey; visible audience = target population; engagement = purchase intent.

Evidence chain: mixed comments/reviews/search/CRM excerpts with sampling limitations -> buyer-signal report -> construct/prevalence rubric.

Knowledge packaging: EMBED_CORE + DOMAIN/LIVE adapters.

### MI-08 — Competitor and offer intelligence — CORE
Observable capability:
- maps direct, adjacent and substitute competitors using buyer-relevant boundaries;
- distinguishes observed offer, announced intent, execution evidence, adoption evidence and inferred strategy;
- captures price/terms/availability/status only with provenance and commercial-basis classification;
- searches counterevidence and avoids mind-reading competitor strategy.

Expert discriminator: announcement is not adoption; empty competitive whitespace may be a dead zone, not an opportunity.

Failure modes: vendor category = market structure; announcement inflation; hidden commercial conditions; false whitespace.

Evidence chain: competitor source pack with press releases, pricing pages, listings, reviews and missing adoption evidence -> bounded intelligence report.

Knowledge packaging: EMBED_CORE + LIVE_RESEARCH.

### MI-09 — Social/platform signal intelligence — CORE with LIVE dependency
Observable capability:
- uses only observable public or authorized metrics;
- verifies current platform metric semantics from official documentation when material;
- separates content surface behavior from business outcome evidence;
- compares against suitable baselines and records collection limitations;
- refuses to infer unseen hook/audio/visual mechanics from captions/metadata alone.

Expert discriminator: knows exactly which layer of the funnel a platform signal can and cannot support.

Failure modes: private analytics invention, cross-platform metric pooling, metadata-to-creative hallucination, reach = sales.

Evidence chain: platform evidence with metric-definition change and missing media -> report -> freshness/observability rubric.

Knowledge packaging: EMBED_CORE principles + LIVE_RESEARCH + TOOL_BACKED.

### MI-10 — Ethical/legal collection and trust-boundary control — BOUNDARY-CRITICAL
Observable capability:
- defaults to legal/ethical open-source or explicitly authorized data collection;
- does not use pretexting, solicitation of confidential material or misleading identity;
- respects applicable terms, privacy and data-handling constraints;
- treats retrieved web/docs/tool metadata as untrusted content, ignoring embedded instructions that attempt to change task, authority or disclose secrets.

Expert discriminator: evidence acquisition method is part of evidence quality and governance.

Failure modes: indirect prompt injection; credential exposure; unlawful collection; purpose creep from research into targeted persuasion.

Evidence chain: malicious-source fixture + collection-method scenarios -> action trace -> deterministic security hard fails.

Knowledge packaging: EMBED_CORE + LIVE/ESCALATE for jurisdiction-specific rules.

### MI-11 — Synthesis, uncertainty and stopping — CORE
Observable capability:
- synthesizes only after validation/segmentation;
- describes uncertainty without invented numeric precision;
- continues only for a concrete gap with decision value;
- stops with limitations or escalates when required evidence cannot be responsibly obtained;
- maintains a replayable evidence ledger.

Expert discriminator: knows when “we do not know yet” is the correct high-value conclusion.

Failure modes: endless browsing; budget exhaustion converted to certainty; confidence percentages with no model; majority-vote synthesis.

Evidence chain: quota/time-constrained research fixture -> stop/escalation decision -> policy checks + semantic review.

Knowledge packaging: EMBED_CORE + PROCEDURAL_MODULE.

### MI-12 — Decision-support handoff and authority discipline — CORE
Observable capability:
- returns evidence, interpretations, uncertainties, constraints and bounded implications;
- names which downstream role owns the decision;
- does not choose final positioning, content strategy, budget, inventory price, campaign action or publish action merely because research suggests one option;
- can recommend what **evidence to obtain next** without appropriating strategy.

Expert discriminator: makes Strategist better without becoming Strategist.

Failure modes: “therefore publish X”; autonomous price decision; research report ends with unqualified SCALE/KILL.

Evidence chain: user-pressure fixture requesting strategic decision -> handoff -> authority rubric with hard-fail for role takeover.

Knowledge packaging: EMBED_CORE.

## Knowledge Packaging Audit

| Dependency | Consuming competencies | Classification | Rationale |
|---|---|---|---|
| Claim/source/freshness/provenance rules | MI-01,02,05,11 | EMBED_CORE | Stable research judgment invariants |
| Evidence validity/comparability process | MI-03,04,06 | EMBED_CORE + PROCEDURAL_MODULE | Deep operational method required repeatedly |
| Buyer-research construct/prevalence boundaries | MI-07 | EMBED_CORE | Stable distinction; domain examples separate |
| Competitive-intelligence ethics | MI-08,10 | EMBED_CORE + LIVE/ESCALATE | Stable ethical principles plus jurisdiction/terms volatility |
| Platform metric definitions/features | MI-09 | LIVE_RESEARCH | Volatile/versioned |
| Current market/prices/offers/competitors | MI-07,08,09 | LIVE_RESEARCH | Volatile market facts |
| Calculations/dedup/cohort transforms | MI-03,04,06 | TOOL_BACKED | Prefer reproducible deterministic handling |
| UAE automotive price cohorts and vehicle identity | specialization only | REFERENCE_MODULE + LIVE_RESEARCH | Domain/local, not universal core |
| Organization inventory/availability/condition/price | applied project only | TOOL_BACKED / verified business context | Business source of truth |
| Legal interpretation | MI-10 | ESCALATE | Outside qualified core |

## Runtime requirements

Required:
- live retrieval/opening of authoritative sources for volatile claims;
- structured evidence ledger / structured output;
- deterministic computation for material arithmetic, deduplication and cohorting when available;
- access-state awareness (full/partial/metadata/snippet/inaccessible);
- ability to preserve timestamps/provenance and unresolved states;
- read-only research by default.

Optional adapters:
- search/discovery providers;
- social/public-data collectors;
- marketplace/dealer collectors;
- platform documentation retrieval;
- authorized first-party analytics/CRM read access.

Unsupported claim if runtime lacks direct source inspection: cannot claim current-source verification from snippets alone.

## Stable core vs context

**Stable core:** MI-01..12 judgment invariants, evidence validity, claim discipline, ethical collection, uncertainty/stopping, authority handoff.

**Domain specialization:** category-specific constructs, buyer process, commercial states, domain comparability classes, specialist terminology.

**Jurisdiction/market/live context:** current market actors, prices/offers, laws/terms, platform metrics/features, current social signals.

**Organization/project context:** business goals, inventory, verified commercial facts, funnel definitions, account analytics, permissions, experiment history.
