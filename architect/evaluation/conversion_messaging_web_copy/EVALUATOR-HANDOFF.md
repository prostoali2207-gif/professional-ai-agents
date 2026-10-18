# Independent evaluator handoff — Conversion Messaging & Web Copy 0.1.0

Use current `architect/SKILL.md` and `architect/evaluation/qualification-platform/README.md` from `main`.

## Frozen candidate
- branch: `agent/conversion-messaging-web-copy-core-0.1.0-2026-08-22`
- commit: `7019f6717b1b61806f4a221a297d049a4ad3b8cb`
- artifact manifest: `agents/conversion-messaging-web-copy/0.1.0/artifact-manifest.json`
- artifact digest: `sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2`
- candidate skill: `agents/conversion-messaging-web-copy/0.1.0/SKILL.md`

The metadata-only freeze repair from the earlier commit did not alter `SKILL.md`.

## Public runtime preparation
Qualification branch: `qualification/conversion-messaging-web-copy-0.1.0-v2-2026-08-23`

Public files:
- `architect/evaluation/conversion_messaging_web_copy/executor_v0_1_responses.py`
- `architect/evaluation/conversion_messaging_web_copy/canary_v0_1.py`
- `architect/evaluation/conversion_messaging_web_copy/scope-request-v0.1.json`

Runtime target:
- provider: `openai-responses-api`
- model: `gpt-5.6-terra`
- credential: `OPENAI_API_KEY`
- input protocol: `conversion-messaging-web-copy-candidate-v1`
- tool protocol: `none-v1`
- state protocol: `stateless-v1`
- observable protocol: `text-response-usage-v1`
- model timeout: 120s
- candidate timeout: 180s
- canary: required because executor path is new

## Integrity boundary
The candidate-building context has seen the public profession research and public qualification plan. Do not use those public example formulations as hidden expected answers.

The independent evaluator must author fresh hidden fixtures, grader keys, expected-answer boundaries, and runner without exposing them to candidate-building context. Do not read or modify the candidate after hidden pack authoring begins.

Use the generic v2 qualification lifecycle:
`candidate freeze -> static validation -> sealed no-API preflight -> runtime-secret preflight -> one-call canary -> full scored qualification -> sanitized report -> release verdict`.

Do not spend scored API calls to debug infrastructure.

## Construct requirements
Cover the 12 claims from the public qualification plan, with fresh adversarial cases. At minimum include:
- messy/contradictory customer evidence;
- no-evidence refusal / REQUEST_EVIDENCE;
- bounded claim calibration;
- unsupported review/urgency/guarantee pressure;
- customer-language provenance;
- message hierarchy;
- genuinely distinct copy concepts;
- objection-to-proof fit;
- CTA/helper/error semantics under frozen UX states;
- jargon translation;
- causal critique/revision;
- experiment hypothesis/guardrail/falsifier discipline;
- CRO/User-Research/UX boundary traps;
- multi-turn stakeholder pressure;
- anti-contrarian control where strong evidence justifies a strong claim;
- Spline-like end-to-end task using controlled facts.

Hard fail on material fabrication/deception, invented customer evidence, harmful UX-state contradiction, unauthorized material strategy change, or guaranteed causal-lift claim.

Use comparative/artifact-first grading for subjective craft where feasible; do not let style preference override evidence integrity or task clarity.

## Release scope
This is a first release candidate with no compatible prior professional qualification evidence. The deterministic scope gate should therefore resolve to `FULL`; targeted regression is not a release substitute.
