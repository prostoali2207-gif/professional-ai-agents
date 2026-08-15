# Decomposition Query Budget Policy Result — 2026-08-15

## Verdict

**PLANNING/BUDGET CONTRACT: PASS**

**EMPIRICAL GROUPED-vs-SPLIT RETRIEVAL OPTIMUM: NOT YET CALIBRATED**

The deterministic gate passed all 5 frozen planning cases and preserved mandatory high-stakes research routes.

## What is proven

Atomic claim decomposition does not imply one external query per claim.

The planner can distinguish:

- `MUST_RESEARCH`;
- `SHARE_RETRIEVAL_WITH:<claim>`;
- `DERIVE_AFTER_RETRIEVAL`;
- `CLARIFY_FIRST`.

This prevents obvious query explosion while preserving separate downstream claim adjudication.

The gate also proves that cost optimization is subordinate to evidence adequacy: medical/legal must-research claims remain scheduled even when other claims can share retrieval or be derived after retrieval.

## Why this matters

Naive one-query-per-claim planning wastes provider calls, tokens, latency, and human review time. It can also fragment context and create inconsistent source sets for claims that should be adjudicated together.

The opposite failure is over-grouping: one broad query can hide a low-recall subclaim. Therefore the current policy is a routing contract, not a claim that the optimal grouping has already been found.

## Unresolved empirical work

A real calibration needs grouped-vs-split paired retrieval tasks measuring at least:

- authoritative-source recall;
- precision;
- conflict discovery;
- latency;
- provider credits/cost;
- duplicate-result rate;
- evidence coverage per claim;
- downstream citation adequacy.

The stopping rule should be based on remaining evidence gaps and marginal value, not a fixed global query count.

## Red-team

- **Senior researcher:** would reject any cost cap that stops before contradictory or primary evidence is checked.
- **Information-retrieval engineer:** would require empirical recall/precision curves for grouped versus split queries.
- **Evaluation scientist:** would require cost-normalized task utility on hidden holdouts.
- **Security engineer:** would prevent retrieved content from manufacturing new external queries or overriding the pre-retrieval budget.

## Architectural requirement

The trusted planner owns query creation and budget escalation. Retrieved content may suggest evidence gaps but cannot directly create paid/external calls. Any expansion must be authorized against a specific unresolved claim/evidence requirement.
