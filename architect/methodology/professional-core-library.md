# Professional Core Library Methodology

Status: v0.1 candidate.

## Purpose

Define how Agent Architect discovers, admits, versions, qualifies, resolves, deprecates, quarantines, and revokes reusable Professional Cores.

This methodology operationalizes the inventory requirement in `professional-core-reuse.md`. It does not replace profession reconstruction or target-specific compatibility evaluation.

## First principle

Library presence is a discovery fact, not a trust verdict.

A catalog match answers only:

`which exact artifacts might be worth inspecting?`

It does **not** answer:

`is this artifact competent?`, `is its evidence current?`, `does its PASS transfer?`, or `is it compatible with this target?`

## Object model

Use three separate objects.

### Core artifact

The immutable profession-level content. Any behavior-relevant modification requires a new artifact identity/version.

### Qualification record

Evidence about an exact artifact digest in a declared evaluation environment. Qualification records are appendable/revocable evidence objects; they do not mutate the qualified artifact.

### Catalog entry

Mutable discovery/lifecycle metadata that points to exact artifact versions and qualification records. Catalog state can change without rewriting historical core/eval evidence.

This separation prevents silent post-PASS mutation, provenance ambiguity, and universalization of a context-bound qualification result.

## Discovery and candidate resolution

After target-profession reconstruction and hidden-gap discovery:

1. derive search facets from responsibilities, outputs, critical competencies, decision types, domain constraints, authority level, runtime/tool constraints, and exclusions;
2. inspect `architect/library/catalog.json` for plausible candidates;
3. do not rank title/alias similarity above responsibility and competency fit;
4. reject catalog records whose lifecycle is `revoked` or `quarantined` from normal reuse consideration;
5. treat `deprecated` as explicit risk requiring a reason to continue;
6. fetch the exact manifest/version and relevant qualification records;
7. run the compatibility decision in `professional-core-reuse.md`.

If no plausible candidate exists, `BUILD NEW` remains valid. Do not create a weak core merely to populate the catalog.

## Admission state machine

A new artifact begins as `candidate`.

It may become `qualified` only when the admission gate is satisfied and at least one qualification record provides qualifying evidence for the declared claim boundary.

Transitions:

```text
candidate -> qualified
candidate -> quarantined
qualified -> deprecated
qualified -> quarantined
qualified -> revoked
quarantined -> candidate | qualified | revoked
 deprecated -> qualified | revoked
```

A transition back to `qualified` requires evidence that addresses the reason for deprecation/quarantine/revocation; status editing alone is insufficient.

## Admission review

Evaluate admission across five independent questions.

### A. Profession construct validity

- Is the profession boundary real and coherent?
- Do responsibilities and outputs reflect actual work rather than a role label?
- Are expert-vs-average discriminators and tacit decisions represented where material?
- Are adjacent/boundary competencies included when their absence creates material failure?

### B. Evidence validity

- Are material claims traceable to evidence appropriate to the claim type?
- Are volatile/current claims separated and assigned freshness policy?
- Are empirical claims valid/comparable for the stated population/conditions?
- Are known evidence conflicts and uncertainty recorded?

### C. Portability and context separation

- Which competencies are stable profession invariants?
- Which are domain, jurisdiction/live, or organization/project context?
- Are dependencies, model/runtime/state/tool assumptions explicit?
- Is the artifact portable without importing hidden project state?

### D. Safety, authority, and governance

- What authority may the core support?
- What must remain human/accountable-professional authority?
- What trust boundaries, security assumptions, privacy constraints, and escalation conditions apply?
- Could reuse expand permissions or side effects silently?

### E. Evaluation sufficiency

- Do fixtures elicit the material claims rather than only test vocabulary?
- Are observables and graders construct-valid?
- Are thresholds frozen before qualifying execution?
- Are practical/adversarial, boundary, composition, and failure cases included as appropriate?
- Has observed stochastic instability been converted into repeated-trial requirements?

A material failure in any required category blocks qualification.

## Versioning

Human versions use semantic-version-like `MAJOR.MINOR.PATCH` identifiers, but version number alone never determines compatibility.

Use these default change classes:

- **MAJOR** — profession boundary, critical competency/judgment contract, authority/security boundary, or incompatible runtime/dependency contract changes materially;
- **MINOR** — backward-compatible competency/capability extension with new evaluation obligations;
- **PATCH** — non-behavioral clarification, source metadata repair, or behavior-preserving defect correction demonstrated by affected regression.

If uncertain whether a change is behavior-relevant, treat it as behavior-relevant until impact analysis proves otherwise.

Every released artifact records a content digest. Qualification evidence points to the digest, not merely the version string.

## Qualification and evidence transfer

Qualification records must state:

`artifact digest -> claims -> fixtures -> observables -> graders -> thresholds -> environment -> trials -> result -> limitations -> freshness/revalidation triggers -> evidence refs`.

A later target may reuse qualification evidence only for unchanged invariants whose implementation and qualifying assumptions remain applicable.

Changed domain assumptions, runtime/model/tool bindings, authority scope, state contract, volatile claims, security boundary, or composition interactions create affected/new evaluation obligations.

## Dependency graph

Declare direct dependencies and classify them as `required`, `optional`, `evaluation`, `tool`, or `runtime`.

Do not silently inherit transitive assumptions. When a dependency materially contributes to a professional claim, its relevant version/constraint and qualification state become part of the compatibility analysis.

Dependency cycles require explicit architectural justification; otherwise reject the library composition because cycles make provenance, update, and regression impact difficult to reason about.

## Lifecycle controls

### Deprecated

Use when a better replacement exists or the artifact remains historically valid but is no longer preferred. Record replacement/migration guidance when available.

### Quarantined

Use when integrity, provenance, security, licensing, evaluation validity, or unexplained behavior is under investigation. Normal automatic resolution must exclude quarantined artifacts.

### Revoked

Use when a former qualification/admission claim is known to be materially false, unsafe, invalid, or irrecoverably superseded. Preserve historical evidence; do not delete history to make the catalog look clean.

## Maintenance triggers

Review a core when any material trigger occurs:

- authoritative profession standard/framework changes;
- material source supersession or contradiction;
- runtime/model/tool behavior changes;
- security/privacy/governance boundary changes;
- repeated production failures or new failure class;
- target compositions reveal hidden coupling;
- grader/evaluation construct is shown invalid;
- dependency becomes deprecated, revoked, or incompatible;
- unexplained reliability regression.

Use:

`trigger -> impact analysis -> affected claims -> evidence refresh/repair -> targeted regression -> broader release gate if coupling warrants -> lifecycle decision`.

## External imports

Open-source repositories and third-party agent/skill libraries are **candidate sources**, not trusted cores.

Before importing external material:

1. identify provenance/license/security implications;
2. reconstruct what profession/capability it actually implements;
3. inspect source quality and hidden project assumptions;
4. map competencies and judgment to the local construct;
5. test rather than inherit popularity, stars, README claims, benchmark self-reports, or role names;
6. admit only the portion that satisfies local library requirements.

Prefer adapting a strong external capability over rebuilding it when evidence supports the choice, but never lower admission criteria merely because external reuse is convenient.

## Professional red-team before admission

Ask exactly:

`What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?`

Then challenge the candidate from:

- senior practitioner — does this preserve real judgment and tacit cues?
- educator/assessor — do the evals measure the claimed competence?
- hiring manager — would this evidence justify trusting someone with the represented work?
- evaluation engineer — are reliability and graders valid?
- systems/security reviewer — are provenance, dependencies, runtime assumptions, trust boundaries, and lifecycle controls operationally safe?

Material criticisms must be repaired or converted into explicit exclusions/limitations before qualification.
