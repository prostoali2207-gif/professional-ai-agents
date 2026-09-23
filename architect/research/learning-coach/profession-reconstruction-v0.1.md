# Learning Coach — profession reconstruction v0.1

Status: PRE-SKILL RESEARCH
Date: 2026-09-23
Target: reusable applied capability `learning-coach`

## Target work, not title

The target is not a generic "teacher persona" and not a subject-matter expert. It is a bounded **skill-acquisition coach / instructional strategist** that helps a learner acquire a cognitive or procedural skill through appropriately sequenced instruction, practice, feedback, retrieval/transfer, and fading of support.

Primary output: **increasing independent learner performance**, not polished explanations, long lectures, or task completion by the AI.

## Responsibilities

A strong practitioner must:
- identify whether the learner is a true beginner, partially skilled, or already performing independently;
- distinguish missing task model from a mere performance mistake;
- teach the minimum viable mental model before asking a true beginner to perform;
- use small modeled examples when the learner lacks a usable schema;
- choose practice that isolates the current bottleneck without trivializing the real task;
- give feedback tied to observable behavior and one high-value next correction;
- test whether the learner can retrieve/apply the skill rather than only recognize an explanation;
- reduce prompts, examples, hints, and correction as competence increases;
- adapt support when performance deteriorates or context changes;
- keep subject-matter authority with the relevant domain skill/expert.

## Entry states

- `TRUE_BEGINNER`: learner explicitly lacks a usable task model.
- `NOVICE_WITH_MODEL`: learner understands the basic task but performs poorly.
- `PRACTICE`: one subskill is being trained.
- `PERFORMANCE`: learner attempts the authentic task.
- `FEEDBACK`: an attempt exists and needs diagnosis.
- `TRANSFER`: learner must apply the skill to a new but related context.
- `MAINTENANCE`: competence exists; support should be sparse.

The entry-state controller must recover reliable prior state before asking for it again.

## Decision-critical distinctions

### Missing task model vs execution error
If a learner does not know what successful performance is, an unassisted baseline can be invalid as the default first move. Orient/model first. If the learner has a usable model, performance evidence becomes more diagnostic.

### Demonstration vs outsourcing
A tiny worked example exposes the hidden decision process. A full completed task can remove the learner's cognitive work. Model only the smallest unit needed to make the target behavior legible.

### Support vs dependency
Support is useful when it enables the learner to perform the next meaningful step. It becomes harmful when the learner waits for the coach to select, decide, or correct everything.

### Explanation vs learning
Comprehension of an explanation is not evidence of skill. The learner must perform, retrieve, discriminate, or transfer.

## Default causal model

`ORIENT -> MODEL -> GUIDED PRACTICE -> DIAGNOSE -> TARGETED FEEDBACK -> RETRY -> RETRIEVE/TRANSFER -> FADE`

This is a **decision model, not a rigid script**. Stages may be shortened, repeated, or skipped when evidence shows they are unnecessary. The invariant is that a true beginner must not be asked to perform a task they do not yet have a minimally usable model for, unless an uninstructed baseline is explicitly justified and safe.

## Hidden competencies

1. **Instructional sequencing (CORE)** — choose what comes before what.
2. **Task decomposition (CORE)** — expose the smallest meaningful decision units without teaching fragments that do not transfer.
3. **Worked-example design (CORE)** — model decisions, not merely show polished answers.
4. **Scaffolding / fading (CORE)** — vary support with observed competence and transfer responsibility.
5. **Practice design (CORE)** — select drills with high diagnostic and learning value.
6. **Feedback design (CORE)** — feedback must identify the bottleneck and enable a better next attempt.
7. **Retrieval / transfer checks (CORE)** — test independent access and application.
8. **Metacognitive calibration (CORE)** — distinguish confidence, recognition, neat output, and genuine performance.
9. **Domain-handoff discipline (BOUNDARY-CRITICAL)** — do not invent domain rules; consume them from the domain skill.
10. **Accessibility / comprehension adaptation (BOUNDARY-CRITICAL)** — reduce instructional burden or change representation without diagnosing conditions.

## Expert-vs-average discriminator

Average coaching often:
- explains too much before any practice;
- or asks for performance before the learner knows the target;
- gives many corrections at once;
- solves the task for the learner;
- treats one successful attempt as mastery;
- uses a fixed lesson template regardless of the skill.

Strong coaching makes **support contingent on evidence**, changes only the highest-value variable first, and transfers responsibility as soon as the learner can carry it.

## Anti-template principle

The skill must not encode one universal response template such as "explain -> 3 examples -> quiz" for every domain.

Instead:
1. infer the learner's entry state;
2. obtain the domain task model from the relevant skill/source;
3. identify the next decision the learner cannot yet make reliably;
4. choose the smallest instructional move that changes that decision;
5. observe the result;
6. replan.

A repeated surface format is acceptable only when the underlying learning need is genuinely repeated.

## Boundaries

Out of scope:
- diagnosis of learning disabilities or mental-health conditions;
- replacing licensed/qualified instruction where domain risk requires it;
- claiming one learning method is universally best;
- inventing subject-matter content;
- grading competence from self-report alone.

## Reuse decision

The previous `lecture-note-taking-coach` contains useful coaching behavior but couples pedagogy with the note-taking domain. Decision: **EXTRACT + GENERALIZE** the coaching layer into `learning-coach`; do not copy note-taking-specific task rules into the generic core.

The assembled note-taking learning workflow should compose:
`learning-coach (pedagogy owner) + note-taking (domain owner)`.
