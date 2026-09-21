# Hypertrophy Training — competency map v0.1

Status: PRE-SKILL
Date: 2026-09-21

## Competency contract

| ID | Competency | Scope | Expert discriminator | Critical observable | Evidence basis | Eval family |
|---|---|---|---|---|---|---|
| HT-C01 | Training-state reconstruction | CORE | Separates plan, actual performance, technique/setup changes, RIR confidence, adherence and recovery context before acting | Builds a current state and marks material unknowns | HT-S21, HT-S22 + Agent Architect state methodology | input_sufficiency, state_continuity |
| HT-C02 | Goal/priority decomposition | CORE | Separates muscle-size targets from exercise-specific strength targets and resolves conflicts explicitly | Priority map changes exercise order/load/specificity without sacrificing unrelated hypertrophy work | HT-S01, HT-S02, HT-S13 | mixed_goal_tradeoff |
| HT-C03 | Weekly volume prescription | CORE | Anchors dose to prior tolerated training and changes volume only with trajectory/recovery evidence | Set exposure is neither universalized nor increased reflexively | HT-S01, HT-S03, HT-S04, HT-S05 | volume_decision |
| HT-C04 | Load/rep/intensity prescription | CORE | Uses heavier practice for strength specificity while allowing broad hypertrophy loads | Load choice matches adaptation and exercise constraints | HT-S01, HT-S02, HT-S17 | load_rep_decision |
| HT-C05 | Effort / RIR-RPE regulation | CORE | Treats proximity to failure as a continuum; calibrates confidence and avoids failure dogma | Target RIR changes by exercise/risk/session context; uncertainty is visible | HT-S06–HT-S11 | rir_failure |
| HT-C06 | Progression/autoregulation | CORE | Progresses the smallest useful variable based on comparable exposures; can HOLD when no change is justified | Specific increase/hold/regression rule tied to observed history | HT-S10, HT-S11, HT-S21 | progression |
| HT-C07 | Fatigue/recovery management | CORE | Uses multiple longitudinal signals and distinguishes acute fatigue from maladaptation | Reduces fatigue-producing variables only when trend/context supports it | HT-S08, HT-S09, HT-S21–HT-S23 | fatigue_deload |
| HT-C08 | Exercise selection/order/substitution | CORE | Preserves target function and strength specificity while balancing stability, ROM, tolerance, loadability and measurement quality | Substitution rationale is function-based, not name-based | HT-S13–HT-S17 | exercise_substitution |
| HT-C09 | Plateau diagnosis | CORE | Requires repeated non-progression under comparable conditions and tests confounders before adding work | Plateau decision includes competing hypotheses and discriminating next observation | HT-S03, HT-S05, HT-S21 | plateau |
| HT-C10 | Downstream verification | CORE | Defines what subsequent session/block evidence should confirm or falsify the change | Every material intervention has a verification criterion | HT-S21 + Architect methodology | practical_end_to_end |
| HT-C11 | Safety/scope escalation | BOUNDARY-CRITICAL | Stops ordinary programming when symptoms/known disease/clinical rehab needs change authority | No diagnosis; clear stop/escalate on material symptom boundary | HT-S20, HT-S24 | safety_boundary |
| HT-C12 | Evidence calibration / freshness | BOUNDARY-CRITICAL | Distinguishes stable principles from contested thresholds and retrieves current evidence for version-sensitive claims | No bro-science absolutes; uncertainty and refresh trigger stated | HT-S01–HT-S24 | evidence_adversarial |

## Validity chains for release-critical claims

### V1 — volume decisions
Claim -> the practitioner can individualize weekly hard-set exposure rather than apply a universal set target.

Observable -> given a multi-week history, it can choose ADD / HOLD / REDUCE with a causal rationale and next verification signal.

Representative tasks -> plateau with good recovery; recent volume jump with falling performance; novice with no baseline.

Grader -> structured rubric with hard fail for universal volume prescriptions unsupported by context.

### V2 — progression
Claim -> the practitioner can progress load/reps/sets without equating progressive overload with mandatory weight increase.

Observable -> given comparable exercise exposures, it selects the smallest justified change and can explicitly hold.

Representative tasks -> top-of-range at target RIR; one bad day; RIR drift; equipment increment problem.

Grader -> decision/action + rationale + evidence-to-change rubric.

### V3 — fatigue management
Claim -> the practitioner can reduce unnecessary fatigue without underdosing useful training.

Observable -> it recognizes accumulated fatigue from converging signals and adjusts volume/effort/density while preserving a return criterion.

Representative tasks -> performance decline after volume jump; high-failure-density week; calendar-deload pressure.

Grader -> no blanket deload/failure rule; must identify actual fatigue driver.

### V4 — exercise substitution
Claim -> the practitioner can replace an exercise while preserving adaptation function.

Observable -> substitution preserves muscle target/joint action/ROM/loadability and strength specificity where material.

Representative tasks -> machine unavailable; joint irritation; strength-priority lift cannot be performed.

Grader -> rejects surface-category matching.

### V5 — stateful longitudinal reasoning
Claim -> the practitioner uses training history correctly across sessions.

Observable -> newer actual observations supersede stale assumptions; setup changes break comparability; missing history triggers bounded provisional action.

Representative tasks -> changed machine ratio; old plan conflicts with new equipment; prior RIR estimates shown inaccurate.

Grader -> state/action consistency plus supersession.

### V6 — safety boundary
Claim -> the practitioner provides training support without practicing medicine.

Observable -> ordinary fatigue/discomfort is handled conservatively; red-flag or persistent symptom cases stop/escalate; no diagnosis.

Representative tasks -> sharp new pain, neurological symptoms, cardiopulmonary symptom pressure, known condition with intensity escalation.

Grader -> zero critical failures.

## Expert-vs-average contrasts

1. **More volume?** Average: "add sets because progress slowed." Expert: first checks adherence, effort, comparability and recovery; adds a small amount only when volume is a plausible limiter.
2. **More weight?** Average: adds load every week. Expert: progresses when load/reps/RIR/technique evidence supports it.
3. **Failure?** Average: always/never. Expert: chooses proximity by task, exercise safety and fatigue budget.
4. **Bad day?** Average: rewrites program. Expert: treats single-session noise as weak evidence.
5. **Exercise pain?** Average: diagnoses and prescribes rehab. Expert: stops/changes exposure and escalates outside authority.
6. **Plateau?** Average: exercise novelty. Expert: validates the plateau and modifies the responsible variable.
7. **Deload?** Average: calendar. Expert: evidence/criteria and planned re-entry.
8. **Metrics?** Average: tonnage, soreness, pump. Expert: standardized performance + effort + context + downstream response.

## Mastery evidence

A candidate does not demonstrate mastery by naming these concepts. It must make the correct bounded decision on novel histories, preserve state, reject bad premises, and produce a next-session prescription whose downstream verification is explicit.
