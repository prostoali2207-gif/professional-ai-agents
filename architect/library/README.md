# Professional Core Library

Status: active registry — first qualified Professional Core admitted on 2026-08-16.

## Purpose

The Professional Core Library is the trusted inventory used by Agent Architect before rebuilding a profession from scratch.

It is deliberately **not** a folder of role prompts. Library membership means that a versioned professional artifact has a coherent boundary, known provenance, declared dependencies and assumptions, and qualification evidence appropriate to its claims.

The library exists to solve two opposite problems:

- wasteful reconstruction of profession-level competence that has already been proved reusable;
- unsafe inheritance of a superficially similar agent/core whose scope, evidence, runtime, authority, or evaluation does not transfer.

## Registry model

The library separates three object classes.

### 1. Core artifact — immutable profession content

A released core artifact contains the profession-level material itself: competency/judgment model, procedural capabilities, stable knowledge, boundaries, assumptions, exclusions, dependency/runtime contract, security/authority requirements, and references to source evidence.

A released artifact is identified by both:

- a human version such as `1.2.0`;
- a content digest recorded in the manifest.

Changing behavior-relevant content creates a new artifact/version. Do not silently mutate an artifact that existing evaluation evidence points to.

### 2. Qualification record — evidence about one exact artifact

Qualification is not embedded as an eternal property of the profession name. A qualification record points to an exact artifact digest and records:

- claims under test;
- fixture/evaluation set and frozen thresholds;
- qualifying runtime/model/tool/environment;
- run/evidence references;
- repeated-trial reliability requirements where applicable;
- limitations and non-transferable assumptions;
- result and date/freshness boundary.

Historical PASS is prior evidence, not a transferable certificate. Target-specific compatibility and composition evaluation remain required by `methodology/professional-core-reuse.md`.

### 3. Catalog entry — mutable discovery/index state

`catalog.json` is a discovery index, not proof. It may point from profession/tags/aliases to available artifact versions and lifecycle state.

Catalog metadata must never make an unqualified artifact eligible for reuse. Search rank, popularity, title similarity, or being present in the catalog are not compatibility evidence.

## Lifecycle

Allowed lifecycle states:

- `candidate` — artifact may be inspected but has not satisfied admission requirements;
- `qualified` — at least one current qualification record satisfies the declared claim boundary;
- `deprecated` — still traceable but should not be selected for new work without explicit justification;
- `quarantined` — temporarily blocked because provenance, security, integrity, or evaluation is under investigation;
- `revoked` — known not to satisfy its former qualification/admission claim.

`qualified` does not mean universally reusable. It means the artifact passed its own declared qualification boundary.

## Directory contract

```text
architect/library/
  README.md
  catalog.json
  professional-core-manifest.schema.json
  qualification-record.schema.json
  cores/
    <core-id>/
      <version>/
        manifest.json
        ...profession artifacts...
  qualifications/
    <core-id>/
      <artifact-digest-or-safe-id>/
        <qualification-id>.json
```

No `cores/` artifact should be added merely to demonstrate the format. A real core must pass the admission gate before `qualified` lifecycle state is recorded.

## Admission gate

A candidate may enter `qualified` state only when all material requirements are satisfied:

1. coherent profession boundary and outputs;
2. observable competency/evidence model, including tacit judgment where material;
3. stable vs domain/jurisdiction/project context separation;
4. provenance for material claims and freshness rules for volatile claims;
5. explicit assumptions, exclusions, dependencies, runtime/tool/state contract;
6. security, privacy, authority, and escalation boundaries where material;
7. practical/adversarial evaluation appropriate to the capability claims;
8. construct-valid graders/verifiers and frozen pass thresholds;
9. repeated-trial reliability evidence when instability has been observed or consequence justifies it;
10. version/regression/deprecation policy and accountable maintainer;
11. evidence that reuse has a plausible benefit over rebuilding without unacceptable degradation, coupling, or coordination cost.

Missing meaningful evaluation evidence for material claims is a hard admission failure.

## Resolution protocol

When Agent Architect has reconstructed a target profession:

1. query the catalog for plausible candidates using profession scope, outputs, competencies, and constraints — not title alone;
2. inspect each candidate manifest and exact qualification record;
3. run the compatibility gate in `methodology/professional-core-reuse.md`;
4. classify `REUSE | ADAPT | EXTEND | FORK | BUILD NEW | REJECT`;
5. retain qualifying evidence only for unchanged invariants whose transfer assumptions hold;
6. perform delta research and affected/new regression for changed or added behavior;
7. evaluate the composed applied agent independently.

## Integrity and provenance design rationale

The library borrows proven registry/supply-chain ideas without pretending professional cores are container images or software packages:

- content-addressed immutable artifacts and separate human-readable tags/versions;
- separate subject-linked attestations/evidence rather than mutating the underlying artifact after qualification;
- explicit dependency/relationship graphs rather than hidden transitive assumptions;
- provenance and integrity metadata tied to exact artifacts;
- lifecycle state that can deprecate, quarantine, or revoke a previously discoverable version.

Reference models:

- OCI Image/Distribution specifications: content digests, manifests, artifact types, subject/referrer relationships;
- SLSA/GitHub artifact attestations: provenance is about the exact produced artifact and qualifying process;
- SPDX/CycloneDX: explicit component/dependency/relationship and provenance models.

These are architectural analogies, not claims of conformance.

## Non-goals

The library is not:

- a marketplace ranking agents by popularity;
- a prompt gallery;
- a cache that bypasses profession reconstruction;
- proof that a core is compatible with a new target;
- permission to copy organization/project context into reusable profession invariants;
- permission to inherit historical PASS across changed runtime, tools, authority, or composition.
