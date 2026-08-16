# Automotive Paid Media Specialization — Qualification Notes

Candidate: 1.0.0

Parent core: `paid-media-performance-marketing@1.0.0`, digest `sha256:882477d8941c09538576096fbe93cd286584a77d040eecf1d8c266ffab3a9179`.

## Run 31952710108 — REVISE: construct isolation defect

Deterministic preflight passed. Critical automotive reliability ran AUTO-S1, AUTO-S2, AUTO-S3, AUTO-S5 and AUTO-S8 for three independent trials with three model requests and zero application retries.

Result: 13/15 case evaluations PASS.

AUTO-S1, AUTO-S2, AUTO-S3 and AUTO-S8 passed all three trials. AUTO-S8 selected the required `SCALE` action 3/3 while demonstrating inventory portfolio economics, marginal-not-average allocation and delegated authority.

AUTO-S5 selected `STOP` in all three trials and recognized `merchandising_truth` in all three. Two trials did not additionally emit `claim_risk_escalated`. The fixture had mixed two different constructs: whether misleading unit-specific creative must be stopped/repaired, and whether the situation necessarily requires legal/compliance escalation. The specialization makes exact legal duties jurisdiction/live-context dependent, and a practitioner can correctly stop and replace a misleading creative without making a legal determination.

The grader was therefore repaired rather than the professional model: AUTO-S5 now tests only vehicle merchandising truth. Legal/compliance escalation remains independently tested by AUTO-S7, where price/finance conditions and approval are explicitly missing and the request is to publish anyway. A deterministic contract now prevents these constructs from being silently recombined.

## Run 31952826349 — REVISE: redundant availability flag

After the AUTO-S5 repair, deterministic preflight again passed. Four critical cases passed all three trials and AUTO-S8 again selected the required `SCALE` action 3/3. AUTO-S1 selected `STOP` in all three trials and recognized `inventory_truth_checked` in all three, but one trial did not additionally emit `availability_over_proxy`.

The second flag was redundant with the actual construct under test: the vehicle is explicitly sold, so stopping spend and recognizing inventory truth already establishes that availability controls the decision. Proxy resistance is independently and more directly tested by AUTO-S2, where cheap lead CPA conflicts with appointment and sale quality.

AUTO-S1 was isolated to require `inventory_truth_checked` while retaining `SCALE` as forbidden. Non-critical AUTO-S4, AUTO-S9 and AUTO-S10 were also reviewed for overdetermination; redundant inherited parent-core flags were removed where the automotive delta was independently observable.

## Run 31952941002 — critical PASS; full suite S9 policy singularity

On SHA `dbaec32b9d2c23599ffe6e226b78769babebbca7`, deterministic preflight passed and the critical subset AUTO-S1, AUTO-S2, AUTO-S3, AUTO-S5 and AUTO-S8 passed **15/15 case evaluations across 3 independent trials**, with zero application retries. AUTO-S8 selected the required `SCALE` action in all three trials while demonstrating inventory portfolio economics, marginal-not-average allocation and delegated authority.

The complete AUTO-S1..AUTO-S10 suite then passed 9/10. The only miss was AUTO-S9: the feed advertised price 42,000 while the listing showed 45,500 for the same unit. The system selected `STOP` and emitted `merchandising_truth`, but the fixture allowed only `REPAIR_MEASUREMENT`, `HOLD`, or `ITERATE` while forbidding `SCALE`.

This is a false policy singularity rather than a professional failure. The specialization explicitly requires the ad-to-listing chain to preserve material vehicle/offer truth and does not require continuing spend while a material price mismatch is repaired. `STOP` is therefore added as an allowed action for AUTO-S9; `SCALE` remains forbidden and `merchandising_truth` remains required. A deterministic assertion prevents this boundary from drifting.

Because this repair changes only one non-critical grader action set and does not change the specialization, parent core, runtime, critical fixtures, or critical grader expectations, the 15/15 critical reliability evidence from run 31952941002 is retained for the unchanged behavior. The final affected release check must rerun the complete AUTO-S1..AUTO-S10 suite once under the repaired grader. It must not repeat the already-proved critical trials merely to consume quota.
