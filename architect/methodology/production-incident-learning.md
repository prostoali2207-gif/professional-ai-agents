# Production Incident Learning

Status: v0.1.

## Goal

Turn real failures, near-misses, user feedback, drift, and unexpected deployment behavior into systematic improvements without corrupting stable professional knowledge or overfitting the agent to isolated incidents.

## Core principle

Production feedback is evidence, not automatically truth.

A single incident must not directly become a permanent rule. The learning path is:

`observation -> reproduce/validate -> classify -> root cause -> affected layer -> candidate change -> regression/adversarial eval -> deploy -> monitor`.

## 1. Incident intake

Capture at least:

- task/context;
- agent/version/configuration;
- tools and data sources involved;
- observed outcome;
- expected outcome;
- severity and user impact;
- reproducibility;
- evidence/logs/traces;
- environmental changes;
- whether the incident is a failure, near-miss, drift signal, or ambiguous report.

Do not erase uncertainty from user reports.

## 2. Failure classification

Classify before changing architecture:

- profession-model failure;
- missing knowledge;
- stale knowledge;
- retrieval failure;
- judgment failure;
- workflow failure;
- tool/interface failure;
- execution failure;
- verification failure;
- coordination/handoff failure;
- grader/eval failure;
- environment drift;
- user/context misunderstanding;
- unsupported capability boundary.

Multiple causes may coexist.

## 3. Reproduction and evidence

Prefer direct reproduction in a realistic environment. When exact reproduction is impossible, preserve the uncertainty and gather the strongest available substitute evidence.

Anecdote alone is not enough for a structural change unless the severity is high enough to justify precautionary action.

## 4. Root-cause standard

Do not stop at the first visible symptom.

Ask:

1. What assumption failed?
2. Which layer owned that assumption?
3. Why did existing checks fail to catch it?
4. Was the behavior reasonable under the information available?
5. Did the agent lack knowledge, fail to retrieve it, misjudge it, or fail to verify execution?
6. Is the failure local or evidence of a broader class?

## 5. Learning destinations

Route validated learning to the correct layer:

- stable recurring principle -> knowledge/judgment layer;
- changing fact or market/platform behavior -> live retrieval/freshness rule;
- operational sequence failure -> workflow;
- interface ambiguity -> tool contract / observability;
- repeated failure family -> regression suite;
- rare catastrophic case -> adversarial/safety gate;
- role-boundary failure -> escalation/agent-boundary architecture.

Do not use `SKILL.md` as the default dumping ground for incidents.

## 6. Promotion gate for permanent knowledge

Before converting an incident into stable agent knowledge, require sufficient evidence that:

- the lesson generalizes beyond one accidental case;
- scope and exceptions are understood;
- the change does not contradict stronger evidence;
- provenance is recorded;
- the target competency is identified;
- an eval demonstrates that the change improves the intended behavior;
- regression tests show no material degradation elsewhere.

Otherwise keep it as an incident case or temporary heuristic.

## 7. Drift and monitoring

Post-deployment behavior may diverge from pre-deployment assumptions because tools, sources, interfaces, markets, policies, models, and user behavior change.

Each deployed agent should define what is monitored, why, at what cadence, with what thresholds, and who/what can trigger escalation or rollback.

Potential signals include:

- success/failure rate changes;
- tool-call errors;
- retrieval miss rate;
- grader disagreement;
- user corrections;
- repeated escalation patterns;
- changed external documentation;
- new failure clusters;
- performance differences between eval and production.

## 8. Near-miss learning

Do not learn only from visible failures. Record cases where a wrong action was avoided by chance, a downstream system rejected an invalid operation, or a human reviewer caught a severe mistake. Near-misses often expose missing controls before harm occurs.

## 9. Feedback contamination control

Production feedback can be noisy, biased, adversarial, or unrepresentative. Therefore:

- deduplicate repeated reports of the same event;
- separate user preference from professional correctness;
- protect against malicious feedback;
- compare feedback with objective outcomes where possible;
- avoid letting a vocal minority redefine general behavior without evidence;
- keep stable foundations separate from volatile operational lessons.

## 10. Change verification

Every incident-driven change must answer:

- Which failure does this fix?
- Why should it fix the root cause?
- What alternative fixes were considered?
- What new failure could this introduce?
- Which eval now fails before the change and passes after it?
- Which unrelated regression tests remain stable?

## Quality gate

Production learning passes only when a reviewer can trace:

`real observation -> evidence -> diagnosis -> architectural layer -> tested change -> post-change monitoring`.

NIST AI RMF requires ongoing production monitoring, incident response, recovery, change management, feedback integration, and continual improvement. NIST AI 800-4 further emphasizes that post-deployment monitoring is necessary because controlled pre-deployment evaluation cannot expose all real-world variability and unexpected consequences.