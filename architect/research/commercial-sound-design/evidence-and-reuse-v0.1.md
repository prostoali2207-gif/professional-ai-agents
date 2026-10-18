# Commercial Sound Design EXTEND — evidence and reuse decision v0.1

Status: candidate evidence record; not qualification evidence.
Issue: #289
Date: 2026-09-06

## Production trigger

A real Toyota Yaris AM-001 post-production failure exposed a gap between the qualified parent core's bounded technical audio-post competence and the creative/professional work required to make a commercial automotive reel function without music.

The observed failure class is broader than noise reduction, EQ, loudness, synchronization, or basic audio QC: the system must decide what the soundtrack is doing, which sonic events deserve emphasis, where silence is stronger than another effect, how layers form one perceptual event, how sound carries pacing across cuts, and whether the finished render feels coherent rather than decorated.

## Parent candidate

Qualified parent:
- `video-editing-post-production@0.1.0`
- exact qualified digest: `sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b`

Inherited evidence retained only for unchanged invariants:
- brief/asset validation;
- editorial pacing/continuity;
- truth/provenance;
- bounded technical audio cleanup/mix controls in VE-06;
- delivery engineering;
- artifact-first QC policy.

The parent qualification explicitly does not prove real-media craft/taste or reliable perceptual inspection of arbitrary footage.

## Current evidence

### Official professional tool/workflow evidence

Blackmagic Design Fairlight (retrieved 2026-09-06):
- positions Fairlight as professional audio post integrated with picture editing;
- distinguishes sound editing, recording, mixing, cleanup/repair, EQ/dynamics and mastering;
- explicitly includes Foley and sound effects;
- supports recording original Foley in sync to picture;
- includes creative sound-design tools, automation, bussing and final-mix delivery.
Source: https://www.blackmagicdesign.com/products/davinciresolve/fairlight

Blackmagic Design DaVinci Resolve overview (retrieved 2026-09-06):
- describes advanced ADR/Foley, sample-accurate editing, effects, mixing and mastering as audio-post functions.
Source: https://www.blackmagicdesign.com/products/davinciresolve

Avid Pro Tools Audio Post (retrieved 2026-09-06):
- treats ADR, Foley, sound design, mixing and delivery as a coherent audio-post workflow to picture.
Source: https://www.avid.com/pro-tools/audio-post

Avid Pro Tools (retrieved 2026-09-06):
- supplies frame-accurate sound-to-picture work, layering, routing, automation and mix workflows.
Source: https://www.avid.com/pro-tools

Adobe Premiere audio editing concepts (updated 2026-01-07; retrieved 2026-09-06):
- supports professional soundtrack construction through multi-track editing, gain/volume automation and mixing.
Source: https://helpx.adobe.com/premiere/desktop/add-audio-effects/basic-audio-editing/audio-editing-concepts.html

## Evidence interpretation

The evidence supports a coherent professional audio-post boundary inside picture post-production: sound design, Foley/SFX editing and final mixing can be integrated into the same post-production workflow. It does not prove that every sound-design assignment should be owned by a general video editor, nor that the existing VE-06 currently models the required creative judgment.

The delta is therefore not primarily a new tool. DAWs/NLE audio pages are execution surfaces. The missing behavior is professional judgment over sonic concept, selection, layering, negative space, pacing, emotional arc, perspective and perceptual verification.

## Reuse decision

Target: commercial sound design for short-form picture-led advertising, initially without music.

Decision:
`video-editing-post-production@0.1.0 -> EXTEND with candidate Commercial Sound Design capability`.

Reject:
- `REUSE` parent VE-06 unchanged: insufficient creative/judgment coverage.
- `TOOL` as solution: tools execute decisions but do not supply the missing professional model.
- `BUILD NEW Sound Designer core` now: evidence does not yet establish a separate responsibility/authority boundary that outweighs the integrated audio-post model.

Automotive-specific sonic vocabulary and vehicle-event truth remain outside this reusable candidate and belong in the applied automotive specialization.

## BUILD NEW trigger

Reconsider a separate reusable Sound Design professional core only if practical/adversarial evaluation shows one or more of:
- materially different responsibility/output ownership from picture post-production;
- specialized source-recording/field-recording workflow that becomes central rather than optional;
- substantially different authority/governance boundary;
- persistent capability collision with picture-editing judgment;
- expert-quality sound work requiring a distinct workflow that cannot be modularly invoked from the parent;
- measurable degradation when one practitioner/system owns both picture edit and commercial sound design.

## Evaluation transfer

Do not rerun the whole parent qualification merely because this candidate exists.

Required new evidence:
1. narrow semantic/adversarial evaluation for the new CSD capability;
2. targeted interaction regression where sound decisions touch parent truth, pacing, controlled experiments and artifact-first QC;
3. direct real-media produced-artifact evaluation;
4. calibrated subjective judgment for coherence, craft, commercial effect and perceptual integration;
5. Toyota Yaris AM-001 no-music practical gate in the applied repository.

Until these pass, status remains candidate EXTEND / NOT QUALIFIED.
