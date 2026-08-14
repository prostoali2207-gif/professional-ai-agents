# Agent Architect Methodology

Status: v0.3, pre-SKILL gate complete pending final executable skill assembly.

## Purpose

Build specialized AI agents that approximate the work patterns of strong professionals by modeling the profession, not by inflating a prompt.

## 1. Profession discovery

Identify the real human role or combination of roles. Define responsibilities, outputs, boundaries, risks, and what counts as evidence of successful work.

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

The competency description must be observable. Avoid labels such as "knows research" or "has taste" without specifying behavior.

## 4. Competency engineering

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

## 5. Scope and adjacent disciplines

Professional reconstruction can expand without bound. Classify adjacent competencies as:

- CORE;
- BOUNDARY-CRITICAL;
- ESCALATION;
- CONTEXTUAL;
- OUT-OF-SCOPE.

Depth must be proportional to decision criticality, coupling, failure severity, reversibility, volatility, and likelihood that the user would omit the requirement.

Do not exclude an important boundary merely because another profession traditionally owns it. Do not pretend the agent becomes a specialist in every adjacent field.

## 6. Knowledge dependency mapping

For every competency, determine which underlying disciplines are actually required. Do not encode a discipline as an instruction. If a competency depends on typography, statistical inference, security engineering, accounting, or another discipline, provide a sufficient knowledge layer or a reliable retrieval process.

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

principle -> causal rationale -> applicability conditions -> exceptions -> trade-offs -> evidence required -> justified violation conditions.

The agent must distinguish facts, assumptions, estimates, and unresolved uncertainty.

## 8. Workflow and tool architecture

Design the work loop around the profession. A generic pattern is:

understand -> diagnose -> identify uncertainty -> retrieve evidence -> generate alternatives -> decide -> execute -> observe actual result -> critique -> revise.

Do not impose this sequence when the profession requires a different one.

Tools are part of competence. If the environment can provide ground truth, the workflow must use it rather than infer success from reasoning alone.

Tool architecture must include observability, failure/partial-success signaling, downstream verification, and recovery when material.

## 9. Architecture selection

Choose the least complex system that satisfies the job:

- single augmented agent;
- deterministic workflow;
- agent plus critic/evaluator;
- specialist handoff;
- orchestrated multi-agent system.

Additional agents require a concrete benefit such as independent judgment, domain separation, parallel search, or risk containment. More agents are not intrinsically better.

Architecture decisions must also consider latency, model/tool cost, human-review burden, and coordination overhead where material.

## 10. Authority and operational governance

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

## 11. Evaluation engineering

Evaluation must cover both outcome and, where material, trajectory/tool use.

Minimum dimensions for serious agents:

- fundamental knowledge;
- application;
- diagnosis;
- practical execution;
- conflicting requirements;
- bad user assumptions;
- insufficient information;
- source selection;
- retrieval quality;
- tool use;
- evidence quality;
- edge cases;
- critique;
- self-critique;
- recovery from failure.

Prefer authentic tasks over trivia. Use code-based or environment-based graders when ground truth is mechanically verifiable; model graders for qualitative dimensions with calibrated rubrics; human/domain-expert review for high-consequence or irreducibly judgment-heavy cases.

Separate development, regression, holdout, and practical evals. Protect against benchmark leakage and prompt-overfitting. Use repeated trials or uncertainty estimates when stochastic variance is material.

## 12. Failure-driven improvement

When an eval fails, classify the root cause before changing the system:

- profession-model failure;
- missing/incorrect knowledge;
- stale knowledge;
- retrieval failure;
- reasoning/judgment failure;
- workflow failure;
- tool/interface failure;
- execution/verification failure;
- coordination/handoff failure;
- context failure;
- instruction failure;
- evaluator defect;
- environmental noise/drift.

Repair the responsible layer, then run regression and adversarial retests.

## 13. Production learning

Production feedback is evidence, not automatically truth.

Use:

observation -> reproduce/validate -> classify -> root cause -> affected layer -> candidate change -> regression/adversarial eval -> deploy -> monitor.

Capture incidents, near-misses, drift, user corrections, and unexpected downstream outcomes. Promote an operational lesson into stable knowledge only when it generalizes, has provenance, survives stronger evidence, and improves representative evals without material regressions.

## 14. Final expert-gap and red-team pass

Before finalization, explicitly ask:

"What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?"

Then red-team the architecture from at least these perspectives:

- senior practitioner;
- educator/competency assessor;
- hiring manager;
- evaluation scientist where evaluation validity is material;
- systems/operations engineer where tool execution is material.

Material gaps must be repaired before release.

## 15. Pre-SKILL gate

Do not write the final role SKILL until:

- profession reconstruction is evidence-backed;
- competency and knowledge architecture exist;
- judgment, scope, tools, authority, and escalation are modeled;
- evaluation integrity and regression design exist;
- production-learning path exists;
- a methodology dry-run exposes and repairs hidden gaps;
- red-team has been run and material findings corrected.

## Definition of done

Profession mapped -> competencies mapped -> authoritative knowledge assembled -> knowledge gaps identified -> workflows designed -> tools/evidence defined -> scope/authority/governance defined -> judgment encoded -> failure modes encoded -> SKILL orchestrates the system -> competency evaluation completed -> weaknesses corrected -> practical evaluation passed -> production feedback loop defined.
