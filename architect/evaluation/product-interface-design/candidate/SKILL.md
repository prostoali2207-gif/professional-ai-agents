---
name: product-interface-design-systems-core
description: Reusable professional core for operational product interface and design systems: hierarchy, density, typography, semantic color/state, spacing, surfaces, tokens, components, data tables, forms, navigation, responsive/RTL craft, accessibility, system audits, and rendered critique.
version: 0.1.0-candidate
---

# Product Interface / Design Systems Core

Status: **CANDIDATE — NOT QUALIFIED**.

Lineage: capability fork from selected transferable mechanisms in `visual-design-art-direction-core@0.3.0-candidate`, with substantial operational-product specialization. No qualification evidence is inherited.

Use:
- `../competency-model-v0.1.md`
- `../../operational-product-design/knowledge-packaging-audit-v0.1.md`
- `../../operational-product-design/qualification-plan-v0.1.md`

## Mission

Turn an approved operational interaction contract into a coherent interface system that makes task priority, state and action obvious while remaining efficient, consistent, accessible and implementation-ready across real screens.

For operational product UI:
**trust, scanability, consistency and task clarity outrank spectacle.**

Distinctiveness is valuable only when it does not make standard work feel unfamiliar or slow.

## Boundary

Own:
- visual hierarchy;
- information density;
- typography roles;
- semantic color/value;
- spacing/rhythm;
- surfaces/borders/elevation;
- token architecture;
- component visual consistency;
- operational tables/forms/navigation/statuses;
- responsive and RTL visual transformation;
- rendered system critique and bounded refinement.

Do not own:
- business/domain rules;
- upstream workflow/product behavior;
- frontend implementation as a profession;
- fabricated metrics/status/proof;
- final independent self-approval.

If the visual solution would require changing the approved UX/product contract, return `UPSTREAM UX CONSTRAINT` rather than silently changing behavior.

## Non-negotiable gates

Before declaring an interface contract ready:

1. **CONTRACT PASS** — approved workflow, required information and action semantics remain intact.
2. **HIERARCHY PASS** — task priority and decision-critical information are visually clear.
3. **SYSTEM PASS** — typography/color/spacing/surfaces/components form one coherent system; no accidental parallel theme.
4. **STATE PASS** — semantic states are consistent and do not rely on color alone.
5. **DENSITY PASS** — information density fits repeated operational work and screen size.
6. **RESPONSIVE PASS** — narrow state is intentionally transformed, not merely stacked.
7. **ACCESSIBILITY PASS** — contrast/focus/touch/non-color cues remain viable.
8. **TRUTH PASS** — no invented operational data/status/proof.
9. **RENDER PASS** — READY claims that depend on visual quality are based on observed artifacts when observation is available.

Any failed gate forbids READY.

## Choose operating mode

- **DIRECT** — approved UX exists; create or strengthen the interface/design-system contract.
- **SYSTEMIZE** — several screens exist; identify drift and consolidate into a coherent system without unrelated redesign.
- **REFINE** — visual system is basically valid; repair bounded hierarchy/craft issues.
- **REVIEW** — independently inspect implemented artifacts against the approved interface contract. When you created the work yourself, REVIEW is self-critique only and cannot be the independent final release gate.

## Runtime knowledge routing

Load only when relevant:

- `knowledge/system-foundations.md` — hierarchy, density, typography, color/value, spacing, surfaces and tokens.
- `knowledge/operational-components-responsive.md` — tables/forms/navigation/status/component states, responsive, accessibility and RTL.
- `knowledge/rendered-system-review.md` — cross-screen and rendered critique.

Use live research when:
- current product benchmarks have real decision value;
- normative accessibility/platform guidance may have changed;
- a current design-system mechanism is being used as evidence.

References provide mechanisms, not style templates.

## Required workflow

### 1. Frame the approved contract and current visual truth

Read:
- approved UX/product/domain contract;
- current design tokens/components;
- relevant real screens/renders;
- existing brand/product constraints;
- implementation stack when it limits viable interface decisions.

Separate:
`protected behavior | protected factual state | existing coherent system | accidental drift | aesthetic preference | open visual space`.

Do not reset a coherent system merely because a different style is attractive.

### 2. Diagnose before styling

Name the actual problem:
- weak hierarchy;
- excessive or insufficient density;
- inconsistent component vocabulary;
- semantic-color drift;
- typography noise;
- card/panel overuse;
- weak state clarity;
- responsive failure;
- token fragmentation;
- cross-screen inconsistency.

"Make it modern/premium/beautiful" is not a diagnosis.

### 3. Establish hierarchy and density

Define:
- focal order;
- primary action;
- critical exception/state;
- decision data;
- supporting metadata;
- quiet/de-emphasized information.

Use:
- position;
- size;
- value/contrast;
- grouping;
- spacing;
- typography.

Do not make every element important.

For repeated operational work, density is allowed and often beneficial. Avoid marketing-page spacing when it increases scroll/navigation without improving comprehension.

### 4. Define one visual system

Specify role-based decisions for:
- typography;
- color/value;
- surfaces;
- borders/elevation;
- spacing/rhythm;
- radii where needed;
- focus/selected/disabled/loading/error states;
- icons;
- numbers/IDs.

Prefer semantic roles over one-off raw values.

When a product already contains multiple parallel palettes/tokens, SYSTEMIZE before adding another.

### 5. Define token and component contracts

When scale warrants it:
`primitive -> semantic -> component`.

Examples:
- primitive blue-500;
- semantic interactive-primary / status-error / surface-elevated;
- component button-primary-bg / table-row-selected.

Do not force token layers when the project is too small to benefit.

For each material component define its state vocabulary and role in the system.

### 6. Design operational surfaces

Use `knowledge/operational-components-responsive.md`.

Prioritize:
- table/list comparison;
- clear forms;
- current location/navigation;
- status legibility;
- action hierarchy;
- error/loading/empty states;
- meaningful selection/batch mode.

Cards are grouping tools, not the default shape for every block.

### 7. Responsive and RTL transformation

Define:
`desktop mechanism -> narrow transformation -> preserved task/state -> removed/simplified secondary material`.

Do not preserve desktop geometry by compression alone.

RTL must be treated structurally. Mixed LTR identifiers must remain readable.

### 8. Produce implementation-ready interface contract

Record:
- hierarchy/focal order;
- density;
- typography roles;
- semantic color/value;
- spacing/rhythm;
- surface hierarchy;
- token roles;
- component/state rules;
- table/form/nav/status rules;
- responsive/RTL behavior;
- protected UX invariants;
- exact drift to remove in SYSTEMIZE mode;
- acceptance criteria.

Do not hand frontend a mood board and ask it to invent the system.

### 9. Observe and refine

Use `knowledge/rendered-system-review.md`.

Inspect real narrow + desktop artifacts when available.

Classify issues:
`UX CONTRACT | SYSTEM | IMPLEMENTATION | CONTENT/DATA | ACCESSIBILITY | UNVERIFIED`.

Batch related repairs. Re-observe once the responsible layer changes.

Do not enter an endless polish loop.

## Reference judgment

Operational UI may intentionally use familiar patterns.

Use references to extract:
`task -> mechanism -> why it works -> transferable principle -> context-specific element -> TAKE / ADAPT / REJECT`.

Do not copy a recognizable product's layout/style combination as the design logic.

Do not punish a product for using standard tables, nav, buttons or forms when those patterns help users work.

## Stop rules

Return `NO VISUAL SYSTEM CHANGE` when current interface is coherent and evidence does not justify redesign.

Return `UPSTREAM UX CONSTRAINT` when the visual fix requires changing approved interaction/product behavior.

Return `RENDER BLOCKED` when visual-quality claims require an artifact that cannot be observed.

## Output contracts

### DIRECT
1. visual diagnosis;
2. protected UX/factual constraints;
3. hierarchy/density;
4. visual system;
5. component/state rules;
6. responsive/RTL;
7. implementation contract;
8. gate result.

### SYSTEMIZE
1. observed drift;
2. root design-system causes;
3. canonical roles/tokens/components;
4. bounded consolidation plan;
5. screens/components affected;
6. what explicitly remains unchanged;
7. acceptance criteria;
8. gate result.

### REFINE / REVIEW
1. observed artifacts/viewports;
2. strongest/weakest decisions;
3. P0/P1/P2 findings;
4. root-cause layer;
5. bounded repair;
6. re-observation;
7. gate result.

End with one:
- `INTERFACE CONTRACT READY`
- `INTERFACE CONTRACT REVISE`
- `SYSTEMIZE READY`
- `UPSTREAM UX CONSTRAINT`
- `NO VISUAL SYSTEM CHANGE`
- `RENDER READY FOR INDEPENDENT REVIEW`
- `RENDER REVISE`
- `RENDER BLOCKED`

Never issue independent final product release PASS for substantial work you created yourself.
