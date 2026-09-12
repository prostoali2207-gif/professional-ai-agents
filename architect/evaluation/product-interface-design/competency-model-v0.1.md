# Product Interface / Design Systems — competency and evidence model v0.1

Date: 2026-09-12  
Issue: #298  
Status: candidate-design input; not qualification evidence

## Mission

Turn approved operational workflows into coherent, readable, efficient product interfaces whose hierarchy, density, typography, semantic color, components, tokens and responsive behavior remain consistent across real screens and states.

## Professional boundary

Own product-interface visual system and design-system judgment.

Do not own:
- business/domain rules;
- upstream product/UX behavior;
- frontend implementation as a profession;
- fabricated evidence or content;
- final independent approval of own work.

## Competency families

### UI-01 — Operational visual hierarchy
**Criticality:** CORE.

**Observable capability**
- makes primary task, critical exceptions, decision data and next action visually obvious;
- keeps secondary metadata available without competing with decision-critical content;
- uses scale, value, placement, grouping and spacing before decoration;
- distinguishes importance from mere visual novelty.

**Expert discriminator**
A strong practitioner can explain why a visually attractive screen still fails because equal emphasis hides the actual operating priority.

### UI-02 — Information density and scanability
**Criticality:** CORE.

**Observable capability**
- chooses density based on task frequency, comparison need and screen size;
- supports compact expert work without creating noise;
- avoids excessive whitespace that forces navigation/scrolling;
- avoids dense walls where grouping or progressive disclosure is needed.

**Failure modes**
- marketing-page spacing in operational tools;
- everything inside large cards;
- ultra-compact UI that destroys readability;
- density changed screen-by-screen with no system.

### UI-03 — Typography system
**Criticality:** CORE.

**Observable capability**
Defines stable roles for:
- page/surface titles;
- section labels;
- body/help;
- control labels;
- statuses;
- numbers/money;
- IDs/codes/plates;
- tables and metadata.

Controls weight, size, line height, tabular numerals/mono usage and truncation behavior based on function.

**Failure modes**
- decorative display type in controls;
- too many font families;
- tiny metadata carrying important state;
- inconsistent number alignment.

### UI-04 — Semantic color/value system
**Criticality:** CORE / P0 when state meaning is wrong.

**Observable capability**
- separates neutral surfaces from interactive accent and semantic states;
- standardizes success/warning/error/info/selected/focus/disabled/loading roles;
- ensures critical meaning is not encoded only by color;
- controls accent saturation so inactive surfaces do not compete with actions/status;
- maintains contrast.

**Adversarial trap**
Stakeholder asks for many bright category colors; agent must preserve hierarchy and semantic meaning.

### UI-05 — Spacing, rhythm and grouping
**Criticality:** CORE.

**Observable capability**
- uses a limited spacing scale;
- groups related data more strongly than unrelated data;
- keeps repeated structures rhythmically consistent;
- uses borders/surfaces only when grouping value exceeds visual cost.

**Failure modes**
- random padding/radius/shadow values;
- card-per-field;
- separators everywhere;
- accidental spacing drift between sibling components.

### UI-06 — Surface/elevation/border system
**Criticality:** CORE.

**Observable capability**
Defines meaningful levels for:
- page background;
- primary workspace;
- secondary panel/sidebar;
- elevated overlay;
- input/control;
- selected/active state.

Avoids using shadows, borders and background shifts simultaneously without a hierarchy reason.

### UI-07 — Design-token architecture
**Criticality:** CORE for reusable systems.

**Observable capability**
- separates primitive, semantic and component tokens where scale warrants it;
- prevents raw hard-coded values from silently becoming parallel themes;
- keeps tokens named by role, not one-off screen;
- plans migration/refactor boundaries without unrelated visual redesign.

**Expert discriminator**
Can tell when a hard-coded value is a legitimate exceptional requirement versus design-system drift.

### UI-08 — Component-system consistency
**Criticality:** CORE.

**Observable capability**
Maintains coherent:
- button hierarchy;
- inputs/selects;
- tables/lists;
- badges/status chips;
- tabs;
- navigation;
- modals/sheets/popovers;
- alerts/toasts;
- empty/loading/error states.

All interactive components account for required states: default, hover, focus, active/selected, disabled, loading and error where applicable.

### UI-09 — Operational table/list visual design
**Criticality:** CORE.

**Observable capability**
- makes columns, alignment and row density support comparison;
- distinguishes primary identifier, decision fields and metadata;
- keeps batch/selection mode visually clear;
- handles empty/loading/error;
- prevents action clutter;
- makes long/missing values readable.

**Knowledge sources**
Carbon, PatternFly, project task/data evidence.

### UI-10 — Forms and consequential-action presentation
**Criticality:** CORE.

**Observable capability**
- clear labels and grouping;
- visible required/optional state;
- inline error hierarchy;
- primary vs secondary action distinction;
- review/confirmation surfaces expose amount/scope/consequence;
- destructive style is reserved for genuinely destructive action.

### UI-11 — Navigation and application shell
**Criticality:** CORE.

**Observable capability**
- current location is obvious;
- active/hover/focus states are consistent;
- navigation density matches product breadth;
- mobile navigation preserves key destinations without mirroring desktop blindly;
- secondary navigation does not compete with page-level actions.

### UI-12 — Responsive product-interface craft
**Criticality:** CORE.

**Observable capability**
- transforms layout structurally at narrow widths;
- changes table/list presentation when required;
- preserves decision hierarchy;
- avoids horizontal page overflow;
- handles overlays, sticky controls and viewport height safely;
- preserves task context.

### UI-13 — RTL and mixed-direction visual behavior
**Criticality:** CONTEXTUAL but CORE for Arabic products.

**Observable capability**
- mirrors spatial hierarchy only where meaning requires it;
- handles LTR numbers/codes/plates/phone within RTL;
- checks icon direction and action ordering;
- preserves table readability and numeric alignment.

### UI-14 — Accessibility visual craft
**Criticality:** BOUNDARY-CRITICAL.

**Observable capability**
- sufficient contrast;
- visible focus;
- non-color state cues;
- readable text and zoom behavior;
- practical touch targets;
- no content/action hidden by overlays;
- supports reduced motion where relevant.

### UI-15 — Motion and feedback restraint
**Criticality:** CONTEXTUAL.

**Observable capability**
- motion communicates state/change;
- avoids decorative choreography in high-frequency product work;
- feedback is fast enough not to interrupt flow;
- loading treatment matches content shape and uncertainty.

### UI-16 — Cross-screen system audit
**Criticality:** CORE / verification.

**Observable capability**
- compares sibling screens and states rather than judging one screen in isolation;
- detects parallel palettes, inconsistent components, hard-coded drift and one-off patterns;
- proposes smallest coherent consolidation without unrelated redesign.

### UI-17 — Rendered artifact critique
**Criticality:** CORE / verification.

**Observable capability**
- observes actual narrow + desktop renders;
- separates concept/system failure from implementation failure;
- scores hierarchy, density, typography, color/value, consistency, state clarity and responsive integrity;
- proposes bounded corrections;
- re-observes after repair.

Code/build success alone cannot PASS visual quality.

### UI-18 — Reference literacy and originality appropriate to product UI
**Criticality:** CORE.

**Observable capability**
- studies strong product interfaces for mechanisms, not imitation;
- prefers familiar affordances when familiarity helps task completion;
- avoids category-interchangeable generic SaaS styling when product-specific structure can improve clarity;
- does not force novelty into standard controls.

**Important distinction**
Operational product UI does not use landing-page originality as a universal goal. Distinctiveness is subordinate to trust, efficiency and consistency when those conflict.

### UI-19 — Boundary and truth discipline
**Criticality:** P0.

**Observable capability**
- preserves approved UX behavior;
- does not change required fields or action semantics for visual convenience;
- does not fabricate metrics, status or proof;
- marks missing assets/data truthfully;
- routes upstream problems rather than disguising them with styling.

## Coverage requirements

Every CORE or BOUNDARY-CRITICAL competency requires:
- application;
- diagnosis;
- comparative judgment;
- artifact verification;
- adversarial coverage where superficial polish could hide failure.

## Required practical families

1. inconsistent multi-screen operational product needing system consolidation;
2. dense table + filters + bulk selection;
3. complex form with errors and review state;
4. financial/destructive confirmation surface;
5. token drift with hard-coded colors/spacing;
6. mobile transformation of a desktop-heavy workspace;
7. Arabic RTL + LTR identifiers;
8. stale/partial/error visual states;
9. visually polished but operationally weak design;
10. competent but generic card-grid design needing stronger hierarchy without spectacle.

## Hard fails

Candidate remains NOT QUALIFIED if it:
- changes approved workflow/product behavior without authority;
- hides critical state or consequences for visual cleanliness;
- relies on color alone for critical status;
- produces unreadable/unusable in-scope mobile;
- introduces conflicting parallel design systems without justification;
- presents fabricated operational data/status as real;
- passes visual quality without observing required rendered artifacts;
- treats generic polish as sufficient professional quality.
