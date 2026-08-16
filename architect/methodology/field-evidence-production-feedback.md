# Field Evidence / Production Feedback Lifecycle

## Purpose

Behavioral qualification is necessary but not equivalent to production evidence. Reusable professional models need a controlled way to learn from real deployments without absorbing local anecdotes, platform drift, survivorship bias, or post-hoc stories.

This lifecycle governs observations returned from consuming projects.

## Evidence classes

A production observation MUST first be classified before any reusable model is changed.

1. **Experiment-instance evidence** — facts/results from one campaign, product, vehicle, creative, account, or test. Keep in the consuming project by default.
2. **Organization evidence** — company economics, sales process, capacity, CRM behavior, authority, customer mix, operational bottlenecks. Keep in organization context.
3. **Live-context evidence** — current country regulation, platform mechanics/policy, market state, product availability, pricing, account configuration. Keep in dated live context and revalidate on use.
4. **Reusable-profession candidate evidence** — an observed failure or success that plausibly reflects transferable professional judgment across materially different operating contexts. This is only a candidate for promotion.

A single production outcome is never sufficient by itself to establish a reusable professional rule.

## Required field record

For any observation proposed as feedback to a Professional Core or durable specialization, preserve at minimum:

- source project and immutable source revision or evidence identifier;
- observation date/window;
- professional model/version/digest used;
- decision or prediction made before the outcome where available;
- evidence available to the agent at decision time;
- action actually taken and whether a human overrode it;
- measured outcome and measurement limitations;
- known interventions, confounders, missing data and attribution uncertainty;
- cost/opportunity-cost consequences where material;
- whether the observation is instance, organization, live-context, or reusable-candidate evidence.

Do not reconstruct a pre-decision hypothesis after seeing the result and present it as prospective evidence.

## Promotion gate

A field observation MAY change a reusable professional model only after all of the following:

1. **Reproduce the claimed failure/success.** Establish what the model actually decided from the information available then. Separate model behavior from human execution and tooling failures.
2. **Root-cause analysis.** Test serious alternatives: measurement failure, random variation, sales/operations failure, creative execution, inventory/availability, platform delivery, external market change, or incorrect business facts.
3. **Boundary classification.** Apply `professional-vs-operating-context-boundary.md`. Local facts remain local.
4. **Transferability evidence.** Explain why the underlying judgment should hold outside the originating project. Prefer multiple independent field observations or external professional evidence. One severe counterexample may justify a safety guardrail candidate, but still requires explicit uncertainty.
5. **Counterargument.** State at least one plausible reason not to change the reusable model.
6. **Behavioral reproduction.** Create an adversarial eval that fails for the demonstrated professional reason under the current qualified model. If the alleged defect cannot be reproduced behaviorally, do not patch prompts merely to fit the story.
7. **Minimal repair.** Change the narrowest Core/specialization policy that addresses the transferable root cause. Do not encode project names, exact campaign outcomes, transient platform rules, or one-off thresholds.
8. **Regression + reliability.** Run deterministic/static checks first, then the affected behavioral test, then reliability trials when the transition is stochastic/critical, then the broader release suite only after affected PASS.
9. **Version + provenance.** Record field evidence identifiers, changed judgments, eval deltas, exact artifact digest, qualification result and superseded version.

Possible decisions are explicitly:

- `NO_MODEL_CHANGE` — result is noise, insufficient, already covered, or not causally diagnostic;
- `UPDATE_EXPERIMENT_CONTEXT`;
- `UPDATE_ORGANIZATION_CONTEXT`;
- `UPDATE_LIVE_CONTEXT`;
- `ADD_OR_REPAIR_EVAL_ONLY` — model policy was already correct but evaluation coverage was missing;
- `REVISE_SPECIALIZATION`;
- `REVISE_CORE`;
- `ESCALATE_RESEARCH` — evidence conflict/uncertainty requires stronger research or a domain specialist.

## Anti-overfitting rules

Never promote a rule because:

- one campaign won or lost;
- a metric moved after an action without causal identification;
- the user, agent, platform UI, or postmortem narrative claims causality;
- a local segment/audience/creative happened to outperform once;
- a current platform feature appears important;
- the proposed rule merely memorizes a threshold observed in one business.

Examples:

- `Russian-language creative won in Showroom 171` -> organization/experiment evidence, not Automotive specialization.
- `Meta changed a UAE campaign mechanic` -> dated live context.
- `The specialist repeatedly scales on qualified-lead efficiency while ignoring deterioration in appointment-to-show quality` -> reusable-profession candidate; reproduce, research, add adversarial eval, then consider specialization/core repair.

## Production track record

Keep **qualification evidence** and **production track record** distinct.

Qualification answers: can the model demonstrate the required professional behavior under controlled evaluation?

Production track record answers: what happened when qualified versions were used in real operating environments, with what measurement quality and intervention history?

Do not label a model production-proven merely because it passed behavioral evals. Do not revoke a qualified professional rule merely because one noisy campaign lost.

## Feedback-loop economics

Field feedback itself consumes human time, model quota and experimentation budget. Capture high-value decision points and material failures; do not create exhaustive bureaucracy for every impression or routine action. Prefer existing project telemetry and immutable experiment records over duplicate reporting.
