# Visual Design / Art Direction v0.3 — fresh R6 held-out pair-contract remediation preregistration

Issue: #158
Date: 2026-09-01
Status: **PRE-SCORE / preregistered before R6 implementation or provider calls**

## Frozen candidate boundary

Candidate behavior is unchanged from the reconciled v0.3 freeze:
- candidate version: `0.3.0-candidate`
- behavior merge: `b4793a66172d4de7fe0ade1b0001bc2621829db2`
- freeze-integrity merge: `347491bbedeaee6fbda038db9639f16040a41301`
- freeze blob: `84db2da24f784591c7cc1feb5f1f9a9c22220e40`
- `candidate/SKILL.md`: `bee4ee67a8aff43016e158f37a6f421cd079581a`
- base professional model: `bbea595e299445cf79f798ed1e86eecd0b53cd50`
- v0.2 repair model: `bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50`
- v0.3 repair model: `dd42d50f07b804c1ddd3c93b96704e0c6256440c`

R6 is evaluator-infrastructure remediation only. Any change to these professional components invalidates this preregistration.

## Closed R5 evidence boundary

R5 run `33420302302` ended `NOT_EXECUTABLE_HELDOUT_AUTHORING_GATE_R5` before sealing and before any candidate execution.

Only the public-safe aggregate counters are admissible for remediation design:
- failed family: `TRUTH`
- `author_calls = 11`
- `audit_calls = 11`
- `candidate_calls = 0`
- `hidden_content_printed = false`
- `TRUTH attempts = 3`
- `TRUTH structural_rejections = 0`
- `TRUTH audit_rejections = 3`

No R5 hidden brief, context, constraint, baseline, criterion, P0 trigger, generated pair text, audit rationale, or rejected output may be inspected, reused, edited, paraphrased, reconstructed, or promoted into R6 evidence. No accepted-but-unsealed R5 family pair may be carried forward. R5 is closed historical evaluator evidence only.

R3 and R4 hidden corpora remain excluded as before.

## Root-cause classification

All three failed `TRUTH` attempts reached independent construct audit, so the observable failure is not JSON shape, deterministic validation, provider transport, or candidate behavior.

The existing paired-family author contract states that a contrastive pair must differ by one decision-relevant material fact, but the structured output schema contains only two independent case objects. The one-variable contrast is therefore an instruction-level semantic invariant rather than an explicit author/evaluator interface object.

This creates an avoidable construct-production ambiguity for all declared contrastive families. R6 repairs that **general paired-case interface**, not the `TRUTH` professional semantics and not the candidate.

## R6 remediation mechanism

Keep the proven R5 family-local first-pass authoring architecture, provider identities, professional family requirements, P0 taxonomy, budget, stop rule and candidate isolation.

For every declared contrastive family, the author must produce an evaluator-only `pair_contract` before the two cases:
- `controlled_material_fact` — the single decision-relevant fact intentionally changed;
- `case_1_value`;
- `case_2_value`;
- `held_constant_facts` — at least four material facts that must remain constant;
- `why_this_one_fact_can_change_professional_stance` — evaluator-only construct rationale.

The author then creates case 1 and derives case 2 under that contract. Candidate-visible fields remain only the existing `brief`, `context`, and `constraints`; the pair contract is never supplied to the candidate.

Deterministic validation must require a complete pair contract for paired families, distinct case values, and the declared held-constant set. Independent construct audit must verify that the authored cases actually honor the pair contract and still meet the unchanged construct-quality criteria. The pair contract is evidence for the auditor, not an automatic PASS.

Unpaired families retain the existing R5 schema and construct audit unchanged.

This interface repair applies uniformly to all five paired families:
`REFERENCE, MOBILE, TRUTH, ADVANCED_MEDIA_ROUTING, AUTHORITY_BOUNDARY`.

It must not add a `TRUTH`-specific escape hatch, loosen the one-material-fact rule, expose expected answers to candidate-visible fields, or alter professional scoring semantics.

## FULL release construct remains unchanged

Required families, exactly two fresh R6 cases each:
`FRAMING, REFERENCE, DIVERGENCE, CRAFT_JUDGMENT, MOBILE, TRUTH, CONTRACT, CRITIQUE_REPAIR, ADVANCED_MEDIA_ROUTING, AUTHORITY_BOUNDARY`.

Declared paired families remain the five listed above. Exactly 20 fresh cases and 5 contrastive pairs are required before sealing.

P0 hard-fail categories remain exactly:
- `FABRICATED_FACTUAL_PROOF`
- `UNOBSERVED_RENDER_SUCCESS_CLAIM`
- `REFERENCE_IMITATION_AS_SOLUTION`
- `KEYWORD_ONLY_ADVANCED_MEDIA_ROUTING`
- `SPECTACLE_BREAKS_HARD_FUNCTION_CONSTRAINT`
- `UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE`
- `ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE`

P0 tolerance remains zero. Release scope remains FULL.

## Authoring providers and acceptance policy

Author: Gemini `gemini-3.5-flash-lite` with native JSON-Schema structured output.
Independent construct auditor: Groq `openai/gpt-oss-120b`, temperature 0, no candidate access.

For each family:
1. author one fresh pair;
2. deterministic structural/interface validation;
3. independent construct audit;
4. accept the **first** pair with audit `accept=true`;
5. discard rejected/invalid pairs without inspection or repair;
6. never rank several passing alternatives.

Maximum attempts: **3 per family**. Every author call counts. Maximum envelope: <=30 Gemini author calls + <=30 Groq construct-audit calls. Stop as soon as every family has its first accepted pair.

If any family reaches 3/3 without acceptance, stop `NOT_EXECUTABLE_HELDOUT_AUTHORING_GATE_R6`. No fourth attempt, no same-cycle model/rubric/family-contract change, no hidden-content inspection, and no candidate call.

Provider/quota/transport failure is infrastructure failure and must not be interpreted as professional failure.

## Independence / leakage controls

Before R6 sealed identity exists, forbidden:
- candidate execution or candidate-output inspection;
- reuse of any R3/R4/R5 hidden case or partial accepted pair;
- human/AI semantic editing of a rejected R6 pair;
- using rejection rationale to rewrite a pair in the same cycle;
- choosing among multiple passing pairs;
- public development fixtures as held-out evidence;
- changing release judges, release thresholds, P0 taxonomy, FULL scope, or professional family semantics.

Public-safe output may contain only aggregate counters, family attempt counts, structural/audit rejection counts, provider identities, sealed artifact identities, `candidate_calls=0`, and `hidden_content_printed=false`.

## Resource / execution gate

Static/no-secret CI must pass before metered authoring. Metered R6 authoring is issue-command opt-in only and must never run automatically on push or pull request.

The R6 pre-run record must state the exact merged evaluator head and `candidate_calls=0` before the one normal authoring trigger.

## After a successful R6 seal

A successful seal is not professional PASS.

Before any v0.3 candidate scoring:
1. freeze exact R6 artifact identity;
2. run blind exact-corpus calibration with the already-established release judges and unchanged thresholds;
3. require `candidate_calls=0` during calibration;
4. candidate scoring remains forbidden until true `CALIBRATION_PASS` on exact R6.

After calibration PASS, freeze the exact semantic release configuration and run one FULL v0.3 semantic qualification. Any confirmed P0 is semantic failure.

Only after semantic PASS may mandatory rendered P1–P4 execute. No final `QUALIFIED` claim without rendered P1–P4 PASS.