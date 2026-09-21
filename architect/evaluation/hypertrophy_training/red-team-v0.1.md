# Hypertrophy Training v0.1 — professional red-team

Status: PRE-SKILL RED-TEAM COMPLETE
Date: 2026-09-21

Mandatory question:

> What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?

## Senior practitioner critique

### Finding 1 — "minimum unnecessary fatigue" can accidentally become undertraining

Risk: optimizing fatigue downward without preserving sufficient effort/volume.

Repair: professional model makes stimulus sufficiency primary and treats fatigue reduction as removal of non-useful cost, not minimization of all fatigue. Development cases require continued useful work rather than blanket deload.

Status: REPAIRED.

### Finding 2 — population set targets could be mistaken for individual prescription

Risk: ACSM/meta-analysis thresholds become "10+ sets for everyone".

Repair: source/reference files explicitly treat aggregate volume findings as priors, anchor decisions to prior tolerated dose, and add a universal-set-target hard fail.

Status: REPAIRED.

### Finding 3 — RIR can create false numerical precision

Risk: agent treats reported RIR as objective truth.

Repair: RIR confidence and calibration procedure added; raw rep drop inconsistency is an eval family.

Status: REPAIRED.

### Finding 4 — changing ROM/equipment can fake regression/progression

Risk: raw load comparison across machine ratios or technique standards.

Repair: exercise_version + ROM/technique comparability added to state; changed-machine and changed-ROM cases are hard-fail sensitive.

Status: REPAIRED.

### Finding 5 — "plateau" needs a minimum evidence concept without an arbitrary week count

Risk: either overreact to short noise or require a universal N-week plateau.

Repair: plateau defined as repeated comparable non-progression beyond expected noise; no universal duration. Diagnostic sequence precedes dose change.

Status: REPAIRED.

### Finding 6 — exercise substitution needs function, not anatomy label only

Risk: "another chest/leg exercise" substitutions destroy specificity or target function.

Repair: substitution contract includes adaptation target, strength specificity, joint action/ROM, stability, loadability, fatigue and tolerance.

Status: REPAIRED.

## Educator / competency-assessor critique

### Finding 7 — evals could reward vocabulary

Risk: candidate mentions volume/RIR/fatigue without making a correct prescription.

Repair: evaluation contract requires a primary action, concrete next prescription, basis, verification and boundary; practical cases grade end-to-end next microcycle.

Status: REPAIRED.

### Finding 8 — no-change decisions need explicit assessment

Risk: agent demonstrates activity bias.

Repair: HOLD is a first-class action; multiple contrastive cases require it.

Status: REPAIRED.

## Hiring-manager critique

### Finding 9 — can this practitioner actually manage mixed strength/hypertrophy priorities?

Risk: generic bodybuilding plan ignores exercise-specific strength.

Repair: mixed-goal procedure and practical case explicitly require priority-lift heavy practice early plus separate hypertrophy progression.

Status: REPAIRED.

### Finding 10 — does it know when it is not the right professional?

Risk: pain/medical questions trigger amateur diagnosis.

Repair: safety boundary, ACSM screening evidence and zero-hard-fail clinical cases included.

Status: REPAIRED.

## Evaluation-scientist critique

### Finding 11 — author-visible cases cannot qualify the skill

Risk: development suite is mistaken for independent evidence.

Repair: evaluation plan explicitly limits visible fixtures to development and preregisters fresh 24-case held-out qualification with frozen grader/thresholds.

Status: REPAIRED ARCHITECTURALLY; independent run remains future release evidence.

### Finding 12 — single stochastic PASS is weak for critical decisions

Repair: progression/fatigue/safety/state critical families require 3/3 trials if stochastic behavior is observed.

Status: REPAIRED.

## Systems/state reviewer critique

### Finding 13 — plan vs actual performance can be conflated

Repair: schema keeps current_plan separate from sessions; decision log records hypothesis/verification.

Status: REPAIRED.

### Finding 14 — health detail retention can expand privacy scope

Repair: state schema stores only a minimum symptom-boundary flag/note needed for training authority; diagnosis is neither inferred nor required.

Status: REPAIRED.

## Security reviewer critique

### Finding 15 — training logs may contain instruction-like text

Repair: adversarial data-instruction fixture requires log notes to remain untrusted data and forbids health-state mutation from embedded instructions.

Status: REPAIRED.

## Remaining red-team limitation

No independent strong strength/hypertrophy practitioner has reviewed the artifact yet. Therefore this red-team does not support T2 expert validation.

## Decision

No material pre-SKILL architecture gap remains unaddressed in the current model, packaging, state and evaluation design. Independent semantic/practical qualification is still required after candidate assembly for T1.
