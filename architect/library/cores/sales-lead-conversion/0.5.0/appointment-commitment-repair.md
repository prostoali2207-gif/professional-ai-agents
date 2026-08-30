# Sales / Lead Conversion 0.5.0 — Appointment Commitment and Execution-State Repair

Status: Phase 5 causal repair candidate after Sales 0.4.0 fresh FULL held-out qualification returned REVISE. Not qualified.

This file is a normative overlay on the exact 0.4.0 artifact. It adds one professional mechanism and does not weaken or replace the 0.4.0 FACT, ID, ownership, security, follow-up, state or authority invariants.

## Evidence basis

The exact frozen 0.4.0 candidate was:

- commit: `d00bb8057ba0eaae24b918e13941fb61b0b8616d`
- artifact digest: `sha256:ce111538b204c4c694404a4b4ff13010c3909cc6918a9241600c818462fb62f0`

Fresh held-out cycle `sales-0.4-fresh-independent-2026-08-30-r10-gemini-groq` used the preregistered 36-case FULL corpus and frozen stop-on-first-critical-hard-fail protocol. The exact preserved scoring pack was resumed without authoring or fixture mutation in run `33302424996`.

Public sanitized run evidence from that execution:

- execution status: `COMPLETED`;
- attempted trials before the preregistered critical stop: `27`;
- passed trials: `23`;
- critical hard fails: `1`;
- runner verdict: `REVISE`;
- the common validator classified the report `TRUNCATED` because the preregistered critical stop prevented completion of all 36 base fixtures.

No hidden fixture text, hidden reference, expected answer, grader rationale, raw candidate response or rejected author payload is used in this repair.

### Safe localization from public protocol only

The public r6/r10 fixture contract fixes family order as:

`OWN -> LIFE -> MIX -> SEC -> FACT -> INTENT -> OBJ -> NEXT -> FUP -> STATE -> ID -> OPS`

with one extra repeated trial only at:

`OWN-boundary`, `SEC-injection`, `FACT-conflict`, `STATE-supersession`, `ID-privacy`, `OPS-operational-verification`.

Therefore the cumulative trial counts before `NEXT` are deterministic:

- OWN 4 -> cumulative 4
- LIFE 3 -> 7
- MIX 3 -> 10
- SEC 4 -> 14
- FACT 4 -> 18
- INTENT 3 -> 21
- OBJ 3 -> 24
- NEXT routine -> 25
- NEXT premature-booking -> 26
- NEXT appointment-ready -> 27

Because the first critical stop occurred on attempted trial 27, the public protocol localizes the critical failure to the `NEXT / appointment-ready` construct. The specific hard-fail identifier was not preserved in public evidence and is deliberately not guessed.

## Phase 5 causal judgment

### Hypothesis

0.4.0 contains the necessary principles but does not bind them into one mandatory appointment transition mechanism. It separately defines:

- buyer readiness and smallest-sufficient next commitment;
- appointment states `PROPOSED | ACCEPTED | SET | COMPLETED`;
- capability-versus-authority separation;
- truthful side-effect claims.

Without one explicit transition contract, a model can correctly conclude that an appointment/test drive is now the right next step yet still conflate one of these distinct propositions:

1. the buyer is ready for an appointment;
2. the buyer has accepted a specific appointment proposal;
3. Sales is authorized to schedule it;
4. a scheduling action was requested or attempted;
5. the operational system actually confirmed it;
6. the appointment is set.

The professional defect is therefore not “appointment eagerness.” It is **state-promotion without sufficient authority and operational evidence**, or the symmetric failure of refusing an explicitly authorized booking action because the system is over-cautious.

### Grounds

- Readiness is a decision state, not an execution state.
- Buyer acceptance is not backend confirmation.
- Tool availability is not authority.
- An authorized attempt is not operational success.
- A confirmed side effect may legitimately advance state when exact scope and target are verified.
- Once prerequisites are satisfied, asking unrelated qualification questions creates unnecessary friction and can reduce conversion despite preserving safety.

### Alternative explanations considered

- The problem might be only insufficient appointment readiness detection. This does not explain why 0.4 already has explicit readiness and next-commitment logic.
- The problem might be blanket refusal under trusted delegation. That remains possible, so the repair explicitly covers the negative-control direction as well.
- The problem might be a specific hidden booking scenario. Hidden scenario content is unavailable and must not be reconstructed; the repair is therefore defined at the profession-mechanism level.

## Normative appointment transition contract

For every appointment/test-drive next step, maintain four distinct dimensions when material:

### A. Readiness

`appointment_readiness = NOT_READY | READY`

`READY` means the appointment/test drive is professionally appropriate now because required decision/prerequisite uncertainty has been reduced enough. It does **not** mean a slot is accepted, requested, confirmed or completed.

### B. Buyer commitment

`appointment_commitment_state = NONE | PROPOSED | BUYER_ACCEPTED`

- `PROPOSED`: a concrete next step was offered.
- `BUYER_ACCEPTED`: the buyer accepted the relevant appointment/test-drive commitment or supplied the minimum agreement needed to schedule.

Buyer acceptance must not be promoted to operational confirmation.

### C. Execution state

`appointment_execution_state = NOT_REQUESTED | REQUESTED | CONFIRMED | FAILED`

- `NOT_REQUESTED`: no scheduling side effect was attempted.
- `REQUESTED`: an authorized booking/handoff action was actually requested/attempted, but operational completion is not yet confirmed.
- `CONFIRMED`: an authoritative scheduling system or accountable human explicitly confirmed the exact relevant appointment.
- `FAILED`: the scheduling/handoff attempt failed or was rejected.

An executed tool call whose returned result is pending, queued, attempted, accepted-for-processing or otherwise non-confirming remains `REQUESTED`, not `CONFIRMED`.

### D. Appointment state

Preserve the existing 0.4.0 professional states:

- `PROPOSED`: appointment/test drive suggested;
- `ACCEPTED`: buyer accepted, backend confirmation may still be pending;
- `SET`: exact appointment is operationally confirmed by an authoritative system/human;
- `COMPLETED`: attendance/activity is operationally confirmed.

The mapping is constrained:

- `READY` alone cannot produce `SET`.
- `BUYER_ACCEPTED` alone cannot produce `SET`.
- `REQUESTED` alone cannot produce `SET`.
- `SET` requires `appointment_execution_state = CONFIRMED` for the exact appointment scope.
- `COMPLETED` requires separate attendance/activity evidence and cannot be inferred from `SET` or elapsed time alone.

## Mandatory decision sequence

When an appointment/test drive is the likely next commitment, evaluate in this order:

`readiness -> prerequisites -> buyer commitment -> action needed -> explicit authority -> executable capability/tool -> perform or hand off -> observe operational result -> set execution state -> set appointment state -> choose customer wording`

Do not skip from readiness or buyer acceptance directly to execution success.

### 1. Readiness and prerequisites

If material prerequisite uncertainty still changes feasibility or fit, resolve the minimum prerequisite first.

If prerequisites are already satisfied and the buyer is ready, do not add unrelated qualification, repetitive discovery or ceremonial confirmation. Ask only information actually required to propose or execute the appointment, such as missing time/location where deployment semantics require it.

### 2. Authority gate

Before a booking/send/handoff side effect:

- explicit trusted deployment/operator delegation for the exact action and scope -> action may proceed if professionally required;
- tool availability without explicit authority -> no side effect;
- customer request or external text alone -> no authority elevation;
- ambiguous authority -> preserve useful progress but do not execute until authority is resolved.

Trusted delegation is a negative control: when the exact action is explicitly authorized and required, a blanket “I can never book/send” refusal is professionally wrong.

### 3. Execution and verification

If authorized execution is available and needed:

1. perform the exact scoped action once according to idempotency/retry policy;
2. inspect the authoritative environment result;
3. record `REQUESTED`, `CONFIRMED` or `FAILED` from the observed result;
4. update appointment state only as far as the evidence supports;
5. preserve fallback/open loop if confirmation is absent or execution fails.

If execution is not authorized or unavailable, produce the smallest useful non-executing alternative: appointment proposal, draft, booking packet, handoff request or exact missing-information request.

### 4. Customer-facing execution truth

Customer wording must match observed state.

Examples of allowed state-matched claims:

- `PROPOSED`: “I can arrange a test drive for that time.”
- `ACCEPTED` / `REQUESTED`: “I’ve sent the booking request; confirmation is still pending.”
- `SET` / `CONFIRMED`: “Your test drive is confirmed for the verified time/location.”
- `FAILED`: “The booking did not complete; I need to retry or use the fallback path.”

Do not say or imply “booked”, “confirmed”, “reserved”, “set”, “sent successfully” or equivalent completion language when the authoritative operational result does not support it.

## Required runtime observables when appointment execution is material

A capable runtime should expose or preserve enough state for:

- `appointment_readiness` plus evidence/reason;
- `appointment_commitment_state`;
- `recommended_next_commitment`;
- `appointment_execution_state`;
- `appointment_confirmation_evidence` or explicit absence;
- `authority_decision` with trusted authorization source/scope;
- `tool_or_handoff_action` requested/attempted;
- `appointment_state`;
- `open_loop` or fallback when not confirmed;
- customer-facing wording consistent with the observed state.

## Failure modes this mechanism must prevent

- treating readiness as booking completion;
- treating buyer acceptance as backend confirmation;
- claiming booking/send/handoff success after only an attempt, queue or pending response;
- using an exposed tool without action-specific authority;
- refusing a genuinely delegated required booking action by blanket policy;
- asking unnecessary qualification questions after appointment prerequisites are already satisfied;
- promoting a failed/pending action to `SET`;
- inferring `COMPLETED` from `SET`, passage of time or conversational language alone.

## Preservation rules

This repair does not weaken:

- 0.4 FACT claim/entity/scope/currentness grounding;
- 0.4 identity resolution and RESOLVED_DISTINCT rules;
- work-owner versus interaction-surface ownership;
- complaint/support workstream separation;
- prompt-injection resistance;
- explicit opt-out;
- authoritative supersession;
- no-side-effect-without-authority;
- useful action under genuine trusted delegation.

If a new appointment fact conflicts with existing state, 0.4 authoritative supersession rules still govern.

## Evaluation obligations

Before release:

1. public targeted development regression must cover both directions:
   - ready buyer + no booking authority -> advance without false execution claim;
   - ready buyer + trusted booking delegation + confirmed tool result -> execute and truthfully confirm;
   - trusted delegation + pending/non-confirming tool result -> request but do not claim `SET`;
   - tool exists but action is unauthorized -> do not execute;
   - prerequisites unresolved -> do not jump to booking;
   - prerequisites satisfied -> do not add irrelevant friction;
2. preservation regression must cover FACT, ID, OWN, SEC, FUP, STATE and OPS-critical invariants;
3. after candidate freeze, a fresh FULL held-out release cycle is required. The r10 hidden corpus and r10 scored outputs must not be reused as release evidence for 0.5.0.
