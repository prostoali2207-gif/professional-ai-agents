# Production Incident Learning

Status: v0.2.

## Goal

Turn real failures, near-misses, user feedback, drift, security events, state corruption, and unexpected deployment behavior into systematic improvements without corrupting stable professional knowledge or overfitting the agent to isolated incidents.

## Core principle

Production feedback is evidence, not automatically truth.

A single incident must not directly become a permanent rule. The learning path is:

`observation -> reproduce/validate -> classify -> root cause -> affected layer -> candidate change -> regression/adversarial eval -> deploy -> monitor`.

## 1. Incident intake

Capture at least:

- task/context;
- agent/version/configuration;
- tools/runtime and data sources involved;
- relevant session/memory/checkpoint state;
- observed outcome;
- expected outcome;
- severity and user impact;
- reproducibility;
- evidence/logs/traces/run record;
- environmental changes;
- whether the incident is a failure, near-miss, drift signal, security event, state-integrity event, or ambiguous report.

Do not erase uncertainty from user reports.

## 2. Failure classification

Classify before changing architecture:

- profession-model failure;
- competency/evidence-model failure;
- missing knowledge;
- stale knowledge;
- retrieval failure;
- evidence-validity/comparability failure;
- memory/state/context failure;
- context-compaction/checkpoint failure;
- judgment failure;
- workflow/execution-control failure;
- stall/termination failure;
- procedural capability selection/loading failure;
- tool/interface failure;
- execution failure;
- verification failure;
- security/trust-boundary failure;
- prompt-injection/agent-hijacking failure;
- skill/dependency supply-chain failure;
- coordination/handoff failure;
- permission/authority failure;
- grader/eval failure;
- environment drift;
- user/context misunderstanding;
- unsupported capability boundary.

Multiple causes may coexist.

## 3. Reproduction and evidence

Prefer direct reproduction in a realistic environment. When exact reproduction is impossible, preserve the uncertainty and gather the strongest available substitute evidence.

For stateful failures reproduce or preserve, where possible:

- initial state/checkpoint;
- state transitions/memory writes;
- tool actions and observations;
- compaction/restart boundaries;
- approvals/security decisions;
- verified end state.

Anecdote alone is not enough for a structural change unless severity is high enough to justify precautionary action.

## 4. Root-cause standard

Do not stop at the first visible symptom.

Ask:

1. What assumption failed?
2. Which layer owned that assumption?
3. Why did existing checks fail to catch it?
4. Was the behavior reasonable under the information/state available?
5. Did the agent lack knowledge, fail to retrieve/use it, preserve bad state, misjudge it, or fail to verify execution?
6. Did untrusted content cross an instruction/authority boundary?
7. Did the execution loop gain new information or merely repeat itself?
8. Is the failure local or evidence of a broader class?

## 5. Learning destinations

Route validated learning to the correct layer:

- stable recurring principle -> knowledge/judgment layer;
- changing fact or market/platform behavior -> live retrieval/freshness rule;
- empirical comparator mistake -> evidence-validity layer;
- operational sequence/stall/retry failure -> workflow/execution-control layer;
- bad persistence/compaction/supersession -> runtime state/memory/context layer;
- interface ambiguity/idempotency/partial-success -> tool contract / observability;
- skill loading/dependency defect -> procedural capability layer;
- prompt injection/data-flow/supply-chain defect -> security/trust layer;
- repeated failure family -> regression suite;
- rare catastrophic case -> adversarial/hard-fail gate;
- role-boundary failure -> escalation/agent-boundary architecture.

Do not use `SKILL.md` as the default dumping ground for incidents.

## 6. Promotion gate for permanent knowledge or state policy

Before converting an incident into stable agent knowledge, memory policy, security policy, or procedural rule, require sufficient evidence that:

- the lesson generalizes beyond one accidental case;
- scope and exceptions are understood;
- the change does not contradict stronger evidence;
- provenance is recorded;
- the target competency/layer is identified;
- an eval demonstrates that the change improves the intended behavior;
- regression tests show no material degradation elsewhere.

Otherwise keep it as an incident case, temporary containment, or hypothesis.

## 7. Drift and monitoring

Post-deployment behavior may diverge from pre-deployment assumptions because tools, sources, interfaces, markets, policies, models, skills, memory stores, attack patterns, and user behavior change.

Each deployed agent should define what is monitored, why, at what cadence, with what thresholds, and who/what can trigger escalation or rollback.

Potential signals include:

- success/failure rate changes;
- critical-failure rate;
- tool-call and retry errors;
- repeated no-progress/stall patterns;
- retrieval miss rate;
- memory contradiction/update errors;
- compaction/restart failures;
- grader disagreement;
- user corrections;
- security denials/injection attempts;
- unexpected network/data-flow events;
- repeated escalation patterns;
- changed external documentation or skill dependencies;
- new failure clusters;
- performance differences between eval and production.

## 8. Near-miss learning

Do not learn only from visible failures. Record cases where a wrong action was avoided by chance, a downstream system rejected an invalid operation, an approval gate blocked injected instructions, a retry happened not to duplicate a side effect, or a human reviewer caught a severe mistake. Near-misses often expose missing controls before harm occurs.

## 9. Feedback contamination control

Production feedback can be noisy, biased, adversarial, or unrepresentative. Therefore:

- deduplicate repeated reports of the same event;
- separate user preference from professional correctness;
- protect against malicious feedback and memory poisoning;
- compare feedback with objective outcomes where possible;
- avoid letting a vocal minority redefine general behavior without evidence;
- keep stable foundations separate from volatile operational lessons;
- do not persist incident text as trusted instruction.

## 10. Change verification

Every incident-driven change must answer:

- Which failure does this fix?
- Why should it fix the root cause?
- What alternative fixes were considered?
- What new failure could this introduce?
- Which eval now fails before the change and passes after it?
- Which unrelated regression tests remain stable?
- Does state/security/tool authority change as a side effect?
- Is rollback possible if the repair regresses production?

## Quality gate

Production learning passes only when a reviewer can trace:

`real observation -> evidence/run record -> diagnosis -> architectural layer -> tested change -> post-change monitoring`.

For stateful or security incidents, the trace must also preserve the relevant state/trust transition. A change is not validated merely because a new prompt sentence appears to suppress the original example.
