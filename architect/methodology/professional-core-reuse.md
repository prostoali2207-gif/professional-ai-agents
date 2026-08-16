# Professional Core Reuse and Specialization

Status: v0.1 candidate.

## Purpose

Avoid rebuilding the same profession for every applied agent while preventing unsafe inheritance of a superficially similar but incompatible agent or capability.

Reuse is an evidence decision, not a naming decision. A professional core is reusable only when its competence claims, evidence, judgment model, runtime assumptions, authority boundaries, and evaluation evidence remain applicable to the new target.

## Layer model

Separate a professional system into four layers when that decomposition is supported by the work:

1. **Professional Core** — profession-level competencies and judgment that remain materially stable across domains and organizations.
2. **Domain Specialization** — industry/product/work-context knowledge and procedures that materially change professional decisions.
3. **Jurisdiction / Market / Live Context** — laws, standards, platform rules, prices, market state, provider limits, language/culture, or other volatile/local knowledge that must be scoped and refreshed appropriately.
4. **Organization / Project Context** — goals, products, data, constraints, policies, tools, budgets, history, permissions, and current operating state of the concrete project.

Do not force every fact into this four-layer model. Some professions have additional specializations or no meaningful jurisdiction layer. The purpose is separation of invariants from context, not taxonomy for its own sake.

## Mandatory reuse decision

After reconstructing the target profession and before rebuilding its competency model from scratch, inspect the available trusted capability/library inventory.

For each plausible reusable core or capability, classify the decision as one of:

- **REUSE** — applicable without behavior-relevant modification; only contextual bindings change.
- **ADAPT** — professional core remains valid but bounded contextual changes are required.
- **EXTEND** — existing core is valid but the target requires additional competencies, tools, judgment, evidence, or eval coverage.
- **FORK** — a substantial branch is justified because preserving a shared core would create coupling, ambiguity, or regression risk.
- **BUILD NEW** — no candidate passes applicability and quality gates.
- **REJECT** — candidate is misleading, stale, weakly evidenced, unsafe, or outside the required profession boundary.

Do not choose reuse because it is cheaper. Do not choose build-new because it feels cleaner. Apply evidence, risk, and total lifecycle cost.

## Compatibility gate

A candidate must be checked against the target on at least these dimensions when material:

- profession responsibility and outputs;
- competency coverage and expert-vs-average discriminators;
- decision cues, trade-offs, exceptions, failure modes, and escalation boundaries;
- domain assumptions and population/condition compatibility;
- jurisdiction / standards / temporal regime;
- tools, permissions, side effects, privacy/security assumptions;
- runtime/model/context/retrieval/state requirements;
- authority and governance level;
- evidence freshness, provenance, and supersession state;
- evaluation construct, fixtures, thresholds, and qualifying environment.

A matching title such as `marketer`, `designer`, `engineer`, or `analyst` is not evidence of compatibility.

## Inheritance contract

Every reused professional core or capability must record:

- stable identifier and version/commit;
- originating profession/scope;
- evidence/provenance references;
- qualifying eval evidence and environment;
- declared invariants expected to transfer;
- declared assumptions and exclusions;
- dependencies and required runtime features;
- freshness policy for volatile components;
- adaptation/extension delta;
- compatibility decision and rationale.

Applied agents should reference inherited artifacts instead of copying them unless portability or deployment constraints require materialization. If materialized, preserve origin/version and divergence state so copies cannot silently drift.

## Delta research

When a candidate passes the compatibility gate, research the **delta**, not the entire profession by default.

Delta research must answer:

- what target requirements are not covered by the inherited core;
- which inherited claims require freshness revalidation;
- which domain/jurisdiction/project assumptions differ;
- what new failure modes or interactions appear at composition boundaries;
- what evidence would falsify the reuse decision.

Delta research must not become an excuse to trust old evidence blindly. Volatile, versioned, disputed, high-stakes, jurisdiction-specific, or weakly evidenced inherited claims require appropriate revalidation.

## Evaluation inheritance

Historical PASS evidence is prior evidence, not a transferable certificate.

Classify eval obligations:

- **unchanged invariant** — prior evidence may support the claim if the implementation and relevant environment are unchanged and the transfer assumption is explicit;
- **affected behavior** — run targeted regression for the affected claim;
- **new capability / interaction** — add new evaluation;
- **shared high-coupling change** — run broader regression or full release gate when blast radius justifies it.

Never inherit a PASS solely because an upstream core passed. The composed applied agent requires its own practical/adversarial evaluation.

### Mandatory transfer obligations

A reuse decision is incomplete until the evaluation obligations are stated explicitly.

- If runtime, tool bindings, authority scope, security boundary, state contract, or other behavior-relevant environment differs from the qualifying evidence, explicitly mark the affected claims and require targeted regression and/or new evaluation before readiness. Do not stop at saying that the historical PASS is non-transferable.
- For **EXTEND**, explicitly preserve and reuse qualifying evidence for unchanged invariants where the transfer assumptions hold, research only the uncovered delta, and separately evaluate every new capability plus material interaction between inherited and added layers.
- For **ADAPT**, explicitly perform delta research: identify which inherited claims remain valid, which contextual bindings changed, which volatile claims require refresh, what target-specific evidence is missing, and which affected behaviors require regression.
- For **FORK**, preserve provenance to the parent, declare the divergence boundary, and establish an independent regression baseline for the branch.

The decision record must therefore state both `evidence retained for unchanged invariants` and `regressions/new interaction evals required for affected or added behavior` when applicable.

## Composition boundary failures

Red-team especially for:

- domain specialization contradicting core judgment;
- local policy silently overriding professional or safety constraints;
- project context contaminating reusable core knowledge;
- stale market/jurisdiction facts becoming durable invariants;
- duplicated copies drifting independently;
- capability collision or ambiguous routing;
- incompatible tools/permissions between inherited and local layers;
- hidden assumptions about model/context window/state persistence;
- over-generalization from one industry's successful workflow;
- under-specialization that produces generic but polished advice.

## Library admission gate

Do not promote an artifact into a reusable professional-core library merely because it worked once.

Admission requires:

- coherent professional boundary;
- explicit competency/evidence model;
- stable vs contextual knowledge separation;
- provenance and freshness policy;
- declared dependencies and portability contract;
- practical and adversarial evaluation appropriate to the claims;
- known limitations / exclusions;
- versioning and regression policy;
- evidence that reuse produces value without unacceptable degradation or coordination cost.

Prefer a small set of strong, well-evaluated cores over a large catalog of shallow role prompts.

## Decision record

For every material reuse decision produce a compact record:

`target profession -> candidate -> compatibility evidence -> gaps/delta -> alternatives -> risks -> lifecycle/resource trade-off -> REUSE/ADAPT/EXTEND/FORK/BUILD NEW/REJECT -> unchanged evidence retained -> required regressions/new interaction evals`.

## Expert-gap and red-team questions

Before finalizing the architecture ask:

`What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?`

Then challenge the reuse decision from at least:

- senior practitioner: does the inherited model preserve real professional judgment or only vocabulary?
- educator/assessor: are transferred competencies observable and construct-valid in the new context?
- hiring manager: would success in the source context predict acceptable performance in the target job?
- systems/evaluation perspective when material: can the composed system be versioned, tested, diagnosed, and rolled back?

Repair material gaps before declaring the core reusable for that target.
