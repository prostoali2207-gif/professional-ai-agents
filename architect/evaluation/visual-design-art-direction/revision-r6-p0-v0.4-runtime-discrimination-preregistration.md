# Visual Design / Art Direction v0.4 — R6 P0 runtime-discrimination preregistration

Date: 2026-09-02
Issue: #158
Status: preregistered before probe implementation/provider calls

## Terminal evidence boundary

The exact frozen v0.3 R6 scored run `33585269478` is terminal `SEMANTIC_FAIL_P0`.

Sanitized report artifact:
- artifact id: `9830265349`;
- artifact name: `visual-design-art-direction-v0-3-r6-semantic-report`;
- artifact digest: `sha256:af856e963c929809b9cd272a80af062f74b7c2f9ee7614e2f1f52e6d8a4432eb`.

Only sanitized release evidence may be used for repair. Hidden R6 prompts, criteria, case metadata beyond the sanitized report, candidate responses, checkpoint contents, and evaluator keys are not eligible for inspection or reconstruction.

Sanitized R6 evidence:
- candidate calls: 20/20;
- Gemini candidate preference: 1.0;
- Groq candidate preference: 1.0;
- combined candidate preference: 1.0;
- pair disagreement: 0.0;
- all ordinary dimension groups passed;
- confirmed P0 count: 3;
- confirmed P0 classes:
  - `ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE`;
  - `REFERENCE_IMITATION_AS_SOLUTION`;
  - `UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE`;
- adjudication-required count: 2:
  - `ADVANCED_MEDIA_ROUTING`: 1;
  - `TRUTH`: 1;
- hidden content printed: false.

R6 is historical professional/runtime failure evidence only. It must not be rerun, resumed for a professional outcome, copied, edited, regenerated from, or used as the next held-out pack.

## Root-cause discrimination

The v0.3 candidate already contains explicit release-critical controls for MOBILE, REFERENCE, AUTHORITY, TRUTH and final-output consistency. Those controls appear in both the v0.3 professional-model repair and the candidate SKILL, and the R6 executor explicitly instructs the runtime to apply them.

Therefore the next repair must not assume that adding more verbal prohibitions is the correct layer.

Current hypotheses:

### H1 — missing professional rule text

Weakly supported. The three confirmed R6 P0 classes are already explicitly represented as vetoes and pre-commit/final-output controls in v0.3.

A prompt-only expansion is not the default repair.

### H2 — runtime decision-consistency/capacity

Plausible and cheapest to discriminate first. Frozen v0.3 executed on `gemini-3.5-flash-lite`, while current Google Gemini documentation describes Flash-Lite as the high-throughput/cost-efficient tier and newer Flash models as stronger for agentic/multi-step execution and web-development work.

Live official references checked before this preregistration:
- https://ai.google.dev/gemini-api/docs/models
- https://ai.google.dev/gemini-api/docs/latest-model
- https://ai.google.dev/gemini-api/docs/deprecations

The first discriminating change is therefore runtime model only:
- from `gemini-3.5-flash-lite`;
- to `gemini-3.7-flash`;
- keep Interactions API;
- keep thinking level `medium` to avoid confounding model change with effort change;
- keep the exact v0.3 professional components unchanged.

### H3 — structural execution controller required

Reserved fallback. If a stronger runtime still violates a public release-critical regression, the next mechanism to test is explicit staged control (`proposal -> structured invariant decision -> allowed-output gate -> finalization`) rather than more prose.

Do not add a critic/multi-agent boundary unless a simpler runtime/control mechanism cannot meet the requirement; extra model calls are not automatically independent verification.

## Opportunity-search decision

Mechanisms considered before convergence:

1. add more SKILL/professional-model warnings — `REJECT FOR FIRST TEST`; repeated failure despite explicit rules gives low expected information gain;
2. stronger eligible runtime with unchanged professional core — `TEST FIRST`; smallest mechanism change and directly supported by current provider capability evidence;
3. deterministic semantic P0 validator — `NOT SUFFICIENT ALONE`; the exposed P0 classes require contextual semantic judgment, so keyword/static checks cannot prove compliance;
4. staged structured controller — `RESERVE`; higher complexity/call cost but materially different failure-control mechanism;
5. independent runtime critic — `RESERVE`; additional latency/cost and judge-independence complications.

## Public development probe

Use only existing public development fixtures from `fixtures-v0.3-targeted-regression.json`:

- `R30_MOBILE_PRECOMMIT_CONTROL` — confirmed R6 P0 class;
- `R31_TRUTH_PROOF_OUTPUT_CONTROL` — R6 TRUTH adjudication family/non-regression;
- `R32_REFERENCE_INDEPENDENCE_CONTROL` — confirmed R6 P0 class;
- `R33_AUTHORITY_PRECOMMIT_CONTROL` — confirmed R6 P0 class;
- `R34_WARNING_ONLY_COMPLIANCE_TRAP` — combined release-critical conflict pressure;
- `R39_BOLD_REFERENCE_ADVANCED_MEDIA_NONREGRESSION` — advanced-media/reference non-regression and R6 adjudication-family coverage.

These are DEVELOPMENT ONLY and may be public. They cannot become held-out release evidence.

Candidate-under-probe:
- exact frozen v0.3 SKILL blob: `bee4ee67a8aff43016e158f37a6f421cd079581a`;
- base professional model blob: `bbea595e299445cf79f798ed1e86eecd0b53cd50`;
- v0.2 repair blob: `bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50`;
- v0.3 repair blob: `dd42d50f07b804c1ddd3c93b96704e0c6256440c`;
- runtime only: Gemini Interactions `gemini-3.7-flash`, thinking `medium`.

Development judges:
- Gemini `gemini-3.5-flash-lite`;
- Groq `openai/gpt-oss-120b`, temperature 0 / medium reasoning where supported, minimum interval 60 seconds.

Each judge receives the public fixture prompt, public `must_observe`, public `must_not_observe`, and candidate output. It must return a schema-enforced/public-safe verdict.

Probe PASS condition:
- all 6 fixtures completed;
- both judges PASS every fixture;
- no `must_not_observe` violation identified by either judge;
- no infrastructure failure;
- no hidden R6 material accessed.

This is a deliberately strict development discrimination gate, not a release threshold.

## Resource gate

Maximum planned provider calls:
- candidate: 6;
- Gemini judge: 6;
- Groq judge: 6;
- total: 18.

No stochastic reruns for a better development outcome. One bounded transient 5xx retry is allowed per transport call. Groq pacing remains at least 60 seconds.

If the probe fails for infrastructure, preserve the partial public results and repair transport only. If it fails professionally on any release-critical fixture, do not repeat the same probe seeking a better sample.

## Promotion / stop rule

If all six public fixtures PASS on both judges:
- classify the evidence as support for a **runtime-only v0.4 candidate delta**;
- do not change v0.3 professional rules merely to restate existing controls;
- create a new candidate freeze binding the unchanged professional components plus the new runtime contract;
- require fresh independent held-out release qualification after that freeze;
- preserve FULL scope, P0 semantics, rendered P1–P4 requirement and independence requirements unless a separate evidence-backed methodology revision exists.

If any confirmed-P0 public fixture fails:
- do not freeze the runtime-only v0.4 candidate;
- move to H3 structural execution-controller discrimination using public development fixtures;
- keep hidden R6 sealed.

Current verdict remains `NOT_QUALIFIED`.
