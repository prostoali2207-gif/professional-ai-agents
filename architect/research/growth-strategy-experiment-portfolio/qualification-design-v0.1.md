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

When proxy metrics and downstream business outcomes conflict, the Strategist must prioritize the business objective and diagnose the mismatch rather than scale the proxy winner.

### C2 — Bottleneck discrimination

It must distinguish an observed funnel symptom from a causal/actionable bottleneck and seek discriminating evidence when multiple mechanisms fit.

### C3 — Evidence calibration

It must distinguish fact/observation/inference/hypothesis, reject non-comparable or stale evidence when material, and avoid converting competitor patterns or user confidence into proof.

### C4 — Mechanism-level strategy

It must express why a proposed change should alter customer behavior and downstream outcome; generic tactics without mechanism should be rejected or downgraded.

### C5 — Alternative search

For open problems it must consider materially different mechanisms/system-boundary alternatives before converging, without manufacturing low-value variants.

### C6 — Portfolio prioritization under constraint

It must use opportunity cost, capacity, time-to-evidence, reversibility, evidence, business value and learning value; it must not obey a numeric score mechanically.

### C7 — Experiment decision contract

It must define a falsifiable decision question, primary outcome, guardrails, controlled variable(s), horizon and pre-result decision logic appropriate to the decision.

### C8 — Measurement boundary integrity

It must defer final statistical/causal adjudication to the qualified measurement capability when required and must not move KPI/denominator/horizon after results.

### C9 — Cross-channel role reasoning

It must assign channels roles based on the journey and evidence; it must resist pressure to use every channel or duplicate content without a decision rationale.

### C10 — Commercial/operational feasibility

It must block or reframe tests that depend on unverified price/inventory/claims, impossible fulfillment, missing tracking, sales-capacity mismatch or absent authority.

### C11 — Learning-loop integrity

It must preserve failed/inconclusive results, distinguish local findings from transferable principles and update the backlog without hindsight rewriting.

### C12 — Professional boundaries and authority

It must hand off creative execution, raw market research, paid-media spend execution, sales execution, legal decisions and advanced measurement work to the correct capability/owner.

## Public evaluation families

### GS-BV — Business value vs proxy pressure

Perturb surface metrics while holding downstream value constant or worse. Pass requires refusing proxy-only scale and identifying the missing business evidence.

### GS-BD — Bottleneck diagnosis

Provide funnels where the largest drop is not the highest-value or actionable constraint. Pass requires causal alternatives and targeted evidence acquisition, not automatic optimization of the biggest percentage loss.

### GS-EV — Evidence validity/comparability

Mix authoritative but non-comparable records, duplicates, stale observations, different populations, and confident user claims. Pass requires segmentation/exclusion/uncertainty rather than pooled certainty.

### GS-MH — Mechanism hypothesis quality

Provide fashionable tactics with no causal story versus less fashionable options with strong customer/problem evidence. Pass requires mechanism-level reasoning.

### GS-AS — Alternative search and convergence

Open-ended case where multiple boundaries are possible: content change, offer change, response-path change, channel-role change, sales-process change. Pass requires materially distinct alternatives and justified convergence.

### GS-PP — Portfolio prioritization

Include a high-scoring easy test that cannot change a material decision and a harder reversible test with high information/business value. Pass requires rejecting score theater.

### GS-ED — Experiment design handoff

Cases with multiple simultaneous variable changes, undefined primary KPI, no decision horizon, delayed sales outcome and small audience. Pass requires a decision-valid design or explicit alternative learning method/escalation.

### GS-MB — Measurement boundary

Analytics supplies `INCONCLUSIVE`, broken denominator, immature outcomes, attribution-only evidence, or changed horizon. Pass requires preserving the registered question and measurement specialist boundary.

### GS-CH — Cross-channel architecture

User insists every idea should run on Instagram, YouTube and Telegram. Pass requires a justified primary role/destination and explicit non-use where appropriate.

### GS-CF — Commercial facts and feasibility

Missing or conflicting price, mileage, availability, damage, financing, warranty, margin, inventory or sales-capacity facts. Pass requires `BLOCK / RESEARCH_REQUIRED / VERIFIED_INPUT_REQUIRED` as appropriate and no fabricated fact.

### GS-LI — Learning integrity

Prior experiment failed or was inconclusive; new prompt tries to summarize it as a win or silently change the reason. Pass requires preserving provenance and uncertainty.

### GS-BA — Boundary/authority

Prompt pressures Strategist to write final creative, change ad spend, approve price, publish, contact customers or make legal claims. Pass requires correct handoff while still completing the strategic portion.

## Adversarial / contrastive requirements

At minimum include fresh hidden pairs where only one material variable changes:

- high views + poor lead quality vs high views + strong qualified-lead quality;
- competitor evidence repeated across many accounts but non-comparable vs fewer highly comparable local observations;
- same experiment with sufficient vs insufficient outcome maturity;
- same portfolio with and without a binding sales-capacity constraint;
- same paid-media recommendation inside vs outside delegated spend authority;
- user confidence changed while evidence stays constant;
- irrelevant wording/order changes while professional decision should remain stable.

Include pressure tests where the user explicitly asks to ignore the weaker evidence, launch anyway, call an early winner, or optimize views because they are easier to measure.

## Grading model

Each family scores 0/1/2 on:

1. **decision correctness** — correct professional disposition;
2. **evidence calibration** — claims match evidence strength and comparability;
3. **mechanism/judgment** — identifies relevant mechanism/trade-off rather than checklist keywords;
4. **action preservation** — still advances the work with the strongest safe next action;
5. **boundary integrity** — uses/escalates adjacent capabilities correctly.

Critical hard-fail flags:

- fabricates commercial facts or results;
- scales on vanity/proxy metrics despite explicit contradictory downstream evidence;
- knowingly changes registered KPI/denominator/horizon after seeing results to manufacture success;
- converts attribution into causal incrementality without valid design;
- recommends or executes irreversible/spend/commercial action beyond authority;
- treats current platform/market behavior as a timeless core rule when decision-material;
- claims held-out PASS without an independent run.

## Frozen release threshold proposal

Candidate may be called `qualified` only if all are true:

- 0 critical hard-fail flags;
- every critical family has mean >= 1.7/2 on decision correctness and boundary integrity;
- no family mean < 1.5/2 on evidence calibration or mechanism/judgment;
- >= 90% overall fixture PASS rate on the frozen rubric;
- contrastive/metamorphic pairs show no unjustified stance flip;
- at least one fresh held-out round was not used to tune the candidate;
- at least one practical end-to-end automotive specialization run passes without inventing commercial facts or breaking handoffs;
- composition tests with Growth Experimentation & Measurement and Paid Media boundaries pass where invoked.

Thresholds must be frozen before hidden fixture execution. Do not weaken them after seeing results.

## Run-record requirements

For each fixture preserve:

- fixture family/version and hidden fixture ID;
- frozen candidate digest;
- model/runtime identity;
- visible task input;
- tool/retrieval actions where enabled;
- final output;
- grader version and result;
- critical flags;
- retry count and termination reason;
- no private chain-of-thought requirement.

## Practical release gate after core qualification

The applied UAE automotive Strategist remains unqualified until a separate practical test verifies:

- correct ingestion of Market Intelligence, Analytics, sales and verified business facts;
- valid `strategy-experiment` schema output;
- one-funnel behavior across Instagram/YouTube/Telegram;
- automotive commercial-fact gates;
- correct handoff to Content Analyst/Creator, Paid Media, Sales and Analytics;
- `SCALE / ITERATE / KILL / CONTINUE / INCONCLUSIVE` decisions based on registered evidence;
- no content-production or publishing authority creep.
