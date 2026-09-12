# Rendered / Runtime UX Review

Serves: UX-14 and verification for UX-01..UX-13.

## Rule: behavior is the evidence target

A source file, design brief or successful build can show intent. It cannot prove the real flow works.

When the task is observable, review the actual interface/runtime.

## Review inputs

Prefer:
- approved UX contract;
- relevant domain/business contract;
- implementation diff where useful;
- narrow + desktop render;
- key state screenshots or runtime transitions;
- browser/interaction evidence;
- accessibility/tool evidence as support.

If the required render/runtime cannot be observed, return `RUNTIME UNVERIFIED` for claims that depend on it.

## Review sequence

### 1. Re-state the task

Record:
- operator;
- trigger;
- completion signal;
- task frequency/risk;
- expected state transition.

Do not review "the screen" without the task it serves.

### 2. Verify path clarity

Check:
- primary next action;
- decision points;
- back/edit;
- alternate path;
- completion;
- exception route.

Flag if the user must remember information from another screen unnecessarily.

### 3. Verify information rules

Check:
- required vs optional/conditional;
- alternatives work as contracted;
- labels and formats;
- no new implementation-required field appeared without contract change.

### 4. Verify states

Exercise applicable:
- loading;
- empty;
- error;
- partial;
- stale;
- disconnected;
- permission/unauthorized;
- success.

Do not invent states that the data model does not support.

### 5. Verify failure and recovery

Trigger at least one meaningful recoverable failure when safe/practical.

Check:
- entered valid data remains;
- error explains correction;
- retry exists;
- false success does not appear;
- duplicate submit is controlled where relevant.

### 6. Verify consequential commit

For high-risk actions verify the user can see:
- target;
- amount/scope;
- resulting state;
- irreversible/downstream consequence;
- cancel/back.

### 7. Verify repeated/bulk work

When in scope:
- selection scope;
- bulk action appearance;
- partial success;
- exception handling;
- context retention;
- retrieval controls.

### 8. Verify narrow/accessibility/RTL

Use the dedicated module.

## Root-cause classification

Classify each material issue:

- `DOMAIN CONTRACT` — missing/incorrect business rule or source-of-truth behavior.
- `UX CONTRACT` — interaction design itself is weak/incomplete.
- `IMPLEMENTATION` — approved interaction was not implemented faithfully.
- `DATA/STATE` — runtime/state semantics do not match contract.
- `ACCESSIBILITY` — keyboard/focus/semantic/touch problem.
- `UNVERIFIED` — evidence unavailable.

Do not repair implementation failures by redesigning the UX contract unless the implementation exposed a real contract weakness.

## Severity

- **P0** — corrupts/loses critical data, creates false success, hides consequential impact, makes core in-scope task impossible, or violates authority/truth boundary.
- **P1** — major friction/confusion likely to block meaningful users or repeated work.
- **P2** — meaningful usability weakness with clear recovery.
- **P3** — minor polish or low-impact inconsistency.

## Review output

1. observed target/states/viewports;
2. task completion verdict;
3. P0/P1/P2/P3 findings;
4. root-cause layer per finding;
5. bounded correction set;
6. re-observation result.

PASS requires no unresolved P0/P1 and direct evidence for claims that require runtime observation.
