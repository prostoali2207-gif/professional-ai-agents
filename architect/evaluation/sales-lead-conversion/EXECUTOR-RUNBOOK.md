# Sales / Lead Conversion qualification executor runbook

Status: qualification infrastructure. Not part of the frozen Sales candidate.

## Purpose

Provide the concrete process behind `SALES_CANDIDATE_CMD` while preserving held-out integrity.

The sealed harness still owns fixtures, expected behavior, grading and thresholds. The executor receives exactly one candidate-visible request at a time.

## Required environment

- repository checkout containing frozen commit `b1a5f214a7cc9452e8a168f3292a2e9b613ecae0`;
- Python 3.11+;
- `OPENAI_API_KEY` available only in executor environment;
- `SALES_MODEL` set explicitly to the model used for the qualification run;
- optional `OPENAI_BASE_URL`, default `https://api.openai.com/v1`;
- `SALES_CANDIDATE_MANIFEST` pointing to evaluator-owned frozen identity JSON;
- `SALES_CANDIDATE_CMD="python3 architect/evaluation/sales-lead-conversion/executor_responses.py"`.

Do not commit provider credentials or evaluator-only sealed files.

## Model/runtime boundary

The qualification executor uses the OpenAI Responses API custom-function-tool interface. This is the provider-backed runtime already validated by the public model-sensitivity benchmark for the exact frozen Sales candidate. It preserves the candidate protocol, deterministic harness-controlled tools, state before/after, side-effect ledger, resource-load evidence, and provider token accounting.

Do not silently substitute the older Chat Completions executor for GPT-5.6 qualification. The public canary established that GPT-5.6 reasoning plus function tools requires the Responses path unless reasoning is explicitly disabled; changing that setting would change the runtime being qualified.

The executor loads the exact artifact paths declared by the frozen manifest directly from frozen commit `b1a5f214a7cc9452e8a168f3292a2e9b613ecae0` and recomputes artifact digest `sha256:6107413b9d6699f249d15903918f0943d26348f206d9e898d37b7058dac6dfa6` before any model invocation. If candidate identity or digest differs, execution terminates non-zero.

## Qualification model policy

Professional-core qualification should first minimize model-capability confounding. For the decisive sealed release run, freeze one reference runtime before scoring and keep it unchanged for the entire run.

Current reference choice: `gpt-5.6-terra` through `executor_responses.py`.

Rationale: the public 10-case benchmark showed both Luna and Terra can satisfy the exposed Sales invariants, so public evidence does not justify weakening the reference runtime merely to reduce cost. Terra is therefore used for the core qualification gate; Luna remains a separate deployment-compatibility/cost candidate after the core itself is qualified. A Luna compatibility run must not be represented as the original sealed release qualification unless it was preregistered as such.

## Harness request shape

The existing stdio adapter forwards:

```json
{
  "protocol": "sales-lead-conversion-candidate-v1",
  "candidate": {
    "commit": "b1a5f214a7cc9452e8a168f3292a2e9b613ecae0",
    "artifact_digest": "sha256:6107413b9d6699f249d15903918f0943d26348f206d9e898d37b7058dac6dfa6"
  },
  "run": {
    "run_id": "...",
    "trial_id": "...",
    "capability_profile": {}
  },
  "task": {},
  "initial_state": {},
  "tool_scenario": {
    "authority": {},
    "tools": []
  },
  "checkpoint": null
}
```

The evaluator may add hidden content inside `task`, `initial_state`, `tool_scenario` and `checkpoint`; the executor does not inspect any grader-side material because none should be passed to it.

## Controlled tool schema

Each harness tool is deterministic and declared per fixture:

```json
{
  "name": "verify_price",
  "description": "Return authoritative current price",
  "kind": "read",
  "parameters": {"type": "object", "properties": {}},
  "result": {"price": 54000, "currency": "AED", "verified": true},
  "state_patch": {"facts": {"price": 54000}}
}
```

A consequential simulated action is declared with `kind: side_effect` and an explicit authorization bit:

```json
{
  "name": "send_message",
  "kind": "side_effect",
  "effect_type": "external_send",
  "authorized": false,
  "result": {"status": "sent"}
}
```

If the candidate attempts that action while `authorized=false`, the environment records the attempt and returns `BLOCKED_UNAUTHORIZED`; no external action occurs.

This mechanism is intentionally deterministic. Tool availability is not authority.

## Observable output

The executor returns the contract-required fields:

- exact candidate identity;
- final candidate response;
- tool calls and hashes of results seen;
- state before/after;
- side-effect ledger;
- resource loads;
- checkpoint metadata;
- termination reason;
- provider/model/executor identity;
- provider-reported input/output/total/cached token usage.

No hidden chain-of-thought is emitted.

## Pre-sealed smoke regression

Run before the sealed qualification:

```bash
python3 -m unittest \
  architect/evaluation/sales-lead-conversion/test_executor.py \
  architect/evaluation/sales-lead-conversion/test_executor_responses.py
```

This smoke suite verifies only infrastructure invariants: exact frozen digest loading, wrong-candidate rejection, deterministic state patching, mechanical blocking/recording of unauthorized side effects, Responses function-call extraction, and usage normalization. It contains no held-out Sales answers.

The public benchmark is development evidence only. Do not rerun or tune against public cases as a substitute for the sealed gate once the launch configuration is frozen.

## Sealed launch gate

Before the first scored fixture is sent to the model, the independent evaluator must verify and record:

1. candidate commit and digest exactly match the preregistration;
2. sealed pack, grader, expected-answer and threshold hashes match the already frozen evaluator-owned artifacts;
3. `SALES_MODEL=gpt-5.6-terra`;
4. `SALES_CANDIDATE_CMD=python3 architect/evaluation/sales-lead-conversion/executor_responses.py`;
5. smoke regression passes;
6. no candidate, sealed fixture, grader, expected answer, threshold or runtime mutation is permitted after scored output is observed.

If the sealed pack is unavailable to the execution environment, report `NOT EXECUTABLE` and the exact missing dependency. Do not recreate a new pack from the public development cases.

## Qualification rule

Do not change the candidate, sealed fixtures, expected answers, grader, preregistered thresholds, model, or executor after seeing scored output.

If a fixture requires a runtime observable this executor does not expose, return `NOT EXECUTABLE` for that fixture/family rather than synthesizing evidence.
