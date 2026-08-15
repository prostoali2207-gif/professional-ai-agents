# Exa P0 empirical result — 2026-08-15

Status: empirical provider-layer result for research architecture benchmarking. This does not modify Agent Architect behavior, `architect/SKILL.md`, v1.1 validation, or PR #1.

## Configuration tested

- provider: Exa;
- transport: hosted MCP, anonymous/no user API key;
- endpoint: `https://mcp.exa.ai/mcp`;
- exposed tools: `web_search_exa`, `web_fetch_exa`;
- execution surface: isolated GitHub Actions workflow on `research/research-architecture-benchmark-2026-08`;
- MCP client: official Python MCP SDK v2 line;
- no Exa API key or paid credits used.

Primary empirical runs:

- connectivity shakeout: GitHub Actions run `31859250467`, head `7931eda76b8a0d4035f7751a17fa3d3468d7c8a5`;
- multi-case P0: run `31859298222`, head `f906d682872504913b85bb2a345895b12e09225a`;
- deep PDF extraction 50k: run `31859344858`, head `1de896bab63bcf2627d810e846f495b0452c1e48`;
- deep PDF extraction 120k: run `31859386006`, head `9e064a1e9058b88924bb85f4e65e9c4e1cb9d695`.

Artifacts were uploaded by the workflows with raw MCP outputs and immutable artifact digests recorded by GitHub Actions.

---

## P0-1 AUTH/FRESH — current authoritative source + lifecycle

Query:

`Model Context Protocol 2026-07-28 specification final stable release official`

Observed result:

Exa returned, within the first results:

1. official GitHub MCP release tag `2026-07-28`, explicitly described as the stable release;
2. canonical MCP specification at `modelcontextprotocol.io/specification/2026-07-28`;
3. official MCP release blog;
4. official changelog;
5. official versioning documentation stating that `2026-07-28` is the current protocol version.

Search latency in the multi-case run: approximately `0.953 s`.

Verdict: **PASS for discovery/freshness on this case**.

Evidence quality note: Exa did not merely surface a secondary summary; it surfaced the canonical specification and official lifecycle evidence.

This is one case, not a generalized accuracy claim.

---

## P0-2 SCHOLAR — preprint vs version of record / DOI identity

Query:

`BERT Devlin Chang Lee Toutanova 2018 arXiv preprint 2019 NAACL version of record DOI`

Observed positive evidence:

- Exa ranked the ACL Anthology version of record first;
- returned Anthology ID `N19-1423`;
- returned DOI `10.18653/v1/N19-1423`;
- also found arXiv `1810.04805`, allowing the preprint and conference publication to be distinguished.

### Material anomaly

The Exa result wrapper for the arXiv record contained an incorrect `Author:` metadata field naming unrelated authors, while the title/highlights contained the correct BERT authors/citation.

Independent direct inspection of arXiv identifies the authors as Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Therefore the provider-level metadata field is demonstrably unreliable on this returned record.

Verdict:

- **PASS for scholarly discovery of the intended works**;
- **FAIL as a standalone bibliographic authority**;
- severity: **P1 if Exa metadata were used directly as verified bibliographic identity**;
- architecture repair: route DOI/work identity through Crossref and/or canonical scholarly venue metadata before representing it as verified.

This is direct empirical support for keeping scholarly verification independent of the general web retriever.

---

## P0-3 EXTRACT — NIST AI RMF PDF structural fidelity

Source:

`https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf`

### 16k extraction

Fast and useful for front matter/text discovery, but insufficient to reach the gold table around document page 22.

### 50k extraction

Reached only approximately page 9 of the document. This exposed an interface-control limitation: `web_fetch_exa` accepts a maximum character count but does not expose page-target selection in this MCP tool.

### 120k extraction

Reached the gold region and preserved:

- table title and `(Continued)` state;
- page markers `Page 22`, `Page 23`, `Page 24`;
- `GOVERN 5` category text;
- `GOVERN 5.1` and `GOVERN 5.2` content;
- `GOVERN 6` category text;
- `GOVERN 6.1` and `GOVERN 6.2` content;
- transition to `5.2 Map` after the table.

Fetch latency at 120k: approximately `1.166 s`.

### Structural defect

The Markdown representation does not preserve the visual table perfectly. Some category labels, column contents, and line-broken subcategory text are flattened or garbled. For example, portions of the `GOVERN 6` row merge category wording with right-column content before the clean category wording appears again outside the Markdown row representation.

Verdict:

- content recall: **strong on the tested region**;
- page provenance: **useful/preserved**;
- continuation/boundary signal: **preserved**;
- exact row/column fidelity: **imperfect**;
- severity: **P2 for research discovery/extraction use**, but this would become P1 if an architecture treated the generated Markdown table as exact structured data without reinspection.

Architecture implication: Exa fetch is useful for locating and reading PDF evidence, but direct PDF/visual or structure-aware inspection remains required for claim-bearing tables where row/column relationships matter.

---

## P0-4 HOP — vocabulary mismatch

Operational query intentionally avoided the canonical information-retrieval terminology:

`Why can a search system miss a document that is relevant in meaning when the query and the document use different words? Information retrieval research terminology and methods.`

Observed result:

Exa surfaced:

- `Semantic Matching in Search`, whose returned text explicitly identifies `term mismatch between queries and documents` as a major relevance problem and discusses semantic matching;
- Stanford IR material on latent semantic indexing, synonymy, polysemy, and limitations of term-vector matching.

Search latency: approximately `1.458 s`.

Verdict: **PASS on this vocabulary-mismatch shakeout**.

This is a meaningful signal for Exa's semantic discovery role, but it remains one development case and is not sufficient to estimate generalized multi-hop recall.

---

## P0-5 ADV — prompt injection

Not scored against raw Exa `web_search_exa` / `web_fetch_exa` primitives.

Reason: these are read-only retrieval tools; prompt-injection compliance is a property of the consuming agent/synthesis system when it interprets retrieved text. Scoring a non-reasoning fetch primitive as though it could "obey" malicious instructions would be a category error.

Relevant tool metadata did advertise the MCP tools as read-only and non-destructive, which is useful for least-privilege architecture, but this is not a substitute for an end-to-end hostile-document test of the future research agent.

Verdict: **NOT APPLICABLE at retriever-only layer; still required at end-to-end layer**.

---

## Provider-layer decision

### Do not reject Exa.

No P0 integrity failure was observed in the tested raw search/fetch configuration.

### Do not adopt Exa as a universal research provider.

The bibliographic metadata anomaly and PDF structural-loss case demonstrate why independent verification/primary inspection are still required.

### Current architectural status: ADVANCE TO PAIRED PILOT as a discovery/fetch adapter.

Promising roles:

- semantic/general web discovery;
- vocabulary-mismatch discovery;
- rapid source-content acquisition;
- locating current primary sources.

Explicit non-authority roles:

- canonical bibliographic identity / DOI verification;
- exact PDF table extraction;
- final citation-to-claim verification;
- research-agent security policy.

## Comparison against simpler baseline

Exa showed a plausible operational advantage in semantic discovery and returned useful clean content with approximately one-second retrieval latency on these cases. However the sample is too small to establish generalized superiority over direct web retrieval.

The next fair step is not additional Exa tuning. It is the same P0 protocol against Tavily, followed by paired comparison on identical cases.

## Resource decision

No Exa paid usage is justified yet.

The anonymous hosted MCP was sufficient for this P0 and incurred no user API-credit spend. Avoid upgrading or spending Exa credits until a later pilot demonstrates a need for higher rate limits, advanced filters, or authenticated agent features.
