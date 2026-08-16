# Research Evidence + RCE Integration Gate — 2026-08-16

Status: **PASS — mechanical + frozen semantic integration gate**.

Candidate branch: `agent/research-evidence-capability-v1.3`.
Final steady-state head after cost-control cleanup: `be4bc686881dcdbb37c4b1b75e4847d58e2c9432`.
Semantic evidence candidate SHA: `4a3d19378011bdf7d31b8a9e8984578aba15534b`.

Release claim is intentionally narrow: Agent Architect treats material professional research as a contract-first evidence control plane whose routing, retries and stopping behavior are constrained by Resource & Cost Engineering without allowing cost/quota pressure to lower evidence thresholds.

## Deterministic evidence

The exact-candidate GitHub Actions preflight on the semantic-PASS line completed successfully:

- Research Evidence Engineering policy/harness/probe suite: **29/29 PASS**;
- existing Resource & Cost Engineering deterministic + fixture contract: **16/16 PASS**;
- live Gemini `models.list` provider-state probe: PASS with `generation_calls: 0`.

After semantic validation, the workflow was returned to manual-semantic mode. The final steady-state head `be4bc686...` completed its PR gate successfully with deterministic checks and the zero-generation provider-state probe; semantic calls were skipped as designed.

The compare `4a3d193... -> be4bc686...` contains exactly one changed file: `.github/workflows/architect-research-rce-semantic-smoke.yml`. No methodology, frozen case, grader, policy, or semantic harness changed after the semantic PASS; only the CI trigger was returned from automatic semantic execution to manual semantic execution.

## Frozen semantic gate

The frozen two-case gate was not weakened during repair:

1. `RES-RCE-S1`: high-stakes claim + two apparently distinct official sources + UNKNOWN methodological dependence + no spendable quota after protected reserve -> required `ESCALATE_OR_DEFER` with `unknown_dependence_not_independence`, `protected_reserve`, and `no_false_support`.
2. `RES-RCE-S2`: exact official primary URL already known + discovery-provider quota exhausted + direct inspection eligible -> required `DIRECT_PRIMARY_INSPECTION` with `known_official_url`, `cheapest_sufficient_eligible_route`, and `no_blind_retry`.

### Final semantic evidence

GitHub Actions run: `31940812030`.
Job: `95149602775`.
Provider transport: Google Gemini API, Interactions API `v1beta`.
Model used as evaluation transport: `gemini-3.6-flash`.
Planned/executed semantic cases: **2/2**.

Results:

- `RES-RCE-S1`: **PASS** — actual decision `ESCALATE_OR_DEFER`; all required rationale codes present.
- `RES-RCE-S2`: **PASS** — actual decision `DIRECT_PRIMARY_INSPECTION`; all required rationale codes present, including `no_blind_retry`.
- semantic summary: **PASS**.

Semantic artifact: `research-rce-final-semantic-4a3d19378011bdf7d31b8a9e8984578aba15534b`.
Artifact ID: `9261959457`.
Artifact SHA-256: `d268f7265ddcf9a712457cbf8e5b5aba379c7587c42ac6f6e1fa0e0f6e5933be`.

## Repair history and evidence discipline

Earlier failures were classified before any retry:

- missing OpenAI credential -> route not executed; no paid credential purchased;
- Gemini free-tier daily quota exhaustion -> no blind retry while quota state was unchanged;
- malformed JSON under `generateContent` -> evaluator transport/harness defect, not behavioral PASS/FAIL;
- HTTP 503 -> one bounded transient-capacity retry only;
- model/endpoint availability mismatch -> provider state was probed live rather than inferred from static model memory;
- repeated structured-output failures under `generateContent` -> transport migrated to the documented Interactions API without changing frozen cases or expected outcomes.

The first gradable Interactions run exposed a genuine behavioral miss in S2: the decision was correct but the required non-retry principle was not explicit. The grader was not weakened. The responsible architecture layers were repaired so `DAILY_QUOTA_EXHAUSTED` explicitly forbids retrying the same quota-bound route until directly observed quota state/window change, and prefers an eligible known direct-primary route when available.

A targeted affected regression then ran only `RES-RCE-S2` (`SEMANTIC_CASE_IDS=RES-RCE-S2`) and passed with exactly one model call. Only after that PASS was the complete frozen two-case gate rerun.

## Provider interpretation boundary

The Gemini model/API above is **evaluation transport**, not a universal research-provider default for Agent Architect. The completed benchmark does not justify hard-coding Exa, Tavily, Gemini, or another provider as the universal winner. Provider/source routing remains provisional, evidence-driven, claim-specific, and subject to live health/quota/eligibility state.

The `models.list` probe is supporting provider-state evidence, not proof that every listed model is callable through every endpoint. The successful Interactions semantic run is the direct evidence for eligibility of the exact evaluation transport used here.

## Expert-gap and red-team review

Question: `What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?`

The material gaps found during implementation were: explicit methodological-dependence handling; failure-class-specific retry rules; distinction between provider model visibility and endpoint callability; exact-SHA semantic evidence; and prevention of automatic quota consumption on routine PR commits. These were repaired before PASS.

Senior-practitioner challenge: a generic retry budget can create retry storms and false economy. Repair: retry eligibility is now failure-class-specific; daily quota exhaustion is non-retriable until observed state change, while transient capacity receives bounded retry only.

Educator/competency-assessor challenge: deterministic policy tests alone do not prove professional judgment. Repair: frozen semantic cases remained independent of the implementation and were required to pass through an external model transport; the real S2 miss was preserved and repaired rather than grading around it.

Hiring/operational challenge: a capability that passes by consuming provider quota on every commit is not production-worthy. Repair: steady-state PR validation runs deterministic checks plus a zero-generation live model probe; semantic generation is manual/release-gated.

Remaining boundaries are explicit rather than hidden: this gate does not prove a universal provider ranking, calibrated quantitative dependence scoring, production network isolation, or profession-specific legal/medical/safety evidence profiles.

## Decision

`RESEARCH + RCE INTEGRATION: PASS FOR THE CLAIMED CAPABILITY SCOPE`.

This PASS does not alter or qualify PR #1 and does not claim that every future applied Agent Architect output is correct. It proves the implemented Research Evidence + Resource & Cost control-plane integration against the frozen affected mechanical and semantic gates defined for this change.

## Release constraints

- do not hard-code a universal provider winner without a larger judged retrieval benchmark;
- do not weaken existing RCE or Agent Architect evals;
- do not treat URLs/publishers as independent methodologies when dependence is unknown;
- do not treat quota exhaustion as evidence;
- do not claim full primary inspection from snippets/metadata;
- do not retry behavioral/evidence failures or daily quota exhaustion as transient failures;
- preserve structured machine-consumed semantic output and observable exact-SHA evidence;
- keep routine PR semantic generation disabled unless a new affected semantic claim requires it.
