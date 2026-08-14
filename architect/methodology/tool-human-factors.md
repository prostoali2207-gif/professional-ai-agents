# Tool and Human-Factors Engineering

Status: v0.1.

## Principle

Tool access is not enough. A professional agent needs an interface that exposes the information required for correct decisions, supports diagnosis/recovery, and makes consequential state observable.

## Tool capability model

For every tool define:

- professional purpose;
- observable state;
- actions available;
- hidden state / blind spots;
- preconditions;
- side effects;
- reversibility;
- failure signals;
- evidence returned after action;
- latency/cost;
- permission/safety boundary.

## Interface quality questions

Ask whether the interface lets the agent:

1. perceive the state needed for the decision;
2. distinguish success from apparent success;
3. diagnose failure rather than merely receive `error`;
4. recover or safely escalate;
5. preserve provenance of observations/actions;
6. avoid destructive actions when a read/check is sufficient;
7. verify downstream effects.

## Situation awareness

For consequential workflows, evaluate whether the agent can maintain:

- what is true now;
- what changed;
- what remains uncertain;
- what action has already been taken;
- what downstream state should now exist;
- what anomaly would indicate failure.

Do not overload the agent with raw telemetry when a decision-relevant representation is possible; do not hide evidence merely to simplify the interface.

## Error-support requirement

Interfaces should support professional diagnosis and correction. A tool that returns only a generic failure message may prevent expert behavior even if the underlying model knows how to diagnose the problem.

## Human oversight

Where a human is the escalation or approval boundary, the handoff should expose decision-relevant evidence, uncertainty, consequences, and available alternatives. Do not require the human to reconstruct the agent's hidden state from a vague summary.

## Evaluation

Tool/interface evals should include:

- ambiguous state;
- partial success;
- stale state;
- permission denial;
- downstream failure after upstream success;
- misleading success signal;
- irreversible action risk;
- recovery after tool error;
- excessive/noisy observation;
- missing observation required for expert judgment.

A tool architecture fails if the agent must guess a state that the real professional would directly inspect.