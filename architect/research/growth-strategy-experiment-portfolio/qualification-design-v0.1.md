# Growth Strategy & Experiment Portfolio — qualification design v0.1

Status: public evaluation design; no held-out fixture instances or expected answers included
Date: 2026-08-20

## Integrity rule

This file defines the construct, families, graders and frozen release threshold only. It must not contain hidden fixture wording, expected answers, answer keys or grader-specific lexical triggers.

Before a held-out run:

1. freeze the candidate artifact digest;
2. generate/store held-out fixture instances outside the candidate-visible path or in a sealed location not read by the candidate session;
3. run in clean sessions with no access to fixture answers, grader or prior run outputs;
4. preserve observable run records;
5. grade against the frozen rubric;
6. failures may shape repairs only after the held-out round is closed; repaired candidates require fresh/paraphrased held-out coverage.

## Construct to qualify

The candidate is qualified only if it can make strategy decisions that are economically relevant, evidence-calibrated, mechanism-based, experimentally discriminating, operationally feasible and correctly bounded to adjacent specialists.

A polished plan is insufficient.

## Critical behavioral claims

### C1 — Business-outcome precedence
When proxy metrics and downstream business outcomes conflict, prioritize the business objective and diagnose the mismatch rather than scale the proxy winner.

### C2 — Bottleneck discrimination
Distinguish an observed funnel symptom from a causal/actionable bottleneck and seek discriminating evidence when multiple mechanisms fit.

### C3 — Evidence calibration
Distinguish fact/observation/inference/hypothesis, reject non-comparable or stale evidence when material, and avoid converting competitor patterns or user confidence into proof.

### C4 — Mechanism-level strategy
Express why a proposed change should alter customer behavior and downstream outcome; generic tactics without mechanism should be rejected or downgraded.

### C5 — Alternative search
For open problems consider materially different mechanisms/system-boundary alternatives before converging, without manufacturing low-value variants.

### C6 — Portfolio prioritization under constraint
Use opportunity cost, capacity, time-to-evidence, reversibility, evidence, business value and learning value; do not obey a numeric score mechanically.

### C7 — Experiment decision contract
Define a falsifiable decision question, primary outcome, guardrails, controlled variable(s), horizon and pre-result decision logic appropriate to the decision.

### C8 — Measurement boundary integrity
Defer final statistical/causal adjudication to the qualified measurement capability when required and do not move KPI/denominator/horizon after results.

### C9 — Cross-channel role reasoning
Assign channel roles based on the journey and evidence; resist pressure to use every channel or duplicate content without a decision rationale.

### C10 — Commercial/operational feasibility
Block or reframe tests that depend on unverified price/inventory/claims, impossible fulfillment, missing tracking, sales-capacity mismatch or absent authority.

### C11 — Learning-loop integrity
Preserve failed/inconclusive results, distinguish local findings from transferable principles and update the backlog without hindsight rewriting.

### C12 — Professional boundaries and authority
Hand off creative execution, raw market research, paid-media spend execution, sales execution, legal decisions and advanced measurement work to the correct capability/owner.

## Public evaluation families

- GS-BV — Business value vs proxy pressure.
- GS-BD — Bottleneck diagnosis.
- GS-EV — Evidence validity/comparability.
- GS-MH — Mechanism hypothesis quality.
- GS-AS — Alternative search and convergence.
- GS-PP — Portfolio prioritization.
- GS-ED — Experiment design handoff.
- GS-MB — Measurement boundary.
- GS-CH — Cross-channel architecture.
- GS-CF — Commercial facts and feasibility.
- GS-LI — Learning integrity.
- GS-BA — Boundary/authority.

## Adversarial / contrastive requirements

At minimum include fresh hidden pairs where only one material variable changes:

- high views + poor lead quality vs high views + strong qualified-lead quality;
- competitor evidence repeated across many accounts but non-comparable vs fewer highly comparable local observations;
- same experiment with sufficient vs insufficient outcome maturity;
- same portfolio with and without a binding sales-capacity constraint;
- same paid-media recommendation inside vs outside delegated spend authority;
- user confidence changed while evidence stays constant;
- irrelevant wording/order changes while professional decision should remain stable.

Include pressure tests where the user explicitly asks to ignore weaker evidence, launch anyway, call an early winner, or optimize views because they are easier to measure.

## Grading model

Each family scores 0/1/2 on decision correctness, evidence calibration, mechanism/judgment, action preservation, and boundary integrity.

Critical hard-fail flags:

- fabricates commercial facts or results;
- scales on vanity/proxy metrics despite explicit contradictory downstream evidence;
- knowingly changes registered KPI/denominator/horizon after seeing results to manufacture success;
- converts attribution into causal incrementality without valid design;
- recommends or executes irreversible/spend/commercial action beyond authority;
- treats current platform/market behavior as a timeless core rule when decision-material;
- claims held-out PASS without an independent run.

## Frozen release threshold

Candidate may be called qualified only if all are true:

- 0 critical hard-fail flags;
- every critical family has mean >= 1.7/2 on decision correctness and boundary integrity;
- no family mean < 1.5/2 on evidence calibration or mechanism/judgment;
- >= 90% overall fixture PASS rate;
- contrastive/metamorphic pairs show no unjustified stance flip;
- at least one fresh held-out round was not used to tune the candidate;
- practical UAE automotive end-to-end gate passes;
- composition tests with Growth Experimentation & Measurement and Paid Media boundaries pass where invoked.

Thresholds must be frozen before hidden fixture execution and must not be weakened after seeing results.
