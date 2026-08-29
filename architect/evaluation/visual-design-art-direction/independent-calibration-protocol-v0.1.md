# Visual Design / Art Direction 0.1.0 — independent calibration protocol

Cycle: `visual-design-art-direction-0.1.0-independent-2026-08-29-r1`
Candidate commit: `e8be839b02f181193afe076839c6ae94fb477a9b`
State: **PRE-SCORE; candidate outcomes forbidden until calibration freeze is complete.**

## Independence boundary

This evaluator cycle is authored after the candidate freeze. Public development fixtures may inform construct coverage only; their prompts, answer shapes and surface wording must not be reused as held-out cases. Hidden cases, expected professional dispositions, grader keys and raw traces remain sealed.

## Calibration corpus requirements

Before any candidate scoring, construct evaluator-owned calibration examples spanning at minimum:

- strong practitioner-quality work;
- competent but generic work;
- derivative/reference-copy work;
- over-designed/spectacle-first work;
- function-damaging novelty;
- mobile-as-collapsed-desktop failure;
- technically faithful implementation with poor rendered quality;
- strong craft with weak communication hierarchy;
- justified unusual/rule-breaking treatment as a negative control;
- justified and ornamental advanced-media routing as a paired control.

Calibration examples are not candidate held-out fixtures and do not count toward candidate coverage.

## Reference judgment structure

Reference judgments must be criterion-specific rather than one aesthetic scalar. For every calibration item, record:

- brief appropriateness;
- reference independence;
- concept distinctiveness;
- divergence quality when applicable;
- hierarchy/composition/typography/rhythm craft;
- communication/function preservation;
- truth/evidence integrity;
- mobile-specific art direction;
- implementation-contract usefulness;
- critique/root-cause quality;
- advanced-media routing judgment;
- authority-boundary discipline.

Mechanical P0 categories are graded deterministically and are never averaged into craft scores.

## Judge validation

A judge configuration is eligible only if it can discriminate the calibration ordering and does not systematically reward verbosity, generic polish, fashionable imitation, or spectacle over function. High-subjectivity dimensions require at least two independent judgments or a defensible practitioner reference adjudication. Material disagreement remains visible and is adjudicated by criterion; it is not erased through averaging.

The calibration pass/fail rule, judge identities/configurations, per-dimension release thresholds, repeat policy, adjudication policy, fixture corpus digest and resource/stop conditions must be frozen in a machine-readable record before the first scored candidate outcome is visible.

## Candidate scoring stop rules

- Calibration failure -> `NOT_EXECUTABLE` for this evaluator configuration; do not score the candidate.
- Deterministic/sealed/runtime-contract failure -> infrastructure classification, not professional failure.
- Any candidate P0 -> professional release failure without compensating aggregate score.
- Professional failure -> `REVISE`; do not patch the frozen candidate or rerun the same sealed pack seeking a better sample.
- Practical rendered gate missing -> no `PASS`, regardless of semantic score.

## Practical gate separation

Semantic calibration does not calibrate rendered-artifact judgment by itself. P1/P2/P3/P4 practical artifacts must be reviewed artifact-first at narrow and wide viewports, with blind comparison where feasible against a competent generic baseline and a strong mechanism benchmark. Render review must distinguish `CONCEPT | CONTRACT | IMPLEMENTATION | ASSET | UPSTREAM_CONSTRAINT`.
