# Professional Agent Qualification Platform

Status: infrastructure architecture for reusable qualification cycles. This does not replace profession-specific evaluation design.

## Decision

Use a **hybrid architecture**.

Generic platform responsibilities:

- frozen candidate identity and artifact digest verification;
- checkout/history availability;
- runtime/executor contract validation;
- model/credential/timeout preflight;
- sealed transport reconstruction, authenticated decryption, digest verification and safe extraction;
- pack component digest checks;
- fixture/grader cardinality and family-structure invariants declared by the evaluator;
- runner/executor protocol compatibility declarations;
- state/checkpoint/tool-protocol capability declarations;
- one-call unscored runtime canary gating when provider/runtime uncertainty remains;
- sanitized report presence/shape checks;
- artifact publication requirements;
- release-verdict enforcement and failure classification.

Profession-specific responsibilities:

- competency model and construct definition;
- fixture content and adversarial cases;
- family taxonomy and weighting;
- grader logic and expert calibration;
- thresholds/hard-fail policy;
- profession-specific tools, state semantics, authority boundaries and observable outcomes;
- whether repeated trials are necessary and what counts as release evidence.

A universal grader or universal fixture schema would create false universality. A universal **qualification lifecycle and transport/runtime contract** does not: it standardizes infrastructure invariants while leaving professional validity evaluator-owned.

## Required lifecycle

`candidate freeze -> static validation -> no-API preflight -> optional one-call runtime canary -> sealed held-out verification -> scored qualification -> sanitized report -> release verdict`

Every stage is fail-closed. A later stage must not run when an earlier required stage fails.

## Failure classes

- `CANDIDATE_UNAVAILABLE`: frozen commit/object is not available to the runner.
- `CANDIDATE_DIGEST_MISMATCH`: frozen artifact does not match the preregistered digest.
- `RUNTIME_CONTRACT_MISMATCH`: executor/protocol/model/state/tool contract cannot satisfy the pack.
- `CREDENTIAL_MISSING`: required provider or sealed-pack credential is absent.
- `TIMEOUT_INCOMPATIBLE`: nested timeouts cannot complete within the outer workflow budget.
- `SEALED_TRANSPORT_INVALID`: chunk set, length or ciphertext digest is wrong.
- `SEALED_KEY_MISMATCH`: repository secret fingerprint does not match evaluator preregistration.
- `SEALED_AUTH_FAILED`: authenticated decryption fails.
- `PACK_INTEGRITY_INVALID`: decrypted archive or component digests differ from freeze record.
- `PACK_STRUCTURE_INVALID`: fixture/grader IDs, cardinality or family invariants differ from preregistration.
- `RUNNER_CONTRACT_MISMATCH`: runner interface is incompatible with the declared executor/report contract.
- `CANARY_FAILED`: one unscored provider invocation cannot exercise the exact scored runtime.
- `QUALIFICATION_NOT_EXECUTABLE`: scored evidence cannot validly run for an infrastructure reason.
- `REPORT_INVALID`: sanitized report missing, malformed or outside declared publication contract.
- `VERDICT_ENFORCEMENT_FAILED`: workflow outcome does not reflect the evaluator verdict.
- `PROFESSIONAL_REVISE`: infrastructure succeeded; candidate failed release criteria.

Infrastructure failures must never be reported as professional candidate failures.

## Stage contracts

### 1. Candidate freeze

Evaluator records immutable candidate commit, artifact digest algorithm, artifact manifest/path set, runtime/model assumptions and evaluation-cycle identity. Qualification code must resolve the exact commit, not merely the current branch.

### 2. Static validation — no API

Validate manifest/schema, referenced files, Python syntax where applicable, candidate object availability, exact artifact digest, executor path, declared protocol, timeout arithmetic, report/verdict configuration and sealed metadata completeness. This stage must not require hidden pack decryption or provider credentials.

### 3. Sealed preflight — no scored API

Using the evaluator-owned key: verify chunk set, ciphertext length/digest, key fingerprint, authenticated decryption, archive digest, safe extraction, freeze-record bindings, component digests, pack digest, fixture/grader ID correspondence, declared cardinality and family structure. Hidden content is not printed.

### 4. Runtime-secret preflight — no API

Verify required provider credential is present. Do not print secret values. Model name and runtime identity must be the same ones used by the scored runner.

### 5. One-call canary — only when required

Run one unscored, non-held-out provider call through the **exact executor/runtime/model/tool/state path** used by qualification. Use when provider model availability, tool protocol, SDK/API behavior, state/checkpoint transport or timeout behavior cannot be established statically. A legacy or different executor is not a valid canary.

The canary may prove executability; it cannot prove professional quality.

### 6. Scored qualification

Run only after all required gates pass. Full held-out execution remains mandatory for release claims because static checks and canaries cannot establish construct performance, adversarial robustness, reliability or threshold compliance.

### 7. Sanitized report and artifact

The evaluator-owned runner emits a public-safe report containing only permitted aggregate/result fields. Raw hidden prompts, expected answers, grader keys, model traces that reveal hidden cases and secrets must not be published. Artifact upload is a required workflow step, not a manual download prerequisite.

### 8. Verdict enforcement

The workflow must fail/stop release when the evaluator verdict is not a release PASS. `set +e` around the runner is acceptable only when the exit code is captured and a later unconditional enforcement step consumes it. Missing report and missing verdict are failures, never PASS.

## Root causes observed in Sales qualification

The repeated Sales failures were enabled by **distributed implicit configuration**: candidate SHA/digest, encrypted transport expectations, secret identity, checkout depth, executor generation, API type and timeout values lived in separate workflow/code fragments. Each manual run discovered only the next incompatible layer.

Specific systemic causes:

1. no single machine-readable qualification manifest bound freeze, runtime, sealed pack and release contract;
2. workflow-specific inline preflight duplicated logic instead of calling a reusable validator;
3. shallow checkout policy was not coupled to frozen-commit resolution requirements;
4. canary and scored workflow were allowed to drift to different executor/API/timeout contracts;
5. timeout values were configured independently without an arithmetic compatibility gate;
6. secret presence/fingerprint and ciphertext integrity were initially detected only at execution time;
7. `NOT_EXECUTABLE` had multiple causes but no stable failure taxonomy;
8. diagnosis required manual workflow reruns rather than deterministic preflight output;
9. sanitized-report publication existed as a workflow behavior rather than a reusable release contract;
10. there was no explicit distinction between infrastructure executability evidence and profession-specific qualification evidence.

## Cost/reliability policy

Do not run a scored held-out suite to diagnose infrastructure. Required order is deterministic/static evidence first, then sealed no-score checks, then at most the smallest valid runtime canary, then the preregistered full scored run.

Retry policy is bounded:

- deterministic preflight failure: zero scored retries; repair infrastructure and rerun preflight;
- provider/transient canary failure: retry only according to declared bounded policy;
- scored-run infrastructure interruption: resume/retry only if evaluator protocol preserves held-out integrity and stochastic policy;
- professional failure: do not rerun the same sealed pack merely to seek a better score unless preregistered repeated-trial policy requires it.

## Senior-practitioner red-team repairs included

A senior ML evaluator would object if infrastructure standardization silently standardized constructs: profession-specific fixture/grader/threshold ownership remains explicit.

A reliability engineer would object to fail-open steps, unsafe archive extraction, implicit timeout nesting and unclassified retries: platform contract requires fail-closed stages, safe extraction, timeout arithmetic and bounded retry classes.

A release/cost owner would object to paying for held-out calls before proving executability: no scored API call is eligible until deterministic and sealed preflight pass; one-call canary is used only for uncertainty that static checks cannot resolve.

## Migration rule

Existing profession workflows can migrate incrementally. The first migration target is Sales 0.2 because its incidents provide concrete regression evidence. Future cycles should create one public qualification manifest and invoke the generic validator rather than copy inline shell/Python checks.
