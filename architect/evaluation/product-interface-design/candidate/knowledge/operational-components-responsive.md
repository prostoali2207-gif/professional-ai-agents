# Operational Components, Responsive, Accessibility and RTL

Serves: UI-08..UI-15.

## 1. Component-state completeness

For interactive components consider applicable:
- default;
- hover;
- focus;
- active/pressed;
- selected/current;
- disabled;
- loading;
- error;
- success.

Do not create visually unrelated state treatments screen by screen.

## 2. Buttons and actions

One primary action per local decision context is a strong default.

Use secondary/tertiary treatment for lower-priority actions.

Destructive visual treatment is reserved for genuinely destructive or irreversible actions.

Avoid icon-only critical actions unless the icon is universally clear and an accessible name is present; for consequential actions prefer visible text.

## 3. Tables and lists

Visual design should support comparison.

Prioritize:
- stable column alignment;
- clear primary identifier;
- numeric alignment;
- readable status;
- restrained row actions;
- visible selected state;
- clear batch-action mode;
- coherent loading/empty/error states.

Density can vary:
- compact when frequent scanning/comparison benefits;
- default/tall when rows contain richer multi-line content.

Do not turn tabular data into a card grid merely to make mobile or aesthetics easier.

On narrow screens choose among:
- priority columns + details;
- responsive record rows;
- dedicated detail view;
- bounded horizontal region when wide comparison is essential.

Avoid horizontal page scroll.

## 4. Forms

Group by task meaning, not database structure.

Visual contract should distinguish:
- label;
- control;
- helper;
- error;
- required/optional/conditional;
- section/group;
- review summary;
- primary/secondary actions.

Errors need enough contrast and text explanation. Do not rely on red border alone.

Long forms should not become one undifferentiated panel.

## 5. Statuses and badges

Status components should use one semantic vocabulary.

A badge is appropriate for concise categorical/state metadata. It should not become the only way to communicate a high-risk consequence.

Avoid a rainbow of unrelated badge colors.

Status vocabulary should map predictably:
- success/available/paid;
- warning/partial/review;
- error/unpaid/destructive;
- neutral/unknown/archived;
with project-specific labels layered on top.

## 6. Navigation and shell

The shell should make current location and product hierarchy obvious.

Check:
- active destination;
- current sub-view/tab;
- page title;
- relationship between navigation and primary page action;
- collapse behavior;
- mobile destination priority.

Avoid styling every navigation level as equally active.

## 7. Modals, sheets and popovers

Choose overlays based on task:
- popover: lightweight contextual choice/info;
- modal/dialog: focused decision that temporarily blocks background work;
- sheet/drawer: supporting detail/secondary workflow where retained context matters;
- full page: complex or high-stakes workflow that needs space/history.

Do not use modal as the first answer to every interaction.

Overlays must:
- fit viewport;
- scroll safely;
- keep close/cancel accessible;
- preserve focus;
- avoid clipping inside overflow containers.

## 8. Loading, empty and error presentation

Loading should preserve expected content structure where possible. Skeletons can help for content-shaped loading; use spinners where the task context makes them clearer.

Empty state should explain:
- what is empty;
- whether that is normal;
- next action if one exists.

Error state should show:
- what failed;
- affected scope;
- recovery/retry.

Do not display missing data as zero.

## 9. Responsive transformation

Responsive product design is structural.

Possible changes:
- collapse/replace side navigation;
- reorder secondary panels;
- convert multi-column grids;
- move lower-priority actions into overflow;
- adapt tables;
- convert persistent detail panel to route/sheet;
- keep primary action reachable.

Do not use fluid display typography as the primary responsiveness mechanism for dense product UI.

## 10. Accessibility visual craft

Retrieve current W3C/WAI guidance when making normative claims.

At minimum preserve:
- readable contrast;
- visible focus;
- focus not hidden by sticky/fixed UI;
- non-color cues;
- meaningful labels/icons;
- practical pointer targets;
- no hover-only critical content;
- reduced-motion support where motion is present.

Automated contrast/a11y tools are supporting evidence, not a substitute for task review.

## 11. RTL and mixed-direction craft

RTL is more than text alignment.

Review:
- shell/nav placement;
- tabs/breadcrumb direction;
- drawers/sheets;
- directional icons;
- button order where semantics require mirroring;
- table alignment;
- numeric columns;
- mixed LTR identifiers.

Keep LTR islands legible:
IDs, VINs, plates, phones, email, codes and similar values.

Do not mirror icons whose meaning is not directional.

## 12. Motion

In operational products, motion primarily communicates:
- state change;
- reveal/hide;
- feedback;
- loading;
- spatial relationship.

Avoid decorative page-load choreography and slow transitions that interrupt repeated work.

## Provenance

Derived from:
- Impeccable Operate product-interface mechanisms;
- IBM Carbon data-table/form patterns;
- PatternFly data list/table patterns;
- W3C WCAG 2.2 / WAI for current accessibility requirements;
- project-local visual/UX evidence.

Implementation details remain project/context dependent.
