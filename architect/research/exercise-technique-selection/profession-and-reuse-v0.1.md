# Exercise Technique & Selection — profession reconstruction and reuse decision

Status: v0.1 pre-SKILL professional model
Date: 2026-09-21
Target population: generally healthy adults performing resistance training for hypertrophy and/or strength.

## 1. Reconstructed profession

The target is not a generic fitness expert and not a clinical biomechanist. The work is best modeled as a **resistance-training technique and exercise-selection practitioner** drawing on:

- strength & conditioning / resistance-training practice — CORE;
- applied resistance-exercise biomechanics — CORE, but used as a constrained reasoning discipline rather than a source of universal posture rules;
- exercise selection and program-context reasoning — CORE;
- visual movement analysis for resistance exercise — CORE when media are supplied;
- fatigue / effort / limiting-factor interpretation — CORE;
- motor-control / coaching-feedback principles — CONTEXTUAL, used to choose a small actionable correction and verify it;
- anthropometry — CONTEXTUAL modifier only where evidence and observed movement make it decision-relevant;
- sports medicine / rehabilitation — OUT OF SCOPE except for BOUNDARY-CRITICAL recognition that pain/injury questions require escalation rather than diagnosis.

The practitioner may analyze resistance-training movement and make non-medical technique/exercise recommendations. It may not diagnose tissue injury, identify pathology from pain, prescribe rehabilitation, clear return to sport, or treat a movement pattern as proof of injury risk.

## 2. Professional outputs

1. A bounded exercise-selection recommendation tied to target muscle/function, strength specificity, equipment, ROM, stability, resistance profile, fatigue cost and program role.
2. A technique-analysis record that separates observation from inference and gives a confidence/visibility ceiling.
3. Classification of observed variation as acceptable individual variation; goal-specific trade-off; likely performance/stimulus-limiting technique issue; indeterminate from available evidence; or pain/medical boundary requiring escalation.
4. A limiting-factor hypothesis ranked by evidence, not a claim that appearance reveals muscle activation.
5. One or a few concrete technique changes with a causal purpose and an observable re-test criterion.
6. A request for a better view/data when the current media cannot support the requested conclusion.

## 3. Difficult recurring decisions

- Whether a visually unusual rep is actually wrong, merely individual, or a rational trade-off for the stated goal.
- Whether an exercise is a good fit for a target when ROM, stability, resistance profile, equipment and the trainee's observed limiting factor interact.
- Whether apparent form change is caused by load/fatigue, task strategy, setup, camera perspective, or a true loss of the intended movement constraint.
- Whether anthropometry materially changes setup/selection or is being used as an unsupported deterministic story.
- Whether a set is limited by the target muscle, another prime mover, stabilization, grip, coordination/skill, systemic/cardiorespiratory demand, equipment geometry, or pain.
- Whether a media input supports a qualitative judgment, a plane-specific observation, or no reliable conclusion.
- Whether a coaching correction is likely to improve the intended constraint without creating unnecessary complexity or fatigue.
- When pain, neurological symptoms, acute injury or health concerns terminate technique diagnosis and require a qualified clinician.

## 4. Decision-critical cues

Useful cues include, when observable:
- target goal and program role;
- exercise variant, equipment and setup;
- rep/load history, approximate effort or RIR if known;
- first/middle/late reps and rep-to-rep change;
- ROM actually completed;
- where velocity slows or the repetition fails;
- balance/support demands and unintended movement that consumes effort;
- whether the target movement constraint is preserved as fatigue rises;
- grip/stance/contact points;
- visible joint/segment paths in the camera plane;
- whether relevant joints and implement remain visible throughout the rep;
- camera position, lens perspective, frame rate, lighting and occlusion;
- pain report as an escalation cue, never as diagnostic evidence.

Misleading cues include:
- a single freeze-frame detached from the full rep;
- looks weird or social-media form rules;
- one body-segment ratio used to dictate a lift variant;
- EMG or feeling the muscle treated as direct proof of long-term hypertrophy;
- bar speed or RIR interpreted without exercise/load/set context;
- a 2D angle treated as a complete 3D joint-load estimate;
- any claim that a pain location reveals the injured tissue.

## 5. Expert-vs-average discriminators

A weak practitioner:
- searches for one canonical-looking form;
- labels deviations as errors without first establishing goal and visibility;
- chooses exercises by muscle-name matching;
- over-weights anthropometry or EMG;
- treats more stable or free weight as universally superior;
- gives many cues at once;
- diagnoses pain from movement.

A strong practitioner:
- starts from task, goal and evidence quality;
- distinguishes visible facts from biomechanical inference;
- uses biomechanics conditionally and compares plausible alternatives;
- recognizes technique specificity and legitimate inter-individual strategies;
- ranks limiting-factor hypotheses and states what evidence would disconfirm them;
- selects the smallest useful correction and verifies the next set/repetition;
- knows when the camera cannot answer the question;
- stops at the medical/rehabilitation boundary.

## 6. Existing Professional Core inventory

Repository catalog inspected at main SHA 62e75f3b5e6808617adab846a0549ce3dc254d04.

| Candidate core | Compatibility | Decision |
| --- | --- | --- |
| paid-media-performance-marketing | Different responsibilities, evidence, decisions and tools | REJECT |
| video-editing-post-production | Media inspection is adjacent, but professional construct is editing/QC rather than human movement analysis | REJECT as professional core |
| growth-experimentation-measurement | General evidence/measurement ideas are useful methodology, but not the target profession | REJECT as professional core |
| market-competitive-intelligence | Research discipline is reusable only through Agent Architect methodology, not as target practitioner | REJECT as professional core |
| social-content-creative | Different outputs and judgment | REJECT |
| sales-lead-conversion | Different outputs and judgment | REJECT |

Code/catalog search found no existing strength, hypertrophy, biomechanics, resistance-training technique or exercise-selection Professional Core.

## 7. Formal reuse decision

**Decision: BUILD NEW applied skill.**

Rationale:
- no existing core matches responsibility/output scope or professional judgment;
- adapting an unrelated core would create false inheritance and misleading qualification provenance;
- promoting this first applied artifact into a generic reusable core is not justified yet because reuse value, portability, independent qualification and cross-context regressions do not exist.

What is reused:
- Agent Architect's generic evidence, uncertainty, retrieval, tool-human-factors, evaluation-integrity, qualification stop-loss and professional-trust methodologies;
- repository conventions for evidence registers, competency maps, practical/adversarial evals and artifact versioning.

What is not inherited:
- no professional qualification PASS;
- no strength/biomechanics competence from unrelated cores;
- no trust tier.

Required new regressions:
- camera/occlusion uncertainty;
- acceptable individual variation;
- anthropometry non-determinism;
- load-induced technique change;
- false user premise;
- missing information;
- pain/medical boundary;
- exercise-selection trade-offs and limiting-factor ambiguity.

## 8. Architecture decision

Use one modular applied skill, not a multi-agent system.

Reason:
- the decisions are tightly coupled around one resistance-training case;
- independent specialist decomposition would add handoff/context cost without evidence of better outcomes;
- high-risk clinical judgment is not delegated to another AI role; it is explicitly escalated to a qualified human clinician.

Deeper knowledge is progressively disclosed through the evidence/reference and vision-analysis procedures rather than a new generic pack.

## 9. Scope / authority

Allowed:
- analyze exercise choice and observable resistance-training technique;
- propose reversible setup, ROM, load, stance/grip, tempo/control or exercise-variant changes within healthy-adult training;
- request additional media/data;
- state uncertainty and compare alternatives.

Not allowed:
- diagnose injury or disease;
- infer tissue damage from pain/location/video;
- prescribe rehabilitation or return-to-play;
- override clinician restrictions;
- present 2D video as clinical motion capture;
- claim injury prevention from cosmetic perfect form;
- autonomously change a user's training system without the required program context.

## 10. Unknown-unknown question

**What would a strong practitioner notice is missing, even though the user did not know to ask for it?**

Answer incorporated into the model:
- technique must be evaluated relative to a goal and task, not aesthetic conformity;
- early vs late reps matter because fatigue itself changes kinematics;
- video validity is a first-class professional competency;
- exercise selection needs a stimulus-to-fatigue and limiting-factor view, not only anatomy;
- anthropometry is often weaker evidence than online coaching culture implies;
- verification of a cue on a subsequent rep/set is part of competence;
- pain is a boundary condition, not another form variable.
