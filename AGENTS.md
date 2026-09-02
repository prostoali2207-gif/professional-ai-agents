# Repository operating rules

This repository exists to design, research, evaluate, and strengthen specialized professional AI agents.

## Prime directive

Do not write a role SKILL.md first.

Before an applied agent can receive a SKILL.md, the profession must be mapped, expert competencies must be identified, authoritative knowledge must be assembled, judgment and failure modes must be modeled, tools/evidence must be specified, and an evaluation plan must exist.

## Evidence over opinion

A user suggestion, an AI suggestion, a popular practice, or an attractive example is not evidence by itself. Material professional claims must be classified and supported by the best available evidence.

Prefer, in order appropriate to the claim:
1. authoritative standards and official documentation;
2. primary research and empirical data;
3. recognized professional frameworks and high-quality technical literature;
4. current practice from demonstrably strong practitioners;
5. examples and inspiration, explicitly labeled as such.

When sources conflict, record the conflict, scope, assumptions, and decision rationale. Do not silently select the convenient source.

## Runtime judgment and opportunity search

For material recommendations, architecture choices, and open-ended solution design, apply `docs/runtime-judgment-and-opportunity.md`.

In particular:
- do not manufacture a low-value balancing objection when an idea is already well supported;
- do not treat user or AI confidence as evidence;
- accept correct corrections when new evidence changes the decision;
- before fixing the first plausible mechanism, briefly test whether the mechanism can be replaced, eliminated, reused through existing capability/integration, or moved across AI/software/human boundaries;
- count alternatives as distinct only when their mechanisms or system boundaries materially differ;
- stop exploring when additional search no longer has plausible decision value.

## Professional model before prompt

For each agent, reconstruct the real profession or combination of professions. Extract observable work, decision points, tacit cues, trade-offs, expert-vs-average differences, failure modes, unknowns, and escalation boundaries.

Do not confuse:
- knowledge with competence;
- competence with judgment;
- judgment with execution;
- execution with verification;
- instructions with training material.

## Verification

If an outcome can be directly observed or tested, direct observation/test is required. Reasoning is not a substitute for execution evidence.

## Evaluation-driven development

Each agent must have evaluation coverage before it is declared ready. Include practical tasks, adversarial cases, ambiguity, conflicting requirements, bad user assumptions, insufficient information, tool/evidence use, critique, self-critique, and regression tests.

Failure handling:

FAIL -> classify failure -> root cause -> repair the correct layer -> regression test -> adversarial retest.

Do not patch every failure by adding arbitrary prompt text.

## Qualification stop-loss

The generic qualification platform is in **STOP / maintenance mode by default** under the evidence-based decision in issue #129.

Before repairing or rerunning any failed qualification, follow `architect/methodology/qualification-stop-loss.md`.

Mandatory rules:
- classify the failure before repair;
- do not reopen generic platform engineering without an explicit #129 reopen criterion and repository evidence;
- do not create serial infrastructure-repair issues to chase executability;
- after one bounded same-class technical repair and one eligible retry in a frozen cycle, another technical defect stops the repair chain and yields `NOT_EXECUTABLE` / the preregistered infrastructure verdict;
- a new issue, provider, transport, or renamed error does not reset the repair budget;
- never weaken professional scope, thresholds, hard-fails, held-out secrecy, independence, or practical evidence to obtain PASS.

This stop-loss limits infrastructure churn, not professional rigor.

## Architecture discipline

Use the simplest architecture that can meet the professional task. Do not default to multi-agent systems. Split roles only when separation of expertise, independent critique, parallel work, or risk boundaries create measurable value.

## Definition of done

An applied agent is not ready until:

profession mapped -> competencies mapped -> authoritative knowledge assembled -> gaps identified -> workflows designed -> tools/evidence strategy defined -> professional judgment encoded -> failure modes encoded -> skill orchestrates the system -> competency evaluation run -> weaknesses corrected -> practical evaluation passed.

Even then, never claim exhaustive knowledge. The agent must know how to handle unknowns and when to research or escalate.
