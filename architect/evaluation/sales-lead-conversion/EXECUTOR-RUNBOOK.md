# Sales / Lead Conversion qualification executor runbook

Status: qualification infrastructure. Not part of the frozen Sales candidate.

## Purpose

Provide the missing concrete process behind `SALES_CANDIDATE_CMD` while preserving held-out integrity.

The sealed harness still owns fixtures, expected behavior, grading and thresholds. This executor receives exactly one candidate-visible request at a time.

## Required environment

- repository checkout containing frozen commit `b1a5f214a7cc9452e8a168f3292a2e9b613ecae0`;
- Python 3.11+;
- `OPENAI_API_KEY` available only in executor environment;
- `SALES_MODEL` set explicitly to the model/snapshot used for the qualification run;
- optional `OPENAI_BASE_URL`, default `https://api.openai.com/v1`;
- `SALES_CANDIDATE_MANIFEST` pointing to evaluator-owned frozen identity JSON;
- `SALES_CANDIDATE_CMD="python3 architect/evaluation/sales-lead-conversion/executor.py"`.

Do not commit provider credentials or evaluator-only sealed files.

## Model/runtime boundary

The executor uses the Chat Completions function-tool interface. It loads the exact artifact paths declared by the frozen manifest directly from the frozen Git commit and recomputes the artifact digest before any model invocation.

If candidate identity or digest differs, execution terminates non-zero.

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
- provider/model/executor identity.

No hidden chain-of-thought is emitted.

## Smoke regression

Run before sealed qualification:

```bash
python3 -m unittest architect/evaluation/sales-lead-conversion/test_executor.py
```

This smoke suite verifies only infrastructure invariants: exact frozen digest loading, wrong-candidate rejection, deterministic state patching and mechanical blocking/recording of unauthorized side effects. It contains no held-out Sales answers.

## Qualification rule

Do not change the candidate, sealed fixtures, expected answers, grader or preregistered thresholds after seeing scored output.

If a fixture requires a runtime observable this executor does not expose, return `NOT EXECUTABLE` for that fixture/family rather than synthesizing evidence.
