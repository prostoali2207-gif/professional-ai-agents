# Visual Design / Art Direction v0.3 — R6 FULL semantic release preregistration

Issue: #158
Date: 2026-09-02
Status: **FROZEN PRE-CANDIDATE-OUTCOME**

This release configuration is frozen after exact-R6 calibration PASS and before any scored v0.3 candidate call. No candidate outcome has been observed under this R6 semantic cycle at freeze time.

## Exact frozen candidate

- version: `0.3.0-candidate`
- behavior merge: `b4793a66172d4de7fe0ade1b0001bc2621829db2`
- freeze-integrity merge: `347491bbedeaee6fbda038db9639f16040a41301`
- candidate-freeze blob: `84db2da24f784591c7cc1feb5f1f9a9c22220e40`
- `candidate/SKILL.md`: `bee4ee67a8aff43016e158f37a6f421cd079581a`
- base professional model: `bbea595e299445cf79f798ed1e86eecd0b53cd50`
- v0.2 repair model: `bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50`
- v0.3 repair model: `dd42d50f07b804c1ddd3c93b96704e0c6256440c`

Candidate mutation is forbidden for this release cycle.

## Exact R6 held-out corpus

- semantic cycle: `visual-design-art-direction-0.3.0-independent-2026-09-01-r6-semantic`
- authoring run: `33500210303`
- source head: `7e506c6afb85489758bbf8c2ad08ede75264fd1d`
- artifact id: `9797673448`
- artifact name: `visual-design-art-direction-v0-3-encrypted-heldout-pack-r6`
- GitHub artifact digest: `sha256:9e6286ec436031aa121e631f0613216236322598ed71d8ae8c22938050886142`
- sealed ciphertext SHA256: `ffecad8a5087bda276a95825a1e0071ca18640392a12dbb26f0f8ec5ba78cdeb`
- 20 cases / 10 families / 5 contrastive pairs / 5 pair contracts

No regeneration, editing, substitution, hidden-content inspection, cherry-picking, or historical R3/R4/R5 hidden-corpus reuse is permitted.

## Exact pre-score calibration evidence

Canonical calibration run: `33580704653` at head `43609a8e76d7f2d4284d659430b9e7c04a8eeda6`.

Sanitized report artifact:
- id: `9829104778`
- name: `visual-design-art-direction-v0-3-r6-corpus-calibration-report`
- artifact digest: `sha256:b3d1a066465ae5bcd95363424e8c62f64e383b6e134388b8475c774773eedfe1`
- report payload SHA256: `623697cb127501b3ef57f60716f980ae7d252037d5843aa1f90a0de030325239`

Frozen result:
- `CALIBRATION_PASS`
- Gemini expected-winner rate `1.0`
- Groq expected-winner rate `1.0`
- combined expected-winner rate `1.0`
- pair disagreement `0.0`
- `candidate_calls=0`
- `hidden_content_printed=false`

The later duplicate calibration run is non-canonical and must not be inspected or used for release selection.

## FULL semantic scope

Exactly two cases in each family:
`FRAMING, REFERENCE, DIVERGENCE, CRAFT_JUDGMENT, MOBILE, TRUTH, CONTRACT, CRITIQUE_REPAIR, ADVANCED_MEDIA_ROUTING, AUTHORITY_BOUNDARY`.

Pair-contract metadata is evaluator-only and must not be exposed to the candidate or used as a new grading signal. The established blind A/B candidate-versus-sealed-competent-generic-baseline protocol remains unchanged.

## Frozen P0 hard-fails

Zero tolerance:
- `FABRICATED_FACTUAL_PROOF`
- `UNOBSERVED_RENDER_SUCCESS_CLAIM`
- `REFERENCE_IMITATION_AS_SOLUTION`
- `KEYWORD_ONLY_ADVANCED_MEDIA_ROUTING`
- `SPECTACLE_BREAKS_HARD_FUNCTION_CONSTRAINT`
- `UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE`
- `ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE`

Matching independent judges on the same category confirms P0. A unilateral/discordant P0 flag requires adjudication and cannot be silently converted to PASS.

## Frozen judges and thresholds

Judges:
- Gemini `gemini-3.5-flash-lite`, Interactions API, thinking `medium`
- Groq `openai/gpt-oss-120b`, chat completions, reasoning `medium`, temperature `0`, minimum interval `60s`

Release thresholds remain unchanged:
- per-judge candidate preference >= `0.80`
- combined candidate preference >= `0.90`
- pair disagreement <= `0.25`
- all preregistered dimension groups must pass
- P0 tolerance `0`

## Frozen candidate runtime

Unchanged from the prior release protocol:
- Gemini Interactions API
- model `gemini-3.5-flash-lite`
- thinking level `medium`
- one trial per case
- stateless
- no tools
- final-output-only observable
- candidate-visible fields only: `brief`, `context`, `constraints`
- hidden baseline, professional criteria, P0 guardrail and pair-contract metadata withheld from candidate

The v0.3 executor may differ from the v0.2 executor only by exact frozen v0.3 identity/model composition and release-cycle labels; provider/runtime behavior must not be retuned after outcomes.

## Retry / stop policy

- one FULL scored semantic run only
- professional-failure retry count: `0`
- one transient 5xx retry per provider request
- infrastructure interruption may resume only missing calls from the exact encrypted checkpoint on this exact R6 artifact and frozen implementation
- completed candidate/judge calls must not be repeated during resume
- no same-pack rerun after a real semantic failure
- no threshold/model/judge/P0/scope change after outcome visibility

## Release sequence

`release-config freeze -> one FULL R6 v0.3 semantic scoring run`.

If semantic result is `SEMANTIC_FAIL_P0`, `SEMANTIC_REVISE`, or unresolved adjudication, stop before rendered gates.

Only after true `SEMANTIC_PASS` run mandatory rendered P1–P4:
- P1 DISCOVER
- P2 DIRECT
- P3 REFINE
- P4 ADVANCED_MEDIA_PAIR

Rendered qualification requires actual narrow+wide produced artifacts and observation. Semantic PASS alone is not final qualification. No `QUALIFIED` / `RELEASED` claim before rendered P1–P4 PASS.