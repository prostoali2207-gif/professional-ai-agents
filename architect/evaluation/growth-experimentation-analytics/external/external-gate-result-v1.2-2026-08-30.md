# Analytics v1.2 external held-out release gate — result record

Recorded: 2026-08-30, from the job log, with no repair and no re-run.

Gate id: `analytics-external-heldout-v1.2-2026-09-09`
Preregistration: `preregistration-external-v1.2-2026-09-09.json`
Candidate: `growth-experimentation-measurement-v1.2-consolidated`,
assembly digest `sha256:d57001f6820cc346098397432bc247d05eb529c1611b785dc978552010b25629`
Run: `33304743788` · job `99239171057` · artifact `9730260513` (78 files)
Commit executed: `1dd1583aad7c39a9c95de336570411f7373674f6`
Pack: Groq `openai/gpt-oss-120b`, 0 admission rejections, 0 candidate calls
Candidate runtime: Gemini `gemini-3.5-flash-lite`, temperature 0, 0 retries, no best-of-N

---

## Verdict

# PASS

`REASON: no tier-1 failure; tier-2 within both caps`

## The ledger

| Fixture | Family | judged-pass | Tier 1 | Tier 2 | INVALID |
|---|---|---|---|---|---|
| EX-01-01 | UPSTREAM_DOWNSTREAM_CONFLICT | 7/7 | 0 | 0 | 0 |
| EX-01-02 | UPSTREAM_DOWNSTREAM_CONFLICT | 7/7 | 0 | 0 | 0 |
| EX-02-01 | UPSTREAM_ONLY_CONFOUNDED | 7/7 | 0 | 0 | 0 |
| EX-02-02 | UPSTREAM_ONLY_CONFOUNDED | 7/7 | 0 | 0 | 0 |
| EX-03-01 | IMMATURE_FIXED_HORIZON | 7/7 | 0 | 0 | 0 |
| EX-03-02 | IMMATURE_FIXED_HORIZON | 7/7 | 0 | 0 | 0 |
| EX-04-01 | CLEAN_SCALABLE_WIN | 7/7 | 0 | 0 | 0 |
| EX-04-02 | CLEAN_SCALABLE_WIN | 6/7 | 0 | 1 | 0 |
| EX-05-01 | SPARSE_BUT_IDENTIFIED | 7/7 | 0 | 0 | 0 |
| EX-05-02 | SPARSE_BUT_IDENTIFIED | 7/7 | 0 | 0 | 0 |

**Tier 1: 0 of 70. Tier 2: 1 of 70 (cap 6). INVALID: 0.** Judged-pass 69/70.

Nine fixtures returned 7/7. The tenth lost one trial to a single output-contract violation, well
inside both the per-fixture cap of 2 and the total cap of 6.

## The repair under test, measured

The identification ledger was the only professional change since the previous cycle. Everything
else — grader, classifier, tier map, output contract, fixture contract, authoring schemas, oracle,
runner, and every threshold — was byte-identical to the cycle that produced run `33299723985`.

| | v1.0 (`33293694601`) | v1.1 (`33299723985`) | v1.2 (`33304743788`) |
|---|---|---|---|
| Tier 1 | 15 | 6 | **0** |
| Tier 2 | 8/70 (over cap) | 2/70 | **1/70** |
| INVALID | 1 | 0 | **0** |
| judged-pass | 39/70 | 62/70 | **69/70** |
| Verdict | INVALID | FAIL | **PASS** |

The dominant blocker is gone. `SPARSE_BUT_IDENTIFIED` — which returned 2/7 on one fixture last
cycle, with four trials writing sparsity into the causal channel — returned **7/7 on both
fixtures**. The two residual failures the same procedure was meant to cover, the decision-basis
omission and the causal-paralysis leak on the confounded family, did not recur either:
`UPSTREAM_ONLY_CONFOUNDED` went 6/7 and 7/7 to **7/7 and 7/7**.

## What this cycle establishes about repair method

Across three externally authored cycles the same distinction held every time.

| Repair | Kind | Class outcome |
|---|---|---|
| §5.9 structural recognition of the comparison-level identifier | procedure | 11 → 0 |
| §6.3 couplings, existing rules restated as emit-time checks | restatement | 4 → 6 |
| §5.2 identification ledger and channel separation | procedure | 6 → 0 |

Twice a procedure eliminated its failure class outright. Once a restatement of rules the document
already carried made its classes slightly worse. That is the transferable finding from this
sequence, and it was recorded as a prediction in `ledger-repair-adjudication-2026-08-30.md` before
this run, not fitted to it afterwards.

## Integrity of this cycle

- **Only the candidate changed.** Asserted deterministically before execution against the previous
  preregistration: grader, classifier, tier map, pack contract, runner and every threshold
  byte-identical; only the novelty guard and its loader moved, and the guard extends the previous
  refusal list rather than replacing it.
- **The pack is genuinely held out.** Authored on Groq by an author that never saw the candidate,
  was not told it had been repaired, and was not told an identification ledger exists. Its schema
  has no field capable of carrying a recommendation, ceiling, causal status or scale state. 0
  admission rejections; the novelty guard refused every identifier observed in either previous
  ledger and the pack passed it.
- **The apparatus measured the candidate on all 70 trials.** 0 INVALID.
- **The criterion was not touched.** Same trial count, same caps, same zero tier-1 tolerance,
  unchanged since the stability audit adopted them. Issue #205 forbade moving them to chase a pass
  and nothing did.

## Honest limits of the claim

* **Cross-runtime portability is untested.** The claim is scoped to `gemini-3.5-flash-lite` at
  temperature 0. Deployment on another family is a revalidation trigger, not an inherited PASS.
* **The author is a model, not a practitioner.** Evaluator authorship is removed; model authorship
  is not.
* **The structural margin is thinner than the professional one.** 1 tier-2 of 70 passes
  comfortably, but this class has never reached zero in any cycle (8, then 2, then 1).
* **A gate is not production.** No affordable gate detects an intermittent judgment defect at low
  incidence; that belongs to production learning, and it is why "any tier-1 failure observed in
  production use" is a recorded revalidation trigger.

## Repository status after this cycle

| Object | State |
|---|---|
| `growth-experimentation-measurement@1.2.0` | **qualified**, catalog and manifest |
| Artifact digest | `sha256:95e743815d93841fb43051ab116613f5108f1683b96584a193d86c5fbd037f7d` |
| `growth-experimentation-measurement@1.1.0` | quarantined, unchanged; history preserved |
| `qualification-status-v0.3.json` | reconciled with a `superseded_by` pointer; its verdict not withdrawn |
| Runs `33293694601`, `33299138334`, `33299723985`, `33293517671` | unchanged and not reinterpreted |

## Issue #205 return value

**`QUALIFIED / RELEASED`** — `growth-experimentation-measurement` 1.2.0, artifact digest
`sha256:95e74381…7f7d`, on external held-out run `33304743788`: 70 trials, 0 tier-1, 1 tier-2, 0
INVALID, scoped to the Gemini runtime family with cross-runtime portability recorded as a
revalidation trigger.
