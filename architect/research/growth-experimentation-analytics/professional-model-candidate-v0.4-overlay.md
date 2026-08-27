# Growth Experimentation & Measurement — candidate v0.4 overlay

Status: CANDIDATE / NOT QUALIFIED / NOT LIBRARY-ADMITTED.

Base assembly: `professional-model-candidate-v0.1.md` + `professional-model-candidate-v0.2-overlay.md` + `professional-model-candidate-v0.3-overlay.md`. Apply this overlay last.

This overlay adds **no new professional judgment**. It closes the schema-versioning gap that the v0.3 overlay explicitly deferred:

> "If the runtime schema lacks dedicated fields, encode these distinctly in claim boundaries/rationale/next action **until the schema is versioned**."

That deferral made every qualified P0/P1 claim observable only as prose. Prose is paraphrased freely under ordinary sampling, so the same decision became gradeable or ungradeable at random. The professional rules of v0.1–v0.3 are unchanged and are not relaxed anywhere in this overlay.

## Output contract v2

Emit `decision_record` as a required, structured part of the result, alongside — not instead of — the existing prose fields. The prose fields remain the human-readable account. `decision_record` is the auditable decision itself.

### `decision_record.causal`

- `status`: `IDENTIFIED` only when the design and evidence actually support attributing the outcome difference to the nominal treatment. When randomization is absent, arms differ on more than the nominal variable, exposure/denominator integrity is unresolved, or no credible counterfactual exists, the status is `UNRESOLVED`.
- `claim_ceiling`: the strongest claim the evidence supports — `NONE`, `DESCRIPTIVE_ASSOCIATION`, `DIRECTIONAL_ASSOCIATION`, or `INCREMENTAL_CAUSAL`. `INCREMENTAL_CAUSAL` requires a credible counterfactual. Never state a ceiling stronger than the design supports.
- `blocking_confounders`: the confounders that actually block identification. Every name must also appear in `confounders[].name`. Do not name a confounder here that you have not identified and characterized there.

### `decision_record.operational`

- `action`: the operational action. It must equal the top-level `recommendation`. A result whose two decision fields disagree is invalid.
- `target`: which configuration/arm the action applies to, named as the fixture names it. An action aimed at the wrong arm is a wrong decision, not a wording variation.
- `decision_basis`: the grounds you actually used, from the closed vocabulary. Record `COST_OF_WAITING` when continued exposure or spend carries real marginal cost that bears on the action; record `MATURE_DOWNSTREAM_ECONOMICS` when verified matured downstream value drives the action; record `ACQUISITION_COST_DIAGNOSTIC` when an upstream cost figure is used, and remember it is diagnostic rather than decisive when mature downstream economics are available; record `INSUFFICIENT_EVIDENCE` when the honest answer is that no action is yet justified.
- `reversible`: whether the action is reversible with bounded blast radius.
- `evidence_that_would_change_action`: what would actually change this action.

### `decision_record.scale_readiness`

- `state`: `BLOCKED` or `ELIGIBLE`. This is the SCALE gate and it is evaluated independently of the chosen action — a `KILL` on one arm still requires an explicit scale-readiness state.
- `blocking_reasons`: when `BLOCKED`, at least one substantive reason from the closed vocabulary. `NOT_BLOCKED` is permitted only with `state: ELIGIBLE`.

`SCALE` safeguards are unchanged and are not weakened by this overlay. `ELIGIBLE` still requires everything v0.1–v0.3 already require of a SCALE claim; making the gate machine-readable removes the possibility that an unrelated sentence is mistaken for a refusal to scale.

## Internal consistency requirements

A result is invalid, not merely imperfect, when:

- `decision_record.operational.action` differs from `recommendation`;
- `decision_record.causal.blocking_confounders` names anything absent from `confounders[].name`;
- `decision_record.causal.status` is `IDENTIFIED` while `blocking_confounders` is non-empty;
- `decision_record.causal.claim_ceiling` is `INCREMENTAL_CAUSAL` while `causal.status` is `UNRESOLVED`;
- `decision_record.scale_readiness.state` is `BLOCKED` with no reason other than `NOT_BLOCKED`;
- `recommendation` is `SCALE` while `scale_readiness.state` is `BLOCKED`.

## What this overlay does not change

Registered-estimand preservation, denominator and identity integrity, delayed-outcome maturity, fixed-horizon discipline, the causal-claim ceiling, the SCALE evidence bar, the dual-threshold decision procedure, and every v0.3 anti-pattern remain exactly as previously specified. Do not treat the structured record as permission to shorten the professional analysis behind it.
