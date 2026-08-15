# Exa vs Tavily paired pilot result v0.1 — 2026-08-15

Status: empirical research-only benchmark result. Does not modify Agent Architect behavior, `architect/SKILL.md`, v1.1 validation, or PR #1.

## Scope

This pilot extends the initial P0 comparison with five deployment-relevant retrieval cases:

1. obscure authoritative evidence recall;
2. counterevidence discovery;
3. cross-lingual authoritative retrieval;
4. citation-candidate identity integrity;
5. raw-document candidate access/lifecycle discrimination.

Fixed-query basic runs were paired across Exa hosted MCP and Tavily Search API. Tavily received one pre-authorized advanced retry only on basic misses. No provider-specific query rewriting or domain allow-list tuning was used.

## Empirical results

### 1. Obscure authoritative evidence — NIST AI 600-1

Gold authority: final NIST Generative AI Profile, NIST AI 600-1, DOI `10.6028/NIST.AI.600-1`.

Exa:
- rank 1 was the final official NIST PDF `nvlpubs.nist.gov/nistpubs/ai/nist.ai.600-1.pdf`;
- returned the correct DOI and final publication text in highlights;
- directly exposed raw primary-source content.

Tavily basic:
- rank 1 was a third-party Modulos summary;
- rank 2 was NIST's withdrawn initial public draft, which explicitly says it was superseded;
- an official NIST framework page appeared, but the final 600-1 PDF was not in top 5.

Tavily advanced retry:
- again ranked Modulos first;
- again returned the withdrawn NIST draft second;
- final official NIST 600-1 PDF remained absent from top 5.

Verdict: **clear Exa edge for lifecycle-sensitive primary-source discovery.** Tavily demonstrates a repeatable authority/lifecycle ranking weakness on this fixture.

### 2. Counterevidence discovery — BM25 versus dense retrieval

Gold evidence: arXiv `2604.01733`, *From BM25 to Corrective RAG: Benchmarking Retrieval Strategies for Text-and-Table Documents* (2026), which reports BM25 outperforming the tested dense retriever on the financial text-and-table benchmark while hybrid + reranking performs best overall.

Exa:
- rank 1 surfaced the exact paper/DOI representation;
- highlights contained the counterevidence claim and numerical retrieval results.

Tavily:
- rank 1 surfaced the exact arXiv paper;
- subsequent results included secondary/practitioner hybrid-retrieval material.

Verdict: **both pass required counterevidence recall.** No universal provider edge established by this case.

Methodological implication: a research layer needs an explicit counterevidence search step. Provider choice alone cannot replace adversarial evidence-seeking.

### 3. Cross-lingual authoritative retrieval — UAE AI Strategy 2031

Task language: English. Required evidence: official Arabic UAE source for the national AI strategy.

Exa:
- rank 1 surfaced the Arabic UAE AI Office (`ai.gov.ae/ar/`), with Arabic strategy text;
- also surfaced the official UAE National Strategy PDF.

Tavily basic:
- top results were secondary English sources;
- official UAE Cabinet and Ministry of Justice sources appeared, but in English;
- required Arabic primary source was absent from top 5.

Tavily advanced retry:
- improved authority by putting UAE Cabinet rank 1;
- still returned the English Cabinet page rather than the requested Arabic primary source;
- secondary English sources remained prominent.

Verdict: **Exa edge on this cross-lingual primary-source fixture.** Tavily improved domain authority but did not satisfy the language requirement.

### 4. Citation candidate identity — BERT NAACL 2019

Gold: ACL Anthology version of record, authors Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova, DOI `10.18653/v1/N19-1423`.

Exa:
- rank 1 surfaced ACL Anthology with correct authors, Anthology ID, DOI, pages and BibTeX candidate;
- this run did not reproduce the malformed arXiv-author metadata seen in the earlier P0 query.

Tavily:
- rank 1 was the DOI/ACL Anthology representation;
- ranks 2-4 were ACL Anthology variants of the same version of record.

Verdict: **both pass candidate identity recall.** Neither becomes the bibliographic authority; final DOI/version verification remains Crossref + primary scholarly source.

### 5. Raw-document candidate access / lifecycle discrimination — NIST AI 600-1

Exa:
- rank 1 was the final official NIST 600-1 PDF with direct content highlights.

Tavily basic:
- rank 1 was NIST's withdrawn draft;
- rank 2 was a public comment attachment from Regulations.gov;
- final primary PDF was absent from top 5.

Tavily advanced retry:
- rank 1 became a Regulations.gov comment attachment;
- rank 3 remained the withdrawn NIST draft;
- final primary PDF was still absent from top 5.

Verdict: **Exa clear edge.** This is not a mere domain-authority problem: both the withdrawn draft and final document are official NIST artifacts, so lifecycle-state reasoning is required downstream even when retrieval succeeds.

## Combined evidence with earlier P0

The extended pilot strengthens, rather than overturns, the initial specialization result:

### Exa observed strengths
- lifecycle-sensitive technical/primary-source discovery;
- semantic/terminology discovery;
- cross-lingual primary-source retrieval in the tested UAE case;
- counterevidence recall;
- direct raw-document candidate surfacing.

### Exa observed weaknesses
- prior run exposed malformed scholarly metadata for an arXiv BERT result;
- long-PDF fetch is prefix/character-window oriented and less controllable for exact page/table inspection;
- provider metadata must not be treated as bibliographic truth.

### Tavily observed strengths
- strong long-PDF extraction in the NIST AI RMF structural fixture;
- good citation-candidate retrieval on BERT;
- passed the counterevidence paper retrieval case;
- very low operational friction through a simple Search/Extract API.

### Tavily observed weaknesses
- repeated ranking of withdrawn/stale official artifacts above final official documents;
- third-party summaries can outrank canonical primary sources even with advanced search;
- advanced mode did not repair the tested cross-lingual language miss;
- stronger extraction does not imply stronger source selection.

## Architecture decision after pilot

Do **not** choose one universal provider.

Current evidence supports the following routed research architecture:

1. task/query classification;
2. lexical/direct-web baseline in parallel where recall matters;
3. Exa as a strong candidate-discovery path for semantic, technical, lifecycle-sensitive and cross-lingual discovery;
4. Tavily as a strong document extraction path, especially for long PDFs/documents;
5. explicit lifecycle-state resolution (`draft -> RC -> final -> superseded/withdrawn`);
6. direct primary-source inspection as the authority boundary;
7. Crossref + scholarly graph/primary venue verification for DOI/bibliographic identity;
8. evidence normalization and comparability checking;
9. explicit counterevidence/conflict search;
10. synthesis;
11. independent claim-to-citation verification.

No provider ranking score should collapse these responsibilities into a single number.

## Perplexity escalation decision

**Do not purchase Perplexity API credits yet.**

The pre-registered escalation rule is not currently satisfied strongly enough:
- observed Tavily discovery weaknesses are substantially covered by Exa + direct primary-source inspection;
- observed Exa extraction weakness is substantially covered by Tavily + direct PDF inspection;
- scholarly identity is covered by Crossref/primary venue verification;
- the ensemble has not yet demonstrated a material gap that only Perplexity Search/Sonar/Deep Research plausibly resolves.

Perplexity remains a serious candidate for a later agentic/deep-research comparison, not a required raw-retrieval purchase at this gate.

## Remaining material gaps

This pilot still does not establish:
- generalized accuracy from a statistically meaningful hidden holdout set;
- retrieval behavior on genuinely blocked/paywalled sources;
- agent-layer prompt-injection resistance;
- synthesis-level conflict handling;
- final claim-to-citation correctness after generated synthesis;
- production routing thresholds and fallback policy;
- longitudinal reliability under provider/index changes;
- cost per successfully verified evidence unit at production scale.

These are the next research gates. The cheapest next step is to test the remaining gaps using direct web, frozen fixtures and existing free Exa/Tavily access before paying for another provider.
