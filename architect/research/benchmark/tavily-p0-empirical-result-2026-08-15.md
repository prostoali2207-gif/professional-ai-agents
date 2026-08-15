# Tavily P0 empirical result — 2026-08-15

Status: empirical research-only result. Does not modify Agent Architect behavior, `architect/SKILL.md`, v1.1 validation, or PR #1.

## Execution

Tavily Search and Extract were invoked from GitHub Actions using repository secret `TAVILY_API_KEY`. The secret-presence gate passed; the secret value was not printed or persisted in benchmark artifacts.

Primary run: `Tavily P0 Smoke`, run 31868387854, head `940d8c0cf134fd3fb551c4df17814f46ba4389c9`.

Protocol-authorized advanced retry: `Tavily P0 Advanced Retry`, run 31868436500, head `18567d695bf97ebd403a2f17e91ffdd376522e6f`.

The retry kept identical queries and result caps. No provider-specific domain tuning was added.

## Case results

### P0-1 AUTH/FRESH — HOLD / P1 ranking-authority weakness

Basic search top five:
1. third-party Kingy AI summary;
2. YouTube;
3. official MCP release-candidate post;
4. third-party migration article;
5. official final-release blog post.

The canonical current specification was not in the top five. The stale/RC official source ranked above the official final-release post.

Advanced retry improved the official final-release post to rank 3 and the release candidate to rank 4, but still ranked a third-party summary first and still omitted the canonical specification from the top five.

Verdict: useful discovery but fails the benchmark's default-authority ranking requirement. A downstream authority resolver could repair this; Tavily search ranking alone cannot be trusted to select the current canonical source.

### P0-2 SCHOLAR — PASS for discovery; external verification still required

Top results included:
1. Semantic Scholar BERT record with DOI `10.18653/v1/N19-1423` and correct authors;
2. arXiv `1810.04805` preprint;
3. arXiv PDF;
4. arXiv HTML version.

The provider successfully separated useful preprint and publication evidence and surfaced the correct version-of-record DOI in the top result.

This is materially cleaner than the Exa run's malformed arXiv metadata field. Nevertheless, Tavily is still a discovery adapter, not the bibliographic authority: DOI identity must be rechecked against Crossref/ACL/primary scholarly metadata.

### P0-3 EXTRACT — STRONG PASS with residual visual-verification requirement

Advanced Extract returned approximately 106k characters from the NIST AI RMF PDF in roughly 0.4 seconds in the observed run.

The extracted representation preserved the gold region:
- continuation marker and page provenance (`Page 22`);
- `GOVERN 5` followed by `GOVERN 5.1` and `GOVERN 5.2`;
- `GOVERN 6` followed by `GOVERN 6.1` and `GOVERN 6.2`;
- transition/boundary before section `5.2 Map`.

The table is flattened into linear markdown/text rather than retaining geometric cells, so exact layout-sensitive claims still require direct PDF/visual inspection. For this fixture, however, parent-child order and page/boundary provenance remained reconstructable.

This is substantially better operationally than the observed Exa default fetch path, which required progressively increasing a prefix-character window to reach page 22 and retained weaker table structure.

### P0-4 HOP — PASS for terminology discovery; weak authority ranking

Basic search recognized the vocabulary-mismatch concept and returned resources discussing lexical vs semantic retrieval and vocabulary mismatch, including a scholarly/academic result lower in the ranking.

Advanced retry ranked `Vocabulary mismatch` on Wikipedia first, followed mostly by practitioner/commercial sources. This is useful terminology discovery but not strong evidence-source ranking.

Verdict: passes the terminology-expansion purpose of the case, but requires a separate scholarly/authority resolver before evidence use.

### P0-5 ADV — NOT SCORED AT RAW RETRIEVER LEVEL

The current Tavily run exercised Search/Extract primitives, not an autonomous synthesis agent with privileged action tools. Prompt-injection compliance must be evaluated at the downstream agent/synthesis boundary where hostile retrieved text could influence behavior. Do not award a fake security PASS to a read-only retrieval primitive.

## Operational observations

- API secret handling through GitHub Actions worked correctly.
- Search latency in the observed basic cases was roughly 1.5–2.9 seconds; advanced retries roughly 2.9–3.2 seconds.
- PDF advanced extraction in this fixture was materially faster and more complete than the observed Exa MCP fetch path.
- Exact Tavily credit consumption should be read from provider usage/billing telemetry; this benchmark does not infer billing from request count when the response does not return a billing field.

## P0 disposition

`ADVANCE TO PAIRED PILOT`, but not as a universal provider.

Best observed role: document extraction / broad web discovery, with especially strong long-PDF extraction in this sample.

Required compensating layers:
- authority/current-version resolver;
- direct primary-source inspection;
- Crossref/scholarly bibliographic verification;
- downstream citation verification;
- agent-layer prompt-injection controls.
