# Growth Experimentation & Measurement — competency matrix v0.1

Status: research/design artifact; not release-ready.
Date: 2026-08-18.
Parent audit: `profession-gap-audit-v0.1.md`.

## Purpose

Turn the profession audit into observable capabilities that can later be tested. A competency is not accepted because an agent says the right rule; it must make the correct decision on a realistic packet and show reproducible evidence where computation is required.

## Release-critical competency matrix

| ID | What the professional must actually do | Why it matters | Observable pass evidence | Failure signal | Current downstream state |
|---|---|---|---|---|---|
| EXP-01 | Check that the experiment actually compares the intended groups, unit, exposure window and locked variable | A clean-looking report is useless if A and B were not comparable | Identifies assignment/exposure mismatch and blocks or downgrades inference | Declares a winner without checking comparability | PARTIAL |
| EXP-02 | Detect broken allocation or instrumentation, including sample-ratio mismatch when randomization exists | Delivery or tracking bugs can create fake winners | Calculates expected vs observed allocation; distinguishes assignment from exposure; stops causal claim on unexplained material mismatch | Treats unequal counts as normal without diagnosis | GAP |
| EXP-03 | Respect fixed-horizon/sequential stopping rules | Repeated peeking inflates false positives | Refuses early winner declaration when fixed test is incomplete; permits only valid preregistered sequential logic | Stops when result first looks favorable | STRONG PROSE / UNQUALIFIED |
| EXP-04 | Judge whether the sample can answer the business question | Tiny samples can produce dramatic but meaningless lifts | Separates minimum useful business effect from detectable effect; marks underpowered design before/after run | Treats large percentage lift from tiny counts as proof | GAP |
| EXP-05 | Control multiple metrics, variants and post-hoc segments | Searching enough cuts will eventually find a fake win | Keeps primary metric fixed; labels post-hoc segments as new hypotheses; accounts for multiplicity where material | Rescues failed test with best-looking segment | PARTIAL |
| EXP-06 | Interpret effect size with uncertainty | Statistical significance alone is not commercial importance | Reports counts, denominators, effect magnitude and plausible range; distinguishes meaningful win/loss/uncertainty | Gives binary verdict from p-value or percentage alone | STRONG PROSE / UNQUALIFIED |
| CAU-01 | Bound causal claims | Attribution or correlation is not proof of incrementality | Uses causal language only when design supports it; explicitly states alternatives | Says an attributed sale was caused by the ad | STRONG PROSE / UNQUALIFIED |
| MET-01 | Preserve exact metric definitions, denominators and versions | Platform metrics with similar names are not interchangeable | Rejects comparison after incompatible definition change or repairs it with comparable data | Compares reach, plays, views or rates as if identical | STRONG / UNQUALIFIED |
| MET-02 | Judge whether the chosen metric represents business value | A metric can improve while sales economics worsen | Detects proxy failure and separates primary, guardrail and diagnostic metrics | Optimizes engagement despite worse qualified outcomes | GAP |
| DAT-01 | Distinguish zero, missing, delayed and invalid data | Missing CRM data can falsely look like zero conversions | Preserves state and refuses fabricated zeros | Converts missing outcomes to 0 | STRONG / UNQUALIFIED |
| DAT-02 | Verify joins, identity and duplicate handling | Bad joins can double-count leads or attach sales to wrong experiment | Reconciles IDs and flags ambiguous/double attribution | Counts duplicate person/events as independent outcomes | PARTIAL |
| DAT-03 | Detect selection, survivorship and censoring | Delayed sales and incomplete follow-up bias conclusions | Identifies immature outcomes/right-censoring and changes evaluation window/confidence accordingly | Calls no-sale while outcomes have not matured | GAP |
| ATT-01 | Separate deterministic, corroborated, assisted and unknown attribution | Different evidence supports different claims | Correctly classifies touchpoints and does not over-credit weak matches | Converts plausible exposure into deterministic attribution | STRONG / UNQUALIFIED |
| ATT-02 | Separate attribution from incrementality | Knowing source does not prove counterfactual effect | Explicitly prevents causal claim from attribution alone | Treats last-click as causal lift | STRONG / UNQUALIFIED |
| FUN-01 | Reconstruct funnel with correct populations | Wrong denominators create meaningless conversion rates | Uses eligible denominator at each stage and flags population mismatch | Divides outcomes by unrelated population | STRONG / UNQUALIFIED |
| FUN-02 | Measure lead quality and downstream commercial outcomes | More messages can mean worse business | Separates qualified/unqualified/spam/unknown and traces appointments/sales where available | Calls message volume a win despite quality collapse | STRONG AUTO DELTA / UNQUALIFIED |
| CON-01 | Find and grade confounders | Price, vehicle, placement or follow-up differences can explain apparent lift | Identifies direction and severity; blocks inference on fatal confounder | Mentions confounders but still declares winner | STRONG LIST / UNQUALIFIED |
| CON-02 | Detect contamination, carry-over and overlapping experiments | A and B may influence each other or share concurrent campaigns | Finds overlap and downgrades/isolation requirement | Assumes treatments are isolated without checking | GAP |
| ECO-01 | Decide whether an effect is economically scalable | Positive response can still destroy margin or fail under higher spend | Checks spend, cost per qualified outcome, margin/capacity where available; distinguishes effect from scalable economics | SCALE from engagement or raw lead lift alone | GAP |
| DEC-01 | Execute preregistered decision rule without moving goalposts | Post-hoc rule changes manufacture wins | Returns decision dictated by frozen rule or INCONCLUSIVE if rule cannot be evaluated | Changes KPI/threshold after seeing results | STRONG / UNQUALIFIED |
| DEC-02 | Use INCONCLUSIVE correctly | Forced winners create bad learning | Chooses INCONCLUSIVE for broken/weak evidence and says what would resolve it | Treats uncertainty as tie/failure/win | STRONG / UNQUALIFIED |
| DEC-03 | Require replication proportional to cost and uncertainty | One noisy win should not trigger expensive scale | Requests confirmation when downside/cost/causal uncertainty warrants it | Scales irreversible/high-cost change from weak first result | PARTIAL |
| TOOL-01 | Produce reproducible calculations | Narrative arithmetic cannot be audited | Emits inputs/formula/method/output or tool record for allocation, rates, intervals and required statistics | Unsupported numerical claim | BLOCKING GAP |
| GOV-01 | Preserve provenance and unknowns; never fabricate | Analytics is decision evidence | Every material result traces to source/window/definition; unavailable stays unavailable | Invented platform/CRM values | STRONG / UNQUALIFIED |
| GOV-02 | Minimize PII | Analytics should not expose customer content/identifiers unnecessarily | Uses privacy-safe IDs/classes and excludes raw personal data | Copies phone/message/document data into analytics output | PRESENT / UNQUALIFIED |

## Criticality tiers

### Tier 1 — must pass before the core can influence SCALE/KILL

`EXP-01, EXP-02, EXP-03, EXP-04, EXP-06, CAU-01, MET-01, DAT-01, DAT-02, DAT-03, ATT-02, FUN-01, CON-01, TOOL-01, DEC-01, DEC-02, GOV-01`

A failure in these can directly produce a false winner, false loser, or fabricated confidence.

### Tier 2 — required for production-quality commercial analysis

`EXP-05, MET-02, ATT-01, FUN-02, CON-02, ECO-01, DEC-03, GOV-02`

These affect commercial usefulness, scaling quality, privacy and robustness but can sometimes be explicitly bounded in a narrow deployment.

## Evaluation mapping

The development suite must contain discriminating fixtures, not questions asking the model to recite rules.

| Fixture | Competencies exercised | Required decision behavior |
|---|---|---|
| F-01 Views winner / qualified-lead loser | MET-02, FUN-02, DEC-01 | Do not call reach winner a business winner when LEAD is primary |
| F-02 Unequal randomized allocation | EXP-01, EXP-02, TOOL-01 | Calculate allocation diagnostic; block causal winner if unexplained material mismatch |
| F-03 Fixed test repeatedly peeked | EXP-03, DEC-01 | Refuse early favorable stop |
| F-04 1 vs 3 conversions from tiny samples | EXP-04, EXP-06 | Report uncertainty; no confident SCALE |
| F-05 Attractive post-hoc subgroup | EXP-05, DEC-01 | Treat as new hypothesis, not rescue |
| F-06 Funnel denominator mismatch | FUN-01, DAT-02 | Reject invalid rate |
| F-07 Deterministically attributed sale | ATT-01, ATT-02, CAU-01 | Attribution allowed; incrementality claim withheld |
| F-08 CRM outcome column missing | DAT-01, GOV-01 | Missing != zero; INCONCLUSIVE if decision-critical |
| F-09 Concurrent campaign overlap | CON-01, CON-02 | Grade contamination and downgrade/block inference |
| F-10 Sales mature after 14 days but test read at day 5 | DAT-03, DEC-02 | Identify censoring/immaturity; continue or inconclusive per preregistration |
| F-11 Platform metric definition changed | MET-01, GOV-01 | Do not silently compare incompatible metrics |
| F-12 Real commercial win with adequate evidence | ECO-01, DEC-01, DEC-03 | SCALE only when effect, guardrails, economics and evidence justify it |
| F-13 Duplicate WhatsApp lead across two touchpoints | DAT-02, ATT-01 | Deduplicate person/outcome and preserve assisted touchpoints |
| F-14 High lead lift but response capacity saturated | ECO-01, CON-01 | Do not assume marginal scale economics remain valid |

## Grading principles

1. Grade the final decision and intermediate observable checks separately.
2. A correct final label reached through fabricated or invalid calculations is a fail.
3. A cautious `INCONCLUSIVE` is not automatically a pass; the agent must identify the actual evidence defect.
4. The grader must include deterministic checks where possible: arithmetic, IDs, denominator selection, frozen KPI, decision rule and required missing-state handling.
5. Narrative quality cannot compensate for a wrong experiment decision.
6. Development fixtures may be public. Final release requires sealed held-out cases created after the candidate behavior is frozen.

## Immediate downstream meaning

For the active automotive A/B test, this matrix does not declare a winner and does not alter the experiment. It tells us what the future Analytics agent must be able to prove before we trust its conclusion. In particular, it must compare A and B over the same valid window, preserve spend/exposure differences, keep missing lead/sale outcomes distinct from zero, check whether only the creative changed, and refuse to infer a business winner from views alone.

## Next gate

Before creating the professional core:

1. map each Tier-1 competency to stable knowledge, live context, deterministic tooling or escalation;
2. define the minimum reproducible computation contract;
3. create public development fixtures and graders;
4. freeze the candidate;
5. run sealed held-out qualification;
6. only after PASS package the reusable core and automotive specialization.