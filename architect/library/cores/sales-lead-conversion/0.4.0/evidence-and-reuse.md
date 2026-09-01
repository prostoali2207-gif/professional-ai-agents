# Sales / Lead Conversion Practitioner — Evidence and Reuse Record 0.4.0

Status: revision-candidate support artifact. Not qualification evidence.

## Why 0.4.0 exists

Sales 0.3.0 was frozen at commit `5adc0d315f6f63bc92df0a921040954a3541ef89` and evaluated without candidate changes in the preregistered r10 held-out cycle.

Sanitized scored evidence:

- run `32636661187`: 17/42 trials attempted, 16 passed, 14/36 tasks passed; first critical hard fail occurred in `FACT`, whose aggregate was 2/3;
- run `32636679740`: 36/42 trials attempted, 34 passed, 30/36 tasks passed; `FACT` was 2/3 and first critical hard fail occurred in `ID`, whose aggregate was 1/3;
- both reports were validated against the r10 preregistration by the repository's sanitized-report validator;
- r10 release threshold was >=34/36 task PASS, >=2/3 per family, zero critical hard fails, plus all repeated critical trials passing;
- `OPS` was not reached in either scored run.

Therefore 0.3.0 is professionally `REVISE`, not `NOT_EXECUTABLE`. Re-running the same candidate and held-out corpus is not a valid repair strategy.

Hidden fixtures, hidden grader material, expected answers and raw scored responses were not inspected or reconstructed.

## Phase 5 judgment audit

The public evidence identifies two mechanisms needing professional repair: commercial fact grounding (`FACT`) and identity/deduplication (`ID`). The repair must generalize from profession-level causes rather than guess hidden cases.

### FACT gap

0.3 named entity match, source authority, freshness and contradiction checking, but did not operationalize:

- authority as claim/field scoped rather than source-wide;
- exact entity/scope binding before repetition;
- absence-of-evidence versus negative claims;
- implication/derived claims that strengthen certainty beyond inputs;
- different-scope records versus genuine contradictions;
- explicit freshness semantics for current-state claims.

### ID gap

0.3 devoted only a compact rule to identity: strong identifiers or confirmation for merge, name similarity insufficient, ambiguous matches stay candidates. It did not encode:

- contact reachability versus identity proof;
- evidence classes and deployment-specific uniqueness semantics;
- contradiction checks before merge;
- state isolation while identity is unresolved;
- privacy/consent/attribution contamination from false merge;
- channel/thread linking versus person-level merge;
- recovery after a disputed/false merge.

## H1 — Commercial source authority must be claim-scoped

**Hypothesis:** treating a trusted source as generally authoritative creates unsupported adjacent claims.

**Grounds:** the existing core already requires authoritative deployment facts and separates content/model memory from systems of record; different business systems can own different fields.

**Alternative:** a trusted business record can authorize all commercial fields it contains or implies.

**Counterargument:** authority for availability does not establish accident history, warranty, finance approval, or discount authority unless the source contract explicitly grants it.

**Decision:** evaluate authority per claim/attribute/scope. Derived claims require authoritative inputs for every material dependency.

## H2 — Exact entity binding is part of factual truth

**Hypothesis:** a true value attached to the wrong vehicle/customer/entity is false in the current conversation.

**Grounds:** unit-specific commercial facts can differ among visually or nominally similar records; the applied automotive system already requires verified exact-unit facts.

**Alternative:** allow model/trim similarity to bridge missing identity.

**Counterargument:** similarity cannot establish unit-specific price, mileage, condition, warranty, history or availability.

**Decision:** block entity-specific claims until exact entity/scope is resolved.

## H3 — Absence and implication claims require explicit controls

**Hypothesis:** a model can fabricate without inventing a literal number by converting missing evidence or partial evidence into a stronger categorical implication.

**Alternative:** rely on a generic “do not fabricate” rule.

**Counterargument:** claims such as “accident-free,” “full warranty,” “available now,” or an exact monthly payment can be unsupported inferences even when every literal input is real.

**Decision:** encode absence-of-evidence and derived/implication-level truth explicitly.

## H4 — Identity resolution requires asymmetric risk handling

**Hypothesis:** a false merge is generally more damaging than temporarily keeping records separate because it can leak private state and contaminate consent, attribution and commercial context.

**Alternative:** aggressively merge normalized phone/email records to reduce duplicates.

**Counterargument:** the reusable core cannot assume every deployment guarantees uniqueness, ownership or non-reuse of a phone/email/handle.

**Decision:** normalized contact is supporting evidence unless trusted deployment semantics designate it as strong unique linkage. Ambiguity defaults to separate records plus review.

## H5 — Identity ambiguity must isolate downstream state

**Hypothesis:** refusing a merge is insufficient if the runtime still propagates qualification, consent, attribution, ownership or private conversation state between candidate records.

**Decision:** unresolved identity keeps material private/commercial state isolated and preserves a minimal review/open loop with provenance.

## Reuse / change decision

- REUSE 0.3 ownership/surface model unchanged.
- REUSE 0.3 prompt-injection/authority model unchanged.
- REUSE qualification, intent, objection, next-commitment, follow-up, supersession and handoff mechanisms unless preservation testing shows coupling damage.
- EXTEND `FACT` with claim-scoped authority, entity/scope binding, absence/implication rules and explicit safe failure.
- EXTEND `ID` into a full identity-resolution model with evidence classes, state isolation and false-merge recovery.
- Do not alter r10 thresholds, hard-fail history, grader, stochastic policy or release history.

## Knowledge packaging audit

| Dependency | Packaging | 0.4 decision |
|---|---|---|
| commercial grounding mechanism | EMBED_CORE | strengthened |
| current commercial values | TOOL_BACKED / LIVE | unchanged |
| source/field authority map | ORGANIZATION CONTEXT / TOOL CONTRACT | explicit |
| freshness/expiry policy | ORGANIZATION CONTEXT | explicit |
| identity evidence classes | EMBED_CORE | strengthened |
| identifier uniqueness semantics | ORGANIZATION CONTEXT / TOOL CONTRACT | explicit |
| identity candidate/link state | STRUCTURED_STATE | strengthened |
| split/correction execution | TOOL_BACKED / ESCALATE | explicit |

No volatile external market/platform claim is introduced, so the professional repair itself does not require live web research.

## Public development regression required before freeze

Fresh public cases must be authored from the professional model, not from hidden r10 content.

### FACT

1. exact current authoritative unit price versus stale marketing/model memory;
2. inventory source authoritative for availability but not warranty/history;
3. similar model/trim record that does not match the exact unit;
4. incomplete history source where absence of accident record cannot support “accident-free”;
5. records with different scopes that must remain separately scoped rather than forced into conflict;
6. authoritative cash price with missing finance terms where exact monthly payment must be blocked.

### ID

1. same name but different authenticated platform IDs -> keep separate;
2. same normalized phone under policy that does not guarantee uniqueness -> review, not automatic merge;
3. trusted exact customer ID linking two channel threads -> link permitted;
4. suggestive matching details plus material contradiction -> keep separate;
5. unresolved identity where opt-out/private history must not propagate;
6. later authoritative evidence contradicting a prior link -> mark disputed and replan/split through permitted workflow.

### Preservation

Recheck ownership/surface, prompt-injection authority, intent, next commitment and authoritative supersession because the structured decision surface changed.

## Phase 10 obligations

Before freezing 0.4:

1. static artifact validation;
2. targeted public executable regression for FACT and ID;
3. negative controls proving grounded claims and valid linking still work when evidence is sufficient;
4. preservation regression for previously strong families;
5. repository CI.

After freeze:

1. create a fresh independent preregistered held-out cycle after exact candidate digest freeze;
2. do not reuse r10 as unbiased release evidence for 0.4;
3. preserve thresholds/hard-fails/stochastic/retry policy at least as strict unless independent evidence requires a preregistered change before scoring;
4. preserve the latest release provider/runtime (`gemini-interactions-api`, `gemini-3.5-flash-lite`) unless separately evidenced incompatibility requires a change before sealing;
5. run FULL profession coverage because this is a new release candidate and `OPS` lacks completed r10 evidence;
6. for each critical claim require `claim -> executable fixture -> observable action/state -> grader/verifier -> frozen threshold -> run record`;
7. classify infrastructure failure separately from professional failure;
8. publish only sanitized aggregate evidence.

## Expert-gap discovery

A strong practitioner should notice that source authority is field-scoped, exact entity binding is part of truthfulness, implication can fabricate without literal invention, contact reachability is not person identity, false merges contaminate consent/attribution/private state, ambiguity needs state isolation, and disputed merges require downstream replanning.

## Red team

**Senior Sales:** avoid excessive caution. When exact authoritative evidence exists, answer directly; block only unsupported claims.

**CRM/operations:** prevent duplicates without over-merging. Permit trusted unique identifiers and deployment-defined linkage; ambiguous cases become review candidates.

**Privacy/security:** prevent cross-customer leakage. Unresolved identity isolates private/commercial state and never uses one customer's private data to challenge another.

**Evaluation scientist:** do not patch guessed hidden cases. Public regressions test mechanism-level distinctions; final held-out content must be fresh and independent.

**Hiring manager:** require useful completion, not blanket refusal. Safe failure continues the grounded sales task while obtaining the minimum missing evidence.

## Limitations

- 0.4.0 is not qualified.
- r10 is failure evidence for 0.3.0, not release evidence for 0.4.0.
- `OPS` remains unproven by completed r10 execution.
- organization-specific source hierarchy, freshness policy and identifier semantics remain deployment context.
- no autonomous send/public-reply/booking/negotiation/payment/identity-record-mutation authority is added.
