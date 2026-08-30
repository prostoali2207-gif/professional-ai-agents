# Visual Design / Art Direction v0.2 — R3 P0 revision record

Date: 2026-08-30
Prior frozen candidate: `e8be839b02f181193afe076839c6ae94fb477a9b`
Prior semantic run: `33299663502`
Prior result: `SEMANTIC_FAIL_P0`

## Evidence boundary

Only sanitized release evidence was used for repair. Hidden R3 case prompts, hidden professional criteria, candidate responses, and per-case hidden evaluator content were not inspected or copied into the new candidate.

Sanitized evidence:
- 20/20 candidate calls completed;
- combined candidate preference rate 1.0;
- pair disagreement 0.0;
- all ordinary semantic dimension groups passed;
- confirmed P0 count 4;
- exposed P0 classes:
  - `ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE`
  - `SPECTACLE_BREAKS_HARD_FUNCTION_CONSTRAINT`
  - `UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE`.

## Failure classification

The base professional model already contained mobile, function, advanced-media and authority concepts. Therefore the smallest evidence-supported repair is not new profession research or broad prompt growth. The failure is classified as insufficient **decision precedence / execution veto semantics**: descriptive rules existed but did not reliably block an invalid READY outcome.

Repair layer:
`professional judgment -> execution control -> ready-state gating`.

## Repair

v0.2 adds:
- hard-function precedence veto;
- mobile viability veto;
- authority veto;
- advanced-media feasibility-before-desirability ordering;
- explicit ready-state gate before implementation/review readiness;
- targeted public development regressions for the three failure classes plus a justified-advanced-media non-regression case.

The repair intentionally does **not**:
- suppress divergence;
- ban 3D/WebGL/motion;
- prefer conservative visual solutions by default;
- transfer UX/product/CRO authority to the visual role;
- reuse or regenerate the R3 held-out corpus as release evidence.

## Evaluation policy for v0.2

1. Run zero-provider structural/static checks.
2. Run public targeted development regression only as development evidence.
3. Freeze the exact v0.2 candidate components.
4. Build a **fresh independent held-out semantic corpus** under the current Agent Architect integrity rules. R3 is historical failure evidence and is not the v0.2 release pack.
5. Preregister judges/configuration, thresholds, retry/resume/stop policy and exact sealed corpus identity before any scored v0.2 candidate outcome.
6. Any P0 occurrence => semantic release failure.
7. Only after fresh semantic PASS run mandatory rendered P1–P4.

Current verdict: `NOT_QUALIFIED`.