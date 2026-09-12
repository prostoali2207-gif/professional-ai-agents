# Operational Product UX/UI — profession reconstruction and reuse decision

Date: 2026-09-12  
Issue: #298  
Status: architecture decision complete; candidate construction NOT YET permitted until competency/evidence models are recorded  
Target: reusable professional capability for operational SaaS, admin tools, dashboards, data-heavy workspaces, and manager workflows, with later FleetDesk specialization.

## 1. Problem statement

The existing FleetDesk project-local `ux-architect` and `ui-guard` are useful routing checklists but are not deep professional models. They encode several correct rules but do not reconstruct the profession, package expert knowledge, model judgment, or define sufficient evaluation evidence.

The goal is not to rewrite those files with more prose. The goal is to establish reusable professional capability in `professional-ai-agents`, qualify it independently, then bind FleetDesk rental-operations specialization on top.

Reuse-first applies. Existing internal and external work must be inspected before any BUILD NEW decision.

## 2. Profession boundary reconstruction

The target is not one generic "UI/UX designer". Operational product work contains two materially distinct accountability boundaries.

### A. Operational Product UX / Interaction Design Practitioner

Owns **how operational work is structured and completed**.

Primary accountable outputs:

1. user/operator job and completion signal;
2. information architecture and decision sequence;
3. path model for happy path, alternates, exceptions, bulk work and recovery;
4. forms/input requirements and validation behavior;
5. tables/lists/primary-detail patterns and retrieval controls;
6. loading/empty/error/partial/stale/success/permission states;
7. consequential-action review and confirmation behavior;
8. mobile, keyboard, accessibility and RTL interaction behavior;
9. implementation-ready interaction contract;
10. rendered/runtime UX review against the approved contract.

It does not own visual style as a profession, frontend implementation, business strategy, fabricated product requirements, or final independent approval of its own work.

### B. Product Interface / Design Systems Practitioner

Owns **how an operational product communicates hierarchy, state and system consistency visually**.

Primary accountable outputs:

1. interface visual diagnosis;
2. visual hierarchy and information-density model;
3. typography role system for labels, data, headings and identifiers;
4. semantic color/value system and state vocabulary;
5. spacing, rhythm, surface and border logic;
6. token architecture and component-level consistency;
7. tables, forms, modals/sheets, navigation, badges/statuses and action hierarchy as a coherent visual system;
8. responsive and RTL visual transformation;
9. implementation-ready design-system/interface contract;
10. rendered interface critique and bounded refinement.

It does not own upstream workflow/product decisions, frontend implementation as a profession, or final independent approval of its own work.

### C. Independent UI Review

Independence creates real value, but the current evidence does not justify a third reusable profession core.

Use an independent reviewer/gate role that evaluates rendered output against the UX contract, interface/design-system contract, accessibility/operational constraints and benchmark evidence. It must not inherit the creator's self-score.

This may later become a reusable evaluator capability, but it is not automatically promoted into a separate professional core.

## 3. Internal candidate inspection

### `auto-parts-landing/.agents/skills/ux-architect`

**Compatibility evidence**
- strong explicit boundary between conversion, UX, visual direction, frontend and QA;
- user-job framing;
- information requirement classification;
- path model;
- field-level design;
- state/recovery and data-preservation discipline;
- mobile stress test;
- accessibility baseline;
- implementation handoff;
- rendered UX review;
- severity and stop rules.

**Gaps**
- optimized around a focused landing/request flow rather than repeated operational work;
- limited data-table, bulk-action, exception-queue, primary-detail and reconciliation logic;
- little role/permission, stale/partial operational data, high-density workspace or multi-entity workflow depth;
- project/business rules are coupled to automotive part requests.

**Decision: EXTEND — primary internal UX starting point.**

Retain profession mechanisms; remove project coupling; add operational-SaaS competencies.

### `auto-parts-landing/.agents/skills/ui-guard`

**Compatibility evidence**
- independent rendered review;
- creator/reviewer separation;
- concrete scorecard;
- mobile gate;
- severity model;
- PASS / REVISE / BLOCK;
- source-only review cannot PASS.

**Gaps**
- scorecard is commercial-landing biased;
- hero/request-tool/credibility gates are project-specific;
- visual magnetism/originality thresholds are inappropriate as universal operational-product gates;
- lacks operational density, state consistency, data readability, cross-screen component consistency and error-prevention review depth.

**Decision: EXTEND capability source / REJECT as reusable core.**

Use its independence and artifact-first mechanisms in the evaluator layer.

### `auto-parts-landing/.agents/skills/visual-taste-agent` knowledge

Useful modules:
- typography;
- color/composition;
- responsive UI craft;
- visual judgment;
- imagery;
- motion.

**Decision: EXTEND knowledge source.**

Do not transfer landing-page creative-reset defaults into operational product UI without evidence.

### Current FleetDesk `ux-architect` and `ui-guard`

Useful project constraints:
- high-frequency manager work;
- financial/legal/availability risk;
- bulk/exception behavior;
- 390px mobile;
- Arabic RTL;
- visible financial/destructive consequences;
- search/filter for operational tables.

**Decision: REJECT as professional cores; RETAIN as FleetDesk specialization evidence.**

They are too shallow to qualify as profession-level reusable capability.

### `visual-design-art-direction-core@0.3.0-candidate`

**Transferable invariants**
- artifact-first rendered review;
- typography/composition/color/value/rhythm craft;
- responsive authorship;
- reference independence;
- truth/evidence firewall;
- authority boundaries;
- critique/root-cause separation.

**Non-transferable assumptions**
- commercial landing-page scope;
- heavy concept/divergence requirements;
- art-direction emphasis over system consistency;
- advanced-media routing;
- anti-dashboard language that can incorrectly reject legitimate operational conventions.

Current status is NOT QUALIFIED.

**Decision: FORK capability lineage for Product Interface / Design Systems.**

Preserve provenance and transferable mechanisms, but do not broaden or mutate the landing-page candidate. Do not inherit qualification evidence. Product-interface competence requires an independent baseline and new evaluation.

## 4. External candidate inspection

External public artifacts are capability hypotheses, not trusted inventory or transferable qualification certificates.

### `pbakaus/impeccable@4.3.1`

Relevant mechanisms:
- explicit `Operate` mode for app UIs, admin dashboards, settings, data tables and tools;
- task-first principle: design serves the product;
- standard affordances and earned familiarity;
- state-rich semantic vocabulary;
- consistency over surprise for operational surfaces;
- density is permitted when the task requires it;
- responsive structure rather than marketing-style fluid display treatment;
- `shape` discovery workflow;
- artifact-first critique with independent assessments, heuristics, severity and evidence.

Material gaps/risks:
- broad suite mixes UX, visual design, implementation craft and tooling;
- not a coherent isolated professional core for our target;
- bundled detector/runtime assumptions are environment-specific;
- no transferable qualification evidence under our construct;
- some style rules are heuristic and require evidence/scope treatment.

**Decision: EXTEND capability source / REJECT as direct core.**

It is one of the strongest external sources for operational interface craft and critique mechanics.

### `ztothez/ztothez-design-engineering`

Relevant mechanisms:
- task-centered product design brief;
- explicit evidence/source classes and assumption control;
- operational task frequency, criticality, failure impact and recovery;
- live/demo/imported/cached/fallback/stale/disconnected state contracts;
- operational information design;
- data provenance/freshness;
- metrics tied to decisions;
- rejection of decorative KPI cards/charts;
- structured finding -> evidence -> action -> verification chain;
- semantic token architecture;
- component/system consistency;
- rendered/browser verification and distinction between declarations and evidence.

Material gaps/risks:
- much broader Design Engineering system rather than one profession;
- tightly coupled to its own schemas, validators, CLIs and generation architecture;
- implementation/tooling obligations should not become universal professional judgment;
- no transferable qualification under our repository's evaluation construct.

**Decision: EXTEND capability source / REJECT as direct core.**

It is the strongest observed source for operational information design, source truth/state modeling and design-system engineering.

### `no-session/pstack` / design-consultation

Relevant mechanisms:
- codebase-context-aware design system consultation;
- product context before visual-system decisions;
- research-assisted visual system creation;
- explicit existing-system update vs reset distinction.

Material gaps:
- design consultation pipeline rather than operational UX profession;
- interactive consultation assumptions;
- not a dedicated data-heavy/product-workflow core.

**Decision: EXTEND narrow design-system consultation mechanisms / REJECT as core.**

## 5. Authoritative knowledge sources

These are knowledge/evidence sources, not agent candidates.

### GOV.UK Design System
Use for:
- form/question design;
- validation and error recovery;
- retaining user-entered values on validation failure;
- error summaries and actionable messages;
- service/problem-state distinctions.

Observed current guidance: validation failures should preserve entered answers and tell the user what went wrong and how to fix it.

### IBM Carbon Design System
Use for:
- operational forms;
- data tables;
- search/filter/toolbars;
- selection and batch actions;
- expansion/progressive disclosure;
- semantic tokens/content guidance;
- product-interface accessibility patterns.

Observed current guidance: table toolbars host search/filter/global actions; batch actions appear after selection; data-table density can vary based on task.

### PatternFly
Use for:
- enterprise data lists/tables;
- bulk selection;
- global vs row actions;
- pagination;
- responsive/compact operational data surfaces;
- loading/empty/error states.

### W3C WCAG 2.2
Use as normative accessibility baseline where applicable, including:
- keyboard focus visibility/not obscured;
- target size minimum;
- dragging alternatives;
- input/error assistance and other relevant criteria.

### Other evidence classes to add during competency research
- WAI-ARIA APG for widget interaction patterns;
- platform-specific official guidance where relevant;
- current strong operational-product examples only as observed pattern evidence, never as authority by popularity.

## 6. Reuse decisions

### Operational Product UX / Interaction Design

**Primary decision: EXTEND.**

Start from the strong local `auto-parts UX Architect` professional mechanisms, then extend only the uncovered operational-product delta using Impeccable Operate/shape/critique, ZtotheZ operational information/task/state mechanisms, and authoritative design-system/accessibility evidence.

This is not a content copy. It is profession reconstruction with explicit provenance and new qualification.

### Product Interface / Design Systems

**Primary decision: FORK + EXTEND.**

Fork the transferable visual-craft lineage of `visual-design-art-direction-core@0.3.0-candidate` at the capability/provenance level, then extend with operational-interface and design-system competencies from Impeccable Operate, ZtotheZ, Carbon/PatternFly/WCAG and the useful local visual knowledge modules.

Do not mutate the landing-page candidate and do not inherit a PASS.

### Independent UI reviewer

**Primary decision: EXTEND capability, not BUILD NEW profession.**

Use independent artifact-first review mechanics from the auto-parts UI Guard and Impeccable critique. Build the evaluator around the two approved contracts and operational hard-fails. Keep creator and reviewer contexts independent where runtime permits.

## 7. Knowledge packaging plan

### Operational Product UX core

Always-loaded core judgment:
- task/operator framing;
- frequency/criticality/risk;
- source-of-truth/data dependency;
- path/decision modeling;
- exception/recovery;
- consequential-action discipline;
- boundary/authority rules.

Procedural/reference modules:
1. forms, validation and data preservation;
2. data tables, search/filter/sort/pagination and primary-detail;
3. selection, bulk work and exception queues;
4. loading/empty/error/partial/stale/disconnected/permission states;
5. information architecture and progressive disclosure;
6. mobile/touch/keyboard behavior;
7. RTL/localization interaction;
8. accessibility interaction patterns;
9. review/confirmation/recovery for financial or destructive operations;
10. rendered/runtime UX review.

Live research:
- product/category-specific workflow patterns when the interaction model is not already established;
- current platform/browser guidance when implementation behavior affects the UX decision.

### Product Interface / Design Systems core

Always-loaded core judgment:
- task hierarchy before decoration;
- consistency/system integrity;
- semantic visual roles;
- density appropriateness;
- cross-screen coherence;
- rendered-artifact truth;
- authority boundary.

Procedural/reference modules:
1. typography for operational products;
2. semantic color/value and status vocabulary;
3. spacing/rhythm/density;
4. surfaces, borders, elevation and grouping;
5. token architecture: primitive -> semantic -> component;
6. form/control visual system;
7. table/list visual system;
8. navigation/shell;
9. badges/status/alerts;
10. modal/sheet/popover hierarchy;
11. responsive visual transformation;
12. RTL visual behavior;
13. accessibility visual craft;
14. rendered critique and system-consistency audit.

## 8. FleetDesk specialization boundary

The reusable cores must not contain FleetDesk-specific business rules.

FleetDesk specialization may add:
- contracts and amendments;
- deposits/payments/refunds;
- fines, Salik and parking;
- vehicle availability/replacement/return;
- reconciliation;
- imports;
- rental-document workflows;
- manager/staff context;
- AED, plates, IDs and dates;
- Arabic RTL + mixed LTR identifiers;
- task-specific financial/legal/availability risk.

`fleetdesk-rental-ops` remains the business-behavior authority. UX/UI cores must consume its approved domain contract rather than invent rental logic.

## 9. Candidate architecture

Smallest sufficient architecture:

```
Operational Product UX / Interaction Design Core
                  |
                  v
approved interaction contract
                  |
                  v
Product Interface / Design Systems Core
                  |
                  v
implementation
                  |
                  v
Independent UI/UX Reviewer
```

Frontend implementation remains a separate capability.

Do not add another orchestrator unless coordination evidence later justifies it.

## 10. Evaluation obligations

No external or local historical result transfers as qualification for these new claims.

Required before reusable-library admission:

### Operational Product UX
- fundamentals/application/diagnosis/judgment/verification coverage;
- forms with validation/recovery/data-preservation traps;
- dense tables with search/filter/sort/pagination/batch actions;
- bulk + exception workflows;
- high-risk confirmation and reversible recovery;
- partial/stale/disconnected data;
- mobile and keyboard;
- RTL mixed with LTR identifiers;
- accessibility;
- misleading user premise;
- boundary/escalation;
- rendered/runtime practical tasks.

### Product Interface / Design Systems
- hierarchy/density judgment;
- typography;
- semantic color/status;
- token/system coherence;
- cross-screen consistency;
- operational tables/forms/nav;
- responsive/RTL;
- accessibility;
- artifact-first critique;
- generic-card-grid trap;
- marketing-style over-decoration trap;
- excessive minimalism/whitespace trap;
- inconsistent hard-coded color/token drift;
- design-system repair without unrelated redesign.

### Independent review
- creator/reviewer separation;
- source-only cannot PASS when rendered proof is required;
- deterministic hard-fail checks + calibrated visual judgment;
- P0/P1/P2 severity;
- regression after repair;
- no score inflation to validate previous work.

### Practical artifact gate
At least one realistic operational SaaS fixture must be produced and reviewed at narrow + desktop sizes. Include a dense data surface, a consequential action, an error/recovery path, and a mobile/RTL case.

Do not overfit the reusable core to FleetDesk. FleetDesk is a later specialization practical.

## 11. Stop-loss / qualification infrastructure

Issue #129 maintenance-mode rules remain binding.

This issue does not authorize generic qualification-platform repair.

If an existing qualification stage becomes technically non-executable:
- classify the failure;
- use at most the authorized bounded repair/retry budget for that execution chain;
- stop on another technical defect;
- return NOT_EXECUTABLE rather than weakening the professional or evaluation standard.

## 12. Decision

Proceed with two reusable professional candidates after the competency/evidence models and knowledge dependencies are recorded:

1. **Operational Product UX / Interaction Design Core**
2. **Product Interface / Design Systems Core**

Do not create a third reusable UI Guard profession at this stage.

Reuse strategy:
- UX: **EXTEND** strong local + external capability sources;
- UI/design systems: **FORK + EXTEND** existing visual-design lineage;
- reviewer: **EXTEND** independent evaluation capability.

No FleetDesk production files are changed by this decision.
