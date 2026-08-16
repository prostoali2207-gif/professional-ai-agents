# Resource & Cost Engineering — v1.2 integration validation

Date: 2026-08-16
Candidate branch: `candidate/architect-rce-v1.2-rebased`
Qualifying candidate SHA: `d0d5b4fcc7613c1139acfbb190d1020cce5f783d`

## Verdict

`RCE v1.2 INTEGRATION: PASS`

Scope: the Resource & Cost Engineering capability routed by Agent Architect, as exercised by the deterministic RCE-B1–B12 checks and the frozen semantic/adversarial RCE-S1–S10 release gate.

This PASS does not make volatile provider prices/quotas durable truth, does not establish a universal provider/model default, and does not transfer automatically to applied agents.

## Integration surface

- `architect/SKILL.md` routes materially expensive/quota-sensitive workflows through `methodology/resource-cost-engineering.md`.
- RCE evaluation artifacts live under `architect/evaluation/resource_cost_engineering/`.
- Exact provider pricing is not embedded as durable routing knowledge.
- Semantic expectations stay grader-side; candidate-visible inputs contain case facts and frozen Agent Architect/RCE instructions, not required decisions.
- Provider/model selection remains an evaluation transport choice, not a universal RCE policy.

## Deterministic gate

The rebased candidate was checked in GitHub Actions with the standard-library RCE suite:

`Ran 16 tests ... OK`

Coverage includes:

- RCE-B1–B12 deterministic budget/accounting behavior;
- exact RCE-S1–S10 semantic fixture set and required fields;
- no embedded named-provider price-memory table in semantic fixtures;
- coverage of the expected false-economy decision classes.

The mechanical gate explicitly records `model/API generation calls = 0`.

## Semantic harness qualification

The original smoke harness bound a no-tool decision case to the general protocol-v2 tool adapter while setting `max_tool_rounds=0`. On the first attempted RCE-S1 call, the model selected an available tool and the adapter correctly stopped with `tool-round budget exhausted`.

That result was classified as **harness/transport failure, not behavioral FAIL**. RCE-S2 was not executed in that attempt. The grader, frozen cases, and expected decisions were not weakened.

The evaluator was repaired by using a tool-free Gemini Interactions request with schema-bound JSON output. It loads only the frozen candidate instruction sources (`architect/SKILL.md` and `architect/methodology/resource-cost-engineering.md`) plus candidate-visible case facts; required decisions and required rationale codes remain grader-side.

A corrected bounded smoke then executed exactly RCE-S1 and RCE-S2:

- RCE-S1: PASS — `STRONG_DIRECT`, with `quality_floor` and `empirical_task_performance`;
- RCE-S2: PASS — `REJECT_CACHE_AND_RESEARCH`, with required `scope_compatibility`;
- planned model calls: 2;
- executed cases: 2;
- application retries: 0.

Smoke evidence:

- candidate SHA: `a92b05281f1dfe9e4cc697fa70391b19347357f2`;
- workflow run: `31944674223`;
- job: `95158762226`;
- artifact ID: `9262949634`;
- artifact digest: `sha256:1aaa826d3e5d2e0adcbcc88d4f062b414149b4842b7a056361f68f842e8f4844`.

## Full frozen RCE-S1–S10 release gate

Only after the corrected minimal smoke passed, the integration gate widened to all ten preregistered P0 semantic/adversarial cases.

Execution policy:

- exact PR-head checkout;
- deterministic 16-test preflight before model use;
- live `models.list` eligibility probe with zero generation calls;
- `gemini-3.5-flash-lite`, `medium` thinking as the evaluation transport;
- one model invocation per frozen case;
- 13-second pacing between cases to reduce RPM pressure;
- zero application retries;
- immediate non-PASS on behavioral, harness, or provider failure;
- mechanical aggregation requires every RCE-S1–S10 result to be PASS.

Result:

`RCE-S1 ... RCE-S10: 10/10 PASS`

The final mechanical aggregator recorded:

`{"release_gate":"PASS","passes":10,"planned_model_calls":10,"application_retries":0}`

Qualifying evidence:

- candidate SHA: `d0d5b4fcc7613c1139acfbb190d1020cce5f783d`;
- workflow: `Agent Architect RCE Semantic Release Gate`;
- workflow run: `31944762944`;
- job: `95158971938`;
- artifact: `rce-semantic-release-d0d5b4fcc7613c1139acfbb190d1020cce5f783d`;
- artifact ID: `9262997828`;
- artifact digest: `sha256:75164af32dfe077b72d225b91e141d875cea7c8ba70b7c8cc5bc8a51a50c2a96`.

All ten cases matched their preregistered required decisions and required rationale codes. No case used an application retry.

## Resource accounting

The full 10-case release run made exactly 10 semantic model calls. Provider-reported total token usage across those ten calls was 73,624 tokens, including 66,804 input tokens. The run used no tool-use tokens.

The earlier corrected 2-case smoke used two additional successful calls. One earlier RCE-S1 call was spent discovering the `max_tool_rounds=0` harness mismatch; that call did not count as behavioral evidence.

The full release run was required independent integration evidence and is therefore not classified as waste merely because the smaller smoke had already passed.

Public Gemini documentation indicates a Standard Free Tier exists for `gemini-3.5-flash-lite`, but this validation does not infer the repository project's exact billing tier or remaining account quota from public pricing. Active project limits remain live provider/account state.

## Post-PASS operational state

After the qualifying SHA, automatic semantic release triggering was returned to `workflow_dispatch`/manual-only so ordinary commits cannot consume model quota. That operational trigger change does not alter the RCE methodology, frozen cases, grader predicates, or qualifying evaluator logic.

A new semantic release run is required when a behavior-relevant RCE instruction, semantic fixture/expectation, grader, or evaluator change can affect the qualified claim. Documentation-only or CI-trigger-only changes require impact analysis but do not mechanically invalidate the qualifying behavior.

## Release boundary

The PASS proves the current RCE integration against the specified deterministic and semantic gates. It does not prove that every future resource/cost decision is optimal, that current provider pricing/quota remains unchanged, or that cheapest/free routes should be preferred. Eligibility, evidence quality, risk, protected reserve, stopping criteria, and live provider/account state remain first-class constraints.
