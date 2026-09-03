# Automotive Commercial Capture Direction — Evaluation Plan v0.1

Status: DEVELOPMENT PLAN / NOT A RELEASE GATE
Candidate: `professional-model-candidate-v0.1.md`
Issue: #229

## Purpose

Prove that the extension produces materially stronger capture decisions than generic content-creator shot lists while preserving the qualified host core's truth, experiment and authority invariants.

A polished textual plan is insufficient evidence. The capability claims artifact-first critique and human-executable capture direction; therefore final qualification requires actual automotive still/video artifacts and observable reshoot decisions.

## Evaluation layers

### Layer A — deterministic / semantic hard constraints

Development fixtures cover:

- no invented equipment/device features;
- no commercial-fact invention or condition concealment;
- no experiment-lock contamination;
- no unsafe road/moving-car operating instructions;
- pre-capture vehicle/location preparation without condition falsification;
- perspective reasoning includes camera position/distance rather than lens-number folklore;
- reflection control is conditional and does not treat polarization as universal;
- frame-rate/shutter/profile decisions are contextual rather than status-driven recipes;
- artificial-light/display flicker is diagnosed at capture when observed;
- rolling-shutter/motion defects are not delegated to post by default;
- movement is tied to shot purpose;
- beauty vs proof responsibilities remain distinct;
- material audio dependencies are surfaced without claiming production-sound expertise;
- source-media handoff and continuity are planned.

P0/P1 hard failures in any release evaluation are disqualifying regardless of aggregate creative quality.

### Layer B — comparative professional judgment

Pairwise cases should compare candidate behavior with plausible generic alternatives such as:

- memorized “front 45 / side / rear 45” list;
- ultra-wide close hero because it fits the car;
- “shoot during golden hour” without reflection/environment diagnosis;
- “use a CPL to remove reflections” as a universal rule;
- generic gimbal orbit/push-in recipe;
- universal 24 fps / LOG / HDR “professional” recipes;
- aesthetic critique such as “make it more premium” without causal reshoot instruction.

Judges evaluate separately:

1. professional diagnosis;
2. automotive surface/form judgment;
3. optics/perspective reasoning;
4. lighting/reflection judgment;
5. camera/motion/capture-format craft;
6. operator executability;
7. artifact critique quality;
8. truth/safety/brief integrity;
9. downstream edit usefulness.

Subjective dimensions require calibrated comparative or multi-judge review; do not use one uncalibrated scalar model score as the sole release evidence.

### Layer C — artifact-first still-image practical gate

Use real automotive images containing combinations of:

- close-wide nose exaggeration;
- weak stance caused by camera height;
- cluttered horizon/background tangencies;
- camera/operator reflection;
- building/pole reflections cutting body lines;
- windshield glare;
- clipped paint highlights;
- underexposed dark paint/interior;
- color/WB mismatch;
- focus/shake defect;
- condition area that beauty framing must not hide;
- acceptable intentional reflection that should **not** be removed.

For each artifact the candidate must:

1. identify the shot's intended job from the case packet;
2. observe the artifact rather than invent unseen detail;
3. rank material defects;
4. identify causal mechanism;
5. prescribe a measurable reshoot change;
6. preserve already-correct variables;
7. identify a bounded fallback if the environment/equipment prevents the preferred solution.

A public real-still development set is recorded in `practical-still-dev-v0.1.md` using three existing Google Drive automotive photographs. It is development evidence only and cannot become held-out release evidence.

### Layer D — artifact-first video practical gate

Use real short clips with defects such as:

- unstable walking orbit;
- speed ramp impossible to rescue because source movement is inconsistent;
- exposure/WB pumping;
- autofocus hunting;
- operator reflection traversing bodywork;
- pan speed mismatched to subject motion;
- flicker/banding from artificial lighting or displays;
- rolling-shutter/skew under aggressive movement;
- incompatible capture profiles/frame rates across edit-connected clips;
- no usable handles;
- continuity direction conflict;
- excessive motion on a proof/detail shot;
- good static clip that should be accepted rather than needlessly reshot.

Candidate must diagnose capture-vs-post defects and avoid routing fixable capture failures to the editor by default.

### Layer E — non-professional operator executability

A human with no professional camera background receives only the candidate's shot instruction plus declared equipment/location packet.

Measure whether the operator can determine without guessing:

- what to prepare before shooting;
- where to stand;
- approximate camera height/distance;
- what to include/exclude;
- how car/background/light should relate;
- what movement to perform and how long;
- what visual cue means success/failure;
- what fallback to use.

Ambiguous adjectives without physical instructions fail this construct.

### Layer F — applied Auto Sales interaction gate

Run the capability inside the real chain:

`Content Analyst spec -> Content Creator + Capture Direction -> human source capture -> Video Post-Production -> approval artifact`

Verify:

- no strategy/offer/KPI/CTA mutation;
- exact vehicle/proof obligations preserved;
- experiment variant controls preserved;
- source media actually supports planned proof and edit blocks;
- post-production can identify preferred takes and known capture deviations;
- Analytics can still trace experiment/content/creative IDs after the extension.

## Release protocol requirements

Before scored qualification:

1. candidate content/digest must be frozen;
2. public development fixtures must be separated from held-out cases;
3. held-out authoring and judging must be independent from candidate optimization to the degree supported by infrastructure;
4. subjective creative/craft judgments require calibration against strong practitioner reference judgments;
5. actual artifact families must be executable in the evaluation environment; otherwise mark them `NOT EXECUTABLE` and do not claim those capabilities;
6. thresholds and hard-fail semantics must be preregistered before scored candidate runs;
7. Auto Sales specialization requires its own practical interaction regression even if reusable capability qualification passes.

## Current gate state

- Profession reconstruction: PASS for candidate construction.
- Reuse decision: EXTEND.
- Mandatory expert-gap/red-team: PASS for entering qualification authoring; unresolved evidence obligations retained.
- Candidate professional model: v0.1 FROZEN for qualification authoring at commit `6e34be04f1bc6912c95e5f6c0b34d1ccf9ccf13c`, git blob `6824ba3256ab6f3b51c5596f6fd6e42e013937f7`.
- Public development fixtures: PRESENT — main 16 cases + preparation 3 cases + motion-technical 5 cases.
- Generic repository qualification static preflight: PASS on branch CI after candidate stabilization.
- Agent Architect Research + RCE deterministic gate: PASS; paid semantic portion was not executed by that generic CI path.
- Real-still public development artifacts: PRESENT / S01–S03 retrievable and visually inspectable during development; candidate scored practical NOT RUN.
- Comparative practitioner calibration: NOT RUN.
- Held-out pack: NOT AUTHORED/FROZEN.
- Still release practical gate: NOT RUN.
- Video practical gate: NOT RUN; current target three-car Drive folders had no media at last check.
- Human executability gate: NOT RUN.
- Auto Sales interaction gate: NOT RUN.

Therefore status remains **NOT QUALIFIED**.
