# Visual Design / Art Direction v0.2 — exact R4 corpus pre-score calibration preregistration

Issue: #158
Date: 2026-08-30
Status: preregistered before R4 calibration implementation/provider calls

## Exact source binding

Fresh R4 held-out authoring run: `33306265227`
Source head: `147f1581c1ff24c51b71169aaad7770d6d27f3ce`
Artifact id: `9730714845`
Artifact name: `visual-design-art-direction-v0-2-encrypted-heldout-pack-r4`
GitHub artifact digest: `sha256:fbe4b03ffc1eede30b3e36dcaa13e7bf96e29c28cf40d722ae2e376355f0e73e`
Sealed ciphertext SHA256: `b6147b01b838aa447fcaff711668771d6347a329f97ac21c7c97f9c9d6e85bf6`
Semantic cycle: `visual-design-art-direction-0.2.0-independent-2026-08-30-r4-semantic`

The exact R4 artifact above is the only eligible corpus for this pre-score calibration. No regeneration, editing, substitution, cherry-picking, or hidden-content inspection is permitted.

## Candidate binding

Candidate version: `0.2.0-candidate`
Candidate merge commit: `0116d20f99fde919fa6e39c700726d16310d010b`
Frozen components:
- `candidate/SKILL.md` blob `b230a06aeca3cc67d0c275889a65b8b7403b59c0`
- inherited `professional-model-candidate-v0.1.md` blob `bbea595e299445cf79f798ed1e86eecd0b53cd50`
- `professional-model-p0-repair-v0.2.md` blob `bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50`

Candidate execution is forbidden during calibration. `candidate_calls` must remain `0`.

## Frozen judges and policy

Reuse the already calibrated release judges and the exact same calibration policy:
- Gemini: `gemini-3.5-flash-lite`
- Groq: `openai/gpt-oss-120b`
- blind A/B comparison
- Groq minimum pacing interval: 60 seconds
- one transient 5xx retry per provider request

Thresholds remain:
- each judge expected-winner rate >= `0.80`
- combined expected-winner rate >= `0.90`
- pair disagreement <= `0.25`

No threshold, judge, model, reasoning policy, or stop-rule change is allowed after outcomes are visible.

## Corpus-specific calibration procedure

For each exact sealed R4 case:
1. use the sealed brief/context/constraints/professional criteria/P0 guardrail to generate one ephemeral senior-practitioner anchor with the frozen Gemini model;
2. independently audit anchor validity with frozen Groq against hidden professional criteria/P0;
3. if any anchor is rejected, stop `CALIBRATION_NOT_EXECUTABLE_ANCHOR_VALIDITY`; do not regenerate/repair that anchor seeking a pass;
4. compare the accepted practitioner anchor blind A/B against the already-sealed competent-generic baseline;
5. deterministic A/B side is derived from calibration cycle + case id;
6. Gemini and Groq independently choose the stronger response;
7. expected winner is the independently accepted practitioner anchor;
8. compute the frozen calibration metrics over all 20 cases.

Judges in the A/B step receive only candidate-visible facts and the two outputs. Hidden professional criteria/P0 are used only for independent anchor validity audit.

## Integrity and failure handling

- hidden R4 cases, criteria, P0 triggers, baselines and anchors must never be printed publicly;
- completed `CALIBRATION_FAIL` is terminal under this configuration; do not rerun seeking stochastic improvement;
- `CALIBRATION_NOT_EXECUTABLE_ANCHOR_VALIDITY` blocks candidate scoring and is evaluator/construct non-executability, not professional failure;
- infrastructure interruption may resume only from the exact encrypted checkpoint for this exact R4 artifact;
- completed provider/case work must not be repeated on resume;
- infrastructure failure is not a professional failure.

## Release sequence

Candidate scoring remains forbidden until true `CALIBRATION_PASS` on this exact R4 artifact.

After `CALIBRATION_PASS`:
1. freeze exact release configuration before any candidate outcome;
2. run FULL semantic qualification of the exact frozen v0.2 candidate;
3. any confirmed P0 is semantic release failure;
4. only after semantic PASS run mandatory rendered P1–P4;
5. no final `QUALIFIED` claim without rendered P1–P4 PASS.
