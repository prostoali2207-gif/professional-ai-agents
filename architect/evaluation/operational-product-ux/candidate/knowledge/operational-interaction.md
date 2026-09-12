# Operational Interaction Patterns

Serves: UX-02, UX-03, UX-04, UX-05, UX-06, UX-07, UX-08, UX-09.

Freshness: slow-changing professional guidance; refresh when authoritative design-system or accessibility guidance materially changes.

## 1. Forms and validation

Design questions around the information actually required for the task.

Classify every input:
- required by system;
- required by task;
- conditional/alternative;
- optional support;
- unnecessary.

Prefer persistent labels. Placeholder text is not a label.

Accept harmless input variation where the system can normalize it safely. Do not force users to repair formatting that software can interpret unambiguously.

Validation must help correction:
- state what went wrong;
- state what to do next;
- place guidance close to the affected control;
- keep valid previously entered values after recoverable validation errors;
- preserve unrelated form data when one field fails.

Distinguish:
- user-correctable validation;
- permission/eligibility;
- service/system failure.

Do not present all three as the same red field error.

### Timing

Validation timing is contextual:
- submit/continue validation is a safe default for complex forms;
- earlier validation may help when research/task evidence shows it prevents wasted work;
- avoid interrupting slow or partially complete input with premature error state.

When client-side validation exists, downstream/server validation still governs acceptance.

## 2. Information architecture and progressive disclosure

Progressive disclosure is useful when it removes irrelevant decisions, not when it merely creates more screens.

Prefer:
- one coherent surface when information must be compared together;
- staged flow when later decisions genuinely depend on earlier answers;
- primary-detail when users need persistent list context plus record depth;
- inline edit for frequent low-risk changes;
- review screen for consequential commit;
- exception queue when failed/uncertain items need separate attention.

Reject a wizard when repeated expert users would be forced through unnecessary navigation.

## 3. Data tables and lists

Use tabular structure when users compare the same attributes across records.

A strong operational table usually needs some combination of:
- search;
- filters;
- sorting;
- pagination or virtualization;
- column priority/management;
- expandable detail;
- row action;
- global action;
- selection/batch mode;
- loading/empty/error state.

Do not add every capability by default. Add what the task and data volume require.

### Retrieval controls

Search answers "find the record".
Filter answers "show the relevant subset".
Sort answers "order the current set".
Pagination/virtualization answers "handle scale".

Do not mix client-side sorting/filtering with server-side pagination in a way that implies the user is operating on the full dataset when only one page is present.

### Row vs global actions

Row action affects one item.
Global action affects the current collection/filter context.
Batch action affects selected items.

Keep these visually and behaviorally distinct.

## 4. Selection and bulk work

Selection scope must be explicit.

If "select all" means only the current page, say so through behavior/copy/state rather than implying the entire dataset.

Batch actions should appear after selection so they do not compete with normal table actions.

For partial batch success, report:
- total attempted;
- succeeded;
- failed;
- skipped/duplicate where relevant;
- reason/action for exceptions.

Preserve an exception path for unresolved records.

## 5. Operational states and provenance

Model only states the real data behavior makes applicable.

Common states:
- loading;
- empty;
- available;
- partial;
- stale;
- disconnected;
- unauthorized;
- error;
- success.

Keep these distinctions:
- missing is not zero;
- partial is not complete;
- stale is not current;
- configured is not connected;
- fallback/demo is not live;
- UI completion is not downstream acceptance.

When state matters to a decision, expose the source/freshness/scope needed to interpret it.

## 6. Consequential actions

Risk depends on:
- financial impact;
- legal effect;
- availability/resource state;
- destructive or irreversible effect;
- blast radius;
- reversibility;
- detectability of error.

Before a consequential commit, surface the data a competent operator needs to judge it.

A useful review includes:
- entity/target;
- old -> new state where relevant;
- amount/scope;
- downstream consequence;
- cancellation/back path;
- recovery/rollback when available.

Avoid generic "Are you sure?" when the real consequence can be stated.

Do not add confirmation to every safe frequent action. Excess confirmation trains users to dismiss it.

## 7. Expert efficiency

For repeated work, evaluate:
- meaningful decisions;
- navigation changes;
- information remembered from another view;
- re-entry of known data;
- unnecessary confirmation;
- search/filter effort;
- exception handling.

Efficiency mechanisms may include:
- stable defaults;
- retained context;
- recent/last-used values;
- keyboard support;
- bulk work;
- inline edit;
- persistent filters.

Use them only when they preserve clarity and error prevention.

## Provenance

Derived, copyright-safe operational principles informed by:
- GOV.UK Design System: validation and error-message guidance;
- IBM Carbon Design System: forms and data-table usage;
- PatternFly: data list/table, selection, bulk/global/row-action patterns;
- ZtotheZ Design Engineering: operational task/state/provenance mechanisms;
- Impeccable 4.3.1 Operate/shape mechanisms.

External systems are evidence sources, not qualification certificates.
