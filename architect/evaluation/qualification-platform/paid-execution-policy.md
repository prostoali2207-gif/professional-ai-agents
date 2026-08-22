# Paid Qualification Execution Policy

## Purpose

Prevent accidental API spend without weakening independent release evidence.

## Mandatory execution rule

Automatic `push` and `pull_request` triggers may run deterministic/static and no-API sealed preflight only.

Any stage that can consume paid model/provider quota — including runtime canaries and scored held-out qualification — must require an explicit manual `workflow_dispatch` approval or an equivalent protected release action.

The manual gate is an execution authorization, not evidence. It must not change the frozen candidate, hidden fixtures, grader, thresholds, model/runtime identity, or preregistered qualification protocol.

## Deterministic enforcement

`paid_workflow_guard.py` scans GitHub Actions workflows during the qualification-platform static preflight.

A workflow that injects a known model/provider credential and also exposes `push` or `pull_request` is rejected by default. A narrow exception is allowed only when the automatic path itself is demonstrably non-generative/no-paid-execution and the reviewed invariants are declared in `paid-workflow-exceptions.json`.

Exceptions fail closed when their required invariants disappear and stale exceptions must be removed. This prevents the policy from depending on humans remembering to audit every new workflow.

## Required order

`static/no-API -> sealed/no-API -> explicit paid-run authorization -> smallest valid runtime canary when needed -> scored release run`

A paid stage is ineligible when an earlier required deterministic gate has failed.

## Development and repair policy

During development or repair:

- prefer deterministic checks first;
- run only the affected targeted regression unless shared coupling justifies broader coverage;
- do not rerun an unchanged scored suite to diagnose infrastructure;
- do not rerun an unchanged professional failure merely to seek a better stochastic result;
- preserve valid completed evidence when the evaluator protocol allows compatible resume.

## Pre-run budget gate

Before authorizing a paid scored run, record at minimum:

- objective and decision impact;
- exact candidate/version and evaluation cycle;
- why reusable evidence is insufficient;
- expected call/token/quota envelope when observable;
- protected reserve for release/recovery;
- stop condition and retry limit;
- maximum acceptable run budget or quota envelope when the provider exposes a usable control.

Unknown provider/account-specific billing values must be recorded as unknown rather than invented. Exact prices or remaining quota that materially affect the decision must be checked from current official/account telemetry.

## Release integrity

A full preregistered held-out suite remains mandatory when the release claim requires it. Cost control may remove redundant runs; it must not silently downgrade required independent evidence.

## Failure handling

Infrastructure/configuration failure: repair first, then rerun the smallest stage that can prove the repair.

Transient provider failure: bounded retry only with a concrete reason to expect success.

Quota/budget exhaustion: stop, preserve completed valid evidence, and do not infer PASS from partial completion.

Professional failure: revise the candidate or follow an explicitly preregistered repeated-trial policy.
