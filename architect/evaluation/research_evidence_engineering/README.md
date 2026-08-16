# Research Evidence Engineering Evaluation

Status: **Research + RCE integration PASS for the claimed capability scope**.

This directory contains the policy, provider-state probe, frozen semantic cases, and evidence for the Agent Architect research-evidence capability introduced from the completed August 2026 Research Architecture benchmark.

## What is mechanically tested

`test_research_policy.py`, `test_semantic_cases.py`, and `test_model_probe.py` cover:

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
- budget exhaustion never converting an unresolved high-stakes claim into PASS;
- provider probe parsing/classification without generation;
- exact frozen Research+RCE semantic case contract.

Current clean-rebase PR validation on head `00e51c6a7b02df5910de373cbf6477d99858091d` recorded:

- Research Evidence Engineering/harness/probe: **29/29 PASS**;
- qualified RCE deterministic/fixture contract: **16/16 PASS**;
- live `models.list` probe: **PASS** with `generation_calls: 0`;
- semantic generation: skipped on routine PR validation as designed.

## Semantic integration evidence

The qualifying frozen two-case gate remains:

- `RES-RCE-S1`: **PASS** — `ESCALATE_OR_DEFER`, preserving high-stakes uncertainty, protected reserve, and unknown methodological dependence;
- `RES-RCE-S2`: **PASS** — `DIRECT_PRIMARY_INSPECTION`, including explicit `no_blind_retry` after discovery-provider quota exhaustion.

Qualifying semantic candidate SHA: `4a3d19378011bdf7d31b8a9e8984578aba15534b`.

Evidence:

- workflow run `31940812030`;
- job `95149602775`;
- artifact ID `9261959457`;
- artifact digest `sha256:d268f7265ddcf9a712457cbf8e5b5aba379c7587c42ac6f6e1fa0e0f6e5933be`.

The first gradable S2 run exposed a genuine behavioral miss: the route choice was correct but the required non-retry principle was absent. The frozen grader was not weakened. The responsible Research/RCE methodology was repaired, a one-case affected S2 regression passed, and only then did the complete two-case frozen gate pass.

## Rebase evidence reuse

After Agent Architect v1.1 and RCE v1.2 were independently qualified and squash-merged into `main`, the Research delta was rebuilt cleanly on top of that qualified mainline.

Impact analysis compares the old semantic-PASS candidate with the clean rebased branch:

- `architect/methodology/evidence-validity-comparability.md`: byte-identical blob `72097e49e67553236410cc06f728f33af96b8213`;
- `architect/methodology/resource-cost-engineering.md`: byte-identical blob `8d8b0c73a0e6db7ff7c8842d9cf7e7eec79f3c55`;
- `run_semantic_smoke.py`: byte-identical blob `34a42bf19f56f9fc9b0571cd773cc8cb5d0b066d`;
- `semantic_cases.json`: byte-identical blob `7b481c304e9cc3b6a6d42f6606ec2b047f25cfa9`.

`architect/SKILL.md` differs only in release-status/evidence metadata: the old candidate still said v1.1 revalidation was pending, while current `main` correctly records the already-proven v1.1 and RCE PASS states. No normative Research/RCE decision rule changed.

Therefore the prior semantic PASS remains applicable by impact analysis; rerunning the same two model calls would add no material evidence and is intentionally avoided. A behavior-relevant change to the Research/RCE methodology, frozen cases, grader/evaluator, or relevant router rules would require affected semantic revalidation.

## Scope

This PASS proves the specified Research Evidence + RCE control-plane integration. It does not prove retrieval recall across every domain, provider superiority, calibrated quantitative methodological-dependence probabilities, full production network isolation, or profession-specific legal/medical/safety evidence sufficiency.

The completed research benchmark remains the evidence basis for the architecture. Provider assignments are intentionally not hard-coded as universal defaults because the benchmark does not justify a population-level universal provider ranking.

## Coupling with Resource & Cost Engineering

The research router consumes budget/quota/provider-health/protected-reserve information as control-plane inputs. The broader qualified RCE policy remains in `../resource_cost_engineering/` and `../../methodology/resource-cost-engineering.md`.

Research-specific resource invariant:

`concrete evidence gap + eligible route + expected decision value + available spendable budget -> route; otherwise stop/defer/escalate`

This prevents both research underreach and search/query explosion.

## Operational rule

Routine PR validation runs deterministic Research/RCE checks and a zero-generation live provider-state probe. Semantic generation remains manual/release-gated so ordinary commits do not consume model quota.

Canonical evidence and repair history: `integration-gate-2026-08-15.md`.
