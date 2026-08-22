# Qualification Scope Policy

## Purpose

Apply Agent Architect Resource & Cost Engineering to qualification scope without weakening professional evidence.

The platform may mechanize **scope enforcement**, but it must not invent profession-specific impact. The evaluator remains responsible for declaring:

- whether professional behavior changed;
- whether the affected surface is local, shared, unknown, infrastructure-only, or unchanged;
- which evaluation families are affected when the surface is local;
- whether existing evidence is compatible for the current candidate/claim;
- whether the release protocol requires a full suite.

The deterministic gate then returns one of:

- `REUSE` — compatible evidence already answers the professional question; no new scored paid suite is justified;
- `TARGET` — run only the declared affected regression families during development/repair;
- `FULL` — broad/shared/unknown impact or a release requirement requires the full suite;
- `BLOCK` — insufficient evidence/impact classification exists to justify either reuse or paid execution.

## Non-negotiable release rule

A preregistered full release qualification cannot be replaced by `REUSE` or `TARGET`. Targeted regression is development/repair evidence, not a release PASS.

## Conservative escalation

`shared` or `unknown` impact -> `FULL`.

A claimed `local` impact without evaluator-declared affected families -> `BLOCK`, not a guessed target set.

Infrastructure-only work with unchanged professional behavior may `REUSE` prior professional evidence only when compatibility is explicitly established. Otherwise it blocks until evidence compatibility is resolved.

## Runtime canary

Runtime uncertainty is orthogonal to professional scope. The gate can mark a canary as required when uncertainty cannot be settled statically, but a canary never proves professional quality.

## Example request

```json
{
  "purpose": "repair",
  "change_surface": "local",
  "existing_evidence": "incompatible",
  "affected_families": ["F-02", "F-07"],
  "full_release_required": false,
  "runtime_uncertainty": false,
  "professional_behavior_changed": true
}
```

Run:

```bash
python architect/evaluation/qualification-platform/qualification_scope_gate.py request.json
```

Expected scope: `TARGET`.

## Evidence boundary

This gate does not infer impact from filenames, branch names, issue titles, or LLM opinion. Professional-family mapping and evidence compatibility are evaluator-owned claims and should themselves be reviewable. This prevents cost optimization from silently reducing construct coverage.
