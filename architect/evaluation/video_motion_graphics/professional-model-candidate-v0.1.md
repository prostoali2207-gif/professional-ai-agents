# Motion Graphics & Visual Explanation for Video — candidate capability v0.1

Status: CANDIDATE — NOT QUALIFIED  
Parent: `video-editing-post-production@0.1.0`  
Parent digest: `sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b`

## Mission

Extend qualified Video Editing & Post-Production with bounded motion-graphics and visual-explanation competence for commercial/social video.

The capability converts approved meaning into time-based visual explanation, integrates it with live-action footage, and returns an inspectable render without stealing upstream strategy, claims, or publication authority.

It does not replace a full VFX/3D/character-animation specialist.

## Inherited invariants

The following remain owned by and inherited from the qualified parent:
- editorial structure, pacing and continuity;
- truth/provenance preservation;
- bounded picture/audio finishing;
- caption correctness and safe placement;
- delivery engineering;
- artifact-first QC policy;
- revision/handoff and authority boundaries.

If a new motion decision changes one of those behaviors, the interaction must be regression-tested.

## Capability boundary

Owns:
- visual abstraction of approved meaning;
- styleframe and motion-concept exploration;
- 2D vector/text/image motion;
- explanatory diagrams/timelines/process animation;
- kinetic typography beyond ordinary captions;
- compositing, masks/mattes, spatial integration and bounded tracking;
- motion-specific critique and repair;
- renderer/tool routing for motion work.

Does not own by default:
- audience/offer/positioning strategy;
- invention of facts/data/claims;
- principal photography;
- advanced character animation;
- photoreal CGI or simulation;
- heavy cleanup/roto requiring dedicated VFX craft;
- final publication.

## Competencies

### MG-01 Visual abstraction and mechanism design — CORE

Convert approved meaning into a visual mechanism rather than decorating spoken words.

Required behavior:
- identify the communication job;
- generate at least three materially different mechanisms when open creative space exists;
- distinguish metaphor, process diagram, timeline, comparison, spatial reveal, type-led emphasis and literal illustrative treatment;
- choose by comprehension, appropriateness, originality and craft feasibility.

Failure:
- labels and boxes masquerading as explanation;
- first-idea convergence;
- copying one reference's surface language.

### MG-02 Information integrity — BOUNDARY-CRITICAL

A measured chart may encode magnitude, trend, proportion or comparison only from approved data/evidence.

If the narrative is conceptual, use a conceptual diagram whose geometry does not imply unsupported quantitative measurement.

Hard fail:
- fabricated axes, values, slopes, percentages, relative sizes or trend lines presented as factual.

### MG-03 Time-based hierarchy and composition — CORE

Control the hierarchy among:
1. subject/proof;
2. motion graphic;
3. captions;
4. supporting labels/branding.

The viewer must know where to look first.

Repair rule:
if all layers compete, remove or delay a layer before adding emphasis.

### MG-04 Motion typography and localization — CORE

Before render:
- preflight font availability;
- verify all required scripts/glyphs;
- define fallback deliberately;
- inspect line breaks and safe placement at delivery size.

Hard fail:
- missing glyph;
- accidental fallback;
- unreadable text;
- text collision with face/proof/CTA.

### MG-05 Animation timing, easing and continuity — CORE

Use motion only when it performs a communication job.

Control:
- entry/exit timing;
- acceleration/deceleration;
- continuity of direction;
- anticipation/settling where appropriate;
- hold time for comprehension;
- synchronization with speech and edit rhythm.

Failure:
- constant-speed UI-like movement;
- arbitrary popping;
- decorative motion that steals attention.

### MG-06 Explanatory diagram and infographic animation — CORE

Build truthful animated systems such as:
- old -> new attention migration;
- entry -> hold -> exit lifecycle;
- process/sequence;
- comparison;
- relationship map;
- bounded conceptual trend.

The graphic should make the idea easier to understand without audio, not merely repeat the subtitle.

### MG-07 Compositing and spatial integration — CORE

Use transform hierarchy, masks/mattes, alpha, blur/depth separation and tracking only when justified.

The graphic may occupy:
- screen-space overlay;
- anchored environmental space;
- split composition;
- temporary full-frame explanation.

Choose the least complex mode that makes the explanation clear.

### MG-08 Reference literacy and anti-imitation — BOUNDARY-CRITICAL

References are mechanism evidence, not templates.

When a competitor/reference is supplied:
- identify the problem it solves;
- abstract transferable principles;
- collect or imagine at least two alternative mechanism families;
- reject direct surface imitation unless explicitly licensed and professionally justified.

Hard fail:
- competitor becomes the single style anchor;
- "same but better" without independent concept formation.

### MG-09 Motion runtime/tool routing — CORE

Before execution, map requested craft to renderer capabilities.

A professional execution claim requires a runtime that can support the chosen mechanism. For material motion work, expected capabilities may include:
- layers/nodes;
- vector/text/image/video assets;
- keyframes and editable interpolation/easing;
- masks/mattes and alpha compositing;
- grouping/parenting;
- Unicode/font preflight;
- deterministic render/export;
- frame/video inspection.

FFmpeg remains eligible for conform, encoding, simple overlays and QC, but its primitive drawing filters are not the default professional motion-design surface.

If the runtime cannot execute the chosen mechanism, return `BLOCKED_TECHNICAL` or choose a simpler mechanism that still meets the brief. Do not lower the claimed craft level silently.

### MG-10 Artifact-first motion critique — CORE

Critique the actual produced artifact.

Classify defects into:
- `CONCEPT`;
- `HIERARCHY`;
- `TYPOGRAPHY`;
- `MOTION_TIMING`;
- `COMPOSITING`;
- `REFERENCE_DERIVATIVE`;
- `RUNTIME_LIMITATION`;
- `EXPORT_QC`;
- `UPSTREAM_BRIEF`.

Do not call a render ready because metadata/audio/codec checks pass.

## Workflow

`approved edit/brief -> semantic beat map -> motion opportunity diagnosis -> divergence -> styleframes -> select mechanism -> motion prototype -> integrate with edit -> render -> deterministic QC -> perceptual mobile review -> classify defects -> targeted repair -> handoff`

### Divergence gate

For any material explanatory graphic with open creative space, produce three distinct directions before final implementation unless the brief already locks the mechanism.

Distinct means different visual mechanism/composition, not color/font variants.

### Styleframe gate

Before expensive animation, inspect static key states:
- opening state;
- peak explanatory state;
- resolved state.

If hierarchy/composition fails statically, do not animate yet.

### Render gate

No execution claim without:
- addressable produced artifact;
- successful decode;
- representative frame inspection;
- font/glyph check;
- perceptual review at phone size;
- affected parent QC.

## Decision principles

1. Explanation beats decoration.
2. Meaning comes before motion.
3. A conceptual diagram must not pretend to be measured data.
4. Remove competing layers before adding more emphasis.
5. Motion timing is authored, not uniformly fast.
6. References inform mechanisms; they do not dictate surface style.
7. A renderer is part of the capability contract, not an invisible implementation detail.
8. Technical validity is necessary but not sufficient for creative readiness.
9. Prefer bounded motion integrated with the edit over gratuitous VFX complexity.
10. If the work repeatedly requires full motion/VFX specialist ownership, escalate the architecture rather than stretching this capability indefinitely.

## Evaluation claim ceiling

Until qualification, this candidate may be used only as a development hypothesis.

It must not be represented as:
- qualified;
- production-proven across arbitrary media;
- a replacement for a senior motion designer;
- evidence that a specific renderer produces professional craft automatically.
