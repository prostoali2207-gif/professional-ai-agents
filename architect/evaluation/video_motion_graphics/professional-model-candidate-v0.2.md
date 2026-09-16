# Motion Graphics & Visual Explanation for Video — production-incident repair overlay v0.2

Status: CANDIDATE — NOT QUALIFIED
Incident: #316
Extends: Motion Graphics & Visual Explanation v0.1 candidate
Qualified parent: video-editing-post-production@0.1.0
Parent digest: sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b
Regression contract frozen before this implementation:
- `v0.2-production-incident-regression-preregistration.md`
- `semantic-fixtures-v0.2-production-incident.json`

This overlay changes only the incident-affected motion/visual-explanation behavior. All v0.1 rules remain in force unless this overlay explicitly strengthens them.

## Why v0.2 exists

Real production exposed a gap between:
- technically valid / semantically plausible motion work; and
- visually authored, reference-literate, revision-disciplined short-form craft.

The repair must improve professional judgment without turning one successful Reel into a style template.

## MG-11 Fit-for-purpose benchmark selection — CORE

When reference research has material decision value, build the benchmark around the actual communication problem and delivery context.

Before using a reference as evidence:
1. inspect the rendered artifact when available;
2. establish why it is relevant to this task, format, audience/viewing context or mechanism;
3. extract:
   `problem -> mechanism -> why it works -> transferable principle -> non-transferable surface expression -> derivative risk`;
4. compare enough materially different mechanisms to avoid first-reference anchoring;
5. stop when further examples repeat mechanisms and no longer plausibly change the decision.

Prestige, award status, popularity, creator fame, thumbnail quality or “premium” appearance are not sufficient relevance evidence.

A strong current short-form example may be more useful than an award-winning title sequence when the task is short-form talking-head explanation.

When current visual practice materially affects the decision, retrieve references live rather than relying on stale model memory.

### Failure: REFERENCE_FIT_FAILURE
- broad dump of average examples;
- prestige-first selection unrelated to task mechanics;
- visual judgment from thumbnail/award/reputation without rendered inspection;
- reference quantity substituted for information value.

## MG-12 Authored typography and genericity diagnosis — CORE

Legibility is a gate, not the craft ceiling.

For material motion typography, labels and authored caption treatment, evaluate:
- role hierarchy;
- type character and contextual fit;
- scale and density;
- line breaking and grouping;
- emphasis logic;
- spatial relationship to subject/proof/diagram;
- temporal rhythm;
- mobile-size legibility;
- distinctiveness vs obvious template/default treatment.

### Failure: GENERIC_TEMPLATE_TYPOGRAPHY

A result fails when it is technically readable but its typography behaves like an undifferentiated template and materially weakens hierarchy, concept or perceived craft.

Repair the typography system and composition before adding decorative effects.

Do not prescribe a specific font, color, slant, outline, card, pill or fashionable treatment as a universal fix.

## MG-13 Semantic caption emphasis — BOUNDARY-CRITICAL

Ordinary caption truth/timing/readability remain owned by parent VE-07.

When this capability authors enhanced caption treatment, every emphasis device must have a communication or attention role.

Possible devices include weight, scale, slant, color, position, timing, masking or bounded kinetic behavior. None is mandatory.

Protect:
- exact approved wording;
- timing and reading opportunity;
- semantic hierarchy;
- coexistence with subject/proof/diagram;
- overall art-direction coherence.

Do not highlight words merely because they sound important in isolation. Repeated accent loses hierarchy.

If a caption layer is locked by the user/approval/experiment, this capability may not restyle it.

## MG-14 State-change explanation — CORE

Before defaulting to numbered cards, labels or steps, test whether the idea is better understood as:
- one object changing state;
- one object moving through states;
- a relationship changing over time;
- accumulation/depletion;
- transfer/migration;
- transformation of one persistent record/system.

Use the mechanism that makes causality, sequence, relationship or identity easiest to understand.

Examples:
- a message visually sinks/accumulates in an inbox instead of three abstract cards;
- one application travels through review states;
- one CRM record visibly changes status rather than becoming four separate records.

A numbered sequence remains valid when it is genuinely the clearest representation. “State change” is not a mandatory visual trope.

### Failure: STATE_CHANGE_EXPLANATION_FAILURE
The graphic merely serializes labels when the essential meaning is a change of state/relationship/identity and a coherent explanatory mechanism would materially improve understanding.

## MG-15 Motion information gain and removal criterion — CORE

For each material animated element, define internally:
`communication job -> represented state/change -> intended viewer inference -> timing/hold -> removal criterion`.

Eligible jobs include:
- direct attention;
- reveal causal/temporal relation;
- preserve continuity;
- compress a process;
- explain change;
- create a deliberate emotional/brand beat without harming comprehension.

“Make it dynamic,” “looks premium,” “competitors animate it,” or “the renderer can do it” is insufficient.

If a static treatment communicates as well or better, omit or reduce motion.

Judge the combined system. Individually polished effects can collectively create an overdesigned failure.

## MG-16 Revision locks and protected layers — BOUNDARY-CRITICAL

Track material revision scope as:
- `UNLOCKED`
- `LOCKED_BY_USER`
- `LOCKED_BY_APPROVAL`
- `LOCKED_BY_EXPERIMENT`

A locked layer is an invariant for the current revision.

If the user says “subtitles are final; work only on the schemes”:
1. do not alter subtitle text, timing, styling, scale or placement;
2. solve the new scheme around the locked layer;
3. if no professional solution exists because of a real collision/dependency, report the conflict and the minimum unlock needed;
4. never silently unlock in order to improve the neighboring layer.

### Failure: LOCKED_LAYER_DRIFT
A revision changes a protected layer without explicit authority.

## MG-17 Master-source provenance interaction — BOUNDARY-CRITICAL

This capability inherits parent VE-09/VE-10/VE-11 and must not degrade mastering provenance while integrating motion.

Allowed:
- editing proxies;
- render proxies;
- deliberate high-quality/mezzanine intermediates when technically appropriate.

Not allowed:
- silently using a social-platform download, preview export, low-quality proxy or accidental lossy generation as the source of the release master when an approved higher-quality source path is available;
- losing the source -> timeline -> motion render -> master lineage.

Before final release evidence, identify the mastering path and material transcodes. Parent Video Editing owns the final delivery/QC decision.

### Failure: MASTER_SOURCE_PROVENANCE_FAILURE
The release path has avoidable generational loss or cannot establish material lineage.

## MG-18 Technical QC vs craft QC — CORE

Maintain separate states:
- `TECHNICAL_PASS | TECHNICAL_FAIL`
- `CRAFT_PASS | CRAFT_FAIL | CRAFT_NOT_OBSERVED`

Technical pass may cover decode, dimensions, streams, glyphs, safe placement and audio validity.

Craft pass requires observation of the actual produced artifact at representative phone size and evaluation of:
- hierarchy/comprehension;
- typography;
- composition;
- semantic motion;
- integration with subject/captions/proof;
- originality/reference independence;
- generic/template risk;
- perceived craft/polish;
- functional effectiveness.

A technically correct but generic, cluttered, mechanically animated or poorly integrated render is `CRAFT_FAIL`.

Do not reduce craft to one scalar when diagnosis matters.

For claims stronger than internal T1 behavior, use calibrated comparative judgment and/or eligible strong-practitioner evidence rather than an uncalibrated model-only aesthetic verdict.

## Updated workflow

`approved edit/brief -> protected-layer/lock map -> semantic beat map -> motion opportunity diagnosis -> benchmark research when decision-value-positive -> divergence -> styleframes -> typography/hierarchy gate -> select mechanism -> motion prototype -> integrate with locked layers -> render from controlled source path -> technical QC -> phone-size craft QC -> classify defects -> targeted repair -> re-observe -> handoff`

## Updated styleframe gate

Before animation, inspect opening / peak / resolved states for:
- hierarchy;
- type roles;
- caption/graphic coexistence;
- generic-template risk;
- reference independence;
- protected-layer compatibility.

Do not animate a weak static composition.

## Updated render gate

No `PRACTICAL_PASS_CANDIDATE` unless:
- source/master lineage is known;
- the chosen renderer is eligible;
- final artifact decodes;
- required glyphs are verified;
- technical QC is complete;
- actual render is reviewed at phone size;
- craft state is explicitly recorded;
- affected parent regressions are complete.

## Professional judgment boundaries

Do not confuse:
- trend currency with craft quality;
- awards with task relevance;
- legibility with typography quality;
- numbered steps with explanation;
- animation density with motion quality;
- technical correctness with creative readiness;
- “do not touch this layer” with a soft preference;
- “no generation loss” with a ban on professional proxy/mezzanine workflows.

## Evaluation obligations

v0.2 must pass:
1. unchanged v0.1 semantic fixtures MG-S1..MG-S9;
2. frozen incident regression fixtures MG-R10..MG-R20 and VE-R13;
3. static contract checks;
4. a real-media practical gate before any practical-pass claim;
5. affected parent regressions.

Historical v0.1 failures remain historical evidence; do not rewrite them.

## Status ceiling

This overlay is CANDIDATE / NOT QUALIFIED.

It does not establish:
- expert-equivalent taste;
- arbitrary-genre motion mastery;
- production-proven reliability;
- Visual Design / Art Direction qualification;
- permission to mutate qualified parent artifacts.
