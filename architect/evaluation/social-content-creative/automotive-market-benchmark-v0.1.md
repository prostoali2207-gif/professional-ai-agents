# Social Content Creative — External Automotive Market Benchmark v0.1

Status: preregistered design. No benchmark verdict has been earned.

## Purpose

Evaluate `social-content-creative` 0.1.0 against strong real automotive/dealership short-form market work without claiming paid expert validation.

This benchmark is a **T1-strengthening external evidence layer**, not T2 `EXPERT-VALIDATED`.

The question is:

> When the candidate and strong market references are judged on the same communication problem and production constraints, is the candidate materially competitive on professional creative decisions, or is it safer, more generic, weaker, or less executable?

## Why this benchmark exists

The existing qualification can detect many professional failures, but it is still partly self-referential: AI-designed constructs and AI/model graders can agree with one another while missing what the market rewards.

Real market work introduces an independent external constraint.

However, raw virality is not professional ground truth. Views can be driven by account size, hypercar novelty, celebrity/personality, paid distribution, trend audio, production budget, geography, or platform timing. The benchmark therefore compares mechanisms and normalized evidence rather than rewarding raw view count.

## Frozen candidate

- core: `social-content-creative`
- version: `0.1.0`
- artifact digest: `sha256:ce5f537d336e6a6396f47c1ae492a687c4dc4b30ade8ab37bb4abb94d6251c0f`
- lifecycle/trust ceiling before this benchmark: `qualified / T1`

Any behavior-relevant change before scored execution requires a new frozen target.

## Benchmark cohorts

### A — Comparable dealer / low-production work

Highest decision weight.

Include ordinary dealerships and small/medium accounts where the concept must do meaningful work without exotic-car novelty or major production.

Prefer:
- phone/small-team production;
- one salesperson or no talent;
- ordinary/used inventory;
- clear offer, information, comparison, utility, humor or buyer tension;
- observable public performance where available.

### B — UAE/GCC relevance

High decision weight when the task is for Al Musafir / UAE deployment.

Include local market formats and buyer contexts such as:
- AED pricing/installments;
- showroom/stock availability;
- local buyer questions;
- used-car trust/condition;
- UAE-specific offers.

Do not let GCC luxury-showroom novelty stand in for comparable creative quality.

### C — Creative-format exemplars

Use to test whether the candidate can discover a strong mechanism rather than produce generic inventory presentation.

Examples:
- comparison/test;
- POV/sketch;
- buyer myth or negotiation tension;
- hidden feature / utility;
- challenge/game;
- sensory/ASMR;
- transformation;
- price/budget anchor;
- interactive choice.

### D — Viral/outlier references

Lower direct comparison weight.

Examples include VIP Motors / F1rst Motors and extreme viral dealership clips.

Use these to learn:
- hook mechanisms;
- visual curiosity;
- interaction patterns;
- pacing;
- novelty.

Do **not** use their raw reach as the candidate threshold.

### E — Ordinary/weak controls

Include some market work that is merely average or weak.

Purpose:
- confirm the grader does not automatically prefer anything labeled "real market";
- test whether the candidate can clearly beat generic listing-style creative.

## Confounder controls

Every reference must be tagged for:

- follower count when available;
- raw views/engagement when available;
- account-size class;
- vehicle novelty: ordinary / premium / exotic / hypercar;
- paid distribution: known / possible / no evidence;
- celebrity/personality dependence;
- trend dependence;
- music/audio dependence;
- production complexity;
- geography;
- sales objective;
- recency/source freshness;
- whether outcome is reach-only or has downstream lead/sales evidence.

### Music rule

Music/trending audio is not a required capability in this benchmark.

If a reference benefits from music, judge separately:

1. underlying concept;
2. visual hook;
3. information/payoff;
4. edit/pacing mechanism;
5. whether the concept still works with permissible non-music sound design, speech, natural sound or silence.

Never fail the candidate for refusing to use music.

## Performance normalization

Raw views are descriptive evidence, not the score.

When follower count is available, record a simple breakout ratio:

`public views / public follower count`

Use it only as one signal. It does not prove causality or quality.

Also consider:
- engagement relative to the account's own norm when available;
- unusually strong performance versus adjacent posts;
- repeated format success;
- downstream visits/leads where official case-study evidence exists.

## Task construction

Build tasks from market mechanisms, not by copying exact public scripts.

For each selected reference:

1. identify the communication problem;
2. identify the creative mechanism;
3. strip brand-specific wording and superficial style;
4. construct a fresh but comparable automotive brief;
5. preserve realistic constraints;
6. ask the candidate for exact concept/hook/script/shot plan;
7. compare against the market reference mechanism and independent alternative references.

Do not expose the reference to the candidate before generation.

## Core scored dimensions

Score each candidate/reference pair on observable evidence:

1. **Scroll-stop / hook**
   - Is the premise understandable immediately?
   - Does the first beat create relevant curiosity/stakes?

2. **Concept strength**
   - Is there an actual mechanism, not just "show the car nicely"?

3. **Distinctiveness**
   - Is it predictable/generic versus meaningfully specific?

4. **Payoff**
   - Does the content deliver what the hook promised?

5. **Sales relevance**
   - Does it reduce buyer uncertainty, create desire, frame value, or create a proportionate next step?

6. **Truthfulness**
   - Are claims supportable and uncertainty handled correctly?

7. **Visual storytelling**
   - Does the concept translate into concrete visible beats?

8. **Shootability**
   - Can a small dealership team execute it with available vehicle/location/phone?

9. **Proportionate boldness**
   - Does the candidate take a justified creative risk when useful, or retreat into safe/generic copy?

10. **Platform-native feel**
   - Does it behave like short-form social rather than a brochure or generic ad?

11. **Selection judgment**
   - Given the candidate and market reference, which would a neutral reviewer choose for the stated objective, and why?

## Blind comparison protocol

Where possible:

- hide which side is "candidate" versus "market";
- remove follower/view counts during qualitative judging;
- remove account names;
- normalize transcript formatting;
- evaluate concept/script/shot logic separately from production polish;
- reveal performance evidence only after the qualitative judgment.

This prevents popularity and production value from becoming circular proof.

## Grader structure

Use at least two independent AI/model judges if available, plus deterministic checks for truth/constraints.

The judges must not receive the desired verdict.

For material disagreements:
- do not average blindly;
- inspect the criterion and evidence;
- classify as candidate weakness, reference weakness, grader bias, or legitimate creative disagreement.

This is still AI judging and therefore cannot support T2.

## Preregistered outcome logic

A candidate cannot PASS solely on aggregate score.

Return `MARKET_BENCHMARK_REVISE` or `FAIL` if there is a repeated material pattern such as:

- generic/safe concepts losing to strong comparable references;
- hooks that are consistently slower/weaker;
- weak payoff;
- brochure-like outputs;
- poor shootability;
- inability to challenge a bad user premise;
- unsupported claims;
- copying superficial market style without understanding the mechanism.

A few outlier losses to hypercar/celebrity/large-budget content do not count as professional failure.

PASS requires:
- no P0/P1 integrity/truth/brief failures;
- candidate is competitive with comparable low-production references across the majority of relevant tasks;
- no repeated "substantive correction needed" pattern;
- no systematic excessive-caution/genericity pattern;
- candidate wins or is professionally defensible on at least some difficult/creative tasks, rather than merely avoiding failure.

A numeric percentage threshold must be frozen only after the final task/reference set is assembled and the distribution is inspected. Do not invent a convenient number now.

## Verdicts

- `MARKET_BENCHMARK_PASS`
- `MARKET_BENCHMARK_REVISE`
- `MARKET_BENCHMARK_FAIL`
- `NOT_EXECUTABLE`

## Trust claim boundary

Even `MARKET_BENCHMARK_PASS` means only:

> The T1-qualified candidate demonstrated competitive performance against the frozen external automotive short-form reference set under the recorded comparison protocol.

It does **not** mean:
- T2 Expert-Validated;
- top human professional;
- safe blind autonomy;
- production-proven.

## Red-team

Senior practitioner:
- Are we rewarding virality instead of transferable judgment?
- Are hypercars/large audiences making weak creative look strong?

Educator/assessor:
- Are the fresh tasks construct-equivalent to the market reference without leaking the answer?

Hiring manager:
- Would repeated benchmark wins translate to useful dealership work, or only test imitation?

Evaluation scientist:
- Are view counts, follower counts, paid distribution and selection bias being handled honestly?

Creative director:
- Is the candidate bold enough, or does truth/safety discipline collapse into blandness?

Material gaps must be repaired before scored execution.
