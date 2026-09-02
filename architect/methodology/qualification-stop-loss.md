# Qualification Stop-Loss

## Purpose

Prevent professional-core qualification from turning into unbounded evaluator/infrastructure repair while preserving the strength of the professional release gate.

This policy operationalizes the evidence-based decision recorded in issue #129. The generic qualification platform is in **STOP / maintenance mode by default**. Qualification failures must be classified before any repair work is authorized.

This policy does **not** weaken frozen professional constructs, held-out secrecy, thresholds, hard-fail rules, independence, practical gates, or required release evidence.

## Mandatory failure classification

After any failed or interrupted qualification step, classify the primary cause before opening a repair issue, changing infrastructure, or rerunning work:

- `PROFESSIONAL_FAIL` — valid professional evidence shows the candidate missed a frozen criterion.
- `EVALUATOR_CONSTRUCT_FAIL` — fixture, rubric, grader, calibration, or profession-specific evaluation design is invalid or insufficient.
- `PROVIDER_RUNTIME_FAIL` — quota, outage, rate limit, provider transport, or subscription/runtime availability prevented valid evidence.
- `LOCAL_EXECUTION_FAIL` — profession-specific adapter, path, schema, Unicode, timeout, permission, packaging, environment, or runner defect prevented valid evidence.
- `GENERIC_PLATFORM_BLIND_SPOT` — a reusable qualification-platform control should reasonably have detected or prevented the infrastructure failure before professional/scored execution but did not.

Do not label every technical failure as a generic platform defect.

## Execution-chain identity

Stop-loss is tracked per **execution chain**, not per agent lifetime.

An execution chain is the same frozen candidate/cycle plus the same qualification stage and materially the same evaluator/transport path, for example:

- held-out author/review/seal;
- judge calibration;
- semantic scored qualification;
- exact runtime canary/probe;
- rendered/practical gate.

A genuinely later stage gets its own chain because it exercises different evidence and runtime surfaces. Splitting one broken stage into new issues, renaming the error, or switching transport/provider does **not** create a new chain when the purpose is still to complete the same failed stage.

## Default decision after classification

### Professional failure

Repair the candidate or responsible professional layer only. Use the smallest valid targeted development/regression evidence. A material candidate revision requires the appropriate fresh release cycle under the frozen integrity policy.

### Evaluator construct failure

Repair the profession-specific evaluator design only. Do not reopen generic qualification-platform engineering unless the evidence also meets a reopen criterion below.

### Provider/runtime failure

Preserve valid completed evidence. Apply the frozen retry policy. If the permitted retry/fallback cannot execute while preserving the qualification contract, return `NOT_EXECUTABLE` or the preregistered infrastructure verdict and STOP. Do not create an open-ended chain of transport repairs merely to force a run.

### Local execution failure

If deterministic/local repair is already authorized by the frozen execution chain and is bounded, one repair may be made with a regression reproducing the exact defect. After that bounded repair, the next eligible execution is the final technical retry for that chain.

If that same execution chain then encounters another non-professional technical defect, STOP the repair chain. Record `NOT_EXECUTABLE` / infrastructure blocker and route the incident to stop-loss review rather than opening serial repair issues by default.

### Generic platform blind spot

Generic platform work is prohibited unless at least one reopen criterion is evidenced. If reopened, fix the smallest generic mechanism, add a deterministic regression for the discovered failure class, then return the platform to maintenance mode.

## Reopen criteria for generic qualification-platform engineering

Resume generic platform engineering only when repository evidence demonstrates at least one of the following:

1. A qualification passed all applicable deterministic/no-provider generic gates and then failed before valid professional evidence because of an infrastructure condition that a generic preflight could reasonably have detected.
2. A scored/paid/model call was consumed solely to discover a generic infrastructure or configuration defect that should have been deterministically detectable beforehand.
3. An existing generic control produced false PASS or fail-open behavior for candidate identity, sealed-pack integrity, runtime contract, report/verdict enforcement, isolation, or execution authorization.
4. The same infrastructure failure class recurs across more than one profession-specific evaluator and cannot be contained locally without duplicated fragile fixes.

Provider outages/rate limits, one-off profession-specific evaluator defects, candidate professional failures, and optional tooling ideas are not sufficient reopen evidence by themselves.

## Repair-chain stop rule

For one frozen execution chain:

`technical failure -> classify -> at most one bounded repair when authorized -> regression -> one eligible retry -> STOP on another technical defect in that chain`

A new issue number does not reset this budget. Renaming the failure, changing transport, or moving to another provider does not reset it when the work still serves the same failed qualification stage. A genuinely later qualification stage may start a new execution chain because it tests a different evidence surface.

Do not create `#N -> #N+1 -> #N+2` infrastructure chains to chase executability of the same stage.

When the stop rule fires:

- preserve all valid evidence and artifacts;
- record the narrowest blocker;
- return `NOT_EXECUTABLE` / the preregistered infrastructure verdict;
- do not infer professional failure or PASS;
- do not weaken thresholds, scope, secrecy, independence, or practical gates;
- do not keep repairing infrastructure inside the same execution chain.

## Cross-stage churn review

Different qualification stages can fail for genuinely different reasons, so one earlier repair does not automatically poison every later stage.

However, repeated infrastructure interruptions across multiple stages are evidence that execution reliability may be dominating professional evaluation. When this pattern appears, Agent Architect must stop before another repair and explicitly compare:

`expected professional information gain -> evidence already obtained -> remaining release-critical evidence -> repair cost/risk -> NOT_EXECUTABLE alternative`

Continue only when the next repair is bounded, stage-specific, preserves the frozen contract, and has clear release-critical information value. Otherwise stop the qualification as not executable rather than continuing infrastructure work for its own sake.

## Pre-run enforcement

Before any model-assisted qualification execution, record:

- current frozen candidate/cycle identity;
- current qualification stage and execution-chain identity;
- whether that execution chain has already consumed a technical repair;
- prior technical failure classes in that chain and relevant cycle-wide infrastructure history;
- whether the proposed run is an allowed first execution, bounded retry, later independent stage, or prohibited serial repair;
- if generic platform work is proposed, which issue #129 reopen criterion is satisfied and the concrete repository evidence.

If this record cannot authorize the run, do not execute it.

## Relationship to professional quality

The stop-loss limits infrastructure churn, not professional rigor.

Required held-out, adversarial, stateful, rendered/practical, calibrated-judge, or domain-expert evidence remains mandatory when the profession requires it. A qualification that cannot produce valid evidence is `NOT_EXECUTABLE`, not PASS.

## Governance

Issue #129 remains the evidence basis for maintenance mode. `architect/evaluation/qualification-platform/README.md` remains the generic platform contract. This policy is the mandatory operational decision gate used by Agent Architect and qualification execution routing.
