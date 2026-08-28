# Analytics qualification oracle/harness — Architect-level audit, 2026-08-28

Scope: the evaluation instrument only. The Analytics candidate was not modified and no
provider call was made. Findings are produced by `oracle_audit.py`, baselined in
`oracle-audit-baseline.json`, and locked by `test_oracle_audit.py`.

## Why

Three consecutive gates failed on the instrument rather than the candidate — v0.4 on
prose-regex grading, v0.5 on an inconsistent ceiling cap, v0.6 on an under-specified target
and an unpinned unit. Across those cycles the count of genuine candidate behavioural failures
is one (H-GDS-02), repaired and since holding 12/12. The instrument is the bottleneck, so it
gets the audit.

## Detector validation

An audit nobody audits is a second place for defects to hide. Two checks on the detector
itself, both locked as tests:

- run against the **v0.5** oracle it reproduces `C2-cap-inconsistency` across
  `CLEAN_SCALABLE_WIN / IMMATURE_FIXED_HORIZON` — the exact defect that cost that cycle — and
  names the cause: the cap varied on a fact the candidate-facing case never declared;
- run against **v0.6** it is silent on that rule, because v0.6 declares the discriminator.

Two false-positive sources were found in the detector during the audit and fixed before any
finding was reported: `configuration` contains the substring `ratio`, and the consistency key
compared confounding wordings literally, so `"none known"` and `"none identified"` fell into
different buckets — which is precisely why the v0.5 defect survived to a paid gate.

## Findings — current oracle (v0.6): 5 HIGH, 8 MEDIUM, 1 LOW

### HIGH

**D4-fails-open** — `IMMATURE_FIXED_HORIZON`, `SPARSE_BUT_IDENTIFIED`
A structurally invalid result is graded as a pass. Setting `computations` to a string rather
than an array passes, because those families assert no computations and nothing else inspects
the field. The grader validates only what it happens to assert on.

This is a spec-versus-implementation gap, not an oversight of design. The harness README
states the grading order as *"1. schema validity; 2. deterministic arithmetic/state checks;
…"*, and **no grader in any cycle has ever implemented step 1**. A candidate can return output
that violates its own contract and still be scored.

**T1-target-not-action-dependent** — `SPARSE_BUT_IDENTIFIED`
Permits `[INCONCLUSIVE, ITERATE]` but forces the single target `experiment`. Those actions span
experiment-scoped and arm-scoped meanings: `INCONCLUSIVE` says the registered question cannot
be answered and scopes to the experiment, while `ITERATE` says run a properly powered test and
defensibly scopes to the treatment arm. This is the defect that burned five trials in the v0.6
gate.

**U1-unit-not-pinned / U2-ratio-scale-ambiguity** — `CLEAN_SCALABLE_WIN`
`relative_lift_variant_b` is asserted as the bare number `0.5`. The same quantity as a
percentage is `50.0`, and nothing excludes it. The result schema carries a `unit` field for
exactly this reason and the assertion ignores it. This burned one trial in the v0.6 gate.

### MEDIUM

**C6-identity-unchecked** — all five families
A result carrying another case's `fixture_id` is graded as a pass. `grade()` never verifies
that the result belongs to the fixture it is being graded against; the runner supplies the
pairing and nothing re-checks it. No observed failure depends on this, but it removes a cheap
integrity check from a qualification instrument.

**T1** — `UPSTREAM_DOWNSTREAM_CONFLICT`
Permits `[KILL, ITERATE]` with a single forced target. Both are arm-scoped here, so no
divergence has been observed, but the expectation is under-specified in the same way.

**U1** — `UPSTREAM_DOWNSTREAM_CONFLICT`, `UPSTREAM_ONLY_CONFOUNDED`
Currency-valued assertions with no unit pinned. Lower risk than the ratio case because the
scale ambiguity is smaller, but the same defect.

### LOW

**U3-tolerance-scale** — absolute tolerances applied across magnitudes spanning three orders of
magnitude, so `0.02` is 4% of one assertion and 0.0001% of another. The policy is uneven rather
than wrong.

## Checks that pass

Grading is pure, non-mutating and order-independent across `decision_basis`, `computations`,
`confounders` and `blocking_reasons`. Every expectation is satisfiable under every scope it
allows, and every one is discriminating — an action aimed at another arm always fails. All
expectation enums are known to the grader. Every oracle target is a declared arm, every
asserted computation is requested in the candidate-facing instruction, and no candidate-facing
suite leaks an oracle key. All fixtures validate against the declared fixture contract.

## Minimal fix

Four changes, none of which touch the candidate, and which together retire every HIGH finding.

1. **Validate the result against the output contract as grading step 0.** One `jsonschema`
   call at the top of `grade()`, failing closed on violation. This is implementing the
   grading order the harness already documents, and it retires `D4-fails-open` for every
   family at once rather than per-assertion.
2. **Make the target expectation action-dependent.** Replace the scalar `target` with
   `target_by_action: {ACTION: [permitted arms]}`, keeping the scalar as shorthand where a
   single action is permitted. Retires both `T1` findings.
3. **Pin units on computation assertions.** Extend the assertion tuple from `(value, tol)` to
   `(value, tol, unit)` and compare the result's `unit` field, or normalise ratio-like
   quantities before comparison. Retires `U1` and `U2`.
4. **Check result-to-fixture identity in `grade()`.** One equality assertion. Retires `C6`.

Changes 1 and 4 are a few lines each and are pure hardening. Changes 2 and 3 alter the
expectation format, so they require a fresh seed and a new freeze, and must not be applied
inside a scored cycle.

Sequencing note: these are instrument repairs, so they need no candidate version. But because
they change what the gate can detect, the next cycle's result is not comparable to v0.6's on
the burned families, and the preregistration should say so.

## Standing recommendation, unchanged

The assembly is six overlays plus the contract and has already made Groq ineligible on
tokens-per-minute grounds. Consolidating the overlays into one normative document should
precede adding a seventh.

---

# Repairs applied — 2026-08-28

All four proposed fixes are applied. The Analytics candidate is unchanged; only the instrument
moved. Findings on the repaired oracle: **1 LOW, no HIGH, no MEDIUM** (from 5 HIGH, 8 MEDIUM,
1 LOW).

The v0.6 grader and generator are bound by the v0.6 preregistration's blob SHAs and are
historical evidence, so they were left untouched and the repairs landed in new `*_v07` files.
The audit still reports the v0.5 and v0.6 finding sets unchanged, and a test asserts that,
so repairing the current oracle cannot quietly rewrite what the closed cycles were.

## What changed

**1 — contract validity is grading step 0.** `grade()` validates the result against the bound
output contract before anything else and fails closed. This implements the grading order the
harness README has documented since v0.1. Because a scored runner may not have `jsonschema`
installed, there is a dependency-free subset validator driven by the same schema file; both
paths are tested, and the fallback fails closed rather than passing by default.

**2 — targets are action-dependent.** Expectations carry `target_by_action`. `SPARSE_BUT_IDENTIFIED`
now permits `ITERATE` to name either the experiment or the treatment arm while `INCONCLUSIVE`
may name only the experiment. This retires the defect that burned five v0.6 trials without
becoming permission for any target: aiming `INCONCLUSIVE` at an arm still fails.

**3 — computation assertions declare RATIO or ABSOLUTE.** For a ratio the candidate's own `unit`
decides which number is correct, so `0.5 ratio` and `50.0 percent` both pass while `50.0 ratio`
and an unrecognised unit both fail. A ratio is dimensionless, so an unitless declaration means
the ratio form. Absolute assertions are unaffected by the unit string, because constraining
free-form currency labels would just move the brittleness rather than remove it.

**4 — result-to-fixture identity is checked.** A result carrying another case's `fixture_id` is
rejected instead of silently graded against the expectation the runner happened to pair it with.

## Contracts and fixtures

Unchanged. `result-v4.schema.json` already carried the `unit` field that repair 3 relies on, and
`fixture-v3.schema.json` already declared everything the repairs key on. Nothing needed to move.

## Verification, no provider calls

`test_oracle_repairs_v07.py` — 23 tests. Each repair is tested in both directions, because a
repair that only loosens is indistinguishable from fitting the instrument to the answers: the
previously-rejected correct answer now passes, and the answer that must still be rejected still
is. A `NothingWasLoosened` class re-asserts every v0.6-era lock under the v0.7 grader — the
censored-estimand rule, the interim re-scoping route, the sparsity rule, the anti-gaming
control, prose independence, and grading purity.

The full pipeline was driven end to end with a scripted stand-in against a scratch freeze that
was deliberately not committed: correct answers produce a clean `PASS`, and a structurally
invalid output is now rejected at every case rather than scored around.

## Residual finding, accepted

`U3-tolerance-scale` (LOW): tolerances are absolute, so `0.02` is 4% of one assertion and
0.0001% of another. It was not in the approved fix set and no observed failure depends on it.
Left baselined and visible.

## Not done, deliberately

No freeze, no preregistration, no gate run. A preregistration should be written immediately
before execution with a fresh seed, and committing one now would either pre-commit a seed that
goes unused or invite a gate nobody asked for.

One thing the next preregistration must state: these repairs change **what the gate can
detect**, so the next cycle's result is not comparable to v0.6's on the burned families. It is a
new measurement, not a re-run.
