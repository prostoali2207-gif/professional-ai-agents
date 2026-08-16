# Tool and Agent-Computer-Interface Engineering

Status: v0.2.

## Principle

Tool access is not enough. A professional agent needs an interface that exposes the information required for correct decisions, supports diagnosis/recovery, and makes consequential state observable.

Open-source engineering agents such as SWE-agent provide concrete evidence that tool/interface design can materially change end-agent performance: observation size, edit feedback, search output, and explicit success/failure signals affect whether the agent can act competently. Therefore evaluate the interface together with the model, not as neutral plumbing.

## Tool capability model

For every tool define:

- professional purpose;
- typed/structured inputs and validation where feasible;
- observable state;
- actions available;
- hidden state / blind spots;
- preconditions;
- side effects;
- reversibility;
- idempotency or duplicate-action risk;
- atomicity/partial-success semantics where relevant;
- timeout/retry semantics;
- failure/error taxonomy;
- evidence returned after action;
- stable machine-observable success criteria where feasible;
- latency/cost/tool-call budget;
- permission/safety boundary;
- version/runtime assumptions.

## Interface quality questions

Ask whether the interface lets the agent:

1. perceive the state needed for the decision;
2. distinguish success from apparent success;
3. diagnose failure rather than merely receive `error`;
4. distinguish transient failure from invalid input, permission failure, stale state, and partial success;
5. recover, retry safely, roll back, or escalate;
6. preserve provenance of observations/actions;
7. avoid destructive actions when a read/check is sufficient;
8. verify downstream effects;
9. avoid drowning decision-relevant evidence in raw telemetry;
10. know when repeating an action is unsafe or useless.

## Observation design

More tool output is not automatically better. Design observations around the decisions the agent must make.

Prefer:

- bounded, navigable views over uncontrolled dumps;
- explicit empty-result vs tool-failure distinction;
- identifiers/state versions needed for subsequent actions;
- structured errors when the failure class matters;
- direct evidence of what changed after write actions;
- links/references back to full evidence when compact summaries are used.

Do not hide information needed for expert diagnosis merely to save tokens.

## Situation awareness

For consequential workflows, evaluate whether the agent can maintain:

- what is true now;
- what changed;
- what remains uncertain;
- what action has already been taken;
- what downstream state should now exist;
- what anomaly would indicate failure.

Use `runtime-state-memory-context.md` when this state must persist across turns or sessions.

## Error-support requirement

Interfaces should support professional diagnosis and correction. A tool that returns only a generic failure message may prevent expert behavior even if the underlying model knows how to diagnose the problem.

For write-capable tools, explicitly model:

`request -> accepted/rejected -> side effect state -> confirmation evidence -> downstream verification`.

A transport-level 200/success message is not sufficient when the professional claim concerns persisted or downstream state.

## Retry, idempotency, and partial success

Before allowing automated retry determine:

- whether the operation is idempotent;
- whether a prior attempt may have partially succeeded;
- how duplicate side effects are detected/prevented;
- how state is reconciled after timeout/unknown result;
- maximum retry/backoff policy;
- escalation condition.

Do not blindly retry money movement, sends/publishes, destructive operations, deployments, or other non-idempotent actions.

Use `execution-control-and-remediation.md` for the runtime decision policy.

## Human oversight

Where a human is the escalation or approval boundary, the handoff should expose decision-relevant evidence, uncertainty, consequences, and available alternatives. Do not require the human to reconstruct the agent's hidden state from a vague summary.

## Interface ablation

When tool-interface design is consequential, compare plausible interface variants on representative tasks rather than assuming one schema is good because it looks clean.

Possible measures:

- task success/reliability;
- tool misuse/error rate;
- unnecessary action count;
- recovery time/steps;
- context/token load;
- latency/cost;
- failure-class detectability.

A simpler, more decision-relevant interface can outperform a more expressive one.

## Evaluation

Tool/interface evals should include:

- ambiguous state;
- partial success;
- stale state;
- permission denial;
- timeout with unknown side-effect state;
- duplicate/retry hazard;
- downstream failure after upstream success;
- misleading success signal;
- irreversible action risk;
- recovery after tool error;
- excessive/noisy observation;
- missing observation required for expert judgment;
- malformed/hostile tool output where security matters.

A tool architecture fails if the agent must guess a state that the real professional would directly inspect.

## Quality gate

Tool architecture passes only when the agent can reliably observe decision-relevant state, act through sufficiently precise contracts, distinguish failure classes, handle retry/partial-success safely, verify downstream effects, and demonstrate that the interface supports rather than obstructs professional behavior.
