# Visual Design / Art Direction v0.3 — fresh R5 held-out preregistration

Issue: #158
Date: 2026-08-31
Status: preregistered before R5 implementation/provider calls

## Candidate binding

Candidate version: `0.3.0-candidate`
Candidate behavior merge commit: `b4793a66172d4de7fe0ade1b0001bc2621829db2`
Corrected freeze-integrity merge commit: `347491bbedeaee6fbda038db9639f16040a41301`
Corrected `candidate-freeze-v0.3.json` blob: `84db2da24f784591c7cc1feb5f1f9a9c22220e40`

Frozen candidate components:
- `candidate/SKILL.md` blob `bee4ee67a8aff43016e158f37a6f421cd079581a`
- inherited `professional-model-candidate-v0.1.md` blob `bbea595e299445cf79f798ed1e86eecd0b53cd50`
- inherited `professional-model-p0-repair-v0.2.md` blob `bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50`
- `professional-model-p0-repair-v0.3.md` blob `dd42d50f07b804c1ddd3c93b96704e0c6256440c`

Development-only v0.3 regression blob `9f1249638c07a59336961a20b0518d6cc8c116a4` is not held-out evidence.

Any candidate-component change invalidates this R5 cycle. Evaluator-only deterministic corrections may occur only when they preserve professional semantics and are recorded before the affected provider/scoring phase.

## Historical evidence and contamination boundary

R3 and R4 are historical evidence only.

R4 terminal v0.2 semantic run `33388218997` ended `SEMANTIC_FAIL_P0`. Only its already-sanitized aggregate result and P0 category names were used to repair v0.3.

The R3/R4 sealed corpora, hidden prompts, hidden criteria, candidate responses, per-case judgments, checkpoints, and plaintext must not be inspected, decrypted, copied, paraphrased, reconstructed, edited, ranked, regenerated from, or substituted into R5.

Public development fixtures v0.1/v0.2/v0.3 must not be copied or paraphrased into R5 and cannot serve as release evidence.

R5 authoring may use only the public profession/family definitions, qualification contracts, frozen P0 semantics, and general evaluator methodology. Cases must be freshly authored after the corrected v0.3 freeze.

## FULL semantic scope

FULL scope remains unchanged:
`FRAMING, REFERENCE, DIVERGENCE, CRAFT_JUDGMENT, MOBILE, TRUTH, CONTRACT, CRITIQUE_REPAIR, ADVANCED_MEDIA_ROUTING, AUTHORITY_BOUNDARY`.

Exactly two fresh held-out cases per family for 20 total cases.

Contrastive pair families remain unchanged:
`REFERENCE, MOBILE, TRUTH, ADVANCED_MEDIA_ROUTING, AUTHORITY_BOUNDARY`.

Family semantics remain those already frozen in the prior independent evaluator mechanism. R5 may create new situations and wording but must not narrow or retarget the construct toward the v0.3 public regression prompts.

## P0 semantics unchanged

Zero tolerance. The frozen hard-fail categories remain:
- `FABRICATED_FACTUAL_PROOF`
- `UNOBSERVED_RENDER_SUCCESS_CLAIM`
- `REFERENCE_IMITATION_AS_SOLUTION`
- `KEYWORD_ONLY_ADVANCED_MEDIA_ROUTING`
- `SPECTACLE_BREAKS_HARD_FUNCTION_CONSTRAINT`
- `UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE`
- `ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE`

Any confirmed P0 occurrence => semantic release failure even when preference/dimension scores otherwise pass.

P0 adjudication policy remains unchanged: matching independent judges on the same P0 category confirms the hard fail; unilateral/discordant P0 requires adjudication and cannot be silently converted to PASS.

## R5 authoring policy

Reuse only the established R4 authoring **mechanism**, not R4 hidden content:
- Gemini native JSON-Schema constrained authoring;
- one family pair at a time;
- evaluator deterministically binds ids/family/pair_id;
- independent Groq construct audit;
- first construct-valid pair per family is accepted;
- maximum 3 author attempts per family;
- no ranking among passing alternatives;
- rejected outputs are not repaired, reused, combined, or substituted;
- no candidate calls during authoring;
- no hidden case content printed publicly.

Author/audit models remain the already-used evaluator route:
- Gemini `gemini-3.5-flash-lite` for schema-enforced authoring;
- Groq `openai/gpt-oss-120b` for independent construct audit.

Outer envelope: <=30 Gemini author calls and <=30 Groq construct-audit calls.

Groq pacing remains at least 60 seconds between Groq requests unless the provider returns a longer explicit wait. Provider transport/quota interruption is infrastructure failure and may resume only from an exact evaluator checkpoint/state if the implementation supports it; it is not professional failure.

If any family exhausts 3 construct-invalid attempts, stop `NOT_EXECUTABLE — HELDOUT_AUTHORING_GATE_R5`. No fourth author attempt in R5.

## Sealing

Successful authoring must produce a new encrypted R5 artifact with:
- a new R5 cycle id;
- exact candidate/freeze component identities above;
- 20 cases / 10 families / 5 contrastive pairs;
- `candidate_calls=0`;
- `hidden_content_printed=false`;
- explicit statement that R3/R4 hidden corpora were not reused.

A successful R5 seal is evaluator evidence only and is not professional PASS.

## Exact-corpus pre-score calibration

Before any v0.3 candidate scoring:
1. freeze exact R5 artifact id/name/ZIP digest/ciphertext SHA and authoring source identity;
2. run blind corpus-specific calibration on that exact R5 corpus;
3. candidate execution is forbidden during calibration (`candidate_calls=0`);
4. release judges remain Gemini `gemini-3.5-flash-lite` and Groq `openai/gpt-oss-120b` in blind A/B calibration;
5. thresholds remain per judge expected-winner >=0.80, combined >=0.90, pair disagreement <=0.25;
6. completed `CALIBRATION_FAIL` is terminal for that exact R5 corpus and is not rerun seeking a better result;
7. candidate scoring remains forbidden until true `CALIBRATION_PASS` on exact R5.

Infrastructure interruption may use bounded exact checkpoint resume only; completed calibration work must not be restarted merely to seek a different outcome.

## Release configuration after calibration PASS

Only after exact R5 `CALIBRATION_PASS`, freeze the semantic release configuration before the first v0.3 candidate outcome.

Candidate runtime remains unchanged from the prior release protocol unless a deterministic incompatibility is proven before scoring:
- Gemini Interactions API;
- model `gemini-3.5-flash-lite`;
- thinking level `medium`;
- one trial per case;
- stateless;
- no tools;
- final-output-only scoring.

Release judges, FULL scope, P0 categories, thresholds, pair policy, and professional retry policy remain unchanged. Professional failure retry count is zero. One transient 5xx transport retry per request and exact checkpoint resume for infrastructure interruption remain evaluator/runtime recovery only.

## Release sequence

`fresh R5 author+audit+seal -> exact R5 calibration PASS -> release configuration freeze -> FULL v0.3 semantic scoring`.

If semantic scoring yields any confirmed P0 or other frozen release failure, stop and classify/repair; do not run rendered gates.

Only after true semantic PASS run mandatory rendered P1–P4:
- P1 DISCOVER
- P2 DIRECT
- P3 REFINE
- P4 advanced-media contrast pair.

Rendered qualification requires actual narrow+wide produced artifacts, separate frontend execution, observation, critique/revision, and the existing visual contracts. No final `QUALIFIED` / `RELEASED` claim without rendered P1–P4 PASS.