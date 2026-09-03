# Automotive Commercial Capture Direction — Expert-Gap / Red-Team v0.1

Date: 2026-09-01
Status: PRE-FREEZE REVIEW
Issue: #229
Candidate reviewed: `architect/evaluation/automotive-capture-direction/professional-model-candidate-v0.1.md`

Required Architect question:

> What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?

## 1. Senior automotive photographer / cinematographer perspective

### Gap A — capture quality begins before camera placement

Risk in initial v0.1: the model could become a sophisticated angle/light adviser while still arriving at a visually unprepared car/location.

A strong automotive practitioner checks the presentation state and the reflected environment before the hero frame: removable dust/fingerprints/clutter, glass/wheel presentation, wheel/body pose, direct background, and objects that will appear only as reflections.

Repair made before freeze:

- added `C0. Vehicle and location preparation`;
- preparation explicitly distinguishes removable visual contamination from material condition/proof;
- added public adversarial preparation fixtures P01–P03;
- added preparation to the decision chain and operator output contract.

### Gap B — motion craft is not just camera-path vocabulary

Risk in initial v0.1: knowing pan/orbit/track vocabulary without frame-rate, shutter/motion rendering, flicker, rolling-shutter and profile consistency can still produce source footage that looks amateur or is expensive/impossible to repair.

Repair made before freeze:

- `C5` expanded to exposure/color/focus/capture-format judgment;
- frame rate and shutter are contextual decisions, not universal cinematic recipes;
- artificial-light/display flicker is an observable capture defect requiring device/context-aware correction;
- LOG/HDR/profile use must match the real downstream color pipeline;
- `C7` now includes judder, motion blur, rolling-shutter, focus/exposure/WB pumping and unstable reflective-surface motion;
- `C8` preserves compatible frame-rate/profile/HDR choices across edit-connected clips.

### Gap C — automotive reflection control can become a cargo-cult gear recipe

Failure pressure: “use CPL,” “golden hour,” “black flags,” “2x lens,” “gimbal orbit.”

Current candidate response:

- reflection is modeled as geometry + surface + environment + source rather than a filter rule;
- camera/car/source repositioning precedes unavailable-gear invention;
- polarizers remain conditional and are not promised to remove metallic reflections;
- field of view is separated from perspective-causing camera distance;
- movement requires a communication/editing job.

Unresolved evidence obligation:

- prose coverage is not sufficient; comparative and artifact-first evaluation must show that the candidate actually applies these distinctions to real images/clips.

### Gap D — accepted picture is not necessarily accepted audiovisual source

Photography/DoP competence does not automatically confer production-sound engineering competence.

Repair made before freeze:

- production sound explicitly remains outside profession ownership;
- when required speech/engine/environment audio is material, candidate must expose the dependency and cannot claim the complete audiovisual take is accepted solely from picture quality.

## 2. Educator / competency-assessor perspective

### Construct risk A — evaluating vocabulary rather than professional judgment

A candidate can repeat “perspective,” “specular,” “negative fill” and still provide unusable advice.

Mitigation:

- fixtures require causal diagnosis and a measurable physical correction;
- operator executability is a separate evaluation family;
- actual images must be observed for artifact-first claims;
- subjective evaluation dimensions are separated: perspective/form, light/reflection, composition/background, restraint, executability and reshoot value.

### Construct risk B — a single aesthetic answer being treated as ground truth

Automotive capture contains legitimate alternate judgments depending on brief, surface, location and intended perception.

Mitigation:

- public still practical has no frozen “winner”;
- later release judgment must be calibrated against strong practitioner reference judgments;
- rule breaking/creative choice remains acceptable when rationale, risk and verification are explicit;
- hard constraints remain deterministic where possible.

### Construct risk C — text-only qualification overclaims image/video competence

Mitigation:

- evaluation plan requires actual still-image and actual video artifact families;
- if image/video bytes cannot be observed, those claims are marked `NOT EXECUTABLE` rather than passed narratively;
- real-still development set S01–S03 has already been established from project Drive assets;
- current three-car target folders contain no new media yet, so the target end-to-end practical cannot be claimed.

### Remaining assessor gap

A calibrated practitioner reference set does not yet exist. Until it does, professional taste/craft dimensions cannot receive a release PASS solely from model-graded prose.

## 3. Hiring-manager perspective

Question: would this candidate, used as an AI director for a non-professional human operator, reliably produce work materially closer to a hired automotive shooter than the existing checklist?

Evidence currently supporting plausibility:

- profession boundary is materially deeper than current Social Content Creative light-production direction;
- project baseline operator document demonstrates the real gap: it covers angles, duration, basic phone setup and completeness but not deeper form/reflection/perspective/capture diagnosis;
- candidate outputs include preparation, camera placement, reflection intent, capture format, movement path, acceptance cues and artifact-first reshoot logic.

Evidence still missing before a hiring-quality claim:

1. blind comparative outputs against a generic shot-list baseline;
2. practitioner-calibrated ranking on real automotive stills;
3. real automotive video diagnosis;
4. a non-professional operator following the directions in the field;
5. source-media usefulness confirmed by downstream Video Post-Production;
6. repeatability across at least materially different vehicle surfaces/body shapes and locations.

Therefore the hiring-manager verdict is **PROMISING CANDIDATE, NOT YET PROVEN PROFESSIONAL SUBSTITUTE FOR CAPTURE DIRECTION**.

## 4. Systems / workflow perspective

### Boundary check

No evidence currently justifies a new top-level workflow agent.

The capture work is tightly coupled to the Content Creator's approved shot jobs and must immediately hand physical instructions to the human operator, then source media to Video Post-Production. A modular capability avoids another workflow state/agent handoff while preserving a distinct professional model and evaluation boundary.

Revisit separate-agent architecture only if future work demonstrates one or more of:

- independent capture briefs that routinely exist outside Content Creator work;
- materially different tools/state/authority that cannot be composed safely;
- measurable quality or coordination benefit from independent critique/separation;
- capture scheduling/crew/location production management expanding into a separate accountable profession.

### Schema check

The current Auto Sales `creator-deliverable.schema.json` can carry professional capture direction inside canonical `shot_list`, `b_roll`, `block_execution` and `creator_checks` strings. No schema change is justified yet. Change only if practical evaluation shows information loss or machine-verification failure.

## 5. Security / truth / safety perspective

Hard failure coverage currently includes:

- fabricated device/equipment capability;
- concealed/staged-away vehicle condition presented misleadingly;
- experiment contamination;
- unsafe rolling/road shooting instruction;
- unverified road/filming permission;
- false claim that planned media was captured/accepted;
- artifact critique without actual artifact observation.

Project-local privacy requirements such as plate/customer/document handling should remain in Auto Sales specialization rather than being generalized into the reusable photographic core unless broader evidence warrants it.

## 6. Pre-freeze verdict

Architecture: **EXTEND** remains justified.

Top-level agent split: **NOT JUSTIFIED**.

Candidate completeness for entering qualification authoring: **CONDITIONALLY READY**, after development fixtures are updated to cover the newly added motion-format/flicker/audio boundary and repository static checks pass.

Production readiness: **NO**.

The next legitimate transition is:

`candidate stabilization -> targeted development fixtures -> static verification -> freeze/preregistration -> independent/calibrated semantic qualification -> actual still/video practical -> human executability -> Auto Sales composition/end-to-end gate`.
