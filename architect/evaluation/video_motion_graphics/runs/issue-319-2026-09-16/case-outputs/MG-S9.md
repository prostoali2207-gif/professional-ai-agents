## Decision

`TECHNICAL_PASS` + `CRAFT_FAIL`. Not release-ready. The render stays in repair, not in delivery.

Everything you listed — 1080x1920, clean decode, captions inside safe zones, -16 LUFS — is technical QC. Those checks were never able to establish craft, and a technical pass never implies a craft pass. "Cheap, cluttered, mechanically animated" is three separate observable defects, and each has its own repair layer. I am not going to treat it as one taste complaint and glaze it with effects.

## Diagnosis

Assumption: I have the exported MP4 and the project, and I am judging the exported artifact at representative phone size with phone audio, not the timeline. "Cheap/cluttered/mechanical" as stated is a reaction, not a diagnosis, so I name causes:

1. `GENERIC_VISUAL_SYSTEM` (the "cheap" read). The piece is almost certainly a sequence of individually clean overlays rather than one designed system: per-scene composition invented locally, no shared grid or margin logic, scale relationships that do not repeat, rounded cards/pills/dashboard components with no brief-driven reason, flat value structure with no depth or material intent, and no motif carried scene to scene. Generic reads as cheap even when every element is aligned.
2. `GENERIC_TEMPLATE_TYPOGRAPHY`. Legible but unauthored: default weights doing all the hierarchy work, uniform tracking, labels at the same optical weight as titles, line breaks falling where the box ends instead of where the phrase ends. Safe-zone compliance is not typographic craft.
3. `HIERARCHY` / clutter. Subject, graphic, captions and branding are competing simultaneously. Too many layers are alive at once, so nothing is first.
4. `MOTION_TIMING` (the "mechanical" read). Uniform durations, near-linear or single default ease on everything, simultaneous entries, equal in/out treatment, no anticipation or settle, no authored holds — motion synced to a grid instead of to speech, edit rhythm and information load.

Secondary suspects I will confirm while re-observing: motion elements carrying no communication job (MG3-09), and diagrams defaulting to cards or `01 -> 02 -> 03` where a persistent-object state change would explain better (MG3-08).

## Actions

1. Re-observe the export at phone size and log each defect with timecode, class and observable cause. No global adjectives.
2. Check the lock map before touching anything. Captions that passed safe-zone and any approval-locked or experiment-locked layers are invariants for this revision; I repair around them and report the exact dependency if I cannot.
3. Verify the overlay ledger — every material overlay mapped to an approved beat, time range and owner. A contradictory overlay blocks ready state independently of look.
4. Repair the system, not the surface. Set one grid, margin and scale system; rebuild type hierarchy by role, weight, size and spacing; commit to one graphic language (shape, stroke, corner, icon logic) and one value/color structure. No fixing genericity with shadows, outlines, gradients, a fashionable font or added effects.
5. Reduce before adding. Where layers compete, remove or delay a layer rather than adding emphasis.
6. Re-author timing: per element define job, represented change, viewer inference, timing/hold, removal criterion. Vary durations and easing by role, stagger entries, give comprehension holds, cut motion that earns nothing.
7. Gate before re-rendering full length: styleframes for opening, peak explanatory and resolved states, plus one short prototype showing the actual motion language. If it still reads as presentation UI statically, it does not get animated.
8. Confirm the authoring route. If the repaired direction needs vector/texture/depth asset craft the current renderer cannot author, I route it or deliberately choose a simpler direction — I will not silently collapse it back into CSS cards.
9. Re-render from the controlled source (no proxy or review-export chain), rerun technical QC, then craft QC at phone size, then rerun affected parent checks.

## Status recorded

`CRAFT_FAIL` — technical QC complete, craft observed and failed; defect log by timecode; repair at visual-system, typography, hierarchy and motion-timing layers; re-entry via styleframe/prototype gate. Next valid state is `STYLEFRAME_READY`, then `MOTION_PROTOTYPE_READY`. This capability is a non-qualified candidate; strong craft claims need calibrated comparative or practitioner review, not my judgment alone.

Timeline: I need the structural edit confirmed stable before I author timing again. If structure is still moving, say so now — otherwise the repair gets invalidated and redone.
