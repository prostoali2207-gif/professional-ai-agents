# Research Evidence Engineering Evaluation

This directory contains the deterministic policy surface for the Agent Architect research-evidence capability introduced from the completed August 2026 Research Architecture benchmark.

## What is mechanically tested

`test_research_policy.py` covers:

- required research-contract fields and stopping criteria;
- no paid/external route without a concrete evidence gap;
- direct-primary routing when a known official URL exists;
- protected external-call reserve;
- access-state honesty (`SNIPPET_ONLY` cannot support a material claim);
- lifecycle invalidation for superseded evidence;
- non-comparability blocking aggregation;
- claim/citation entailment conflict preservation;
- source-lineage and methodological-dependence controls;
- fail-closed behavior when dependence is unknown;
- bounded retry taxonomy for capacity/rate/provider failures;
- no blind retry for behavioral failure, quota exhaustion, auth/config, or retired models;
- stopping, clarification, continuation, and escalation/defer behavior;
- budget exhaustion never converting an unresolved high-stakes claim into PASS.

## Scope

These tests validate deterministic policy invariants only. They do not prove retrieval recall, provider superiority, semantic decomposition quality, production network isolation, or domain-specific high-stakes evidence sufficiency.

The completed research benchmark remains the evidence basis for the architecture. Provider assignments are intentionally not hard-coded as universal defaults because the benchmark itself states that the retrieval pilot is too small for population-level provider ranking.

## Coupling with Resource & Cost Engineering

The research router consumes budget/quota/provider-health/protected-reserve information as control-plane inputs. The broader RCE policy remains in `../resource_cost_engineering/` and `../../methodology/resource-cost-engineering.md`.

Research-specific resource invariant:

`concrete evidence gap + eligible route + expected decision value + available spendable budget -> route; otherwise stop/defer/escalate`

This prevents both research underreach and search/query explosion.

## Required next validation

Before declaring the integrated capability release-ready:

1. run this deterministic suite together with the existing RCE deterministic suite;
2. run a small frozen semantic integration set that requires claim decomposition, routing, lifecycle/dependence reasoning, citation status, and stopping under quota pressure;
3. preserve the existing Agent Architect release gates; do not weaken or replace them;
4. do not hard-code provider defaults until a larger frozen judged retrieval benchmark establishes them.
