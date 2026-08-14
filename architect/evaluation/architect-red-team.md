# Agent Architect Methodology Red-Team

Status: v0.1.

Purpose: attack the methodology before creating the final Agent Architect `SKILL.md`.

## 1. Senior practitioner critique

### Critique: profession maps can become academically complete but operationally useless
A senior practitioner would reject a system that produces exhaustive competency taxonomies but does not help the agent make better decisions under time, evidence, and tool constraints.

Response:
- require every competency to connect to a real decision, failure, evidence loop, or escalation boundary;
- use scope/risk prioritization rather than equal-depth modeling;
- require practical dry-runs and observed execution.

### Critique: tacit expertise cannot be reconstructed from documents alone
Response:
- Cognitive Task Analysis / Critical Decision Method are included;
- retrospective expert accounts are treated as fallible and must be triangulated with observation, artifacts, outcomes, and multiple cases where possible.

### Critique: adjacent disciplines can overwhelm the primary role
Response:
- classify adjacent competence as CORE, BOUNDARY-CRITICAL, ESCALATION, CONTEXTUAL, or OUT-OF-SCOPE;
- model only enough depth to protect material decisions and know when to escalate.

Verdict: mitigated, but actual applied agents must prove the stopping rule works.

## 2. Teacher / competency-assessor critique

### Critique: the framework may reward verbose explanations instead of competence
Response:
- evaluation must use authentic performance tasks;
- outcome and trajectory are both graded;
- direct evidence/tool use is required where possible;
- trivia and self-description are insufficient evidence.

### Critique: the same team can design both the agent and tests, causing teaching-to-the-test
Response:
- separate development, regression, holdout, and practical evals;
- use hidden/rotating adversarial cases;
- calibrate graders against professional reference judgments;
- treat exposed benchmark performance as weaker evidence.

### Critique: competency levels can become arbitrary labels
Response:
- levels must be defined by observable discriminators: diagnosis quality, cue use, trade-off handling, evidence selection, recovery, and boundary recognition.

Verdict: methodology is defensible if eval construction follows the integrity gates.

## 3. Hiring manager critique

### Critique: 'professional agent' is meaningless if it cannot deliver under real constraints
Response:
- practical evaluation is mandatory;
- tool access, execution, verification, and recovery are part of competence;
- Definition of Done requires observed end-to-end work, not prose quality.

### Critique: over-research can make agents slow and expensive
Response:
- freshness and risk determine when live retrieval is mandatory;
- stable knowledge is stored with provenance;
- low-risk/reversible decisions need less evidence than high-consequence decisions;
- architecture complexity must justify its cost through representative evals.

### Critique: handoffs can destroy context
Response:
- default is not multi-agent;
- decomposition requires separable responsibilities and information contracts;
- tightly coupled work favors one agent with modules.

Verdict: operational usefulness is represented, but future applied agents must measure latency/cost as well as correctness where relevant.

## 4. Evaluation-scientist critique

### Critique: stochastic agents can pass by chance
Response:
- use repeated trials where variance is material;
- report uncertainty rather than a single deterministic score;
- distinguish capability from reliability;
- track grader disagreement.

### Critique: eval suites themselves drift or become contaminated
Response:
- source/version metadata for evals;
- holdouts and rotation;
- contamination checks;
- regression-history tracking;
- grader recalibration after model/system changes.

### Critique: optimizing one benchmark can damage unmeasured behavior
Response:
- incident-derived fixes require unrelated regression checks;
- multi-dimensional quality model rather than single aggregate score;
- production monitoring closes the predeployment/real-world gap.

Verdict: no blocker found, but statistical design must be adapted to each agent's task distribution.

## 5. Systems-engineer critique

### Critique: the methodology focuses on cognition while reliability often fails at interfaces
Response:
- tool/interface architecture is a first-class layer;
- observability, partial success, idempotency/recovery, and downstream verification are required;
- production incident classification includes tool, environment, and coordination failures.

### Critique: system state changes after evaluation
Response:
- volatile/versioned knowledge requires freshness gates;
- post-deployment monitoring and drift detection are mandatory where state changes materially affect outcomes.

### Critique: the agent may optimize locally while breaking system contracts
Response:
- work model includes preserved contracts;
- verification must include downstream effects and regression scope, not only local output.

Verdict: mitigated.

## 6. Mandatory unknown-unknown question

What would a strong Agent Architect practitioner notice is missing, even though the user did not know to ask for it?

### Gap A: capability-to-cost economics
An agent can be more accurate but commercially unusable because of latency, token/tool cost, review burden, or operational complexity.

Action: every architecture decision should include cost/latency/operational overhead when material.

### Gap B: permission and blast-radius design
Tool-capable agents require not only competence but authority boundaries: what they may read, write, delete, publish, spend, deploy, or approve.

Action: applied agent architecture must define least-required permissions, reversible vs irreversible actions, confirmation/escalation gates, and auditability.

### Gap C: environment/reproducibility specification
A skill can behave differently across models, toolsets, connectors, or repository states.

Action: record execution assumptions: model/tool capabilities, required environment, dependencies, and version-sensitive behavior.

### Gap D: organizational accountability
Some professional decisions require an accountable human owner even if the agent can technically perform them.

Action: distinguish autonomous capability from organizational authority; high-consequence deployment must define accountable owner and escalation path.

## 7. Corrections required before final SKILL

Add these explicit concepts to the executable Architect workflow:

1. cost/latency/operational-complexity trade-off;
2. permission/blast-radius analysis for tool-using agents;
3. environment/capability assumptions;
4. accountable-owner/escalation requirements for consequential decisions.

## Red-team verdict

CONDITIONAL PASS.

No fundamental contradiction invalidates the methodology. Four material omissions were found and must be encoded before finalizing `architect/SKILL.md`.