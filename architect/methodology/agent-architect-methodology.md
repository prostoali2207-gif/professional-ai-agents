# Agent Architect Methodology

Status: v1.1 release candidate — benchmark qualification pending fresh held-out B1 revalidation and a complete one-SHA B1–B10 release gate after the authoritative-supersession repair.

## Purpose

Build specialized AI agents that approximate the work patterns of strong professionals by modeling the profession and the runtime system required to execute that model reliably—not by inflating a prompt.

## 1. Profession discovery

Identify the real human role or combination of roles. Define responsibilities, outputs, stakeholders/work context, boundaries, risks, and what counts as evidence of successful work.

Do not accept the user's role label as authoritative. Reconstruct the work from the goal.

## 2. Work and decision decomposition

Map what a strong practitioner actually does:

- recurring tasks;
- difficult decisions;
- inputs and cues;
- misleading cues;
- uncertainty;
- trade-offs;
- stopping conditions;
- escalation points;
- verification actions.

Use cognitive-task-analysis logic: difficult professional work is often distinguished by decisions and cue recognition that are tacit rather than by explicit checklist knowledge.

## 3. Expert-vs-average discriminator

For each significant capability, identify:

- novice/weak behavior;
- competent behavior;
- expert behavior;
- typical failure;
- evidence of mastery.

The competency description must be observable. Avoid labels such as `knows research` or `has taste` without specifying behavior.

## 4. Competency and evidence engineering

A competency unit should contain, when relevant:

- purpose;
- professional situation;
- required knowledge;
- observable capability;
- inputs/cues;
- decision model;
- trade-offs;
- failure modes;
- expert behavior;
- tools;
- evidence;
- boundary/escalation;
- evaluation;
- adversarial evaluation.

Separate knowledge, competence, judgment, execution, and verification.

For critical capabilities make the validity chain explicit:

`competency claim -> observable evidence -> representative task -> grader/verifier`.

## 5. Scope and adjacent disciplines

Professional reconstruction can expand without bound. Classify adjacent competencies as:

- CORE;
- BOUNDARY-CRITICAL;
- ESCALATION;
- CONTEXTUAL;
- OUT-OF-SCOPE.

Depth must be proportional to decision criticality, coupling, failure severity, reversibility, volatility, difficulty of detecting error, and tacit-judgment burden.

Do not exclude an important boundary merely because another profession traditionally owns it. Do not pretend the agent becomes a specialist in every adjacent field.

## 6. Knowledge dependency mapping

For every competency, determine which underlying disciplines are actually required. Do not encode a discipline as an instruction. If a competency depends on typography, statistical inference, security engineering, accounting, or another discipline, provide a sufficient knowledge layer or reliable retrieval process.

Classify knowledge as:

- foundations;
- standards/specifications;
- empirical evidence;
- current professional practice;
- heuristics;
- cases/examples;
- failure patterns;
- volatile/current knowledge.

Maintain provenance and freshness. Volatile or version-sensitive knowledge should normally be retrieved live.

## 7. Professional judgment

Rules must include scope and exceptions. A useful judgment unit records:

`principle -> causal rationale -> applicability conditions -> exceptions -> trade-offs -> evidence required -> justified violation conditions`.

The agent must distinguish facts, assumptions, estimates, and unresolved uncertainty.

## 8. Procedural capability architecture

Separate reusable procedural competence from the always-loaded router. Distinguish:

- routing metadata;
- procedural instructions;
- references;
- executable helpers/scripts;
- schemas/contracts;
- examples/templates/assets;
- tool bindings.

Use progressive disclosure where the runtime supports it, but evaluate both capability selection and staged resource loading. Do not equate a file-format standard with behavioral portability.

See `procedural-skill-packaging.md`.

## 9. Workflow and tool architecture

Design the work loop around the profession. A generic pattern is:

`understand -> diagnose -> identify uncertainty -> retrieve evidence -> generate alternatives -> decide -> execute -> observe actual result -> critique -> revise`.

Do not impose this sequence when the profession requires a different one.

Tools are part of competence. If the environment can provide ground truth, the workflow must use it rather than infer success from reasoning alone.

Tool architecture must include decision-relevant observations, failure/partial-success signaling, idempotency/retry semantics where material, downstream verification, and recovery.

See `tool-human-factors.md`.

## 10. Runtime state, memory, and context

For long-horizon, multi-turn, interruptible, or multi-session work, explicitly model:

- working context;
- session/task state;
- persistent episodic/semantic/procedural memory as applicable;
- memory write/use/update/forgetting gates;
- context assembly and compaction;
- contradictions and temporal supersession;
- checkpoint/resume;
- privacy and poisoning risk;
- multi-session/stateful evaluation.

A transcript, vector store, or large context window is not by itself a memory architecture.

See `runtime-state-memory-context.md`.

## 11. Execution control and remediation

For material multi-step execution define:

- objective/definition of done;
- preserved constraints and established facts;
- progress evidence;
- expected vs observed state;
- stall/anomaly triggers;
- retry vs replan vs rollback vs escalation policy;
- correction/retry budgets;
- termination reason;
- replayable observable run record.

Do not rely on unbounded intrinsic self-reflection. Correction should be driven by new evidence, environment feedback, invariants, or independent verification.

See `execution-control-and-remediation.md`.

## 12. Architecture selection

Choose the least complex system that satisfies the job:

- single augmented agent;
- deterministic workflow;
- agent plus critic/evaluator;
- specialist handoff;
- orchestrated multi-agent system.

Additional agents require a concrete benefit such as independent judgment, domain separation, parallel search, or risk containment. More agents are not intrinsically better.

Architecture decisions must also consider latency, model/tool cost, human-review burden, shared-state consistency, context loss, and coordination overhead where material.

## 13. Security and trust boundaries

For agents that process untrusted content or possess consequential tools, distinguish data, instruction, and authority channels.

Model as relevant:

- indirect prompt injection/agent hijacking;
- tool-output/retrieval injection;
- memory poisoning;
- skill/script/plugin supply-chain trust;
- secret/data-flow boundaries;
- sandbox/network policy;
- safe delegation;
- security telemetry and adversarial tests.

Permissions without a trust model are insufficient.

See `agent-security-and-trust.md`.

## 14. Authority and operational governance

Capability and authority are different.

For tool-using agents define:

- what they may read, propose, modify, send, publish, delete, deploy, spend, or approve;
- least-required permissions;
- reversibility and blast radius;
- confirmation/escalation rules;
- rollback and auditability;
- environment/model/tool/version assumptions;
- accountable owner for consequential deployment.

High-impact, irreversible, uncertain, or weakly authorized actions require stronger safeguards.

## 15. Evaluation engineering

Evaluation must cover both outcome and, where material, trajectory/tool/state use.

Minimum dimensions for serious agents include as applicable:

- fundamental knowledge;
- application;
- diagnosis;
- practical execution;
- conflicting requirements;
- bad user assumptions;
- insufficient information;
- source/retrieval quality;
- empirical validity/comparability;
- tool use/interface quality;
- evidence quality;
- state/memory correctness;
- context-compaction/checkpoint integrity;
- replanning/recovery/termination;
- security/trust-boundary behavior;
- edge cases;
- critique;
- professional boundary/escalation.

Prefer authentic tasks over trivia. Use deterministic/environment graders when ground truth is mechanically verifiable; calibrated model graders for qualitative dimensions where appropriate; human/domain-expert review for high-consequence or irreducibly judgment-heavy cases.

Separate development, regression, holdout, and practical evals. Protect against benchmark leakage and prompt-overfitting. Use repeated trials or uncertainty estimates when stochastic variance is material.

## 16. Failure-driven improvement

When an eval fails, classify the root cause before changing the system:

- profession-model failure;
- missing/incorrect knowledge;
- stale knowledge;
- retrieval failure;
- memory/state/context failure;
- reasoning/judgment failure;
- workflow/control failure;
- procedural capability selection/loading failure;
- tool/interface failure;
- execution/verification failure;
- security/trust-boundary failure;
- coordination/handoff failure;
- instruction failure;
- evaluator defect;
- environmental noise/drift.

Repair the responsible layer, then run regression and adversarial retests.

## 17. Production learning

Production feedback is evidence, not automatically truth.

Use:

`observation -> reproduce/validate -> classify -> root cause -> affected layer -> candidate change -> regression/adversarial eval -> deploy -> monitor`.

Capture incidents, near-misses, drift, security events, state corruption, user corrections, and unexpected downstream outcomes. Promote an operational lesson into stable knowledge or memory policy only when it generalizes, has provenance, survives stronger evidence, and improves representative evals without material regressions.

## 18. Final expert-gap and red-team pass

Before finalization, explicitly ask:

`What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?`

Then red-team the architecture from at least:

- senior practitioner;
- educator/competency assessor;
- hiring manager;
- evaluation scientist where evaluation validity is material;
- systems/operations engineer where tool execution is material;
- security reviewer where untrusted content or consequential authority is material.

Material gaps must be repaired before release.

## 19. Pre-SKILL gate

Do not write the final role SKILL until:

- profession reconstruction is evidence-backed;
- competency/evidence and knowledge architecture exist;
- judgment, scope, tools, authority, and escalation are modeled;
- procedural packaging is designed where useful;
- state/memory/context and execution control are designed where material;
- security/trust boundaries are designed where material;
- evaluation integrity and regression design exist;
- production-learning path exists;
- red-team has been run and material findings corrected.

## Definition of done

`profession mapped -> competencies/evidence mapped -> authoritative knowledge assembled -> knowledge gaps identified -> judgment/workflows/tools designed -> procedural capabilities defined -> state/memory/context defined where material -> execution-control/remediation defined where material -> security/trust boundaries defined where material -> scope/authority/governance defined -> failure modes encoded -> SKILL orchestrates the system -> competency evaluation completed -> stateful/security/control-loop tests completed where applicable -> weaknesses corrected -> practical evaluation passed -> production feedback loop defined`.

## Benchmark qualification note

The original v1.0 cross-domain work remains useful evidence for the profession-first core, but it was not sufficient by itself for the runtime layers added in v1.1. Earlier controlled runs exercised B1–B10 and the P0 trust/state/authority families, but the sealed-head revalidation later exposed a real B1 authoritative-supersession defect. That defect has been repaired in the memory policy and executable router. Therefore the current candidate is not benchmark-qualified until a fresh held-out B1 passes and a complete preregistered B1–B10 release suite passes on one final candidate SHA. Every applied agent still requires its own profession-specific evidence, runtime checks, practical evaluation, adversarial testing, and release decision.
