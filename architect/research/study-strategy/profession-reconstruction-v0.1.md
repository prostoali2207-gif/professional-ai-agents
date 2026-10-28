# Study Strategy — profession reconstruction v0.1

Status: PRE-SKILL RESEARCH
Date: 2026-10-28
Target: reusable applied capability `study-strategy`

## Target work, not title

The target is not a generic "study tips" persona and not a flashcard generator.

It is a bounded **durable knowledge-acquisition / study-strategy specialist** that helps a learner decide what knowledge deserves active memory investment, how it should be encoded/retrieved/reviewed, and what evidence is sufficient to treat it as retained.

Primary output: **durable, retrievable, correctly scoped knowledge with controlled review cost**.

## Responsibility boundary

### Owns
- classify study targets by the kind of knowledge that must be retained;
- decide whether an item should be reference-only, understood, actively recalled, memorized exactly, discriminated from similar items, or applied;
- design retrieval prompts that match the target;
- combine retrieval with corrective feedback/restudy;
- distribute practice over time without pretending one fixed interval schedule is universal;
- use cumulative review and delayed checks;
- track evidence of retention and review burden;
- retire, downgrade, or re-scope low-value items.

### Does not own
- generic skill-acquisition pedagogy and scaffolding -> `learning-coach`;
- live capture, note structure, compression -> `note-taking`;
- religious/legal/medical/etc. authority over what is doctrinally obligatory or exact -> relevant domain owner;
- exact religious quotations from uncertain memory.

## Entry states

- `NEW_MATERIAL` — lesson/source just studied.
- `TARGET_SELECTION` — decide what deserves memory investment.
- `INITIAL_ENCODING` — learner has not yet shown recall.
- `RETRIEVAL` — active recall is due.
- `RELEARNING` — failed/partial recall needs corrective study + retry.
- `DELAYED_CHECK` — retention after time gap.
- `TRANSFER` — apply/reconstruct in a changed context.
- `REVIEW_LOAD` — too many items/reviews compete for time.
- `MAINTENANCE` — knowledge is stable and review frequency can be reduced.

## Core knowledge-target model

Do not ask "Should this be memorized?" as a binary question.

Classify the required endpoint:

- `REFERENCE_ONLY` — useful to keep accessible, low value to actively memorize.
- `UNDERSTAND` — learner must explain meaning/relationship in own words.
- `RECALL` — learner should retrieve a proposition, label, list, or relationship without seeing it.
- `EXACT` — wording/sequence/identity itself matters; exact target must come from an authoritative verified source/domain requirement.
- `DISCRIMINATE` — distinguish similar concepts, cases, conditions, or sources.
- `APPLY` — use knowledge in a problem/case/decision.
- `EVIDENCE_CHAIN` — reconstruct claim -> evidence -> reasoning -> conditions/exception/attribution where material.

One item may require more than one endpoint.

## Memory-investment decision

Before creating review work, ask:
1. What future use requires this knowledge?
2. Does failure to retrieve it matter?
3. Is exact wording required, or is semantic reconstruction sufficient?
4. Can it be cheaply referenced when needed?
5. Does the domain owner mark it as foundational, source-critical, repeatedly used, or assessment-critical?
6. What review cost will this item add?
7. What evidence would show it is retained?

Do not turn every note into a memory target.

## Evidence-informed learning loop

Default professional loop:

`SELECT TARGET -> DEFINE ENDPOINT -> INITIAL UNDERSTANDING -> RETRIEVE -> FEEDBACK/CORRECT -> RETRY -> SPACE -> DELAYED RETRIEVE -> TRANSFER/MAINTAIN`

This is a decision loop, not a rigid schedule.

## Retrieval principles

- Retrieval is a learning event, not merely an exam.
- Prefer effortful recall when recall is the goal; recognition alone can overstate mastery.
- Correct errors after retrieval using the source/domain authority.
- Do not keep testing corrupted wording without correction.
- Use prompts that match the target type: free recall, cue recall, explanation, discrimination, reconstruction, application.
- A single immediate successful recall is insufficient evidence of durable retention.

## Spacing principles

Distributed practice generally supports longer retention better than massing, but optimal gaps depend on retention horizon, material, prior success, and relearning.

Therefore:
- do not encode `1-3-7-30` or another fixed schedule as universal;
- schedule a next review far enough to require retrieval, but not so far that repeated failure makes learning inefficient;
- use observed recall quality and desired retention horizon to adjust;
- reduce frequency when delayed recall is consistently strong;
- bring review forward when important material repeatedly fails.

Simple defaults may be offered only as clearly provisional starting points when the user needs an operational schedule and no individualized data exists.

## Successive relearning

For durable factual/definition targets, repeated cycles of retrieval to criterion across separated sessions can be useful.

Do not waste large amounts of time overlearning one item in the first sitting if future relearning sessions are planned. Prefer successful retrieval plus later spaced relearning.

## Understanding / self-explanation

For conceptual relations, the learner should explain or reconstruct connections, not only recite labels.

Self-explanation can support learning, but prompts must fit the domain and target. Do not force explanation when exact verbatim recall is the actual endpoint, and do not let self-generated explanations replace authoritative source wording when exactness matters.

## Generation

Learner generation can improve memory, but it must not become uncontrolled invention.

Generate:
- recall answers;
- summaries in own words;
- examples;
- discriminations;
- causal/relational explanations.

Do not generate:
- quotations;
- source identities;
- doctrine/standards;
- authenticity grades;
- exact legal/religious wording.

## Interleaving

Interleaving can help discrimination/induction in some domains, especially where similar categories must be distinguished. Evidence is not universal across all material.

Use when the learning target benefits from comparison/discrimination.
Do not interleave merely because it is fashionable.

## Review-load control

A study system fails if review demand grows faster than available time.

When review load is high:
1. protect high-consequence/foundational targets;
2. suspend or downgrade low-value exact memorization;
3. merge redundant prompts;
4. reduce duplicated cues for the same proposition;
5. move reference-only material out of active review;
6. preserve fidelity-critical items even if they are fewer.

## Mastery evidence

Use multiple evidence levels:
- immediate retrieval;
- delayed retrieval;
- reconstruction without notes;
- discrimination against plausible confusions;
- application/transfer when relevant;
- exactness check for exact targets.

Do not infer durable mastery from:
- familiarity;
- rereading ease;
- recognition;
- one same-session correct answer;
- confidence alone.

## Composition

### With `learning-coach`
`study-strategy` owns the knowledge-retention decisions and success criteria.
`learning-coach` owns how the learner is taught to perform those decisions independently.

### With `note-taking`
`note-taking` produces a faithful, structured representation of the lesson.
`study-strategy` decides which parts become active study targets and which remain reference notes.

### With domain specialization
The domain owner decides whether exactness, source identity, conditions, disagreement, or particular items are materially required.
`study-strategy` must not manufacture these requirements.

## Islamic-study boundary

For Islamic lessons:
- preserve source/authority distinctions inherited from the note-taking specialization;
- do not independently label something religiously obligatory to memorize;
- do not convert a paraphrase into an exact memorization target;
- exact Qur'an/hadith/scholar wording must be verified or sourced before exact-memory drills;
- conditions, exceptions, disagreement and attributed tarjih must not disappear from recall prompts when they materially qualify the point;
- the learner's own explanation must remain distinguishable from transmitted content.

## Expert-vs-average discriminator

Average "study advice" often:
- flashcardizes everything;
- prescribes fixed intervals;
- rewards familiarity;
- overuses multiple choice;
- treats one successful recall as mastery;
- ignores source fidelity;
- creates so many review items that the system collapses.

Strong study strategy allocates memory effort by future use and consequence, matches practice to target type, uses delayed evidence, corrects errors, and controls review load.

## Reuse decision

Existing `learning-coach` and `note-taking` are adjacent capabilities but neither owns durable knowledge-target selection and review scheduling.

Decision:
- `learning-coach`: **REUSE as composition dependency**, not extend;
- `note-taking`: **REUSE as upstream representation dependency**, not extend;
- `study-strategy`: **BUILD NEW** as a separate responsibility boundary.

Reason: merging retention strategy into either existing skill would recreate the coupling problem already repaired in the note-taking architecture.
