# Agent Boundary and Coordination Engineering

Status: v0.1.

## Default

Do not decompose a system into multiple agents merely because multiple professional labels can be named.

Start with the simplest architecture capable of meeting the competency/evidence requirements. Multi-agent decomposition must earn its coordination cost.

## Decomposition test

Prefer one agent with modular knowledge/workflows when:

- decisions share substantial context;
- the same evidence is reused across stages;
- handoffs would discard important tacit state;
- one role can execute and verify the work without independence requirements;
- specialization can be represented as modules without role conflict.

Consider multiple agents when one or more are materially true:

- distinct professions require genuinely different competency/knowledge systems;
- independent critique or separation of duties is important;
- tool permissions or safety boundaries differ;
- subtasks can be parallelized with low coupling;
- context size/interference materially harms a single agent;
- a specialist needs an independent evidence process;
- the task has clear contractual handoff boundaries.

## Coordination tax

Every extra agent introduces potential:

- context loss;
- contradictory assumptions;
- duplicated research;
- stale handoff state;
- ownership ambiguity;
- error propagation;
- verification gaps;
- extra latency/cost;
- coordination loops with no information gain.

Therefore compare at least:

A. single agent + modules/tools;
B. orchestrator + specialists;
C. specialist + independent critic when verification independence is the actual need.

## Handoff contract

A handoff must specify:

- objective;
- inputs and their provenance;
- assumptions already established;
- unresolved uncertainties;
- decisions already made and why;
- constraints that must not change;
- required output schema;
- evidence required;
- definition of done;
- escalation condition;
- downstream consumer.

A summary without provenance and unresolved uncertainty is not a sufficient professional handoff.

## Coordination evaluation

Test the system for:

- information preservation across handoffs;
- conflicting specialist recommendations;
- circular delegation;
- orphaned responsibilities;
- duplicated actions;
- specialist overreach outside role boundary;
- failure to challenge upstream assumptions;
- downstream acceptance without evidence;
- recovery when one specialist fails.

## Architecture decision record

For each multi-agent design record:

`problem -> decomposition hypothesis -> single-agent alternative -> expected benefit -> coordination risks -> evidence/test -> decision`.

Do not claim that a multi-agent architecture is better until a representative evaluation demonstrates an advantage that matters for the target work.