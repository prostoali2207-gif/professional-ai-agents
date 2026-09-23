# Note-Taking

Version: 0.1.0-candidate
Status: project-use candidate; below T1 until independent qualification

Pre-SKILL gate: `architect/evaluation/note_taking/pre-skill-gate-result-v0.1.json`

## Mission

Provide professional note-taking judgment: select what matters, preserve meaning and exactness, expose structure, compress appropriately, route format from the material, revise notes, and make them useful for retrieval.

This skill owns the **note-taking domain model**.

It does not own generic pedagogy. When the user wants to learn note-taking, compose with `learning-coach`.

## Trigger

Use when the user wants to:
- take notes from a lecture/lesson/video/podcast/text;
- analyze or improve their notes;
- decide what to record and what to omit;
- compress without losing meaning;
- choose a note structure;
- distinguish core ideas, evidence, examples, conditions, exceptions;
- revise rough notes;
- prepare notes for later recall;
- handle source-sensitive notes, including Islamic lessons.

If the objective is explicitly skill acquisition, invoke `learning-coach` as pedagogy owner and supply it with the note-taking task model.

## Reuse provenance

Adapted from `lecture-note-taking-coach@0.1.0-candidate`.

Research:
- `architect/research/note-taking/split-professional-model-v0.1.md`
- `architect/research/note-taking/composition-contract-v0.1.md`
- `architect/research/note-taking/source-register-v0.1.md`

## Core information-role model

For each incoming idea classify its function:

`CORE | DEFINITION | PROCEDURE | EVIDENCE | EXAMPLE | EXCEPTION | TRANSITION | LOW_VALUE`

Then choose an action:

`EXACT | COMPRESS | SYMBOLIZE | LINK | OMIT`

### EXACT
Preserve/verify exactness when wording or identity is material:
- formal definition;
- formula/theorem/rule;
- quotation;
- source-critical textual proof/reference;
- named condition/exception;
- critical number/date.

### COMPRESS
Use shorter wording while preserving the semantic skeleton.

### SYMBOLIZE
Use stable shorthand only when later decodeability remains high.

### LINK
Make the relation explicit:
- cause;
- contrast;
- sequence;
- dependency;
- category;
- exception;
- comparison.

### OMIT
Remove filler, duplicate restatement, and low-value material.

Do not omit merely to make notes look short.

## Structure-first routing

Before choosing a format, identify the structure of the material.

Load `references/method-routing.md` when routing format or compression.

Default mappings:
- hierarchy/argument -> outline;
- repeated comparison dimensions -> matrix/table;
- procedure/branches -> process/decision flow;
- dense conceptual relations -> sparse concept map;
- cue/question review -> Cornell-style container;
- mixed material -> hybrid.

These are routing heuristics, not mandatory templates.

## Main note lifecycle

`CAPTURE -> REVISE -> RETRIEVE`

### CAPTURE
Preserve the lesson's flow:
- topic/heading;
- core proposition;
- relation;
- material support;
- exact-source item;
- uncertainty marker.

Rough grammar is acceptable.

If something is missed, mark `...` or `?` and continue rather than losing the next section.

For recorded lessons, pausing/replay can be used when appropriate to the user's goal and stage.

### REVISE
After the segment/lesson:
- fill important gaps;
- expose hidden headings;
- compress long lines;
- remove repetition;
- connect relations;
- verify exact-source items;
- preserve conditions/exceptions;
- keep examples that materially support understanding.

Revision is not decorative recopying.

### RETRIEVE
Use notes to reconstruct:
- main ideas;
- relations among them;
- exact definition/rule where relevant;
- important evidence/conditions/exceptions.

A neat page that does not support reconstruction is not automatically a good note.

## Compression rule

Compress **surface wording**, not decision-critical meaning.

Prefer to remove, in order:
1. filler/rhetorical padding;
2. duplicate restatement;
3. redundant examples;
4. grammar that does not change meaning.

Be cautious with:
- conditions;
- exceptions;
- causal links;
- scope;
- negation;
- attribution;
- exact definitions;
- evidence identity.

## Cue detection

Treat structural language as information:
- first/second/third;
- main point;
- two reasons;
- in contrast;
- therefore;
- exception;
- definition;
- example;
- summary.

Convert such cues into structure rather than copying them as ordinary prose.

## Quality dimensions

Judge notes on:
- core coverage;
- fidelity;
- hierarchy/relations;
- appropriate compression;
- decodeability after delay;
- retrieval usefulness;
- exact/source integrity when material.

No universal numeric score is required.
Shortest notes are not automatically best.

## Anti-template rule

Never impose one default format across all material.

Reject claims such as:
- Cornell is always best;
- handwriting is always best;
- mind maps are always best;
- every lesson should become 3-5 bullets;
- every concept needs definition/example/conclusion;
- the same compression ratio fits all lessons.

Choose from the actual information structure, learning purpose, medium constraints, and fidelity requirements.

## Medium rule

Do not claim paper or keyboard is universally superior.

Choose based on:
- speed;
- distraction risk;
- diagrams/equations;
- structuring ability;
- accessibility;
- user preference;
- later revision/retrieval workflow.

## Learning composition

When the user says "научи меня конспектировать":
1. load `learning-coach`;
2. provide it the smallest current note-taking task model;
3. let `learning-coach` choose orientation/model/practice/feedback/fading;
4. diagnose the learner's note-taking attempt using this skill;
5. return domain error + decision rule + success criteria to the coaching layer.

Do not run a generic teaching sequence from this skill alone.

## Islamic lessons

When the material is Islamic knowledge, load:
`references/islamic-lesson-specialization.md`

The governing rule becomes:

`COMPRESS WITHOUT LOSING MEANING, SOURCE, AUTHORITY LEVEL, CONDITIONS, OR MATERIAL DISAGREEMENT`

Source fidelity outranks additional compression.

## Uncertainty

Never silently repair uncertain exact-source material from memory.

Mark uncertainty and verify when material.

## Evidence stance

Evidence:
`architect/research/note-taking/source-register-v0.1.md`

Use live research when:
- the user asks for latest note-taking evidence;
- a tool/product/medium comparison is current;
- accessibility claims are material;
- a high-stakes domain requires current standards.

## Hard failures

- choosing a format before understanding material structure;
- flattening hierarchy into a transcript/bullet dump;
- aggressive compression that drops conditions/exceptions/relations;
- presenting uncertain paraphrase as exact quotation;
- universal handwriting/Cornell/mind-map claims;
- optimizing for brevity or visual neatness rather than meaning/retrieval;
- when Islamic specialization is active: mixing Qur'an/hadith/scholar/teacher/learner layers;
- flattening material scholarly disagreement or unattributed tarjih;
- taking over pedagogy when `learning-coach` should own the learning sequence;
- claiming T1/T2/T3 validation without evidence.

## Qualification boundary

Project-use candidate below T1.
Pre-SKILL gate PASS authorizes assembly only.
T1 requires independent held-out semantic/practical evaluation.
T2 requires independent strong-practitioner validation.
T3 requires representative monitored field evidence.
