# Visual Design / Art Direction v0.3 — exact R6 corpus pre-score calibration preregistration

Issue: #158
Date: 2026-09-01
Status: **PRE-SCORE / preregistered before R6 calibration implementation or provider calls**

## Exact source binding

Fresh R6 held-out authoring run: `33500210303`
Source head: `7e506c6afb85489758bbf8c2ad08ede75264fd1d`
Artifact id: `9797673448`
Artifact name: `visual-design-art-direction-v0-3-encrypted-heldout-pack-r6`
GitHub artifact digest: `sha256:9e6286ec436031aa121e631f0613216236322598ed71d8ae8c22938050886142`
Sealed ciphertext SHA256: `ffecad8a5087bda276a95825a1e0071ca18640392a12dbb26f0f8ec5ba78cdeb`
Semantic cycle: `visual-design-art-direction-0.3.0-independent-2026-09-01-r6-semantic`

The exact R6 artifact above is the only eligible corpus for this pre-score calibration. No regeneration, editing, substitution, cherry-picking, hidden-content inspection, or reuse of R3/R4/R5 hidden material is permitted.

Public authoring evidence is limited to the already-emitted aggregate/identity record: 20 cases, 10 families, 5 contrastive pairs, 5 pair contracts, `author_calls=10`, `audit_calls=10`, all family attempts `1`, zero structural/audit rejections, `candidate_calls=0`, `hidden_content_printed=false`, and no historical R3/R4/R5 reuse.

## Frozen candidate binding

Candidate version: `0.3.0-candidate`
Behavior merge: `b4793a66172d4de7fe0ade1b0001bc2621829db2`
Freeze-integrity merge: `347491bbedeaee6fbda038db9639f16040a41301`
Candidate freeze blob: `84db2da24f784591c7cc1feb5f1f9a9c22220e40`
Frozen components:
- `candidate/SKILL.md`: `bee4ee67a8aff43016e158f37a6f421cd079581a`
- base professional model: `bbea595e299445cf79f798ed1e86eecd0b53cd50`
- v0.2 repair model: `bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50`
- v0.3 repair model: `dd42d50f07b804c1ddd3c93b96704e0c6256440c`

R6 calibration is evaluator-only. Candidate execution is forbidden. `candidate_calls` must remain `0`. Any professional candidate mutation invalidates this preregistration and requires a new evidence-governed revision cycle.

## Frozen release judges and policy

Reuse the already-established release calibration configuration unchanged:
- Gemini judge/anchor model: `gemini-3.5-flash-lite`
- Groq judge/anchor-audit model: `openai/gpt-oss-120b`
- blind A/B comparison
- Groq minimum pacing interval: `60` seconds
- one transient 5xx retry per provider request

Thresholds remain exactly:
- each judge expected-winner rate >= `0.80`
- combined expected-winner rate >= `0.90`
- pair disagreement <= `0.25`

No threshold, judge, provider model, reasoning policy, hidden construct, P0 semantics, FULL scope, or stop-rule change is allowed after outcomes are visible.

## Exact-corpus calibration procedure

Use the previously validated exact-corpus calibration mechanism, adapted only for R6 transport/schema bindings.

For each exact sealed R6 case:
1. use the sealed candidate-visible facts plus hidden professional criteria/P0 guardrail to generate one ephemeral senior-practitioner anchor with frozen Gemini;
2. independently audit anchor validity with frozen Groq against the hidden professional criteria/P0;
3. if any anchor is rejected, stop `CALIBRATION_NOT_EXECUTABLE_ANCHOR_VALIDITY`; do not regenerate or repair that anchor seeking a pass;
4. compare the accepted practitioner anchor blind A/B against the already-sealed competent-generic baseline;
5. derive A/B side deterministically from calibration cycle + case id;
6. Gemini and Groq independently choose the stronger response;
7. expected winner is the independently accepted practitioner anchor;
8. compute the frozen calibration metrics over all 20 cases.

Judges in A/B receive only candidate-visible facts and the two outputs. Hidden professional criteria/P0 are used only for independent anchor-validity audit. Evaluator-only `pair_contract` metadata must not be exposed to candidate-visible A/B judging and must not alter the established release thresholds.

## R6 structure/integrity requirements

Before calibration calls, deterministic/sealed verification must establish:
- cycle, candidate commit, freeze-integrity commit, freeze blob, and all four candidate component blobs match this preregistration;
- `item_count=20`, `family_count=10`, `pair_count=5`, `pair_contract_count=5`;
- pair-contract schema version remains `0.1`;
- `candidate_calls=0`, `hidden_content_printed=false`;
- `historical_r3_reused=false`, `historical_r4_reused=false`, `historical_r5_reused=false`;
- source artifact id/name/digest/run/head and sealed ciphertext SHA256 match exactly.

No hidden case text may be printed to logs or published artifacts. Sanitized progress/report and encrypted checkpoint only.

## Integrity and failure handling

- completed `CALIBRATION_FAIL` is terminal under this exact configuration; do not rerun seeking stochastic improvement;
- `CALIBRATION_NOT_EXECUTABLE_ANCHOR_VALIDITY` blocks candidate scoring and is evaluator/construct non-executability, not professional failure;
- provider/transport interruption is infrastructure failure, not professional failure;
- resume is allowed only from the exact encrypted checkpoint produced for this exact R6 artifact, and completed provider/case work must not be repeated;
- no candidate call is allowed during calibration;
- hidden R6 cases, criteria, P0 triggers, baselines, pair contracts, and anchors must never be printed publicly.

## Resource / cost gate

Calibration implementation and all zero-provider checks must land and pass before any calibration provider call. The paid calibration workflow must remain explicit issue-command opt-in only and must not run on push or pull request.

Use the smallest valid next execution: one exact-corpus calibration cycle, bounded by the frozen procedure above. Do not run semantic candidate scoring to diagnose calibration infrastructure.

## Release sequence

Candidate scoring remains forbidden until true `CALIBRATION_PASS` on this exact R6 artifact.

After `CALIBRATION_PASS`:
1. freeze the exact v0.3 semantic release configuration before any candidate outcome;
2. run one FULL semantic qualification of the exact frozen v0.3 candidate against this exact R6 corpus;
3. any confirmed P0 is semantic release failure;
4. only after semantic PASS run mandatory rendered P1–P4;
5. no final `QUALIFIED` claim without rendered P1–P4 PASS.
