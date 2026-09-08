# Video Capture & Camera Operations — Profession Model v0.1

Status: Agent Architect research candidate. Not a SKILL. Not qualified. Issue: #294.

## Target job

Build a reusable professional core that converts an approved visual/communication intent into technically and editorially usable source footage on location, while preserving the intended truth of what is being shown.

Working profession family:
- single-camera / location camera operator;
- unscripted self-shooting / lighting-camera operation;
- basic location production sound only where the same operator is explicitly responsible for it.

This is not Social Content Creative and not Video Editing/Post-Production.

## Responsibility boundary

### Owns
- interpret an approved shot intent into a camera-executable capture plan;
- select feasible camera/lens/device configuration from known hardware;
- framing, composition, camera height/distance and perspective;
- camera movement and stabilization method;
- focus strategy and focus-failure detection;
- exposure and dynamic-range protection;
- white-balance / colour-consistency decisions appropriate to capture;
- basic available-light/location-light control;
- production speech/audio capture when assigned and feasible;
- coverage, continuity, cutaways/B-roll and editability;
- source-media quality checks before leaving the location;
- reshoot/fallback decisions when source quality is not sufficient;
- instruct/coach a non-professional human operator so the physical capture can be executed repeatably;
- surface device/location limitations before they become irreversible capture failures.

### Does not own
- audience, offer, KPI, funnel role, experiment decision or strategy;
- final script, hook, CTA or commercial copy;
- commercial fact creation/approval;
- final edit, pacing, transitions, colour grade, sound design/mix or export;
- publishing;
- physical camera operation by the AI itself unless a runtime exposes a real authorized camera-control tool and the action is explicitly delegated.

## Evidence-backed profession reconstruction

ScreenSkills describes unscripted camera operators as responsible for camera movement, framing/composition and checking shot quality against production requirements; on single-camera work they may also carry lighting and sometimes sound responsibility. The role requires composition, light, colour, focus, framing, camera/lens knowledge, fast problem solving and adaptation to location conditions.

ScreenSkills self-shooting and shooting-AP material adds a second requirement especially relevant to small teams: lens choice, focus, exposure, framing, shot composition, lighting, sound, and "shooting for the edit" so the final sequence contains the coverage the edit needs.

ScreenSkills scripted camera-operator guidance independently supports planning movement/framing and checking image quality against production requirements.

Official Sony movie-recording guidance demonstrates that frame rate, shutter speed, exposure/ISO and white balance materially affect motion rendering and edit consistency. These are not merely aesthetic preferences.

Official Apple and Samsung device documentation demonstrates that capture capability is device/version dependent. Example: iPhone 15 Pro supports device-specific ProRes/Log and frame-rate options; Galaxy A56 has a different video capability envelope. Therefore device configuration belongs in a live/tool-backed binding rather than a frozen universal rule.

## Core professional decisions

### D1 — Intent -> executable shot
Question: What must the viewer be able to see/understand, and what camera position/movement makes that legible without introducing an unintended implication?

Strong behavior:
- identifies the communication/proof job of the shot;
- chooses a feasible framing, perspective and movement;
- preserves upstream intent and truth rather than beautifying away material information.

Weak behavior:
- copies a fashionable shot regardless of purpose;
- treats "cinematic" as the objective;
- invents a camera move that cannot be executed with available space/equipment.

### D2 — Perspective and lens/distance
Question: Which camera/lens position shows the subject truthfully and attractively without distortion that undermines the intended read?

Strong behavior:
- reasons jointly about lens/FOV, distance, camera height and subject geometry;
- notices wide-angle distortion, cramped-interior constraints and misleading compression.

Weak behavior:
- chooses zoom numerically without considering perspective;
- stands too close with an ultra-wide lens and distorts vehicle/body proportions;
- uses digital zoom or lens changes without a quality reason.

### D3 — Exposure and dynamic range
Question: What must be protected from clipping/crushing, and how should exposure adapt to mixed or changing light?

Strong behavior:
- protects decision-relevant highlight/shadow detail;
- recognizes when exterior sun/interior shade exceeds device dynamic range;
- changes position/light/exposure or narrows the shot instead of accepting unusable footage.

Weak behavior:
- trusts auto exposure blindly;
- exposes for a bright background and loses the subject;
- hides condition/detail in crushed shadows or blown reflections.

### D4 — Focus and image integrity
Question: Is the decision-relevant subject actually sharp and stable through the shot?

Strong behavior:
- picks an appropriate focus mode/target;
- watches for focus hunting and missed focus;
- reshoots before leaving.

Weak behavior:
- notices focus defects only during editing;
- assumes autofocus success from a small phone preview.

### D5 — Motion and stabilization
Question: Should the shot be static, handheld, body-stabilized, optically stabilized or mechanically stabilized, and how fast should the camera move?

Strong behavior:
- matches motion to communication purpose and equipment;
- controls start/stop, horizon, gait and parallax;
- avoids movement that prevents viewers from inspecting the subject.

Weak behavior:
- moves constantly because motion feels "professional";
- walks too fast around a vehicle;
- uses stabilization that creates visible warping/pulsing without noticing it.

### D6 — Light, reflections and colour
Question: Does the available light reveal the form/material/condition needed by the brief?

Strong behavior:
- repositions car/camera/operator when practical;
- recognizes reflection hotspots, mixed colour temperatures and dark cabin failure;
- uses simple light control only when it improves truth/readability.

Weak behavior:
- treats harsh UAE daylight as unavoidable;
- hides body shape in specular glare;
- lets automatic white balance shift visibly between adjacent shots without reason.

### D7 — Production speech/audio
Question: Can the spoken content be understood cleanly enough for the intended use?

Strong behavior:
- evaluates mic distance, wind, traffic/AC noise, handling noise and clipping;
- tests/monitors audio when assigned;
- escalates to dedicated sound capture when single-operator audio cannot meet the requirement.

Weak behavior:
- assumes video audio is usable because speech is audible in person;
- discovers wind/echo/clipping after the vehicle is unavailable.

### D8 — Shoot for the edit
Question: Has enough usable coverage been captured to build the intended sequence?

Strong behavior:
- captures the main action plus needed wides, mediums, details, cutaways and transitions;
- avoids coverage gaps that force post-production to fake continuity;
- tracks orientation/continuity where material.

Weak behavior:
- captures one long walkaround and expects the editor to manufacture variety;
- overshoots decorative details while missing the proof/coverage the brief needs.

### D9 — On-location QC and reshoot
Question: Is the footage actually good enough before the operator leaves?

Strong behavior:
- reviews representative clips at useful magnification and with audio;
- identifies technical vs intentional imperfections;
- reshoots high-impact failures while the scene is still available.

Weak behavior:
- relies on memory or confidence;
- performs no source inspection;
- shifts irreversible capture defects downstream.

### D10 — Human operator coaching
Question: What is the smallest executable instruction that lets a non-professional operator reproduce the required shot?

Strong behavior:
- gives concrete position, height, lens/mode, path, speed, start/end and QC cues;
- adapts instruction after observing the operator's actual result;
- teaches a reusable principle when it will prevent repeated failure.

Weak behavior:
- gives abstract advice ("make it cinematic", "move slowly");
- overloads the operator with technical theory during the shoot;
- repeats the same instruction after evidence shows it is failing.

## Expert-vs-average discriminators

| Dimension | Average behavior | Strong practitioner behavior |
|---|---|---|
| Shot choice | aesthetically plausible shot | purpose-driven shot that preserves proof/intent |
| Exposure | accepts auto result | protects decision-relevant detail and adapts to scene DR |
| Focus | assumes autofocus | verifies focus behavior and reshoots misses |
| Movement | motion = production value | motion only when it improves spatial/semantic read |
| Lighting | accepts location as-is | diagnoses direction/contrast/reflection and changes geometry/light |
| Coverage | collects many clips | captures an editable sequence with sufficient complementary coverage |
| QC | checks later | detects/reshoots irreversible defects on location |
| Coaching | abstract film vocabulary | executable cues tied to observable result |
| Boundaries | absorbs upstream/downstream work | preserves Creator intent and Post-Production authority |

## Automotive specialization delta

The universal core must remain industry-neutral. UAE automotive specialization may add:
- vehicle exterior geometry and perspective traps;
- paint/body reflection management;
- truthful condition/damage visibility;
- VIN/odometer/feature proof legibility when upstream requires it;
- cabin exposure and window contrast;
- dashboard/display flicker;
- wheel/interior/exterior coverage conventions;
- phone-first one-person capture;
- UAE sun/heat/wind/showroom practical constraints;
- device-specific iPhone/Samsung operating bindings;
- fast inventory throughput and minimal-setup capture routines.

The specialization may not create commercial facts or decide which facts must be advertised.

## Reuse decision

### social-content-creative@0.1.0
Decision: REJECT as parent/substitute; retain as upstream dependency.

Reason:
It is qualified for social creative, copy, visual storytelling intent and shootability. It does not establish professional camera-craft execution, source-media QC, focus/exposure/audio control or edit-coverability. Extending it with the full target profession would create responsibility ambiguity and a large unqualified behavior delta.

### video-editing-post-production@0.1.0
Decision: REJECT as parent/substitute; retain downstream.

Reason:
Its evidence object is the captured media/timeline/render. It cannot reliably repair missing source coverage, missed focus or unrecoverable capture exposure. Giving it capture authority collapses a useful production boundary.

### trusted library
No existing qualified professional core in the current catalog covers the target responsibility/output scope.

Decision: BUILD NEW candidate core.

## Knowledge packaging

### EMBED_CORE
- intent-to-shot translation;
- perspective/framing/movement judgment;
- exposure/focus/light principles;
- coverage/editability reasoning;
- on-location QC/reshoot;
- boundary discipline.

### PROCEDURAL_MODULE
- phone-first capture workflow;
- spoken walkaround capture;
- B-roll/coverage capture;
- on-location QC checklist;
- novice operator coaching loop.

### LIVE_RESEARCH / TOOL-BACKED
- exact device camera modes;
- current OS/app camera behavior;
- codec/resolution/frame-rate capability;
- accessory compatibility;
- current platform technical delivery requirements when they affect capture.

### ESCALATE
- complex lighting rigs;
- dedicated production-sound requirements;
- drone/jib/vehicle-rig operation;
- safety-critical rigging;
- specialized colour-management pipelines;
- legal/privacy/location permissions.

## Production workflow

`approved shot intent -> inspect device/location constraints -> executable capture plan -> human capture -> observe actual clip -> QC -> reshoot/fallback if needed -> source-media handoff -> Post-Production`

The agent must not mark capture complete from the written plan. Completion evidence is the actual source media or explicit human confirmation when the runtime cannot inspect it.

## Definition of done for this research phase

- profession boundary established;
- reuse decision explicit;
- observable competencies defined;
- evidence sources and transfer limits recorded;
- practical and adversarial evaluation designed before candidate implementation.
