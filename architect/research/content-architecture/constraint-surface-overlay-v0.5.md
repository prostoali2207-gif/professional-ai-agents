# Content Architecture v0.5 candidate — Constraint Surface Overlay

Status: CANDIDATE / NOT QUALIFIED / NOT LIBRARY-ADMITTED
Issue: #306
Date: 2026-09-13

Load after exact qualified Content Architecture v0.4 blob:
`5d440e1bf3e20fbd35c6ab276310a904e36cc06d`.

Protocol frozen before this implementation:
`architect/research/content-architecture/constraint-surface-qualification-protocol-v0.1.md`.

All unchanged v0.4 rules remain authoritative.

## CA-16 — Constraint surface classification

Before placing a constraint, correction, lock, caveat, or user-feedback-derived item into semantic architecture, classify its **public surface**:

- `INTERNAL_ONLY`
- `PUBLIC_MESSAGE_CANDIDATE`
- `PUBLIC_MESSAGE_REQUIRED`

Do this independently from HARD / COMMUNICATION / CONTEXTUAL / PREFERENCE classification.

A constraint can be HARD and still be INTERNAL_ONLY.

### INTERNAL_ONLY

The item changes what the architecture may do but does not itself belong in audience-facing content.

Typical examples:
- negative user correction;
- previous-system failure guard;
- experiment implementation lock that does not need disclosure;
- provenance/claim-safety rule;
- internal service-composition rule;
- production limitation whose existence is irrelevant to the audience.

Execution rule:
`satisfy by construction, omission, substitution, or bounding`.

Do not create a semantic block whose only job is to explain the internal constraint.

### PUBLIC_MESSAGE_CANDIDATE

The item may be public, but only when the approved communication job, audience relevance, offer truth, proof burden, or explicit public-message request independently justifies it.

Do not promote it merely because it is important internally.

### PUBLIC_MESSAGE_REQUIRED

The audience must receive it because omission would break truth, comprehension, legal/safety duty, approved offer, experiment integrity, or the explicit communication job.

## Negative-constraint invisibility rule

When a constraint is phrased as:
- do not imply X;
- do not mention Y;
- do not overstate Z;
- do not make A look mandatory;

default to `INTERNAL_ONLY` unless an independent reason makes the distinction itself audience-relevant.

Examples:

`do not imply landing -> CRM is mandatory`
-> architecture simply avoids that dependency.
-> do NOT add `services are separate` as a block unless independently needed.

`do not lead with AI`
-> choose a buyer-relevant opening.
-> do NOT add `you don't need AI` by default.

`do not invent results`
-> omit unsupported result claims.
-> do NOT add a public disclaimer about not promising results by default.

## User-feedback firewall at Architecture boundary

If an upstream user comment arrives as feedback rather than an explicit audience-message request, preserve its semantic type.

Treat as internal by default when it is primarily:
- a failure report;
- an objection to prior system behavior;
- a constraint on future work;
- a preference about what not to do;
- an example/hypothesis.

Do not convert the user's wording into content simply because it is vivid, recent, or strongly expressed.

If uncertain whether the user wants the statement said publicly, inspect the approved COMMUNICATION_JOB.
If the content job does not need it, keep it internal.

## Handoff requirement

Add a surface field for material locks when leakage risk exists:

`constraint -> lock_class -> surface_class -> execution effect -> public wording allowed?`

Examples:

`service adjacency != dependency -> HARD -> INTERNAL_ONLY -> do not encode dependency -> NO`

`mandatory safety disclosure -> HARD -> PUBLIC_MESSAGE_REQUIRED -> place before action -> YES`

Creator handoff must distinguish:
- what must be preserved silently;
- what may be verbalized;
- what must be verbalized.

## Failure taxonomy delta

Add:
- `INTERNAL_CONSTRAINT_TO_PUBLIC_MESSAGE_LEAK`
- `USER_FEEDBACK_OVERLITERALIZATION`
- `REQUIRED_PUBLIC_DISCLOSURE_SUPPRESSED`

## Definition-of-done delta

Before handoff:
- every high-risk constraint has a surface classification;
- no INTERNAL_ONLY item is present in INFORMATION_ORDER solely because it was mentioned by the user/upstream;
- every public block has an independent audience/communication justification;
- required disclosures are not suppressed by the invisibility rule.