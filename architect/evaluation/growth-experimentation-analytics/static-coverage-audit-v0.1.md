# Analytics public-fixture static coverage audit v0.1

Status: static audit only; NOT a behavioral run and NOT qualification evidence.
Date: 2026-08-18.
Candidate inspected: `prostoali2207-gif/auto-sales-growth-system/agents/analytics.md` (current main at audit time).

## Purpose

Before paying for or manually executing a model runtime, compare the current Analytics instructions against the 14 public development fixtures. This answers only: "Does the written agent explicitly contain rules that should support the desired behavior?" It does NOT answer: "Will a model actually execute those rules correctly?"

## Summary

- Strongly covered by explicit current rules: F-01, F-03, F-05, F-06, F-07, F-08, F-09, F-11.
- Partially covered / execution risk remains: F-04, F-10, F-13, F-14.
- Material written gap: F-02 (explicit randomized allocation/SRM diagnosis).
- Written rules appear sufficient for F-12 at a policy level, but reproducible calculation/tool execution remains unproven.

Therefore the current candidate must NOT be marked PASS. The likely remediation target is focused, not a wholesale rewrite.

## Fixture-by-fixture assessment

| Fixture | Static status | Why |
|---|---|---|
| F-01 Views winner, business loser | STRONG | Agent explicitly freezes the primary KPI, treats views as diagnostic for LEAD/DIRECT_SALE, and says a rise in messages with falling qualified rate is not automatically a win. |
| F-02 Broken allocation / exposure imbalance | GAP | Agent prefers randomized concurrent controls and checks comparability, but does not define an explicit assignment-vs-exposure diagnostic, expected allocation test, or sample-ratio mismatch procedure. A model may notice the imbalance, but the written behavior is not reliably specified. |
| F-03 Peeking at fixed horizon | STRONG | Explicit rule: fixed-horizon test is judged at preregistered sample/window; repeated peeking must not trigger SCALE/KILL; early stopping only under preregistered sequential method or guardrail. |
| F-04 Tiny sample, dramatic lift | PARTIAL | Agent explicitly requires counts, uncertainty, sparse binary methods and allows INCONCLUSIVE. Missing piece is a reproducible computation/power contract; correct caution is specified, quantitative execution is not proven. |
| F-05 Post-hoc rescue segment | STRONG | Explicitly says secondary metrics cannot rescue failed primary KPI and post-hoc segments are new hypotheses. |
| F-06 Wrong funnel denominator | STRONG | Explicitly forbids denominators from different populations and gives the same conceptual example. Arithmetic itself is simple but still requires runtime/tool verification. |
| F-07 Attribution is not incrementality | STRONG | Explicitly states deterministic attribution does not prove incrementality and forbids causal overclaim. |
| F-08 Missing CRM outcome is not zero | STRONG | Explicit availability states plus repeated MUST NOT treat unknown/missing as zero. |
| F-09 Concurrent campaign contamination | STRONG | Concurrent campaign touching same audience/vehicle is explicitly on confounder checklist; material/fatal confounders block SCALE. |
| F-10 Delayed outcome / right-censoring | PARTIAL | Agent warns that zero sales from tiny samples does not establish zero probability and records delayed data states, but does not explicitly define outcome maturity/right-censoring logic from historical conversion lag. |
| F-11 Metric definition changed | STRONG | Explicit rule: do not silently compare changed metric definitions; record version/source. |
| F-12 Valid commercial SCALE case | POLICY-STRONG / EXECUTION-UNPROVEN | SCALE rules match fixture: horizon complete, threshold passes, guardrails pass, no material confounder, practical relevance. However the current agent has no proven deterministic calculation toolchain, so numeric correctness remains unqualified. |
| F-13 Duplicate lead across touchpoints | PARTIAL | Agent preserves person/lead/touchpoint IDs and classifies duplicates, but identity-resolution/deduplication procedure is not explicit enough to guarantee one-customer/one-sale counting under formatting variants. |
| F-14 Capacity saturation | PARTIAL | Appointment capacity and response-time confounding are listed, and SCALE requires practical executability. But there is no explicit commercial scaling/capacity gate describing when acquisition lift must be bounded rather than scaled. |

## Focused remediation required before candidate freeze

1. Add an explicit randomization/allocation integrity check: assignment counts, exposure counts, expected allocation, material unexplained imbalance, and causal-blocking behavior.
2. Add outcome-maturity handling: if downstream outcomes have known lag, distinguish observed zero from not-yet-mature outcome and delay/limit the decision.
3. Add explicit deduplication/identity-resolution decision rules for one person across multiple CRM/touchpoint records.
4. Add a scaling-capacity/economic gate: acquisition improvement alone is insufficient when response capacity or downstream conversion materially deteriorates.
5. Bind required quantitative checks to a reproducible computation interface rather than unsupported narrative arithmetic.

## What must NOT happen

- Do not claim that this audit means the current Analytics "passed 14 tests".
- Do not update the public fixture answers to match the current agent.
- Do not create sealed held-out fixtures yet; the candidate is not frozen.
- Do not rewrite the entire Analytics agent when the observed written gaps are localized.

## Next gate

Create a focused candidate revision that closes the listed gaps while preserving existing strong rules. Then freeze that candidate version and run actual behavioral development fixtures through a model/runtime (manual Claude/Gemini is acceptable for development). Only after development behavior is stable should a fresh sealed held-out qualification fixture be created.