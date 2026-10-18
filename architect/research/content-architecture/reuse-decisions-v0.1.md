# Content Architecture — reuse decisions v0.1

Status: Architect research artifact. No reuse certificate is implied.

## Target

**Content Architecture & Creative Structure Practitioner**: converts an approved strategic brief into a creator-ready structural architecture while preserving strategy, commercial truth, and experimental invariants.

## Decision records

### 1. Existing `auto-sales-growth-system/agents/content-analyst.md`

**Compatibility evidence**
- Strong overlap in target output: hook job, semantic blocks, proof, pacing, CTA placement, visual requirements and creator handoff.
- Correctly blocks audience/KPI/strategy/final-copy ownership in many places.

**Gaps / risks**
- It is an applied automotive artifact, not a qualified reusable professional core.
- No profession-first qualification record supports its material judgment claims.
- It overreaches into Analytics by specifying a large analytics/instrumentation contract.
- It mixes universal craft with project/platform/application details.

**Decision: REJECT for direct reuse; BUILD NEW universal core using it only as a legacy work sample.**

Reason: title/scope overlap is not enough for reuse; material qualification evidence is absent and the layer boundary is not clean.

### 2. `social-content-creative` research artifact

**Compatibility evidence**
- Shares brief interpretation, hooks, narrative construction, claim grounding, experiment-lock preservation, platform adaptation and handoff discipline.

**Gaps / risks**
- Explicitly targets final public-facing words and shoot-ready creative execution.
- It is currently a research artifact marked not qualified.
- Direct adoption would collapse Content Architecture into Content Creator.

**Decision: REJECT as the target core; retain as an adjacent research dependency.**

Potential later composition: Content Architecture hands a structural spec to a separately qualified Social Content Creative core.

### 3. `video-editing-post-production` 0.1.0

**Compatibility evidence**
- Qualified library catalog entry; relevant invariants include pacing/continuity, truth preservation, experiment variant integrity and artifact-first QC.
- Clear downstream ownership of frame-level editorial execution and finishing.

**Gaps / risks**
- Its professional output is an edited/rendered artifact, not a pre-creator content architecture.
- Importing its whole core would create duplicate authority over pacing and editorial structure.

**Decision: REUSE as an adjacent downstream boundary contract, not as the Content Architecture core.**

Transferred invariant: architecture may define semantic jobs, proof visibility and broad timing constraints; post-production owns frame-level cut/edit execution inside the approved structure. Any runtime coupling requires targeted interaction regression.

### 4. `growth-experimentation-measurement` 1.0.0

**Compatibility evidence**
- Qualified core owns experiment-integrity validation, registered estimand preservation and decisioning.
- Target Content Architecture must preserve locked variables when executing an experiment.

**Gaps / risks**
- Analytics/measurement is not the target profession.
- Pulling KPI/attribution/decision logic into Content Architecture would create authority leakage.

**Decision: REUSE only as an upstream/downstream contract for experiment locks and observability; REJECT as a professional-core substitute.**

The Content Architecture core consumes declared tested/controlled variables and emits execution-structure metadata. It does not calculate, reinterpret or decide experiment outcomes.

### 5. `paid-media-performance-marketing` 1.0.0

**Compatibility evidence**
- Adjacent creative-learning and experimentation concepts.

**Gaps / risks**
- Primary responsibilities are media allocation, measurement, auction/automation reasoning and spend governance.
- Does not model the target structural creative craft.

**Decision: REJECT as target reuse.**

If the content is a paid-media asset, this core remains an adjacent owner for media/budget/placement decisions.

### 6. External `realjaymes/marketingagentskills/skills/ad-creative`

**Compatibility evidence**
- Includes hooks, video structures, proof/CTA and production templates.

**Gaps / risks**
- Bundles creative strategy, final copy, performance iteration and production.
- Encodes rigid/default formulas and market-specific stylistic assumptions as defaults.
- No independent professional qualification evidence was established.
- Platform/spec claims may be volatile.

**Decision: REJECT.**

Useful only as discovery evidence for common industry patterns, not as a reusable professional core.

## Net architecture decision

**BUILD NEW** narrow universal core: `content-architecture-creative-structure`.

Do not create a new autonomous team role solely because a core exists. In the auto-sales system this core can continue to be bound to the existing logical `Content Analyst` stage for compatibility, while the profession name and authority boundary become precise.

## Transfer obligations

- Keep Content Creator and Video Post-Production as separate downstream owners.
- Preserve Analytics qualification for experiment outcome interpretation; remove metric-design ownership from Content Architecture.
- Add interaction tests for strategy-lock preservation, creator freedom, post-production boundary and analytics boundary.
- No existing PASS transfers to the new core itself; the new core requires its own development, adversarial and held-out qualification.
