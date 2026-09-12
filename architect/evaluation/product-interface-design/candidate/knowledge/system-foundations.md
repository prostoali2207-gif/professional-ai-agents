# Product Interface System Foundations

Serves: UI-01..UI-08, UI-18, UI-19.

Freshness: stable/slow-changing craft principles; current accessibility and platform-specific requirements must be retrieved live when material.

## 1. Hierarchy before decoration

An operational screen should visually answer:

1. Where am I / what task am I doing?
2. What requires attention now?
3. What decision/action matters most?
4. Which data supports that decision?
5. What is secondary context?

Use position, scale, contrast/value, grouping and spacing first.

Avoid:
- every section having equal title weight;
- every card having equal visual weight;
- multiple competing primary buttons;
- accent color on non-priority decoration.

## 2. Density is task-dependent

Dense is not automatically bad. Sparse is not automatically premium.

Increase density when:
- users repeat the task frequently;
- comparison across records matters;
- metadata must stay visible;
- extra scrolling/navigation adds work.

Reduce density when:
- a decision is rare/high-risk;
- comprehension needs sequential focus;
- multiple unrelated concepts are colliding;
- the viewport is narrow.

The target is usable information per decision, not maximum whitespace or maximum compression.

## 3. Typography roles

Use a small coherent role set.

Typical operational roles:
- page/surface title;
- section heading;
- body;
- control label;
- helper/error;
- metadata;
- status;
- numeric/data value;
- code/ID/plate.

One strong UI sans family is often enough. Use mono/tabular numerals only where alignment or identifier character matters.

Prefer a tighter scale than marketing pages. Large display typography inside dense tools usually consumes space without improving task clarity.

Keep important metadata readable; do not bury critical state at 10px merely because it is "secondary-looking".

## 4. Semantic color and value

Separate:
- neutral surface hierarchy;
- interactive accent;
- semantic status;
- focus;
- selected/active;
- disabled.

Color roles should be stable across screens.

Suggested semantic vocabulary:
- primary interaction;
- success/available/paid;
- warning/partial/needs review;
- error/destructive/unpaid;
- info;
- selected;
- focus;
- disabled.

Do not use semantic colors as decoration.

Critical meaning needs text/icon/value/shape in addition to hue.

## 5. Surface hierarchy

Use as few layers as the product needs.

Typical roles:
- page background;
- primary work surface;
- secondary panel/sidebar;
- input/control surface;
- overlay/elevated surface;
- selected/active surface.

Borders, shadows and background shifts all communicate grouping/elevation. Stacking all three everywhere creates noise.

## 6. Spacing and rhythm

Use a limited spacing scale.

Relationship rule:
- items inside one concept are closer;
- sibling groups have more separation;
- major sections have the strongest separation.

Repeated structures should share rhythm.

Watch for accidental drift caused by many one-off values.

## 7. Radii, shadows and visual effects

Use them as system properties, not screen decoration.

Too many radius values create a fragmented product.
Heavy shadows are rarely needed for dense operational products.
Glass/gradients/glows should not obscure state, text or action hierarchy.

## 8. Token architecture

Use tokens when they reduce drift and make system intent explicit.

Three useful levels:

### Primitive
Raw values:
- neutral-900;
- blue-500;
- space-3.

### Semantic
Purpose:
- surface-page;
- surface-raised;
- text-primary;
- text-muted;
- interactive-primary;
- status-error;
- border-subtle.

### Component
Only when components need stable variation:
- button-primary-bg;
- table-row-selected;
- input-border-focus.

Do not create component tokens for every CSS property.

## 9. Systemization decision

A hard-coded value is likely drift when:
- the same role uses several slightly different values;
- no functional reason explains the variation;
- sibling screens look like different products;
- state meaning changes across surfaces.

A hard-coded value may be justified when:
- a one-off external brand/legal/document requirement exists;
- the component is intentionally isolated;
- system token would misrepresent its semantic role.

The goal is coherent behavior, not replacing every literal with a token.

## 10. Product-specific distinctiveness

Operational UI earns character through:
- precise hierarchy;
- strong data typography;
- intentional shell/navigation;
- domain-relevant information structure;
- controlled accent;
- polished states;
- subtle, consistent details.

Do not force novelty into standard controls.

Familiarity is valuable when it reduces hesitation.

## Provenance

Derived from:
- transferable visual-craft mechanisms in the existing visual-design/art-direction candidate;
- Impeccable 4.3.1 Operate mode;
- ZtotheZ Design Engineering token/system mechanisms;
- IBM Carbon and other official design-system patterns;
- project-local visual knowledge modules.

These sources inform mechanisms only; they are not transferred qualification.
