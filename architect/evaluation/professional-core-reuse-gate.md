# Professional Core Reuse Gate

Status: candidate validation gate for `methodology/professional-core-reuse.md`.

## Claim under test

Agent Architect must not rebuild a profession blindly when trustworthy reusable material exists, and must not reuse a professional core merely because role names look similar.

## Required behaviors

A candidate architecture passes this gate only if it can demonstrate all of the following on representative cases:

1. **Inventory check** — after target-profession reconstruction, it searches/inspects available trusted reusable cores/capabilities before full rebuild.
2. **Layer separation** — it distinguishes stable professional competence from domain specialization, jurisdiction/live context, and organization/project context where the distinction is meaningful.
3. **Compatibility reasoning** — it compares responsibility, competencies, judgment, evidence scope, tools/runtime, authority, freshness, and eval environment rather than matching titles.
4. **Decision classification** — it selects and justifies `REUSE`, `ADAPT`, `EXTEND`, `FORK`, `BUILD NEW`, or `REJECT`.
5. **Delta research** — when reuse is justified, it researches missing/changed claims and freshness-sensitive inherited claims instead of repeating the complete profession research without cause.
6. **No blind PASS inheritance** — it distinguishes unchanged invariants from affected/new behavior and specifies targeted/broader regression accordingly.
7. **Composition evaluation** — it evaluates the assembled applied agent and the interaction between inherited and local layers.
8. **Provenance/versioning** — reused material identifies origin/version, assumptions, exclusions, dependencies, and qualifying evidence.
9. **Resource discipline** — reuse/build decisions consider lifecycle cost and risk, but cheapness alone cannot override eligibility, evidence, security, or quality floors.

## Adversarial fixtures

### R1 — Same title, incompatible work

Candidate: a `marketing specialist` core qualified for B2B enterprise account-based marketing.
Target: high-volume local used-car acquisition through marketplace/paid-social/WhatsApp flows.

Expected: no automatic REUSE from title overlap. Architect must identify meaningful decision/workflow differences and choose ADAPT/EXTEND/FORK/BUILD NEW according to evidence.

### R2 — Strong core, stale volatile layer

Candidate: a professionally strong automotive advertising core containing old platform policy, pricing, or jurisdiction-specific facts.
Target: current market deployment.

Expected: preserve stable professional competence but refresh/revalidate volatile current claims; stale live knowledge must not become inherited invariant.

### R3 — Project facts leaking into core

Candidate: a core derived from one showroom with its budget, inventory, audience size, channel history, and local operating rules embedded as universal instructions.

Expected: reject or refactor those facts into organization/project context before library admission.

### R4 — Prior PASS temptation

Candidate core has a historical behavioral PASS in another runtime/version.
Target composition changes tool bindings and authority scope.

Expected: historical PASS is prior evidence only; targeted/new regression is required for affected claims.

### R5 — Wasteful rebuild

Candidate: versioned, compatible, well-evaluated core whose stable competence and runtime contract match the target; only domain-specific additions differ.

Expected: do not repeat complete foundation research without a falsifiable reason; perform delta research and target affected/new behavior.

### R6 — Cheap but weak reuse

Candidate: low-cost shallow role prompt with no provenance or meaningful evals.
Alternative: more work to construct/extend a properly evidenced core.

Expected: reject cheap candidate; resource optimization occurs only after quality/evidence/eligibility constraints.

## Hard fails

- reuses by role-name similarity alone;
- copies project-specific state into a reusable core as invariant knowledge;
- claims inherited PASS proves the composed agent is ready;
- skips freshness checks for materially volatile inherited claims;
- defaults to rebuilding everything despite a proven compatible core without documenting why;
- admits a core to a reusable library without provenance, boundary, dependencies, limitations, and evaluation evidence.

## Evidence standard

For behavior-relevant release claims, use an executable fixture/observable trace/grader chain when the runtime can expose the behavior. Narrative compliance alone is insufficient for P0/P1 claims.

A minimal initial integration may use deterministic/static checks to prove router reachability and required decision vocabulary, followed by targeted behavioral fixtures before claiming behavioral PASS.
