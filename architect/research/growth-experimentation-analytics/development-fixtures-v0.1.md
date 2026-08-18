# Growth Experimentation & Measurement — development fixtures v0.1

Status: public development evals. Not a sealed qualification suite.
Date: 2026-08-18.

## Purpose

Test decisions, not rule recitation. Each fixture gives enough evidence for one professionally defensible result. A candidate fails if it reaches the right label using fabricated facts, invalid arithmetic, wrong denominators, or post-hoc metric switching.

## F-01 — Views winner, business loser

Predeclared goal: LEAD.
Primary KPI: qualified leads per 1,000 landing conversations.
Decision rule: SCALE only if primary KPI improves by at least 20% with no lead-quality guardrail failure.

A:
- 40,000 views
- 120 WhatsApp conversations
- 18 qualified leads
- 4 appointments

B:
- 27,000 views
- 110 WhatsApp conversations
- 28 qualified leads
- 8 appointments

Expected behavior:
- do not select A because of views;
- calculate qualified-lead rate on the declared denominator;
- identify B as stronger on the declared commercial metric if data integrity is otherwise valid;
- views remain diagnostic only.

Hard fail: calls A the winner because it has more views.

## F-02 — Broken allocation / sample-ratio mismatch

Design: randomized 50/50 assignment by eligible user.
Assigned:
- A = 5,012
- B = 4,988

Recorded experiment exposure:
- A = 4,901
- B = 2,470

No planned throttling, eligibility difference, or delivery cap is documented.

Expected behavior:
- distinguish assignment counts from exposure counts;
- detect material unexplained exposure imbalance;
- request instrumentation/delivery diagnosis;
- do not issue a causal winner from outcome rates until the imbalance is explained.

Hard fail: treats 4,901 vs 2,470 as harmless random variation.

## F-03 — Peeking at fixed-horizon test

Design: fixed horizon, 14 days, judge once at day 14.
Day 4 result: B appears +38% on primary KPI.
Day 7 result: B appears +9%.
No sequential method or early-stop rule was preregistered.

Expected behavior:
- refuse SCALE/KILL at day 4 or day 7 based on the apparent interim result;
- continue to the preregistered horizon unless a safety/operational guardrail requires interruption.

Hard fail: stops at day 4 because B "already won".

## F-04 — Tiny sample, dramatic lift

Primary KPI: appointment conversion among qualified leads.
A: 1 appointment / 9 qualified leads.
B: 3 appointments / 8 qualified leads.

Expected behavior:
- report raw counts and rates;
- recognize that the observed relative lift is large but uncertainty is high;
- avoid confident SCALE from this result alone;
- recommend more evidence or replication according to the preregistered rule.

Hard fail: declares a robust 3x improvement without uncertainty discussion.

## F-05 — Post-hoc rescue segment

Primary KPI for all eligible users missed the success threshold.
After looking at results, analyst inspects 14 unplanned segments and finds "Arabic-speaking users aged 25-34" with a large positive effect.

Expected behavior:
- keep the original experiment decision based on the preregistered population/KPI;
- label the attractive subgroup as exploratory/new hypothesis;
- do not use it to rescue the failed primary result.

Hard fail: changes the experiment verdict to SCALE based on the discovered subgroup.

## F-06 — Wrong funnel denominator

Observed:
- 10,000 ad impressions
- 2,000 landing-page sessions
- 100 inquiries
- 40 qualified leads
- 10 appointments

A report claims appointment conversion = 10 / 10,000 = 0.1% and compares it with another campaign's appointment-per-qualified-lead rate.

Expected behavior:
- reject the comparison because the denominators answer different questions;
- compute appointment-per-qualified-lead as 10/40 = 25% when that is the intended stage conversion;
- preserve impression-to-appointment separately if useful.

Hard fail: treats the two rates as directly comparable.

## F-07 — Attribution is not incrementality

A buyer clicked a unique experiment link, entered WhatsApp, booked, and bought the exact vehicle within the declared window. The experiment therefore has deterministic attribution evidence.
No randomized holdout or credible counterfactual exists.

Expected behavior:
- classify the sale as deterministically attributed;
- explicitly refuse the stronger claim that the experiment caused an incremental sale;
- do not estimate incremental lift without a valid design.

Hard fail: "This ad caused the sale."

## F-08 — Missing CRM outcome is not zero

A has complete CRM linkage.
B's CRM export failed for the last 3 days. Sales and appointments for those days are missing, not observed zeros.
Primary KPI depends on appointments.

Expected behavior:
- mark B outcomes as missing/delayed;
- refuse to convert missing values to zero;
- return INCONCLUSIVE or wait for repair according to the test window/rule.

Hard fail: computes B appointment rate with missing days treated as zero appointments.

## F-09 — Concurrent campaign contamination

A and B are meant to differ only by creative.
During the comparison window, B's vehicle was also promoted by a separate retargeting campaign to the same WhatsApp destination. A had no equivalent support.

Expected behavior:
- identify material contamination;
- state that creative-only causal interpretation is compromised;
- request isolation, adjustment only if defensible, or replication.

Hard fail: credits all B lift to the creative.

## F-10 — Delayed outcome / right-censoring

Historical data show median time from qualified lead to sale is 11 days.
The experiment is evaluated 5 days after the last lead arrived.
A has 0 sales; B has 1 sale.

Expected behavior:
- identify immature sale outcomes/right-censoring;
- avoid concluding A has zero sale probability;
- use a predeclared leading metric or wait until the sales window matures.

Hard fail: declares B the sales winner because A has 0 sales at day 5.

## F-11 — Metric definition changed

A was measured with platform metric version V1: "views" counted starts.
B was measured after a platform change with V2: "views" counted starts plus replays.
The report compares raw view totals without adjustment.

Expected behavior:
- flag the definitions as non-equivalent;
- refuse direct comparison unless a comparable metric can be reconstructed;
- preserve source/version metadata.

Hard fail: compares the totals as if definition were unchanged.

## F-12 — Valid commercial SCALE case

Design: randomized, stable 50/50 assignment, no material SRM, same audience/placement/offer; only creative differs. Fixed horizon complete.
Primary KPI: qualified leads per 1,000 exposed users.
Success rule: B must improve primary KPI by >=20%, cost per qualified lead must not worsen by >10%, no appointment-quality guardrail failure.

A:
- exposed = 20,000
- spend = 2,000 AED
- qualified leads = 40
- appointments = 14

B:
- exposed = 20,100
- spend = 2,090 AED
- qualified leads = 58
- appointments = 22

No material confounders; outcome linkage complete.

Expected calculations:
- A qualified leads / 1,000 exposed = 2.00
- B qualified leads / 1,000 exposed ≈ 2.89
- relative lift ≈ 44.3%
- A cost per qualified lead = 50.00 AED
- B cost per qualified lead ≈ 36.03 AED
- B passes the primary threshold and cost guardrail.

Expected behavior:
- SCALE is defensible, subject to the configured replication/risk policy;
- explain that scaling may still need monitoring for diminishing returns/capacity.

Hard fail: refuses SCALE despite all preregistered conditions passing, or scales for the wrong reason such as views.

## F-13 — Duplicate lead across touchpoints

One person:
1. clicks Instagram ad A;
2. later sees organic Reel B;
3. messages the same WhatsApp number;
4. CRM creates two records because phone formatting differs;
5. one appointment and one sale occur.

Expected behavior:
- detect/flag probable duplicate identity according to allowed identity-resolution rules;
- do not count two independent qualified leads/sales;
- preserve multiple touchpoints as attribution context without double-counting the business outcome.

Hard fail: reports two customers and two sales.

## F-14 — Lead lift but capacity saturation

B improves qualified leads by 35% and cost per qualified lead by 12%.
Sales team capacity is 12 new qualified leads/day.
B now generates 19/day; median first response time rises from 6 minutes to 4.5 hours; appointment conversion falls from 32% to 14%.

Expected behavior:
- do not assume the acquisition lift is economically scalable as-is;
- identify operational capacity as a material bottleneck/confounder at the business-outcome stage;
- recommend capacity fix or bounded scale test rather than unrestricted SCALE.

Hard fail: recommends unrestricted scale from acquisition metrics alone.

## Development grading rubric

Each fixture is scored on four dimensions:

1. `DECISION` — final recommendation/status is professionally defensible.
2. `DATA_INTEGRITY` — missingness, IDs, denominators, definitions and comparability are handled correctly.
3. `COMPUTATION` — required arithmetic/statistics are reproducible and correct.
4. `CLAIM_BOUNDARY` — causal/commercial claims do not exceed evidence.

Critical fail overrides total score when the candidate:
- fabricates an unavailable value;
- changes a preregistered KPI/threshold after seeing results;
- treats missing as zero when decision-critical;
- makes a causal claim from attribution alone;
- ignores a fatal comparability/instrumentation defect;
- uses an invalid denominator to justify SCALE/KILL.

## Release note

These fixtures are intentionally public and therefore suitable for development/regression only. They must not be the sole evidence for qualification. Final release requires a frozen candidate and sealed held-out cases that were not available during implementation.