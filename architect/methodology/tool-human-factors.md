# Tool and Agent-Computer-Interface Engineering

Status: v0.3.

## Principle

Tool access is not enough. A professional agent needs an interface that exposes the information required for correct decisions, supports diagnosis/recovery, and makes consequential state observable.

Open-source engineering agents such as SWE-agent provide concrete evidence that tool/interface design can materially change end-agent performance: observation size, edit feedback, search output, and explicit success/failure signals affect whether the agent can act competently. Therefore evaluate the interface together with the model, not as neutral plumbing.

## Tool capability model

For every tool define:

- professional purpose;
- underlying capability supplied independently of vendor/product name;
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

## Capability-first tool reasoning

Do not bind a professional workflow to a product name when the real dependency is a capability.

For material tool-dependent steps represent the dependency as:

`required professional outcome -> required capability -> evidence/quality constraints -> candidate mechanisms/tools -> selected implementation`.

Examples of capabilities include retrieving an authoritative record, transforming structured data, computing a metric, publishing an approved artifact, observing downstream state, or communicating with a stakeholder. A product may supply several capabilities; several unrelated products or mechanisms may supply the same capability.

This abstraction is required for both architecture design and runtime recovery. It prevents vendor/tool availability from being mistaken for the professional requirement itself.

## Tool resilience and capability substitution

When a preferred tool is unavailable, broken, quota-exhausted, permission-incompatible, too costly, unreliable, or otherwise unsuitable, do not stop merely because the named tool cannot be used. Reconstruct the missing capability and search the available mechanism space.

Use:

`failed/unavailable tool -> missing capability -> invariant requirements -> candidate substitutes -> compatibility/risk check -> smallest discriminating test -> execute -> verify outcome`.

Candidate substitutes may include:

- another tool in the same category;
- a deterministic script/query/transform instead of an AI tool;
- a direct API instead of a dashboard or automation platform;
- an export/import or intermediate representation;
- composition of several narrower tools;
- a tool normally associated with an adjacent profession or workflow when its actual capability contract fits;
- a bounded manual/human step when automation would be less reliable or less safe;
- deliberate graceful degradation when the full capability cannot be preserved.

Do not require category similarity. Cross-domain transfer is legitimate when capability compatibility is demonstrated. Conversely, superficial similarity or a vendor claim is not evidence that a substitute preserves the required capability.

### Substitution compatibility gate

Before adopting a substitute check, as material:

1. **Functional equivalence** — does it actually provide the decision/action capability required?
2. **Evidence fidelity** — does it preserve authoritative source, provenance, precision, units, coverage, freshness, and observability needed for the professional claim?
3. **Semantic equivalence** — are definitions, populations, filters, transformations, and success criteria compatible?
4. **Authority and permissions** — can it perform the action within delegated scope and least-required permissions?
5. **Security/privacy/compliance** — does the workaround introduce an unacceptable trust boundary, secret exposure, data transfer, or policy violation?
6. **Side-effect semantics** — are idempotency, partial success, reversibility, and rollback sufficiently understood?
7. **Reliability/latency/SLO** — is degradation acceptable for the task consequence and time horizon?
8. **Resource economics** — is expected total cost, quota use, human effort, and rework acceptable?
9. **Verification** — is there direct evidence that the substitute produced the required downstream result?

A substitute that fails a decision-critical invariant is not a fallback; it is a different, weaker capability and must be represented as such.

### Constraint-aware improvisation

Professional improvisation is bounded search, not arbitrary tool use. Generate materially different mechanisms before converging when the obvious route fails, especially when the task is important and the first fallback repeats the same dependency or failure mode.

Prefer substitutions that remove the failed dependency rather than merely wrapping it. For example, if a dashboard is unavailable but authoritative export/API data remain available, compute from those data rather than using a search engine to guess the dashboard's private state.

Do not improvise around hard security, legal, authorization, evidence-authority, or irreversible-action constraints. Escalate when no candidate preserves the critical invariants.

### Graceful degradation

When exact equivalence is impossible, explicitly identify what is lost: automation, coverage, freshness, precision, latency, confidence, auditability, or another material property. Then determine whether the degraded route remains sufficient for the decision.

Use:

`full capability -> preserved properties -> lost properties -> consequence -> acceptable for this task? -> proceed / narrow claim / escalate`.

Never silently convert a degraded workaround into a full-capability success claim.

### Verification after substitution

A workaround is provisional until verified. Prefer direct comparison against known-good fixtures, authoritative records, downstream state, deterministic invariants, or a small paired run using the preferred mechanism when it becomes available.

Record enough provenance to distinguish the normal route from the substitute route and to support later diagnosis of systematic differences.

## Interface quality questions

Ask whether the interface lets the agent:

1. perceive the state needed for the decision;
2. distinguish success from apparent success;
3. diagnose failure rather than merely receive `error`;
4. distinguish transient failure from invalid input, permission failure, stale state, and partial success;
5. recover, retry safely, roll back, substitute the failed capability, or escalate;
6. preserve provenance of observations/actions;
7. avoid destructive actions when a read/check is sufficient;
8. verify downstream effects;
9. avoid drowning decision-relevant evidence in raw telemetry;
10. know when repeating an action is unsafe or useless;
11. distinguish a named-tool dependency from the underlying professional capability;
12. identify when a cross-domain substitute preserves the capability and when it only appears to.

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
- successful capability substitution rate;
- false-equivalence/substitution error rate;
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
- preferred tool unavailable while an equivalent mechanism exists;
- same-category fallback that shares the original failure dependency;
- cross-domain substitute that is valid despite an unfamiliar category;
- tempting substitute that is superficially similar but loses authoritative/private state;
- composition of narrower tools to restore a missing capability;
- graceful degradation where exact equivalence is impossible;
- refusal/escalation when no substitute preserves a critical invariant;
- verification that the substitute produced the required downstream result;
- excessive/noisy observation;
- missing observation required for expert judgment;
- malformed/hostile tool output where security matters.

A tool architecture fails if the agent must guess a state that the real professional would directly inspect, or if a named-tool failure unnecessarily becomes a task failure despite an available safe equivalent mechanism.

## Quality gate

Tool architecture passes only when the agent can reliably observe decision-relevant state, act through sufficiently precise contracts, distinguish failure classes, handle retry/partial-success safely, verify downstream effects, and demonstrate that the interface supports rather than obstructs professional behavior.

For material tool-dependent workflows it must additionally demonstrate capability-first reasoning: identify the underlying dependency, find materially distinct substitutes when appropriate, reject false equivalence, degrade explicitly when necessary, and verify the substituted route rather than claiming success from plausibility alone.
