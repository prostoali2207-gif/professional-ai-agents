# Study Strategy

Version: 0.1.0-candidate
Status: project-use candidate; below T1 until independent qualification

Pre-SKILL gate: `architect/evaluation/study_strategy/pre-skill-gate-result-v0.1.json`

## Mission

Help the learner turn lessons and sources into **durable, retrievable, correctly scoped knowledge** without memorizing everything or creating an unsustainable review system.

This skill owns durable study strategy:
- what deserves active memory investment;
- what kind of retention is required;
- how to retrieve, correct, space, recheck and maintain it;
- when to retire or downgrade review.

It does not own generic teaching sequence, note-taking, or domain authority.

## Trigger

Use when the user wants to:
- decide what from a lesson should be learned, understood, memorized, or merely kept in notes;
- remember material long term;
- build a review routine;
- practice recall;
- decide whether something needs exact memorization;
- test whether knowledge is actually retained;
- reduce forgetting or review overload;
- create study questions/cards only when the target benefits from them;
- track durable knowledge across lessons.

Do not use as the primary skill for:
- teaching a procedural/cognitive skill from zero -> `learning-coach`;
- live lecture capture and note structure -> `note-taking`;
- domain rulings/authority -> relevant domain specialization.

## Required composition

### With `learning-coach`
When the goal is to teach the user **how to study independently**, this skill supplies:
- study-target model;
- practice/review decision rules;
- error taxonomy;
- success criteria.

`learning-coach` owns:
- orientation/modeling;
- guided practice;
- feedback sequence;
- fading of assistance.

### With `note-taking`
`note-taking` preserves a faithful structured representation of the lesson.
This skill decides what from that representation becomes an active study target.

### With domain specialization
The domain owner decides what wording, source identity, conditions, disagreement, safety or authority are material.
This skill must not invent domain requirements.

## Core target model

For each candidate item, choose one or more required endpoints:

- `REFERENCE_ONLY` — keep accessible; no recurring memorization by default.
- `UNDERSTAND` — explain meaning/relationship in own words.
- `RECALL` — retrieve proposition, label, list, relationship or structure without seeing it.
- `EXACT` — reproduce verified wording/order/identity where exactness itself matters.
- `DISCRIMINATE` — distinguish similar concepts, conditions, cases or sources.
- `APPLY` — use knowledge in a case/problem/decision.
- `EVIDENCE_CHAIN` — reconstruct claim -> evidence/source -> reasoning -> conditions/exceptions/attribution where material.

Do not collapse these into one generic "memorize" bucket.

## Memory-investment gate

Before creating active review, ask:

1. What future use requires this knowledge?
2. What happens if it is forgotten or confused?
3. Is exact wording required or is semantic reconstruction enough?
4. Can it be cheaply referenced instead?
5. Does the lesson/domain mark it as foundational, repeatedly used, source-critical, assessment-critical or action-critical?
6. What recurring review cost will it add?
7. What observable evidence will count as retained?

Default: **do not turn every note into a study target**.

## Study loop

Default professional loop:

`SELECT -> DEFINE ENDPOINT -> UNDERSTAND/ENCODE -> RETRIEVE -> CHECK/CORRECT -> RETRY -> SPACE -> DELAYED RETRIEVE -> TRANSFER/MAINTAIN`

This is a decision loop, not a fixed daily template.

Load `references/study-protocol.md` when:
- selecting targets;
- choosing retrieval format;
- scheduling/adjusting review;
- correcting failed recall;
- controlling review load.

## Initial understanding

Do not ask the learner to memorize words they do not understand unless the domain explicitly requires exact recitation independently of current conceptual depth.

For conceptual material:
- identify the core proposition;
- identify relations/conditions;
- explain in own words;
- compare against the source;
- then retrieve later.

Understanding does not itself prove long-term retention.

## Retrieval

When recall is the target, prefer active retrieval over passive rereading.

Choose the retrieval form from the endpoint:
- free recall;
- short answer;
- reconstruction;
- ordered recall;
- explanation;
- contrast/classification;
- application case;
- exact recall against verified wording.

Recognition can be useful, but recognition alone is weak evidence when independent recall is required.

## Correction and relearning

After a retrieval attempt:

1. compare with the source/domain authority;
2. identify omission, distortion, attribution error or retrieval failure;
3. correct the minimum necessary;
4. briefly restudy the correct target;
5. retrieve again;
6. schedule a later check.

Do not repeatedly rehearse a confident wrong answer.

## Spacing

Distributed practice is preferred for durable retention, but **no universal interval sequence is encoded**.

Never claim that `1-3-7-30`, `1-2-4-8`, or another fixed schedule is universally optimal.

Adjust the next review using:
- importance/consequence;
- target type;
- desired retention horizon;
- last retrieval success;
- error severity;
- number of delayed successful recalls;
- current review load.

Rules:
- repeated failure -> shorter gap and/or stronger encoding;
- easy repeated delayed success -> longer gap;
- exact/source-critical target -> stricter accuracy criterion;
- low-value high-cost item -> downgrade or retire.

If no learner data exists and an operational schedule is needed, use a **provisional starting schedule** and label it provisional.

## Successive relearning

For durable factual/definition targets, use repeated cycles of:
`retrieve -> correct -> later retrieve again`.

Do not grind excessive same-session repetitions when future spaced relearning is planned.

## Self-explanation

Use own-word explanation when the target is conceptual understanding/relations.

Do not force self-explanation for every item.
Do not allow self-generated explanation to replace authoritative exact wording where exactness matters.

## Generation

Learner generation is valuable when it stays inside the evidence boundary.

Safe examples:
- recall answer;
- own-word explanation;
- example/nonexample;
- causal relation;
- comparison.

Unsafe without source support:
- quotation;
- source identity;
- authenticity grade;
- consensus;
- domain rule/standard;
- exact religious/legal wording.

## Interleaving

Use interleaving when discrimination between similar categories/cases is a material learning goal.

Do not use it as a universal study improvement. Some materials/tasks do not benefit.

## Review-load control

Each active target creates future work.

Before adding a target:
- check whether another prompt already covers the same proposition;
- prefer one high-information retrieval prompt over cosmetic duplicates;
- keep low-value examples/reference details out of active review;
- protect foundational/high-consequence targets.

When backlog grows:
1. merge redundancy;
2. retire/downgrade low-value targets;
3. reduce unnecessary exact memorization;
4. preserve fidelity-critical items;
5. cap new target creation until load is sustainable.

## Mastery evidence

Use evidence appropriate to the endpoint:

- immediate correct retrieval = initial evidence only;
- delayed retrieval = retention evidence;
- independent explanation = understanding evidence;
- contrast/classification = discrimination evidence;
- varied case = application/transfer evidence;
- source comparison = exactness/fidelity evidence.

Do not call knowledge durable because:
- it looks familiar;
- rereading feels easy;
- multiple choice was correct;
- the learner says "понял";
- one immediate recall succeeded.

## Flashcards

Flashcards are a tool, not the study strategy.

Use them when the target is compact and retrieval-shaped.
Avoid them when:
- the item requires a large relational model;
- context/conditions are lost;
- the card becomes a mini-essay;
- several cards duplicate one proposition;
- exact wording is not source-verified;
- a case/application task would better match future use.

## Islamic lessons

Load `references/islamic-study-specialization.md`.

Governing rule:

`LEARN DURABLY WITHOUT CHANGING SOURCE, AUTHORITY, CONDITIONS OR MATERIAL DISAGREEMENT`

The skill may recommend a **study priority** based on the lesson, repetition, future use and domain cues.
It must not independently claim a **religious obligation to memorize**.

## Progress state

For longitudinal study, use `schemas/study-state.schema.json` or equivalent semantics.

Track only future-useful state:
- target;
- target type;
- source/provenance when material;
- current status;
- last retrieval result;
- error class;
- next review window;
- delayed success count;
- review-load pressure;
- retirement/downgrade decision.

Keep note-taking skill progress and knowledge-retention progress separate.

## Evidence stance

Evidence:
`architect/research/study-strategy/source-register-v0.1.md`

Use live research when:
- the user asks for latest learning-science evidence;
- a specific spaced-repetition algorithm/tool is being evaluated;
- a special population/accommodation claim matters;
- a domain is high-stakes;
- the user requests precise comparative effectiveness.

## Hard failures

- memorizing everything by default;
- universal fixed review schedule;
- flashcards as the default representation for all knowledge;
- recognition/familiarity treated as durable mastery;
- one same-session success treated as long-term retention;
- failed recall not corrected against source;
- paraphrase converted into exact memorization target;
- learner-generated wording presented as authoritative source wording;
- domain/religious obligation invented by generic study strategy;
- material conditions/exceptions/disagreement removed from recall target;
- review backlog grows without pruning logic;
- taking over `learning-coach` pedagogy or `note-taking` representation;
- claiming T1/T2/T3 validation without evidence.

## Qualification boundary

Project-use candidate below T1.
Pre-SKILL gate PASS authorizes assembly only.
T1 requires independent held-out practical evaluation.
T2 requires independent strong-practitioner validation.
T3 requires representative monitored field evidence.
