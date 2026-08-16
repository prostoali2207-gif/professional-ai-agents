# Field Evidence / Production Feedback Loop

## Purpose

Behavioral qualification proves that a professional model can make required decisions in controlled cases. It does **not** prove production effectiveness across real operating environments.

Real projects therefore act as evidence producers, not as automatic training data for Professional Cores.

The loop exists to learn from production without contaminating reusable expertise with local anecdotes, platform drift, survivorship bias, or post-hoc storytelling.

## Evidence classes

Every field observation MUST first be classified as one of:

1. **Experiment-instance evidence** — specific to one campaign, product, vehicle, creative, audience, time window, or test.
2. **Organization evidence** — specific to one company's economics, sales process, staffing, capacity, CRM, authority, inventory, or operating constraints.
3. **Live-context evidence** — country, regulation, platform, policy, auction, product, interface, or account mechanics that can change with time.
4. **Reusable professional evidence candidate** — a possible transferable competency, judgment rule, failure mode, escalation rule, or procedure.

Classes 1–3 remain in the consuming project by default. They MUST NOT silently mutate a Professional Core or durable specialization.

## Required field record

A production experiment intended to inform professional-model quality SHOULD preserve, when available:

- exact professional model and specialization version/digest used;
- dated live and organization context used;
- decision/hypothesis recorded before outcome observation;
- known facts and explicit unknowns at decision time;
- measurement design and data-quality limitations;
- planned success, stop, iterate and scale criteria;
- decisions actually made during execution and their timestamps;
- observed funnel/business outcomes, including downstream outcomes when available;
- deviations from the planned procedure;
- operational interventions by humans or other systems;
- missing data, attribution uncertainty and plausible alternative explanations;
- cost/resource consumption relevant to the decision;
- postmortem findings.

Absence of these fields lowers evidential weight; it must not be filled with invented facts.

## Pre-registration rule

Do not judge a professional model only after seeing the outcome.

Where practical, record before launch:

1. the hypothesis;
2. what evidence would support or weaken it;
3. measurement limitations;
4. decision thresholds or qualitative gates;
5. stop/iterate/scale policy;
6. important unknowns.

This reduces hindsight bias and makes later comparison between expected and observed behavior possible.

## Postmortem

After a meaningful production interval, compare:

- what the specialist believed and recommended with the evidence available at the time;
- what actually happened;
- whether the measurement system was capable of answering the question;
- whether failure came from professional judgment, execution, creative, sales operations, inventory, data quality, external change, or an unresolved combination;
- whether an alternative decision was reasonably available ex ante, not merely obvious in hindsight.

A bad business outcome is not by itself evidence that the specialist was wrong. A good business outcome is not by itself evidence that the specialist was right.

## Promotion gate: project finding -> reusable model

A field finding may become a candidate change to a Professional Core or durable specialization only when all of the following are addressed:

1. **Root cause** — identify the professional judgment/procedure that may be deficient.
2. **Alternative explanations** — seriously test at least one plausible non-model cause.
3. **Transferability** — explain why the finding should generalize beyond this company/country/platform/experiment.
4. **Independent evidence** — seek authoritative literature, additional field cases, controlled evidence, or strong practitioner evidence where feasible. One anecdote is normally insufficient for promotion.
5. **Boundary check** — confirm the finding is not merely live context or organization context.
6. **Counterexample** — identify conditions under which the proposed rule would be wrong or harmful.
7. **Evaluation first** — encode the suspected gap as an adversarial/behavioral fixture that fails for the right reason before changing the professional model, where feasible.
8. **Repair root cause** — change the smallest appropriate layer: Core, durable specialization, evaluation, or nothing.
9. **Regression and reliability** — rerun affected deterministic checks, minimal affected behavioral tests, and required reliability/release gates before qualification.
10. **Version/provenance** — record the field evidence, decision, changed artifact digest and qualification evidence.

## Decision outcomes

The review MUST end in one of these explicit dispositions:

- `NO_CHANGE` — observation does not justify a model change.
- `PROJECT_CONTEXT_UPDATE` — update experiment/organization context only.
- `LIVE_CONTEXT_UPDATE` — update dated market/platform/regulatory context only.
- `EVAL_GAP` — professional model may be adequate, but evaluation failed to cover an important transferable behavior.
- `SPECIALIZATION_CANDIDATE` — evidence suggests a durable domain-specific professional gap.
- `CORE_CANDIDATE` — evidence suggests a cross-domain professional gap.
- `INSUFFICIENT_EVIDENCE` — plausible signal, but causal/transferability evidence is too weak.

Promotion is not automatic even when production performance is poor.

## Anti-patterns

Do not:

- add a rule because one campaign lost money;
- add a rule because one campaign made money;
- turn a successful creative, audience, vehicle, geography or platform tactic into universal expertise;
- infer causality from platform attribution alone;
- rewrite an eval to match a preferred production story;
- use outcome knowledge to pretend the earlier decision was obviously wrong;
- copy current platform mechanics into durable professional knowledge;
- treat the consuming project as an uncurated memory dump for the reusable agent.

## Resource & Cost Engineering

Field learning should be proportional to decision value.

Use existing production telemetry and deterministic analysis before commissioning additional model calls or paid research. Escalate to controlled experiments, external research, or repeated behavioral reliability only when the expected information value can affect a material professional-model decision.

Do not rerun the entire qualification suite when the architecture permits a sealed unaffected layer plus an affected test; do not reuse old behavioral PASS after changing behavior-relevant content.

## Ownership boundary

The consuming project owns raw production evidence, live context, organization context and experiment records.

`professional-ai-agents` owns only the reviewed promotion decision and any resulting reusable professional-model/evaluation change.

This keeps real-world learning connected to the Professional Core without making the Core project-specific.
