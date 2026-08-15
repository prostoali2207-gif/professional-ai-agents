# Exa vs Tavily paired interim — 2026-08-15

Status: empirical paired interim. Research-only; no Agent Architect behavior change.

## Executive result

The empirical evidence rejects the hypothesis that one of Exa or Tavily should simply replace the other as a universal research provider.

Observed specialization is complementary:

- Exa was stronger on current technical-source discovery/ranking and terminology-oriented semantic discovery.
- Tavily was stronger on this scholarly identity case and substantially stronger on long-PDF extraction fidelity/completeness.
- Both still require independent primary-source and bibliographic verification.

## Paired case comparison

### Current authoritative technical source

Exa:
- surfaced stable release, official final-release blog, and canonical current specification in the leading evidence set;
- better represented the final lifecycle state in the observed run.

Tavily:
- basic and advanced modes both ranked a third-party summary first;
- official release candidate remained close to or above final official evidence;
- canonical specification did not appear in the top five under the fixed query.

Interim edge: **Exa**.

### Scholarly identity / DOI

Exa:
- found the correct ACL version of record and DOI;
- also exposed an arXiv result whose metadata author field was malformed/inconsistent with the underlying BERT evidence.

Tavily:
- ranked Semantic Scholar first with correct BERT authors and DOI `10.18653/v1/N19-1423`;
- arXiv preprint followed separately.

Interim edge: **Tavily**, while neither becomes bibliographic authority.

### PDF structural extraction

Exa:
- fetched the NIST PDF as a prefix-character representation;
- reaching the page-22 gold table required progressively increasing the character window up to 120k;
- table structure remained partially flattened and less controllable by page/region.

Tavily:
- advanced Extract returned the full ~106k-character document in one observed request;
- retained `Page 22`, continuation marker, GOVERN 5/6 ordering and the boundary before `5.2 Map`;
- geometric table cells are still flattened, so visual verification remains necessary for exact layout claims.

Interim edge: **Tavily**, clearly for this fixture.

### Vocabulary mismatch / terminology discovery

Exa:
- surfaced terminology around term/vocabulary mismatch, semantic matching and stronger IR-oriented evidence.

Tavily:
- identified the vocabulary-mismatch concept, but top results were more practitioner/commercial; advanced mode moved Wikipedia to rank 1 rather than improving authority.

Interim edge: **Exa** for discovery quality; neither should be the final evidence authority.

## Architecture implication

Current evidence supports a provider-neutral routed ensemble rather than a universal provider:

1. query/task classifier;
2. Exa candidate discovery for semantic/current technical search where its observed strengths apply;
3. Tavily extraction path for long documents/PDFs where its observed extraction advantage applies;
4. lexical/direct-web fallback to reduce correlated retriever failure;
5. direct primary-source inspection;
6. Crossref + scholarly graph verification for bibliographic identity;
7. evidence normalization and comparability analysis;
8. synthesis;
9. independent citation/claim verification.

Provider routing must remain evidence-driven and replaceable. These four P0 cases are insufficient to hard-code permanent routing policy.

## What this does NOT establish

- It does not prove Exa globally has higher retrieval recall.
- It does not prove Tavily globally has better PDF extraction.
- It does not evaluate Perplexity yet.
- It does not evaluate autonomous Deep Research quality.
- It does not establish agent-layer prompt-injection resistance.
- It does not measure statistically stable generalized accuracy.

The result is a P0 routing hypothesis that has survived the first paired empirical tests and should advance to a larger pilot, not a final winner declaration.

## Next evidence gate

Before paying for Perplexity, expand the paired pilot just enough to determine whether the Exa/Tavily/direct-web ensemble leaves a material gap in:
- fresh authoritative discovery;
- obscure evidence recall;
- conflict/counterevidence discovery;
- cross-lingual retrieval;
- blocked/raw-document access;
- citation correctness after synthesis.

Only if a material unresolved gap remains should Perplexity receive a paid smoke, per the pre-registered escalation rule.
