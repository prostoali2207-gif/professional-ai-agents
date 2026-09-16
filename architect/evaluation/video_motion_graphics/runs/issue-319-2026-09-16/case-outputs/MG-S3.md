## Decision

Rejected as proposed. The upper-third timeline, floating labels and animated arrows do not go on screen simultaneously, and none of them land on the point-at-camera beat. This is not a styling problem and I am not fixing it with opacity, drop shadows, blur separation or a smaller type size.

## Diagnosis

Primary defect: `HIERARCHY`. Secondary: `MOTION_TIMING`, with a `CONCEPT` component.

In a 9:16 frame the usable graphic real estate is already spent. Two-line captions own the lower third, platform UI chrome eats below that, and the speaker's head and pointing hand own the centre. Loading the upper third with a timeline plus free-floating labels plus arrows means the frame is committed top, middle and bottom at once, with three independently moving element families competing. Per MG-03 the viewer must know where to look first; here four layers all claim first position.

The timing is the worse half. A speaker pointing at the camera is the strongest direct-address moment in the piece — it is itself an authored attention event. Putting three graphic reveals on top of it does not reinforce it, it cancels it. Judged as combined attention load (MG3-09) rather than effect by effect, that beat is oversubscribed.

There is also a concept redundancy: a timeline already encodes sequence and direction along its own axis. Animated arrows restate what the track's geometry says, and floating labels restate what an anchored label at the read position would say. Three element families are doing one job.

## Actions

1. Hierarchy for this beat, in order: subject and gesture, then captions, then at most one graphic element. Graphics time-share the frame; they do not space-share it.
2. Hold the pointing beat clean — subject plus captions only, for the full gesture through its settle. Graphics enter after the gesture resolves.
3. Re-test the mechanism against MG3-08 before building the proposed set. A single persistent marker travelling one track carries sequence, direction and position in one object. That collapses timeline plus arrows plus floating labels into one element, removes the arrows entirely, and reduces labels to a just-in-time reveal at the marker with the previous label retiring. If the content is genuinely parallel rather than sequential, the timeline is the wrong mechanism and I will bring an alternative instead of decorating this one.
4. Write the MG3-09 line for every surviving element: job, represented change, intended viewer inference, timing and hold, removal criterion. Anything without a removal criterion is not authored and gets cut.
5. Build the MG3-04 overlay ledger: each label maps to an approved semantic statement or source beat, a time range and an owner. Labels that exist because the frame looked empty do not get a ledger row and do not ship. The timeline must not imply measured dates, durations or rates unless approved evidence supports them; if it reads as measured and the content is conceptual, the tick treatment changes.
6. Captions stay put. I am treating wording, timing and placement as `LOCKED_BY_APPROVAL` (VE-07, MG3-07) and solving around them by taking budget from time, not from their space. If the selected direction genuinely cannot work without moving the caption block, I will report the exact dependency and the minimum unlock rather than nudging them.
7. Confirm the structural edit is locked (MG3-03) before authoring any keyframes. If the pointing beat can still move in the cut, prototype timing only — I am not authoring final arrow or marker curves against an unstable edit.
8. Styleframe gate before animation: opening state, peak explanatory state, resolved state, then one short prototype showing the actual motion language, all reviewed at phone size.

## Status recorded

`DEVELOPMENT_DIRECTION`. Defects logged as `HIERARCHY` + `MOTION_TIMING` + `CONCEPT`. Craft state `CRAFT_NOT_OBSERVED` — nothing rendered yet. If the simultaneous version were rendered as proposed, I would expect `CRAFT_FAIL` at phone-size review. No ready state until the overlay ledger is clean and the exported artifact has been observed at representative phone size.

Assumptions: open creative space on mechanism; captions approved and locked; timeline content is sequential and not quantitatively evidenced; delivery is a vertical social placement with standard UI chrome.
