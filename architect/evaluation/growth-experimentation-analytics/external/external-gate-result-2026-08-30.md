# Analytics external held-out release gate — result record

Recorded: 2026-08-30, from the job log, with no repair and no re-run.

Gate id: `analytics-external-heldout-2026-09-02`
Preregistration: `preregistration-external-2026-09-02.json`
Candidate: `growth-experimentation-measurement-v1.0-consolidated`,
digest `sha256:3f4f3e133e81b00a1536fc6c72f1f59c24ef9f7b4c50c762c3c6c5bf6c4dd63d`
Run: `33293694601` · job `99209632986` · artifact `9727031366` (74 files)
Commit executed: `1697c9c688e734582a1354d74593b4279846e847`
Pack author: Groq `openai/gpt-oss-120b`, 5 author calls, 0 admission rejections, 0 candidate calls
Candidate runtime: Gemini `gemini-3.5-flash-lite`, temperature 0, 0 retries, no best-of-N

---

## Verdict

# INVALID

`REASON: 1 trial(s) did not measure the candidate; the gate is void.`

One trial — `EX-05-01` trial 6 — returned `Gemini API HTTP 500: "gemini-3.5-flash-lite is
currently experiencing high demand"`. Under the frozen tier map that is an apparatus failure, and
under the preregistered pass rule any INVALID trial voids the whole gate: not PASS, not FAIL.

**The release does not close. `growth-experimentation-measurement` stays quarantined.**

## The observed ledger

An INVALID verdict means the gate produced no *verdict* about the candidate. It does not mean the
run produced no *observations*: 69 of 70 trials did reach the candidate and were graded. Reporting
the verdict without the ledger would hide a critical-failure rate behind a procedural outcome,
which `eval-integrity-and-regression.md` and `behavioral-validation-harness.md` both forbid. So the
ledger is recorded here in full, as observation and explicitly **not** as a verdict.

| Fixture | Family | judged-pass | Tier 1 | Tier 2 | INVALID |
|---|---|---|---|---|---|
| EX-01-01 | UPSTREAM_DOWNSTREAM_CONFLICT | 7/7 | 0 | 0 | 0 |
| EX-01-02 | UPSTREAM_DOWNSTREAM_CONFLICT | 4/7 | 1 | 2 | 0 |
| EX-02-01 | UPSTREAM_ONLY_CONFOUNDED | 5/7 | 0 | 2 | 0 |
| EX-02-02 | UPSTREAM_ONLY_CONFOUNDED | 5/7 | 1 | 1 | 0 |
| EX-03-01 | IMMATURE_FIXED_HORIZON | 6/7 | 1 | 0 | 0 |
| **EX-03-02** | IMMATURE_FIXED_HORIZON | **0/7** | **7** | 0 | 0 |
| EX-04-01 | CLEAN_SCALABLE_WIN | 6/7 | 0 | 1 | 0 |
| EX-04-02 | CLEAN_SCALABLE_WIN | 7/7 | 0 | 0 | 0 |
| EX-05-01 | SPARSE_BUT_IDENTIFIED | 3/7 | 2 | 1 | 1 |
| EX-05-02 | SPARSE_BUT_IDENTIFIED | 3/7 | 3 | 1 | 0 |

**Tier 1: 15. Tier 2: 8 of 70. INVALID: 1.**

Against the preregistered bar — Tier 1 tolerance 0, Tier 2 ≤ 2 per fixture and ≤ 6 in total — an
apparatus-clean run carrying these observations would have been a **FAIL on both counts**: 15
Tier 1 failures against a zero tolerance, and 8 Tier 2 against a total cap of 6. Nothing in this
run points toward a PASS.

## The Tier 1 failures, by class

### A. Experiment-scoped actions aimed at a single arm — 11 of 15

The largest class. When the correct action is scoped to the comparison as a whole, the candidate
named one arm instead, or named something that is not an arm at all:

```
EX-03-02 t1,2,4,5,6  target is 'ui_refresh', but action 'CONTINUE' may only be aimed at ['ui_experiment']
EX-03-02 t3,7        target 'EX-03-02' is not one of the declared arms ['legacy_ui','ui_experiment','ui_refresh']
EX-03-01 t2          target 'EX-03-01' is not one of the declared arms ['bundle_off','price_opt','pricing_test']
EX-05-01 t1          target is 'personalized_sort', but action 'INCONCLUSIVE' may only be aimed at ['sort_algorithm_test']
EX-05-02 t1,3        target is 'guided_tour_flow', but action 'INCONCLUSIVE' may only be aimed at ['onboarding_experience_test']
```

Three of these returned the **fixture id** as the operational target. That is wrong under any
reading: a fixture id is not an arm, and `operational.target` is a structural identifier resolved
by set membership against the case's declared arms.

The other eight are the substantive part of the class: at an incomplete fixed horizon, `CONTINUE`
means continue the experiment to its registered horizon — it is not a per-arm instruction, and
aiming it at the leading arm is the early-stopping error in different clothing. The same reasoning
applies to `INCONCLUSIVE`, which says the registered question cannot be answered.

**This is the class the external pack was built to expose.** The frozen generator named the scope
arm literally `experiment` in every case, and the candidate scored 7/7 on this family in the v1.0
gate. Here the external author named it `ui_experiment`, `pricing_test`, `sort_algorithm_test` and
`onboarding_experience_test`, and the same behavior did not survive. The v1.0 result on this
family was, at least in part, riding on the evaluator's own vocabulary.

**Open adjudication item, recorded rather than resolved.** I authored this oracle, and 11 of 15
Tier 1 failures land on one assertion (`target_by_action` for experiment-scoped actions). Whether
that assertion is *too* strict is a legitimate question. It is not one I may answer now: relaxing
an assertion after seeing which trials it failed is precisely the construct-fitting this cycle
exists to prevent. It is carried forward as an item for a fresh, separately preregistered cycle.
Note that the assertion is byte-identical in intent to the frozen generator's, which the candidate
satisfied 7/7 — so it is not a *new* strictness, only a newly un-cued one.

### B. Required decision basis omitted — 2 of 15

```
EX-02-02 t7  decision_basis must record COST_OF_WAITING
EX-05-01 t3  decision_basis must record INSUFFICIENT_EVIDENCE
```

The action was right; the recorded grounds for it were incomplete.

### C. Substantive professional errors — 2 of 15

These two are not vocabulary, not scoping, and not disputable:

```
EX-01-02 t1  action must be one of ['KILL','ITERATE'], got 'INCONCLUSIVE'
             decisive_metric 'NONE_DECIDABLE' is not defensible here; expected MATURE_DOWNSTREAM_ECONOMICS
             decision_basis must record MATURE_DOWNSTREAM_ECONOMICS
```
Downstream-versus-proxy precedence. Verified mature gross profit made the decision, and the
candidate declared nothing decidable — decision paralysis on a case that was decidable.

```
EX-05-02 t6  causal.status must be one of ['IDENTIFIED'], got 'UNRESOLVED'
             claim_ceiling 'NONE' understates this design for scope REGISTERED_ESTIMAND
             (min INCREMENTAL_CAUSAL); sparse counts are a precision problem, not an
             identification failure
```
Sparsity-versus-identification. A randomized, window-complete design with thin counts was treated
as an identification failure — the exact confusion the v0.6 overlay was written to prevent, and a
P0 claim of this core.

**Even discounting class A entirely, four Tier 1 failures remain, two of them on P0 behavior, and
Tier 2 alone exceeds its total cap.** The gate does not pass under any reading of the disputed
assertion.

### Tier 2 — 8 of 70

Five malformed JSON (truncated or unterminated objects at char ~1400–3100) and three placements of
`scale_readiness` inside `decision_record.operational` instead of `decision_record`. The v1.0 gate
saw 6/70 of this class; 8/70 here is consistent with it, not a new failure mode.

## What must not be concluded, and what must not be done next

* **This is not a FAIL verdict.** The preregistered rule returns INVALID and I am not entitled to
  convert it. The ledger above is evidence for the next cycle to preregister against, not a verdict
  reached after the fact.
* **This gate must not be re-run.** The preregistration permits a re-run after an apparatus fault,
  written on the assumption that an INVALID run measured nothing. That assumption does not hold
  here: 69 trials were measured and 15 of them failed. Re-running now, having seen that ledger,
  would be seeking a better sample on an unchanged candidate — forbidden by
  `eval-integrity-and-regression.md` ("do not quote a best run as system reliability") and by
  `paid-execution-policy.md` ("do not rerun an unchanged professional failure merely to seek a
  better stochastic result"). The letter of the preregistration allows it; its purpose does not.
* **The criterion must not be changed now.** That an INVALID trial can void a run whose measured
  content was plainly failing is a real weakness in the rule I preregistered — the INVALID class
  was designed to stop throttling being blamed on the candidate, not to erase observed professional
  failures. Correcting it after seeing this result would be fitting the criterion to the outcome.
  It is recorded here as an input to the next criterion review, unchanged for this cycle.

## Repository status after this cycle

| Object | State |
|---|---|
| `growth-experimentation-measurement@1.1.0` | **quarantined**, unchanged |
| Consolidated v1.0 artifact | **candidate**, not released, not admitted to the library |
| v1.0 two-tier gate result (`33264418604`, PASS) | unchanged; still valid for what it measured |
| Cross-model protocol revision | in force, unchanged; it was not the blocker |
| External pack apparatus | frozen, unchanged |

The cross-model revision and the external pack both did their job: the pack was authored on an
independent family with no candidate access, admitted without a single rejection, and it found
behavior the evaluator's own generator did not. The blocker is not the protocol.

## Issue #189 return value

**`INVALID / NOT EXECUTABLE — apparatus blocker: one trial returned Gemini HTTP 500 (model
capacity), which voids the gate under the preregistered pass rule.`**

With the material qualification that the 69 measured trials carried 15 Tier 1 professional-judgment
failures against a zero-tolerance bar, including two P0-class errors, so the release does not close
and the core remains quarantined on professional grounds as well as procedural ones.
