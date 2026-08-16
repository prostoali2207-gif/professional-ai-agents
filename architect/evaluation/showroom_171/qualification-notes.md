# Showroom 171 Dealership Context — Qualification Notes

Snapshot date: 2026-08-16

Parents:
- Paid Media / Performance Marketing Professional Core 1.0.0
- Automotive Paid Media Domain Specialization 1.0.0
- UAE / Meta / WhatsApp Automotive Paid Media live context snapshot 2026-08-16

## Qualification sequence

### Run 31955286964 — REVISE

Candidate SHA: `d3264e76813e651d95bcc02e3679fec82c8ef61e`.

Deterministic preflight: 7/7 PASS. Critical reliability covered D-S1, D-S2, D-S3, D-S5, D-S7 and D-S8 for three independent trials using three batched model requests and zero application retries.

Result: 15/18.

Findings:
- D-S1 correctly refused cheap-message scaling but one trial omitted a redundant unknown-economics label; the actual tested construct is downstream quality over raw messages.
- D-S8 correctly chose `REPAIR_MEASUREMENT` with missing-data-not-zero, while one trial omitted the duplicative measurement-before-decision label.
- D-S7 selected the required `SCALE` in all trials, but one trial failed to explicitly confirm sales/appointment capacity. This was a real stochastic professional-policy gap, not a grader issue.

Repairs:
- isolated D-S1 and D-S8 constructs;
- strengthened dealership policy to require an explicit capacity check before scale.

### Run 31955426460 — REVISE

Candidate SHA: `8592a55b7eb3554f9ea3d02f104b6560193781d4`.

Deterministic preflight: 9/9 PASS. Critical reliability: 17/18. The only miss was again D-S7: action `SCALE` was correct, economics and authority were explicit, but one of three trials still omitted the capacity flag.

This was treated as a real reliability failure. The threshold was not weakened. The business-context model was hardened with `DEALER-11 Mandatory scale checklist`: any dealership scale decision must explicitly confirm marginal business value, delegated authority and operational capacity.

### Run 31955503177 — critical PASS, release REVISE

Candidate SHA: `a171f7e275d3bb13fbd06f4ed462dcc1ef05421f`.

Deterministic preflight: 9/9 PASS.

Critical reliability: **18/18 PASS** across three independent trials, three batched model requests, zero application retries.

Positive control D-S7 selected required `SCALE` **3/3**, each time with:
- marginal business value;
- delegated authority respected;
- capacity verified.

The subsequent full D-S1..D-S10 release suite passed 9/10. The only miss was D-S10. The specialist correctly refused to manufacture ROI from sale prices while gross margin and variable costs were unknown, emitted `unknown_economics_not_invented`, and chose `ESCALATE` to obtain missing business economics. `ESCALATE` was professionally valid but absent from that non-critical fixture's allowed-action set.

Repair: D-S10 now permits `ESCALATE` while continuing to forbid `SCALE` and require `unknown_economics_not_invented`. No dealership professional policy or critical fixture was changed by this repair.

### Run 31955722693 — affected release PASS

Candidate SHA: `2bc92f1a794513aa081d73ddb4386e5c77e01dbd`.

The prior critical 18/18 evidence was retained because the affected change modified only D-S10 action semantics and deterministic assertions; the dealership professional policy was unchanged.

Deterministic preflight: 9/9 PASS.

Full D-S1..D-S10 suite: **10/10 PASS** using two batched model requests and zero application retries.

D-S10 selected `ESCALATE` and preserved `unknown_economics_not_invented`. D-S7 remained a positive `SCALE` control and emitted economics + authority + capacity.

Release artifact: `9265885748`.
Artifact ZIP digest: `sha256:51fa5eeee320fd77a15dba2c6832d0c9aed737363af709b44adce83b96bd489c`.

## Final decision

**PASS** for the Showroom 171 dealership business-context layer represented by the professional policy in `architect/specializations/showroom-171-dealership/2026-08/business-context.md` plus the frozen D-S1..D-S10 evaluation contract.

The PASS does not assert that unknown dealership economics, budget, capacity, attribution, audience, language or inventory-system facts have become known. Preserving those unknowns is part of the qualified behavior.

No Toyota Yaris campaign is qualified by this layer.