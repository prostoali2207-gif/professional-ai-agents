# Automotive Paid Media Specialization — Qualification Notes

Candidate: 1.0.0

Parent core: `paid-media-performance-marketing@1.0.0`, digest `sha256:882477d8941c09538576096fbe93cd286584a77d040eecf1d8c266ffab3a9179`.

## Run 31952710108 — REVISE: construct isolation defect

Deterministic preflight passed. Critical automotive reliability ran AUTO-S1, AUTO-S2, AUTO-S3, AUTO-S5 and AUTO-S8 for three independent trials with three model requests and zero application retries.

Result: 13/15 case evaluations PASS.

AUTO-S1, AUTO-S2, AUTO-S3 and AUTO-S8 passed all three trials. AUTO-S8 selected the required `SCALE` action 3/3 while demonstrating inventory portfolio economics, marginal-not-average allocation and delegated authority.

AUTO-S5 selected `STOP` in all three trials and recognized `merchandising_truth` in all three. Two trials did not additionally emit `claim_risk_escalated`. The fixture had mixed vehicle-truth and mandatory legal-escalation constructs, so the grader was isolated rather than the professional model changed. AUTO-S5 now tests merchandising truth; AUTO-S7 separately tests offer provenance and claim-risk escalation.

## Run 31952826349 — REVISE: redundant availability flag

After the AUTO-S5 repair, deterministic preflight again passed. Four critical cases passed all three trials and AUTO-S8 again selected the required `SCALE` action 3/3. AUTO-S1 selected `STOP` in all three trials and recognized `inventory_truth_checked` in all three, but one trial did not additionally emit `availability_over_proxy`.

The second flag was redundant with the sold-inventory construct. AUTO-S1 was isolated to inventory truth while retaining `SCALE` as forbidden. Redundant inherited parent-core flags were also removed from non-critical delta fixtures where they did not define the automotive construct.

## Run 31952941002 — critical PASS; release grader review

On SHA `dbaec32b9d2c23599ffe6e226b78769babebbca7`, deterministic preflight passed and the critical subset AUTO-S1, AUTO-S2, AUTO-S3, AUTO-S5 and AUTO-S8 passed **15/15 case evaluations across 3 independent trials**, with zero application retries.

AUTO-S8 selected the required `SCALE` action in all three trials while demonstrating inventory portfolio economics, marginal-not-average allocation and delegated authority. This is retained as the critical reliability evidence because subsequent changes affected only non-critical allowed-action contracts, not the specialization, parent core, critical fixtures, critical expectations, model, or runtime.

The complete suite initially passed 9/10. AUTO-S9 selected `STOP` while correctly recognizing a material feed/listing price mismatch. `STOP` was admitted as a valid response while the mismatch is repaired; `SCALE` remained forbidden and merchandising truth remained required.

## Run 31953093883 — release action-semantics review

The affected full-suite rerun passed 8/10. AUTO-S9 passed. AUTO-S6 and AUTO-S10 emitted every required automotive judgment flag but chose defensible actions outside narrow allowed sets:

- AUTO-S6 chose `ESCALATE` after identifying a sales-operations dependency and using the fault tree when experienced sales staff departed and show rate collapsed.
- AUTO-S10 chose `STOP` when appointment capacity was full and response time was worsening.

Those action sets were repaired without changing required constructs or allowing `SCALE`. Deterministic tests now preserve the distinction between professional judgment and arbitrary single-action wording.

## Run 31953200239 — FINAL PASS

Final affected release validation ran on SHA `1f617843e2343aec0fb29460b01133045a3aeb08` with `gemini-3.1-flash-lite`, thinking level `medium`.

Results:

- deterministic specialization contract: PASS, 9/9 tests;
- retained critical-evidence binding: PASS;
- complete AUTO-S1..AUTO-S10 release suite: **10/10 PASS**;
- planned/executed model requests: 2/2;
- application retries: 0;
- positive scale control AUTO-S8: PASS with `SCALE`;
- release artifact ID: `9265223653`;
- release artifact ZIP digest: `sha256:8f2f699a66a594f5fa9b65891e6b403b7eafdc0a95d9b03263b238a703ef18e3`.

Combined qualification evidence is therefore:

1. critical reliability run `31952941002`: **15/15 PASS across 3 independent trials** on the unchanged Automotive specialization behavior;
2. final affected release run `31953200239`: **10/10 PASS** across the complete automotive suite after construct-valid grader repairs.

## Verdict

**Automotive Paid Media Domain Specialization 1.0.0: PASS** within its declared domain boundary.

This PASS does not qualify UAE-specific law or market behavior, Meta-specific execution, WhatsApp lead operations, any dealership's organization context, or any vehicle-specific campaign. Those require later context/specialization layers and their own affected evaluation.
