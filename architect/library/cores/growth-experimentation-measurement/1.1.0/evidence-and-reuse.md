# Growth Experimentation & Measurement 1.1.0 — Evidence and Reuse

## Inherited qualified evidence

Professional Core 1.1.0 retains the exact v0.1 + v0.2 components from qualified Core 1.0.0. Historical qualification evidence for unchanged invariants therefore remains supporting evidence where implementation and assumptions are unchanged: pre-registration, registered-estimand preservation, denominator and identity integrity, delayed outcomes, attribution versus incrementality, reproducible calculations, and strict SCALE safeguards.

Parent qualification record:
`architect/library/qualifications/growth-experimentation-measurement/91da2e74afa2c3c81ecbd3fbedc7a3f89b6cb538b1470d0711f689bba779e41c/growth-experimentation-measurement-1-0-0-20260819.json`

## Behavior-relevant delta

Production incident evidence exposed a profession-general gap: material confounding can block attribution of performance difference to the nominal treatment while still leaving enough mature business evidence for a bounded, reversible operational action. The prior model could over-apply `INCONCLUSIVE` from the causal question to the business action.

Candidate v0.3 adds dual-threshold decision judgment:

- causal conclusion and confidence/evidence strength;
- operational conclusion and confidence/evidence strength;
- materiality;
- reversibility and blast radius;
- cost of waiting or continued spend;
- downstream economics/guardrails;
- whether a plausible confounder can actually reverse the current operational action;
- evidence likely to change that action.

It explicitly preserves strict causal-claim and SCALE safeguards and rejects both causal overclaiming and decision paralysis.

## Executable qualification evidence for the delta

Frozen v0.3 assembly digest:
`sha256:9e503603ec80290b349b523f95c1037ce89daa91de3815d01afbfc928eee46db`

OpenAI family:
- targeted provider-backed decision-sufficiency regression: PASS — workflow run `32563140932`, job `97007724416`;
- fresh post-freeze adversarial heldout: PASS — workflow run `32563284789`, successful rerun job `97008206844`.

Gemini family:
- `GEMINI_API_KEY` preflight and exact frozen candidate verification: PASS;
- fresh decision-sufficiency case H-GF-01: PASS;
- final fresh downstream case H-GFD-01: PASS — workflow run `32621655293`, job `97150580735`.

Earlier Gemini attempts that exposed grader construct defects are diagnostic/burned and are not retroactively counted as PASS. The frozen candidate was not changed to repair those scorer/grader defects.

The affected decision-sufficiency behavior therefore has fresh executable evidence on two independent model families, OpenAI and Gemini. This claim is limited to the tested behavior and does not imply universal cross-model portability of every future runtime.

## Reuse boundary

Stable profession behavior belongs in this core. Domain, organization, platform, legal, price, margin, inventory, capacity, and current metric-definition facts remain external context.

Specializations may add domain-specific measurement definitions and operating constraints but may not weaken registered-estimand preservation, causal-claim ceilings, fixed-horizon discipline, SCALE safeguards, or the requirement to evaluate causal and operational sufficiency separately when materially different.

Any behavior-relevant change to the frozen assembly, repeated production failure on a qualified critical claim, materially changed runtime behavior, or new evidence invalidating a critical policy triggers affected regression or requalification.
