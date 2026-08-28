# Does outcome-data maturity bound the causal claim ceiling? — adjudication, 2026-08-28

Question raised by the v0.5 held-out gate, where the evaluator's oracle capped `claim_ceiling`
at `DIRECTIONAL_ASSOCIATION` for a **randomized, unconfounded** design whose registered window
was ~30% complete, while permitting `INCREMENTAL_CAUSAL` for a randomized, unconfounded design
whose window was complete. That oracle was internally inconsistent and its cases were burned.

This adjudication is written **before** any v0.6 rule, oracle or fixture change, and it does not
adopt the hypothesis floated in the v0.5 post-mortem. It reaches a materially different answer.

## The hypothesis under test

> "Outcome-data maturity should bound the causal claim ceiling independently of randomized design."

**As stated, this is wrong, and adopting it would encode a professional error.**

Randomization is what buys *identification*. Identification is a property of the assignment
mechanism, not of how much data has accrued. A randomized experiment with a half-observed
window still identifies the causal effect **of the treatment on the outcome as measured at that
read**. A blanket rule that immaturity lowers the ceiling would teach the agent that
randomization stops working when data is thin, which is false and would corrupt reasoning well
beyond this fixture.

It would also collapse a distinction the profession depends on:

- **identification** — does the design permit a causal attribution at all? (randomization,
  exposure validity, no interference)
- **precision** — how well can the magnitude be estimated? (sample size, variance)

Sparse counts are a precision problem. Treating `n = 4 versus n = 1` as an identification
failure is a category error. The v0.5 oracle made exactly that error by folding immaturity and
sparsity into one cap.

## What is actually true

The defensible rule is narrower and follows from the candidate's own existing invariants rather
than from anything observed in v0.5.

v0.2 already defines the registered estimand as including its **window**:

> "A registered primary KPI, including its numerator, denominator, population, unit of analysis,
> **window** and decision rule, remains the official primary estimand."

v0.1 already classifies unmatured downstream outcomes correctly:

> "If downstream outcomes are known to mature after the current read, treat them as
> **immature/right-censored** rather than observed zeroes."

Put together: while the registered window is incomplete, the quantity the analyst can observe is
**not the registered estimand**. It is a time-truncated relative of it. So a causal claim *about
the registered estimand* is not licensed — not because randomization failed, but because the
claim is being made about a quantity that has not been measured yet.

This is not merely a precision argument. Right-censoring at an interim read is a **bias**
mechanism, not only a noise mechanism:

- early converters differ systematically from late converters, so the interim contrast is
  computed on a non-representative subset of the eventual outcome population;
- if the arms differ in *timing* of conversion — entirely plausible when the treatment changes
  the funnel — the interim contrast is biased for the final contrast, and more data at the same
  read depth does not remove the bias;
- this is the familiar interim/surrogate-endpoint problem: an interim endpoint is a different
  endpoint, and agreement with the final endpoint is an empirical claim, not a given.

## Adjudication

The rule is justified, in this form and no wider:

> **The claim ceiling is scoped to the registered estimand.** Randomization identifies the causal
> effect on the outcome as observed at the current read. It does not license a causal claim about
> the registered estimand while that estimand is still right-censored. Therefore, while the
> registered window is incomplete, the ceiling **on the registered estimand** is at most
> `DIRECTIONAL_ASSOCIATION`.
>
> An analyst who wishes to make a causal claim about the interim outcome may do so by **saying so
> explicitly** and scoping the claim to the interim outcome. That claim can be
> `INCREMENTAL_CAUSAL` when the design identifies it.
>
> **Sample sparsity never lowers the ceiling.** A randomized, unconfounded, window-complete
> experiment with very few outcomes retains an `INCREMENTAL_CAUSAL` ceiling and expresses its
> weakness as uncertainty and as a blocked `SCALE`, not as a downgraded causal claim.

## Why this is not fitted to the v0.5 results

The v0.5 post-mortem floated "maturity bounds the ceiling independently of design". That
hypothesis is **rejected here**. What survives is an estimand-scoping rule that was already
implicit in v0.2's registered-estimand invariant and v0.1's right-censoring language, and that
cuts in a direction the v0.5 oracle did not implement: under the corrected rule the candidate's
failing v0.5 answers are still not automatically wrong, because the candidate was never told
which estimand the ceiling referred to, and an `INCREMENTAL_CAUSAL` ceiling scoped to the
interim outcome is legitimate. The v0.5 burn therefore stands.

The rule also creates a new obligation the evaluator did not previously carry: the oracle must
now **accept both** scopings when both are professionally correct, and must stop treating
sparsity as a ceiling constraint. That is a loosening as well as a tightening, which is what
distinguishes a principled rule from one reverse-engineered to fail the observed outputs.

## Consequences for v0.6

1. Professional layer: state the estimand scoping of the ceiling, the right-censoring
   consequence, the explicit interim re-scoping route, and the identification/precision
   separation.
2. Output contract: `causal.claim_scope` becomes a required closed-vocabulary field, so the
   scope of a ceiling is observable instead of guessed.
3. Fixture contract: cases declare `registered_window_complete`, so the rule is checkable
   against a stated fact rather than parsed out of prose.
4. Evaluation: add a family that is randomized, window-complete and deliberately sparse, whose
   correct answer keeps `INCREMENTAL_CAUSAL` while blocking `SCALE`. Without it, a candidate that
   wrongly treats sparsity as an identification failure would pass unnoticed.
