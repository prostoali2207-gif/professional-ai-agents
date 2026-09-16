## Decision

`BLOCKED_TECHNICAL` on the selected direction. I am not animating it on this executor, and I am not quietly reshaping it into something drawtext/drawbox can produce.

## Diagnosis

This is a runtime/asset-authoring mismatch (MG-09, MG3-14), not a craft problem and not a brief problem. The selected direction requires four capabilities the executor does not have:

- **vector paths** — authored shape/path geometry with control over stroke, fill, corner and path-level animation;
- **masks/mattes** — alpha-channel reveals, travelling mattes, layered compositing order;
- **editable easing curves** — authored acceleration/deceleration per element, which is the substance of MG-05/MG3-09 motion authoring;
- **tracked compositing** — a graphic anchored to moving environmental space rather than screen space.

FFmpeg `drawtext`/`drawbox` plus encode filters is eligible for conform, encoding, simple flat overlays and QC. Its primitive drawing filters are not a motion-design authoring surface. What it can imitate is axis-aligned rectangles and text with linear or step-expression movement — i.e. constant-velocity UI-like motion, which the model already names as a failure mode, and box-and-label layout, which is the `GENERIC_VISUAL_SYSTEM` failure. Attempting the direction here would not produce a weaker version of it; it would produce a different, generic direction wearing its name. That silent downgrade is the exact prohibited behaviour in MG3-14.

I am assuming the direction was selected legitimately (styleframes reviewed, brief-driven) and that the executor constraint surfaced after selection rather than being a stated brief constraint.

## Actions

1. **Freeze the direction, do not degrade it.** Styleframes and the motion-language intent stay as approved. No partial FFmpeg build is presented as this direction.
2. **Route to an eligible authoring capability (preferred path).** Request a layer/node-based surface with vector/text/image assets, keyframes with editable interpolation, masks/mattes and alpha compositing, grouping/parenting, font preflight, deterministic export and frame inspection. A programmatic compositor such as Remotion, or a conventional motion application, satisfies the renderer side; I flag separately that tracking and any custom vector/texture asset craft may still need dedicated authoring beyond the renderer itself. That is a capability request to the owner of the toolchain, not something I can grant myself.
3. **Prepare a bounded fallback in parallel, declared as a different direction.** If no eligible surface is available within the deadline, I will author a deliberately simpler mechanism that this executor can actually execute with integrity — screen-space type-led treatment with authored hold times, cut-driven state changes carried by the edit rather than by tracked graphics, and no pseudo-vector, pseudo-mask or pseudo-tracked effects. This is presented as a re-selection under MG3-02 against the same brief, with its own styleframes, not as a delivery of the original direction. It changes what the piece communicates and how distinctive it reads; the brief owner decides.
4. **Keep what is unaffected moving.** Structural edit lock, semantic beat map, overlay ledger and source/master lineage all proceed independently of this block, so the decision costs no schedule where it does not have to.
5. **Escalate the architecture signal.** If this executor is the standing environment, the mismatch is structural, not incidental. Recorded for the toolchain owner.

## Status recorded

- Direction: `BLOCKED_TECHNICAL` — vector paths, masks, editable easing, tracked compositing unavailable on FFmpeg drawtext/drawbox executor.
- Craft QC: `CRAFT_NOT_OBSERVED` — no exported artifact for this direction.
- Fallback mechanism: `DEVELOPMENT_DIRECTION`, pending brief-owner acceptance as a substitute selection.
- Capability requested: eligible motion-authoring surface (layers/keyframes/easing/masks/alpha/tracking) plus asset-authoring route.
- Unblocked by: eligible executor, or explicit approval of the simpler re-selected direction.
- Candidate remains `NOT_QUALIFIED`; no qualified, production-proven or craft-pass claim is made here.
