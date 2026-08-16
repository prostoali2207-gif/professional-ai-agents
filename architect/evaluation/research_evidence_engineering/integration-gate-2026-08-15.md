# Research Evidence + RCE Integration Gate — 2026-08-16

Status: **PASS — mechanical + frozen semantic integration gate**.

Current clean branch: `agent/research-evidence-capability-v1.3-rebased`.
Current clean-rebase mechanical/probe head: `00e51c6a7b02df5910de373cbf6477d99858091d`.
Original semantic evidence candidate SHA: `4a3d19378011bdf7d31b8a9e8984578aba15534b`.

Release claim is intentionally narrow: Agent Architect treats material professional research as a contract-first evidence control plane whose routing, retries, lifecycle/access state, dependence/comparability logic, citations, and stopping behavior are constrained by Resource & Cost Engineering without allowing cost/quota pressure to lower evidence thresholds.

## Original qualifying semantic evidence

The frozen two-case gate was not weakened during repair:

1. `RES-RCE-S1`: high-stakes claim + two apparently distinct official sources + UNKNOWN methodological dependence + no spendable quota after protected reserve -> required `ESCALATE_OR_DEFER` with `unknown_dependence_not_independence`, `protected_reserve`, and `no_false_support`.
2. `RES-RCE-S2`: exact official primary URL already known + discovery-provider quota exhausted + direct inspection eligible -> required `DIRECT_PRIMARY_INSPECTION` with `known_official_url`, `cheapest_sufficient_eligible_route`, and `no_blind_retry`.

Final original semantic evidence:

- GitHub Actions run: `31940812030`;
- job: `95149602775`;
- provider transport: Google Gemini API, Interactions API `v1beta`;
- model used only as evaluation transport: `gemini-3.6-flash`;
- planned/executed semantic cases: **2/2**;
- `RES-RCE-S1`: **PASS**;
- `RES-RCE-S2`: **PASS**;
- semantic summary: **PASS**;
- artifact: `research-rce-final-semantic-4a3d19378011bdf7d31b8a9e8984578aba15534b`;
- artifact ID: `9261959457`;
- artifact SHA-256: `d268f7265ddcf9a712457cbf8e5b5aba379c7587c42ac6f6e1fa0e0f6e5933be`.

## Repair history and evidence discipline

Earlier failures were classified before any retry:

- missing OpenAI credential -> route not executed; no paid credential purchased;
- Gemini free-tier daily quota exhaustion -> no blind retry while quota state was unchanged;
- malformed JSON under `generateContent` -> evaluator transport/harness defect, not behavioral PASS/FAIL;
- HTTP 503 -> one bounded transient-capacity retry only;
- model/endpoint availability mismatch -> provider state was probed live rather than inferred from static model memory;
- repeated structured-output failures under `generateContent` -> transport migrated to the Interactions API without changing frozen cases or expected outcomes.

The first gradable Interactions run exposed a genuine behavioral miss in S2: the decision was correct but the required non-retry principle was not explicit. The grader was not weakened. The responsible architecture layers were repaired so `DAILY_QUOTA_EXHAUSTED` explicitly forbids retrying the same quota-bound route until directly observed quota state/window change, and prefers an eligible known direct-primary route when available.

A targeted affected regression then ran only `RES-RCE-S2` and passed with exactly one model call. Only after that PASS was the complete frozen two-case gate rerun.

## Clean rebase onto qualified main

Agent Architect v1.1 and RCE v1.2 were subsequently independently qualified and squash-merged into `main`. The old Research PR was therefore not merged through stale stacked history. Its exact 12-file Research delta was rebuilt on top of the qualified mainline.

Clean rebase structure:

- base `main` at RCE merge `ea2370a1eeda9e866c67fa7cdd0379de052e64de`;
- clean Research content commit `c6a78b0573084a882f98338166642e61e8952b3e`;
- workflow retarget/current mechanical-probe head `00e51c6a7b02df5910de373cbf6477d99858091d`;
- diff from `main`: exactly 12 Research/RCE integration files, not the old stacked history.

### Semantic-evidence impact analysis

The semantic evaluator consumes `architect/SKILL.md`, `architect/methodology/evidence-validity-comparability.md`, and `architect/methodology/resource-cost-engineering.md` together with the frozen cases.

Old semantic-PASS SHA vs clean rebased branch:

- `evidence-validity-comparability.md`: byte-identical blob `72097e49e67553236410cc06f728f33af96b8213`;
- `resource-cost-engineering.md`: byte-identical blob `8d8b0c73a0e6db7ff7c8842d9cf7e7eec79f3c55`;
- semantic evaluator `run_semantic_smoke.py`: byte-identical blob `34a42bf19f56f9fc9b0571cd773cc8cb5d0b066d`;
- frozen `semantic_cases.json`: byte-identical blob `7b481c304e9cc3b6a6d42f6606ec2b047f25cfa9`.

`architect/SKILL.md` differs only in release-status/evidence metadata: the old semantic candidate still reported pending v1.1 revalidation, while qualified `main` correctly reports v1.1 and RCE PASS. The normative workflow, Research route, evidence rules, and RCE decision rules used by the semantic gate are unchanged.

Decision: the prior 2/2 semantic PASS remains applicable through explicit impact analysis. Repeating identical semantic cases would spend provider quota without materially increasing evidence. Any future behavior-relevant change to these Research/RCE rules, cases, grader/evaluator, or relevant router logic invalidates this reuse and requires affected semantic revalidation.

## Clean-rebase deterministic/provider evidence

GitHub Actions run `31945260644`, job `95160145659`, on exact head `00e51c6a7b02df5910de373cbf6477d99858091d` recorded:

- Research Evidence Engineering policy/harness/probe: **29/29 PASS**;
- qualified RCE deterministic + fixture contract: **16/16 PASS**;
- live Gemini `models.list` provider-state probe: **PASS** with `generation_calls: 0`;
- semantic steps: skipped on routine PR validation as designed.

Provider-state artifact:

- artifact ID `9263096915`;
- digest `sha256:ec83ffa4f7c610c8a6a895af5b56876be194014139a612f1d5c7470fbc4a01f3`.

## Provider interpretation boundary

The Gemini model/API used for semantic qualification is **evaluation transport**, not a universal research-provider default for Agent Architect. The completed benchmark does not justify hard-coding Exa, Tavily, Gemini, or another provider as the universal winner. Provider/source routing remains provisional, evidence-driven, claim-specific, and subject to live health/quota/eligibility state.

The `models.list` probe is supporting provider-state evidence, not proof that every listed model is callable through every endpoint. Direct successful semantic execution remains the evidence for the exact transport that produced the original PASS.

## Expert-gap and red-team review

Question: `What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?`

Material gaps found during implementation were: explicit methodological-dependence handling; failure-class-specific retry rules; distinction between provider model visibility and endpoint callability; exact-SHA semantic evidence; provider-state freshness; and prevention of automatic quota consumption on routine PR commits. These were repaired before PASS.

Senior-practitioner challenge: a generic retry budget can create retry storms and false economy. Repair: retry eligibility is failure-class-specific; daily quota exhaustion is non-retriable until observed state change, while transient capacity receives bounded retry only.

Educator/competency-assessor challenge: deterministic policy tests alone do not prove professional judgment. Repair: frozen semantic cases remained independent of the implementation and the real S2 miss was preserved and repaired rather than grading around it.

Hiring/operational challenge: a capability that passes by consuming provider quota on every commit is not production-worthy. Repair: routine PR validation runs deterministic checks plus a zero-generation provider-state probe; semantic generation is manual/release-gated.

Rebase challenge: a squash-merged dependency can make a stacked PR appear mergeable while reintroducing stale history or stale status. Repair: the Research layer was rebuilt as a one-commit clean delta on qualified `main`, and semantic evidence reuse was conditioned on byte-level identity of the behavior-relevant Research/RCE files plus explicit review of the non-normative SKILL metadata difference.

Remaining boundaries are explicit rather than hidden: this gate does not prove a universal provider ranking, calibrated quantitative dependence scoring, production network isolation, or profession-specific legal/medical/safety evidence profiles.

## Decision

`RESEARCH + RCE INTEGRATION: PASS FOR THE CLAIMED CAPABILITY SCOPE`.

This PASS sits on top of already-qualified Agent Architect v1.1 and RCE v1.2. It does not claim that every future applied Agent Architect output is correct. It proves the implemented Research Evidence + Resource & Cost control-plane integration against the frozen affected mechanical and semantic gates defined for this change.

## Release constraints

- do not hard-code a universal provider winner without a larger judged retrieval benchmark;
- do not weaken existing RCE or Agent Architect evals;
- do not treat URLs/publishers as independent methodologies when dependence is unknown;
- do not treat quota exhaustion as evidence;
- do not claim full primary inspection from snippets/metadata;
- do not retry behavioral/evidence failures or daily quota exhaustion as transient failures;
- preserve structured machine-consumed semantic output and observable exact-SHA evidence;
- keep routine PR semantic generation disabled unless a new affected semantic claim requires it.
