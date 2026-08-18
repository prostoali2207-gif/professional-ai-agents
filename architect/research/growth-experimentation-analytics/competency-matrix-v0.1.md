# Growth Experimentation & Measurement — competency matrix v0.1

Status: research/design artifact; not release-ready.
Date: 2026-08-18.
Parent audit: `analytics-agent-profession-gap-audit-v0.1.md`.

## Purpose

Define observable capabilities for a reusable Growth Experimentation & Measurement professional core. A competency passes only when the candidate demonstrates the behavior on realistic cases; prose claiming the rule is insufficient.

## Release-critical competencies

| ID | Required capability | Observable pass evidence | Failure signal |
|---|---|---|---|
| EXP-01 | Validate experiment comparability: unit, assignment, exposure window and locked variable | Detects material mismatch and blocks/downgrades inference | Declares winner without checking comparability |
| EXP-02 | Detect broken allocation/instrumentation, including SRM where randomization exists | Distinguishes assignment from exposure and diagnoses unexplained imbalance | Treats material imbalance as harmless |
| EXP-03 | Respect fixed-horizon vs sequential stopping rules | Refuses invalid early winner declaration | Stops when result first looks favorable |
| EXP-04 | Judge sample adequacy and minimum useful effect | Identifies underpowered evidence | Treats tiny-sample percentage lift as proof |
| EXP-05 | Control multiple metrics, variants and post-hoc segments | Keeps primary metric fixed and labels post-hoc findings exploratory | Rescues failed test with best-looking subgroup |
| EXP-06 | Interpret effect size with uncertainty | Reports counts, denominators, effect and uncertainty | Gives binary verdict from percentage/p-value alone |
| CAU-01 | Bound causal claims | Uses causal language only when design supports it | Treats attribution/correlation as causation |
| MET-01 | Preserve metric definitions, denominators and versions | Rejects incompatible comparisons | Treats unlike metrics as equivalent |
| MET-02 | Judge whether the primary metric represents business value | Detects proxy failure and applies guardrails | Optimizes proxy while downstream value worsens |
| DAT-01 | Distinguish zero, missing, delayed and invalid | Preserves state and refuses fabricated zeroes | Converts missing outcome to zero |
| DAT-02 | Verify joins, identity and duplicate handling | Reconciles duplicate people/events/outcomes | Double-counts one outcome |
| DAT-03 | Detect selection, survivorship and censoring | Recognizes immature/right-censored outcomes | Calls absent-yet-unmatured outcome a true zero |
| ATT-01 | Grade attribution evidence | Distinguishes deterministic, corroborated, assisted and unknown | Over-credits weak matches |
| ATT-02 | Separate attribution from incrementality | Explicitly withholds causal lift claim without counterfactual evidence | Treats last-touch attribution as incrementality |
| FUN-01 | Reconstruct funnel with valid populations | Uses the correct eligible denominator at each stage | Divides by unrelated population |
| FUN-02 | Measure downstream quality, not just activity volume | Detects quality collapse behind higher activity | Calls raw activity growth a business win |
| CON-01 | Find and grade confounders | Identifies severity/direction and blocks fatal inference | Mentions confounder but still declares clean winner |
| CON-02 | Detect contamination, carry-over and overlapping treatments | Finds treatment overlap and downgrades causal confidence | Assumes isolation without checking |
| ECO-01 | Decide whether an effect is economically/operationally scalable | Checks cost/capacity constraints where relevant | Recommends unrestricted scale from upstream lift alone |
| DEC-01 | Execute preregistered decision rule | Returns the decision dictated by frozen rules | Moves KPI/threshold after seeing results |
| DEC-02 | Use INCONCLUSIVE correctly | Names the actual evidence defect and what resolves it | Forces win/loss despite insufficient evidence |
| DEC-03 | Require replication proportional to uncertainty and downside | Requests confirmation when risk warrants it | Scales high-risk change from weak first result |
| TOOL-01 | Produce reproducible calculations | Emits inputs, method and output/tool record | Unsupported narrative arithmetic |
| GOV-01 | Preserve provenance and unknowns; never fabricate | Material result traces to source/state | Invents unavailable values |
| GOV-02 | Minimize PII | Uses privacy-safe analytical identifiers | Copies unnecessary personal data into outputs |

## Criticality

Tier 1, required before the core can influence SCALE/KILL:
`EXP-01, EXP-02, EXP-03, EXP-04, EXP-06, CAU-01, MET-01, DAT-01, DAT-02, DAT-03, ATT-02, FUN-01, CON-01, TOOL-01, DEC-01, DEC-02, GOV-01`.

Tier 2, required for production-quality commercial analysis:
`EXP-05, MET-02, ATT-01, FUN-02, CON-02, ECO-01, DEC-03, GOV-02`.

## Development fixture mapping

The public suite should cover at least:
- proxy winner / business loser;
- unequal randomized allocation;
- fixed-horizon peeking;
- tiny sample with dramatic lift;
- post-hoc subgroup rescue;
- funnel denominator mismatch;
- attribution without incrementality;
- missing outcome treated as zero;
- concurrent-treatment contamination;
- delayed/right-censored outcome;
- metric-definition change;
- valid commercial SCALE case;
- duplicate identity/outcome counting;
- capacity saturation under acquisition lift.

## Grading principles

1. Grade final decision and intermediate checks separately.
2. Correct label reached through fabricated or invalid calculations is a fail.
3. `INCONCLUSIVE` passes only when the actual evidence defect is identified.
4. Use deterministic checks wherever possible: arithmetic, IDs, denominator selection, frozen KPI and decision rules.
5. Narrative quality cannot compensate for a wrong decision.
6. Public development fixtures cannot qualify the candidate; final release requires fresh sealed held-out cases after candidate freeze.

## Next gate

Map Tier-1 competencies to stable knowledge, live context, deterministic tooling or escalation; finish the provider-neutral development harness; then build and qualify the reusable core.
