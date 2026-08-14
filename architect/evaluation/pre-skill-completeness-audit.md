# Agent Architect Pre-SKILL Completeness Audit

Status: v0.2 / PASS.

The Architect must not receive a final `SKILL.md` until this audit passes.

## A. Profession reconstruction — PASS

The methodology can reconstruct a profession from real work rather than user labels alone, including responsibilities, boundaries, task/decision decomposition, expert-vs-average discriminators, tacit cues, uncertainty, hidden adjacent competencies, failure/recovery patterns, and tools/evidence loops.

Evidence: `dry-run-frontend-engineer.md` exposed material competencies that a superficial frontend prompt would omit.

## B. Knowledge engineering — PASS

Implemented:

- claim-first sourcing;
- source-type distinctions;
- provenance;
- freshness classes;
- live-research rules;
- conflict handling;
- knowledge inclusion/maintenance gates;
- retrieval evaluation.

## C. Judgment architecture — PASS

Implemented:

- causal rationale;
- trade-offs;
- exceptions;
- scope conditions;
- uncertainty;
- justified rule-breaking;
- professional boundaries;
- escalation.

## D. Workflow and tools — PASS

Implemented:

- profession-specific execution loops;
- tools/interfaces as part of competence;
- observability;
- direct verification where possible;
- downstream-result checks;
- recovery from partial/failed execution.

## E. Evaluation engineering — PASS

Implemented:

- knowledge/application tests;
- authentic practical tasks;
- adversarial and false-premise tests;
- diagnosis/critique;
- tool/evidence tests;
- outcome + trajectory evaluation;
- grader calibration;
- holdouts/leakage controls;
- regression suites;
- stochastic/uncertainty-aware measurement.

## F. Lifecycle learning — PASS

Implemented in `production-incident-learning.md`:

- incident intake;
- reproduction/root cause;
- near-misses;
- drift monitoring;
- routing lessons to the correct architecture layer;
- feedback-contamination controls;
- post-fix regression verification.

## G. Architecture choice — PASS

Implemented mechanism for choosing among one agent, modular agent, specialist + critic, orchestrator + specialists, and broader multi-agent systems. Complexity must be justified by representative-task performance, risk boundaries, latency, cost, and coordination overhead.

## H. Scope and operational governance — PASS

Red-team exposed four missing areas. They have been added through `scope-risk-prioritization.md` and `operational-governance.md`:

- adjacent-competency stopping rule;
- capability-to-cost economics;
- permission/blast-radius analysis;
- environment/reproducibility assumptions;
- accountable owner and escalation for consequential deployment.

## I. Red-team — PASS

Completed in `architect-red-team.md` from:

- senior practitioner;
- educator/competency assessor;
- hiring manager;
- evaluation scientist;
- systems engineer.

Material findings were corrected before this PASS.

## J. Mandatory unknown-unknown question — PASS

Question asked:

`What would a strong practitioner of this profession notice is missing, even though the user did not know to ask for it?`

It exposed cost economics, authority/blast radius, environment assumptions, and organizational accountability. These are now encoded.

## K. Practical methodology dry-run — PASS

The frontend-engineer dry-run demonstrated that the methodology can:

- reject an underspecified role label;
- discover hidden competencies;
- identify evidence loops;
- distinguish local code success from browser/downstream success;
- avoid unnecessary multi-agent decomposition;
- expose a new methodological gap and repair it.

The dry-run did not create a frontend agent; it tested the Architect methodology only.

## Decision

`PASS` for creation of the first Agent Architect `SKILL.md`.

This does **not** mean the Architect is finished. After SKILL assembly, the Architect itself must be evaluated as an executable agent workflow. Failures must be repaired at the responsible methodology/knowledge/process layer rather than patched with arbitrary prompt lines.