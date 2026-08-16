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

## Professional model before prompt

For each agent, reconstruct the real profession or combination of professions. Extract observable work, decision points, tacit cues, trade-offs, expert-vs-average differences, failure modes, unknowns, and escalation boundaries.

Do not confuse:
- knowledge with competence;
- competence with judgment;
- judgment with execution;
- execution with verification;
- instructions with training material.

## Reuse before rebuild

Before substantial implementation of a non-trivial applied professional agent, perform a professional-agent landscape and reuse audit using `architect/methodology/professional-agent-reuse-discovery.md`.

Do not assume the requested specialist, skill, workflow, tool, benchmark, dataset, or evaluation asset must be built locally. Search for complete specialist agents and for reusable components separately, including professional skill packs, SOP/workflow implementations, domain tools/MCP servers/APIs, evaluation assets, structured knowledge resources, adjacent specialist systems, and mature infrastructure components.

Start from the reconstructed profession and critical competency map, not repository names. A repository called `marketing-agent`, `lawyer-agent`, or `financial-analyst` is not evidence that it performs that profession competently.

Inspect serious candidates beyond README claims and classify them as:

`USE AS-IS | ADAPT | COMBINE | BENCHMARK ONLY | REJECT | BUILD MISSING PART`.

For material candidates evaluate professional fidelity, behavioral evidence, evaluation validity, knowledge/source provenance, engineering quality, maintenance/freshness, security and supply-chain risk, licensing/reuse rights, runtime compatibility, and total resource/operational cost.

New implementation requires an explicit residual gap:

`target competency -> strongest existing candidate(s) -> evidence strength -> residual gap -> action`.

Do not rebuild a mature sufficient capability merely because local implementation is easier than landscape research. Do not reuse a weak or unsafe capability merely because reuse appears cheaper. Reused components must still pass the target system's own local evaluation and governance requirements.

## Verification

If an outcome can be directly observed or tested, direct observation/test is required. Reasoning is not a substitute for execution evidence.

## Evaluation-driven development

Each agent must have evaluation coverage before it is declared ready. Include practical tasks, adversarial cases, ambiguity, conflicting requirements, bad user assumptions, insufficient information, tool/evidence use, critique, self-critique, and regression tests.

Failure handling:

FAIL -> classify failure -> root cause -> repair the correct layer -> regression test -> adversarial retest.

Do not patch every failure by adding arbitrary prompt text.

## Architecture discipline

Use the simplest architecture that can meet the professional task. Do not default to multi-agent systems. Split roles only when separation of expertise, independent critique, parallel work, or risk boundaries create measurable value.

## Definition of done

An applied agent is not ready until:

profession mapped -> competencies mapped -> existing professional-agent/component landscape audited -> reuse/adapt/build decisions evidenced -> authoritative knowledge assembled -> residual gaps identified -> workflows designed -> tools/evidence strategy defined -> professional judgment encoded -> failure modes encoded -> skill orchestrates the system -> competency evaluation run -> reused/adapted components locally verified -> weaknesses corrected -> practical evaluation passed.

Even then, never claim exhaustive knowledge. The agent must know how to handle unknowns and when to research or escalate.
