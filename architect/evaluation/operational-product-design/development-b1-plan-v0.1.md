# Operational Product UX/UI — B1 development run plan

Date: 2026-09-12
Issue: #298
Stage: DEVELOPMENT ONLY
Prerequisite: B0 PASS recorded in PR #300 / run 34690536632
Release evidence: NO
Held-out evidence: NO

## Objective

Test professional discrimination beyond the B0 hard-fail set before candidate freeze.

B1 focuses on cases where a shallow checklist agent often produces a plausible answer but a strong practitioner should make a materially better decision.

## Selected cases

### Operational Product UX
- UX01_COMPONENT_FIRST_TRAP — P1
- UX02_WIZARD_FOR_FREQUENT_WORK_TRAP — P1
- UX03_CONDITIONAL_FORM_ALTERNATIVES — P1
- UX05_PARTIAL_STALE_DISCONNECTED_STATE — P0
- UX06_DENSE_TABLE_RETRIEVAL — P1
- UX14_RUNTIME_FALSE_PASS — P0

### Product Interface / Design Systems
- UI01_EQUAL_WEIGHT_HIERARCHY — P1
- UI02_MARKETING_SPACING_TRAP — P1
- UI03_TYPOGRAPHY_NOISE — P1
- UI06_PARALLEL_SURFACE_SYSTEMS — P1
- UI07_HARDCODED_TOKEN_DRIFT — P1
- UI14_POLISHED_BUT_OPERATIONALLY_WEAK — P1
- UI18_SOURCE_ONLY_VISUAL_PASS — P0

## Execution policy

Candidate:
- Gemini Interactions API
- gemini-3.5-flash-lite
- current candidate + packaged knowledge
- synthetic/public fixtures only

Development judge:
- Gemini Interactions API
- gemini-3.5-flash
- development-only, not release-calibrated
- judges explicit required/forbidden behavior and fixture criticality

Stop:
- stop remaining cases for a core on its first professional FAIL;
- continue the other core independently.

## PRE-RUN BUDGET GATE

Maximum:
- 13 candidate calls;
- 13 judge calls;
- 26 total generation calls;
- no Groq;
- no images;
- no external paid tools.

Decision effect:
- any valid FAIL -> repair the responsible professional layer and targeted regression;
- all B1 PASS -> candidate may proceed to pre-freeze expert-gap/red-team review; B1 PASS alone does not freeze or qualify.

Known quota/cost:
- exact provider billing is not asserted without account-specific evidence;
- call count is the hard budget control.

Mid-run failure:
- preserve completed results;
- technical/provider failure -> DEVELOPMENT_NOT_EXECUTABLE;
- do not convert unexecuted cases into PASS.

## Governance

Paid execution is manual-only through workflow_dispatch.

This is a later development stage than B0 and tests different fixture families. It is not a retry of the repaired B0 workflow-trigger defect.

Issue #129 stop-loss remains binding for any B1 technical repair.
