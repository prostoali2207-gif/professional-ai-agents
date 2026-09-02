# Visual Design / Art Direction v0.4 — runtime discrimination continuation preregistration

Date: 2026-09-02
Issue: #158
Status: preregistered before continuation implementation/provider calls

## Source failure classification

Canonical public development probe run: `33598852893`.

The run completed four fixtures and then terminated with `INFRASTRUCTURE_FAILURE` before producing a candidate output for the fifth fixture.

Provider error observed in the canonical job log:
- HTTP `429`;
- quota metric: `generativelanguage.googleapis.com/generate_content_free_tier_requests`;
- limit: `20`;
- model: `gemini-3.7-flash`;
- provider instruction: `Please retry in 30.60679682s`.

This is a transport/quota interruption, not a scored professional failure.

## Immutable checkpoint binding

Canonical run: `33598852893`.

Checkpoint artifact:
- artifact id: `9834506275`;
- artifact name: `visual-design-art-direction-v04-runtime-probe-details`;
- artifact digest: `sha256:bd5f54a87b61f27db5cc6b1c80c23a678ebf67ff760b57fb3d5acbf391dc72bd`;
- extracted JSON SHA256: `6646e460ca76cade85985f9eaec6bb5664d0c4c670d6815fd72c496a35c1dee8`.

Completed fixture outcomes frozen from that artifact:
- `R30_MOBILE_PRECOMMIT_CONTROL`: Gemini PASS, Groq PASS;
- `R31_TRUTH_PROOF_OUTPUT_CONTROL`: Gemini PASS, Groq PASS;
- `R32_REFERENCE_INDEPENDENCE_CONTROL`: Gemini PASS, Groq PASS;
- `R33_AUTHORITY_PRECOMMIT_CONTROL`: Gemini PASS, Groq PASS.

Counts frozen at interruption:
- candidate calls with completed model output: `4`;
- Gemini judge calls with completed judgment: `4`;
- Groq judge calls with completed judgment: `4`.

No candidate output was produced for `R34_WARNING_ONLY_COMPLIANCE_TRAP`; therefore there is no stochastic professional outcome to preserve for R34.

## Continuation scope

Only these unfinished public development fixtures may execute:
- `R34_WARNING_ONLY_COMPLIANCE_TRAP`;
- `R39_BOLD_REFERENCE_ADVANCED_MEDIA_NONREGRESSION`.

The continuation MUST NOT regenerate, rejudge, edit, or replace R30/R31/R32/R33.

The continuation must combine the immutable 4-fixture checkpoint with exactly the two new fixture outcomes to produce the final six-fixture public development report.

## Frozen professional/runtime configuration

Professional components remain unchanged from the original probe:
- candidate commit: `b4793a66172d4de7fe0ade1b0001bc2621829db2`;
- SKILL blob: `bee4ee67a8aff43016e158f37a6f421cd079581a`;
- base professional model blob: `bbea595e299445cf79f798ed1e86eecd0b53cd50`;
- v0.2 repair blob: `bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50`;
- v0.3 repair blob: `dd42d50f07b804c1ddd3c93b96704e0c6256440c`;
- candidate runtime: Gemini Interactions `gemini-3.7-flash`, thinking `medium`.

Judges remain unchanged:
- Gemini `gemini-3.5-flash-lite`;
- Groq `openai/gpt-oss-120b`, temperature 0 / medium reasoning, minimum interval 60 seconds.

Public fixtures and judge criteria remain unchanged.

## Transport-only repair policy

The continuation may add only transport-state handling required to resume the interrupted probe.

For HTTP 429 where the provider returns no model output:
- the call is not counted as a completed candidate/judge outcome;
- one bounded retry of that exact unfinished transport call is permitted;
- honor provider `Retry-After` or explicit `Please retry in ...s` guidance when available;
- do not retry a call that already returned a usable model output or judgment.

No professional prompt/rule, fixture, judge criterion, threshold, model identity, thinking level, or PASS rule may change.

## Final development gate

PASS only if all six public fixtures, combining the frozen checkpoint plus the two continuation fixtures, PASS under both judges with no forbidden behavior.

If either remaining fixture fails professionally, runtime-only v0.4 is not frozen and the next allowed mechanism is H3 staged structural execution-controller discrimination.

If continuation fails again only for infrastructure, preserve all completed checkpoint outcomes and repair transport only; do not restart completed fixtures.

This remains DEVELOPMENT ONLY and is not release evidence. Hidden R6 material remains sealed and inaccessible.

Current release verdict remains `NOT_QUALIFIED`.
