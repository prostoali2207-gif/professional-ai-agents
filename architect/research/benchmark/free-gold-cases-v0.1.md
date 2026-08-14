# Free Gold Cases v0.1

Status: empirical/free benchmark artifacts for the future Agent Architect research layer. No paid provider keys required.

## Purpose

These cases establish a no-cost control group before comparing Perplexity, Exa, Tavily, or other paid research providers.

The objective is not to maximize answer polish. The objective is to measure whether a research system can retrieve the right evidence, identify document state/version, preserve provenance, detect non-comparability, and refuse unsupported synthesis.

---

## GOLD-FRESH-01 — Official source lifecycle: MCP 2026-07-28

### Target capability

Freshness, lifecycle-state recognition, authoritative-source selection.

### Task

Determine the current released MCP specification version as of 2026-08-14 and distinguish it from the release candidate.

### Gold evidence

1. Model Context Protocol official blog: `The 2026-07-28 Specification`, published 2026-07-28.
2. Model Context Protocol official blog: `The 2026-07-28 MCP Specification Release Candidate`, published 2026-05-21.

### Gold conclusion

The released specification is `2026-07-28`. The May 21 page is explicitly a release candidate and states that the final specification would ship July 28, 2026.

### Hard negatives

- treating the RC as the current final document;
- choosing a previous official specification merely because it ranks highly;
- selecting the newest crawl timestamp rather than document lifecycle state;
- using third-party MCP commentary as authority when first-party release evidence exists.

### Required trace

The system should record:

`candidate -> publisher -> document date -> lifecycle state -> supersession relationship -> selected authority`

### Severity

P1 for stale/RC selection in normal research; P0 if the stale result would drive a safety/security-critical implementation decision.

---

## GOLD-FRESH-02 — Current document vs current lifecycle status: NIST AI RMF

### Target capability

Distinguishing document validity from revision status.

### Task

Identify the current status of NIST AI RMF 1.0 as of 2026-08-14.

### Gold evidence

1. NIST AI Risk Management Framework landing page states that AI RMF 1.0 is being revised.
2. NIST publication record for AI RMF 1.0 identifies the published framework as NIST AI 100-1, published 2023-01-26.

### Gold conclusion

AI RMF 1.0 remains an official published NIST framework, but NIST explicitly states that it is being revised. A system should not falsely claim that a newer final AI RMF version already exists unless it retrieves such a publication.

### Hard negatives

- inferring that "being revised" means the 2023 framework is withdrawn;
- claiming that a draft/concept note is a finalized replacement;
- presenting 2023 as the latest lifecycle update without checking current NIST status.

### Required trace

`published artifact -> current status page -> revision state -> unresolved future replacement`

### Severity

P1.

---

## GOLD-SCHOLAR-01 — Preprint vs version of record: BERT

### Target capability

Scholarly identity resolution, version control, DOI verification.

### Task

Resolve the scholarly identity of `BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding` and distinguish the preprint from the conference version of record.

### Gold evidence

1. arXiv record `1810.04805`, first submitted 2018-10-11.
2. ACL Anthology entry `N19-1423`, NAACL 2019, pages 4171–4186.
3. DOI `10.18653/v1/N19-1423` associated with the NAACL 2019 publication.

### Gold conclusion

The arXiv preprint and NAACL 2019 publication refer to the same research work lineage but are distinct publication records. The DOI belongs to the NAACL 2019 version, not to the arXiv identifier.

### Hard negatives

- presenting `1810.04805` as a DOI;
- assigning the NAACL DOI to the 2018 preprint record without version distinction;
- treating publication dates as contradictory rather than version-specific;
- choosing a similarly titled BERT paper such as `Visualizing and Understanding the Effectiveness of BERT`.

### Required trace

`title -> authors -> preprint identifier/date -> venue record -> DOI -> version relationship`

### Severity

P0 for wrong DOI; P1 for version conflation.

---

## GOLD-IR-01 — Retrieval architecture evidence

### Target capability

Evidence synthesis across independent IR studies without collapsing conflicting results.

### Task

Assess whether a future research layer should rely on one semantic retriever or preserve multiple retrieval modes.

### Gold evidence

1. BrowseComp-Plus uses a fixed corpus and shows large performance differences when the same research agent is paired with different retrievers.
2. `Revisiting Text Ranking in Deep Research` reports that web-search-style agent queries can favor lexical, learned sparse, and multi-vector retrievers; reranking helps materially; query formulation mismatch matters.
3. AgentIR reports gains from reasoning-aware retrieval over conventional embeddings and BM25 in its tested configuration.
4. Cross-lingual BrowseComp-Plus reports substantial degradation in evidence recall, calibration and citation reliability when evidence is language-mismatched.

### Gold conclusion

The evidence does not support a universal single retriever. Retrieval effectiveness depends on query style, corpus, language, task and downstream agent behavior. The defensible architecture is provider-agnostic and supports routing/ensembling plus reranking, with evaluation by task family.

### Conflict rule

Do not interpret one paper's superiority result as globally overriding another. Compare agent, corpus, query formulation, retrieval unit, reranker, language and benchmark conditions.

### Hard negatives

- "semantic search always beats BM25";
- "BM25 is best" based on one setting;
- selecting AgentIR or another model as a universal default from one benchmark;
- averaging heterogeneous benchmark scores across incompatible conditions.

### Severity

P1.

---

## GOLD-VERIFY-01 — Bibliographic authority routing

### Target capability

Independent DOI/bibliographic verification.

### Task

Define what Crossref can and cannot prove in the research architecture.

### Gold evidence

Crossref's official REST API documentation states that its public API exposes scholarly metadata deposited by members and trusted sources, supports direct DOI metadata retrieval, and requires no signup for public access.

### Gold conclusion

Crossref is appropriate as a bibliographic/DOI verification layer, not as a substitute for full-text inspection or a universal scholarly discovery engine.

### Hard negatives

- treating Crossref metadata as proof that a paper's substantive claim is true;
- assuming DOI registration implies full-text access;
- treating absence from Crossref as proof that a scholarly work does not exist.

### Severity

P1.

---

## Scoring notes

Each case should be scored separately for:

- evidence recall;
- authority correctness;
- freshness/version correctness;
- identifier correctness;
- provenance completeness;
- unsupported inference;
- conflict/comparability handling;
- citation-to-claim association.

Critical errors must not be averaged away by a high aggregate score.

## Why these cases matter

These free cases already test several properties that a paid provider may hide behind a polished research report. Any paid provider must therefore demonstrate measurable improvement over this baseline in retrieval recall, ranking, extraction, latency/cost, or workflow efficiency while preserving or improving integrity.
