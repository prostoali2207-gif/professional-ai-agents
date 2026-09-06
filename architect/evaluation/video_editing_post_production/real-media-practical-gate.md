# Real-Media Practical Gate — Video Editing & Post-Production

Status: evaluation extension. This file does not change the qualified claims of `video-editing-post-production@0.1.0`.

## Purpose

Close the evidence gap between correct editorial decision policy and observable execution on real footage. Use this gate before claiming real-media editorial craft, perceptual QC, broad NLE/runtime portability, or an applied composition whose acceptance depends on the quality of an exported video.

A production failure is evidence. Classify it before changing the professional core.

## Freeze before execution

Freeze before editing:
- exact source asset IDs/hashes and included/excluded set;
- fixed creative brief and delivery target;
- truth/fact references and forbidden transformations;
- allowed editorial degrees of freedom;
- failed baseline artifact(s);
- runtime/tool versions;
- reviewer rubric and decision rule.

Do not tune the brief, baseline, rubric, or threshold after seeing the candidate.

## Required candidate evidence

The candidate must provide the actual exported artifact and an execution manifest containing:
- source-to-timeline lineage and selected in/out points;
- ordering, crop/reframe/stabilization/retime decisions;
- picture/color and audio transforms;
- graphics/captions with factual provenance;
- export settings, tool/runtime versions and output hash;
- deviations and unresolved limitations.

An edit plan, command log or timeline screenshot is not a substitute for the exported artifact.

## Deterministic gate

All applicable checks must pass:
1. decode start-to-finish;
2. expected video/audio streams exist for the declared mode;
3. dimensions, frame rate, duration, codec/container and color metadata match the frozen delivery target;
4. no unintended black/frozen intervals or truncated head/tail;
5. no unintended clipping, missing audio, sync break or undeclared silence;
6. hashes/lineage are recorded;
7. every material graphic/claim resolves to frozen authoritative evidence;
8. no forbidden asset or different vehicle/product is introduced.

This proves technical integrity only, not craft.

## Perceptual craft rubric

Score each item 0–4 against the frozen brief:
- **selection** — strongest usable moments chosen; weak/redundant footage omitted;
- **pacing** — shot duration and energy support comprehension and intended rhythm;
- **continuity** — spatial/action/semantic progression feels intentional;
- **stabilization / reframing / retiming** — benefit exceeds crop, warping, judder or truth risk;
- **picture / color** — exposure, contrast, white balance and matching are coherent without hiding real condition;
- **sound** — declared audio mode is intentional and clean;
- **graphics** — hierarchy, timing, readability and safe placement are controlled;
- **perceptual quality** — output is coherent at realistic viewing size without distracting processing/compression defects;
- **truth / identity preservation** — real appearance, condition and evidence remain materially faithful;
- **delivery finish** — output feels complete rather than like a rough assembly.

Score meaning: 0 unusable/critical; 1 major defects; 2 usable but clearly weak; 3 commercially usable with minor polish; 4 strong professional execution.

## Generative transformation gate

Generative/reference-video tools are tools, not evidence authorities. The practical case fails if a transformation materially changes vehicle/product identity, trim, geometry, paint, damage, controls, displays, mileage, labels or condition; invents evidence; conceals condition; or cannot be compared closely enough to verify preservation.

When generative processing is used, preserve source/output pairs and transformation provenance. Evidence-critical shots should default to non-generative editing unless preservation is directly verified.

## Calibrated human comparison

Compare the strongest failed production baseline against the candidate.

1. Randomize labels/order.
2. For a qualification claim use at least two independent humans: the accountable project reviewer and an independent practitioner competent in video editing/post-production or the target commercial-video domain.
3. Before scored comparison, calibrate on at least one clear-failure anchor and one agreed commercially acceptable/professional anchor using the same rubric.
4. Freeze rubric interpretation after calibration.
5. Reviewers independently record criterion scores, overall winner, commercial-usability judgment and concrete failure observations.
6. If reviewers differ by more than one point on two or more P1 craft criteria, miss a critical condition, or split on overall winner, calibration is insufficient; investigate disagreement instead of averaging it away.

A single-user preference remains valuable production evidence, but does not by itself establish reusable profession-level craft qualification.

## Practical decision rule

Pass for the frozen deployment slice requires:
- deterministic gate pass;
- zero truth/identity/AI-distortion critical failures;
- median score >=3 on every P1 craft criterion;
- both calibrated reviewers prefer the candidate to the failed baseline;
- both judge it commercially usable without structural re-edit;
- median score improves by at least one point on at least four craft criteria and introduces no new P1 regression.

Otherwise return revise, blocked, or not-executable with the narrowest root-cause classification.

## Failure routing

Classify the responsible layer before repair:
- professional knowledge/decision-policy;
- perceptual craft;
- runtime/tool capability;
- evaluator construct/calibration;
- specialization;
- upstream brief/assets/facts;
- local/provider execution.

Repair the smallest correct layer. Do not create a new professional core solely because the artifact is weak.

## Qualification semantics

One real-media case can establish evidence only for that bounded deployment slice. Broader creative-craft or NLE-portability claims require additional independent real-media practical cases varying source quality, editorial problem and runtime conditions while preserving held-out integrity.
