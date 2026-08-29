# Paid Qualification Execution Policy

## Purpose

Prevent accidental metered API spend and quota waste without weakening independent release evidence.

Read together with `../../methodology/qualification-execution-routing.md`.

## Mandatory execution rule

Automatic `push` and `pull_request` triggers may run deterministic/static and no-metered-API sealed preflight only.

Any stage that can consume metered model/provider quota — including runtime canaries and scored held-out qualification — must require an explicit manual `workflow_dispatch` approval or an equivalent protected release action.

The manual gate is an execution authorization, not evidence. It must not change the frozen candidate, hidden fixtures, grader, thresholds, model/runtime identity, or preregistered qualification protocol.

## Execution route before metered API

Before authorizing Gemini, Groq, OpenAI API, Anthropic API, xAI/Grok API, or another metered model API, classify the required evidence and check the eligible routes in this order:

`deterministic/no-model -> valid reusable evidence -> subscription-backed Codex/Claude Code when eligible -> metered API when required or justified`

Subscription-backed Codex/Claude Code is preferred only when it preserves the required quality, observability, reproducibility, security, frozen protocol, and evaluator independence. Subscription access is quota-bearing capacity, not unlimited compute.

Do not silently substitute Codex/Claude Code for a provider/model whose identity is part of a frozen qualification, calibrated judge, comparability requirement, or independence contract. Such a migration requires explicit revalidation first.

Do not encode Gemini, Groq, or another metered provider as a universal default merely because an adapter or repository secret already exists.

## Deterministic enforcement

`paid_workflow_guard.py` scans GitHub Actions workflows during the qualification-platform static preflight.

A workflow that injects a known model/provider credential and also exposes `push` or `pull_request` is rejected by default. A narrow exception is allowed only when the automatic path itself is demonstrably non-generative/no-paid-execution and the reviewed invariants are declared in `paid-workflow-exceptions.json`.

Exceptions fail closed when their required invariants disappear and stale exceptions must be removed. This prevents the policy from depending on humans remembering to audit every new workflow.

## Required order

`static/no-API -> sealed/no-API -> choose eligible execution route -> explicit metered-run authorization if still required -> smallest valid runtime canary when needed -> scored release run`

A metered stage is ineligible when an earlier required deterministic gate has failed.

## Development and repair policy

During development or repair:

- prefer deterministic checks first;
- run only the affected targeted regression unless shared coupling justifies broader coverage;
- prefer eligible already-included subscription capacity over additional metered API spend;
- do not rerun an unchanged scored suite to diagnose infrastructure;
- do not rerun an unchanged professional failure merely to seek a better stochastic result;
- preserve valid completed evidence when the evaluator protocol allows compatible resume.

## Pre-run budget gate

Before authorizing a metered scored run, record at minimum:

- objective and decision impact;
- exact candidate/version and evaluation cycle;
- why deterministic, reusable, or eligible subscription-backed evidence is insufficient;
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

Quota/budget exhaustion: stop, preserve completed valid evidence, and do not infer PASS from partial completion. Do not repeatedly retry the same unchanged quota-bound Gemini, Groq, or other provider route. Move to another eligible route only if the frozen protocol and evidence validity remain intact; otherwise defer or revalidate the migration.

Professional failure: revise the candidate or follow an explicitly preregistered repeated-trial policy.
