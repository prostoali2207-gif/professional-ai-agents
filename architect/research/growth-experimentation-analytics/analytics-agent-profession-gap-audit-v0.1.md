# Growth Experimentation & Analytics — profession/gap audit v0.1

Status: research/design artifact; not a SKILL and not release-ready.

Date: 2026-08-18.

## 1. Decision

Do not rewrite the downstream `auto-sales-growth-system/agents/analytics.md` from intuition.

Current disposition: **UPGRADE CANDIDATE**, not KEEP and not REBUILD yet.

Reason: the downstream agent already encodes several strong professional behaviors — preregistered decision rules, metric-definition governance, direct/assisted/unknown attribution, small-sample caution, fixed-vs-sequential test discipline, funnel reconstruction, lead-quality controls, confounder analysis, and SCALE/ITERATE/KILL/INCONCLUSIVE boundaries. However, this is still prose-level evidence. The repository currently has no dedicated professional core and no behavioral qualification package proving the agent can execute these judgments reliably on adversarial or ambiguous cases.

The target profession is not generic "analytics". It is a composition of:

- experimentation analysis and causal inference;
- growth/product measurement and metric design;
- attribution and measurement validity;
- funnel/commercial analytics;
- decision support under sparse and imperfect data.

For the automotive project, paid-media and vehicle-sales context should remain specialization/live context rather than be baked into a reusable professional core.

## 2. Evidence basis

### Internal

- Agent Architect `architect/SKILL.md` requires profession reconstruction, reusable-core inspection, observable competencies, evidence packaging, professional judgment, and behavioral/adversarial evaluation before release.
- Downstream source: `prostoali2207-gif/auto-sales-growth-system/agents/analytics.md`.
- No dedicated analytics/experimentation professional core was found in the current trusted library during targeted repository search.

### External primary/authoritative practice evidence

The following sources establish that trustworthy experimentation work includes more than reporting uplift:

1. Ron Kohavi et al., *Practical Guide to Controlled Experiments on the Web* (KDD 2007 / ExP Platform): controlled experiments require clear evaluation criteria, statistical power/sample-size discipline, trustworthy randomization and attention to technical/organizational limitations.
2. ExP Platform, *A/B Testing at Scale Tutorial* (SIGIR/KDD 2017): trustworthy experimentation explicitly includes data quality, A/A tests, sample-ratio mismatch, carry-over/random imbalance, guardrails, metric design, metric interpretation pitfalls and effect heterogeneity.
3. Ron Kohavi, Alex Deng, Lukas Vermeer, *A/B Testing Intuition Busters* (KDD 2022): intuitive metric/test interpretations can be materially misleading and require explicit statistical safeguards.
4. ExP Platform bibliography on metric development and long-term experiments: goal metrics require directionality/sensitivity; short-term metric movement may fail to represent long-term value; survivorship/selection/cookie-stability and other biases can corrupt long-horizon interpretation.

These sources are not copied into runtime knowledge by default. They support profession reconstruction and competency requirements.

## 3. Core competency model — provisional

Legend:
- CORE — stable transferable professional capability.
- BOUNDARY-CRITICAL — protects the correctness of adjacent roles/decisions.
- CONTEXTUAL — must bind to current platform/business data.
- ESCALATION — requires human/statistical specialist review beyond safe competence.

| ID | Competency | Class | Current downstream coverage | Audit status |
|---|---|---|---|---|
| EXP-01 | Experiment design integrity audit: unit, assignment, exposure, control, interference, stopping rule | CORE | Partial | GAP |
| EXP-02 | Randomization/data-quality diagnostics including sample-ratio mismatch and A/A sanity | CORE | Weak/implicit | GAP |
| EXP-03 | Fixed-horizon vs sequential inference and peeking control | CORE | Strong prose | UNQUALIFIED |
| EXP-04 | Power, MDE, sample-size adequacy and sparse-outcome reasoning | CORE | Partial | GAP |
| EXP-05 | Multiple metrics/variants/segments and post-hoc inference control | CORE | Partial | UNQUALIFIED |
| EXP-06 | Effect size + uncertainty interpretation, not significance-only decisions | CORE | Strong prose | UNQUALIFIED |
| EXP-07 | Observational/quasi-experimental causal-claim boundary | CORE | Strong prose | UNQUALIFIED |
| MET-01 | Metric definition/version/denominator governance | CORE | Strong | UNQUALIFIED |
| MET-02 | Goal metric/OEC design: directionality, sensitivity and business alignment | CORE | Partial | GAP |
| MET-03 | Guardrail, diagnostic and primary-metric separation | CORE | Strong | UNQUALIFIED |
| MET-04 | Metric validity under platform-definition changes and non-equivalent populations | BOUNDARY-CRITICAL | Strong | UNQUALIFIED |
| DAT-01 | Data lineage, completeness, delayed/missing/invalid-state distinction | CORE | Strong | UNQUALIFIED |
| DAT-02 | Identity/join correctness and duplicate/event-state handling | CORE | Partial | GAP |
| DAT-03 | Selection, survivorship, censoring and missing-not-at-random risks | CORE | Weak | GAP |
| ATT-01 | Deterministic/self-reported/assisted/unknown attribution hierarchy | CORE | Strong | UNQUALIFIED |
| ATT-02 | Attribution-vs-incrementality distinction | BOUNDARY-CRITICAL | Strong | UNQUALIFIED |
| ATT-03 | Cross-device/offline/identity-resolution uncertainty and double-count prevention | CONTEXTUAL + CORE | Partial | GAP |
| FUN-01 | Funnel reconstruction with correct denominator population | CORE | Strong | UNQUALIFIED |
| FUN-02 | Lead-quality and business-outcome linkage | CONTEXTUAL + CORE | Strong automotive delta | UNQUALIFIED |
| ECO-01 | Economics: gross profit, cost per qualified outcome, marginal scaling economics | CONTEXTUAL + CORE | Partial | GAP |
| CON-01 | Confounder identification and severity grading | CORE | Strong list | UNQUALIFIED |
| CON-02 | Interaction/carry-over/contamination/concurrent-experiment effects | CORE | Partial | GAP |
| DEC-01 | Decision rule execution without metric switching | CORE | Strong | UNQUALIFIED |
| DEC-02 | Distinguish INCONCLUSIVE from failure and from insufficient execution | CORE | Strong | UNQUALIFIED |
| DEC-03 | Replication requirement based on uncertainty, cost and reversibility | CORE | Partial | GAP |
| GOV-01 | No fabrication; preserve unknown; evidence provenance | BOUNDARY-CRITICAL | Strong | UNQUALIFIED |
| GOV-02 | PII minimization in analytical outputs | BOUNDARY-CRITICAL | Present | UNQUALIFIED |
| TOOL-01 | Reproducible computations / deterministic calculator or statistical tooling | CORE runtime | Not specified enough | BLOCKING GAP |
| EVAL-01 | Behavioral qualification on realistic experiment packets | CORE release | Absent | BLOCKING GAP |
| EVAL-02 | Adversarial cases: peeking, SRM, Simpson-like aggregation, denominator mismatch, post-hoc rescue, attribution overclaim | CORE release | Absent | BLOCKING GAP |

## 4. What the current agent already gets right

These should be preserved unless evaluation disproves them:

- primary KPI and decision rule are frozen before result inspection;
- secondary metrics diagnose mechanism but cannot rescue a failed primary outcome;
- missing/unknown is not treated as zero;
- views are diagnostic for LEAD/DIRECT_SALE rather than the sales-system objective;
- attribution is explicitly separated from incrementality;
- organic observational tests do not receive causal language automatically;
- small samples are represented with counts/denominators and uncertainty;
- fixed-horizon peeking is prohibited unless a valid sequential design was preregistered;
- lead-quality deterioration can invalidate apparent message-volume growth;
- funnel denominators must correspond to the same eligible population;
- INCONCLUSIVE is a legitimate outcome;
- the Strategist, not Analytics, owns the final portfolio decision.

This is sufficient to reject REBUILD at this stage. The problem is not that the current agent is empty; the problem is that important professional invariants remain either incomplete or untested.

## 5. Blocking gaps before qualification

### G-A01 — Sample-ratio mismatch / assignment integrity

The agent discusses joins and execution fidelity but lacks an explicit diagnostic for treatment/control allocation integrity and sample-ratio mismatch. A test may look statistically clean while assignment or exposure is broken.

Required closure:
- encode expected vs observed allocation checks when randomization exists;
- distinguish randomization-unit count from exposure/metric count;
- stop causal interpretation on material unexplained mismatch.

### G-A02 — A/A and instrumentation sanity

There is no explicit A/A or negative-control style sanity logic. The profession model needs a method for detecting measurement/systematic bias before trusting treatment effects.

Required closure:
- define when A/A is appropriate;
- detect false positive drift, instrumentation asymmetry, and metric pipeline inconsistency;
- do not require A/A mechanically for every small automotive test.

### G-A03 — Power / MDE / minimum useful effect

The current file mentions minimum sample and practical effect but does not define a reliable decision model for power, detectable effect and rare-outcome feasibility.

Required closure:
- separate business minimum useful effect from statistical detectability;
- surface underpowered designs before launch;
- avoid false precision when traffic/lead volume cannot resolve the intended question.

### G-A04 — Metric quality, not only metric usage

The agent correctly freezes metrics, but the profession must also assess whether the primary metric itself has valid directionality, sensitivity and business alignment.

Required closure:
- evaluate whether a metric can move in the desired direction while harming the business;
- distinguish local feature metrics from system/business outcome criteria;
- document known proxy failure modes.

### G-A05 — Selection/survivorship/censoring

The current confounder list is broad but under-models selection and survivorship mechanisms, especially delayed sales outcomes, sold inventory, incomplete follow-up, channel eligibility and maturation windows.

Required closure:
- represent right-censoring/delayed outcomes;
- distinguish missing outcome from no outcome;
- detect cohort changes caused by inclusion/exclusion after treatment.

### G-A06 — Interaction and contamination

Concurrent campaigns are listed as confounders, but the agent lacks an explicit model of overlapping experiments, spillover, treatment contamination and carry-over.

Required closure:
- check overlapping audience/vehicle/time exposure;
- downgrade causal claims when isolation fails;
- preserve direct evidence of cross-treatment exposure where measurable.

### G-A07 — Economics and scale validity

The agent mentions gross profit and time-to-sale but SCALE logic is not yet a full marginal-economics model.

Required closure:
- distinguish positive effect from economically scalable effect;
- include cost per qualified lead/appointment/sale when spend exists;
- detect capacity constraints and diminishing returns;
- require stronger confirmation when scale cost or downside risk is material.

### G-A08 — Reproducible computation tooling

The prompt describes statistical discipline but does not specify a minimum deterministic computation path. Narrative arithmetic is insufficient for qualification.

Required closure:
- define calculator/statistical-tool eligibility;
- require reproducible formulas/inputs/outputs for rates, intervals and allocation diagnostics;
- require explicit failure when a requested inference exceeds available tooling/assumptions.

### G-A09 — Behavioral qualification

No dedicated held-out qualification package was found for this profession.

Required closure:
Build a discriminating suite that includes at minimum:

1. apparent winner on views but loser on qualified leads;
2. unequal assignment/sample-ratio mismatch;
3. repeated peeking at a fixed-horizon test;
4. small sample with large apparent lift and wide uncertainty;
5. post-hoc segment that looks excellent after aggregate failure;
6. denominator mismatch across funnel stages;
7. deterministic attribution without evidence of incrementality;
8. missing CRM outcomes incorrectly presented as zero;
9. concurrent campaign contamination;
10. delayed sale outcome / right-censoring;
11. metric-definition change between A and B;
12. valid SCALE case with commercial/economic guardrails passed.

The grader must score observable decisions and calculations, not self-reported adherence.

## 6. Reuse decision

No trusted analytics/experimentation core was identified in the current library.

Nearby `paid-media-performance-marketing` material is **not** a substitute. Paid media contains measurement competence but has a broader campaign-optimization responsibility and different authority surface. Reusing it as the analytics core would create coupling and duplicate decision rights.

Disposition:

`Target profession -> no compatible core -> BUILD NEW professional core candidate from the strongest existing downstream Analytics behavior + new evidence-backed gaps`.

This does **not** mean writing a new SKILL now. The next artifacts should be the competency matrix, knowledge/evidence packaging, and behavioral evaluation design.

## 7. Downstream architecture recommendation

Target stack:

`Growth Experimentation & Measurement Professional Core`
→ `Automotive Sales Analytics specialization`
→ `UAE / Meta / YouTube / Telegram / WhatsApp live context`
→ `Showroom 171 business definitions and economics`
→ `specific experiment packet (e.g. Yaris A/B)`

Do not create a Toyota/Yaris analytics agent. Vehicle-specific details belong to the experiment instance.

## 8. Immediate implication for the current Yaris A/B

Do not wait until the end of the test to discover measurement defects.

Before final analysis, verify that the experiment packet preserves:
- exact common evaluation start at B launch if A was already running;
- spend/exposure per variant over the same comparison window;
- actual placement/audience/optimization equivalence except the declared creative variable;
- qualified WhatsApp/DM leads by variant where attribution is available;
- appointments/test drives/sales by exact vehicle when observable;
- missing/unknown outcomes separately from zero;
- any execution deviations or platform delivery imbalance.

This packet can become the first field case, but it must not be the only qualification evidence because the test design may itself be imperfect and field data is not a sealed held-out eval.

## 9. Next gate

Before modifying `auto-sales-growth-system/agents/analytics.md`:

1. create observable competency matrix with criticality and evidence mapping;
2. package stable vs live knowledge dependencies;
3. define deterministic computation/tool contract;
4. design public development fixtures plus sealed held-out cases;
5. implement/qualify the reusable core;
6. then integrate an automotive specialization and compare against the current downstream agent;
7. preserve any current behavior that outperforms the new candidate.

Until these gates pass, status remains **UPGRADE CANDIDATE / NOT QUALIFIED**.
