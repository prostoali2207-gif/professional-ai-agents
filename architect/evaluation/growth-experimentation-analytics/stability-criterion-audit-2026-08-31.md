# Qualification stability criterion — audit

Date: 2026-08-31. Scope: the **criterion**, not the candidate.

Nothing in the Analytics candidate, consolidated v1.0, grader, generator, fixtures, contracts,
freezes or the v1.0 gate result was changed by this audit. No provider call was made. No
qualification policy is changed by this document; it is the evidence record for a decision that
must be taken, and preregistered, before the next seed is drawn.

Authority: `architect/SKILL.md` Phase 10 (evaluation before readiness), Phase 6A (resource and
cost engineering), Phase 14 (production learning); `methodology/eval-integrity-and-regression.md`
§"Reliability across trials"; `evaluation/behavioral-validation-harness.md` §"Release rule".

**The v1.0 gate verdict stands as FAIL.** Nothing below may be applied retrospectively to it.

## 0. Evidence base

Three gates, identical frozen instrument (generator, grader, runner, output contract, fixture
contract byte-identical throughout), 10 fixtures × 3 trials each, Gemini `gemini-3.5-flash-lite`
at temperature 0.

| gate | seed | trials | pass | judgment failures | record-completeness | contract-invalid |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v0.7 | 20260829 | 30 | 24 | **4** | 0 | 2 |
| v0.8 | 20260830 | 30 | 28 | 0 | **1** | 1 |
| v1.0 | 20260831 | 30 | 29 | 0 | 0 | **1** |

Every failure, classified by the axis that turns out to decide everything — **is this failure
deterministically detectable by the consuming system?**

- **Judgment** — the decision itself is wrong: `INCONCLUSIVE` aimed at an arm (v0.7 ×3),
  `causal.status UNRESOLVED` with the ceiling understated on an identified design (v0.7 ×1).
  Nothing downstream catches these. A wrong recommendation arrives looking exactly like a right one.
- **Record completeness** — the decision is right, the audit record is incomplete: `decision_basis`
  omitted `REGISTERED_PRIMARY_KPI` (v0.8 ×1). No validator catches it either.
- **Contract-invalid** — the output is not a valid instance of the frozen contract: invalid JSON
  (v0.7, v0.8), an invented field (v0.7), a field in the wrong place (v1.0). **JSON-Schema
  validation catches every one of these, every time, in production as in the gate.**

Judgment failures went **4 → 0 → 0**. What remains is expression, at roughly 4% per trial.

## 1. What reliability claim do we actually want to prove?

Not "the candidate never errs." That claim is unprovable against a non-deterministic sampler and
was never the professional requirement.

**The premise that broke the criterion is that `temperature = 0` makes the provider
deterministic. It does not** — batching, kernel non-determinism and routing all leave residual
variation, and the three gates measure it directly at ~4% per trial. The criterion was designed
as if for a deterministic system.

The claim we need before production has two parts, and they are not the same kind of claim:

**(a) Professional judgment is correct — categorical, zero tolerance.** For each of the five
construct families, the frozen candidate reaches the professionally correct decision: the right
action, aimed at the right scope, with a causal status and claim ceiling the design supports, a
defensible decisive metric, a complete record of the grounds actually used, and a SCALE gate that
holds. A failure here is silent: it reaches the decision-maker looking like a valid answer.

**(b) Output is contract-valid often enough — rate-bounded, not categorical.** The candidate
emits a valid instance of the frozen contract at a rate high enough that the deterministic
validation already required of any consuming system absorbs the remainder. A failure here is
loud: it is caught with certainty before anyone reads it.

These need different instruments. One criterion that treats them identically cannot measure
either well.

## 2. Does `3 trials → required 3/3` match that claim?

**No, on three counts.**

**It conflates (a) and (b).** A misplaced field and a causal overclaim end the gate identically,
though one is caught by a validator and the other reaches a decision-maker.

**Its rejections are dominated by (b).** With sound judgment and a 4.4% contract-invalid rate, the
rule rejects **74.4%** of the time. That is not a bar the candidate is failing to clear; it is an
instrument that mostly returns FAIL.

**Its apparent power against judgment defects is largely borrowed from that noise.** At an
intermittent judgment defect appearing in a third of trials (q = 0.33) the rule "detects" 91.2% —
but it also rejects 74.4% of sound candidates. Its discrimination ratio (detection ÷ false-reject)
is **1.2×**. A rule that rejects nearly everything will of course also reject defective things.
That is not measurement.

A coherence check settles it: under this rule, P(a sound-judgment candidate fails one gate) =
74.4%, and P(it fails two in a row) = **55.4%**. Observing v0.8 and v1.0 both fail is *more likely
than not* even if the professional judgment was perfect throughout. The criterion cannot
distinguish the world we are in from the world where nothing is wrong.

**What the rule gets right, and must be preserved:** zero tolerance is correct for professional
judgment. It is the *scope* of the zero tolerance that is wrong, not the idea.

## 3. Expected false-reject rate at the observed error rate

FR = 1 − (1 − p)^30, for a candidate whose judgment is sound.

| p (per-trial expression error) | false-reject | expected gates until a PASS |
| ---: | ---: | ---: |
| 0.006 (95% CI lower) | 16.5% | 1.2 |
| 0.033 (v1.0 observed) | 63.5% | 2.7 |
| **0.044 (pooled, 90 trials)** | **74.4%** | **3.9** |
| 0.067 (v0.7/v0.8 observed) | 87.5% | 8.0 |
| 0.167 (95% CI upper) | 99.6% | 240 |

A second finding matters as much: **from one gate we cannot even estimate p.** v1.0's 1-in-30 gives
a 95% Wilson interval of [0.6%, 16.7%] — a false-reject rate somewhere between 17% and 99.6%. The
three gates pooled narrow it to [2.4%, 12.4%]. Any criterion tuned to a point estimate from 30
trials is tuned to noise; this is an argument for *more trials*, independent of the threshold.

## 4. Alternatives, each tested rather than asserted

All figures at the pooled contract-invalid rate p₂ = 4/90 = 0.044, ten fixtures.

| rule | false-reject | detect q=0.5 | q=0.33 | q=0.2 | discrimination |
| --- | ---: | ---: | ---: | ---: | ---: |
| **CURRENT** k=3, every trial must pass | 74.4% | 96.3% | 91.2% | 85.0% | 1.2× |
| k=5, every trial must pass | 89.5% | 99.6% | 98.2% | 95.7% | 1.1× |
| k=5, per-fixture ≥4/5 (any failure) | 9.7% | 86.2% | 65.0% | 43.3% | 6.7× |
| two-tier k=5, tier1=0, tier2 ≤2/fixture ≤4 | 7.4% | 97.1% | 87.5% | 69.6% | 11.9× |
| **two-tier k=7, tier1=0, tier2 ≤2/fixture ≤6** | **5.4%** | **99.3%** | **94.3%** | **80.2%** | **17.4×** |

**More trials at the same bar — rejected, and it is worth saying why loudly.** k=5 under unanimity
makes false-reject *worse*, 74.4% → 89.5%. More draws means more chances for a stochastic
expression error. Under a unanimity rule, adding trials degrades the instrument. This is the
intuitive fix and it is backwards.

**Binomial per-fixture threshold on all failures — rejected.** k=5 requiring ≥4/5 has an attractive
9.7% false-reject, but it tolerates *judgment* failures: 35% false-pass at q = 0.33, 57% at
q = 0.2. That is precisely "a critical failure hidden by averaging", which
`behavioral-validation-harness.md` forbids in its release rule.

**Per-family threshold — rejected, worse.** Pooling two fixtures per family aggregates across
distinct constructs; a fixture that is systematically wrong can be carried by its partner.

**Structural retry for malformed output — rejected as the primary mechanism.** It looks clean: the
trigger is mechanical (output fails schema validation), decision-free, and it would cut the
contract-invalid rate to p₂² ≈ 0.1%. But a retried trial produces *different professional content*,
and that content is what gets graded. It is a second judgment draw, granted exactly on the cases
where the model was confused enough to break the contract — the worst possible place to grant one.
It buys less than the two-tier rule and costs an integrity property. Kept as a rejected option with
its reason recorded, not as a fallback.

**Two-tier — recommended.** Zero tolerance on judgment; a rate ceiling on contract validity. It
does not weaken tier 1 at all: tier-1 power is 1 − (1−q)^k, which depends only on the trial count
and is *strictly better* at k=7 than the current rule at k=3. It removes only the rejections that
were never measuring professional error.

## 5. Does the recommendation hide a real P0/P1 failure?

Asked adversarially, because the honest answer is "partly, and here is the containment".

**No, for tier 1.** Every failure that changes or misstates the decision keeps zero tolerance
across all 70 trials, and detection improves over the current rule at every defect rate.

**The real masking risk, stated plainly.** A contract-invalid trial is never graded for judgment —
the grader returns before it looks. So a candidate that breaks the contract precisely when it is
about to be professionally wrong would have that wrongness absorbed as tier 2. Three containments,
all preregistered:

1. **Per-fixture cap of 2 in 7** — every fixture is judged on at least 5 gradeable trials. A
   fixture cannot qualify on a single observation of its judgment.
2. **Total ceiling of 6 in 70 (8.6%)** — set as the production-acceptable rate of outputs a
   consuming system must reject, not as a noise filter. It sits well above the observed 4.4%
   (2.6% chance of tripping on noise) and detects a systemic breakdown decisively (75% chance of
   tripping at a 12% rate).
3. **The tier map is frozen from the grader's own failure strings**, fixed in the preregistration
   before any output is seen, and covered by a regression test. It cannot be reinterpreted after a
   result is observed — the failure mode that would make this whole change a laundering device.

**Where the boundary was deliberately drawn tighter than convenience.** A first pass put
"`decision_basis` omitted a required ground" in tier 2 — the decision is right, only the record is
incomplete. Tested against history, that map **qualifies v0.8**, a gate carrying a real,
later-repaired knowledge gap. Nothing downstream catches an incomplete grounds record. It belongs
in **tier 1**. Tier 2 is exactly one thing: *the output is not a valid instance of the frozen
contract*, the class a JSON-Schema validator catches with certainty. With that boundary the
proposed rule fails both gates that carried real defects and passes only the one that did not.

**Tier 2 is not a free pass; it transfers an obligation.** It is sound only if the consuming system
actually validates every result against `result-v4.schema.json` and has defined behavior on failure
— reject, retry, or escalate, never proceed on a partial record. That becomes a stated production
requirement of qualification, not an assumption.

**A residual risk no criterion of this size can remove.** An intermittent judgment defect appearing
in 1 trial of 10 is detected 27% of the time at k=3, 52% at k=7, and would need ~300 trials
(~90 min, past the job cap) to reach 96%. No affordable gate closes this. It belongs to Phase 14
production incident learning, not to an ever-larger pre-release gate. Qualification should say so
rather than imply a coverage it does not have.

**Disclosed against my own recommendation:** under the proposed rule, v1.0's observed ledger would
have passed. That is exactly why it must not be applied to v1.0. The rule was derived from
production-detectability and validated against all three gates before its effect on v1.0 was used
as an argument — but a criterion that changes a verdict must earn that verdict on a seed it has
never seen.

## 6. Criterion to preregister for the next independent gate

```
trials_per_fixture        7            (10 fixtures, 5 families, 70 trials)
retries_permitted         0            no best-of-N, every trial recorded
seed                      new, unused  (20260827-31 and 999999 are burned)
candidate / instrument    unchanged and frozen before the seed is drawn

TIER 1 — professional judgment. Zero tolerance across all 70 trials.
  Every grader failure EXCEPT those named in tier 2. Includes: wrong action, wrong
  target or scope, causal status or claim ceiling unsupported or understated, claim
  scope unavailable, decisive metric not defensible, scale_readiness state or reasons
  wrong, SCALE without ELIGIBLE, internal inconsistency, wrong or missing computation,
  a claimed ground the case does not support, and an omitted ground actually used.
  Any single tier-1 failure -> GATE FAIL.

TIER 2 — output not a valid instance of the frozen contract. Bounded.
  Exactly: parse failure, and grader failures prefixed "output contract violation at".
  <= 2 per fixture  (every fixture judged on >= 5 gradeable trials)
  <= 6 of 70 total  (8.6% ceiling; a production-acceptable reject rate, not noise slack)
  Either cap exceeded -> GATE FAIL.

Reported regardless of verdict: per-family pass rate, tier-1 count, tier-2 rate with
its Wilson interval, and the full per-trial ledger.

Frozen with the seed: this criterion and its tier map. Neither may be revisited after
any result is observed.
```

Qualification on this criterion licenses a bounded claim, and the preregistration should say so:
*on held-out cases from five construct families, on one model family, judgment correct on every
graded trial, with a contract-validity rate whose lower confidence bound the consuming system's
validation must absorb.* It is not a claim about rare intermittent behavior, other providers, or
families not generated.

## 7. Verdict

**CHANGE.** Not because v1.0 nearly passed — under the current rule v1.0 failed and that verdict
stands — but because the current rule rejects sound candidates 74.4% of the time, achieves a
discrimination ratio of 1.2×, and cannot distinguish the world we are in from the world in which
nothing is wrong. Two of its three FAILs are more likely than not to have been noise.

The cheaper option, two-tier at k=5 (50 trials, ~15 min, 7.4% false-reject, 11.9×), is defensible
if the budget matters. k=7 is better on both axes and costs six minutes more.

| | trials | wall | input tokens | false-reject | detect q=0.33 |
| --- | ---: | ---: | ---: | ---: | ---: |
| current | 30 | ~9 min | ~303k | 74.4% | 91.2% |
| proposed k=5 | 50 | ~15 min | ~505k | 7.4% | 87.5% |
| **proposed k=7** | **70** | **~21 min** | **~707k** | **5.4%** | **94.3%** |

Wall time measured at 17.9 s/trial on run 33244861553; token counts from the measured 40,392-char
injected assembly. Both proposals sit inside the 60-minute job cap. Per Phase 6A, the Gemini
free-tier request and token-per-minute limits must be **verified live against account evidence**
before committing to k=7 — they are volatile and are not asserted here from memory. If the tier
holds 70 calls at 3-second pacing the run is unchanged in shape; if it does not, k=5 is the
fallback, not a relaxation of the criterion.
