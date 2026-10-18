# Content Architecture — Constraint Surface Qualification Protocol v0.1

issue: #306
date: 2026-09-13
status: FROZEN BEFORE CANDIDATE IMPLEMENTATION
baseline: Content Architecture & Creative Structure Practitioner v0.4 — QUALIFIED / RELEASED
baseline_blob: 5d440e1bf3e20fbd35c6ab276310a904e36cc06d
target: v0.5 candidate overlay / NOT YET IMPLEMENTED at protocol freeze

## Construct

Test whether Content Architecture can preserve internal constraints without incorrectly promoting them into audience-facing semantic blocks.

## New required distinction

Every material constraint that could affect public architecture must be classified by surface:
- `INTERNAL_ONLY`
- `PUBLIC_MESSAGE_CANDIDATE`
- `PUBLIC_MESSAGE_REQUIRED`

### INTERNAL_ONLY
Shapes the allowed solution but is not itself audience content.
Default for negative guards, system corrections, workflow locks, internal provenance requirements and many user feedback constraints.

### PUBLIC_MESSAGE_CANDIDATE
May be communicated only when the approved communication job/audience relevance independently justifies it.

### PUBLIC_MESSAGE_REQUIRED
Must be communicated because the communication objective, legal/safety obligation, experiment lock, offer truth or functional comprehension requires it.

## Governing rule

`constraint importance != audience-message importance`

A constraint may be critical internally and still have zero public surface.

Negative constraints are normally satisfied by absence/avoidance, not by public explanation.

## Visible development fixtures

### CA-CML-01 — service-dependency guard
Input:
- orientation/content about services;
- internal guard: do not imply landing -> CRM is mandatory.

Expected:
- mark guard INTERNAL_ONLY;
- architecture may list services or show a standalone service;
- no semantic block explaining service independence unless audience job independently requires it.

Hard fail:
- adds `not everything at once`, `you can buy them separately`, or equivalent solely because guard exists.

### CA-CML-02 — AI-first guard
Input:
- internal guard: do not make AI the buyer-facing front door.

Expected:
- simply omit AI-first framing.

Hard fail:
- creates a public anti-AI clarification solely from the guard.

### CA-CML-03 — unsupported-results guard
Input:
- internal truth lock: do not invent results or numbers.

Expected:
- unsupported outcomes omitted.

Hard fail:
- public block says `we don't promise results` merely because the guard exists.

### CA-CML-04 — explicit public-message control
Input:
- user explicitly requests audience-facing message that a landing can be ordered standalone;
- truthful and strategy-compatible.

Expected:
- classify PUBLIC_MESSAGE_CANDIDATE or REQUIRED depending brief;
- may enter information order.

Hard fail:
- suppresses it merely because similar statements are often internal guards.

### CA-CML-05 — required disclosure control
Input:
- legally/functionally required audience disclosure.

Expected:
- PUBLIC_MESSAGE_REQUIRED;
- architecture surfaces it appropriately.

Hard fail:
- hides it as INTERNAL_ONLY.

### CA-CML-06 — feedback-report trap
Input:
- user says prior content over-emphasized CRM and that annoyed them.

Expected:
- classify as failure evidence / internal revision input;
- do not create a public block about not over-emphasizing CRM.

Hard fail:
- converts the user's complaint itself into audience-facing content.

## Scoring dimensions

- surface_classification_accuracy
- negative_constraint_invisibility
- public_message_justification
- required_disclosure_preservation
- handoff_clarity

0 = material failure
1 = usable but weak/ambiguous
2 = professionally strong

Any hard-fail = REVISE.

## Practical regression

Use the exact PBGS ORIENTATION-01 incident:
- communication job: new viewer understands what Ali does;
- services: Website/Landing, CRM, Automation/Integrations, Custom Systems;
- internal guard: services are modular, not mandatory sequence.

PASS requires architecture that communicates range without inserting a disclaimer/explanation about modularity unless independently justified.

## Inheritance

All v0.4 truth, brief, proof, pacing, experiment, authority, reference-independence and handoff requirements remain active.

## Qualification consequence

This targeted protocol alone cannot re-qualify the profession.
A v0.5 candidate must pass affected-case development/regression plus broader compatibility checks before any release claim.