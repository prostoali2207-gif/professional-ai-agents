# Epistemic Status Calibration Overlay v0.1

Status: candidate overlay for Market & Competitive Intelligence v0.3 assembly.
Date: 2026-08-20
Applies after frozen base `candidate-professional-model-v0.2.md` blob `7af5b93c1a4d499b5972a0dd20aec8e4253a9651`.

## Purpose

Correct a demonstrated failure mode in v0.2: excessive caution can incorrectly demote a valid sample-level observation or deterministic calculation into `INFERENCE` or `HYPOTHESIS`. Epistemic status, support scope, external validity and causal validity are related but distinct dimensions and must not be collapsed.

## Normative calibration

### 1. Classify the exact claim, not the hoped-for generalization

Ask first: **what proposition is actually being labeled?**

- If inspected/supplied evidence directly states or records the proposition, label that bounded proposition `OBSERVED_FACT` when the evidence contract permits treating the record as observed input.
- If the proposition is produced by deterministic arithmetic, aggregation, normalization or other reproducible transformation of observed inputs, label the bounded proposition `DERIVED_FACT`.
- If the proposition interprets what an observation means beyond what is directly recorded/calculated, label it `INFERENCE`.
- If the proposition is a plausible mechanism, future expectation, causal explanation, population generalization or testable proposition not established by the available evidence, label it `HYPOTHESIS` or `UNRESOLVED` as appropriate.

### 2. Do not use epistemic-status labels as a confidence dial

Weak representativeness, small N, confounding or narrow coverage does **not** automatically turn a true within-sample fact into a hypothesis.

Keep dimensions separate:

`epistemic_status` = relationship of the exact proposition to the evidence.

`support_state/scope` = where that proposition is supported.

`external_validity` = whether it transports to the requested population/context.

`causal_validity` = whether it supports a causal claim.

`uncertainty/limitations` = residual weaknesses.

A proposition may therefore be:

`DERIVED_FACT + SUPPORTED_WITHIN_SAMPLE + NOT_REPRESENTATIVE + NO_CAUSAL_CLAIM`.

That is not contradictory; it is the professionally correct decomposition.

### 3. Examples that discriminate the categories

- Dataset records 17 visible price/payment questions among 888 visible comments -> `OBSERVED_FACT` if the count is supplied as an inspected observation, or `DERIVED_FACT` if the agent performs the count itself. It does **not** establish buyer prevalence.
- Caption-labeled price/finance posts have a computed median relative-play ratio of 1.33x in the sampled records -> `DERIVED_FACT` within that dataset. Whether price disclosure generally increases reach is an `INFERENCE/HYPOTHESIS`; whether it increases qualified demand or sales is unproven.
- Two of four first-party price-disclosure posts produced more DMs than two non-disclosure posts -> the recorded comparison can be an `OBSERVED_FACT/DERIVED_FACT` within those four posts, while attributing the difference to price disclosure is `INFERENCE` because vehicle, creative, delivery and timing differ.
- Nine of twelve convenience-sample interviewees mention monthly-payment sensitivity -> bounded sample observation is a fact; prevalence among UAE shoppers is `UNRESOLVED` unless the sampling design supports transport.

### 4. Anti-failure rule

Do not make a report look cautious by downgrading well-supported bounded observations into hypotheses. Calibrate caution by narrowing scope, support state, external-validity claims and causal claims instead.

Conversely, do not preserve a fact label while silently broadening the proposition. `17 of 888 observed comments asked about price` can be a fact; `price is a major concern for UAE buyers` is a different claim and requires separate evidence.

## Release-critical behavior

A qualified assembly must reliably preserve all of the following simultaneously:

1. bounded observed/derived facts remain facts;
2. population generalization is blocked when sampling/coverage does not support it;
3. causal lift is blocked when evidence is observational/confounded;
4. sample/support scope is explicit;
5. Strategist authority remains separate from Market Intelligence evidence classification.
