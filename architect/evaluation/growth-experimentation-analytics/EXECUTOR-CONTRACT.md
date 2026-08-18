# Analytics candidate executor contract

The evaluation harness is provider-neutral. A candidate executor is a small program outside the grader that binds the exact frozen Analytics instructions to one eligible model/runtime.

## Input

Read exactly one JSON object from stdin using protocol `growth-experimentation-analytics-candidate-v1`.

The envelope contains:
- `candidate` — frozen source identity;
- `task.instruction` — execution instruction;
- `task.fixture` — the candidate-facing experiment case.

The executor must fetch/load and bind the exact candidate instructions identified by the manifest. If the exact source cannot be obtained or verified, fail; do not substitute a newer file.

## Output

Write exactly one JSON object to stdout matching `schemas/candidate-output.schema.json`.

No Markdown fences, explanations outside JSON, grader answers, or hidden state.

## Security / eval integrity

The executor must not receive:
- expected answers or deterministic grader assertions;
- sealed held-out fixtures other than the single case being executed;
- repair notes based on sealed failures;
- unrelated customer data or secrets.

Provider credentials belong in the executor environment, never fixtures, manifests, run logs, or committed files.

## Failure behavior

Exit non-zero if:
- model/runtime is unavailable;
- candidate instructions cannot be loaded exactly;
- timeout occurs;
- the model returns no usable result;
- output cannot be normalized to the required JSON without changing its substantive decision.

The adapter/harness treats execution failure as a failed run, not as an opportunity to synthesize a plausible answer.

## Why this boundary exists

The professional core should not depend on OpenAI, Anthropic, or any other single model provider. Qualification concerns the assembled candidate under a recorded runtime. The same harness can therefore compare runtimes or rerun regressions without rewriting fixtures or graders.
