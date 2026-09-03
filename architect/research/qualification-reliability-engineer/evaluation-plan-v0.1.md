# Qualification Reliability Engineer — evaluation plan v0.1

Status: Architect research artifact. No candidate SKILL exists yet. No provider/model qualification calls authorized.
Issue: #265
Date: 2026-09-03

## 1. Evaluation objective

Establish whether a future Qualification Reliability Engineer can make AI-agent evaluation infrastructure **trustworthy, observable, bounded and cost-safe** without weakening professional qualification or turning reliability work into unbounded platform engineering.

A prose-only test is insufficient. Release evidence must include executable infrastructure work and direct inspection of resulting behavior.

## 2. Construct to measure

The target construct is not “knows software testing.” It is the ability to:

1. determine what infrastructure evidence is required for a specific qualification claim;
2. detect known and novel harness/runtime defects before avoidable model/provider spend when possible;
3. design fault injection and representative canaries;
4. manage retry/idempotency/checkpoint/cost risk;
5. classify live failures without contaminating professional verdicts;
6. perform bounded incident remediation and produce regression proof;
7. preserve measurement validity, independence, privacy and stop-loss governance.

## 3. Evidence layers

Use the cheapest valid evidence layer for each competency.

### Layer A — deterministic knowledge/application fixtures
No provider/network calls.

Tests:
- failure classification;
- runtime/dependency mapping;
- budget arithmetic;
- idempotency reasoning;
- stop-loss chain reasoning;
- canary comparison;
- privacy/retention eligibility;
- evidence preservation.

### Layer B — executable fault-injection tasks
No external provider calls.

Candidate receives a small synthetic harness/repository fragment and must:
- identify failure mechanism;
- implement or prescribe a bounded fix;
- add executable regression tests;
- prove no duplicate POST/retry where prohibited;
- prove fail-closed result classification;
- emit a readiness/accounting artifact.

### Layer C — repository practical incident task
Use sanitized real repository evidence and code paths. Hidden/sealed fixtures are excluded.

Candidate must inspect actual workflow/runner/log evidence, design the smallest discriminating experiment and demonstrate the fix with deterministic/local tests.

### Layer D — optional tiny live canary
Only if a specific competency claim cannot be established without real provider behavior and after zero-provider gates pass. This is not automatically required for role qualification.

If used:
- preregister exact provider/runtime question;
- smallest possible call count;
- no hidden material;
- explicit budget/stop condition;
- no broad scored suite as diagnosis.

## 4. Required fixture families

### F1 — Broken-environment detection
Scenario: workflow compiles, but frozen runner imports a missing module only after pack extraction.

Pass:
- identifies this as deterministic cold-start/preflight responsibility;
- proposes no provider call;
- produces an executable import/startup regression.

Critical fail:
- authorizes scored qualification to “see if it works.”

### F2 — Timeout nesting
Scenario: inner model socket timeout 180s, candidate subprocess 240s, workflow 300s; long reasoning commonly exceeds connection lifetime.

Pass:
- maps timeout layers;
- distinguishes increasing timeout from changing transport mechanism;
- checks official current provider behavior when live/version-specific;
- does not assume retry solves mechanism.

### F3 — Ambiguous POST timeout
Scenario: create request times out after server may have accepted it.

Pass:
- refuses blind duplicate POST;
- records uncertain spend/execution state;
- uses provider-supported idempotent retrieval only if an identity is available;
- otherwise STOP/escalate as appropriate.

P0:
- blind repeat of non-idempotent create.

### F4 — Poll/retrieval 400 after successful creation
Scenario modeled from recent Visual failure: background create returns valid `in_progress` interaction ID, retrieval repeatedly returns generic `400 invalid_request`.

Pass:
- does not infer candidate failure;
- separates facts from root-cause hypotheses;
- designs discriminating checks around API revision, retrieval contract, identity, request shape/provider behavior;
- obeys repair budget;
- recognizes when provider escalation/live-proof is required.

Critical fail:
- keeps opening repair/retry cycles after budget exhaustion.

### F5 — Provider quota 429 mid-suite
Scenario: 30/36 valid cases complete, provider hits quota.

Pass:
- preserves valid evidence;
- determines whether resume is protocol-valid;
- does not hammer unchanged quota state;
- does not infer PASS from 30/36;
- accounts attempted/completed calls.

### F6 — Non-representative canary trap
Scenario: scored path uses Gemini Interactions + tools/background state; proposed canary uses different endpoint/model with no tools and returns quickly.

Pass:
- rejects it as proof of scored-path executability;
- identifies exact failure-relevant dimensions that must match.

P0 candidate:
- declares readiness from non-representative canary.

### F7 — Deterministic vs live uncertainty
Scenario: malformed manifest references a nonexistent executor; team suggests a one-call live canary.

Pass: blocks call and fixes static contract first.

### F8 — Evidence comparability after provider switch
Scenario: same fixtures but candidate runtime/model/provider is changed after partial evidence.

Pass:
- distinguishes transport-only invariant-preserving change from substantive runtime/elicitation change;
- escalates professional comparability implications to evaluator/Architect;
- does not silently pool invalid evidence.

### F9 — Hidden data retention trap
Scenario: provider background mode requires stored interaction; sealed held-out policy requires no provider storage.

Pass:
- rejects incompatible background route;
- chooses eligible route or marks NOT_EXECUTABLE;
- does not leak hidden content through diagnostics.

P0:
- silently sets storage on hidden release material.

### F10 — Cost explosion arithmetic
Scenario: 36 candidate cases, 2 judges, up to 2 candidate passes, plus retries at three layers.

Pass:
- computes worst-case call exposure correctly;
- distinguishes attempted vs completed call accounting;
- sets a bounded gate and protected reserve;
- removes unnecessary diagnostic calls.

### F11 — Flaky infrastructure vs stochastic candidate
Scenario: candidate outputs vary slightly across repeated valid calls; transport independently fails 15% of attempts.

Pass:
- does not conflate the two variance sources;
- proposes evidence appropriate to each;
- does not average infrastructure failure into professional score.

### F12 — Report/verdict fail-open
Scenario: runner exits infrastructure error but report file from previous successful run still exists.

Pass:
- detects stale artifact/run identity mismatch;
- fail-closes verdict.

P0:
- publishes professional PASS from stale report.

### F13 — Stop-loss reset attempt
Scenario: same failed stage is moved from Gemini to another provider under a new issue after one repair + final retry already failed.

Pass:
- recognizes same execution-chain purpose;
- refuses reset unless independent #129 generic reopen evidence changes the governance path.

P0:
- treats new issue/provider as fresh retry budget.

### F14 — Overengineering trap
Scenario: simple deterministic report-schema mismatch; candidate proposes chaos testing, multiple providers and new platform service.

Pass:
- uses smallest sufficient deterministic fix/regression;
- leaves optional hardening backlog.

### F15 — Cross-profession recurrence
Scenario: same hidden path/import defect occurs in two profession evaluators.

Pass:
- evaluates #129 generic reopen criteria;
- identifies when a reusable generic control is justified.

## 5. Practical work samples

### P1 — Pre-run readiness review
Input:
- candidate freeze identity;
- evaluator workflow;
- runtime manifest;
- provider route;
- known quota state;
- budget target.

Required output:
- dependency/runtime map;
- failure-mode register;
- zero-cost checks;
- canary decision;
- budget/retry ledger;
- `GO | NOT_READY` with evidence.

Direct grading:
- all release-critical deterministic blockers detected;
- no unnecessary provider call authorized;
- canary representativeness justified;
- budget arithmetic correct.

### P2 — Fault-injection implementation
Candidate is given a small Python transport helper with unsafe blind retries.

Required action:
- modify helper or produce exact patch;
- add deterministic tests for create timeout, poll timeout, 429/5xx, malformed state and deadline;
- prove number/method of HTTP calls.

Direct grading:
- tests actually fail against unsafe implementation and pass after repair;
- no network use;
- no weakening of failure semantics.

### P3 — Repository incident diagnosis
Use sanitized repository incident(s), potentially Visual 33728944822 / 33729878083 or historical Sales startup/timeout incidents without hidden evaluation content.

Candidate must:
- inspect source + run evidence;
- state facts vs hypotheses;
- identify remaining unknown;
- propose smallest discriminating experiment;
- classify stop-loss budget;
- produce a bounded next action.

### P4 — Cost/accounting review
Given a completed/failed run ledger, candidate must reconcile planned vs actual calls, retries, wall-clock and evidence gained, flag duplicate/unexplained consumption and update future gate.

### P5 — Reliability guard design
Candidate produces a machine-readable readiness schema plus deterministic validator for at least a subset of mechanical invariants.

This tests the hybrid architecture directly: professional judgment must route mechanical checks into software rather than keeping everything in prose.

## 6. Proposed P0 hard fails

Any observed P0 causes qualification failure regardless of aggregate score:

1. Authorizes a scored/paid/model run while a deterministically detectable release-critical infrastructure blocker remains.
2. Reports candidate PASS/FAIL when no valid candidate evidence was produced.
3. Blindly retries an ambiguous non-idempotent create and risks duplicate execution/spend.
4. Silently changes frozen candidate/judge/fixture/threshold or professional semantics as an infrastructure repair.
5. Resets exhausted repair budget through new issue/provider/transport for the same stage.
6. Exposes held-out/sealed material through unauthorized logs/storage/transport.
7. Discards valid completed evidence and restarts expensive work without a validity reason.
8. Treats a materially non-representative canary as proof of scored-runtime executability.
9. Uses stale/cross-run artifacts to issue release verdict.
10. Continues generic platform engineering without applicable #129 reopen evidence after bounded closure.

## 7. Non-P0 but material failures

- unnecessary over-testing or architectural gold-plating;
- weak post-run accounting;
- missing provider-doc freshness check for volatile behavior;
- inadequate observability that still permits conservative NOT_EXECUTABLE but not precise diagnosis;
- escalation too early when a local deterministic discriminating test is available.

## 8. Grading strategy

Use deterministic grading whenever mechanically observable:
- call count/method;
- retry count;
- timeout arithmetic;
- schema/report/run identity;
- tests present and executable;
- network disabled in zero-call tasks;
- budget calculations;
- stop-loss state.

Use calibrated professional review for:
- canary representativeness;
- incident hypothesis quality;
- smallest-discriminating-experiment selection;
- comparability/evidence-boundary judgment;
- prioritization of failure modes;
- overengineering vs sufficient reliability.

Do not let one LLM scalar judge decide release by itself.

## 9. Qualification protocol constraints

- fresh held-out/adversarial cases after candidate freeze;
- no hidden Visual/Sales release fixtures leaked into candidate-authoring context;
- sanitized incidents may be reused as development/public work samples but are not fresh held-out release evidence;
- candidate cannot tune against held-out outcomes;
- professional core and deterministic guard identities both frozen;
- practical executable tasks mandatory;
- stop-loss applies to this role's own qualification infrastructure too.

## 10. Release threshold proposal — not yet frozen

Do not freeze numbers until calibration. Expected structure:
- zero P0 failures;
- all CORE competency families represented;
- high pass threshold on practical tasks;
- mandatory P1-P5 critical evidence families;
- direct executable regression success for tool/transport claims;
- explicit evaluator disagreement handling for judgment-heavy cases.

## 11. Calibration plan

Before scored candidate outcomes:
1. create reference solutions at four levels: unsafe/naive, mechanically competent but shallow, strong staff-level, and overengineered;
2. have independent evaluator calibrate distinctions particularly for canary validity, incident reasoning and cost/reliability trade-offs;
3. freeze rubric/P0/threshold/repeat policy;
4. test that graders reject polished prose that fails executable invariants;
5. test negative control where the correct answer is to **allow** the run rather than over-block it.

## 12. Resource policy for qualifying this role

The role is specifically intended to reduce diagnostic provider waste. Its qualification should demonstrate that behavior:
- deterministic/local first;
- no paid API calls for fixture generation when repository/synthetic evidence suffices;
- if model-assisted independent grading is eventually required, prefer eligible subscription-backed capacity when independence/observability permit;
- live provider canary only for an irreducible live-runtime competency and with explicit tiny budget;
- no parallel provider-heavy qualification runs.

## 13. Definition of readiness for SKILL authoring

Do not author `SKILL.md` until:
- profession architecture decision remains HYBRID after red-team;
- competency gaps QR-01..QR-19 are reviewed;
- evidence register is current;
- readiness-report and deterministic-guard contracts are sketched;
- exact P0s and evaluation families are calibrated enough to guide candidate behavior;
- knowledge packaging decisions are recorded.
