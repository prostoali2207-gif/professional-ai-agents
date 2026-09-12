# Rendered System Review

Serves: UI-16, UI-17 and verification for UI-01..UI-15.

## Rule: render is the visual evidence

Source code and token declarations show intent. They do not prove hierarchy, density, contrast, responsive behavior or cross-screen coherence.

When possible inspect:
- narrow viewport;
- desktop viewport;
- key loading/error/selected/disabled states;
- representative sibling screens.

If render evidence is unavailable, return `RENDER BLOCKED` for visual-quality claims that depend on it.

## 1. Review the system, not one screenshot

Operational product quality is cross-screen.

Compare:
- page backgrounds/surfaces;
- navigation;
- page headings;
- buttons;
- inputs/selects;
- tables/lists;
- statuses/badges;
- modals/sheets;
- empty/loading/error;
- spacing/radius/border/shadow;
- typography roles;
- semantic colors.

A locally attractive screen can still be a system failure if it creates a parallel visual language.

## 2. First-pass unanchored visual judgment

Before reading creator self-assessment, judge:
- task focal point;
- information hierarchy;
- density;
- scanability;
- component familiarity;
- state clarity;
- consistency;
- apparent quality;
- mobile viability.

Do not inflate scores to validate previous work.

## 3. Operational score dimensions

Use evidence-based qualitative or calibrated scoring for:
- hierarchy;
- density/scanability;
- typography;
- semantic color/value;
- spacing/rhythm;
- component consistency;
- table/list craft;
- form/action craft;
- navigation clarity;
- state clarity;
- responsive integrity;
- RTL integrity when applicable;
- accessibility visual craft;
- system coherence;
- product-specific appropriateness.

Do not use landing-page magnetism/originality thresholds as universal operational-product gates.

## 4. Visual-load audit

Count competing emphasis mechanisms:
- accent color;
- semantic color;
- borders;
- shadows;
- cards/panels;
- uppercase labels;
- mono type;
- icons;
- motion;
- background changes.

If many are active at once, check whether hierarchy collapses into noise.

## 5. Density audit

Ask:
- can the operator compare the records/data needed for the task?
- is space being spent on decoration rather than decisions?
- are critical labels/amounts too small because density is too high?
- is scrolling/navigation excessive because density is too low?

Judge against task frequency and risk.

## 6. State audit

Verify consistency of:
- selected/current;
- hover/focus;
- disabled;
- loading;
- error;
- warning;
- success;
- partial/unknown where relevant.

Critical state must not depend on hue alone.

## 7. Token/drift audit

When repository access exists, compare rendered inconsistency with implementation evidence.

Look for:
- duplicate semantic colors;
- near-duplicate backgrounds;
- many one-off spacing values;
- inconsistent radii;
- parallel button/input styles;
- hard-coded colors bypassing the system.

Do not assume every raw value is a bug. Link drift to an actual system role before proposing consolidation.

## 8. Responsive/RTL audit

At narrow width verify:
- primary task/action remains obvious;
- no horizontal page scroll;
- table/list transformation is usable;
- overlays fit;
- text does not collapse;
- sticky controls do not cover content/focus;
- density is rebalanced.

For RTL verify:
- layout direction is meaningful;
- mixed LTR data remains readable;
- directional icons are correct;
- numeric alignment remains useful.

## 9. Root-cause classification

- `UX CONTRACT` — approved interaction itself needs change.
- `SYSTEM` — visual roles/tokens/components are weak or incoherent.
- `IMPLEMENTATION` — approved system was not implemented faithfully.
- `CONTENT/DATA` — weak/missing/false content or runtime state prevents valid design.
- `ACCESSIBILITY` — contrast/focus/non-color/touch issue.
- `UNVERIFIED` — required artifact/state unavailable.

Do not patch an upstream UX problem with decorative styling.

## 10. Severity

- **P0** — critical state/consequence hidden, inaccessible core task, fabricated status/proof, unauthorized behavior change.
- **P1** — major hierarchy/system/mobile issue that materially harms repeated work or trust.
- **P2** — meaningful craft/consistency weakness.
- **P3** — minor polish.

## 11. Bounded repair

Group findings by root cause.

Prefer:
- fix the canonical token/component once;
- update the affected screens;
- re-observe representative states.

Avoid screen-by-screen cosmetic patches that preserve the broken system.

## Review output

1. observed screens/viewports/states;
2. strongest system decisions;
3. P0/P1/P2/P3 findings;
4. root-cause classification;
5. canonical repair set;
6. affected surfaces;
7. re-observation result.

Self-review may end with `RENDER READY FOR INDEPENDENT REVIEW`, never independent final product PASS.
