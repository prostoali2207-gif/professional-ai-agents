# Learning Coach × Note-Taking — composition contract v0.1

Status: PRE-SKILL ARCHITECTURE
Date: 2026-09-23

## Responsibility boundary

### `learning-coach` owns
- learner entry state;
- instructional sequencing;
- size of explanation/model;
- practice choice and progression;
- feedback cadence;
- retry/transfer design;
- fading of support.

### `note-taking` owns
- what counts as a note-taking decision;
- information-role classification;
- exact/compress/link/omit rules;
- structure recognition;
- format routing;
- note-quality diagnosis;
- domain-specific fidelity.

## Composition rule

When the user wants to **learn note-taking**:

1. `learning-coach` asks the domain skill for the smallest task model needed now.
2. `note-taking` returns the relevant decision rule + authentic tiny example + success criteria.
3. `learning-coach` decides how much of that to expose before practice.
4. learner attempts;
5. `note-taking` diagnoses domain errors;
6. `learning-coach` chooses the single next instructional target and retry;
7. repeat with fading.

The pedagogy layer must not invent note-taking rules.
The domain layer must not force a teaching sequence.

## True-beginner invariant

If the learner says they have no usable note-taking method:
- do not request an unsupported baseline first;
- give a compact task model;
- show one tiny modeled contrast;
- run a short guided attempt;
- diagnose from the attempt;
- then continue with targeted coaching.

## Non-template invariant

Neither skill may force a fixed lesson or page format merely because it was used previously.

The response shape must be derived from:
- learner state;
- material structure;
- active bottleneck;
- domain fidelity constraints;
- current stage of support/fading.

## Islamic lesson composition

When the source is Islamic learning material:
- load the Islamic fidelity module from `note-taking`;
- preserve source/authority distinctions and uncertainty;
- `learning-coach` may teach those distinctions but may not independently adjudicate religious claims;
- if religious verification is required, use the Islamic domain authority/source process separately.

## Failure routing

If the failure is:
- wrong teaching order -> repair `learning-coach`;
- wrong note selection/compression/format -> repair `note-taking`;
- wrong religious attribution/fidelity -> repair Islamic note-taking specialization or religious source layer;
- wrong composition/delegation -> repair this contract/router;
- one-off phrasing -> do not patch architecture unless repeated/systemic.
