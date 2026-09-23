# Lecture Note-Taking Coach — knowledge packaging audit v0.1

Status: PRE-SKILL COMPLETE

## Decision-critical knowledge

| Dependency | Packaging | Reason |
|---|---|---|
| selection/compression rules | EMBED_CORE | used every session |
| exact-vs-paraphrase decision | EMBED_CORE | prevents fidelity failures |
| staged coaching progression | EMBED_CORE | core behavior |
| detailed coaching drills | PROCEDURAL_MODULE | load when training/practice |
| format routing and examples | REFERENCE_MODULE | useful when selecting format |
| evidence on medium/summarization/retrieval | REFERENCE_MODULE | needed for contested advice |
| current research updates | LIVE_RESEARCH | only when latest evidence is requested |
| learner progress/state | TOOL/STATE-BACKED | requires persistence across lessons |

## Progressive disclosure

Always-loaded SKILL should contain:
- mission;
- entry state;
- capture/revise/retrieve loop;
- core information-role model;
- coaching/fading rules;
- hard failures.

Load `references/coaching-protocol.md` for detailed drills, diagnosis, and progression.
Load `references/note-taking-methods.md` for format choice, symbols, examples, and exactness rules.
Use learner-state schema for longitudinal coaching.

## Knowledge not retained as universal rule

- mandatory compression percentage;
- fixed words-per-minute target;
- one best note template;
- handwriting superiority;
- prohibition on transcription in all contexts.

These claims are too context-dependent or unsupported as universal rules.
