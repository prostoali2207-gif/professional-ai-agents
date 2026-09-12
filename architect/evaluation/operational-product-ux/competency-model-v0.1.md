# Operational Product UX / Interaction Design — competency and evidence model v0.1

Date: 2026-09-12  
Issue: #298  
Status: candidate-design input; not qualification evidence

## Mission

Design operational workflows that let real users complete repeated, data-heavy, consequential work quickly and safely, with clear state, low memory burden, recoverable errors, appropriate bulk/exception handling, and usable mobile/keyboard/RTL behavior.

## Professional boundary

Own interaction structure, task flow, information requirements, states, validation, recovery and implementation-ready UX contracts.

Do not own:
- business/domain rules;
- visual styling as a profession;
- frontend implementation;
- fabricated user research or metrics;
- final independent approval of own work.

## Competency families

### UX-01 — Task and operating-context modeling
**Criticality:** CORE / P0 when wrong.

**Professional purpose:** model the real operator job before choosing screens or components.

**Observable capability**
- identifies trigger, goal, completion signal, frequency, criticality, inputs, outputs and failure impact;
- separates frequent safe work from rare/consequential work;
- identifies source of truth and data dependencies;
- distinguishes user evidence from assumptions.

**Expert discriminator**
A strong practitioner notices that two visually similar actions may need different interaction models because frequency, reversibility or financial/legal impact differs.

**Failure modes**
- starts from components;
- optimizes clicks without task context;
- invents personas/requirements;
- treats rare and frequent work the same.

**Evidence chain**
claim -> ambiguous operational brief -> explicit task/risk/source model -> domain-aware grader + deterministic coverage checks.

### UX-02 — Information architecture and path modeling
**Criticality:** CORE.

**Observable capability**
- defines entry, primary action, decision points, alternates, completion, back/edit and recovery;
- minimizes recall across screens;
- uses progressive disclosure only when it reduces decision burden;
- chooses table, primary-detail, inline edit, wizard, queue or review screen based on work shape rather than fashion.

**Expert discriminator**
Can explain why a familiar pattern fits this task and what failure a competing pattern would introduce.

**Adversarial trap**
User asks for "a wizard because it looks cleaner" when repeated expert work would become slower.

### UX-03 — Information requirement and field modeling
**Criticality:** CORE.

**Observable capability**
Classifies each datum as:
- system required;
- task required;
- conditional/alternative;
- optional support;
- unnecessary.

Defines purpose, format, input behavior, validation timing, persistence and failure recovery.

**Failure modes**
- all fields mandatory;
- placeholder-only labels;
- strict formatting with no task reason;
- clearing valid input after unrelated error.

### UX-04 — Validation, error prevention and recovery
**Criticality:** CORE / P0 for data loss or false success.

**Observable capability**
- prevents predictable errors before commit;
- uses actionable field and global errors;
- preserves valid entered data after recoverable failure;
- distinguishes user-correctable validation from service/system failure;
- defines retry and partial completion;
- never presents success before downstream acceptance when acceptance matters.

**Knowledge dependencies**
GOV.UK validation/error guidance; WCAG input assistance; domain constraints.

**Adversarial trap**
Network failure after a long form; weak agent resets the form or claims success.

### UX-05 — Operational states and provenance
**Criticality:** CORE.

**Observable capability**
Designs only applicable states, including:
loading | empty | available | partial | stale | disconnected | unauthorized | error | success.

Keeps:
- missing != zero;
- partial != complete;
- stale != current;
- configured != connected;
- interface available != downstream accepted.

**Expert discriminator**
Recognizes when state/provenance ambiguity creates an operational decision error even if the UI looks polished.

### UX-06 — Data tables, lists and retrieval controls
**Criticality:** CORE for data-heavy products.

**Observable capability**
Chooses and specifies:
- search/filter/sort;
- pagination/virtualization;
- column priority;
- expansion;
- row vs global actions;
- sticky behavior where justified;
- primary-detail patterns;
- empty/loading/error states.

**Knowledge dependencies**
Carbon and PatternFly table guidance plus project data characteristics.

**Failure modes**
- card grid for tabular comparison;
- table with no retrieval controls;
- horizontal overflow as default mobile plan;
- client sorting over server pagination that misrepresents results.

### UX-07 — Selection, bulk work and exception queues
**Criticality:** CORE for repeated operations.

**Observable capability**
- exposes bulk actions only after selection;
- makes selection scope clear;
- separates normal work from exceptions;
- supports review of uncertain/failed items;
- defines partial bulk success and reconciliation.

**Adversarial trap**
"Select all" appears to mean all records but only selects visible page without explanation.

### UX-08 — Consequential action design
**Criticality:** BOUNDARY-CRITICAL / P0.

**Observable capability**
For financial, legal, availability, destructive or irreversible actions:
- shows decision-critical context before commit;
- makes amount/scope/consequence explicit;
- uses review/confirmation proportional to risk;
- preserves cancel/back;
- defines idempotency/double-submit expectations where implementation matters;
- provides recovery/rollback when possible.

**Failure modes**
- hidden totals;
- generic "Are you sure?";
- destructive icon-only action;
- confirmation everywhere including trivial safe actions.

### UX-09 — Efficiency for expert/repeated work
**Criticality:** CORE.

**Observable capability**
- supports recognition over recall;
- reduces unnecessary navigation;
- preserves context;
- uses defaults, recent values, shortcuts or batch operations only when evidence/work pattern supports them;
- does not trade error prevention away for speed.

**Expert discriminator**
Can optimize a repeated manager task without turning the interface into unexplained power-user controls.

### UX-10 — Mobile and touch interaction
**Criticality:** CORE where mobile supported.

**Observable capability**
At narrow widths:
- preserves primary task and critical state;
- avoids desktop stacking as the only adaptation;
- prevents horizontal page scroll;
- makes controls tappable and reachable;
- handles keyboards and sticky controls;
- rethinks dense tables into priority/detail/breakpoint patterns when required.

### UX-11 — Keyboard and accessibility interaction
**Criticality:** BOUNDARY-CRITICAL.

**Observable capability**
- semantic labels;
- logical focus order;
- visible focus;
- keyboard completion;
- errors exposed in text;
- no color-only meaning;
- alternatives to dragging;
- target-size and focus-obscuration constraints;
- status updates surfaced appropriately.

**Knowledge dependencies**
WCAG 2.2 and WAI-ARIA APG where widget behavior is involved.

### UX-12 — RTL/localization and mixed-direction data
**Criticality:** CONTEXTUAL but CORE for Arabic products.

**Observable capability**
- treats RTL as layout/flow behavior, not text alignment;
- preserves readable LTR values such as plates, IDs, phone numbers, money and codes;
- tests icon/action ordering, table alignment, dates and mixed-direction strings;
- avoids semantic reversal of controls that should remain physically/chronologically stable.

### UX-13 — UX writing and action clarity
**Criticality:** CORE.

**Observable capability**
- explicit action labels;
- plain error messages;
- status text that says what happened and next action;
- avoids vague "Submit/Continue" when task-specific label matters;
- does not invent guarantees or business claims.

### UX-14 — Rendered/runtime UX review
**Criticality:** CORE / verification.

**Observable capability**
After implementation:
- inspects actual rendered/runtime flow;
- checks contract fidelity;
- tests key states and recovery;
- classifies failures as contract vs implementation vs domain dependency;
- returns bounded repair, then re-observes.

Source inspection alone cannot prove rendered/runtime UX.

### UX-15 — Boundary and evidence discipline
**Criticality:** P0.

**Observable capability**
- does not invent business rules, user research or data behavior;
- escalates upstream domain uncertainty;
- does not silently take visual-design or engineering authority;
- distinguishes observed evidence, documented guidance, inference and assumption.

## Coverage requirements

Every CORE or BOUNDARY-CRITICAL competency must receive:
- application evidence;
- diagnosis evidence;
- judgment/conflict evidence;
- verification evidence;
- adversarial evidence where a plausible shortcut exists.

Knowledge-only probes cannot establish readiness.

## Required practical families

1. repeated expert table workflow;
2. long/conditional form with recoverable validation;
3. bulk import or reconciliation with row-level exceptions;
4. high-risk financial/destructive action;
5. stale/partial/disconnected state;
6. mobile narrow-screen flow;
7. Arabic RTL + mixed LTR values;
8. misleading stakeholder premise;
9. implementation mismatch requiring rendered review.

## Hard fails

Any candidate remains NOT QUALIFIED if it:
- loses valid user-entered data on recoverable error without necessity;
- hides decision-critical financial/destructive impact;
- claims success without required downstream success evidence;
- fabricates business/user evidence;
- produces unusable mobile for an in-scope task;
- relies on color alone for critical state;
- exceeds professional authority in a consequential way;
- passes an artifact without observing the render/runtime when observation is available and required.
