# Study Strategy — competency and knowledge packaging v0.1

Status: PRE-SKILL MODEL
Date: 2026-10-28

## Competency map

| Competency | Class | Observable capability | Failure mode | Evaluation |
|---|---|---|---|---|
| Study-target selection | CORE | separates reference, understanding, recall, exact, discrimination, application targets | memorizes everything | mixed lesson fixture |
| Endpoint definition | CORE | states what successful knowledge looks like | vague "know this" | target conversion task |
| Retrieval design | CORE | uses recall task matched to target type | recognition-only / generic flashcards | varied target fixture |
| Corrective relearning | CORE | checks answer against source and repairs error before next cycle | rehearses wrong answer | error-repair fixture |
| Spacing judgment | CORE | adapts timing to horizon and recall evidence | rigid 1-3-7-30 dogma | schedule adversarial case |
| Delayed mastery check | CORE | requires evidence after delay | same-session success = mastery | longitudinal fixture |
| Transfer/discrimination | CORE | tests use/contrast when required | assumes recall = application | transfer fixture |
| Review-load control | CORE | protects high-value items and retires low-value review | review backlog explodes | constrained-time fixture |
| Source fidelity | BOUNDARY-CRITICAL | exact drills use verified authoritative wording | paraphrase memorized as quote | exact-source fixture |
| Domain composition | BOUNDARY-CRITICAL | domain owner controls importance/exactness requirements | generic study skill invents doctrine | Islamic/domain fixture |
| Coaching composition | BOUNDARY-CRITICAL | delegates teaching of the method to learning-coach | becomes monolithic tutor | composition fixture |

## Critical decision model

For each candidate item:

`FUTURE USE -> CONSEQUENCE OF FORGETTING -> REQUIRED ENDPOINT -> SOURCE/FIDELITY -> PRACTICE TYPE -> REVIEW COST -> MASTERY EVIDENCE`

### Examples

- Explanation repeated only as illustration -> likely `REFERENCE_ONLY` or `UNDERSTAND`.
- Core named principle used repeatedly -> `RECALL` + possibly `UNDERSTAND`.
- Source-critical wording explicitly required -> `EXACT` after verification.
- Similar conditions that are easily confused -> `DISCRIMINATE`.
- Rule whose use matters -> `UNDERSTAND + APPLY`.
- Claim with proof and conditions -> `EVIDENCE_CHAIN`.

These are task-shape examples, not domain authority claims.

## Practice router

### REFERENCE_ONLY
Keep in notes/index. No recurring active review by default.

### UNDERSTAND
Use:
- own-word explanation;
- relationship reconstruction;
- "why/how" prompt;
- simple concept comparison.

### RECALL
Use:
- free recall;
- short answer;
- cue recall;
- ordered reconstruction if order matters.

### EXACT
Use:
- exact-source prompt;
- compare against verified wording;
- immediate correction;
- repeated later exact recall.

### DISCRIMINATE
Use:
- paired contrast;
- classify examples/nonexamples;
- identify which condition/source applies.

### APPLY
Use:
- scenario/case;
- explain choice;
- vary surface features to test transfer.

### EVIDENCE_CHAIN
Use:
- reconstruct claim;
- source/dalil/evidence;
- reasoning link;
- conditions/exceptions;
- attribution/disagreement when material.

## Feedback / relearning protocol

After a retrieval attempt:
1. score against the source/domain authority;
2. identify omission, distortion, attribution error, or retrieval failure;
3. show only the correction needed;
4. restudy the correct target briefly;
5. retrieve again;
6. schedule a later check.

Do not reward fluency if fidelity is wrong.

## Spacing controller

Inputs:
- importance/consequence;
- target type;
- desired retention horizon;
- last retrieval success;
- error severity;
- number of successful delayed recalls;
- current review load.

Behavior:
- repeated failure -> shorten next gap and/or strengthen encoding;
- easy repeated delayed success -> lengthen;
- exact/source-critical target -> require stricter accuracy criterion;
- low-value item with high review cost -> downgrade/retire;
- no data -> use a provisional interval and state it is provisional.

Do not claim an exact optimal schedule from generic evidence.

## Review-load budget

Each new active target creates future cost.

Before adding:
- check whether another prompt already tests the same proposition;
- prefer one high-information prompt over several cosmetic variants;
- protect foundational/high-consequence items;
- allow reference notes to remain searchable instead of memorized.

## Knowledge packaging

### EMBED_CORE
- target classification;
- retrieval > recognition for recall goals;
- spacing is adaptive, not fixed;
- delayed evidence required;
- domain/source fidelity boundary;
- review-load control.

### PROCEDURAL_MODULE
- target-selection and practice router;
- failed-recall correction/relearning;
- review-load triage.

### REFERENCE_MODULE
- evidence summary and boundary conditions;
- examples of target types.

### LIVE_RESEARCH
Use when:
- the user asks for the latest learning-science evidence;
- a specific tool/algorithm claims optimal scheduling;
- special population/accommodation claims matter;
- a high-stakes domain introduces current requirements.

### TOOL_BACKED
Optional:
- flashcard/spaced-repetition systems for execution;
- calendar/task scheduler for reviews;
- learner progress store.

Tool use does not define the pedagogy.

## Progress state

Persist only future-useful evidence:
- active study targets and target type;
- source identity/provenance where required;
- last retrieval result;
- error class;
- next review window;
- number/quality of delayed successes;
- retirement/downgrade status;
- review-load pressure.

Do not store every rehearsal transcript.

## Hard boundaries

- no fabricated exact wording;
- no fixed universal review schedule;
- no indiscriminate flashcard creation;
- no religious/domain importance claim without domain support;
- no durable mastery claim from immediate recognition;
- no "learning style" personalization unless supported by direct performance evidence and relevant research.
