# Field Evidence Feedback Gate

Use this gate whenever real deployment is proposed as evidence for:

- changing a qualified Professional Core or durable specialization; or
- supporting a T3 `PRODUCTION-PROVEN` trust claim under `../methodology/professional-trust-validation.md`.

These are different decisions. A field observation can justify neither automatically.

## Deterministic gate

REVISE if any are missing:

- immutable source project/revision or evidence identifier;
- model version/digest used;
- observation window;
- pre-outcome decision/prediction when available;
- evidence available at decision time;
- actual action and human override/intervention state;
- outcome plus measurement limitations;
- explicit evidence-class decision: experiment / organization / live-context / reusable-profession candidate;
- explicit proposed disposition from the allowed decision set.

## Causal / professional-judgment gate

Before `REVISE_CORE` or `REVISE_SPECIALIZATION`, require:

- a clearly stated professional failure mode, not merely a bad business outcome;
- at least one serious alternative explanation;
- measurement/data-quality review;
- operating-context boundary review;
- evidence for transferability beyond the originating project;
- a counterargument against promotion;
- an adversarial behavioral fixture that reproduces the claimed professional defect against the currently qualified model.

If the fixture does not reproduce the claimed defect, default to `NO_MODEL_CHANGE`, `ADD_OR_REPAIR_EVAL_ONLY`, or `ESCALATE_RESEARCH` rather than prompt-patching.

## T3 production-proof gate

When field evidence is being used to support T3 rather than only a model change, also require a preregistered production-evidence plan that defines:

- exact deployed behavior/version/runtime;
- representative task/exposure boundary;
- monitoring window or exposure target and why it is sufficient;
- substantive human correction/override capture;
- incident and near-miss severity definitions;
- outcome/quality signals and attribution limits;
- expert spot-review plan where professional judgment is material;
- drift and downgrade triggers;
- frozen T3 promotion rule.

Anecdotal success, elapsed time, absence of complaints, or selective examples do not establish T3.

If the field sample is too narrow, too selectively reviewed, too poorly measured, or materially different from the intended deployment, return `INSUFFICIENT_T3_EVIDENCE` while still routing any valid learning.

## Repair gate

When a reusable defect is demonstrated:

1. deterministic/static checks;
2. minimal affected behavioral test;
3. reliability trials for stochastic critical transitions;
4. broader release suite only after affected PASS;
5. exact artifact digest + provenance + version change;
6. verify no project/company/country/platform-instance facts leaked into durable knowledge.

Do not weaken a grader merely because production behavior disagreed with the expected result. First determine whether the grader, model, measurement, execution, or original causal story is wrong.

## Red-team questions

Before promotion ask:

- Would a senior practitioner call this a transferable judgment defect or just a local outcome?
- Would a researcher accept the causal claim from the available design and measurement?
- Would a hiring manager want this behavior generalized to other accounts and businesses?
- What evidence would make the opposite conclusion more likely?
- Are we learning from the agent's decision, or from a human/platform action that occurred after it?

For model-learning use, PASS means the feedback has been correctly routed and, if it changes reusable knowledge, the change has earned requalification. PASS does not mean every successful field tactic becomes part of the agent.

For T3 use, return `T3_SUPPORTED` only when both this gate and the promotion requirements in `professional-trust-validation.md` are satisfied. Otherwise retain the strongest lower tier actually supported.
