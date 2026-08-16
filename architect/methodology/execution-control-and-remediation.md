# Execution Control and Runtime Remediation

Status: v0.1.

## Purpose

Professional competence is not only choosing a good first action. Long-horizon agents need explicit control over progress, replanning, recovery, and termination.

A generic instruction to `reflect` or `keep trying` is not a control system. Intrinsic self-correction can preserve or amplify an error when no new evidence enters the loop. Runtime remediation should therefore be driven by observations, invariants, verifier feedback, or explicit uncertainty—not ritual self-critique.

## 1. Task control record

For material multi-step work maintain a compact control record containing, as applicable:

- objective and definition of done;
- hard constraints/contracts;
- established facts and evidence references;
- assumptions/hypotheses;
- unresolved unknowns;
- current plan or next milestones;
- completed actions and side effects;
- expected next observation;
- current blockers;
- remaining budget: time/tool calls/cost/retries;
- escalation and stop conditions.

This record is an operational state artifact, not hidden reasoning that must be exposed verbatim.

## 2. Plan only to the useful horizon

Planning depth must match task uncertainty and reversibility.

Use a detailed plan when coordination, dependencies, irreversible actions, or long horizons make it valuable. Prefer short-horizon plan-act-observe cycles when early observations can materially change the route.

Do not force exhaustive planning before obtaining cheap decisive evidence.

## 3. Progress and discrepancy detection

After material actions compare:

`expected state -> observed state -> discrepancy -> implication`.

Possible triggers for remediation include:

- no measurable progress across repeated steps;
- tool/action repetition without new information;
- violated invariant or contract;
- downstream state differs from claimed success;
- evidence invalidates a key assumption;
- new authoritative information supersedes the plan;
- verifier/critic disagreement on a critical criterion;
- budget or deadline threshold reached;
- action failed partially and state is ambiguous.

Without a trigger, repeated self-reflection is not automatically useful.

## 4. Remediation policy

Classify the failure before choosing a response:

- transient tool/environment failure -> bounded retry/backoff when safe;
- bad input/state assumption -> reacquire evidence/update state;
- plan failure -> replan from preserved objective and constraints;
- partial side effect -> reconcile/rollback/complete safely;
- knowledge/retrieval failure -> obtain stronger evidence;
- capability boundary -> route/escalate;
- authority/permission failure -> stop or seek explicit authorization;
- repeated unexplained failure -> stop and preserve diagnostic evidence.

Do not retry irreversible operations blindly.

## 5. Bounded correction

Every autonomous correction loop should define:

- what new evidence can enter;
- maximum retries/iterations or equivalent budget;
- whether retries are idempotent;
- state reconciliation between attempts;
- escalation threshold;
- termination reason.

A loop that can continue indefinitely without information gain is a design defect.

## 6. Independent verification

Self-critique is not independent verification.

When consequence or failure history warrants it, use one or more independent signals:

- deterministic invariant/test;
- environment/downstream state;
- alternative data source;
- specialist/critic with genuinely different evidence or role;
- accountable human review.

Adding another LLM call with the same context and incentives does not automatically create independence.

## 7. Run record and replayability

For consequential or diagnostically difficult workflows maintain a vendor-neutral run record sufficient to reconstruct what happened:

- task/agent/runtime/model/tool/eval versions;
- material inputs and evidence references;
- structured state/checkpoint references;
- actions/tool calls and results;
- approvals/permission decisions;
- errors, retries, replans, rollbacks;
- outcome verification;
- termination reason;
- material cost/latency.

Do not require storage of hidden chain-of-thought. Record observable decisions, actions, evidence, and state transitions.

## 8. Evaluation

Control-loop evals should include:

- initial plan invalidated by new evidence;
- false success signal contradicted downstream;
- transient failure that merits retry;
- non-idempotent operation that must not be retried blindly;
- repeated no-progress/stall sequence;
- corrupted or stale checkpoint;
- constraint forgotten after context compaction;
- tool disagreement requiring evidence reconciliation;
- task that should terminate early because success is already proven;
- task that must stop/escalate because no safe path remains.

Grade both outcome and control behavior: information gain, unnecessary actions, unsafe retries, recovery quality, and termination correctness.

## Quality gate

Execution-control architecture passes only when the agent has observable answers to:

1. What state is it trying to change?
2. How does it know progress occurred?
3. What observation invalidates the current plan?
4. How does it choose retry vs replan vs rollback vs escalate?
5. What bounds correction loops?
6. What independently verifies critical success?
7. Why did the run terminate?

A professional long-horizon agent is incomplete if its only recovery mechanism is `try again` or `reflect on your answer`.
