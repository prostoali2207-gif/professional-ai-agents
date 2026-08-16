# Procedural Skill and Capability Packaging

Status: v0.1.

## Purpose

Professional agents need a disciplined way to package reusable procedural knowledge without turning the system prompt into an encyclopedia.

A skill is not merely a long instruction file. Mature agent systems increasingly separate a small discoverable interface from instructions, references, scripts, schemas, templates, and tools that are loaded or executed only when needed.

This methodology stays vendor-neutral: a runtime may call the package a skill, plugin, capability, module, toolset, or workflow.

## 1. Separate capability artifacts

Classify reusable material by function:

- **router metadata** — what capability exists, when it applies, prerequisites and exclusions;
- **procedural instructions** — nontrivial workflow and professional decision sequence;
- **reference knowledge** — evidence or documentation loaded when relevant;
- **deterministic helpers/scripts** — executable operations better encoded as software than prose;
- **schemas/contracts** — structured inputs, outputs, state, handoffs and validation rules;
- **templates/assets/examples** — reusable artifacts or contrastive demonstrations;
- **tool bindings** — external capabilities and permission requirements.

Do not encode deterministic transformation logic in prose when tested software is materially more reliable.

## 2. Progressive disclosure

Keep the always-loaded routing layer small enough to support reliable capability selection. Load deeper resources only after task relevance is established.

For each capability define:

- trigger/description;
- non-trigger cases;
- required dependencies;
- resources to load by stage;
- expected context cost;
- tool/permission requirements;
- output/evidence contract;
- version and provenance.

Progressive disclosure is an optimization only if the correct capability is selected and the required deeper material is actually loaded. Both stages require evaluation.

## 3. Capability boundary

A reusable skill should normally have a coherent professional responsibility or workflow. Avoid:

- one giant `expert` skill containing unrelated professions;
- microscopic skills that create coordination overhead without a real boundary;
- duplicated knowledge across many packages that will drift independently;
- hidden dependencies on undeclared tools, files, models, or environment state.

Use the same decomposition discipline as `agent-boundary-and-coordination.md`: packaging boundaries must earn their cost.

## 4. Procedural knowledge vs professional judgment

A procedure can encode recurring work, but judgment-heavy exceptions must remain connected to their evidence, applicability conditions, and escalation rules.

Do not convert:

`principle -> context -> evidence -> trade-off -> decision`

into an unconditional recipe merely because it is easier to package.

## 5. Executable resource discipline

Scripts and tools inside a capability package are software supply-chain artifacts.

Require as appropriate:

- source/provenance;
- dependency/version declaration;
- least-required permissions;
- deterministic tests or static checks;
- sandbox/network policy;
- input/output validation;
- side-effect and rollback semantics;
- review before adopting third-party executable resources.

Use `agent-security-and-trust.md` for trust-boundary requirements.

## 6. Examples and demonstrations

Demonstrations can teach trajectories and tacit procedural patterns, but they can also induce imitation and benchmark leakage.

When using examples:

- identify the capability they demonstrate;
- separate invariant principle from incidental surface details;
- include counterexamples or contrastive cases where useful;
- track whether eval cases have leaked into examples;
- avoid letting one canonical trajectory become the only accepted solution.

## 7. Portability contract

Represent a capability in terms of required features rather than one platform API.

A portable capability record should state:

- required context/retrieval features;
- required tools/actions;
- structured-output needs;
- memory/state needs;
- sandbox/network needs;
- human approval/escalation needs;
- acceptable substitutes;
- unsupported environments.

A file format being portable does not prove behavioral portability. Cross-runtime behavior must be tested.

## 8. Evaluation

Evaluate capability packages separately from the base model:

- selection precision/recall: loaded when needed, not loaded when irrelevant;
- dependency completeness;
- correct staged resource loading;
- procedural compliance on novel tasks;
- successful use of scripts/tools/resources;
- context-cost/latency impact;
- robustness to conflicting capabilities;
- graceful behavior when a dependency is missing;
- security/provenance of third-party packages;
- transfer across supported runtimes when portability is claimed.

Use ablation where practical: compare representative performance with and without the capability or against a simpler instruction-only alternative.

## Quality gate

A procedural capability package passes only when it has a clear professional boundary, discoverable interface, declared dependencies, staged context strategy, evidence/output contract, security posture, and behavioral evaluation.

Do not infer reliability from the existence of `SKILL.md` or equivalent files alone.
