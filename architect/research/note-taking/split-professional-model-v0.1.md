# Note-Taking — split professional model v0.1

Status: PRE-SKILL RESEARCH
Date: 2026-09-23
Target: reusable domain skill `note-taking`

## Architecture decision

The previous `lecture-note-taking-coach` combines two distinct responsibilities:
1. pedagogy / skill acquisition;
2. note-taking domain judgment.

This creates coupling: a change in teaching sequence can be buried inside note-taking rules, and note-taking logic can accidentally dictate pedagogy.

Decision:
- extract pedagogy into `learning-coach`;
- retain and adapt note-taking expertise into `note-taking`;
- compose them when the user wants to **learn** note-taking;
- allow `note-taking` alone when the user wants analysis, critique, structure selection, or documentation rather than coaching.

Reuse classification: **ADAPT** from `lecture-note-taking-coach@0.1.0-candidate`.

## Domain mission

Help select, structure, compress, preserve, revise, and retrieve information from spoken or written learning material without forcing a universal template.

The domain skill owns:
- information-role classification;
- importance and support distinctions;
- exactness vs paraphrase;
- hierarchy and relation capture;
- format routing;
- capture/revise/retrieve mechanics;
- note quality diagnosis;
- source-fidelity rules for specialized domains.

It does **not** own the pedagogical sequence for teaching the learner.

## Core decision model

For each material unit classify:
`CORE | DEFINITION | PROCEDURE | EVIDENCE | EXAMPLE | EXCEPTION | TRANSITION | LOW_VALUE`

Then choose:
`EXACT | COMPRESS | SYMBOLIZE | LINK | OMIT`

### EXACT
Use when wording/identity is material: formal definition, formula, rule, quotation, textual proof/reference, named condition/exception, critical number/date.

### COMPRESS
Preserve semantic skeleton, not surface grammar.

### SYMBOLIZE
Use compact notation only if later decodeability is preserved.

### LINK
Expose cause, contrast, sequence, dependency, category, exception, comparison.

### OMIT
Remove only content that does not materially support understanding, fidelity, or later retrieval.

## Structure-first routing

Do not choose a note format from preference or trend.

Infer content structure first:
- hierarchy/argument -> outline;
- repeated dimensions -> matrix/table;
- procedure/branching -> process/decision flow;
- dense relations -> sparse concept map;
- cue-based review -> Cornell-style container;
- mixed structure -> hybrid.

No format is universal.

## Quality dimensions

- coverage of core propositions;
- fidelity;
- visible relations/hierarchy;
- appropriate compression;
- decodeability after delay;
- retrieval usefulness;
- exact-source integrity where material.

Shorter is not automatically better.

## Domain boundary with `learning-coach`

When the user asks "teach me to take notes":
- `learning-coach` owns entry state, sequencing, practice, feedback cadence, fading;
- `note-taking` supplies the task model, examples, error taxonomy, and success criteria.

When the user asks "make/repair/analyze these notes":
- `note-taking` may operate directly without the pedagogy layer unless skill acquisition is also requested.

## Islamic specialization

Islamic lessons add a transmission-fidelity requirement. The specialization must preserve distinctions among:
- Qur'an;
- hadith;
- athar/salaf;
- scholar;
- teacher explanation;
- learner inference/reflection.

Compression must not erase source identity, conditions, exceptions, disagreement, or attributed tarjih.

The specialization is a domain fidelity module, not a fixed page template.

## Anti-template principle

A note-taking system must be selected from the structure and purpose of the material. Avoid canned outputs such as:
- always 3 bullets;
- always Cornell;
- always "definition / example / conclusion";
- always a mind map;
- arbitrary compression targets.

Use decision rules and observable quality dimensions instead.
