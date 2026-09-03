# Qualification Reliability Engineer 0.1.0 — independent qualification plan

Status: **PREREGISTERED PLAN — candidate not yet frozen or qualified**
Issue: #265
Date: 2026-09-03

## 1. Purpose

Qualify the reusable `qualification-reliability-engineer-core` as a professional reliability judgment layer paired with its deterministic readiness guard.

The release claim is narrow and operational:

> Given an AI-agent qualification/evaluation system, the core can determine whether the measurement machinery is trustworthy, executable, observable, bounded and cost-safe enough to run; can distinguish infrastructure failure from professional candidate evidence; can design the smallest valid diagnostic/repair evidence; and can enforce stop-loss without weakening professional qualification.

This qualification does **not** claim the core is a universal SRE, security engineer, evaluation scientist or provider expert.

## 2. Candidate components to freeze after merge

Freeze all behavior-bearing components together:
- `candidate/SKILL.md`;
- `professional-model-candidate-v0.1.md`;
- `candidate/guard/readiness-report.schema.json`;
- `candidate/guard/validate_readiness_report.py`.

Bind exact merged commit and Git blob identities in a separate freeze record after this candidate PR merges. The candidate guard regression test is release-supporting evidence and should also be recorded by blob identity, but changing only tests after freeze must not silently change candidate behavior.

## 3. Scope

First release qualification: **FULL**.

No historical QRE professional PASS exists. Research/prototype tests are development evidence only.

Required lifecycle:

`candidate merge -> exact freeze -> deterministic candidate/guard preflight -> fresh independent held-out authoring -> judge/rubric calibration -> semantic/adversarial qualification -> executable practical tasks -> sanitized report -> PASS | REVISE | FAIL | NOT_EXECUTABLE`

No Professional Core Library admission before PASS.

## 4. Independence boundary

The independent evaluator must:
- author fresh held-out/adversarial cases after freeze;
- not reuse hidden Visual/Sales/Conversion Messaging release fixtures;
- use only public/sanitized repository incidents as development/reference material;
- not tune the frozen QRE candidate against held-out outcomes;
- keep professional evaluator judgments independent of the candidate authoring context;
- preserve current stop-loss rules for this qualification's own infrastructure.

## 5. Required competency coverage

Held-out coverage must represent all CORE and BOUNDARY-CRITICAL competencies from `architect/research/qualification-reliability-engineer/competency-map-v0.1.md`, including at least:

- evidence-machine traceability;
- runtime/dependency contract engineering;
- deterministic preflight decomposition;
- fault injection;
- API transport/idempotency;
- representative canary design;
- observability/run accounting;
- resource/quota/cost engineering;
- evidence preservation/resume;
- measurement-validity boundary;
- secrets/privacy/retention;
- incident diagnosis/smallest discriminating experiment;
- bounded repair/regression closure;
- flakiness/repeated-trial reasoning;
- readiness gating;
- cross-profession recurrence/#129 reopen reasoning;
- provider/API live-research routing and escalation.

Repository-specific GitHub skill is practical context, not the universal profession construct.

## 6. Mandatory adversarial families

Fresh cases must include equivalents of these mechanisms without copying development fixture wording:

1. deterministic blocker hidden behind a proposed paid canary;
2. ambiguous non-idempotent create timeout;
3. safe idempotent retrieval retry contrast;
4. quota interruption after substantial valid partial evidence;
5. materially non-representative canary that looks superficially convincing;
6. transport/provider migration that threatens evidence comparability;
7. provider storage required for hidden material where retention is not authorized;
8. stale/cross-run artifact that would falsely imply PASS;
9. same-stage retry-budget reset disguised as a new provider/issue;
10. cross-profession recurrence that actually justifies #129 generic reopen;
11. one-off local defect that does **not** justify generic platform work;
12. overengineering trap where simple deterministic closure is sufficient;
13. negative control where the correct professional decision is `GO`, not defensive over-blocking;
14. ambiguous generic provider error where root cause is not yet established;
15. stochastic candidate variance mixed with independent infrastructure flakiness.

## 7. P0 hard fails

Any observed P0 is release failure regardless of aggregate score:

1. Authorizes scored/paid/model execution while a deterministically detectable release-critical infrastructure blocker remains.
2. Reports candidate professional PASS/FAIL from a run that did not produce valid candidate evidence.
3. Blindly retries an ambiguous non-idempotent create/model call with duplicate execution/spend risk.
4. Silently changes frozen candidate, fixture, judge/grader, threshold, hard-fail or professional semantics as an infrastructure repair.
5. Resets an exhausted same-stage repair/retry budget through a new issue/provider/transport/branch.
6. Exposes held-out/sealed material through unauthorized provider storage, logs or transport.
7. Discards valid compatible completed evidence and restarts material expensive work without a validity reason.
8. Treats a materially non-representative canary as proof of scored-runtime executability.
9. Uses stale/cross-run artifacts as current release evidence.
10. Continues generic qualification-platform engineering after bounded closure without applicable current #129 reopen evidence.

## 8. Practical executable gate — mandatory

Prose-only answers cannot PASS this core.

### P1 — Readiness review

Given a small realistic qualification repository/workflow packet, candidate must produce:
- exact execution-chain identity;
- evidence/runtime dependency map;
- failure-mode register;
- deterministic vs live evidence routing;
- canary requirement + representativeness rationale;
- pre-run candidate/judge/retry/wall-clock budget;
- privacy/storage decision;
- `GO | NOT_READY | NOT_EXECUTABLE`.

The packaged deterministic guard must accept/reject the machine-readable readiness report consistently with the candidate's professional decision on mechanical invariants.

### P2 — Unsafe retry repair

Given a synthetic transport helper that blindly retries an ambiguous create:
- identify the duplicate-execution risk;
- make the smallest repair;
- add executable zero-network regressions;
- prove exact call method/count behavior;
- prove safe retrieval retry is not incorrectly prohibited where valid.

### P3 — Novel incident diagnosis

Given a sanitized repository-like failure with incomplete evidence:
- separate facts from hypotheses;
- identify at least one serious alternative mechanism;
- choose the smallest discriminating experiment;
- avoid unsupported root-cause certainty;
- bind current stop-loss budget and next allowed action.

### P4 — Interrupted-suite preservation/accounting

Given partial valid evidence, quota/runtime interruption and run ledger:
- preserve valid compatible evidence;
- decide whether resume is valid;
- reconcile attempted/completed calls and retries;
- compute remaining worst-case exposure;
- avoid blind restart.

### P5 — Generic-reopen decision

Given incidents across multiple profession evaluators:
- distinguish repeated generic blind spot from unrelated local/provider failures;
- apply exact current #129 reopen criteria;
- propose the smallest reusable control only when justified;
- otherwise keep generic platform in maintenance mode.

## 9. Mechanical grading

Use deterministic/environment grading for mechanically observable claims:
- readiness-report schema validity;
- guard verdict behavior;
- exact call method/count in synthetic retry tests;
- no network/provider use in zero-call tasks;
- budget arithmetic;
- stale artifact/run identity rejection;
- stop-loss state;
- test execution success/failure.

Candidate-written tests must be mutation/discrimination checked where feasible: demonstrate they fail on representative unsafe behavior, not merely pass on the repaired code.

## 10. Judgment grading and calibration

Judgment-heavy dimensions require calibrated professional review:
- canary representativeness;
- incident mechanism reasoning;
- smallest discriminating experiment quality;
- comparability/evidence-validity boundary;
- residual-risk prioritization;
- overengineering vs sufficient reliability;
- escalation quality.

Before scored candidate outcomes, freeze:
- rubric dimensions;
- P0 policy;
- reference judgments/calibration exemplars;
- judge identities/configuration if model judges are used;
- deterministic grader identities;
- disagreement/adjudication policy;
- threshold/repeat policy;
- stop/resource conditions.

Do not use one uncalibrated scalar LLM score as release evidence.

Calibration set must include at least:
- unsafe/naive solution;
- mechanically competent but shallow solution;
- strong staff-level solution;
- overengineered solution;
- negative control where allowing the run is correct.

## 11. Threshold policy

Exact numeric thresholds are **not frozen in this document** because calibration has not yet established defensible cutoffs.

Before first scored candidate outcome, evaluator must freeze thresholds based on calibration evidence. Regardless of numeric threshold:
- P0 count must be zero;
- all mandatory P1-P5 practical gates must be executable;
- no practical gate may be substituted by narrative simulation;
- critical CORE families must meet the calibrated competency floor;
- mechanical assertions must pass their executable verifiers.

If calibration cannot support a defensible threshold, status is `NOT_EXECUTABLE`/evaluation-design incomplete rather than inventing a convenient number.

## 12. Resource and execution routing

Qualification of the reliability role must itself demonstrate resource discipline.

Required order:
1. deterministic/static candidate + guard validation;
2. reusable sanitized repository evidence;
3. fresh held-out authoring using an eligible independent route;
4. local executable practical tasks;
5. model-assisted professional judging only where irreducible;
6. live provider canary only if a specific QRE competency cannot be validly tested synthetically/local and after explicit preregistration.

Prefer subscription-backed independent execution/judging such as Codex or Claude Code when it preserves independence, observability and frozen semantics. Metered API is not default.

No parallel provider-heavy qualification runs.

Before any material model-assisted run record:
- max candidate calls;
- max judge calls;
- max retries;
- max wall-clock;
- quota/plan state if observable;
- stop-loss chain identity;
- exact stop condition.

## 13. Infrastructure stop-loss for this qualification

This QRE qualification is not exempt from `qualification-stop-loss.md`.

Each distinct qualification stage has an execution-chain record. Same-stage technical failure follows:

`classify -> at most one bounded repair if authorized -> exact regression -> one eligible retry -> STOP on another technical defect`

Do not create a reliability-engineering agent by reproducing the same unbounded reliability-engineering failure mode it is meant to prevent.

## 14. Public-safe qualification record

Final sanitized record must bind:
- exact frozen candidate commit and component blobs/digests;
- held-out/evaluator cycle identity;
- rubric/grader/calibration identity;
- thresholds/P0/repeat/stop policy;
- runtime/executor environment;
- semantic family outcomes;
- practical P1-P5 outcomes and executable artifacts;
- call/retry/resource accounting;
- known limitations;
- final verdict `PASS | REVISE | FAIL | NOT_EXECUTABLE`.

## 15. Release rule

Only `PASS` permits:
- Professional Core Library admission;
- use as an authoritative reliability gate for other agents' qualification flows.

Until then the v0.1 artifacts remain candidate/research infrastructure and may not be represented as a qualified professional core.
