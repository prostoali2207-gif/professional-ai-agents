# Learning Coach × Note-Taking × Study Strategy — composition contract v0.1

Status: PRE-SKILL ARCHITECTURE
Date: 2026-10-28

## Responsibility owners

### `learning-coach`
Owns:
- teaching sequence;
- scaffolding;
- practice progression;
- feedback cadence;
- fading of help.

### `note-taking`
Owns:
- live capture;
- information roles;
- compression;
- structure;
- exact/paraphrase distinction;
- faithful revision.

### `study-strategy`
Owns:
- what becomes an active study target;
- target endpoint (understand/recall/exact/discriminate/apply/etc.);
- retrieval/relearning protocol;
- spacing decisions;
- delayed mastery evidence;
- review-load control.

### Domain specialization
Owns:
- what exactness/source/conditions/disagreement matter;
- domain-specific meaning and authority;
- what may be safely generalized.

## Lesson workflow

A lesson may flow through:

`SOURCE/LESSON -> NOTE-TAKING -> TARGET SELECTION -> INITIAL UNDERSTANDING -> RETRIEVAL -> CORRECTION -> SPACED REVIEW -> DELAYED CHECK -> TRANSFER/MAINTENANCE`

When the learner is being taught how to perform any stage independently, `learning-coach` controls the instructional scaffolding around that stage.

## Non-monolith rule

No one skill should silently take ownership of all three:
- teaching;
- note representation;
- durable study strategy.

If a failure occurs, route it:
- wrong coaching order -> `learning-coach`;
- wrong capture/compression/structure -> `note-taking`;
- wrong memory target/review protocol -> `study-strategy`;
- wrong domain attribution/exactness/importance -> domain specialization;
- coordination failure -> this contract/router.

## Islamic lesson workflow

For Islamic material:
1. note-taking preserves source layers and uncertainty;
2. study-strategy selects active memory targets only from source-supported material;
3. exact memorization requires verified exact wording/source when material;
4. study-strategy must not call something religiously obligatory to memorize merely because it is important for learning;
5. retrieval prompts preserve conditions, exceptions, disagreement, and attributed preference where those qualify the knowledge;
6. learner-generated explanations remain labeled as learner understanding, not transmitted tafsir/hadith/scholar wording.

## Project progress model

Across lessons, maintain:
- note-taking skill progress;
- study-strategy skill progress;
- active knowledge targets;
- delayed retention evidence;
- current main bottleneck;
- next learning objective.

Do not conflate:
- "I can take good notes" with "I retained the lesson";
- "I can recite it" with "I understand it";
- "I understand it" with "I can retrieve it later";
- "I recall the rule" with "I can apply it";
- "I generated an explanation" with "that explanation is authoritative source content".
