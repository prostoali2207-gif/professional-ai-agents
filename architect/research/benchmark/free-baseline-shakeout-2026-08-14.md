# Free Research Baseline Shakeout — 2026-08-14

Status: empirical shakeout using only currently available no-key research primitives. This is not a provider ranking and does not modify Agent Architect runtime behavior.

## Purpose

Establish a free baseline before spending money on Perplexity, Exa, Tavily, or other providers.

The baseline tests whether direct web retrieval plus primary-source inspection can already satisfy important research-integrity requirements, and identifies exactly which capabilities remain untested because of tool-access limitations rather than research quality.

## Environment

Available for this run:

- general/direct web search;
- opening retrieved web pages;
- official primary-source inspection;
- public scholarly/metadata web pages;
- GitHub repository evidence capture.

Not available as a clean executable primitive in this run:

- direct arbitrary HTTP calls to Crossref singleton endpoints from the browser harness;
- direct arbitrary HTTP calls to Semantic Scholar paper endpoints from the browser harness;
- paid Perplexity/Exa/Tavily APIs;
- controlled raw rank/result dumps from those providers.

Important: inability to execute a public API through this tool environment is an integration limitation, not evidence that the underlying service is weak.

---

## Case LIVE-AUTH-01 — Current MCP specification

### Target capability

Authoritative-primary-source retrieval + freshness + document-state discrimination.

### Task

Determine the current released Model Context Protocol specification as of 2026-08-14 and distinguish it from older official pages and the preceding release candidate.

### Retrieval trace

Broad search surfaced:

- official 2025-03-26 specification pages still indexed;
- official 2025-11-25 specification pages;
- March 2026 roadmap stating that November 2025 was then the current release;
- May 2026 `2026-07-28` release-candidate announcement;
- July 28, 2026 final `2026-07-28` specification announcement;
- current SDK documentation referring to the `2026-07-28` revision.

### Gold resolution

Current released specification: `2026-07-28`.

The May 2026 page is a release candidate and must not be treated as the final authority once the July 28 final release exists.

The 2025-11-25 pages are authoritative historical specification pages but stale for a question asking for the current release.

### Result

**PASS** for direct-web + primary-source inspection.

### What this exposed

1. `official domain` is not sufficient for freshness.
2. `newest date` is not sufficient unless document lifecycle/status is understood.
3. Search can return stale authoritative pages high in results.
4. The research system needs explicit fields such as:
   - publication state: draft / RC / final / superseded;
   - version;
   - effective/release date;
   - supersedes / superseded-by relation.
5. Freshness evaluation must grade state resolution, not merely retrieval of a recent URL.

---

## Case SCHOLAR-01 / SCHOLAR-02 shakeout — BERT bibliographic identity and version control

### Target capability

DOI/bibliographic identity + preprint/version-of-record distinction.

### Task

Identify the intended work `BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding`, determine the peer-reviewed/conference version identifier, and distinguish it from the arXiv preprint.

### Retrieved evidence

Primary/strong records surfaced:

- ACL Anthology conference record: NAACL 2019, pages 4171–4186, DOI `10.18653/v1/N19-1423`;
- arXiv record: `arXiv:1810.04805`, initially submitted October 2018;
- Google Research publication page linking the work to NAACL 2019;
- DBLP conference record carrying DOI `10.18653/V1/N19-1423`;
- DBLP arXiv/CoRR record separately representing the 2018 preprint.

### Gold resolution

Version of record / conference publication:

- title: `BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding`;
- venue: NAACL 2019;
- DOI: `10.18653/v1/N19-1423`.

Preprint:

- arXiv identifier: `1810.04805`;
- separate from the conference DOI and publication date.

A title match alone is insufficient because the preprint and conference version share title/authors while representing different bibliographic records and dates.

### Result

**PASS** for version distinction using direct scholarly/publication records.

**PARTIAL / NOT SCORED** for Crossref and Semantic Scholar API verification because the current browser harness did not permit clean execution of arbitrary constructed singleton API URLs during this run. Their public documentation confirms the required endpoint classes exist, but documentation is not substituted for an empirical API result.

### What this exposed

1. Research records need `work identity` separate from `document/version identity`.
2. A paper can have multiple legitimate identifiers across manifestations.
3. `same title + same authors` must not automatically collapse records.
4. DOI verification belongs after discovery and before final citation emission.
5. Scholarly verification should reconcile at least:
   - title;
   - authors;
   - venue;
   - year/date;
   - DOI;
   - preprint identifier;
   - version relationship.

---

## Baseline scorecard

| Capability | Direct web baseline | Evidence from shakeout | Status |
|---|---|---|---|
| authoritative primary-source discovery | strong | official MCP and ACL records found | PASS |
| freshness | usable but requires reasoning | old official MCP versions coexisted with final 2026 release | PASS with explicit lifecycle logic |
| document-state discrimination | necessary and achievable | RC vs final vs historical spec | PASS |
| scholarly identity | usable | ACL + arXiv + DBLP cross-check | PASS |
| preprint vs version-of-record | usable | BERT 2018 arXiv vs 2019 NAACL | PASS |
| DOI verification via canonical registry | theoretically available | Crossref endpoint documented, not cleanly executed in current harness | NOT YET EMPIRICALLY SCORED |
| scholarly graph retrieval | theoretically available | Semantic Scholar API documented, not cleanly executed in current harness | NOT YET EMPIRICALLY SCORED |
| raw rank/recall measurement | weak in current live browser | no frozen comparable provider result arrays | NOT SUFFICIENT |
| extraction fidelity | not yet run in this shakeout | requires frozen HTML/PDF gold corpus | PENDING |
| conflict/comparability | not yet run in this shakeout | requires controlled evidence pair/set | PENDING |
| prompt-injection robustness | not yet run in this shakeout | should use frozen adversarial pages/docs | PENDING |
| provider cost/latency comparison | impossible without provider calls | no paid API runs | PENDING |

---

## Architectural consequences from the free baseline

### 1. Direct web must remain a first-class fallback

Even if a commercial search provider becomes the default discovery adapter, the architecture should retain direct primary-source retrieval and source reopening. The free baseline already resolves important current/authoritative cases without a paid provider.

### 2. Source authority and source state are separate fields

Required normalized record fields should include at least:

`authority_class`, `version`, `publication_state`, `published_at`, `updated_at`, `effective_at`, `supersedes`, `superseded_by`, `retrieved_at`.

### 3. Scholarly records need manifestation-aware identity

Use a model similar to:

`research work -> manifestations/versions -> identifiers -> source records`.

Do not flatten arXiv, proceedings, journal version, correction, retraction, and metadata mirrors into one undifferentiated paper object.

### 4. Free infrastructure is sufficient for a meaningful baseline, not a final provider comparison

The no-key stack can test:

- authority routing;
- source opening;
- freshness/state reasoning;
- bibliographic/version distinctions;
- citation-to-source inspection;
- many adversarial frozen cases.

Paid or keyed access is only required to answer a narrower question:

> Which commercial discovery/retrieval provider improves recall, ranking, extraction, latency, and cost over this baseline on the same hidden cases?

This is materially different from requiring paid tools to build the research architecture itself.

---

## Next free experiments

Before requesting paid keys, expand the baseline with:

1. `EXTRACT-01`: frozen official HTML table with human gold cells/anchors;
2. `EXTRACT-02`: frozen PDF with selected page/table gold evidence;
3. `CONFLICT-01`: two authoritative sources whose apparent disagreement is scope-dependent;
4. `COMP-01`: credible but non-comparable metrics;
5. `ADV-02`: synthetic hostile page with prompt injection;
6. `ADV-03`: fake paper/DOI metadata requiring independent rejection;
7. `HOP-01`: vocabulary-mismatch retrieval;
8. at least three rolling live freshness cases from the previous 30–90 days.

Only after these gold cases exist should commercial provider runs begin.

## Current decision

The free baseline is **worth keeping permanently**. It is not a temporary substitute for paid search; it is the control condition and authority-verification path against which commercial providers must demonstrate incremental value.
