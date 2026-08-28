# Growth Experimentation & Measurement — candidate v0.6 overlay

Status: CANDIDATE / NOT QUALIFIED / NOT LIBRARY-ADMITTED.

Base assembly: `v0.1` + `v0.2-overlay` + `v0.3-overlay` + `v0.4-overlay` + `v0.5-overlay`.
Apply this overlay last.

Adjudication behind this overlay:
`maturity-and-causal-ceiling-adjudication-2026-08-28.md`.

## What this overlay fixes

The model has always required a causal claim ceiling but has never said **what the ceiling is a
claim about**. That ambiguity is real: in a randomized experiment whose registered window is
only part-complete, `INCREMENTAL_CAUSAL` is simultaneously defensible (about the outcome
observed so far) and unsupportable (about the registered estimand), and nothing told the analyst
which one was being asked for.

This overlay resolves the ambiguity by scoping the ceiling. It does **not** say that immature
data weakens randomization, and it does **not** treat sparse outcomes as a causal defect.

## Added rule — the claim ceiling is scoped to an estimand

Every causal claim ceiling is a claim about a specific quantity. Record which one.

**Registered estimand.** The registered primary KPI including its numerator, denominator,
population, unit of analysis, **window** and decision rule, as already required by the v0.2
registered-estimand invariant.

**Interim outcome.** The same measurement taken at the current read, before the registered
window has completed. This is a different quantity from the registered estimand, not an early
view of it.

### While the registered window is incomplete

The registered estimand is right-censored and has not been measured. Randomization still
identifies the causal effect on the interim outcome — the design has not stopped working — but a
causal claim **about the registered estimand** is not licensed by data that does not yet contain
it. Therefore:

- with the claim scoped to the registered estimand, the ceiling is at most
  `DIRECTIONAL_ASSOCIATION` until the window matures;
- an analyst who wants a causal claim about what has actually been observed must scope the claim
  to the interim outcome and say so; `INCREMENTAL_CAUSAL` is then available when the design
  identifies it.

The reason is not imprecision. Early converters differ systematically from late converters, and
when arms differ in conversion timing the interim contrast is **biased** for the final contrast
rather than merely noisy. Waiting is what fixes it; more data at the same read depth is not.

Re-scoping to the interim outcome is a statement about evidence, never a licence to act. The
fixed-horizon and stopping-rule discipline of v0.1 is unchanged: an interim causal claim, however
well identified, does not permit an early `SCALE` or an early `KILL` where the registered rule
forbids one.

### Sparse outcomes never lower the ceiling

Sample sparsity is a precision problem, not an identification problem. A randomized, unconfounded
experiment whose registered window is complete retains an `INCREMENTAL_CAUSAL` ceiling even when
the outcome counts are very small. Express that weakness where it belongs — as uncertainty in the
estimate, as `INSUFFICIENT_SAMPLE` blocking `SCALE`, and as an action that does not outrun the
evidence — not by downgrading the causal claim.

Downgrading the ceiling because counts are small is a professional error: it conflates "we cannot
say how large the effect is" with "we cannot attribute the effect at all".

## Output contract v4

`decision_record.causal` gains a required `claim_scope` from the closed vocabulary
`REGISTERED_ESTIMAND` or `INTERIM_OUTCOME`. The ceiling is read against that scope.

A result is invalid when:

- `claim_scope` is `REGISTERED_ESTIMAND`, the case declares the registered window incomplete, and
  `claim_ceiling` is `INCREMENTAL_CAUSAL`;
- `claim_scope` is `INTERIM_OUTCOME` while the case declares the registered window complete —
  there is no interim to scope to;
- `claim_scope` is `INTERIM_OUTCOME` and the action taken would violate the registered stopping
  rule, which re-scoping does not unlock.

## Anti-patterns / hard failures

Fail the professional behavior if it:

- claims an incremental causal effect on the registered estimand while the registered window is
  still open;
- silently reports an interim result as though it were the registered result;
- lowers the causal claim ceiling because outcome counts are small in an otherwise identified,
  window-complete design;
- uses an interim causal claim to justify acting before the registered horizon.
