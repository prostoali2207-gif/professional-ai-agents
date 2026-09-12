# Operational Product UX/UI — B0 development run plan

Date: 2026-09-12
Issue: #298
Stage: DEVELOPMENT ONLY
Release evidence: NO
Held-out evidence: NO

## Objective

Run a small discriminating development batch against the two current 0.1.0 candidates before freeze.

This batch is allowed to inform candidate repair. It must not be reused as held-out release evidence.

## Candidate scope

- Operational Product UX / Interaction Design Core 0.1.0-candidate
- Product Interface / Design Systems Core 0.1.0-candidate

Both remain NOT QUALIFIED.

## B0 cases

### Operational UX
1. UX04_RECOVERABLE_FAILURE_DATA_PRESERVATION
2. UX07_SELECT_ALL_SCOPE_TRAP
3. UX08_CONSEQUENTIAL_GENERIC_CONFIRMATION
4. UX10_COLLAPSED_DESKTOP_MOBILE
5. UX13_BOUNDARY_DOMAIN_RULE_TRAP

### Product Interface
1. UI04_SEMANTIC_COLOR_DRIFT
2. UI08_COMPONENT_STATE_INCONSISTENCY
3. UI12_COLLAPSED_DESKTOP_RESPONSIVE
4. UI16_UNAUTHORIZED_UX_CHANGE
5. UI17_FAKE_OPERATIONAL_STATUS

All selected cases are P0 in the development fixture set.

## Execution

Candidate:
- provider: Gemini Interactions API
- model: gemini-3.5-flash-lite
- public synthetic fixtures only
- no tools or side effects
- current candidate SKILL + packaged knowledge supplied as runtime context

Development judge:
- provider: Gemini Interactions API
- model: gemini-3.5-flash
- receives fixture criteria and candidate observable output
- returns JSON PASS/FAIL and evidence
- judge is development feedback only; it is not release-calibrated

## PRE-RUN BUDGET GATE

Objective:
- find high-value P0 professional failures before freeze.

Decision impact:
- FAIL -> repair candidate professional layer and add regression;
- all B0 PASS -> proceed to broader B1 development coverage, not freeze automatically.

Eligibility:
- synthetic/public content only;
- existing repository Gemini credential;
- model availability was already probed successfully on PR #299 without generation.

Maximum budget:
- 10 candidate generation calls;
- 10 judge generation calls;
- 20 total generation calls maximum;
- no Groq calls;
- no image generation;
- no browser/paid external service calls.

Stop condition:
- stop remaining cases for a core immediately after its first confirmed development P0 FAIL;
- continue the other core independently;
- infrastructure failure does not count as professional FAIL;
- no retries except one transient 5xx retry per provider request.

Protected reserve:
- this B0 cannot consume or substitute the later fresh held-out and rendered practical qualification budget.

Mid-run exhaustion:
- preserve completed sanitized case results;
- return DEVELOPMENT_NOT_EXECUTABLE for unfinished cases;
- do not infer PASS from missing cases.

## Stop-loss

This is a new profession-specific development execution chain, not a generic qualification-platform repair.

If a technical defect prevents execution:
- classify it under issue #129 methodology;
- at most one bounded local repair plus one eligible retry for this B0 chain;
- another technical defect stops the chain.

## Result meanings

- B0 PASS: all selected P0 development cases pass. Candidate is still NOT QUALIFIED.
- B0 REVISE: a valid professional P0 development failure is confirmed.
- B0 NOT_EXECUTABLE: technical/provider failure prevents valid evidence.
