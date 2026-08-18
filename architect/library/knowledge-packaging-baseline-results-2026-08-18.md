# Knowledge Packaging Targeted Baseline Results — 2026-08-18

Status: evidence record. Do not treat PM-04 aggregate FAIL as a proven knowledge-packaging defect until the grader is repaired for construct validity.

## Scope

Targeted baseline run: GitHub Actions run `32109315597` from draft PR #22.

The run intentionally tested only:

- Paid Media PM-04 experimentation/statistical judgment using the existing `paid-media-performance-marketing` Professional Core and Gemini 3.1 Flash Lite;
- Video Editing VE-11 deterministic artifact-first QC using injected media defects and ffmpeg/ffprobe.

No full release suite was required for these diagnostics.

## VE-11 — deterministic artifact QC

Result: **PASS 5/5**.

Observed cases:

1. valid control artifact passed decode, video/audio presence, no-long-black and no-long-silence checks;
2. injected long black interval was detected;
3. injected long silence interval was detected;
4. missing audio stream was detected;
5. truncated/corrupt media failed clean decode and was rejected.

Decision: the mechanical part of VE-11 is demonstrably `TOOL_BACKED`. Do not add prose/reference knowledge merely to explain checks that ffmpeg/ffprobe can observe deterministically. Preserve the professional-core rule that artifact observability is required, and make the runtime/tool contract responsible for mechanical verification. This PASS does not qualify perceptual/editorial QC.

## PM-04 — experimentation operational-depth baseline

Raw result: **2 PASS / 4 FAIL** across 6 hard cases. One Gemini call consumed 4,417 total tokens (3,426 input, 358 output, 633 thought tokens).

### Case-level observations

- `KP-PM04-01`: model identified insufficient power/precision and immature conversion lag, but omitted the separate `no_winner_claim` label. It did not emit a forbidden winner/proven claim.
- `KP-PM04-02`: model identified the unit-of-randomization mismatch and need for cluster-aware analysis, but omitted the redundant/derived `effective_sample_size_not_sessions` label. It did not treat 420,000 sessions as independent.
- `KP-PM04-03`: model identified interference risk and weakened causal identification, but omitted the prescriptive `redesign_or_specialist_review` label. It did not claim a clean causal estimate.
- `KP-PM04-04`: PASS; optional stopping, multiple-testing/selection risk, and need for an analysis plan were all identified.
- `KP-PM04-05`: PASS; practical significance, economic value, and rejection of p-value-only rollout were all identified.
- `KP-PM04-06`: model rejected fabricated precision and requested obtaining/bounding the baseline, but omitted the separate `baseline_required_for_sample_size` label. It did not invent an exact sample size.

## Construct-validity judgment

The current PM-04 gate is **not sufficient evidence that the Professional Core lacks operational statistical knowledge**.

Reason: four failures arise from all-required-label grading where the missing label is largely entailed by findings the model already emitted. The grader therefore confounds professional failure with ontology/label completeness. It also asks only for classification flags, so it does not directly test calculations, design construction, or interpretation of quantitative outputs—the operational depth the Knowledge Packaging audit intended to measure.

Decision: classify current PM-04 result as **EVAL_REVISE**, not `MODULE_REQUIRED`.

Do not weaken the gate merely to turn the current output into PASS. Instead redesign the task so the evidence target is the profession claim itself.

## Required PM-04 v2 design

The next gate should include independently observable tasks such as:

1. construct an experiment plan from incomplete business inputs and explicitly identify which missing values block numeric power/sample-size calculation;
2. compute or verify a two-proportion sample-size/MDE case with a deterministic calculator/grader and stated assumptions;
3. diagnose cluster-randomization analysis with effective independent units and reject pseudo-replication;
4. choose between fixed-horizon, sequential, or corrected multiple-testing approaches under a stated decision policy;
5. evaluate interference/contamination and decide whether the design can support the requested causal claim;
6. separate statistical from economic significance using supplied cost/margin data.

Grade observable decisions/calculations and forbidden claims, not exact wording or redundant taxonomy labels.

## Architecture decision

- VE-11 mechanical QC: `TOOL_BACKED` is supported by direct evidence. No new reference module justified for this slice.
- PM-04: current stable core already recognizes the tested conceptual failure modes. `PROCEDURAL_MODULE` / `REFERENCE_MODULE` / calculator helper remain plausible hypotheses, but **UNPROVEN** until PM-04 v2 demonstrates an actual execution or calculation failure.
- The Knowledge Packaging methodology behaved as intended: it prevented a formal FAIL from automatically causing prompt/module bloat and forced evaluation quality to be examined first.

## Red-team

Senior practitioner: would reject a test that rewards naming every taxonomy flag over making the correct decision. Repair by grading decisions and quantitative implications.

Educator/assessment specialist: would flag construct underrepresentation because a classification-only test does not demonstrate experiment design or statistical execution. Repair with authentic work samples and deterministic calculation checks.

Hiring manager: would care whether the agent can design, calculate, diagnose, and explain a real experiment under messy constraints, not whether it emits the repository's labels. Repair with realistic briefs, missing inputs, tool use, and decision outputs.
