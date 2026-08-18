# Growth Experimentation & Measurement — profession/gap audit v0.1

Status: research/design artifact; not release-ready.
Date: 2026-08-18.

## Decision

Target profession: **Growth Experimentation & Measurement**.

This is not generic dashboard analytics. The reusable professional core must combine:
- experiment-integrity analysis;
- statistical decision discipline;
- metric and denominator governance;
- attribution and causal-claim boundaries;
- funnel/commercial measurement;
- data-quality and identity integrity;
- decision support under sparse, delayed and imperfect data.

No compatible trusted core was identified in the current library. Nearby paid-media capability is not a substitute because it owns campaign optimization rather than independent experiment evidence.

Disposition: **BUILD NEW professional core candidate**, but do not write the final SKILL until competency, knowledge, tooling and behavioral qualification gates pass.

## Evidence basis

Agent Architect requires profession reconstruction, reusable-core inspection, observable competencies, evidence packaging and behavioral evaluation before release.

External professional practice indicates that trustworthy experimentation requires more than reporting uplift. Relevant evidence includes controlled-experiment design, randomization integrity, sample-ratio mismatch, power/sample adequacy, metric quality, peeking/sequential controls, selection/censoring, carry-over/contamination and practical effect interpretation.

These references support design requirements; they are not copied wholesale into runtime knowledge.

## Blocking competency areas

1. **Experiment integrity** — assignment unit, exposure, expected allocation, interference, stopping rule and execution fidelity.
2. **Instrumentation sanity** — detect tracking asymmetry, broken joins and systematic measurement drift.
3. **Sample adequacy** — distinguish business-relevant effect from what the available sample can detect.
4. **Metric quality** — ensure the primary metric is comparable, directionally aligned and protected by guardrails.
5. **Missingness and maturity** — distinguish zero from missing, delayed, invalid and censored outcomes.
6. **Identity integrity** — prevent duplicate people/events/outcomes from inflating results.
7. **Attribution boundary** — attribution evidence does not by itself establish incrementality.
8. **Contamination/interference** — overlapping treatments, spillover and carry-over can invalidate causal interpretation.
9. **Economics and scale validity** — positive effect does not automatically imply economically or operationally scalable effect.
10. **Reproducible computation** — material calculations require recorded inputs, method and outputs rather than narrative arithmetic.
11. **Decision discipline** — execute preregistered rules without metric switching or post-hoc rescue.
12. **Behavioral qualification** — release requires realistic adversarial cases and sealed held-out evaluation after candidate freeze.

## Core vs context boundary

The reusable core owns stable reasoning rules and generic computation contracts.

It must not hard-code:
- one industry or company;
- one advertising platform;
- one CRM/channel;
- current prices, inventory, campaign settings or business definitions;
- one downstream project's experiment data.

Those belong to specialization or live context supplied at execution time.

## Reuse decision

`Target profession -> no compatible trusted core -> BUILD NEW candidate core`

The candidate should reuse proven generic mechanisms from existing architecture where appropriate, but not inherit paid-media decision rights or project-specific business logic.

## Evaluation requirement

Development fixtures should discriminate among real professional failure modes, including:
- proxy-metric winner but business-outcome loser;
- broken randomized allocation;
- fixed-horizon peeking;
- tiny samples with dramatic percentage lifts;
- post-hoc subgroup rescue;
- denominator mismatch;
- attribution presented as causality;
- missing outcomes treated as zero;
- concurrent-treatment contamination;
- delayed/right-censored outcomes;
- metric-definition changes;
- a valid SCALE case;
- duplicate identity/outcome counting;
- capacity/economic failure under apparent acquisition lift.

Public cases are development evidence only. Final qualification requires a frozen candidate and fresh sealed held-out cases.

## Next gate

1. finalize observable competency matrix;
2. finalize stable-vs-live knowledge packaging;
3. define deterministic computation interface;
4. keep evaluation harness provider- and project-neutral;
5. develop against public fixtures;
6. freeze candidate;
7. qualify on sealed held-out cases;
8. only then package the reusable professional core.
