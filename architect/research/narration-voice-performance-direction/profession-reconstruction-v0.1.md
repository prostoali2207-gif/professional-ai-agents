# Narration & Voice Performance Direction — Profession Reconstruction v0.1

issue: #304
date: 2026-09-13
status: RESEARCH / BUILD NEW APPROVED / NOT QUALIFIED
working_core_id: narration-voice-performance-direction

## Mission

Turn an approved spoken script plus authorial intent into executable, evidence-grounded direction for a human narrator, then judge actual recorded takes for performance quality and downstream editability.

The AI specialist directs and critiques. The human performs.

## Profession boundary

### Own

- interpret an approved spoken script for performance;
- thought grouping / phrasing;
- pace and pause decisions;
- stress / emphasis;
- pitch / intonation / modulation where useful;
- articulation / intelligibility coaching;
- breath planning for the script;
- naturalness vs announcer/overacting diagnosis;
- vocal energy and emotional congruence;
- coaching a non-professional narrator with bounded, actionable notes;
- multiple-take direction;
- pickup continuity;
- compare actual takes;
- diagnose whether a weak result is primarily:
  - text/script;
  - vocal performance;
  - technical recording/capture;
  - downstream post issue;
- accept / reject / request pickup on source vocal performance;
- hand accepted take(s) and performance notes to Post.

### Do not own

- audience / positioning / offer / KPI;
- commercial facts;
- final script facts, hook, CTA or authorial wording;
- camera framing/exposure/movement;
- recording noise removal, EQ, compression, loudness or final mix;
- publishing;
- medical diagnosis;
- speech-language pathology;
- vocal-health treatment;
- synthetic voice cloning or speaker replacement by default.

## Required upstream / downstream chain

`Content Architecture -> Social Content Creative -> Narration & Voice Performance Direction -> Human Narrator -> Capture/recording -> Narration source QC -> Video Editing & Post-Production`

Practical composition may interleave Narration Direction and Capture because microphone behavior affects performance, but ownership remains distinct:

- Narration Direction owns the human read/performance.
- Capture owns technical source-recording conditions.
- Post owns edit/repair/mix after source exists.

## Profession evidence

### EV-NV-01 — voice-over is performance, not text reading

Al Jazeera Media Institute, Dubbing & Voice Over:
- distinguishes voice-over from plain reading;
- trains pitch, articulation, delivery, pauses and production-specific tone/rhythm;
- includes practical recording, feedback and performance correction;
- includes microphone handling as adjacent studio craft.

Decision supported:
Actual vocal delivery requires a professional skill layer beyond scriptwriting.

### EV-NV-02 — narration uses modulation, rhythm and pause to serve meaning

Al Jazeera Media Institute, Documentary Voiceover:
- trains articulation, breathing, tone, modulation, rhythm and pauses;
- explicitly ties vocal control to clarity and message credibility.

Decision supported:
A narrator should not be coached by one universal "more energy" rule.

### EV-NV-03 — voice work requires interpretation / acting judgment

Backstage guidance citing working voice directors/casting professionals:
- recommends acting as a foundation;
- identifies pitch, pace, pause, tone, volume, emphasis and intonation as observable performance dimensions;
- describes voice-over as a specialized performance craft.

Decision supported:
Performance direction requires interpretation and behavior change, not only audio engineering.

### EV-NV-04 — text and prosody are separate evidence layers

Rosenberg & Hirschberg, Speech Communication 51(7), 640–655.
DOI: 10.1016/j.specom.2008.11.001.

Decision supported:
Lexical/syntactic content and acoustic/prosodic features should not be collapsed into one core or inferred from each other.

### EV-NV-05 — professional voice direction is communication with the performer

Voices.com / Sound Stories, discussion with voice-acting coach/director Sunday Muse:
- director must translate desired effect into performer-understandable direction;
- generic line reads such as "higher/lower/quieter" can fail;
- environment, action and physical/mental framing can help the actor produce the intended read;
- encouragement/communication quality is part of the directing job.

Decision supported:
Coaching quality is itself a competency; an accurate critique that a non-professional cannot execute is insufficient.

## Compatibility / reuse decision

### Social Content Creative 0.1.0 + authorial-voice v0.2 candidate
**REJECT as owner / REUSE upstream.**

Transfer:
- exact words;
- authorial stance;
- speakability;
- intended emphasis opportunities.

Non-transfer:
- actual prosody;
- articulation;
- take performance;
- performance coaching.

### Video Capture / Camera Operations candidate #294
**REJECT as parent / REUSE composition boundary.**

Transfer:
- technical microphone/device constraints;
- recording environment;
- source-media QC;
- operator execution constraints.

Non-transfer:
- script interpretation;
- acting/narration craft;
- prosody coaching;
- performance direction.

### Video Editing & Post-Production 0.1.0
**REJECT as owner / REUSE downstream.**

Transfer:
- take assembly/selection where authorized;
- technical repair;
- audio mix;
- final perceptual QC.

Non-transfer:
- live human performance coaching before recording.

### Architecture decision
**BUILD NEW.**

Reason:
- distinct recurring responsibility;
- stable professional craft;
- different evidence object: actual human vocal take;
- adjacent failures cannot reliably repair weak source performance;
- recurring need across faceless Personal Brand content;
- clean handoff boundaries.

## Competency model

### NV-01 Script interpretation
Can identify:
- thought units;
- semantic pivots;
- proof-bearing phrases;
- emotional/authorial intent;
- where the read should accelerate, settle, pause or stress.

Does not rewrite facts unless handed back to Social Content Creative.

### NV-02 Pace / rhythm / pause judgment
Can:
- distinguish conversational irregularity from robotic evenness;
- place pauses for comprehension, emphasis or tension;
- avoid breathless constant-speed delivery;
- avoid theatrical pauses that make technical content feel fake.

### NV-03 Stress / emphasis
Can:
- identify which word carries the thought;
- prevent random stress on function words;
- preserve factual qualifiers and conditional language;
- avoid over-emphasizing every noun.

### NV-04 Prosody / modulation
Can:
- use pitch/intonation variation to clarify meaning;
- distinguish natural conversational movement from forced "radio voice";
- scale energy to format/content.

### NV-05 Articulation / intelligibility
Can:
- identify swallowed endings, blurred consonants, rushed technical terms and unclear word boundaries;
- give bounded mechanical practice direction;
- escalate persistent speech/medical concerns rather than diagnosing.

### NV-06 Breath and phrasing
Can:
- identify phrases too long for a natural read;
- advise breath points;
- hand true script defects upstream rather than forcing the narrator through them.

### NV-07 Naturalness / anti-announcer
Can diagnose:
- reading punctuation instead of meaning;
- over-projecting;
- artificial smile voice;
- monotone;
- fake dramatic emphasis;
- "YouTube presenter" overacting.

### NV-08 Authorial fit
Can preserve:
- user's real conversational identity;
- intended intimacy / authority level;
- brand register.

Must not optimize the human into a generic broadcaster.

### NV-09 Coaching executability
Direction should be:
- one or two changes per take when possible;
- observable;
- understandable to a non-professional;
- testable in the next recording.

Bad:
"be more charismatic."

Better:
"На первой фразе не ускоряйся. Ударение на 'PDF'. После 'ничего не знает' — короткая пауза, затем вопросы чуть быстрее."

### NV-10 Take diagnosis / iteration
For each take:
- identify strongest moment;
- identify single highest-value repair;
- distinguish global vs line-specific issue;
- avoid asking for a full retake when pickup is enough;
- avoid polishing indefinitely after useful performance is achieved.

### NV-11 Pickup continuity
Can match:
- pace;
- energy;
- mic distance/performance posture;
- sentence-entry/exit tone;
- surrounding take character.

### NV-12 Root-cause routing
Classify:
- SCRIPT_PROBLEM -> Social Content Creative;
- PERFORMANCE_PROBLEM -> Narration Direction;
- CAPTURE_PROBLEM -> Video Capture;
- POST_PROBLEM -> Video Post;
- MEDICAL/SPEECH_HEALTH -> human specialist.

### NV-13 Source performance QC
Judge actual audio for:
- intelligibility;
- naturalness;
- emphasis;
- rhythmic variation;
- authorial fit;
- emotional congruence;
- continuity;
- downstream editability.

## Expert-vs-average discriminators

Average:
- says "speak slower", "more energy", "more confident";
- tries to fix every problem at once;
- confuses clean audio with strong delivery;
- treats charisma as pitch/speed formula;
- overdirects every word;
- prefers broadcaster voice over authentic fit.

Strong practitioner:
- identifies the thought behind the line;
- chooses one repair that unlocks multiple symptoms;
- explains direction in performer-executable terms;
- knows when the script is causing the bad read;
- knows when technical recording is causing the issue;
- preserves the speaker's identity;
- stops when further polish has low value.

## Failure modes

- charisma = louder/faster;
- overacting;
- monotone correction through random pitch changes;
- mechanical punctuation reading;
- constant high energy;
- too many notes per take;
- imitation of a reference creator's cadence;
- forcing profanity/slang through performance;
- hiding script defects with performance tricks;
- treating diction issue as medical diagnosis;
- treating noise/EQ as performance coaching;
- endless retakes;
- AI voice replacement as shortcut.

## Required evaluation design

### Deterministic/boundary fixtures
- script-vs-performance routing;
- medical boundary;
- synthetic voice pressure;
- authority boundary;
- fact qualifier preservation.

### Audio/performance fixtures
Require real or controlled audio takes for:
- monotone but intelligible;
- rushed technical terms;
- overacting;
- wrong stress;
- unnatural pauses;
- flat joke/punchline;
- pickup mismatch;
- noisy-but-good-performance vs clean-but-flat-performance;
- script too long for natural breath.

### Practical gate
Real Personal Brand Reel:
1. approved script;
2. baseline human take;
3. candidate direction;
4. take 2;
5. optional targeted take 3/pickup;
6. blind/calibrated review;
7. Video Post acceptance.

No practical PASS without actual source audio.

## Current gate

Profession reconstruction: **PASS TO EVIDENCE / EVALUATION DESIGN.**

No candidate implementation or qualification claim yet.
