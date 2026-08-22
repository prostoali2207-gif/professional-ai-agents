# Market & Competitive Intelligence — evidence and reuse v0.1

Status: Architect research artifact; pre-qualification.
Date: 2026-08-20

## 1. Reconstruction evidence

### E1 — O*NET: Market Research Analysts and Marketing Specialists
Source: U.S. Department of Labor / O*NET OnLine, occupation 13-1161.00, current page marked Updated 2026.
URL: https://www.onetonline.org/link/details/13-1161.00

Relevant professional work includes researching local/regional/national/online markets; collecting and analyzing customer demographics, preferences, needs and buying habits; devising/evaluating data-collection procedures; gathering competitor prices/sales/marketing/distribution data; monitoring industry statistics and trends; analyzing web metrics; and preparing reports that translate findings.

Use: supports the market-research component of the profession model.
Limit: occupation taxonomy is broad and does not by itself establish evidence-validity, OSINT ethics, or AI runtime requirements.
Freshness: slow; occupational task content is partly older than the 2026 page update, so treated as profession-boundary evidence rather than live market truth.

### E2 — Insights Association Code of Standards & Ethics, 2025 edition
Source: professional association for market research/data analytics.
URL: https://ia.insightsassociation.org/codeofstandards

Relevant principles include professional integrity/transparency, lawful and terms-compliant data collection, clear handling of AI-generated data, disclosure/citation of secondary data, sufficient technical information for independent assessment, and avoiding misleading findings.

Use: supports MI-02, MI-05, MI-10 and reviewability/accountability requirements.
Limit: professional code, not a complete research-methods curriculum and not jurisdiction-specific legal advice.
Freshness: versioned; verify current edition when material.

### E3 — SCIP Code of Ethics / Ethical Intelligence
Source: Strategic Consortium of Intelligence Professionals.
URL: https://www.scip.org/page/Ethical-Intelligence

Relevant principles include legal compliance, integrity, transparency and accurate disclosure of identity before interviews. SCIP frames ethics/integrity as foundational to competitive/market intelligence.

Use: supports the competitive-intelligence profession component and ethical collection boundary.
Limit: code is guidance rather than a substitute for applicable law/terms or evidence-validity methodology.
Freshness: slow/versioned.

### E4 — Agent Architect source/evidence engineering
Internal sources:
- `architect/methodology/source-knowledge-engineering.md`
- `architect/methodology/evidence-validity-comparability.md`

Relevant principles: claim-first source selection; authority is claim-dependent; live retrieval for volatile facts; provenance; access-state honesty; evidence-generating-process mapping; construct validity; selection/coverage risk; lineage/dependence; comparability before aggregation; categorical claim states; claim/citation verification; resource-aware stopping; prompt-injection trust boundary.

Use: provides cross-profession evidence-engineering capability required by this analytical profession.
Freshness: repository-versioned; candidate binds to current main as of 2026-08-20 and must pin exact blobs if promoted.

### E5 — Existing UAE automotive research artifacts
Applied repository evidence reviewed:
- `research/uae-market/2026-08-11-quantitative-instagram-report.md`
- `research/uae-market/2026-08-11-creative-manual-review-batch-1.md`
- current `agents/market-intelligence.md`

Observed strengths:
- explicit no-fabrication rules;
- account-baseline reasoning instead of raw view comparison;
- recognition that extreme hypercar virality may be non-transferable;
- explicit refusal to assert first-three-second creative details when media frames were unavailable;
- price-population separation and vehicle comparability rules in the applied agent.

Observed gaps / qualification risks:
- no explicit evidence-generating-process ledger for the 200-post Instagram sample;
- weak visibility into sampling/coverage and collection-selection bias;
- caption-detectable labels can be mistaken for complete creative mechanisms;
- buyer-comment themes are useful qualitative signals but counts do not establish population prevalence;
- current agent asks for “evidence-grounded test recommendations,” which creates a boundary collision with Strategist;
- no formal source access-state, lineage/dependence, claim-entailment, or stale/superseded-source handling;
- no qualified evidence that the prompt behaves correctly under adversarial mixed-quality evidence.

Use: real work-sample evidence for failure-mode discovery and applied delta design. It is not proof the current agent is professionally qualified.

## 2. Professional Core Library inspection

Catalog inspected: `architect/library/catalog.json`.
Current qualified entries relevant to this target:

### Candidate A — Paid Media / Performance Marketing Practitioner 1.0.0
Decision: **REJECT as the Market Intelligence professional core**.

Compatibility evidence:
- useful overlap in measurement integrity, attribution/causal discipline, experimentation and creative learning;
- similar need for live verification of volatile platform claims.

Critical gaps:
- core responsibility is paid-media allocation/optimization and spend governance, not market/competitive evidence acquisition and synthesis;
- does not cover buyer qualitative research, competitor OSINT, source provenance/lineage, market structure or broad evidence collection;
- authority and output construct are materially different.

Retained value: individual measurement/causal principles may remain reference evidence or adjacent capability, but no core inheritance is claimed.
Required regressions if later composed: interaction between social/market evidence and paid-media conclusions; no transfer of paid-media PASS to MI.

### Candidate B — Growth Experimentation & Measurement Practitioner 1.0.0
Decision: **REJECT as the Market Intelligence professional core**.

Compatibility evidence:
- strong overlap in measurement integrity, denominator/identity discipline, causal-claim boundaries, delayed outcomes and reproducible calculations.

Critical gaps:
- profession is registered-experiment evaluation, not external market research or competitive intelligence;
- lacks source discovery/authority, competitor/buyer research, OSINT collection and broad market evidence synthesis.

Retained value: deterministic measurement-validity patterns can inform eval design; no primary inheritance.

### Candidate C — Video Editing & Post-Production Practitioner 0.1.0
Decision: **REJECT**; wrong profession boundary.

## 3. External repository scan

### deanpeters/Product-Manager-Skills, commit 91956c91f39176b654c11002c48eaaca865742f2
Files inspected:
- `skills/autonomous-investigation/SKILL.md`
- `skills/market-landscape-scan/SKILL.md`

Useful candidate ideas:
- explicit Fact / Inference / Assumption labeling;
- do-not-invent lists;
- decision-linked search plan;
- stable/diffable outputs for repeated scans;
- buyer-view segmentation, substitutes/non-consumption and a “dead-zone” counter-reading for whitespace;
- legal/ethical open-source collection emphasis.

Direct reuse decision: **REJECT**.
Reasons:
- product-management workflow rather than a professionally reconstructed Market/Competitive Intelligence core;
- no qualifying evaluation evidence for the target professional claims;
- fixed “1/2/3+ channels” confidence-stacking heuristic can overstate evidence when sources are dependent, low quality, incomparable or generated from the same upstream signal;
- some downstream strategic “so what” behavior crosses the desired evidence-to-Strategist boundary.

The inspected artifacts are inspiration/evidence candidates only. No prompt or skill text is inherited as a core.

### Other public agent repositories surfaced during search
Examples included competitive-intelligence/research-agent implementations centered on LLM + search/scraping pipelines. None was admitted for reuse because implementation novelty, repository popularity, tool count or self-authored demos do not establish the target professional construct or qualification evidence.

Decision: **REJECT for core reuse unless later evidence demonstrates provenance, construct compatibility and target-relevant qualification**.

## 4. Reuse decision

Target profession: **Market & Competitive Intelligence Research Practitioner**.

Decision: **BUILD NEW** universal professional core.

Grounds:
- no catalog core matches the profession responsibility/output boundary;
- neighboring qualified cores cover only analytical sub-problems;
- external candidates contain useful patterns but lack target-profession qualification and contain at least one unsafe confidence heuristic;
- the profession has stable cross-domain invariants worth separating from UAE automotive/live context.

Alternative considered: EXTEND Growth Experimentation & Measurement.
Rejected because the extension would be larger than the inherited profession, creating misleading identity and coupling. Experiment analysis is a downstream/adjacent capability, not the stable center of market intelligence.

Alternative considered: ADAPT external Market Intelligence Suite.
Rejected because missing qualified professional-core evidence is a hard compatibility failure under Architect reuse policy.

Lifecycle/resource trade-off: BUILD NEW has higher initial evaluation cost but reduces repeated ad-hoc research logic across future domains and prevents UAE automotive specifics from contaminating stable evidence judgment.

## 5. Required evaluation obligations

No prior qualification transfers to the new core.

New core must be evaluated on:
- source authority/freshness/access-state and citation entailment;
- empirical validity/comparability and proxy mismatch;
- sampling/selection and large-biased-sample traps;
- lineage/syndication/cross-post deduplication;
- fact/inference/hypothesis/assumption discipline;
- pattern elevation under spectacular outliers and weak recurrence;
- buyer-comment qualitative insight vs prevalence overclaim;
- competitor announcement vs execution/adoption;
- social metric vs qualified demand/sale construct;
- research stopping and unresolved evidence;
- prompt injection / hostile external content;
- authority handoff to Strategist rather than strategy takeover;
- live-retrieval failure and stale-source behavior.

Applied UAE automotive specialization must then receive separate practical/adversarial evaluation for vehicle comparability, GCC/import/new/used/export states, local marketplace evidence, current platform signals, business-source-of-truth facts and handoff compatibility.