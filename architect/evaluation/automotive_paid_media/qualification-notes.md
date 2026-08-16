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

The complete AUTO-S1..AUTO-S10 suite then passed 9/10. The only miss was AUTO-S9: the feed advertised price 42,000 while the listing showed 45,500 for the same unit. The system selected `STOP` and emitted `merchandising_truth`, but the fixture did not allow `STOP`.

`STOP` is professionally valid while a material price mismatch is repaired. It was added as an allowed action; `SCALE` remains forbidden and `merchandising_truth` remains required.

## Run 31953093883 — release semantics review

The affected full-suite rerun passed 8/10. AUTO-S9 passed under the repaired contract. The two misses again had all required automotive judgment flags but selected professionally defensible actions outside an overly narrow action set:

- AUTO-S6 recognized both `sales_ops_dependency` and `fault_tree_used` after experienced sales staff departed and show rate collapsed, but selected `ESCALATE` rather than only `HOLD`/`ITERATE`. Escalating an identified sales-operations dependency is valid and does not imply cutting media.
- AUTO-S10 recognized `sales_ops_dependency` when appointment capacity was full and response time was worsening, but selected `STOP` rather than only `HOLD`/`ITERATE`. Stopping additional acquisition pressure is valid under exhausted operating capacity; `SCALE` remains forbidden.

The action sets were repaired to admit these defensible operating responses while retaining the actual constructs: AUTO-S6 still requires `sales_ops_dependency` plus `fault_tree_used` and forbids `STOP`/`SCALE`; AUTO-S10 still requires `sales_ops_dependency` and forbids `SCALE`. Deterministic assertions now freeze those semantics.

No behavior-relevant specialization rule, parent-core content, critical fixture, critical expectation, model, or runtime changed. Therefore the **15/15 critical reliability evidence from run 31952941002 remains the qualifying critical evidence**. A final complete AUTO-S1..AUTO-S10 one-trial run is required after this action-contract repair; repeating the critical trials would provide no affected evidence and would waste quota.
