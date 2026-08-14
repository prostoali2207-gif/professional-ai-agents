# Agent Architect Methodology

Status: v0.2, pre-SKILL.

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

## 5. Knowledge dependency mapping

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

## 6. Professional judgment

Rules must include scope and exceptions. A useful judgment unit records:

principle -> causal rationale -> applicability conditions -> exceptions -> trade-offs -> evidence required -> justified violation conditions.

The agent must distinguish facts, assumptions, estimates, and unresolved uncertainty.

## 7. Workflow and tool architecture

Design the work loop around the profession. A generic pattern is:

understand -> diagnose -> identify uncertainty -> retrieve evidence -> generate alternatives -> decide -> execute -> observe actual result -> critique -> revise.

Do not impose this sequence when the profession requires a different one.

Tools are part of competence. If the environment can provide ground truth, the workflow must use it rather than infer success from reasoning alone.

## 8. Architecture selection

Choose the least complex system that satisfies the job:

- single augmented agent;
- deterministic workflow;
- agent plus critic/evaluator;
- specialist handoff;
- orchestrated multi-agent system.

Additional agents require a concrete benefit such as independent judgment, domain separation, parallel search, or risk containment. More agents are not intrinsically better.

## 9. Evaluation engineering

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
- tool use;
- evidence quality;
- edge cases;
- critique;
- self-critique;
- recovery from failure.

Prefer authentic tasks over trivia. Use code-based or environment-based graders when ground truth is mechanically verifiable; model graders for qualitative dimensions with calibrated rubrics; human/domain-expert review for high-consequence or irreducibly judgment-heavy cases.

## 10. Failure-driven improvement

When an eval fails, classify the root cause before changing the system:

- missing/incorrect knowledge;
- retrieval failure;
- reasoning/judgment failure;
- workflow failure;
- tool/interface failure;
- context failure;
- instruction failure;
- evaluator defect;
- environmental noise.

Repair the responsible layer, then run regression and adversarial retests.

## 11. Final expert-gap and red-team pass

Before finalization, explicitly ask:

"What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?"

Then red-team the architecture from three perspectives:

- senior practitioner;
- educator/trainer of the profession;
- hiring manager responsible for selecting strong practitioners.

Material gaps must be repaired before release.

## Definition of done

Profession mapped -> competencies mapped -> authoritative knowledge assembled -> knowledge gaps identified -> workflows designed -> tools/evidence defined -> judgment encoded -> failure modes encoded -> SKILL orchestrates the system -> competency evaluation completed -> weaknesses corrected -> practical evaluation passed.
