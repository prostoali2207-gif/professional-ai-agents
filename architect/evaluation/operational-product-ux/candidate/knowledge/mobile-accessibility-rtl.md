# Mobile, Accessibility and RTL Interaction

Serves: UX-10, UX-11, UX-12.

Freshness:
- WCAG/WAI and platform interaction guidance: LIVE_RESEARCH when material/current version matters.
- stable interaction principles below: reference module.

## 1. Narrow-screen transformation

Do not treat mobile as desktop stacked vertically.

At narrow width, preserve:
- task identity;
- primary action;
- decision-critical state;
- error/recovery;
- context needed to avoid mistakes.

Possible transformations:
- side navigation -> compact bottom/top/drawer navigation;
- multi-column workspace -> prioritized primary surface + detail transition;
- wide table -> priority columns + row detail / responsive list / horizontal region only when the task truly requires wide comparison;
- side panel -> sheet or dedicated detail route;
- multi-action toolbar -> primary action + explicit overflow for lower-frequency actions.

Do not hide a critical action merely to make the layout cleaner.

## 2. Touch ergonomics

Critical controls should be comfortably tappable and separated enough to avoid accidental activation.

WCAG 2.2 Success Criterion 2.5.8 defines a 24x24 CSS pixel minimum target-size requirement with documented exceptions. Product teams may choose larger ergonomic targets.

Avoid:
- tiny icon-only destructive actions;
- adjacent high-risk controls with weak separation;
- hover-only disclosure;
- fixed controls that cover the focused input or error message.

## 3. Keyboard operation and focus

A keyboard user must be able to identify where focus is and complete critical in-scope tasks.

Check:
- logical focus order;
- visible focus indicator;
- focus not obscured by sticky/fixed content;
- escape/cancel behavior for overlays where appropriate;
- no keyboard traps;
- action order matches visual/semantic order.

WCAG 2.2 includes Focus Not Obscured and additional focus guidance. Retrieve current W3C guidance when making normative claims.

## 4. Alternatives to dragging

If functionality relies on dragging, provide a single-pointer/non-drag alternative when required by WCAG 2.2 and when the task does not make dragging essential.

Operational tools should not make basic reordering/selection impossible for users who cannot drag precisely.

## 5. Error and status accessibility

Critical status must have a readable text/semantic signal in addition to color.

Errors should:
- identify the affected input or operation;
- explain correction/recovery;
- remain discoverable by keyboard/screen-reader users;
- preserve valid data.

Dynamic status should be exposed appropriately to assistive technology where implementation supports it.

## 6. RTL is structural

RTL adaptation may affect:
- navigation placement/order;
- breadcrumbs;
- back/forward icons;
- form alignment;
- table alignment;
- sheet/drawer origin;
- directional chevrons;
- step/progress direction.

Do not mirror values whose meaning remains LTR.

Common LTR islands inside Arabic UI:
- vehicle plates;
- contract IDs;
- phone numbers;
- VINs/codes;
- email;
- many dates;
- money/numeric columns depending on locale policy.

Use bidi isolation/appropriate markup in implementation. UX contract should explicitly call out mixed-direction values that must remain readable.

## 7. Mobile + RTL stress test

For an in-scope narrow RTL flow verify:
1. user can identify current task;
2. primary action is reachable;
3. critical amount/status is visible before commit;
4. no horizontal page scroll;
5. mixed-direction identifiers remain legible;
6. error text remains near the problem;
7. keyboard/focus path is coherent where relevant;
8. sheets/modals fit viewport and scroll safely;
9. back/cancel does not lose valid work.

## Provenance

- W3C WCAG 2.2 and WAI Understanding documents are normative/official sources for current accessibility requirements.
- WAI-ARIA APG should be retrieved live when widget-specific keyboard/ARIA behavior is material.
- Impeccable Operate and project-local UX knowledge informed product-specific stress-test framing but are not standards.
