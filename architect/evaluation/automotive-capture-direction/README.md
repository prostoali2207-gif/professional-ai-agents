# Automotive Commercial Capture Direction — Evaluation Workspace

Issue: #229
Applied integration tracker: `prostoali2207-gif/auto-sales-growth-system#37`
Status: **FROZEN CANDIDATE / NOT QUALIFIED**

## Architecture

Decision: `EXTEND social-content-creative@0.1.0` with a modular professional capture-direction capability used by Content Creator. Do not add a new top-level workflow agent unless later evidence justifies the coordination boundary.

Human remains the physical camera operator.

## Frozen candidate

- model: `professional-model-candidate-v0.1.md`
- candidate commit: `6e34be04f1bc6912c95e5f6c0b34d1ccf9ccf13c`
- git blob: `6824ba3256ab6f3b51c5596f6fd6e42e013937f7`
- freeze record: `candidate-freeze-v0.1.json`

## Research / architecture

- `../../research/automotive-capture-direction/profession-reconstruction-and-reuse-v0.1.md`
- `../../research/automotive-capture-direction/expert-gap-red-team-v0.1.md`

## Public development evaluation

- `fixtures-dev-v0.1.json` — 16 core semantic/adversarial cases
- `fixtures-dev-v0.1-preparation.json` — 3 pre-capture preparation/truth cases
- `fixtures-dev-v0.1-motion-technical.json` — 5 frame-rate/flicker/profile/rolling-shutter/audio-boundary cases
- `practical-still-dev-v0.1.md` — real Google Drive automotive stills S01–S03; development only
- `evaluation-plan-v0.1.md` — required release evidence and current gate state
- `qualification-route-decision-v0.1.md` — deterministic/subscription/metered/artifact route status

## Current verified state

- profession reconstruction: complete for qualification authoring;
- reuse decision: EXTEND;
- expert-gap/red-team: complete; preparation and motion-technical gaps repaired before freeze;
- generic repository qualification static preflight: PASS after stabilization;
- Agent Architect Research + RCE deterministic gate: PASS after stabilization;
- real-still development artifacts: retrievable and observable;
- independent semantic qualification: NOT RUN;
- practitioner-calibrated subjective craft gate: NOT RUN;
- held-out pack: NOT AUTHORED/FROZEN;
- target real-video practical: NOT EXECUTABLE YET because the target Drive folders contained no media at last inspection;
- human operator executability: NOT RUN;
- Auto Sales end-to-end integration: NOT RUN;
- production binding: intentionally NOT DONE.

## Stop condition

Do not claim qualification or bind this capability into production until independent/calibrated semantic evaluation, actual still/video practical evidence, human executability and the Auto Sales interaction gate satisfy the frozen release protocol that will be preregistered before scored runs.
