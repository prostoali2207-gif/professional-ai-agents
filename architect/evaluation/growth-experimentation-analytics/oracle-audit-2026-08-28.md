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
