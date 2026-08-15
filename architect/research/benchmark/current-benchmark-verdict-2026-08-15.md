# Current Research Benchmark Verdict — 2026-08-15

Status: interim evidence-backed verdict. Research-only; no Agent Architect behavior change.

## What is established now

### Architecture

**PASS:** the evidence supports a routed multi-layer research architecture over a one-provider design.

Reason: tested providers exhibit materially different strengths and failure modes. No tested system spans authoritative discovery, extraction, scholarly identity, evidence normalization, conflict handling, citation verification and security strongly enough to justify one-provider authority.

### Exa

Current tested role: **candidate default for authority-sensitive/current web discovery and cross-lingual authoritative discovery**.

Evidence observed:

- stronger than Tavily on tested current/final authority ranking;
- stronger on tested cross-lingual official-source discovery;
- handled vocabulary mismatch well in earlier paired pilot.

Limits:

- not established as universal highest-recall search;
- extraction was weaker than Tavily on the tested long PDF;
- larger frozen retrieval set still required.

### Tavily

Current tested role: **candidate default/fallback for long-document/PDF extraction**.

Evidence observed:

- very strong structural extraction on tested NIST PDF;
- preserved page/section hierarchy and long content better than Exa in that case.

Limits:

- authority ranking repeatedly preferred withdrawn/secondary material over final authoritative material on tested lifecycle case;
- advanced retry did not repair that weakness;
- therefore should not currently own final authority selection.

### Direct browser / primary source

Current role: **authority inspection boundary**.

Search-provider ranking is candidate discovery, not final evidence. Material claims should be verified against the actual source when accessible.

### Crossref / scholarly verification

Current role: **bibliographic/DOI identity verification**, not full-text evidence.

A DOI registry, scholarly graph and full-text source solve different problems and should remain separate.

### Perplexity

Current verdict: **UNTESTED EMPIRICALLY / OPTIONAL CANDIDATE**, not rejected.

Documentation indicates useful Search/Sonar/Deep Research/MCP surfaces, but current empirical gaps do not justify paying for it yet. A Perplexity test becomes justified only if an unresolved route-level capability remains after the current stack, or if a future controlled benchmark shows material expected value.

## Integrity / synthesis result

### Deterministic gate

PASS 10/10 on registered integrity fixtures.

### Frozen behavioral synthesis

After preserving raw runs, repairing grader implementation defects, and enforcing JSON schema output, the frozen 5-case synthesis set is adjudicated **PASS 5/5** with zero P0 and zero content-level P1 findings.

Covered:

- inaccessible primary source;
- scoped conflict;
- citation entailment/global overclaim;
- indirect prompt injection in evidence;
- incomparable quantitative metrics.

Important limitation: this is evidence on a small frozen set, not generalized safety or research accuracy.

## Eval defects discovered

The benchmark itself exposed important failure modes:

1. naive phrase matching can generate false failures when a phrase appears under negation;
2. claim text must be interpreted together with `status` and citations;
3. plain JSON prompting can yield malformed structured output even with semantically correct content;
4. hidden holdouts must not be committed into a searchable benchmark corpus before execution;
5. provider operational failures must not be graded as behavioral failures.

These are benchmark-architecture findings, not cosmetic test fixes.

## Provider operational evidence

Observed during real execution:

- retired GitHub Models endpoint/model path: provider lifecycle failure;
- Gemini temporary HTTP 503: capacity/transient failure;
- Gemini free-tier daily request exhaustion at 20 requests for the tested project/model: quota failure;
- schema-enforced Gemini response successfully corrected a previously malformed structured response.

Routing/retry policy must distinguish these classes.

## Current routing recommendation

```text
high-level claim/research need
  -> research contract
  -> cheap discovery route
      authority/current/cross-language -> Exa candidate
      known URL -> direct retrieval
      long PDF/extraction -> Tavily candidate
      scholarly discovery -> scholarly graph(s)
      DOI identity -> Crossref/publisher registry
  -> primary inspection
  -> normalize identity/lifecycle/access/scope
  -> conflict/comparability
  -> structured synthesis
  -> claim+status+citation verification
  -> evidence ledger
```

Escalate to a second provider only when risk/uncertainty warrants it.

## What is not established yet

Do not claim any of the following:

- Exa is globally the best search provider;
- Tavily is globally the best extractor;
- Gemini synthesis is robust to arbitrary adversarial content;
- indirect-injection safety is proven with real write-capable tools;
- Perplexity is worse or better than the current stack;
- the free-tier quota behavior is a universal commercial pricing property beyond the observed project/model execution;
- one clean frozen run proves general research quality.

## Remaining critical gates

1. Perturbation A after quota reset.
2. Perturbation B only if A has no P0.
3. Sandboxed real-tool indirect-prompt-injection test with canary effects.
4. Larger frozen retrieval-only benchmark before hard provider defaults.
5. Final integration design with Resource & Cost Engineering budgets, provider health, quotas and retry policy.

## Interim decision

**RESEARCH ARCHITECTURE: PASS FOR DESIGN DIRECTION.**

**PROVIDER HARD-DEFAULTS: NOT YET.**

**IMPLEMENTATION INTO AGENT ARCHITECT: NOT YET.**

The next expensive/model-dependent work is intentionally blocked until the free quota resets; no paid access is currently justified.