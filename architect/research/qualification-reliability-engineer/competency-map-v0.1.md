# Qualification Reliability Engineer — competency map v0.1

Status: Architect research artifact. Not a SKILL. Not qualified.
Issue: #265
Date: 2026-09-03

## Classification

- `CORE` — indispensable to the profession.
- `BOUNDARY-CRITICAL` — protects validity, cost, privacy or role separation.
- `ESCALATION` — recognizes when another specialist/provider owner is required.
- `CONTEXTUAL` — useful in some stacks, not universal.

## QR-01 — Evaluation-machine traceability
Type: CORE

Purpose: map the professional claim to the exact machinery that can produce or invalidate the evidence.

Observable capability:
- traces `claim -> fixture/input -> candidate runtime -> tools/state -> judge/verifier -> report/artifact -> verdict`;
- identifies which component owns each transformation;
- identifies where an infrastructure failure can masquerade as professional failure.

Expert cues:
- different runtime path between canary and scored execution;
- hidden implicit configuration;
- missing observable between provider call and recorded verdict;
- report says FAIL while candidate execution never completed.

Failure modes:
- treating workflow green/red status as professional evidence;
- assuming candidate_calls counter proves provider acceptance semantics;
- failing to bind runtime/model/transport identity to the evidence record.

Evaluation: given a sanitized workflow with three plausible failure points, produce the dependency/evidence chain and correctly identify which facts can and cannot support a professional verdict.

## QR-02 — Runtime and dependency contract engineering
Type: CORE

Observable capability:
- specifies provider/API/model/protocol/runtime/SDK/tool/state/storage/secret/artifact dependencies;
- validates timeout nesting and outer budgets;
- distinguishes static compatibility from live provider compatibility.

Failure modes:
- distributed implicit configuration;
- canary/scored drift;
- timeout arithmetic that guarantees inner failure before outer budget;
- missing import/path/secret discovered only after provider eligibility.

Evaluation: reconstruct an exact runtime contract from repo/workflow evidence and detect contract drift before a provider call.

## QR-03 — Deterministic preflight decomposition
Type: CORE

Purpose: move deterministically detectable defects before credentials/provider calls.

Observable capability:
- classifies each uncertainty as static, synthetic, local integration, live canary or scored-only;
- designs fail-closed zero-provider checks where valid;
- refuses to spend model calls on questions a deterministic test can answer.

Failure modes:
- using full qualification as diagnostic;
- false confidence from superficial syntax checks;
- ceremonial checks with no link to a real failure mechanism.

Evaluation: choose the cheapest sufficient evidence layer for a mixed set of infrastructure questions.

## QR-04 — Fault injection and negative-path testing
Type: CORE

Observable capability:
- creates synthetic failure cases for timeout, connection reset, 408/429/5xx/4xx, malformed response, partial state, missing secret, import/path failure, artifact/report failure, runner crash and checkpoint corruption;
- verifies fail-closed classification and retry policy;
- tests recovery path as well as happy path.

Professional judgment:
- inject the failure at the correct boundary; a mock at the wrong layer can prove nothing about the real mechanism.

Evaluation: implement or specify executable zero-network tests that prove exact retry/no-retry semantics.

## QR-05 — Distributed/API transport and idempotency judgment
Type: CORE

Observable capability:
- distinguishes safe idempotent retrieval retry from ambiguous non-idempotent creation retry;
- reasons about server acceptance uncertainty;
- preserves interaction/request identity when possible;
- identifies duplicate-call/spend risk.

P0 candidate:
- blindly retries an ambiguous creation call that may already have been accepted.

Evaluation: adversarial timeout-after-acceptance case; candidate must refuse blind POST retry and design an evidence-preserving recovery/STOP path.

## QR-06 — Representative canary design
Type: CORE

Observable capability:
- determines which runtime dimensions must match the scored path;
- rejects canaries that differ on the failure-relevant provider/API/executor/storage/tool/state/timeout contract;
- minimizes canary size while preserving diagnostic value.

Failure modes:
- proving the wrong API works;
- canarying a cheap model when model identity affects protocol/latency behavior;
- claiming executability from a no-op health check.

Evaluation: compare three canary proposals and identify which one actually reduces the live uncertainty.

## QR-07 — Observability and run accounting
Type: CORE

Observable capability:
- records attempted vs completed candidate/model/judge calls;
- distinguishes request submission, provider acceptance, usable output and persisted evidence;
- captures failure class without leaking secrets/held-out content;
- binds artifacts/checkpoints to run identity.

Failure modes:
- counters that increment only after success and therefore hide attempted spend;
- logs insufficient to distinguish executor crash from provider rejection;
- leaking hidden fixtures in diagnostics.

Evaluation: given ambiguous logs, state what additional observables are required and what conclusions remain unsupported.

## QR-08 — Resource, quota and cost engineering
Type: CORE

Observable capability:
- creates a PRE-RUN BUDGET GATE;
- bounds candidate calls, judge calls, retries, wall-clock, quota reserve and expected spend/tokens where material;
- designs checkpoint/resume to avoid repeating valid work;
- performs post-run accounting and detects unexplained cost regression.

P0 candidate:
- authorizes a broad paid rerun when targeted deterministic evidence can answer the infrastructure question.

Evaluation: calculate worst-case call exposure from a staged plan including retries and explain the stop condition.

## QR-09 — Evidence preservation and resumability
Type: CORE

Observable capability:
- determines whether completed cases remain valid after an interruption;
- preserves immutable evidence/checkpoints where protocol permits;
- distinguishes safe resume from contamination/comparability invalidation.

Failure modes:
- discarding all valid completed evidence;
- resuming after a semantic change that invalidates prior cases;
- reconstructing hidden material from public artifacts.

Evaluation: interrupted 36-case qualification with 30 valid records and transport failure; decide exactly what can be reused.

## QR-10 — Measurement-validity boundary management
Type: BOUNDARY-CRITICAL

Observable capability:
- recognizes when infrastructure changes alter elicitation, population, runtime or observability enough to threaten comparability;
- escalates construct/grader implications to Architect/Independent Evaluator;
- does not reinterpret professional thresholds itself.

Failure modes:
- changing provider/judge/runtime and claiming evidence continuity without justification;
- overreaching into profession-specific scoring.

Evaluation: migration scenario where transport-only change is safe in one case but provider/model switch is not.

## QR-11 — Secrets, privacy, retention and held-out transport
Type: BOUNDARY-CRITICAL

Observable capability:
- maps secrets and hidden data exposure;
- distinguishes provider storage requirements from local processing;
- refuses background/stored execution when held-out contract forbids retention;
- ensures diagnostics sanitize hidden content and secrets.

P0 candidate:
- moves sealed/held-out material to a stored provider path without explicit authorization.

Evaluation: choose an eligible transport for public development vs sealed release material with differing storage rules.

## QR-12 — Incident diagnosis and smallest discriminating experiment
Type: CORE

Observable capability:
- separates facts, hypotheses and unknowns;
- narrows the failure boundary;
- proposes alternatives;
- chooses the smallest experiment that distinguishes the leading mechanisms;
- avoids changing multiple variables simultaneously.

Expert-vs-average discriminator:
Average operator sees `HTTP 400` and edits retry code. Strong practitioner asks whether request format, retrieval route, API revision, resource identity, provider state or local parsing is actually responsible, then designs evidence to discriminate them.

Evaluation: novel sanitized provider failure with incomplete evidence; candidate must not jump to unsupported root cause.

## QR-13 — Bounded repair and regression closure
Type: CORE

Observable capability:
- applies current stop-loss chain identity;
- repairs the correct layer only when authorized;
- adds an exact regression/fault-injection case;
- requires live proof only if deterministic regression cannot close the relevant uncertainty;
- returns infrastructure to maintenance mode.

P0 candidate:
- opens a new issue/provider/transport to reset the same exhausted stage.

Evaluation: post-failure plan must obey `one bounded repair -> one eligible retry -> STOP` for the same chain.

## QR-14 — Flakiness and repeated-trial reasoning
Type: CORE

Observable capability:
- distinguishes deterministic defect, stochastic candidate behavior and flaky infrastructure;
- avoids classifying one transient as a systemic defect without evidence;
- does not hide recurrent failures by averaging them into a pass rate;
- uses repeated trials only when the inference requires them.

Evaluation: mixed repeated outcomes from candidate and transport; partition the sources of variance and propose valid next evidence.

## QR-15 — Release/readiness gating
Type: CORE

Observable capability:
- issues evidence-backed `GO`, `NOT_READY`, or `NOT_EXECUTABLE` for infrastructure;
- blocks scored/paid execution when a release-critical infrastructure risk is unresolved;
- avoids blocking when only non-material optional hardening remains.

Failure mode:
- gold-plating the platform until qualification never happens.

Evaluation: prioritize a risk register into must-fix before run, canary-only uncertainty, and backlog.

## QR-16 — Cross-profession recurrence detection
Type: BOUNDARY-CRITICAL

Observable capability:
- recognizes repeated infrastructure mechanisms across profession evaluators;
- separates one-off local defect from generic blind spot;
- applies issue #129 reopen criteria with concrete evidence.

Evaluation: compare incidents from Sales, Visual and Conversion Messaging and decide whether generic platform reopening is justified.

## QR-17 — Tooling/repository execution competence
Type: CONTEXTUAL but operationally required in this repository

Observable capability:
- reads workflows, runner code, manifests, CI logs and artifacts;
- writes deterministic tests and small infrastructure patches;
- uses version control/PRs without contaminating candidate/held-out boundaries.

Boundary:
The core should be portable; GitHub Actions is current implementation context, not the profession definition.

## QR-18 — Provider/API documentation and live research
Type: BOUNDARY-CRITICAL

Observable capability:
- checks current official provider/API docs for volatile runtime behavior;
- records version/date/assumptions;
- avoids relying on stale model knowledge for endpoints, retention, limits or supported modes.

Evaluation: provider feature changed recently; candidate must research authoritative docs before prescribing a repair.

## QR-19 — Escalation to provider/domain specialist
Type: ESCALATION

Observable capability:
- recognizes when remaining uncertainty requires provider support, security/privacy owner, evaluation scientist or domain evaluator;
- packages a minimal reproducible evidence set rather than vague escalation.

Evaluation: undocumented persistent provider response after local contract validation; produce a provider escalation packet and STOP criteria.

## Knowledge packaging implications

Likely `EMBED_CORE`:
- ownership boundary;
- failure taxonomy;
- evidence-layer selection logic;
- retry/idempotency principles;
- stop-loss governance;
- GO/NOT_READY/NOT_EXECUTABLE semantics.

Likely `PROCEDURAL_MODULE`:
- pre-run readiness review;
- incident diagnosis;
- fault-injection design;
- post-run accounting;
- regression closure.

Likely `REFERENCE_MODULE`:
- repository-specific failure classes;
- qualification-platform contracts;
- incident exemplars.

Likely `LIVE_RESEARCH`:
- provider API behavior;
- model availability;
- quotas/pricing/retention;
- SDK/API versions and limits.

Likely `TOOL_BACKED`:
- workflow/static inspection;
- deterministic preflight;
- fault injection;
- CI/artifact/log inspection;
- call/cost accounting.

## Current critical gaps before SKILL authoring

1. Define a compact, enforceable readiness-report schema.
2. Define a deterministic guard contract that complements rather than duplicates professional judgment.
3. Calibrate how canary representativeness is graded.
4. Create repository-derived sanitized incident fixtures without leaking held-out material.
5. Define practical execution task where the candidate must actually inspect/repair a broken harness and prove the fix with zero-network regressions.
6. Determine exact P0 list after adversarial design review.
