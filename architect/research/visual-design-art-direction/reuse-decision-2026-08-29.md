# Visual Design / Art Direction — profession reconstruction and reuse decision

Date: 2026-08-29
Status: architecture decision complete; candidate construction permitted; not qualified
Target: reusable professional core for visual design / art direction of commercial landing pages

## 1. Target profession reconstructed

The target is not a generic UI designer, frontend builder, CRO strategist, UX architect, brand strategist, motion designer, 3D specialist, or final release reviewer.

The reusable profession is a **Visual Design / Art Direction Practitioner for landing pages** whose accountable work is to convert a constrained commercial brief into a distinctive, implementable visual thesis; explore materially different concepts before convergence; control typography, composition, scale, color/value, imagery, rhythm and responsive behavior; translate the chosen direction into an implementation-ready contract; and diagnose/revise the actual rendered artifact.

### Primary outputs

1. Visual diagnosis and constraint map.
2. Current-reference / benchmark mechanism map with provenance.
3. Materially different visual direction families.
4. Selected visual thesis and art-direction rationale.
5. Implementation-ready visual design contract.
6. Mobile and desktop rendered critique plus bounded refinement decisions.
7. Optional advanced-media routing decision for motion / 3D / WebGL when justified.

### Profession boundaries

The core does **not** own:
- conversion strategy, offer, claims, CTA priority, funnel architecture, or proof creation;
- information architecture, form fields, validation, recovery, or product logic;
- frontend implementation as a profession;
- fabricated brand/business evidence or synthetic proof;
- final independent release approval of its own work.

Those inputs may constrain visual work, but ownership remains with the relevant upstream/downstream discipline.

## 2. Why the current Spline split is not a stable profession boundary

`auto-parts-landing` currently routes beauty/originality problems to Visual Taste Agent and implementation-oriented visual direction to Visual Director. The two artifacts nevertheless share the same profession-level competencies: external references, composition, typography, rhythm, originality, mobile art direction, visual thesis, imagery, implementation handoff, and rendered review.

The difference is primarily **workflow state**:
- open/reset problem -> research and divergence are heavier;
- already-understood thesis -> specification and refinement are heavier.

That does not justify two reusable professional cores. Agent Architect requires the least-complex architecture unless separation creates measurable expertise, independence, risk-containment, or coordination value. Independent rendered release criticism is already provided by UI Guard, which is a real independence boundary. Therefore the smallest sufficient architecture is one Visual Design / Art Direction core with internal operating modes.

## 3. Mandatory reusable-candidate inspection

External public artifacts are treated as hypotheses, not trusted inventory. None has a transferable qualification certificate for this target profession.

| Candidate | Useful compatibility evidence | Material gaps / risks | Decision |
|---|---|---|---|
| `divyanshu-iitian/agent-website-design-skills` — `web-visual-direction` | Closest professional boundary: visual thesis, reference mechanisms, composition-before-detail, typography/color/imagery/motion, responsive intent, implementation-ready spec, desktop/mobile proof | Thin live-research requirement; weak divergence protocol; limited critique/refinement model; no evidenced creative qualification; no advanced-media routing model; no explicit separation of creative concept from rendered execution failure | **EXTEND** — primary conceptual starting point, not direct reuse |
| `pbakaus/impeccable` / Impeccable 4.1.2 | Strong craft/refinement procedures, live visual iteration, responsive adaptation, typography/layout/motion commands, redesign-vs-refinement distinction, bounded visual verification | Much broader UI/frontend suite; command/tool oriented rather than a coherent art-direction profession; mixes UX, accessibility, implementation and design; no mandatory benchmark breadth or deep divergence by default | **EXTEND capability source / REJECT as core** |
| `ChuluuMGL/business-website-skill` | Benchmark-first taste gate, named visual systems, divergence contract, cross-industry specificity test, desktop/mobile screenshot QA, standard/premium/showcase interaction tiers including 3D/WebGL routing | Full business-site pipeline bundles IA, SEO/GEO, implementation and content; conservative B2B defaults can bias the profession; no qualifying evidence for the target core | **EXTEND capability source / REJECT as core** |
| `TheMattBerman/landing-page-factory` | Strong truth/proof discipline, evidence-vs-synthesis separation, product-visual preservation classes, explicit anti-slop and artifact handoffs | Primarily end-to-end landing strategy/copy/visual/build pipeline; visual art direction is not the profession boundary; category/marketing pipeline assumptions would over-couple the core | **EXTEND truth/imagery capability / REJECT as core** |
| `redhoram/claude-landing-template` | Correctly treats visual quality as an iterative see-change-see loop; desktop/mobile live-preview QA; useful premium-design craft reminders | Template/pipeline architecture, generic premium-design heuristics, shallow divergence and benchmark model, no reusable professional qualification | **ADAPT visual-loop mechanism / REJECT as core** |
| Spline Visual Taste Agent | Strong current-reference breadth, aggressive creative divergence, anti-sterility, visual fundamentals, render-is-truth | Project-local, Spline-coupled, not admitted/qualified as reusable core; fixed reset protocol can be excessive when thesis is already established | **EXTEND into reusable core; remove project coupling** |
| Spline Visual Director | Strong commercial boundary, design-contract discipline, automotive imagery/art direction, visual-load/rhythm craft, independent UI Guard handoff | Project-local and automotive-coupled; substantially overlaps Visual Taste; not reusable qualification evidence | **EXTEND into reusable core; move automotive rules to specialization** |

### Source observations inspected

- `divyanshu-iitian/agent-website-design-skills/web-visual-direction/SKILL.md`, current `main`, inspected 2026-08-29.
- `pbakaus/impeccable/plugin/skills/impeccable/SKILL.md`, version 4.1.2, inspected 2026-08-29.
- `ChuluuMGL/business-website-skill/SKILL.md`, MIT, inspected 2026-08-29.
- `TheMattBerman/landing-page-factory/README.md`, MIT project, inspected 2026-08-29.
- `redhoram/claude-landing-template/README.md` and `.claude/skills/premium-design/SKILL.md`, MIT project, inspected 2026-08-29.
- Spline `visual-taste-agent`, `visual-director`, and `visual-quality-scorecard` at the current `auto-parts-landing/main`, inspected 2026-08-29.

No external candidate is treated as trusted or qualified merely because it is public, popular, licensed, current, or well written.

## 4. Reuse decision

**Primary decision: EXTEND.**

Use the profession boundary and implementable-direction discipline represented by `web-visual-direction` as the closest reusable starting hypothesis, then extend it with only the professionally necessary missing capabilities demonstrated by the Spline work and the other candidate mechanisms:

1. current external visual research with actual rendered-page inspection;
2. explicit benchmark-mechanism extraction and transfer-risk judgment;
3. strong divergence before convergence;
4. calibrated visual taste as observable comparative judgment rather than unexplained preference;
5. implementation-ready art-direction contract;
6. rendered mobile/desktop artifact critique and bounded revision loop;
7. truth/proof/imagery boundary;
8. optional motion/3D/WebGL routing instead of a separate 3D profession.

This is not direct code/content reuse. External artifacts provide provenance for mechanisms and gap discovery; the resulting professional model is independently assembled and must be independently qualified.

## 5. Smallest reusable professional core

The stable reusable core contains only these competence families:

1. **Brief and constraint framing** — separate hard constraints, communication/function constraints, conventions, stakeholder taste, and open creative space.
2. **Reference literacy and current research** — inspect current rendered work, extract mechanisms, reject surface copying, stop when additional search has low decision value.
3. **Creative divergence and concept formation** — generate mechanism-distinct solution families, preserve uncomfortable options, converge only after comparison against the brief.
4. **Visual craft and calibrated taste** — typography, composition, hierarchy, scale, color/value, imagery, density, rhythm, perceived quality and intentional rule breaking.
5. **Responsive/mobile art direction** — treat narrow composition as authored design, not collapsed desktop.
6. **Implementation contract** — specify enough visual decisions that frontend does not invent the art direction.
7. **Artifact-first critique and refinement** — inspect actual renders, separate concept failures from execution failures, repair the responsible layer, re-observe.
8. **Advanced-media routing** — motion/3D/WebGL is an optional production capability chosen only when it earns its complexity and preserves function/accessibility/performance.
9. **Evidence integrity** — never manufacture business imagery, proof, metrics, product evidence or claims to make the design look complete.

Anything more specific belongs in specialization/project context unless evidence shows it transfers across the profession.

## 6. Spline-specific delta that should stay local

The following should **not** be baked into the reusable core:

### Domain specialization — automotive / parts
- art-direction vocabulary may draw from real sourcing and verification work: physical components, fitment, VIN/OEM/part identifiers, packaging/labels, specialist handling, inspection and sourcing;
- avoid racing, luxury-car, HUD/telemetry and generic automotive clichés unless the brief actually supports them;
- real part/product photography must preserve evidentiary truth.

### Project / commercial context — Spline
- `Find My Part / Request a Part` remains the dominant commercial action;
- the visual system must not weaken the approved request path or form usability;
- unknown business imagery, proof, partners, stock, guarantees, delivery times and other claims remain forbidden;
- exact Spline implementation/backend contracts remain outside the core;
- Spline's current numerical visual-quality targets and approximately 390px / 1440px review viewports remain project-level acceptance criteria;
- UI Guard remains an independent reviewer and owns final rendered PASS / REVISE / BLOCK.

## 7. Architecture decision

Use one reusable **Visual Design / Art Direction Practitioner** with three internal modes:

- `DISCOVER` — new/reset direction: heavy research + divergence + selection;
- `DIRECT` — thesis substantially known: formalize/strengthen the visual system and implementation contract without unnecessary rediscovery;
- `REFINE` — implementation exists: artifact-first diagnosis, targeted correction, bounded re-observation.

Modes are not separate agents and do not create separate professional cores.

Motion/3D/WebGL is a routed capability, not a separate agent.

## 8. Evaluation obligations before library admission

No historical Spline or external PASS is inherited because no candidate carries qualifying evidence for this assembled profession.

Required new evidence:
- deterministic checks for truth, scope, mobile, render-honesty and advanced-media routing invariants;
- adversarial semantic cases for generic polish, trend imitation, pseudo-divergence, premature convergence, dashboard/card-grid bias, automotive clichés, fake proof, and unjustified spectacle;
- comparative/pairwise creative judgment calibrated against strong practitioner judgments;
- practical artifact tasks with actual mobile + desktop renders;
- critique/revision tasks where design intent and produced render differ;
- reference-independence checks;
- at least one Spline specialization practical evaluation after the reusable core itself is stable.

Until those gates pass, the candidate must remain **NOT QUALIFIED** and must not enter the Professional Core Library as qualified.
