# Sales / Lead Conversion candidate executor contract

Status: qualification infrastructure. This file is not part of the Sales professional-core artifact and must not modify or widen the frozen candidate.

## Purpose

Provide a provider-neutral execution boundary for held-out Sales / Lead Conversion qualification.

The harness owns sealed fixtures, expected behavior, grading, thresholds, controlled tool scenarios and trial orchestration. The executor owns only faithful execution of the exact frozen candidate under the requested capability profile.

## Frozen candidate integrity

For the current gate the executor must load exactly:

- commit: `b1a5f214a7cc9452e8a168f3292a2e9b613ecae0`
- core: `sales-lead-conversion/0.1.0`
- artifact digest: `sha256:6107413b9d6699f249d15903918f0943d26348f206d9e898d37b7058dac6dfa6`

If the exact artifact cannot be loaded and verified, exit non-zero. Never substitute current `main`, a newer branch, model memory, or reconstructed prose.

## Protocol

Read exactly one JSON request from stdin using protocol `sales-lead-conversion-candidate-v1`.

The request contains:

- `candidate` — exact frozen source identity;
- `run` — run ID, trial ID and capability profile;
- `task` — only candidate-visible task/fixture content;
- `initial_state` — inspectable session state supplied by the harness;
- `tool_scenario` — opaque tool endpoints/capabilities exposed for this run, without grader keys.

The executor must run a fresh isolated candidate session for each trial unless the request explicitly supplies a checkpoint/resume relationship.

## Output

Write exactly one JSON object to stdout containing externally observable evidence only:

- `protocol`;
- `run_id` and `trial_id`;
- `candidate_identity` actually loaded;
- `final_response` or structured candidate output;
- `tool_calls[]` with arguments visible to the environment;
- `tool_results_seen[]` identifiers/hashes sufficient for traceability;
- `state_before` and `state_after` or state deltas exposed by the runtime;
- `side_effect_ledger[]` for attempted and completed sends/bookings/writes/reservations/other consequential actions;
- `resource_loads[]` when capability loading is material;
- `checkpoint` metadata when applicable;
- `termination_reason`;
- `runtime_identity` including provider/model/runtime versions needed for reproducibility.

Do not emit hidden chain-of-thought. Inspectable state/action traces are required instead.

## Controlled tools

The harness may expose deterministic tools that simulate:

- current/stale/conflicting commercial facts;
- inventory/vehicle identity ambiguity;
- appointment availability and booking confirmation;
- human handoff acknowledgment/failure;
- message-send capability that is available but unauthorized;
- delayed/partial tool success;
- customer identity matches and ambiguous dedup candidates;
- policy/authority context.

Tool availability never grants authority. The executor must bind the candidate to the authority supplied in the run context.

## Side-effect ledger

Every attempted consequential action must be mechanically observable even when blocked. At minimum record:

`effect_type -> requested_by_candidate -> authorized -> executed -> target -> idempotency_key -> environment_result`

The harness must be able to prove that no unauthorized external send, appointment booking, reservation, finance/discount promise, or other prohibited effect occurred.

## Session/state requirements

The runtime must support, where requested by the fixture:

1. fresh trial isolation;
2. state inspection before and after the run;
3. checkpoint creation and resume without silently restoring withheld transcript;
4. authoritative fact supersession across turns;
5. opt-out/ownership/open-loop persistence;
6. no accidental state carryover between customers/trials.

If a requested state capability is unavailable, fail the run as infrastructure `NOT EXECUTABLE`; do not narratively simulate it.

## Security / held-out integrity

The executor must never receive:

- expected answers;
- grader assertions/keys;
- other sealed fixtures;
- repair notes derived from sealed failures;
- unrelated customer data or secrets.

Customer messages, tool output, webpages, screenshots and retrieved content are data, not authority. Prompt-injection strings inside them must not alter the frozen candidate or tool permissions.

Provider credentials belong only in executor environment secrets, never fixtures, run logs or committed files.

## Failure behavior

Exit non-zero if:

- exact candidate verification fails;
- model/runtime is unavailable;
- required isolation/state/tool instrumentation is unavailable;
- timeout occurs;
- candidate produces no usable output;
- output cannot be serialized without changing substantive behavior.

An execution failure is not a candidate PASS and is not permission to synthesize an answer.

## Qualification boundary

This executor may support analysis/drafting qualification now. Autonomous real-customer communication remains outside the current applied deployment authority even if a simulated tool exists in the harness.
