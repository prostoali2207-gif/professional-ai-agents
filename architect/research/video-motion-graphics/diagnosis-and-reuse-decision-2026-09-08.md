# Motion Graphics & Visual Explanation for Video — GAP diagnosis and reuse decision

Date: 2026-09-08  
Status: RESEARCH DECISION — capability not qualified; no parent-core mutation authorized

## Trigger / production incident

A real short-form talking-head edit exposed a repeated failure pattern:

- editorial structure, trimming, captions, audio leveling and export were technically adequate;
- visual explanation remained weak: static labels/lines substituted for professional motion graphics;
- a technical QC pass was incorrectly treated as sufficient evidence of creative readiness;
- one render exposed a Cyrillic font/glyph failure;
- reference comparison created anchoring and surface imitation instead of independent concept formation.

This incident is evidence for gap discovery, not proof of a universal solution.

## 1. Target work reconstructed

The target is **bounded motion graphics and visual explanation inside commercial/social video post-production**.

The work is not merely “add graphics.” It includes:

1. translate spoken or approved narrative structure into visual concepts that clarify meaning;
2. distinguish a true quantitative chart from a conceptual diagram/metaphor so visual form does not fabricate measurement;
3. design hierarchy, typography, composition and color for time-based media;
4. create styleframes / key visual states before polishing animation;
5. animate shapes, type, diagrams and visual emphasis with intentional timing, easing and spatial continuity;
6. composite graphics with live-action footage without fighting the subject, captions or proof;
7. use tracking/masking/mattes when the communication job requires them;
8. preserve brand/brief truth and reference originality;
9. inspect the produced artifact at representative mobile size and revise perceptual defects;
10. hand the result back into editorial finishing, delivery and QC.

Boundary: advanced character animation, photoreal CGI, complex VFX simulation, heavy 3D scene work and specialist cleanup remain escalation candidates rather than default scope.

## 2. Evidence that this is a real professional delta

### Film/video editing overlaps with graphics but does not fully subsume motion-design craft

O*NET 27-4032 Film and Video Editors (updated 2026) includes:
- organizing footage into a coherent whole;
- manipulating plot, sound and graphics;
- programming computerized graphic effects;
- working with visual/special-effects departments.

Source: https://www.onetonline.org/link/summary/27-4032.00

This supports retaining the existing Video Editing & Post-Production core as the parent for the integrated finished artifact.

### Motion Graphics Artist exists inside a distinct animation/effects occupational family

O*NET 27-1014 Special Effects Artists and Animators explicitly lists **Motion Graphics Artist** among reported titles and includes:
- designing complex graphics and animation with independent judgment and creativity;
- creating 2D/3D images that depict motion or illustrate a process;
- manipulating light, color, texture, shadow and transparency;
- scripting/planning animated sequences.

Source: https://www.onetonline.org/link/summary/27-1014.00

BLS likewise separates Special Effects Artists and Animators from Film and Video Editors and describes the former as creating moving images and visual effects.

Sources:
- https://www.bls.gov/ooh/arts-and-design/multimedia-artists-and-animators.htm
- https://www.bls.gov/ooh/media-and-communication/film-and-video-editors-and-camera-operators.htm

This is evidence that substantial motion-graphics work has its own craft boundary even when it is integrated into post-production.

### Tool vendors also separate editing from motion graphics / compositing

Adobe distinguishes Premiere’s editing role from After Effects, which it positions for professional-quality motion graphics, animation and visual effects.

Source: https://www.adobe.com/creativecloud/video.html

Blackmagic’s official DaVinci Resolve training separates Edit from Fusion. Fusion training covers motion graphics, compositing, tracking, keying, shapes, cameras, lights and 2D/3D rendering.

Source: https://www.blackmagicdesign.com/products/davinciresolve/training

These are vendor-specific implementation sources, not universal aesthetic authority, but they strongly support the runtime/tool distinction.

## 3. Trusted-library reuse inspection

### Candidate A — `video-editing-post-production@0.1.0`

Qualified digest: `sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b`

**Retain / compatible invariants**
- editorial structure and pacing;
- truth/provenance preservation;
- picture/audio finishing;
- caption correctness and safe placement;
- delivery engineering;
- artifact-first QC policy;
- authority and revision routing.

**Material delta not qualified by parent**
- visual abstraction / explanatory graphic concept formation;
- graphic-design fundamentals applied to moving media;
- styleframe development and composition;
- animation timing/easing and motion continuity;
- kinetic typography beyond bounded captions/titles;
- infographic/process animation;
- compositing/tracking/masking craft;
- motion-specific critique and taste;
- capable motion-graphics render/runtime contract.

The parent qualification explicitly states that it does **not** prove real-media editorial taste, broad NLE operation or reliable perceptual inspection of arbitrary footage.

**Decision: EXTEND through a bounded candidate capability.**

Do not rewrite or invalidate the qualified parent. Preserve its evidence for unchanged invariants.

### Candidate B — `social-content-creative@0.1.0`

Useful upstream coverage:
- visual storytelling;
- message sequencing;
- shoot direction;
- bounded creative concept generation.

Its manifest explicitly excludes video editing, rendering, finishing and perceptual QC.

**Decision: REUSE as upstream brief/handoff only; REJECT as the motion-graphics execution parent.**

### Candidate C — Visual Design / Art Direction research track

Current repository work is landing-page-specific and not a qualified library core. It contains useful creative-architecture ideas such as divergence, hierarchy and artifact-first critique, but it does not establish portable motion-video competence.

**Decision: REJECT direct inheritance; retain only as non-authoritative research/reference where compatible.**

### BUILD NEW top-level Motion Designer core

A separate occupational family exists, so BUILD NEW is plausible for full-scope motion/VFX work. However the current need is a bounded slice integrated into short-form post-production and shares final-render, editorial, truth, delivery and QC ownership with the qualified parent.

**Decision: REJECT BUILD NEW for now as premature architecture.**

Reopen BUILD NEW only if targeted evaluation shows the capability needs materially different stable judgment/workflow/ownership that cannot be composed cleanly with Video Editing & Post-Production.

## 4. Architecture decision

### Primary decision

`Video Editing & Post-Production@0.1.0 + Motion Graphics & Visual Explanation capability candidate -> EXTEND`

This is an architecture/research decision, **not a qualification PASS**.

The capability should remain modular so it can later be:
- retained inside the video post-production system if composition works;
- split into a separate professional core if evaluation proves a distinct profession boundary is operationally necessary.

## 5. Candidate capability competencies

### MG-01 Visual abstraction and concept formation — CORE
Convert approved meaning into a visual mechanism instead of decorating words.

Discriminator: generates materially different explanatory mechanisms and selects by communication value, not trend/style imitation.

### MG-02 Information integrity — BOUNDARY-CRITICAL
Distinguish measured charts/data graphics from conceptual diagrams, timelines and metaphors.

Hard fail: visual encodes invented quantities, relative magnitudes or trends as factual evidence.

### MG-03 Motion composition and hierarchy — CORE
Control subject, typography, shapes, contrast, negative space and visual priority across time.

Discriminator: viewer can tell where to look first without graphics competing with speech/captions.

### MG-04 Typography in motion / localization — CORE
Control font coverage, line breaks, scale, timing and script support.

Hard fail: missing glyphs, fallback corruption, unreadable mobile typography or text collisions.

### MG-05 Animation timing and easing — CORE
Use keyframes, interpolation/easing, anticipation/settling and motion continuity intentionally.

Discriminator: animation feels authored and supports comprehension rather than looking like mechanical UI movement.

### MG-06 Explanatory diagrams / infographic animation — CORE
Build animated timelines, process maps, comparisons and conceptual flows with semantically meaningful motion.

### MG-07 Compositing and spatial integration — CORE
Integrate graphics into footage using transforms, masks/mattes, occlusion and tracking where justified.

### MG-08 Reference literacy / anti-imitation — BOUNDARY-CRITICAL
Extract mechanisms from multiple references without using one competitor as a surface template.

Adversarial trap: “make ours like this competitor but better.”

### MG-09 Runtime/tool judgment — CORE
Choose a renderer that actually supports the required craft; do not use FFmpeg primitives as the default motion-design engine merely because they are available.

### MG-10 Artifact-first motion critique — CORE
Inspect the produced animation, not only code/timeline/metadata. Separate concept, craft, compositor, font, renderer and export failures.

## 6. Root-cause classification of the observed failure

### A. Professional-model GAP
The parent has `VE-07 Text, captions and graphics` and `VE-08 Effects, motion and transitions`, but those clauses are intentionally bounded. They do not model full motion-graphics craft.

### B. Runtime/tool GAP
The actual execution path used FFmpeg `drawtext/drawbox` as the primary design renderer.

FFmpeg remains appropriate for deterministic transforms, conform, encoding and QC. It is not sufficient evidence of a professional motion-design execution surface.

Required motion runtime features include:
- layers/nodes and reusable vector/text/image/video assets;
- keyframes plus editable easing/curves;
- masks/mattes and alpha compositing;
- transform parenting/grouping;
- reliable Unicode/font preflight;
- deterministic render/export;
- frame/video inspection;
- optional tracking/3D only when justified.

Eligible implementation families may include Fusion, After Effects, or a comparably capable programmable motion renderer. Tool selection is a later implementation decision, not part of the profession invariant.

### C. Evaluation GAP
The current parent qualification states that synthetic FFmpeg rendering does not establish:
- real-media editorial taste;
- broad NLE operation;
- reliable perceptual inspection of arbitrary footage.

The observed incident falls exactly inside those exclusions.

### D. Process GAP
Creative-profession methodology requires divergence before convergence and explicitly warns against reference copying. The competitor-anchored pass violated that design principle.

## 7. Targeted evaluation required before promotion

Do **not** rerun the old Video Editing core from zero. Preserve evidence for unaffected parent invariants.

### Semantic / judgment families

1. **EXPLAIN** — choose an explanatory visual mechanism from a spoken concept.
2. **DATA_TRUTH** — distinguish conceptual illustration from measured chart; refuse invented quantitative encoding.
3. **HIERARCHY** — detect subject/caption/graphic competition and repair the responsible layer.
4. **MOTION** — choose timing/easing/spatial behavior that serves comprehension.
5. **TYPE** — multilingual font/glyph/readability failure.
6. **REFERENCE** — resist competitor-style imitation while extracting transferable principles.
7. **COMPOSITE** — decide when tracking/masks/occlusion are justified.
8. **TOOL_ROUTE** — recognize when the renderer cannot produce the requested professional result.
9. **CRITIQUE** — observe an actual weak render and diagnose concept vs execution vs runtime failure.

### Practical real-media gate

Use a real talking-head source and require three authored visual explanations:

1. **attention migration** — old project -> new project;
2. **investment lifecycle** — entry / hold / exit as a coherent animated system;
3. **CTA transition** — restrained motion that resolves cleanly back to the speaker.

Requirements:
- create at least 3 genuinely different styleframe/mechanism directions before selecting one;
- no competitor video may be the primary reference/template;
- render the actual sequence;
- inspect at representative phone size;
- verify Cyrillic glyph coverage;
- run deterministic export/audio checks;
- run perceptual review by multiple independent judges or a calibrated expert process;
- separate concept, appropriateness, originality, craft and functional effectiveness;
- user approval is useful production evidence but is not the sole professional qualification oracle.

### Interaction regressions with parent

At minimum target affected interactions with:
- VE-02 pacing/comprehension;
- VE-07 text/captions/graphics;
- VE-08 effects/motion;
- VE-09 reproducibility/font/assets;
- VE-11 artifact-first QC;
- VE-12 revision/root-cause repair.

Broaden only if coupling evidence justifies it. Do not weaken existing thresholds.

## 8. Promotion / stop rule

### Keep as capability inside Video Post-Production if:
- the new motion competencies pass targeted semantic and practical evaluation;
- the composed system maintains clear failure ownership;
- one workflow can coherently own edit -> motion integration -> finish -> QC;
- runtime/tool complexity remains bounded and reproducible.

### Consider BUILD NEW Motion Graphics professional core only if:
- motion concept/taste/workflow repeatedly dominates the task rather than remaining a bounded post-production delta;
- separate specialist ownership materially improves reliability;
- composition with the editor causes routing ambiguity or coupling failures;
- representative motion tasks outside short-form post-production reveal a coherent reusable profession larger than the extension.

## 9. Current verdict

**Diagnosis: confirmed material GAP.**

**Architecture: EXTEND the existing Video Editing & Post-Production system with a candidate `Motion Graphics & Visual Explanation` capability.**

**Do not create a new professional core yet.**

**Do not claim the capability is ready until the real-media practical gate passes.**
