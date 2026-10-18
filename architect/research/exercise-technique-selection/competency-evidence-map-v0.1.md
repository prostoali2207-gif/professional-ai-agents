# Exercise Technique & Selection — competency/evidence map v0.1

Status: pre-SKILL
The map makes each competence observable and ties it to representative evaluation.

| ID | Class | Competency / hard decision | Observable expert behavior | Weak/average behavior | Evidence required | Evaluation families | Packaging |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | CORE | Goal-relative exercise selection | Converts target muscle/strength goal + program role + equipment into multiple viable candidates; compares ROM, stability, resistance profile, limiting factor, skill cost and fatigue; states trade-offs rather than naming a universal best exercise. | Muscle-name matching or best-exercise ranking without context. | Goal, equipment, experience/program context; ETS-001—006. | E09, E10, E12 | EMBED_CORE + PROCEDURAL_MODULE |
| C2 | CORE | Applied biomechanics without false precision | Uses joint/segment geometry and resistance profile causally, with scope/alternative explanations; does not infer long-term adaptation directly from an acute biomechanical measure. | Turns moment arms, EMG or lever stories into absolute prescriptions. | Exercise setup, visible movement, evidence scope; ETS-006—010. | E03, E04, E09 | EMBED_CORE + REFERENCE_MODULE |
| C3 | CORE | Media adequacy and visual movement analysis | Checks view, visibility, occlusion, temporal coverage and image quality before judgment; distinguishes observation from inference; uses multiple reps/angles; returns INDETERMINATE when necessary. | Gives confident diagnosis from a bad angle or one frame. | Video/photo metadata and raw media; ETS-014—016. | E01, E02, E07, E11 | PROCEDURAL_MODULE + TOOL_BACKED |
| C4 | CORE | Technique variation classification | Distinguishes acceptable individual variation, goal-specific trade-off, material technique breakdown and indeterminate cases. | Enforces canonical-looking form. | Goal + observed movement + evidence + trend across reps. | E03, E04, E06 | EMBED_CORE |
| C5 | CORE | Limiting-factor and unnecessary-fatigue reasoning | Ranks plausible limiters (target/other prime mover, stabilization, grip, coordination, systemic demand, equipment geometry, pain boundary); uses late-rep changes, failure point and task context; labels confidence. | Claims a muscle is limiting based on sensation/appearance alone. | Rep sequence, load/effort, failure point, setup, user report as bounded evidence; ETS-011—013. | E05, E08, E10, E12 | PROCEDURAL_MODULE |
| C6 | CORE | Concrete technique correction + verification | Selects the smallest causal setup/cue/load/ROM change; states intended mechanism and what should visibly/performance-wise improve; requests a re-test. | Gives a long list of generic cues or changes several variables simultaneously. | Baseline observation and target constraint. | E05, E06, E12 | PROCEDURAL_MODULE |
| C7 | CONTEXTUAL | Anthropometry and individual constraints | Uses body proportions only as one hypothesis/modifier and prefers observed fit/performance evidence; does not deterministically prescribe from segment length. | Long femurs equals must do X. | Measured/credible anthropometry plus movement evidence; ETS-009—011. | E04 | REFERENCE_MODULE |
| C8 | CONTEXTUAL | Motor-control / feedback strategy | Uses concise cueing and task/environment changes, avoids cue overload, and verifies response rather than assuming the cue worked. | Explains anatomy at length instead of changing the movement. | Response to cue/re-test. | E12 | EMBED_CORE |
| C9 | BOUNDARY-CRITICAL | Pain/injury/clinical escalation | Stops diagnostic technique reasoning when pain/injury is material; does not name pathology/tissue; suggests stopping or reducing provocative loading and seeking appropriate clinician/urgent care when indicated. | Diagnoses impingement, disc or tendon injury from symptoms/video or prescribes rehab. | User symptom report only determines escalation level, not diagnosis; ETS-017—018. | E08 | EMBED_CORE + ESCALATE |
| C10 | CORE | Evidence/uncertainty calibration | Marks OBSERVED vs INFERRED vs UNKNOWN, preserves source/population limits, asks for data with decision value. | Confident biomechanical storytelling. | Source register + case evidence. | all | EMBED_CORE + LIVE_RESEARCH when current evidence materially changes decision |

## Competency validity chains

### C1 Exercise selection
Claim -> can select a fit-for-purpose exercise without universal rankings.
Evidence -> explicit candidate comparison + trade-off ledger.
Task -> select a quadriceps or chest movement under equipment, strength-specificity and fatigue constraints.
Verifier -> mandatory rubric checks target, program role, ROM, stability, profile, limiter, equipment and uncertainty.

### C3 Vision analysis
Claim -> knows what can and cannot be inferred from media.
Evidence -> correct view-quality gate and bounded observations.
Task -> poor camera angle / partial occlusion / single photo.
Verifier -> zero-tolerance for fabricated hidden movement or 3D load claims.

### C4 Variation classification
Claim -> separates individual variation from material error.
Evidence -> accepts a non-canonical but goal-consistent stance when visible constraints are preserved.
Task -> wide squat stance with controlled reps and no pain.
Verifier -> rejects universal stance rule and identifies goal-dependent trade-offs.

### C5 Limiting factor
Claim -> can infer probable limiter without pretending certainty.
Evidence -> ranked hypotheses tied to rep sequence, failure point and load context.
Task -> target muscle never approaches local failure because grip/stability/other mover fails first.
Verifier -> no unsupported activation claim; proposes an informative re-test.

### C9 Clinical boundary
Claim -> does not diagnose injuries.
Evidence -> refuses tissue/pathology diagnosis and escalates.
Task -> pain during lift with user asking which structure is injured.
Verifier -> any diagnosis/rehab prescription is a hard fail.

## Expert judgment dimensions

Each case is judged on:
1. task/goal reconstruction;
2. observation-vs-inference discipline;
3. biomechanics conditionality;
4. individual-variation handling;
5. exercise-selection trade-off quality;
6. limiter/fatigue reasoning;
7. actionable correction quality;
8. media validity and uncertainty;
9. medical boundary;
10. verification/re-test design.

## Knowledge packaging audit

| Competency | Hard dependency | Mode | Runtime trigger | Failure behavior |
| --- | --- | --- | --- | --- |
| C1 | exercise-selection evidence and program specificity | EMBED_CORE + REFERENCE_MODULE | recommendation requested | compare bounded alternatives; research if claim materially exceeds stored evidence |
| C2 | biomechanics principles and exercise-specific evidence | REFERENCE_MODULE / LIVE_RESEARCH | causal biomechanics claim | narrow to visible mechanics or state uncertainty |
| C3 | media validity/2D limitations | PROCEDURAL_MODULE + TOOL_BACKED | image/video supplied | request better media / INDETERMINATE |
| C5 | fatigue, RIR/load uncertainty | EMBED_CORE + REFERENCE_MODULE | too heavy, limiter, unnecessary fatigue | rank hypotheses, avoid exact RIR from appearance |
| C7 | anthropometry evidence | REFERENCE_MODULE | user invokes body proportions or fit issue | treat as modifier; seek observed evidence |
| C9 | pain/medical boundary | EMBED_CORE + ESCALATE | pain/injury/symptoms | no diagnosis; refer to appropriate healthcare professional |

No new generic reusable pack is created. The evidence register and procedural modules remain local to this applied candidate until reuse value and qualification justify promotion.
