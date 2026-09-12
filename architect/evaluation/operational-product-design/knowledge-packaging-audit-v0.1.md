# Operational Product UX/UI — knowledge packaging audit v0.1

Date: 2026-09-12  
Issue: #298  
Status: pre-candidate audit

## Purpose

Ensure difficult UX/UI decisions do not depend on undeclared model priors. This audit maps material knowledge dependencies for the two proposed reusable cores.

## A. Operational Product UX / Interaction Design

| Competency | Hard decision | Material knowledge dependency | Packaging mode | Risk if absent | Required evaluation |
|---|---|---|---|---|---|
| UX-01 Task context | choose interaction model based on frequency/risk/reversibility | task analysis, consequential-action framing | EMBED_CORE + PROCEDURAL_MODULE | component-first design | ambiguous task fixture |
| UX-02 IA/path | wizard vs inline vs table/detail vs queue | interaction pattern trade-offs, memory burden, progressive disclosure | EMBED_CORE + REFERENCE_MODULE | fashionable but slow flow | conflicting-pattern case |
| UX-03 Fields | required vs conditional vs alternative | information requirement modeling, input semantics | EMBED_CORE + PROCEDURAL_MODULE | overlong forms, missing data | conditional form fixture |
| UX-04 Validation/recovery | when/how to validate and preserve data | GOV.UK/standards guidance, recovery patterns | REFERENCE_MODULE + LIVE_RESEARCH for superseded standards | user data loss, unusable errors | failure/retry practical |
| UX-05 Operational state | partial/stale/disconnected semantics | data provenance/state modeling | EMBED_CORE + REFERENCE_MODULE | false certainty | stale/partial adversarial |
| UX-06 Tables | retrieval controls and table vs alternatives | Carbon/PatternFly table mechanisms, dataset shape | REFERENCE_MODULE + LIVE_RESEARCH where current component behavior matters | unusable data surfaces | large dataset practical |
| UX-07 Bulk/exceptions | selection scope and partial success | bulk action patterns, reconciliation/exception models | PROCEDURAL_MODULE + REFERENCE_MODULE | accidental mass action | batch/exception fixture |
| UX-08 Consequential actions | confirmation/review proportional to risk | reversibility, confirmation design, domain consequence | EMBED_CORE + domain specialization | hidden financial/destructive effect | high-risk fixture |
| UX-09 Efficiency | expert speed without unsafe shortcuts | recognition/recall, repeated work heuristics | EMBED_CORE + artifact evidence | slow or cryptic workflows | repeated-task comparison |
| UX-10 Mobile | structural transformation of dense work | responsive interaction patterns, touch ergonomics | REFERENCE_MODULE + TOOL_BACKED render/browser | collapsed desktop | 390px practical |
| UX-11 Accessibility | keyboard/focus/drag/target/error behavior | WCAG 2.2, WAI-ARIA APG | LIVE_RESEARCH + REFERENCE_MODULE + TOOL_BACKED | inaccessible core tasks | deterministic + browser checks |
| UX-12 RTL | mixed-direction operational data | bidi/RTL layout principles, locale behavior | REFERENCE_MODULE + TOOL_BACKED render | reversed/garbled task flow | Arabic RTL practical |
| UX-13 UX writing | precise actions/errors/status | interface content guidance | REFERENCE_MODULE | vague actions, poor recovery | critique case |
| UX-14 Review | distinguish contract vs implementation failure | artifact-first verification procedure | PROCEDURAL_MODULE + TOOL_BACKED | source-only false PASS | rendered mismatch case |
| UX-15 Boundary | when to research/escalate | authority/evidence model | EMBED_CORE | invented business rules | adversarial premise |

### UX runtime packages

1. `forms-validation-recovery.md`
2. `tables-bulk-exceptions.md`
3. `operational-states-provenance.md`
4. `mobile-accessibility-rtl.md`
5. `consequential-actions-and-review.md`
6. `rendered-ux-review.md`

Core router should contain only compact stable judgment and routing triggers.

## B. Product Interface / Design Systems

| Competency | Hard decision | Material knowledge dependency | Packaging mode | Risk if absent | Required evaluation |
|---|---|---|---|---|---|
| UI-01 hierarchy | what visually dominates | perceptual hierarchy, task priority | EMBED_CORE + REFERENCE_MODULE | equal emphasis | comparative render |
| UI-02 density | compact vs spacious | operational density patterns | EMBED_CORE + REFERENCE_MODULE | marketing spacing or clutter | dense workspace pair |
| UI-03 typography | role system for data/control/meta | product typography, tabular data | REFERENCE_MODULE | noisy/inconsistent type | multi-screen artifact |
| UI-04 color/value | semantic state vocabulary | color semantics, contrast | EMBED_CORE + REFERENCE_MODULE + TOOL_BACKED | decorative/status confusion | state matrix + contrast |
| UI-05 rhythm | grouping without card explosion | spacing/rhythm/gestalt | REFERENCE_MODULE | arbitrary panels/cards | critique fixture |
| UI-06 surfaces | layer/elevation hierarchy | surface/elevation semantics | REFERENCE_MODULE | parallel visual worlds | screen family audit |
| UI-07 tokens | primitive/semantic/component boundary | design-system architecture | PROCEDURAL_MODULE + REFERENCE_MODULE | hard-coded drift | token-repair task |
| UI-08 components | consistent interactive states | component-state matrix | PROCEDURAL_MODULE | screen-by-screen inconsistency | cross-screen audit |
| UI-09 tables | comparison/readability/action clutter | operational table craft | REFERENCE_MODULE + rendered proof | unreadable dense data | table render |
| UI-10 forms | visual grouping/error/action hierarchy | form craft + UX contract | REFERENCE_MODULE | visual clean-up hides meaning | form render |
| UI-11 navigation | active/current/action hierarchy | app-shell patterns | REFERENCE_MODULE | lost location/competing nav | responsive shell task |
| UI-12 responsive | narrow transformation | responsive product craft | REFERENCE_MODULE + TOOL_BACKED | stacked clutter | narrow/wide render |
| UI-13 RTL | visual mirroring and mixed LTR | RTL/bidi visual rules | REFERENCE_MODULE + TOOL_BACKED | semantic reversal | RTL render |
| UI-14 accessibility | contrast/focus/non-color/touch | WCAG 2.2 + platform behavior | LIVE_RESEARCH + TOOL_BACKED | inaccessible states | deterministic + browser |
| UI-15 motion | feedback vs decoration | state motion heuristics, reduced motion | REFERENCE_MODULE | flow interruption | interaction review |
| UI-16 system audit | when hard-coded value is drift | token/system diagnostic procedure | PROCEDURAL_MODULE + TOOL_BACKED repo inspection | parallel themes | real diff audit |
| UI-17 rendered critique | concept vs system vs implementation | critique procedure | PROCEDURAL_MODULE + TOOL_BACKED | source-only PASS | artifact mismatch |
| UI-18 references | familiarity vs distinctiveness | reference literacy/product conventions | EMBED_CORE + LIVE_RESEARCH when benchmarking | imitation or novelty-for-novelty | reference trap |
| UI-19 authority/truth | visual change vs UX/product change | authority + evidence boundary | EMBED_CORE | styling alters semantics | adversarial case |

### UI runtime packages

1. `hierarchy-density-typography.md`
2. `semantic-color-surfaces-states.md`
3. `spacing-tokens-component-systems.md`
4. `operational-tables-forms-navigation.md`
5. `responsive-accessibility-rtl.md`
6. `rendered-system-review.md`

## C. Live research policy

Use live retrieval when:
- normative accessibility/platform guidance may be versioned;
- the task depends on current browser/platform interaction;
- a product/category pattern is being benchmarked and current implementations matter;
- a design-system component API/version is implementation-relevant.

Preferred source classes:
1. W3C/WAI normative or official guidance;
2. official design-system documentation (GOV.UK, Carbon, PatternFly, platform systems);
3. current product documentation where the product itself is evidence;
4. observed strong product implementations as examples, explicitly non-authoritative.

Do not use remembered volatile guidance as current fact when live retrieval is available.

## D. Tool-backed requirements

Rendered/runtime verification is required when the claim is observable.

Relevant tool classes:
- browser/render/screenshot observation;
- accessibility scanner as supporting evidence, never sole proof;
- deterministic token/color/spacing lint where available;
- repository diff/search for hard-coded design drift;
- interaction tests for keyboard/state/recovery.

If observation is unavailable, narrow the verdict to `RENDER BLOCKED` / `RUNTIME UNVERIFIED` rather than inventing confidence.

## E. Copyright/provenance rule

Store copyright-safe derived principles, not copied protected books or large third-party skill text.

External skills are provenance and capability evidence. New runtime modules must be independently written and must identify the decisions they support.

## F. Audit verdict

**MODULE_REQUIRED** for both proposed cores.

The competency descriptions alone are insufficient. Candidate construction may proceed only with the runtime packages above or an equivalent progressively disclosed structure, plus live-research/tool routing for versioned/observable claims.
