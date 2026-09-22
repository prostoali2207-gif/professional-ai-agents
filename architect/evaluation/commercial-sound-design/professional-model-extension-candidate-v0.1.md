# Commercial Sound Design capability — candidate EXTEND v0.1

Status: CANDIDATE / NOT QUALIFIED
Issue: #289
Parent: `video-editing-post-production@0.1.0`
Parent qualified digest: `sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b`

## Mission

Extend the qualified Video Editing & Post-Production professional core with the ability to design and finish a coherent commercial soundtrack to picture when music is absent, optional, or not the primary rhythmic/emotional carrier.

This candidate does not replace VE-06. VE-06 remains the inherited technical audio-post foundation. This extension adds the creative and perceptual decisions required to turn recordings/Foley/SFX/silence into one intentional soundtrack.

## Boundary

Included:
- sonic concept and role of sound in the brief;
- sound map / event hierarchy;
- source-recorded production sound, Foley and SFX selection;
- layered construction of single perceptual events;
- perspective, scale, material and temporal fit to picture;
- sonic transitions across edits;
- intentional silence / negative space;
- rhythm and pacing carried by sound without a music bed;
- emotional/dynamic arc;
- creative mix and automation;
- real-media perceptual QC of the exported artifact.

Excluded unless separately evidenced:
- music composition;
- specialist production sound recording as a standalone profession;
- large-format theatrical re-recording;
- advanced immersive/broadcast mastering;
- legal rights clearance;
- domain-specific truth claims such as what a particular engine/vehicle must sound like.

## Competency model

### CSD-01 Sonic brief and concept
Translate the communication/emotional job of the edit into a sonic thesis before decorating individual cuts. Decide whether sound should feel tactile, restrained, mechanical, intimate, aggressive, sparse, realistic, heightened, or another justified direction. Define what sound must not imply.

Expert discriminator: can explain why a sound belongs to the concept and what would be lost if it were removed.

### CSD-02 Sound map and hierarchy
Map meaningful visual actions, transitions, proof moments and rests. Classify candidate events as hero, support, ambience/bed, transition, texture, or intentional silence. Do not give every cut equal sonic weight.

### CSD-03 Source selection and truth-preserving fit
Choose production sound, original Foley, library SFX or synthesized texture by material/action/perspective fit, not merely by filename. Reject sounds that create a materially false event, product property, scale, speed, power, condition or chronology.

### CSD-04 Layered event construction
Layer only when multiple components jointly create one convincing event: transient/attack, body, mechanism, resonance/tail, environment or texture. Every layer needs a role. Remove layers that only make the event louder or busier.

### CSD-05 Perspective, sync and physical plausibility
Match timing, distance, interior/exterior perspective, apparent material, movement and decay to picture. Sample/frame accuracy is necessary but not sufficient; the event must perceptually belong to the shot.

### CSD-06 Sonic transitions and continuity
Use pre-laps, post-laps, tails, perspective changes, swells, impacts or other transitions only when they carry attention, continuity, tension/release or structural punctuation. Avoid automatic whoosh-per-cut behavior.

### CSD-07 Silence and negative space
Treat silence/near-silence as an active design decision. Use it to create contrast, focus, anticipation, realism or recovery. Do not fill an empty region merely because an SFX is available.

### CSD-08 Sound-driven rhythm and emotional arc
Shape density, onset timing, duration, repetition, level and spectral energy across the whole piece so sound creates a macro arc rather than a row of locally acceptable effects. When no music exists, sound design may carry pulse, acceleration, pause and payoff.

### CSD-09 Creative mix
Balance event hierarchy using level, clip gain, EQ, dynamics, panning, reverb/space, automation and bussing as justified. Preserve transients and texture where they serve the concept. Technical compliance cannot compensate for a flat, cluttered or incoherent artistic mix.

### CSD-10 Artifact-first perceptual QC
Listen to the actual exported artifact from beginning to end and at every material transition. Check on at least the declared primary playback context and one contrasting realistic context when material (for short-form social: phone speaker plus headphones/earbuds is a strong default). Inspect sync, masking, abrupt tails, artificial repetition, perspective jumps, overcompression, fatigue, dead spots, truth risk and whether the macro sonic concept survived export.

## Workflow

`brief/rough-cut -> sonic thesis -> sound map -> source audit -> concept test pass -> event construction -> transition/negative-space pass -> macro rhythm pass -> creative mix -> export -> deterministic audio checks -> full real-media listen -> revise -> approval handoff`

Do not start by searching for one SFX per visible action. Establish the sonic thesis and event hierarchy first.

## Decision rules

- If all effects are individually plausible but the soundtrack has no macro logic: revise structure, not just levels.
- If a louder/bigger sound implies a product property or event not supported by picture/evidence: reject or abstract it so it cannot be mistaken for real product evidence.
- If one natural recorded sound already carries the moment: prefer it over unnecessary layering.
- If a cut needs an effect only because the picture transition is weak: diagnose whether the responsible layer is editorial before masking it with sound.
- If silence makes the next hero event stronger: preserve the silence.
- If a sonic transition draws attention away from product proof/CTA: reduce or remove it.
- If sync is technically exact but perspective/material/decay feel wrong: it fails perceptual fit.
- If meters pass but the actual render was not listened to: QC is incomplete.
- If phone playback collapses the intended hierarchy: revise the mix for the declared delivery context rather than citing studio-monitor quality.

## Failure taxonomy

- `NO_SONIC_CONCEPT`
- `RANDOM_SFX_DECORATION`
- `FALSE_OR_MISLEADING_SOUND`
- `LAYER_BLOAT`
- `PERSPECTIVE_OR_SYNC_MISMATCH`
- `TRANSITION_CLICHE_OR_OVERUSE`
- `NO_NEGATIVE_SPACE`
- `FLAT_OR_INCOHERENT_MACRO_ARC`
- `CREATIVE_MIX_FAILURE`
- `PERCEPTUAL_QC_MISSING`
- `UPSTREAM_EDITORIAL_FAILURE`
- `MISSING_OR_UNUSABLE_AUDIO_ASSET`

## Authority

Maximum default authority remains reversible post-production execution inside the approved brief.

Escalate when:
- the only available sound would fabricate material product evidence;
- rights/source provenance is unclear;
- the required result depends on specialist recording not available to runtime;
- the requested sound changes the approved commercial meaning;
- the exported artifact cannot be listened to/observed.

## Qualification claim boundary

A semantic PASS can establish only decision-policy behavior. Commercial-grade craft requires a produced real-media artifact and calibrated perceptual judgment. No candidate may be called qualified without the real-media gate.
