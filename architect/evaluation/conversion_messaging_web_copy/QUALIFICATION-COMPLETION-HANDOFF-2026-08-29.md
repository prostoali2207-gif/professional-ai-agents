# Qualification completion handoff — Conversion Messaging & Web Copy 0.1.0

Date: 2026-08-29
Role: independent held-out evaluator / qualification executor
Release scope: FULL first-release qualification
Candidate: frozen and unchanged

## Frozen subject

- branch: `agent/conversion-messaging-web-copy-core-0.1.0-2026-08-22`
- commit: `7019f6717b1b61806f4a221a297d049a4ad3b8cb`
- manifest: `agents/conversion-messaging-web-copy/0.1.0/artifact-manifest.json`
- digest: `sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2`
- skill: `agents/conversion-messaging-web-copy/0.1.0/SKILL.md`

Do not change candidate content during this release cycle.

## Existing qualification evidence that may be reused

Reuse only infrastructure/protocol evidence whose invariants remain valid:
- public profession and qualification claim from PR #49 / Issue #50;
- frozen candidate identity above;
- Issue #93 construct coverage requirements;
- FULL scope requirement;
- existing hard-fail classes;
- existing release thresholds and contrastive-craft requirement;
- public executor/canary contracts where compatible with the chosen runtime.

Do not treat any previous interrupted run as a candidate PASS or FAIL.

## Burned / non-release attempts

The prior R2 free attempts failed before scored candidate execution while fresh hidden-pack authoring/review was being performed. Their result class is `INFRA_FAILURE` / evaluation-path failure. They provide no professional score and must not be converted into `PROFESSIONAL_REVISE`.

The stale R2 sequence must not simply be retried. It performed model-dependent hidden-pack generation before enough deterministic validation of the eventual sealed execution path, contrary to the current resource/cost and qualification-platform ordering.

## Frozen professional gate

Preserve the previously preregistered release semantics. In particular:
- material fabrication/deception: hard fail;
- invented customer evidence: hard fail;
- harmful contradiction of frozen UX semantics: hard fail;
- unauthorized material strategy change: hard fail;
- guaranteed causal conversion-lift claim: hard fail;
- critical evidence/claim-integrity hard checks: 100% pass;
- scored non-critical aggregate threshold: >= 85%;
- no competency family below 75%;
- subjective craft cannot be reduced to one uncalibrated stylistic judgment;
- no best-of-N or post-output threshold repair.

If the sealed Issue #93 pack has already been exposed to the candidate-building context or is otherwise no longer held out, author a fresh equivalent pack in an isolated evaluator context. Do not publish hidden fixtures, expected answers, grader keys, or raw hidden candidate responses.

## Required execution order

### Gate 0 — deterministic identity / scope

With zero model calls:
1. verify candidate commit, manifest and digest;
2. verify FULL first-release scope;
3. verify expected artifact paths and runtime contract;
4. verify thresholds/hard-fails are unchanged;
5. verify no existing compatible PASS already satisfies the exact release claim.

Any mismatch stops the run as infrastructure/scope failure.

### Gate 1 — deterministic executor / runner preflight

Before authoring hidden material or invoking a candidate model:
1. validate executor protocol locally/static where possible;
2. validate sealed-runner input/output schemas and report fail-closed behavior;
3. validate that all declared fixture families can be represented and graded by the runner;
4. validate call accounting, timeout/error propagation and incomplete-run rejection;
5. validate sanitized-report and release-ledger schema path.

Use stand-in/deterministic responses for this preflight. No scored API/model calls.

### Gate 2 — hidden-pack authoring and independent review

Only after Gates 0-1 pass:
- author fresh held-out fixtures/expected boundaries in evaluator-isolated context if a still-valid sealed pack is unavailable;
- independently review construct coverage, hard-fail encoding, leakage, answerability and grader validity;
- freeze fixture/grader/runner/threshold digests before candidate execution;
- run the generic sealed no-API preflight against the actual frozen pack.

Do not repair the candidate from hidden answers.

### Gate 3 — runtime capability / canary

Use an unscored canary only if the chosen runtime still has unresolved execution uncertainty after deterministic preflight. The canary must not reveal held-out content or affect thresholds.

Eligible execution may use an approved API-backed runtime or a subscription-backed Codex/Claude Code route only when that route can preserve the same frozen artifact identity, isolation, hidden-pack secrecy, observable output, call/run accounting, and reproducible execution contract. If it cannot, mark that route ineligible rather than weakening the gate.

### Gate 4 — scored FULL qualification

Run the exact frozen suite once under the preregistered retry/stochastic policy. Preserve partial-run evidence but reject an incomplete suite as release evidence.

Separate outcome classes:
- `PASS`: all frozen release conditions satisfied;
- `PROFESSIONAL_REVISE`: complete valid run exposes candidate competence failure;
- `INFRA_FAILURE`: runner/provider/secret/schema/transport/execution failure prevents valid professional inference;
- `NOT_EXECUTABLE`: required construct cannot be validly observed in the available environment.

### Gate 5 — release evidence

Emit only sanitized release evidence publicly:
- candidate SHA/digest;
- qualification pack/runner/grader digests;
- runtime/model/tool identity;
- case/family completion counts;
- aggregate/family/hard-fail results;
- verdict and failure class;
- resource accounting;
- no hidden fixture text, grader keys, expected answers, or raw held-out responses.

If PASS, create the normal Professional Core Library manifest/evidence/qualification record under the existing library contracts. Only then may `Conversion Messaging & Web Copy 0.1.0` be described as a reusable qualified core.

If `PROFESSIONAL_REVISE`, repair only the demonstrated professional layer, freeze a new candidate identity and run targeted regression plus the required fresh release gate according to current methodology.

If `INFRA_FAILURE`, repair infrastructure only; do not mutate the candidate.

## Spline composition after core PASS

Do not fold Spline-specific assumptions into the reusable release fixture. After core PASS, apply `spline-auto-parts-application-contract-v0.1.md` and run its narrow S1-S3 composition regression. That is the minimum application evidence required before using this core to author final Spline landing copy.
