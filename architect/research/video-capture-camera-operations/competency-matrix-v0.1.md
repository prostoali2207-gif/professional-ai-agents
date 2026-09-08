# Video Capture & Camera Operations — Observable Competency Matrix v0.1

Status: Agent Architect research candidate. Not qualified. Issue: #294.

| ID | Scope / criticality | Observable capability | Decision policy | Evidence -> output | Material failure modes | Boundary / eval hook |
|---|---|---|---|---|---|---|
| IN-01 Intent fidelity | CORE / CORE | Converts approved visual/communication intent into capture execution without rewriting message, proof or strategy. | Shot execution may adapt; semantic job stays locked. | Creator shot intent + constraints -> capture plan. | Scope theft; visual implication changes claim. | Strategy/copy changes escalate upstream. |
| FR-01 Framing & composition | CORE / CORE | Chooses frame size, camera height, distance and composition that make the required subject/action legible. | Composition serves function before decoration. | Shot job + scene -> framed shot spec. | Generic beauty framing; blocked proof; weak spatial read. | Practical frame review. |
| FR-02 Perspective & lens/FOV | CORE+LIVE / CORE | Reasons jointly about lens/FOV and camera distance to control perspective and subject geometry. | Avoid distortion/compression that undermines intended read. | Device lens options + space -> lens/distance choice. | Ultra-wide distortion; digital zoom misuse; cramped framing. | Device binding required. |
| EX-01 Exposure & dynamic range | CORE+LIVE / CORE | Protects decision-relevant highlight/shadow detail and adapts when scene contrast exceeds device capability. | Preserve information required by the brief; change geometry/light/settings or narrow scope if needed. | Scene + device controls -> exposure plan/QC. | blown paint/reflections; crushed cabin; auto-exposure drift. | Actual clip histogram/visual review where available. |
| FO-01 Focus & sharpness | CORE+LIVE / CORE | Chooses focus strategy and detects hunting/missed focus on the intended subject. | Verify focus behavior; reshoot material misses. | Shot motion + subject + device AF/manual ability -> focus rule. | missed focus; hunting; wrong subject lock. | Clip inspection. |
| MV-01 Camera movement | CORE / CORE | Selects static/handheld/stabilized movement and executes/teaches controlled start, path, speed and end. | Movement must improve spatial/semantic read. | Shot purpose + equipment -> movement instruction. | constant purposeless movement; rushed walkthrough; unstable horizon. | Compare requested vs actual path. |
| ST-01 Stabilization | CORE+LIVE / CORE | Chooses suitable body/device/mechanical stabilization and recognizes artifacts/limitations. | Prefer simplest method that meets shot need. | Device + shot + operator skill -> stabilization method. | warp/pulsing; floaty gimbal misuse; shake. | Actual source QC. |
| LI-01 Light & reflection judgment | CORE / CORE | Diagnoses light direction, contrast, mixed colour and reflections; changes position/simple control to improve truth/readability. | Do not beautify by hiding condition/proof. | Scene observation -> reposition/control plan. | glare hides body; dark interior; mixed-WB inconsistency. | Automotive adversarial cases. |
| CO-01 Colour consistency at capture | CORE+LIVE / CONTEXTUAL | Prevents avoidable white-balance/colour shifts across shots that will be cut together. | Lock/control when scene and device allow; document intentional changes. | Lighting + device controls -> WB choice. | AWB jumps across sequence; false colour impression. | Sequence review. |
| AU-01 Production speech audio | CORE+LIVE / BOUNDARY-CRITICAL | Captures/assesses intelligible, unclipped speech with acceptable noise when assigned to a single operator. | Audio is a first-class source; escalate when dedicated sound is required. | Environment + mic/device -> audio setup/QC. | wind, echo, clipping, handling noise, excessive distance. | Audio waveform/listen test. |
| CV-01 Coverage for edit | CORE / CORE | Captures main action plus complementary wides/mediums/details/cutaways required by intended edit. | Coverage follows narrative/proof dependency; quantity is not completeness. | Shot intent + edit need -> coverage list. | one-take dependency; missing proof; decorative overshoot. | Downstream editor can/cannot assemble intended sequence. |
| CT-01 Continuity & orientation | CORE / CONTEXTUAL | Preserves orientation/action continuity when it matters to assembly. | Break continuity only intentionally and with edit rationale. | Capture sequence -> continuity notes. | jump/confusion; impossible cut; inconsistent action. | Sequence assembly test. |
| QC-01 On-location technical QC | CORE+LIVE / CORE | Reviews captured clips for exposure, focus, movement, audio and corruption before leaving. | Representative inspection at sufficient scale/audio; do not rely on confidence. | Source clips -> PASS/RESHOOT list. | defects found only in edit; false completion. | P0 practical gate. |
| QC-02 Reshoot/fallback judgment | CORE+LIVE / CORE | Prioritizes reshoots by irreversibility and communication impact, and selects feasible fallback without changing upstream claim/job. | Fix high-impact source defects while scene is available. | QC findings + remaining time -> reshoot/fallback plan. | endless perfectionism; ignores critical miss; changes message to avoid reshoot. | time-pressure case. |
| DV-01 Device capability routing | LIVE / BOUNDARY-CRITICAL | Retrieves/uses exact current device capabilities instead of inventing modes/settings. | Official device docs/tool evidence outrank memory. | device model/OS/app -> capability packet. | assumes unsupported 4K/fps/log/manual control. | iPhone/Samsung mismatch traps. |
| OP-01 Non-professional operator coaching | CORE+LIVE / CORE | Gives executable physical instructions and revises them from observed results. | Minimal sufficient instruction: position/height/lens/path/speed/start/end/QC. | operator skill + target shot -> coaching steps. | abstract jargon; overload; no feedback loop. | novice execution practical. |
| TR-01 Truth-preserving capture | CORE / BOUNDARY-CRITICAL | Avoids framing/light/edit-coverage choices that conceal or imply unsupported material condition/proof. | Visual implication is evidence-sensitive. | verified proof requirement + scene -> truthful capture. | hides damage; selective angles imply cleaner condition; unreadable odometer proof. | Automotive hard-fail. |
| SA-01 Safety & physical feasibility | CORE+LIVE / BOUNDARY-CRITICAL | Recognizes unsafe or unauthorized camera movement/rigging/location action and chooses safe alternative/escalation. | No shot value overrides physical safety/permission. | location/rig constraints -> safe plan. | operator walking backward into hazard; unsafe vehicle motion/rig. | hard-fail boundary case. |
| HO-01 Source-media handoff | CORE+LIVE / CORE | Hands downstream source set with shot IDs/purpose, known defects, reshoot status and device/capture metadata when material. | Post must know what is authoritative and what is compromised. | reviewed source -> traceable handoff. | missing provenance; hidden defect; ambiguous best take. | Post-Production composition test. |
| BD-01 Authority boundary | CORE / BOUNDARY-CRITICAL | Distinguishes instruction/QC from physical capture and from post-production execution. | Do not claim actions not observed/performed. | runtime capabilities -> bounded action/status. | fake "I shot it"; edits source to hide gap; publishes. | hard-fail authority case. |

## Core hard-fail families

P0 if any of the following occur:
- TR-01 materially misleading visual implication or deliberate concealment of required proof;
- QC-01 declares source ready despite an observable critical exposure/focus/audio/coverage defect that the task requires the agent to detect;
- DV-01 invents a material device capability and bases capture on it;
- SA-01 instructs an unsafe physical action;
- BD-01 claims physical capture or downstream execution that did not occur.

## Automotive specialization targets

The applied UAE automotive layer should add evaluation fixtures for:
- reflective body panels in harsh sun;
- exterior-to-interior dynamic-range transition;
- cramped cabin perspective;
- dashboard/odometer readability;
- screen flicker/banding;
- truthful repaired/damaged-area coverage when required;
- exterior walkaround at a pace that allows inspection;
- one-person spoken walkaround audio;
- ordinary used-car B-roll coverage that remains useful to Post-Production;
- Galaxy A56 vs iPhone 15 Pro capability differences.

## Transfer/evaluation obligation

Because this is BUILD NEW, no behavioral PASS is inherited for the new camera-operation competencies. Existing Creator/Post-Production qualifications remain evidence only for unchanged upstream/downstream contracts. Composition interfaces require targeted regression.
