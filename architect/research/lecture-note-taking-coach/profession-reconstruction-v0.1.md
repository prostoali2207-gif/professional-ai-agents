# Lecture Note-Taking Coach — profession reconstruction v0.1

Status: PRE-SKILL RESEARCH
Date: 2026-09-23
Target: applied skill `lecture-note-taking-coach`

## Target work, not title

The target is not a transcription assistant and not a generic summarizer. It is the work of a learning-strategy instructor / note-taking coach who teaches a novice to extract structure from spoken lessons, compress information without losing meaning, create usable notes, and improve through feedback until the learner can do the work independently.

The user may currently find verbatim rewriting easier than deciding what matters. The skill must therefore train selection and compression explicitly rather than merely outputting a polished summary.

## Primary responsibilities

1. Diagnose the learner's current note-taking behavior from real samples.
2. Teach how to distinguish core idea, support, example, evidence, definition, procedure, exception, and filler.
3. Teach hierarchical organization while listening.
4. Train compression: phrase-level notes, symbols, abbreviations, paraphrase, and omission.
5. Preserve accuracy when exact wording matters.
6. Prevent overcompression that destroys meaning.
7. Teach two-pass work: capture during the lesson, then revise after.
8. Convert notes into retrieval cues/questions rather than passive rereading material.
9. Track skill progression and raise difficulty gradually.
10. Avoid doing all cognitive work for the learner when the training goal is independence.

## Core outputs

- diagnosis of a note sample;
- one or two priority errors, not an overwhelming critique;
- corrected example fragments with explanation;
- a targeted drill;
- a constrained next-lesson rule;
- a post-lesson revision protocol;
- a short recall/self-test;
- progress update based on observable behavior.

## Scope

### CORE
- lecture listening and information selection;
- note hierarchy and organization;
- paraphrase/compression;
- abbreviation/symbol systems;
- recognition of lecturer structure and verbal cues;
- post-lecture revision;
- retrieval-question generation;
- metacognitive monitoring of note quality;
- scaffolded instruction and fading of support.

### BOUNDARY-CRITICAL
- cognitive load during simultaneous listening/writing;
- language proficiency when the lecture language itself is difficult;
- domain specificity: some fields require formulas, exact definitions, quotations, or procedural steps;
- accessibility needs that may make transcription support appropriate.

### OUT OF SCOPE
- pretending verbatim transcription is always bad;
- guaranteeing exam performance from note format alone;
- forcing Cornell, outline, mapping, or any single template universally;
- replacing a lecturer's exact legal/religious/technical wording when exact wording is decision-critical;
- clinical diagnosis of attention or learning disorders.

## Difficult decisions

### D1 — What is worth writing?
A strong coach teaches decision rules based on the function of information, not word count.

### D2 — When should wording be exact?
Use exact wording for definitions, formulas, quoted evidence, named rules, textual proofs, or when the learner is explicitly studying wording. Otherwise prefer concise paraphrase.

### D3 — How much compression is enough?
Compression is successful only if the learner can reconstruct the idea later without inventing missing links.

### D4 — Should the learner write during the lesson or pause?
For recorded lessons, pausing can be used as scaffolding early, then reduced. For live lessons, use lighter capture and delayed revision.

### D5 — Which note format?
Choose based on information structure: outline for hierarchy/sequences; matrix/table for comparisons; map for relationships; question/cue format for review. Do not prescribe a format for aesthetic reasons.

### D6 — When should the AI intervene?
Prefer feedback, prompts, and constrained examples before producing the final note. Full reconstruction is allowed when the user asks for a reference answer or when source fidelity is the task rather than skill training.

## Expert-vs-average discriminators

A strong coach:
- diagnoses the decision failure behind over-writing;
- teaches one transferable rule at a time;
- separates capture quality from review quality;
- checks whether the learner can recall/reconstruct the idea;
- adapts to lecture type and language;
- fades scaffolding as competence rises.

A weak coach:
- says only "write less";
- provides a pretty template without teaching selection;
- rewrites the whole lesson for the user;
- judges notes by neatness or brevity alone;
- treats one method such as Cornell as universally superior.

## Verification evidence

Progress must be visible in behavior:
- lower unnecessary verbatim overlap while core ideas remain represented;
- clearer hierarchy and relationships;
- fewer missing decision-critical points;
- faster capture at similar fidelity;
- better ability to explain the lesson from notes;
- better delayed recall/retrieval from cues;
- declining dependence on coach prompts.

## Architecture choice

Use one applied coaching skill with staged references and a learner-state schema. Multi-agent separation is unnecessary because diagnosis, instruction, practice, feedback and progression depend on the same learner state.
