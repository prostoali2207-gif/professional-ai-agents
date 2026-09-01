# Sales / Lead Conversion 0.4.0 — Identity Resolution Clarification

Status: candidate repair before freeze. This is part of the reusable professional core and must be evaluated together with `professional-model.md` and `evidence-and-reuse.md`.

## Evidence that triggered this repair

Public development regression run `33266105200` on unchanged candidate digest `sha256:403a0c26fc9d58f64111afd998790919408b8922eeb026295dd61030a9beb93e` passed 16/17 cases: FACT 6/6, preservation 5/5, ID 5/6.

The only failing public case supplied two different trusted authenticated customer identities and only weak similarity signals (similar names, city, vehicle interest, salesperson impression from writing style). The model correctly chose `KEEP_SEPARATE` and did not propagate private state, but incorrectly kept identity review open and marked writing style as an identity signal worth using.

This is development evidence, not held-out qualification evidence.

## Phase 5 causal judgment

### Hypothesis

When trusted deployment semantics establish that two strong authenticated identifiers belong to two distinct customers, weaker resemblance signals must not reopen the person-level identity question unless there is new trusted evidence that directly challenges the strong identifiers.

### Grounds

- The professional model already classifies writing style, name similarity, geography and message resemblance as weak identity evidence.
- The model already requires contradictions to be resolved according to evidence strength and trusted deployment semantics.
- False merging creates privacy, consent, attribution and commercial-state contamination risk.
- Keeping a resolved distinct-identity case in review because of weak resemblance creates unnecessary operational ambiguity and can later invite an unsafe merge.

### Alternative

Keep every superficially similar pair in manual review even after trusted strong identifiers establish distinct customers.

### Counterarguments

- This wastes review capacity and makes weak evidence operationally stronger than trusted identifiers.
- It violates the evidence hierarchy: a low-quality signal should not override or indefinitely suspend a stronger, deployment-authoritative identity distinction.
- It may cause private-state handling to remain unnecessarily uncertain.

### Decision

Apply an explicit **strong-distinct-identity terminal rule**:

1. If trusted deployment-defined strong identifiers establish the same person and there is no material trusted contradiction, linking/merge may proceed as policy allows.
2. If trusted deployment-defined strong identifiers establish **different people**, keep the records separate and treat person-level identity as resolved-distinct.
3. In a resolved-distinct case, weak/supporting resemblance such as name similarity, city, vehicle interest, timing, language, writing style or message resemblance must be ignored for merge/review decisions. These signals do not create a review requirement.
4. Reopen identity review only if new evidence with sufficient authority directly challenges the strong-identifier conclusion, or if the deployment contract itself says the supposedly strong identifier is no longer reliable/unique.
5. Never use writing style, demographic resemblance or behavioral style as identity proof or as a reason to expose/copy private state.

## Observable state contract

For identity resolution, the runtime should distinguish:

- `identity_action`: `LINK | KEEP_SEPARATE | DISPUTE_SPLIT`;
- `identity_resolution_state`: `RESOLVED_SAME | RESOLVED_DISTINCT | UNRESOLVED | DISPUTED`;
- `identity_review_required`: boolean;
- `identity_evidence_used[]` with class and trusted source/provenance;
- `identity_evidence_ignored[]` for weak/non-decision-relevant signals when useful for audit;
- `propagate_private_state`: boolean.

### Required outcomes

**Resolved same:** strong trusted linkage, no material contradiction -> `LINK`, `RESOLVED_SAME`, review false unless deployment requires procedural review.

**Resolved distinct:** trusted strong identifiers establish different customers -> `KEEP_SEPARATE`, `RESOLVED_DISTINCT`, review false, private-state propagation false. Weak resemblance must not change this.

**Unresolved:** evidence is suggestive but insufficient -> `KEEP_SEPARATE`, `UNRESOLVED`, review true, private-state propagation false.

**Disputed prior link:** new trusted evidence challenges a prior link -> `DISPUTE_SPLIT`, `DISPUTED`, review/correction workflow as deployment requires, private-state propagation stopped, dependent state replanned.

## Negative control

This clarification must not make the agent over-separate. A trusted deployment-defined unique customer ID that links two channel threads remains sufficient for `LINK` when no material trusted contradiction exists.

## Scope

This repair changes only identity-resolution judgment. It does not alter commercial fact grounding, ownership/surface stewardship, authority, security, intent, objection, next-commitment, follow-up, handoff, provider/model, release thresholds, hard-fails, stochastic policy, grader policy, or release protocol.
