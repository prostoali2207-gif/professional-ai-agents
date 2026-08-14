# Agent Architect Pre-SKILL Completeness Audit

Status: v0.1 / blocking gate.

The Architect must not receive a final `SKILL.md` until this audit passes.

## A. Profession reconstruction

PASS requires evidence that the methodology can reconstruct a profession from real work rather than user labels alone.

Check:

- responsibilities and boundaries;
- task and decision decomposition;
- expert-vs-average discriminators;
- tacit cues and uncertainty;
- hidden adjacent competencies;
- failure and recovery patterns;
- tools and evidence loops.

## B. Knowledge engineering

PASS requires:

- claim-first sourcing;
- distinction among standards, empirical evidence, professional literature, practitioner evidence, opinion, and examples;
- provenance;
- freshness classes;
- live-research rules;
- conflict handling;
- knowledge inclusion and maintenance gates;
- retrieval evaluation.

## C. Judgment architecture

PASS requires the agent design method to encode:

- causal reasoning;
- trade-offs;
- exceptions;
- scope conditions;
- uncertainty;
- justified rule-breaking;
- professional boundaries;
- escalation.

## D. Workflow and tools

PASS requires:

- execution loops appropriate to the profession;
- tool/interface design as part of capability;
- observability;
- direct verification where possible;
- downstream-result checking;
- recovery from partial/failed execution.

## E. Evaluation engineering

PASS requires:

- knowledge and application tests;
- authentic practical tasks;
- adversarial tests;
- false-premise tests;
- diagnosis and critique tasks;
- tool-use and evidence tests;
- outcome + trajectory evaluation;
- grader calibration;
- holdouts and leakage control;
- regression suites;
- stochastic/uncertainty-aware measurement.

## F. Lifecycle learning

PASS requires:

- production incident intake;
- reproduction and root-cause analysis;
- near-miss handling;
- drift monitoring;
- correct routing of lessons to architecture layers;
- protection from noisy feedback contamination;
- regression verification after fixes.

## G. Architecture choice

PASS requires a reasoned mechanism for choosing among:

- one agent;
- one agent with modules;
- specialist + critic;
- orchestrator + specialists;
- multi-agent system.

Complexity must be justified by task decomposition and measurable performance, not fashion.

## H. Red-team questions

Before PASS, explicitly ask:

### Senior practitioner
- Which essential tacit skill is missing?
- Where does the design substitute a checklist for judgment?
- Which decision cannot actually be made from the available evidence?
- Which tool/observation would a real expert insist on using?

### Teacher / competency assessor
- Are capabilities observable and testable?
- Are tests authentic or just trivia?
- Can a weak agent pass by memorizing expected language?
- Are mastery levels meaningfully discriminative?

### Hiring manager
- Would this agent produce useful work under real constraints?
- Can it diagnose ambiguous failures?
- Can it work with incomplete information without bluffing?
- Can it explain trade-offs and evidence?
- Does it know when to escalate?

## I. Unknown-unknown prompt

Mandatory final question before any agent is finalized:

`What would a strong practitioner of this profession notice is missing, even though the user did not know to ask for it?`

Any material answer must be investigated and incorporated or explicitly deferred with justification.

## J. Decision rule

- `PASS`: no material architectural gap remains and the dry-run demonstrates the methodology working end to end.
- `CONDITIONAL`: gaps are known and bounded but still require targeted evidence/testing.
- `FAIL`: important capability, evidence, evaluation, or lifecycle layer is absent or only asserted.

Current status: CONDITIONAL. The methodology now covers the major architecture layers, but it still requires an end-to-end profession dry-run and red-team before a final Architect SKILL is justified.