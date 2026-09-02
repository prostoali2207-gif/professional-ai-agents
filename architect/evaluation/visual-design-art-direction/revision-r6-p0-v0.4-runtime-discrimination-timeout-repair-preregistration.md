# Visual Design / Art Direction v0.4 — read-timeout transport repair preregistration

Date: 2026-09-02
Issue: #158
Status: preregistered before timeout-repair implementation/provider calls

## Incident binding

Canonical continuation run: `33603188376`.

The continuation loaded and verified the immutable four-fixture checkpoint successfully, then failed on the first unfinished candidate call before any new model output or judgment was produced.

Sanitized continuation progress artifact:
- artifact id: `9836056465`;
- artifact name: `visual-design-art-direction-v04-runtime-probe-resume-progress`;
- artifact digest: `sha256:d00dd3052d91a2f26334843b025e73024bad3cd156a7fa22b8b2d4b5228b0968`.

Observed sanitized state:
- status: `INFRASTRUCTURE_FAILURE`;
- checkpoint candidate calls: `4`;
- checkpoint judge calls: Gemini `4`, Groq `4`;
- continuation candidate calls with completed output: `0`;
- continuation judge calls with completed judgment: Gemini `0`, Groq `0`;
- failure class: candidate executor transport read timeout (`The read operation timed out`).

This is infrastructure/transport failure, not a professional outcome.

## Immutable professional state

No professional or evaluation semantics may change:
- completed R30/R31/R32/R33 checkpoint outcomes remain immutable and MUST NOT be regenerated or rejudged;
- only unfinished public development fixtures R34 and R39 may execute;
- frozen candidate components, Gemini 3.7 Flash runtime, medium thinking, both judge models, public fixtures, criteria, PASS rule and development-only boundary remain unchanged from the prior preregistration;
- hidden R6 material remains sealed and inaccessible.

## Timeout-only repair policy

The transport wrapper may recognize a read/operation timeout only when the provider/executor returned no usable model output or judgment.

For such a timeout:
- one bounded retry of that exact unfinished transport call is permitted;
- no completed model output or judgment may be replaced;
- retry must preserve the exact prompt, fixture, model identity, thinking level and judge configuration;
- no stochastic professional retry is permitted after a usable output/judgment exists;
- HTTP 429 handling remains exactly as preregistered previously.

No other error class is newly retryable under this repair.

## Gate

The combined six-fixture development gate remains unchanged: PASS only if immutable R30–R33 plus newly completed R34/R39 all PASS under both judges with no forbidden behavior.

If this exact continuation again fails only for infrastructure before usable output/judgment, preserve every completed outcome and stop for another evidence-backed transport decision. If R34 or R39 completes and fails professionally, do not retry that professional outcome.

This remains DEVELOPMENT ONLY and is not release evidence. Current release verdict remains `NOT_QUALIFIED`.
