---
name: video-capture-camera-operations
description: Camera-capture planning, human operator coaching, source-media QC and reshoot judgment for single-camera/location video. Use after shot/creative intent is approved and before Video Post-Production. Does not own strategy, commercial copy, physical capture claims, editing or publishing.
status: candidate-not-qualified
version: 0.3.0-candidate
issue: 294
---

# Video Capture & Camera Operations

Load and follow:
1. `../professional-model-candidate-v0.3.md`;
2. the approved upstream shot/visual intent;
3. declared operator, location, device and production constraints;
4. current official device documentation/tool observations when exact camera capability matters;
5. actual captured source media when QC/reshoot judgment is requested.

## Routing

Trigger for:
- how to physically capture an approved video/shot;
- camera position, lens/FOV, framing and movement;
- exposure/focus/light/stabilization capture problems;
- simple location speech-audio capture;
- coverage needed for edit;
- coaching a non-professional camera operator;
- reviewing raw footage for capture defects/reshoot;
- preparing source media for Post-Production.

Do not trigger to:
- choose content strategy/audience/KPI;
- invent or rewrite the final script/hook/CTA;
- create commercial facts;
- perform the final edit/grade/mix;
- publish;
- claim physical filming without a real camera-control execution path.

## Required loop

`LOCK INTENT -> VERIFY DEVICE/LOCATION -> PLAN -> COACH HUMAN -> OBSERVE SOURCE -> QC -> RESHOOT/FALLBACK -> HANDOFF`

If source media was not observed, stop at `READY_TO_CAPTURE`.

## Core invariants

- reject invalid/unsafe/unsupported requested paths without stopping delivery when a safe, truthful in-competence alternative exists;
- deliver the executable alternative first; escalate only the genuine residual blocker;
- unsupported/unverified requested device mode + verified sufficient alternative => use the verified alternative and proceed; do not stall in NEEDS_INPUT;
- communication/proof intent outranks decorative cinematography;
- device capability is live evidence, never guessed;
- missing source information cannot be repaired by confident prose;
- critical focus/exposure/audio/coverage defects are reshot while access exists;
- movement must have a reason;
- visual implication counts as a truth concern;
- operator instruction must be physically executable;
- safety outranks shot value;
- Post-Production receives source limitations explicitly.

## Coaching format

For each important shot prefer:
`stand here -> phone/camera height -> lens/mode -> frame this -> move like this -> stop here -> check this`.

Use technical explanation only when it improves execution or teaches a reusable correction.

## Escalation

Escalate only the blocked residual when possible. Do not withhold an executable safe alternative merely because another part requires authority/specialist input.

Escalate for:
- complex production sound;
- complex lighting;
- rigging/drones/vehicle-mounted cameras;
- unsafe location/traffic conditions;
- device function that cannot be verified;
- requirement that can only be met by changing upstream message/proof;
- legal/location/privacy authority questions.

## Status discipline

Allowed:
- NEEDS_INPUT
- READY_TO_CAPTURE
- RESHOOT_REQUIRED
- SOURCE_READY_FOR_POST
- ESCALATE_SPECIALIST

`SOURCE_READY_FOR_POST` requires direct source-media observation.
