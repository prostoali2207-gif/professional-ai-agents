# MCP / Tool Poisoning + Provenance Boundary — Result — 2026-08-15

Status: **DETERMINISTIC POLICY PASS (6/6)**. This is not yet a live MCP+LLM security PASS.

## What was tested

The preflight validates backend trust and provenance rules for research tool outputs:

1. malicious instructions embedded in MCP/tool metadata are treated as data;
2. malicious instructions embedded in tool results are treated as data;
3. a provider's own claim that a URL is canonical/official cannot promote authority;
4. source-identity mismatch blocks promotion even when an authoritative-looking source is later opened;
5. independently reopened and identity-matched primary evidence may be promoted;
6. independently reopened secondary evidence remains secondary and never becomes primary merely because it was successfully fetched.

GitHub Actions run: `31874557322`.
Artifact: `mcp-tool-poisoning-provenance-boundary-v0.1-record`.

## Result

All six deterministic cases passed with zero P0 failures.

Key invariant:

`transport/provider trust != evidence authority`

Every external research tool result enters the evidence pipeline as `unverified-tool-output`. Authority promotion requires an independent verification event that binds the candidate record to a reopened source identity and source class.

## Architecture consequence

The future research layer must preserve at least three independent fields rather than one generic confidence score:

- `tool/provider_identity` — which adapter produced the candidate;
- `source_identity_verified` — whether the cited/reported source was independently resolved/reopened and matched;
- `source_class/authority_basis` — why that source is primary, secondary, official product documentation, scholarly index, etc.

MCP server installation or OAuth trust must never imply evidence authority.

## What remains unproven

This gate is deliberately scoped. It does **not** prove:

- a real MCP server cannot return adversarial metadata/results that influence an LLM before normalization;
- a live LLM will always respect these backend types;
- a compromised MCP server cannot attempt source-identity spoofing through redirects or look-alike domains;
- real Exa/Tavily results with embedded prompt injection will be contained end-to-end;
- OS/network egress isolation.

Therefore the next empirical security stage should use a real retrieval adapter plus canary hostile content, while keeping the grader and authority promotion deterministic. It should not spend synthesis-model quota until the retrieval/provenance path itself is proven.

## Verdict

- MCP/tool metadata trust boundary: **POLICY PASS**
- tool-result instruction boundary: **POLICY PASS**
- independent provenance/authority promotion: **POLICY PASS**
- live MCP + LLM poisoning resistance: **NOT YET PROVEN**
