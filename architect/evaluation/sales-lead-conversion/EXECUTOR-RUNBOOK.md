# Sales / Lead Conversion qualification executor runbook

Status: qualification infrastructure. Not part of the frozen Sales candidate.

## Purpose

Provide the concrete process behind the Sales qualification runtime while preserving held-out integrity.

The evaluator-owned sealed harness owns fixtures, expected behavior, grading and thresholds. The executor receives exactly one candidate-visible request at a time.

## Frozen target

- candidate commit: `b1a5f214a7cc9452e8a168f3292a2e9b613ecae0`
- candidate digest: `sha256:6107413b9d6699f249d15903918f0943d26348f206d9e898d37b7058dac6dfa6`
- reference runtime: OpenAI Responses API via `executor_responses.py`
- reference model for the scored run: `gpt-5.6-terra`

## Required environment

- repository checkout containing the frozen candidate commit;
- Python 3.11+;
- `OPENAI_API_KEY` available only in executor environment;
- `SALES_MODEL` set explicitly;
- optional `OPENAI_BASE_URL`, default `https://api.openai.com/v1`.

Do not commit provider credentials or plaintext evaluator-only sealed files.

## Model/runtime boundary

The qualification executor uses the OpenAI Responses API custom-function-tool interface. It loads the exact artifact paths declared by the frozen manifest directly from the frozen Git commit and recomputes the artifact digest before any model invocation. If candidate identity or digest differs, execution terminates non-zero.

## Fresh sealed cycle (2026-08-21)

The original evaluator-owned 45-fixture pack became non-recoverable and was invalidated as future release evidence. A fresh post-freeze cycle was created against the unchanged candidate.

Public repository storage contains only an authenticated encrypted pack:

`architect/evaluation/sales-lead-conversion/sealed/fresh-cycle-2026-08-21.pack.fernet`

The plaintext fixtures, grader and runner are not committed. The ciphertext is decrypted only inside the manual GitHub Actions run by `.github/workflows/sales-fresh-sealed-qualification.yml` using repository secret `SALES_SEALED_PACK_KEY`.

Frozen evaluator references before any scored call:

- 45 fixtures, 15 required families, 3 trials/family;
- 3 restart/stateful sequence fixtures in the state-supersession family;
- sealed pack digest: `sha256:ae91ccef4bc48905c1970629a6ff8920e12d95db31b4d11b2325c691f0ad68d8`;
- encrypted ciphertext digest: `sha256:5a0dc49630cb0c8d75d7f6550b2ac04993121fad93f46cce338c38c1195fef62`;
- decrypted ZIP digest: `sha256:11ae925d27d90e94ed7432ed481ee996b2921bd17c792922e7a2ccf13e2d24ab`;
- fixtures digest: `sha256:c81d2ab8cf6dc9c0bb66299ff42dbc10bbb9a3102fce873e449ce0379c9c3ce0`;
- grader digest: `sha256:80aa871f81951348f332061f8cd2b4ebabe98592754d8d346b1dae213e1eb9a0`;
- runner digest: `sha256:4e80d6b8e5e18e57b6c5bf32fe0b14568e2b61f8caa2b544de59cae8f97f50b8`.

The workflow verifies ciphertext, decrypted ZIP and pack freeze digests before the first model call. The evaluator secret is used only during the decryption step; candidate runtime receives only candidate-visible task/state/tool/authority data.

### Scored-run stop policy

Before scoring, the stop condition is frozen as follows: if a critical hard-fail is observed, the release verdict is already `REVISE`, so the runner stops rather than spending remaining API quota merely to reconfirm a failed release gate. Runtime failure yields `NOT_EXECUTABLE`. Otherwise all 45 fixtures execute.

## Harness request shape

The executor receives:

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

The evaluator may add hidden content inside `task`, `initial_state`, `tool_scenario` and `checkpoint`; grader-side expectations are never passed to the executor.

## Controlled tools and observables

Each harness tool is deterministic and declared per fixture. Consequential simulated actions carry an explicit authorization bit. If a candidate attempts an unauthorized side effect, the environment records the attempt and blocks the external action. Tool availability is not authority.

The executor returns exact candidate identity, final response, tool calls, hashes of tool results seen, state before/after, side-effect ledger, resource loads, checkpoint metadata, termination reason, provider/model/executor identity and provider-reported token usage. No hidden chain-of-thought is emitted.

## Qualification rule

Do not change the candidate, sealed fixtures, grader, thresholds, runtime/model identity or stop policy after seeing scored output. Any behavior-relevant candidate repair after scored output requires a new held-out cycle.

If a fixture requires a runtime observable that cannot be exposed, return `NOT EXECUTABLE` rather than synthesizing evidence.
