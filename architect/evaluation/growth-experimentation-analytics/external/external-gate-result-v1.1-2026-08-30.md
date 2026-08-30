# Analytics v1.1 external held-out release gate — result record

Recorded: 2026-08-30, from the job log, with no repair and no re-run.

Gate id: `analytics-external-heldout-v1.1-2026-09-05`
Preregistration: `preregistration-external-v1.1-2026-09-05.json`
Candidate: `growth-experimentation-measurement-v1.1-consolidated`,
digest `sha256:3c83f266a4191b2137e8a1cc974bab89d59d2308896b1752a4881205e3019081`
Run: `33299723985` · job `99225432014` · artifact `9728699042` (79 files)
Commit executed: `b1818d580208b874b14e331803c3497c498d3675`
Pack: Groq `openai/gpt-oss-120b`, 5 author calls, **0 admission rejections**, 0 candidate calls
Pack plaintext sha256: `abd40fa429c5fc517d90fd890deb7bd723d6a9811f1eab8db5f08c5686fe802e`
Candidate runtime: Gemini `gemini-3.5-flash-lite`, temperature 0, 0 retries, no best-of-N

---

## Verdict

# FAIL

`REASON: 6 tier-1 professional judgment failure(s)`

Tier 1 tolerance is zero. **The core remains quarantined.**

## The ledger

| Fixture | Family | judged-pass | Tier 1 | Tier 2 | INVALID |
|---|---|---|---|---|---|
| EX-01-01 | UPSTREAM_DOWNSTREAM_CONFLICT | 7/7 | 0 | 0 | 0 |
| EX-01-02 | UPSTREAM_DOWNSTREAM_CONFLICT | 7/7 | 0 | 0 | 0 |
| EX-02-01 | UPSTREAM_ONLY_CONFOUNDED | 6/7 | 1 | 0 | 0 |
| EX-02-02 | UPSTREAM_ONLY_CONFOUNDED | 7/7 | 0 | 0 | 0 |
| EX-03-01 | IMMATURE_FIXED_HORIZON | 6/7 | 0 | 1 | 0 |
| EX-03-02 | IMMATURE_FIXED_HORIZON | 6/7 | 0 | 1 | 0 |
| EX-04-01 | CLEAN_SCALABLE_WIN | 7/7 | 0 | 0 | 0 |
| EX-04-02 | CLEAN_SCALABLE_WIN | 7/7 | 0 | 0 | 0 |
| **EX-05-01** | **SPARSE_BUT_IDENTIFIED** | **2/7** | **5** | 0 | 0 |
| EX-05-02 | SPARSE_BUT_IDENTIFIED | 7/7 | 0 | 0 | 0 |

**Tier 1: 6. Tier 2: 2 of 70 (cap 6). INVALID: 0.** Judged-pass 62/70.

## Movement against the v1.0 external gate

Same criterion, same grader, same tier map, same authoring schemas and oracle behaviour, same
author family and model. The candidate is the only professional thing that changed.

| | v1.0 (run `33293694601`) | v1.1 (run `33299723985`) |
|---|---|---|
| Tier 1 | 15 | **6** |
| Tier 2 | 8 of 70 (cap exceeded) | **2 of 70** (within cap) |
| INVALID | 1 | **0** |
| judged-pass | 39/70 | **62/70** |
| Verdict | INVALID (voided) | **FAIL** |

## What the repair fixed, and what it did not

This is the part that matters more than the verdict.

### Class A — repaired completely: 11 → 0

Not one trial in 70 aimed `CONTINUE` or `INCONCLUSIVE` at an arm, and not one returned a fixture
id as the target. `IMMATURE_FIXED_HORIZON`, which produced 0/7 on one fixture in the previous
cycle and 7 of the 11 class-A failures, is now 6/7 and 6/7 with **zero Tier 1 on either fixture**;
both remaining losses there are Tier 2. The externally authored scope identifiers this time were
again unrelated to the token `experiment`, so the structural recognition rule — *the declared
identifier that keys no per-arm outcome block is the comparison as a whole* — carried across
vocabulary, which is exactly what it was written to do.

### Class C1 — repaired on the family it was observed on: 1 → 0

Both `UPSTREAM_DOWNSTREAM_CONFLICT` fixtures returned 7/7. The decision-paralysis failure against
verified mature downstream economics did not recur there.

### Class D — improved: 8 → 2, within cap

Both remaining Tier 2 are on `IMMATURE_FIXED_HORIZON`: one `scale_readiness` placed outside
`decision_record` (the same misplacement class as before, once in 70 rather than three times), and
one enum typo, `REGISTERed_PRIMARY_KPI`. No malformed or truncated JSON occurred at all this
cycle, against five last cycle.

### Class C2 — **not repaired. This is the blocker.**

`EX-05-01` returned, in four separate trials (1, 3, 4, 7):

```
causal.status must be one of ['IDENTIFIED'], got 'UNRESOLVED'
claim_ceiling 'NONE' understates this design for scope REGISTERED_ESTIMAND (min
INCREMENTAL_CAUSAL); sparse counts are a precision problem, not an identification failure
```

Three of those also failed to cite `INSUFFICIENT_SAMPLE` in `scale_readiness`. A randomised,
exposure-verified, window-complete design with thin outcome counts was treated as an
identification failure — the exact confusion the v0.6 overlay exists to prevent, and a P0 claim of
this core.

It is fixture-specific rather than uniform: `EX-05-02`, the other case in the same family, scored
7/7. Whatever separates the two cases is not visible from the failure text, and the pack is sealed.

### Class B — not repaired: 2 → 2

`EX-05-01` trial 6 omitted `INSUFFICIENT_EVIDENCE` from `decision_basis`; `EX-02-01` trial 4
returned `INCONCLUSIVE` with `NONE_DECIDABLE` where `KILL` on acquisition cost was required, which
is the C1 failure mode appearing on the confounded family instead of the conflict family.

## The finding this cycle establishes about repair method

The adjudication in `failure-adjudication-2026-08-30.md` made two different kinds of repair and
predicted both would work. The evidence separates them, and it does not support one of them.

| Repair | Kind | Result |
|---|---|---|
| Class A: recognition procedure in §5.9 | **new normative content** — a rule the candidate did not previously hold | **11 → 0** |
| Classes B, C: couplings gathered into §6.3 | **no new rule** — existing rules restated as emit-time invalidity conditions | **4 → 6** |

The class-A hypothesis is strongly supported: the candidate was missing a decision procedure, it
was given one, and the failure class vanished across unseen vocabulary. The B/C hypothesis — that
those failures happened because correct rules were stated in their own sections and never gathered
where the result is checked — is **not supported**. Restating them in §6.3 did not make them fire.

That is a genuine result about this candidate and about repair method generally: adding a missing
procedure changed behavior; re-asserting a rule the document already stated did not. Recorded for
whoever takes the next cycle; **not acted on here**, because issue #196 authorises one fresh
release cycle and forbids continuing into another repair cycle after its result.

## Integrity of this cycle

- The grader, classifier, tier map, output contract, fixture contract and every threshold were
  byte-identical to the previous external cycle, and the pack contract's admission behaviour was
  proved identical against the version at commit `1697c9c`. A different result is attributable to
  the candidate.
- The pack was authored on Groq by an author that never saw the candidate, was not told it had
  been repaired, and could not state an expectation. **0 admission rejections** this cycle, against
  the ambiguity that voided run `33299138334`.
- The novelty guard refused every identifier from the previous ledger and from the repository's
  public construct tests; the pack passed it.
- 0 INVALID trials. The apparatus measured the candidate on all 70.

## Repository status after this cycle

| Object | State |
|---|---|
| `growth-experimentation-measurement@1.1.0` | **quarantined**, unchanged |
| Consolidated v1.1 artifact | **candidate**, not released, not admitted to the library |
| Consolidated v1.0 artifact | superseded as candidate; its recorded results stand |
| Run `33293694601` | INVALID, unchanged and not reinterpreted |
| Run `33299138334` | INVALID / burned, apparatus, unchanged |
| Cross-model protocol revision | in force, unchanged; not the blocker |

## Issue #196 return value

**`FAIL — remaining professional blocker: on a randomised, exposure-verified,
registered-window-complete design with thin outcome counts, the candidate still reports
causal.status UNRESOLVED and claim_ceiling NONE — conflating sparsity with identification failure
— in 4 of 7 trials on one fixture, plus 2 further judgment failures. 6 tier-1 against a
zero-tolerance bar.`**

No further repair cycle was started. The core stays quarantined.
