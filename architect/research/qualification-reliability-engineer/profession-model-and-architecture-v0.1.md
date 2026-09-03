# Qualification Reliability Engineer — profession model and architecture v0.1

Status: Architect research artifact. Not a SKILL. Not qualified. Not ready for deployment.
Issue: #265
Date: 2026-09-03

## 1. Decision summary

The target capability is not generic QA and not a duplicate of the Independent Evaluator.

The real professional system is a combination of:
- AI evaluation / benchmark engineering;
- software test engineering;
- Site Reliability / Production Engineering;
- distributed/API transport reliability;
- observability and incident analysis;
- measurement validity / experimental design boundaries;
- resource and cost engineering;
- security/privacy handling for evaluation data;
- CI/CD release gating for qualification infrastructure.

Architecture decision: **HYBRID**.

Use a reusable **Qualification Reliability Engineer professional core** for judgment-heavy work, paired with a **deterministic Qualification Reliability Guard** for mechanical fail-closed checks.

Do not make either half sufficient by itself.

## 2. Why the role exists

The repository has repeatedly produced runs in which the professional candidate never reached evaluation because the measurement machinery failed first. Recent examples include synchronous long-call timeout, background Interaction retrieval failure, path/import/runtime-contract defects, quota/provider interruptions, and runs that produced zero completed candidate cases and zero judge calls.

These incidents establish a distinct ownership problem:

> Before accepting a professional verdict or authorizing material provider spend, who establishes that the qualification machine can produce trustworthy evidence under the declared runtime, budget, privacy and comparability contract?

Agent Architect owns profession/qualification design and governance. The Independent Evaluator owns profession-specific judgment. Neither role should silently absorb ongoing responsibility for production reliability of the evaluation machine.

## 3. Primary evidence anchors

### OpenAI — trustworthy third-party evaluations, 2026-05-29

OpenAI states that modern evaluation performance depends on the tested model **and** the environment/setup/harness. Recommended reporting includes model/reasoning/tool access/harness, turns, tokens, attempts/retries, wall-clock, inference cost, expected cost per successful solve where applicable, elicitation methods, and validity checks. Omitting harness choices or validity checks can understate capability or overstate confidence.

Professional implication: harness design, runtime configuration and resource budgets are part of evaluation validity, not incidental DevOps metadata.

Source: https://openai.com/index/trustworthy-third-party-evaluations-foundations/

### NIST — AI measurement and TEVV

NIST treats trustworthy AI evaluation as measurement science and emphasizes tasks, testbeds, software tools, datasets, metrics, context, limitations and reliable measurement methods. The 2026 TEVV-Athlon draft formalizes customized assessment design around explicit organizational TEVV objectives rather than universal one-size-fits-all tests.

Professional implication: the Reliability Engineer must protect the validity of the measurement process without appropriating profession-specific construct design from the evaluator.

Sources:
- https://www.nist.gov/ai-measurement-and-evaluation
- https://www.nist.gov/artificial-intelligence/ai-research/tevv-athlon-framework-evaluating-ai-systems
- https://airc.nist.gov/airmf-resources/playbook/measure/

### Google SRE — Testing for Reliability

Google SRE frames testing as a way to quantify confidence in system reliability. Passing tests do not prove reliability absolutely, while failures often prove absence of reliability. System/integration/configuration testing, monitoring and realistic production probes are distinct evidence layers.

Professional implication: green unit tests are insufficient when the actual live evaluation path has not been exercised. The role must know when deterministic proof is enough and when a small representative live canary is still necessary.

Source: https://sre.google/sre-book/testing-reliability/

### Google SRE — Canarying releases

Canaries should be small, attributable and representative. Test environments are not identical to production, so controlled exposure to real execution is used to discover defects absent from artificial tests.

Professional implication: a canary earns value only if it exercises the same relevant provider/runtime/transport semantics as the expensive scored path. A convenient but non-representative canary is false reassurance.

Source: https://sre.google/workbook/canarying-releases/

### Google Gemini — Background execution

Google documents that long-running reasoning can exceed ordinary HTTP connection lifetimes and provides background Interactions + retrieval/polling for supported models. Background execution introduces storage/retention implications and therefore cannot be silently substituted for non-stored hidden evaluation material.

Professional implication: transport reliability, idempotency and privacy eligibility are coupled decisions.

Source: https://ai.google.dev/gemini-api/docs/background-execution

## 4. Responsibility boundary

### Agent Architect owns
- target profession architecture;
- competency/evidence requirements;
- qualification scope and governance;
- independence requirements;
- professional release lifecycle;
- stop-loss policy.

### Independent Evaluator owns
- profession-specific fixtures and adversarial construct coverage;
- grader/judge logic and professional calibration;
- thresholds/hard fails;
- interpretation of valid professional evidence;
- PASS / REVISE / FAIL when infrastructure produced valid evidence.

### Qualification Reliability Engineer owns
- executability and dependency/runtime contract of the evaluation machinery;
- observability sufficient to determine what actually executed;
- deterministic pre-run validation and fault-injection strategy;
- idempotency/retry safety at provider boundaries;
- canary representativeness assessment;
- quota/token/call/time/cost exposure and retry accounting;
- checkpoint/resume safety;
- infrastructure failure classification;
- incident mechanism isolation and bounded repair design;
- regression proof and recurrence prevention;
- GO / NOT_READY / NOT_EXECUTABLE for the evaluation machine.

### Explicit non-ownership
The Reliability Engineer must not silently change:
- candidate professional behavior;
- evaluator fixtures;
- professional judges/graders;
- thresholds or hard fails;
- hidden/held-out semantics;
- professional release criteria.

## 5. Core work products

A strong practitioner produces auditable artifacts, not only advice:

1. Qualification Readiness Report
   - exact execution-chain identity;
   - candidate/evaluator/runtime identities;
   - dependency map;
   - required observables;
   - unresolved infrastructure risks;
   - GO / NOT_READY.

2. Runtime & Dependency Contract
   - provider/API/model/runtime/SDK or protocol;
   - timeout nesting;
   - state/storage requirements;
   - secret requirements;
   - artifact/checkpoint paths;
   - retry/idempotency semantics.

3. Failure-Mode Register
   - failure mechanism;
   - detection layer;
   - whether deterministic simulation is possible;
   - impact on evidence/cost/privacy;
   - fail-closed behavior.

4. Fault-Injection Matrix
   - timeout, connection reset, 408/429/5xx/4xx;
   - malformed/partial response;
   - duplicate/ambiguous create;
   - polling/retrieval failure;
   - missing secret;
   - schema drift;
   - path/import failure;
   - artifact/report failure;
   - runner crash;
   - checkpoint/resume corruption.

5. Pre-run Budget Ledger
   - maximum candidate calls;
   - maximum judge calls;
   - retries by failure class;
   - maximum wall-clock;
   - expected token/cost range where material;
   - protected quota reserve;
   - stop condition;
   - checkpoint/resume policy.

6. Live Run Accounting
   - attempted vs completed calls;
   - valid evidence produced;
   - retries;
   - wall-clock;
   - quota/cost exposure;
   - infrastructure/professional classification.

7. Incident / Postmortem Record
   - observed facts;
   - evidence boundary;
   - mechanism hypotheses;
   - discriminating tests;
   - selected root cause;
   - repair scope;
   - regression evidence;
   - residual uncertainty.

## 6. Tacit professional judgment

The differentiator is not knowing a retry library or writing unit tests. It is correctly deciding what evidence is needed before spending scarce execution budget.

### J1 — Ambiguous create acceptance
If a POST times out after the provider may have accepted the request, a blind retry can duplicate model work and spend. The correct response may be STOP/uncertain rather than retry.

### J2 — Representative canary
A canary is valid only if it traverses the failure-relevant path of the scored run. A different API, timeout, executor, storage mode or tool protocol can make it irrelevant.

### J3 — Deterministic confidence vs live proof
Mocks/fault injection can prove fail-closed behavior and retry logic, but cannot prove a volatile provider contract works live. Conversely, a full scored suite is an unnecessarily expensive provider probe.

### J4 — Infrastructure change vs evidence comparability
Changing model/provider/transport can preserve professional semantics in some cases and invalidate frozen comparability in others. This is an evidence-validity judgment, not a syntax check.

### J5 — Preserve completed evidence
When execution is resumable without contamination or protocol drift, preserve valid completed cases. Restarting everything may waste quota and alter stochastic evidence unnecessarily.

### J6 — Stop rather than optimize
When the remaining uncertainty cannot be resolved within the execution-chain budget without violating stop-loss, the professional result is `NOT_EXECUTABLE`, not an invitation to open another repair chain.

### J7 — Avoid ceremonial over-testing
Not every evaluation needs chaos engineering, multiple providers or elaborate load tests. Choose the smallest evidence set that closes the material failure modes. Reliability engineering itself can become wasteful if not bounded.

## 7. Failure taxonomy

Minimum operational taxonomy:

- `PROFESSIONAL_RESULT` — valid execution completed; result belongs to evaluator.
- `PROFESSION_SPECIFIC_EVALUATOR_DEFECT` — construct/grader/fixture defect local to the profession evaluation.
- `PROVIDER_TRANSIENT_OR_QUOTA` — provider availability/rate/quota interruption without evidence of local defect.
- `LOCAL_EXECUTION_OR_TRANSPORT_FAIL` — runner/transport/environment defect local to current path.
- `GENERIC_PLATFORM_REOPEN_CANDIDATE` — concrete evidence may satisfy issue #129 reopen criteria.
- `NOT_EXECUTABLE` — valid professional evidence cannot be completed under current frozen contract/budget.

Classification must be evidence-backed. `0 candidate calls` or `0 judge calls` is highly material but not by itself sufficient to name the root cause.

## 8. Architecture alternatives

### Alternative A — keep everything inside Agent Architect

Strengths:
- no new role boundary;
- Architect already knows qualification governance.

Weaknesses:
- overloads profession design with production reliability operations;
- encourages infrastructure work to grow inside every qualification cycle;
- weak separation between the party designing the evaluation lifecycle and the party certifying its technical readiness;
- repository history shows this responsibility has already diffused across ad hoc fixes.

Decision: REJECT as sole architecture.

### Alternative B — deterministic software-only guard

Strengths:
- cheap, reproducible, fail-closed;
- ideal for schema, paths, secrets presence, timeout arithmetic, trigger policy, artifact contracts and synthetic fault injection.

Weaknesses:
- cannot reliably decide whether a canary is representative;
- cannot reason about measurement validity or comparability after runtime changes;
- cannot choose the smallest discriminating experiment under novel incidents;
- cannot determine when live evidence is necessary vs wasteful;
- cannot perform a serious postmortem on an unknown unknown from rules alone.

Decision: REJECT as sole architecture; retain as mandatory mechanical layer.

### Alternative C — standalone agent-only Reliability Engineer

Strengths:
- handles novel incidents and contextual trade-offs.

Weaknesses:
- mechanical fail-closed invariants should not depend on model judgment;
- agent-only enforcement can hallucinate, drift or approve an unsafe run;
- using model judgment to decide whether model spend is allowed is circular when deterministic proof is available.

Decision: REJECT as sole architecture.

### Alternative D — hybrid professional + deterministic guard

Professional core owns diagnosis, evidence design, canary validity, cost/retry strategy, comparability and incident judgment. Deterministic guard owns mechanically observable fail-closed gates and fault-injection regressions.

Decision: **ADOPT**.

## 9. Proposed operating workflow

`qualification claim -> runtime/dependency map -> failure-mode analysis -> deterministic/static gates -> synthetic fault injection -> budget/retry gate -> representative canary only if unresolved live risk remains -> GO / NOT_READY -> live accounting -> classify result -> bounded repair if authorized -> regression -> maintenance mode`

The Independent Evaluator consumes the machinery only after readiness is established; the Reliability Engineer does not consume or reinterpret hidden professional answers beyond what is needed to validate transport/infrastructure contracts.

## 10. Feedback loops

- CI/static regression catches known mechanical defects before credentials.
- Fault injection proves failure behavior without provider spend.
- Small representative canaries test volatile provider assumptions.
- Live run accounting reveals escaped defects and cost regressions.
- Incident postmortems feed regression cases.
- Cross-profession recurrence can justify generic platform reopen under #129.
- Cost accounting should show decreasing provider calls spent solely on discovering infrastructure defects.

## 11. Unknown unknowns / research gaps

Still unresolved before a candidate SKILL can be written:
- exact boundary between evaluation scientist and reliability engineer for construct-validity disputes;
- minimum standard for declaring a canary representative across provider SDK/API-version drift;
- objective readiness metrics for infrastructure beyond binary preflight;
- how to quantify acceptable flakiness for provider-dependent qualification stages;
- retention/privacy decision template across providers and hidden material;
- whether provider-level idempotency keys are available/appropriate for each supported API path;
- portability contract for Codex/Claude Code/subscription-backed execution vs metered APIs.

These require targeted knowledge/evidence work, not generic prompt additions.

## 12. Red-team review

### Senior SRE critique
A checklist-only role would miss live-path equivalence, attribution, stateful retry hazards and the difference between hermetic tests and production evidence. The hybrid architecture addresses this by making live canary judgment explicit while retaining mechanical gates.

### Evaluation scientist critique
Technically green CI can still measure the wrong construct. Therefore the role is prohibited from owning professional construct validity; it must surface infrastructure changes that affect elicitation/comparability back to the Independent Evaluator/Architect.

### Staff test engineer critique
Happy-path preflight is insufficient. Fault injection and negative controls must prove fail-closed behavior, retry/idempotency semantics and artifact/accounting behavior.

### Hiring-manager critique
A useful specialist must diagnose ambiguous incidents, write discriminating experiments, quantify blast radius/cost, and say STOP when evidence is insufficient — not merely operate CI.

## 13. Current Architect decision

`BUILD NEW professional core + REUSE/EXTEND deterministic qualification-platform capabilities`.

Do not create a new generic qualification platform. Build a reusable judgment layer around the already existing platform controls, and extend deterministic enforcement only when a concrete competency claim requires it and current maintenance-mode governance authorizes the change.
