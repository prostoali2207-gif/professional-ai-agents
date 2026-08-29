# Conversion Messaging & Web Copy — completion / reuse decision

Date: 2026-08-29
Status: REUSE + PROJECT-CONTEXT ADAPT; core release qualification still pending
Target application: `prostoali2207-gif/auto-parts-landing`

## Decision

Reuse the existing frozen `Conversion Messaging & Web Copy 0.1.0` candidate rather than rebuilding, extending, or merging it into Conversion/CRO.

Frozen candidate invariant:
- branch: `agent/conversion-messaging-web-copy-core-0.1.0-2026-08-22`
- commit: `7019f6717b1b61806f4a221a297d049a4ad3b8cb`
- artifact digest: `sha256:da7662f95dcf132d9a9875849b7bb5d5d831d1d54821f0b109b543a1f299e1d2`
- candidate: `agents/conversion-messaging-web-copy/0.1.0/SKILL.md`

Do not mutate that artifact before independent qualification unless executable evidence demonstrates a professional defect. A candidate change would invalidate the existing freeze and require a new qualification boundary.

Classification under `architect/methodology/professional-core-reuse.md`:

`Conversion Messaging & Web Copy 0.1.0 -> REUSE`

`Spline auto-parts operating context -> ADAPT as project context, not as a new profession or core extension`

## Capability / responsibility diff

### Existing Spline Conversion Agent

Owns commercial diagnosis and decision framing: conversion objective, KPI/qualified-request definition, offer/proposition diagnosis, trust and objection priorities, CTA hierarchy, evidence plan, experiment priority, and conversion change contract.

It does not provide the dedicated exact-copy craft layer required to turn those approved decisions into complete customer-facing language.

### Conversion Messaging & Web Copy 0.1.0

Already covers the required missing layer:
- expression of an approved offer/value proposition;
- headline/subheadline and supporting copy;
- message hierarchy;
- customer-facing explanation;
- objection/trust copy matched to available proof;
- CTA/helper/error/state microcopy inside frozen UX semantics;
- evidence-strength / claim calibration;
- exact-copy handoff with claim/evidence notes;
- causal critique and revision;
- genuine framing divergence when variants are requested.

It also already encodes the needed boundaries against CRO, User Research, UX, Brand/Visual, Legal/Compliance, Frontend and publishing authority.

Therefore the requested Spline scope does not justify `EXTEND` or `BUILD NEW`.

## Rejected alternatives

### Merge exact-copy craft into the Spline Conversion Agent — REJECT

This would conflate commercial diagnosis/KPI ownership with copy execution, weaken separation of responsibility, and duplicate the already-built professional candidate.

### Build an automotive-parts copywriting profession — REJECT

The automotive-parts requirements here are project/domain context: request qualification semantics, VIN or make/model/year identification, useful part signal, mobile-first constraints, and a strict commercial-truth ceiling. They do not establish a distinct underlying writing profession.

### Extend the frozen core before qualification — REJECT

No executable professional failure currently demonstrates a missing core competency. Prior qualification attempts did not establish a candidate defect.

## Qualification evidence status

The candidate has preregistered FULL held-out qualification infrastructure, including fresh adversarial work samples, hard-fails, contrastive cases, subjective-craft assessment requirements, and frozen release thresholds.

The latest R2 free attempts are not professional failures. They terminated before scored candidate execution while creating/reviewing the fresh sealed pack. Classify these as evaluation/infrastructure failures, not `PROFESSIONAL_REVISE`.

There is no sanitized successful FULL release record for this messaging core in the Professional Core Library. Do not call the core QUALIFIED until such evidence exists.

## Minimum remaining qualification

Because this is a first release with no compatible prior PASS, retain FULL core qualification. Do not downgrade to TARGET/REUSE merely to reduce cost.

Use the current qualification-platform ordering rather than replaying the stale R2 workflow unchanged:
1. verify frozen candidate commit/digest and artifact manifest;
2. run deterministic FULL-scope gate;
3. run generic/static executor and contract preflight;
4. validate sealed-runner structure and fail-closed report path with zero model/API calls where mechanically possible;
5. verify runtime credentials/capability only after deterministic gates pass;
6. author/review a fresh hidden held-out pack in an evaluator-isolated context;
7. freeze fixtures, grader, runner, thresholds and digests before candidate execution;
8. run only the preregistered canary if runtime uncertainty remains;
9. execute the scored FULL qualification;
10. emit sanitized report + release ledger and enforce the frozen verdict.

Do not spend scored calls debugging infrastructure. Do not change thresholds, hard-fails, sealed policy, candidate content, or expected-answer boundaries after seeing candidate output.

Subscription-backed Codex or Claude Code may be used only if the current evaluation environment can preserve evaluator isolation, sealed hidden material, reproducible runtime identity, observable execution, and the existing frozen release contract. Subscription access itself is not evidence and must not be used to bypass qualification integrity.

## Required post-core composition regression for Spline

After the reusable core passes FULL qualification, apply the separate Spline context contract and run only the affected composition checks:
- end-to-end exact copy for the qualified auto-part request landing;
- claim-pressure case attempting to introduce unsupported fitment, stock, price, delivery, guarantee, urgency or social proof;
- UX-boundary case where VIN OR make/model/year and the part-signal requirements are frozen and copy must not redesign the form or interaction semantics.

These checks validate composition with Spline; they are not a substitute for the reusable core's first FULL qualification.
