# Visual Design / Art Direction v0.2 — fresh R4 held-out preregistration

Issue: #158
Date: 2026-08-30
Status: preregistered before R4 implementation/provider calls

## Candidate binding

Candidate version: `0.2.0-candidate`
Candidate merge commit: `0116d20f99fde919fa6e39c700726d16310d010b`

Frozen candidate components:
- `candidate/SKILL.md` blob `b230a06aeca3cc67d0c275889a65b8b7403b59c0`
- inherited `professional-model-candidate-v0.1.md` blob `bbea595e299445cf79f798ed1e86eecd0b53cd50`
- `professional-model-p0-repair-v0.2.md` blob `bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50`

Any component change invalidates this cycle.

## Historical evidence boundary

R3 semantic run `33299663502` is historical failure evidence for v0.1 only. The R3 sealed corpus and hidden cases must not be reused, inspected, paraphrased, ranked, edited, or substituted into R4 release evidence.

R4 authoring may use only the already-public profession family definitions, FULL scope, preregistered P0 categories, and general evaluator contracts. It must generate fresh cases after v0.2 freeze.

## Scope unchanged

FULL scope remains:
`FRAMING, REFERENCE, DIVERGENCE, CRAFT_JUDGMENT, MOBILE, TRUTH, CONTRACT, CRITIQUE_REPAIR, ADVANCED_MEDIA_ROUTING, AUTHORITY_BOUNDARY`.

At least two fresh held-out cases per family. Contrastive pair families remain:
`REFERENCE, MOBILE, TRUTH, ADVANCED_MEDIA_ROUTING, AUTHORITY_BOUNDARY`.

Professional criteria, family semantics, P0 categories, release thresholds, judge policy, retry/resume/stop semantics and rendered P1-P4 requirements are unchanged from the prior frozen release protocol unless a deterministic infrastructure incompatibility makes execution impossible; any such infrastructure correction must be recorded before candidate scoring and must not change professional semantics.

## R4 authoring policy

Reuse the R3 **mechanism** only:
- Gemini native JSON-Schema constrained authoring;
- one family pair at a time;
- evaluator deterministically binds ids/family/pair_id;
- independent Groq construct audit;
- first construct-valid pair per family is accepted;
- maximum 3 author attempts per family;
- no ranking among passing alternatives;
- rejected outputs are not repaired, reused or substituted;
- no candidate calls during authoring;
- no hidden content printed publicly.

Outer envelope: <=30 Gemini author calls and <=30 Groq construct-audit calls.

If any family exhausts 3 attempts without an accepted pair, stop `NOT_EXECUTABLE — HELDOUT_AUTHORING_GATE_R4`. No fourth attempt in R4.

Provider/transport/quota failures are evaluator infrastructure failures, not professional failures, and may only follow the existing bounded retry/resume methodology without changing semantic requirements.

## Sealing

Successful authoring must produce a new encrypted R4 artifact with a new cycle id, ciphertext identity and manifest bound to the exact v0.2 candidate components above.

A successful R4 seal is not professional PASS.

## Pre-score calibration

Before any v0.2 candidate scoring:
1. exact R4 sealed artifact identity must be frozen;
2. blind corpus-specific pre-score calibration must run on that exact R4 corpus using the already-calibrated release judges;
3. candidate execution must be absent from calibration;
4. thresholds remain per-judge >=0.80, combined >=0.90, pair disagreement <=0.25;
5. candidate scoring remains forbidden until true `CALIBRATION_PASS` on exact R4.

A completed `CALIBRATION_FAIL` is not rerun to seek a better outcome.

## Release sequence after CALIBRATION_PASS

Freeze exact release configuration before any candidate outcome, then run FULL semantic qualification of the exact v0.2 candidate.

Any confirmed P0 => semantic release failure.

Only after semantic PASS run mandatory rendered P1-P4:
- P1 DISCOVER
- P2 DIRECT
- P3 REFINE
- P4 advanced-media contrast pair.

No final QUALIFIED claim without rendered P1-P4 PASS.