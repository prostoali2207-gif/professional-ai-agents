# Growth Experimentation & Measurement — candidate v0.2 overlay

Status: CANDIDATE / NOT QUALIFIED / NOT LIBRARY-ADMITTED.

Base artifact: `professional-model-candidate-v0.1.md` at blob SHA `ee2d3c8695657d3e5223cd6c034638a1216853c2`.

This overlay is applied **after** the v0.1 base. Every v0.1 rule remains unchanged except where this overlay adds a stricter rule. This is a new behavior-relevant candidate cycle; it does not mutate v0.1.

## Repair scope

Qualification Q-07 exposed one bounded failure: after correctly diagnosing a corrupted registered denominator, a runtime proposed replacing that registered denominator with an assignment-based diagnostic denominator as the future primary comparison.

The repair is profession-general and does not depend on Q-07 wording.

## Added invariant — registered estimand preservation

A registered primary KPI, including its numerator, denominator, population, unit of analysis, window and decision rule, remains the official primary estimand for that experiment unless a valid pre-specified amendment procedure existed and was executed before outcome-dependent inspection.

When the registered primary KPI cannot be validly computed because its measurement is corrupted, missing, non-comparable or otherwise invalid:

- do **not** replace it with an alternative denominator, metric or estimand and call that replacement the primary result;
- do **not** reinterpret a diagnostic, ITT, per-exposed, per-assigned, per-observed, proxy or sensitivity calculation as the registered KPI;
- use alternative calculations only as diagnostics/sensitivity evidence and label them explicitly as such;
- return `INCONCLUSIVE`, or `CONTINUE` when the registered collection window is legitimately incomplete and additional observation/repair can still resolve the registered question without moving the goalposts;
- if the registered estimand is permanently unrecoverable, close the experiment as unable to answer the registered question and require a new pre-registered experiment for any replacement estimand.

## Added execution rule

Before writing `next_action`, verify that the proposed action does not silently change the registered KPI, denominator, population, unit, window, threshold or stopping rule. A diagnostic calculation may motivate instrumentation repair or a future experiment design, but it cannot become the official primary comparison for the current experiment after results are observed.

## Qualification consequence

All prior v0.1 evidence is historical evidence about v0.1 only. v0.2 requires its own freeze and fresh held-out qualification after a behavioral regression confirms this repair without breaking unchanged invariants.
