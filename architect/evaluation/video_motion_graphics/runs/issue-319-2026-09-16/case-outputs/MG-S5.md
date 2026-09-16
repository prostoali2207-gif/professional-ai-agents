## Diagnosis

This is not a synchronization problem, and I will not fix it by adjusting keyframe positions against the waveform. Speech sync is already correct; sync only guarantees temporal alignment, it does not give motion a communication job. Two coupled defects are in play, and the order matters.

`CONCEPT` (primary). Entry, hold and exit is one lifecycle — one thing persisting through three states. Representing it as three co-equal circles turns a single persistent object into three unrelated objects, so identity and causality are destroyed before timing is even considered. The viewer sees three items appear, not one thing being gained, retained and lost. Fixing the easing on the wrong mechanism buys nothing.

`MOTION_TIMING` (secondary but visible). Constant-speed translation with an abrupt stop is linear interpolation with no authored curve: no anticipation, no deceleration, no settle, no hold. That is precisely the signature of default UI/CSS transform behavior, which is why the piece reads as interface animation rather than authored explanation.

`GENERIC_VISUAL_SYSTEM` (contributing). Three identical circles differentiated only by a label is dashboard/step-card language. Nothing in the form tells you which state is which — the label carries all the meaning and the graphic carries none.

Assumptions: the beat is approved and the structural edit is locked, the graphic layer is `UNLOCKED`, and I observed the exported artifact at phone size. If the circle layer is in fact `LOCKED_BY_APPROVAL`, I stop here and report the dependency plus the minimum unlock required rather than editing it.

## Actions

1. Write the motion information-gain sheet before touching curves. For each material element: communication job, represented change, intended viewer inference, timing and hold, removal criterion. Any circle that earns no job gets removed, not re-eased. I expect at least one of the three to fail this test.

2. Re-test the representation. Candidates: (a) one persistent token that enters frame, is visibly held, then leaves — identity preserved across all three states; (b) one token traversing three spatial zones, so position encodes state; (c) accumulation/depletion, if the beat is really about retention volume rather than an individual journey. I will select on clarity and truthfulness, not novelty. Numbered or discrete treatment stays valid if it turns out to be genuinely clearest. No implied durations, rates or magnitudes unless approved evidence supports them — a lifecycle diagram must not read as measured data.

3. Only then author timing. Asymmetric easing: quick departure, decelerated arrival with a small settle instead of a hard stop. Brief anticipation before entry. A deliberate hold at the peak explanatory state — hold is reading time, not a frozen object. Continuity of direction so exit continues the established vector rather than arbitrarily reversing. Stagger tied to speech stress, not uniform intervals.

4. Give the states different form. Weight, scale, containment or value should make "held" read as held and "exit" read as loss, so meaning does not live entirely in type.

5. Runtime route check. If the selected mechanism needs vector, mask or texture authoring beyond the available surface, I route it to an eligible authoring capability or deliberately pick a simpler direction. I will not silently collapse it back into three easy shapes.

6. Gate before full render: opening, peak and resolved styleframes plus one short prototype showing the actual curve language, reviewed at phone size. Overlay ledger updated for the three labels.

## Status recorded

`CRAFT_FAIL` — defects `CONCEPT`, `MOTION_TIMING`, `GENERIC_VISUAL_SYSTEM`. Technical state unchanged; technical validity never implied craft pass here. Not release-ready. Next reportable state after repair is `MOTION_PROTOTYPE_READY`, pending re-observation.
