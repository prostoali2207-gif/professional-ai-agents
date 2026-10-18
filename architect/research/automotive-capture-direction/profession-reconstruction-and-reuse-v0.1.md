# Automotive Commercial Capture Direction — profession reconstruction and reuse decision

Date: 2026-09-01
Status: architecture decision complete; candidate construction permitted; NOT QUALIFIED
Issue: #229
Target: professional capture-direction capability attached to Social Content Creative / Content Creator while a human remains the physical camera operator

## 1. Actual profession reconstructed

The target is not a generic content creator who happens to write shot lists. It is a bounded combination of **commercial automotive photographer**, **cinematographer / director of photography**, and **capture supervisor** whose accountable work is to turn an approved creative intent, verified vehicle facts, actual location/light conditions, declared equipment, and downstream edit needs into technically and aesthetically controlled source media.

The AI does not physically operate the camera. It must externalize senior-practitioner judgment into instructions precise enough that a non-professional human can execute them, then inspect trial captures and direct corrections.

### Primary outputs

1. Capture diagnosis: purpose, vehicle, condition/proof obligations, location, sun/light, environment, reflections, equipment, operator limits, safety and downstream edit needs.
2. Shot-specific capture plan: camera position/height/distance, focal-length or device-camera choice, orientation, subject angle, wheel/steering state when relevant, lighting/reflection intent, exposure/color/motion intent, movement path, duration, stabilization and acceptance criteria.
3. Still-photo coverage plan: hero, supporting, interior, detail and evidence/condition frames without confusing beauty imagery with factual proof.
4. Motion coverage plan: static, pan, push/pull, orbit, tracking/parallax and detail movement chosen for a communication/editing job rather than spectacle.
5. Test-capture critique and bounded reshoot directions based on the actual artifact.
6. Source-media handoff requirements for Video Post-Production, including continuity, clean handles, orientation, duplicate/failed-take rejection and proof-bearing source preservation.

### Authority boundary

The capability may decide capture craft inside an approved brief: camera position, perspective, lens/device-camera choice, lighting/reflection treatment, exposure/color/motion approach, shot sequence for efficient capture, safe bounded movement and reshoot corrections.

It does not own campaign strategy, audience, offer, factual claims, experiment variables, paid distribution, final edit, publication, vehicle driving, public-road safety authorization, legal permits or irreversible actions.

It must not fabricate equipment availability, camera features, permissions, road access, crew, lighting gear or vehicle condition.

## 2. Why this is a real capability gap

The qualified `social-content-creative@0.1.0` already owns visual storytelling, shootability and **light production direction**, but its professional model explicitly scopes this as bounded shoot directions rather than principal-photography craft. The current Auto Sales Content Creator specialization similarly asks for framing, action, camera movement and B-roll, but it does not encode a full photographic/cinematographic judgment model for optics, perspective, reflective-surface lighting, exposure, motion rendering, automotive surface control, artifact-first capture critique or reshoot diagnosis.

The qualified `video-editing-post-production@0.1.0` is downstream and explicitly excludes **principal photography**. Therefore assigning this gap to Post-Production would violate its profession boundary.

## 3. Mandatory reusable-candidate inspection

Repository library inspected: `architect/library/catalog.json` on 2026-09-01.

| Candidate | Compatibility evidence | Material gap / risk | Decision |
|---|---|---|---|
| `social-content-creative@0.1.0` | Qualified; owns brief fidelity, truthful persuasion, visual storytelling, shootability, platform adaptation, experiment locks and traceable creative handoff | Capture direction is intentionally light/bounded; no deep principal-photography craft, optics/perspective model, reflective automotive lighting model or artifact-first capture correction loop | **EXTEND** — retain unchanged qualified invariants and add capture craft as a bounded capability |
| `video-editing-post-production@0.1.0` | Qualified; strong continuity, picture/color finishing, source-media QC and downstream handoff | Explicitly excludes principal photography; moving capture ownership here would collapse an intentional upstream/downstream boundary | **REJECT as capture core**; retain as downstream consumer |
| Visual Design / Art Direction candidate | Useful creative critique/reference mechanisms | Different artifact and profession construct; not principal photography; current candidate/evaluation state is not transferable qualification evidence | **REJECT as capture core** |
| Build a new top-level workflow agent | Would create a clean role title | Adds routing/state/handoff overhead while the actual task is a tightly coupled execution capability of Content Creator and the human operator | **REJECT unless later evidence shows measurable independence value** |

### Primary architecture decision

**EXTEND `social-content-creative@0.1.0` with a modular Automotive Commercial Capture Direction capability. Do not create a new top-level workflow agent.**

The extension is behavior-relevant and is not covered by the existing qualification certificate. It must remain NOT QUALIFIED until the new capability and its interaction with Content Creator pass targeted semantic/adversarial evaluation plus artifact-first practical capture evaluation.

## 4. Evidence base for profession reconstruction

The evidence target is professional decision structure, not fixed camera recipes.

### A. Reflective automotive surfaces and lighting

- American Society of Cinematographers, Jay Holben, `Shot Craft: Using Specular Reflections` (2019): glossy product/car surfaces are shaped through controlled specular reflections; car work commonly uses very large reflected sources; law-of-reflection geometry matters. https://theasc.com/articles/shot-craft-using-specular-reflections
- American Society of Cinematographers, Bill Bennett, ASC, car-commercial lighting material (2017/2020): dedicated step-by-step automotive hero-shot lighting and location methods from a cinematographer with extensive car-commercial experience. https://theasc.com/videos/lighting-tech-tips-household-lightbulb-russell-carpenter-asc-1/car-commercial-lighting-onstage-demo and https://theasc.com/articles/hablando-sobre-autos
- American Society of Cinematographers, `Understanding Polarizing Filters`: a polarizer can reduce reflections from windshields and clear-coated surfaces, but is not a universal reflection remover and does not cancel metallic-surface reflections. https://theasc.com/articles/shot-craft-understanding-polarizing-filters

Operational implication: the capability must reason about which reflections reveal form, which distract, what geometry creates them, and whether to move camera/car/source before reaching for a filter. “Remove all reflections” is professionally wrong.

### B. Perspective, distance and lens/device-camera choice

- Sony Lens Basics, `Focal length, angle of view and perspective`: apparent perspective differences are driven by camera-to-subject distance; wide views commonly require closer camera positions and therefore exaggerate relative size, while greater distance compresses relative size. https://www.sony.com/en-eg/electronics/focal-length-angle-of-view-perspective
- Canon lens knowledge, `Perspective`: shorter focal lengths strengthen perspective while longer focal lengths compress it, supporting deliberate control of subject/background relationships. https://files.canon-europe.com/files/webcontent/rf-lens-world/knowledge/perspective/index.html
- Nikon, `Understanding Focal Length`, updated 2025: focal length controls angle of view and magnification; standard ranges minimize distortion relative to wider views. https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/understanding-focal-length

Operational implication: the capability must specify camera **position/distance and height**, not merely a focal-length number or “use 2x.” It must adapt equivalent field of view to the actual device and avoid pretending that lens choice alone determines perspective.

### C. Motion rendering and camera movement

- Nikon, `10 Tips for Better Camera Panning`: panning is coordinated camera motion following the subject; shutter choice and tracking execution jointly determine subject sharpness/background motion. https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/10-tips-for-better-camera-panning
- ASC cinematography case material repeatedly treats camera placement/movement and available light as expressive choices constrained by the real environment rather than decorative movement. Example: https://theasc.com/articles/fear-and-loathing-in-las-vegas-gonzo

Operational implication: movement must have a visual/communication job and an executable path. The capability must distinguish static proof coverage from motion/desire coverage and must not add camera motion merely because it looks cinematic.

### D. Reflection and flare controls are conditional tools

- Canon UAE circular-polarizer documentation: reduces reflections from non-metallic surfaces such as water/glass and can increase clarity/saturation. https://sfcc-service.canon-europe.com/3445C001/3445C001.html
- Canon lens technology: coatings/hooding reduce flare and ghosting caused by stray light/internal reflections. https://files.canon-europe.com/files/webcontent/rf-lens-world/features/technology/index.html

Operational implication: filters, flags, shade, camera repositioning and light-source control are different mechanisms. The practitioner must diagnose the artifact before selecting a mechanism.

## 5. Competency families required by the target

1. **Intent and constraint framing** — separate communication job, beauty job, proof job, experiment locks, location/equipment limits and safety constraints.
2. **Automotive form reading** — understand body lines, stance, surface curvature, glass, chrome, wheels and how camera/light/reflections alter perceived geometry.
3. **Perspective and camera placement** — control height, distance, angle, field of view and background relation; distinguish distance-caused perspective from lens magnification.
4. **Lighting and reflection control** — use sun/sky, negative fill, bounce, flags, large-source logic and conditional polarization to shape reflective surfaces rather than flatten them.
5. **Exposure, color and focus control** — choose a device-appropriate exposure/WB/focus strategy that preserves highlights, paint color, screens/interior detail and shot-to-shot consistency; never invent unavailable manual controls.
6. **Still-photography craft** — hero/supporting/detail/interior/evidence coverage with deliberate composition and clean geometry.
7. **Cinematography and motion** — choose static/pan/push/orbit/tracking/parallax paths, speed, duration and stabilization based on shot purpose and edit needs.
8. **Continuity and edit coverage** — preserve direction, exposure/color consistency, action continuity, handles and complementary shot sizes for downstream editing.
9. **Truth-preserving presentation** — beauty lighting may improve legibility/desire but may not conceal required condition evidence or imply unsupported vehicle facts.
10. **Human-operator direction** — instructions must be physically measurable/executable by a non-professional: where to stand, camera height, distance, vehicle orientation, movement path, duration, what reflection/background to watch, acceptance/rejection cue and fallback.
11. **Artifact-first critique and reshoot** — inspect actual trial stills/frames/clips; diagnose root cause (perspective, reflection, exposure, shake, focus, background, continuity, framing, motion), then prescribe the smallest corrective change and re-observe.
12. **Equipment adaptation** — adapt to declared phone/camera/lens/gimbal/tripod/filters/light; never prescribe nonexistent features as if available.
13. **Safety/escalation** — no unsafe handheld operation while driving, risky road positioning or unverified public-road permissions; human owns physical execution and safety authorization.
14. **Source-media handoff** — preserve clean originals/proof-bearing shots and give Post-Production adequate, traceable coverage.

## 6. Expert-vs-average discriminators

A strong practitioner:

- sees the car as a reflective three-dimensional form, not as a subject to place at a memorized “45-degree angle”;
- predicts how moving the camera, car or large reflected source changes body-line readability before adding gear;
- controls perspective through camera distance/height and then chooses field of view to frame the result;
- distinguishes useful specular highlights from distracting reflections instead of trying to remove all reflections;
- separates hero/desire imagery from evidence/condition imagery and does not let beautification corrupt proof;
- notices background poles, horizon cuts, wheel/body tangencies, camera/operator reflections, windshield glare and paint highlight clipping before capture is accepted;
- gives a non-professional operator a reproducible instruction rather than aesthetic adjectives;
- tests a frame/clip, diagnoses the actual artifact, changes one causal variable when practical, and rechecks;
- plans source coverage for the edit rather than treating every shot as an isolated beauty shot.

An average content operator often produces a generic angle list, uses ultra-wide framing because it “fits the car,” relies on automatic exposure without checking paint/glass highlights, adds arbitrary gimbal movement, ignores reflection geometry, and cannot explain why the result looks amateur.

## 7. Knowledge packaging

### Embed in capability
- perspective/distance reasoning;
- automotive reflective-surface lighting logic;
- shot-purpose taxonomy;
- artifact-first critique loop;
- truth/safety/equipment boundaries;
- continuity and source-handoff fundamentals.

### Runtime / project packet
- exact vehicle and condition/proof obligations;
- actual location and time/daylight conditions;
- actual device/camera/lenses/accessories and supported modes;
- operator count/skill and available time;
- platform/output orientation and content-spec locks;
- current permissions/safety constraints.

### Live retrieval when material
- device-specific camera feature behavior if the declared hardware/software version matters;
- current platform capture/upload constraints if they materially affect capture;
- location/permit rules where required.

## 8. Evaluation obligations

Retain prior qualified evidence only for unchanged Social Content Creative invariants: brief fidelity, truthful persuasion, claim grounding, experiment locks, platform/creative handoff and authority boundaries.

New or affected behavior requires:

1. deterministic/semantic adversarial fixtures for perspective, reflection diagnosis, device capability honesty, truth/proof separation, motion purpose, continuity and safety;
2. comparative judgment cases where a generic shot list competes with professional capture reasoning;
3. artifact-first practical evaluation on real automotive stills/clips with hidden defects and required reshoot diagnosis;
4. an operator-executability test: a non-professional should be able to follow the instruction without filling material gaps by guesswork;
5. at least one end-to-end Content Creator -> human capture -> Video Post-Production handoff test;
6. regression that the new capability does not change strategy/offer/facts/experiment locks.

Until these pass, the extension is **NOT QUALIFIED** and must not be represented as production-ready professional capture capability.
