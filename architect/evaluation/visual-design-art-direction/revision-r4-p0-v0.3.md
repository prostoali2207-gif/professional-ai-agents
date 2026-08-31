# Visual Design / Art Direction v0.3 — R4 P0 revision record

Date: 2026-08-31
Prior frozen release head: `774ba8bb9f1ae5643250e15eaa25a53b585478ae`
Prior semantic run: `33388218997`
Prior result: `SEMANTIC_FAIL_P0`
Sanitized report artifact: `9756857311`
Sanitized report artifact digest: `sha256:98158107d57f8b59f468cf8aae12f9927c3eb4affd87a51d09427d974fb65d3d`
Sanitized report payload SHA256: `9011fb75429d67a58b6cfc495a4bdc498d382554360acdf7480e1a8cf3b975dd`

## Evidence boundary

Only sanitized terminal release evidence was used for this repair. Hidden R4 prompts, hidden criteria, hidden case metadata beyond sanitized release reporting, candidate responses, and per-case evaluator content were not inspected, copied, paraphrased, or repaired.

R4 remains sealed historical failure evidence. It is not eligible to become v0.3 final held-out evidence.

Sanitized evidence:
- 20/20 candidate calls completed;
- Gemini expected-winner rate 1.0;
- Groq expected-winner rate 1.0;
- combined preference 1.0;
- disagreement 0.0;
- all ordinary semantic dimension groups passed;
- confirmed P0 count 4;
- confirmed P0 classes:
  - `ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE`;
  - `FABRICATED_FACTUAL_PROOF`;
  - `REFERENCE_IMITATION_AS_SOLUTION`;
  - `UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE`.

## Failure classification

v0.2 already encoded explicit mobile, truth, authority, function and ready-state vetoes. The fresh R4 result demonstrates that those concepts were not reliably controlling the **actual selected output** under conflict/pressure.

The smallest supported repair is therefore not a profession rebuild and not another list of warnings. It is an execution-control repair:

`risk trigger -> protected invariant -> preserve/transform/escalate -> allowed output -> final-output consistency check`.

A response that states the correct rule but still selects a violating mechanism must fail.

## Repair

v0.3 adds:
- pre-commit invariant control for mobile, proof-bearing factual content, reference influence and upstream UX/product/CRO/IA behavior;
- explicit `PRESERVE | TRANSFORM | ESCALATE` outcomes before a risky move can enter the selected direction;
- conflict precedence that forbids comply-first/warn-later behavior;
- truth/proof evidence status enforced in the actual contract;
- mechanism-independence control for references while preserving analytical reference research;
- authored mobile-transformation requirements;
- authority control on the selected implementation-ready default, not merely on recommendation prose;
- a final-output consistency gate that checks the assembled recommendation itself;
- public synthetic targeted regressions for all four exposed P0 classes plus a combined warning-only adversarial trap;
- contrastive non-regression cases proving that authored mobile transformation, clearly non-factual placeholders, analytical reference adaptation, conditional upstream recommendations, and justified bold/reference-informed 3D remain eligible.

The repair intentionally does **not**:
- suppress meaningful divergence;
- ban references, 3D, WebGL or motion;
- impose a generic safe/minimal aesthetic;
- turn visual design into UX/product/CRO ownership;
- reuse or inspect hidden R4 content.

## Evaluation policy for v0.3

1. Run zero-provider structural/static checks.
2. Treat v0.3 targeted fixtures as public DEVELOPMENT ONLY evidence; never as held-out release evidence.
3. Freeze the exact v0.3 candidate components after repair.
4. Create a **fresh independent held-out semantic corpus** after freeze. R4 cannot be reused, edited, regenerated from, paraphrased into, or relabeled as the v0.3 release pack.
5. Preregister exact corpus identity, judges/configuration, thresholds, P0 policy, retry/resume/stop policy and candidate runtime before scored v0.3 outcomes.
6. Preserve the previous release standard unless current Agent Architect methodology provides an evidence-backed reason to change it; do not tune thresholds after seeing outcomes.
7. Any confirmed P0 occurrence remains a semantic release failure.
8. Only after fresh semantic PASS may rendered P1–P4 execute.

Current verdict: `NOT_QUALIFIED`.
