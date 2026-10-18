# Automotive Capture Direction — Real-Still Development Practical v0.1

Status: DEVELOPMENT ONLY / NOT HELD-OUT / NOT QUALIFICATION EVIDENCE
Issue: #229
Candidate: `professional-model-candidate-v0.1.md`
Source: user-authorized project Google Drive imagery

## Purpose

Test the capability on real automotive photographs rather than only textual hypotheticals. The images are used strictly as capture artifacts. Their age, vehicle identity, ownership, availability, price, condition and other business facts are out of scope and must not be inferred.

This development set is intentionally public and may be used for candidate diagnosis. It must not later be relabeled as hidden qualification evidence.

## Source handling

The source files remain in Google Drive; this repository stores identifiers and observable task framing only. Do not copy the private/project media into the reusable professional-core repository merely to make the fixture self-contained.

At execution time the evaluator must retrieve and actually inspect the image. If the evaluator cannot observe the image bytes, the artifact-first claim is `NOT EXECUTABLE`; filename/metadata-only reasoning does not count.

### Asset S01

- Drive file: `IMG_5909.JPG`
- Drive file ID: `1BnTC23GcdEY56XiKjkBfpwu4c7NLQNad`
- MIME: `image/jpeg`
- Development task: treat the image as a proposed exterior front-three-quarter hero/source frame. Diagnose whether it should be accepted for a professional automotive social capture package and, if not, give the smallest high-value reshoot corrections.
- Evaluator-observable features to verify before judgment: a red coupe occupies the center/lower frame; urban buildings, roadway, railings and vehicles form the background; reflective dark hood/body surfaces show environment reflections; foreground vegetation intrudes along the lower edge.
- Required judgment dimensions: subject/background hierarchy, camera height/distance/perspective, reflective-surface control, foreground intrusion, crop/composition, exposure/highlight preservation, operator-executable reshoot specificity.

### Asset S02

- Drive file: `IMG_5900.JPG`
- Drive file ID: `1d3T64XZD57AqL4MoFT1niawvdiCoIzM7`
- MIME: `image/jpeg`
- Development task: treat the image as another proposed exterior three-quarter hero/source frame from the same shoot. Diagnose it independently, then compare its camera/background/form decisions with S01 without assuming either is the correct reference.
- Evaluator-observable features to verify before judgment: the red coupe fills more of the frame; palm-lined urban environment is visible; strong environmental reflections are present on hood/glass/body; front wheel and side body are prominent.
- Required judgment dimensions: perspective and stance, environmental context vs distraction, reflection structure, car-to-background separation, crop/negative space, condition/proof neutrality, concrete reshoot direction.

### Asset S03

- Drive file: `IMG_5895.JPG`
- Drive file ID: `1A93ZdUu13jNHPvifJxK7_kxW15ovpSCA`
- MIME: `image/jpeg`
- Development task: treat this as a third exterior three-quarter candidate from the same shoot. Evaluate whether the changed viewpoint improves or weakens the intended hero/form job and identify the causal variables rather than choosing by vague preference.
- Evaluator-observable features to verify before judgment: more surrounding urban/palm environment is visible; camera viewpoint differs from S02; reflective hood/side/glass surfaces remain prominent; the full vehicle is clearly readable.
- Required judgment dimensions: camera height/distance/viewpoint, body proportion/form readability, background hierarchy, reflections, wheel/ground stance, exposure/color consistency, measurable correction if reshoot is warranted.

## Candidate response contract

For each asset, candidate output must include:

1. `observations` — only what is actually visible; no invented unseen defects/settings/equipment.
2. `shot_job` — assumed task from this fixture, not a new strategy.
3. `accept_or_reshoot` — `ACCEPT`, `ACCEPT_WITH_LIMITATION`, or `RESHOOT`.
4. `dominant_reasons` — ranked causal diagnosis, not generic aesthetic adjectives.
5. `preserve` — what is already working and should not be changed casually.
6. `reshoot_direction` — measurable physical instruction: camera position/height/distance or framing cue, vehicle/environment relation, reflection/background target and acceptance cue.
7. `equipment_assumptions` — explicit; unknown device features remain unknown.
8. `truth_safety_check` — confirm no condition/business facts or unsafe execution were invented.

## Development grading

### Deterministic hard fails

- claims a specific camera/lens/settings were used without source evidence;
- invents vehicle condition/history/equipment or current business state;
- claims to have inspected an artifact when image bytes were unavailable;
- gives unsafe road-positioning/moving-vehicle execution;
- proposes hiding a material visible condition issue in order to imply better condition.

### Professional-quality dimensions requiring calibration

Score comparatively rather than from one uncalibrated scalar judge:

- observation fidelity;
- causal diagnosis;
- perspective/form judgment;
- reflection/light judgment;
- composition/background judgment;
- restraint/preservation of already-good variables;
- operator executability;
- value of the proposed correction relative to reshoot cost.

A generic response such as “use golden hour, shoot lower, use 2x, remove reflections and make the background cleaner” does not by itself demonstrate professional judgment. The response must connect a visible artifact property to a causal change and a verifiable next-frame acceptance cue.

## Comparative task

After individual assessment, compare S01/S02/S03 and answer:

- which differences are caused by viewpoint/composition/environment rather than by the car itself;
- which visible reflections are distracting vs potentially useful for form;
- which one or two changes would provide the largest professional-quality improvement across the series;
- what should remain invariant in the next controlled reshoot;
- what additional on-location observation would be needed before prescribing a stronger lighting/reflection intervention.

There is deliberately no frozen “winner” in this public development case. The reference judgment must later be calibrated with a qualified automotive/commercial photography reviewer before any subjective release threshold is frozen.

## Current execution state

- Source retrieval through connected Google Drive: PASS during development on 2026-09-01.
- Artifact bytes visually inspectable in current development environment: PASS for S01/S02/S03.
- Candidate-v0.1 scored run against this set: NOT RUN.
- Calibrated practitioner reference: NOT CREATED.
- Hidden still practical: NOT AUTHORED/FROZEN.
- Release evidence: NONE.
