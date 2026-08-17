# Knowledge Packaging and Runtime Availability

Status: v0.1.

## Purpose

Prevent a professional agent from having a strong profession model while still depending on undeclared base-model memory for the operational knowledge needed to perform difficult work.

Research is not retained merely because it influenced agent design. A material knowledge dependency is retained only when the assembled agent can obtain the right knowledge, at the right depth and freshness, at the moment a decision consumes it.

This methodology complements `source-knowledge-engineering.md` and `procedural-skill-packaging.md`.

## 1. Knowledge dependency inventory

For every CORE or BOUNDARY-CRITICAL competency, identify the material knowledge dependencies behind its difficult decisions.

Record at least:

`competency -> decision/task -> required knowledge -> depth -> decay/freshness -> evidence/provenance -> packaging mode -> retrieval trigger -> fallback/escalation -> evaluation`

Do not infer that a competency description itself supplies enough operational knowledge.

A dependency is material when missing, shallow, stale, or misapplied knowledge could materially worsen a decision, cause repeated hallucination/research, make execution non-reproducible, or defeat the competency claim.

## 2. Packaging modes

Classify each material dependency into one or more justified modes:

### `EMBED_CORE`

Use for compact, stable, high-frequency professional invariants that materially shape judgment across many tasks.

Examples: attribution is not incrementality; capability is not authority; averages can conceal marginal saturation.

Do not embed encyclopedic detail merely because it is stable.

### `PROCEDURAL_MODULE`

Use when correct performance depends on a nontrivial recurring sequence, branching diagnosis, calculation, verification routine, or recovery procedure that cannot safely be reconstructed from a short principle each time.

The module must preserve applicability conditions, exceptions, evidence requirements, and escalation boundaries rather than becoming a blind checklist.

### `REFERENCE_MODULE`

Use for deeper stable or slow-changing disciplinary material that is needed selectively: definitions, diagnostic taxonomies, statistical interpretation guidance, technical standards summaries, contrastive cases, worked examples, or domain-specific reasoning aids.

Load on demand rather than forcing it into the always-loaded core.

### `LIVE_RESEARCH`

Use when correctness materially depends on current law, platform behavior, policy, pricing, market conditions, current specifications, current evidence, or other volatile/versioned facts.

Define authoritative source classes, freshness requirements, minimum triangulation where needed, and behavior when live retrieval is unavailable.

Do not silently fall back to remembered volatile facts.

### `TOOL_BACKED`

Use when software, a calculator, validator, database, measurement system, renderer, static analyzer, or other executable capability is materially more reliable than prose/model reasoning for the operation.

Declare inputs, outputs, permissions, failure semantics, provenance/version, and verification evidence.

### `ESCALATE`

Use when the knowledge/judgment cannot be responsibly packaged within the validated scope, requires a licensed/specialist practitioner, depends on unavailable decision-critical evidence, or exceeds the system's observability/authority.

Escalation is a valid architecture outcome, not a packaging failure.

## 3. Selection test

For each dependency ask in order:

1. Is it a compact stable invariant used frequently? Consider `EMBED_CORE`.
2. Does reliable use require a repeatable workflow or branching diagnostic procedure? Add `PROCEDURAL_MODULE`.
3. Is substantial but selective stable/slow knowledge required? Add `REFERENCE_MODULE`.
4. Can the fact materially decay or vary by version, jurisdiction, account, market, or time? Add or prefer `LIVE_RESEARCH`.
5. Is deterministic/executable computation or observation materially more reliable? Add `TOOL_BACKED`.
6. Is the required competence outside validated scope or impossible to support with available evidence/runtime? `ESCALATE`.

Modes may compose. For example, an experiment-design principle may be `EMBED_CORE`, its power-analysis workflow `PROCEDURAL_MODULE`, statistical tables/formulas `REFERENCE_MODULE` or `TOOL_BACKED`, and current platform experiment eligibility `LIVE_RESEARCH`.

## 4. Runtime availability gate

For every material dependency, prove that the assembled agent can actually access it when needed.

Check:

- discovery: can the agent recognize that the knowledge is needed?
- routing: can it select the correct module/tool/research path?
- retrieval: can it load or obtain the required content?
- sufficiency: is the retrieved depth adequate for the claimed decision?
- freshness: is stale/version-mismatched material rejected or refreshed?
- provenance: can material claims be traced to appropriate evidence?
- context fit: does the knowledge fit the actual population, jurisdiction, version and task?
- failure behavior: if unavailable, does the agent narrow the claim, obtain evidence, or escalate rather than improvise?

A file existing in the repository is not proof of runtime availability.

## 5. Operational-depth test

For each critical competency, select at least one difficult representative decision and ask:

`Could a capable base model produce a plausible answer from the competency description while still lacking the professional depth needed to execute or diagnose this case?`

If yes, identify what additional operational knowledge distinguishes the expert trajectory. Package only that material knowledge; do not respond by dumping an entire textbook into context.

Useful indicators that a deeper module is warranted:

- calculations or statistical interpretation with consequential edge cases;
- multi-stage diagnosis where similar symptoms have different causes;
- standards/specification application beyond a short invariant;
- recurring exceptions that materially change the action;
- high-cost or irreversible procedures;
- repeated need to rediscover the same stable evidence;
- expert use of discriminating cues not captured in the profession model;
- output whose correctness requires a reproducible verification protocol.

## 6. Progressive disclosure and context budget

Knowledge packaging must reduce, not merely relocate, context bloat.

Prefer:

`small routing/core layer -> task-triggered module -> narrow reference section/tool/live retrieval -> evidence-producing action`

Avoid one file per concept, duplicate explanations across packages, and unconditional loading of all references.

A new module must earn its coordination/context cost by improving correctness, reproducibility, retrieval reliability, maintenance, or evaluation.

## 7. Knowledge retention from research

At the end of profession research, classify every material derived finding:

- retained as stable professional invariant;
- retained in a procedural/reference module;
- represented only by provenance/evidence because the underlying fact must be retrieved live;
- delegated to a tool;
- explicitly excluded/out of scope;
- unresolved and escalated.

Do not allow material research findings to survive only in temporary chat/research notes when production behavior depends on them.

Conversely, do not preserve research exhaust that has no decision consumer.

## 8. Evidence and maintenance

Every stored module should declare or inherit:

- competencies/decisions served;
- source/provenance references;
- freshness class and review trigger;
- assumptions and exclusions;
- version or content identity where behavior-relevant;
- owner/maintenance path when appropriate.

When a source is superseded or a procedure changes, identify dependent modules and affected evaluations. Do not update a URL while leaving derived operational guidance silently stale.

## 9. Evaluation

Knowledge architecture requires behavioral evidence, not file-count evidence.

Test at least:

- correct recognition that deeper knowledge is needed;
- correct package/research/tool selection;
- successful staged loading/retrieval;
- novel cases requiring operational depth rather than vocabulary;
- stale/versioned knowledge traps;
- missing-resource behavior;
- conflicting-source/context-fit cases;
- context-cost and unnecessary-loading regressions;
- ablation where practical: core-only/base-model behavior vs packaged knowledge on representative hard tasks.

A module is justified when it improves a material capability or reliability boundary enough to warrant its lifecycle/context cost.

## 10. Required audit for reusable Professional Cores

Before admitting or materially revising a reusable Professional Core, produce a Knowledge Packaging Audit for its CORE and BOUNDARY-CRITICAL competencies.

Minimum fields:

| Competency | Hard decision | Material knowledge dependency | Current availability | Packaging mode | Gap/risk | Required action/eval |
|---|---|---|---|---|---|---|

Possible audit outcomes:

- `SUFFICIENT_CORE` — compact core knowledge is demonstrably enough for the claim;
- `MODULE_REQUIRED` — deeper stable/procedural knowledge must be packaged;
- `LIVE_REQUIRED` — runtime retrieval/freshness gate is required;
- `TOOL_REQUIRED` — executable capability is required;
- `ESCALATION_REQUIRED` — claim must narrow or escalate;
- `UNPROVEN` — architecture may be plausible but runtime sufficiency has not been demonstrated.

Do not equate `UNPROVEN` with failure, but do not call the knowledge architecture complete.

## Quality gate

Knowledge packaging passes only when material professional decisions are not accidentally dependent on undeclared model priors, the required knowledge is available at runtime with appropriate depth/freshness/provenance, deeper material is progressively disclosed rather than always loaded, and behavioral evaluation demonstrates that the packaging improves or protects the claimed professional capability.
