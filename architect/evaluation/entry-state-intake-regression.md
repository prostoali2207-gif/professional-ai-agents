# Entry-state / intake regression — 2026-09-21

Status: targeted architecture regression.

## Incident

Observed failure: on a new muscle-gain coaching conversation, the response immediately proposed a baseline week and requested the last workout without first establishing the user's physical/training baseline.

User-corrected missing dimensions included body mass, height, age/adult status and prior training experience. The user also suggested "body type"; that label is not accepted automatically and must be translated into decision-relevant measurements/history if needed.

## Root cause classification

Primary: profession-model / workflow-entry failure.

Contributors:
- applied specialist selected from the middle of the lifecycle (progress analysis);
- no mandatory cold-start entry mode in Agent Architect;
- no owner for shared first-contact intake across training/nutrition/recovery/progress specialists;
- existing incomplete-information evals did not require a realistic first-turn trajectory.

## Required regression families

### R1 — cold start

Prompt: "I want to gain muscle and strength. Where do we start?"

No usable baseline is supplied.

PASS:
- does not prescribe the first training week or calorie target yet;
- recovers any reliable existing project context if available;
- asks one compact batch covering the decision-changing baseline for the next step;
- asks training history/consistency, goal priority, schedule/equipment and relevant safety constraints;
- for a holistic muscle-gain setup, captures age/adult status, height and current body mass because downstream nutrition/progress decisions need them;
- does not request somatotype/ectomorph-mesomorph-endomorph as a required biological variable.

FAIL:
- asks only for the last workout;
- starts a program then appends baseline questions;
- uses a body-type label as a primary programming variable;
- asks an exhaustive unrelated questionnaire.

### R2 — known-context contrast

The same prompt arrives with reliable current baseline/state already present.

PASS: does not repeat already-known baseline questions; asks only unresolved decision-changing facts.

### R3 — partial baseline

Height, body mass, age and training age are known; equipment and days available are missing.

PASS: asks for equipment/days (and any unresolved safety boundary) before a personalized microcycle.

### R4 — provisional

All material training inputs are known; exact body-fat percentage is unknown.

PASS: training design may proceed; unknown body-fat percentage is not treated as a blocker unless a specific downstream decision actually depends on it.

### R5 — weak proxy

User says "I'm an ectomorph, build the plan around that."

PASS: does not use somatotype as a validated prescription variable; uses observed training history, performance, body-mass trend, appetite/intake and constraints instead.

## Architecture expectation

Future applied-agent pre-SKILL gates must show that first-contact behavior is either:
- explicitly out of deployment scope, or
- modeled and evaluated through `initial-intake-and-decision-readiness.md`.

This regression is aimed at the architecture class, not only fitness wording.
