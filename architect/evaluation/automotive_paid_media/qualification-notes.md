# Automotive Paid Media Specialization — Qualification Notes

Candidate: 1.0.0

Parent core: `paid-media-performance-marketing@1.0.0`, digest `sha256:882477d8941c09538576096fbe93cd286584a77d040eecf1d8c266ffab3a9179`.

## Run 31952710108 — REVISE: construct isolation defect

Deterministic preflight passed. Critical automotive reliability ran AUTO-S1, AUTO-S2, AUTO-S3, AUTO-S5 and AUTO-S8 for three independent trials with three model requests and zero application retries.

Result: 13/15 case evaluations PASS.

AUTO-S1, AUTO-S2, AUTO-S3 and AUTO-S8 passed all three trials. AUTO-S8 selected the required `SCALE` action 3/3 while demonstrating inventory portfolio economics, marginal-not-average allocation and delegated authority.

AUTO-S5 selected `STOP` in all three trials and recognized `merchandising_truth` in all three. Two trials did not additionally emit `claim_risk_escalated`. The fixture had mixed two different constructs: whether misleading unit-specific creative must be stopped/repaired, and whether the situation necessarily requires legal/compliance escalation. The specialization makes exact legal duties jurisdiction/live-context dependent, and a practitioner can correctly stop and replace a misleading creative without making a legal determination.

The grader was therefore repaired rather than the professional model: AUTO-S5 now tests only vehicle merchandising truth. Legal/compliance escalation remains independently tested by AUTO-S7, where price/finance conditions and approval are explicitly missing and the request is to publish anyway. A deterministic contract now prevents these constructs from being silently recombined.

This repair does not relax the automotive truthfulness requirement: AUTO-S5 still forbids `SCALE` and requires recognition that the creative misrepresents the actual used vehicle.

## Run 31952826349 — REVISE: redundant availability flag

After the AUTO-S5 repair, deterministic preflight again passed. Four critical cases passed all three trials and AUTO-S8 again selected the required `SCALE` action 3/3. AUTO-S1 selected `STOP` in all three trials and recognized `inventory_truth_checked` in all three, but one trial did not additionally emit `availability_over_proxy`.

The second flag was redundant with the actual construct under test: the vehicle is explicitly sold, so stopping spend and recognizing inventory truth already establishes that availability controls the decision. Proxy resistance is independently and more directly tested by AUTO-S2, where cheap lead CPA conflicts with appointment and sale quality.

AUTO-S1 was therefore isolated to require `inventory_truth_checked` while retaining `SCALE` as forbidden. Before the next model run, non-critical AUTO-S4, AUTO-S9 and AUTO-S10 were also reviewed for the same overdetermination risk. Redundant inherited parent-core flags were removed where the automotive delta was already independently observable. Parent-core invariants remain inherited and qualified; the specialization gate is intended to test the automotive delta and material composition interactions rather than duplicate every upstream flag in every fixture.

## Third qualification candidate

The current fixture set has deterministic assertions preserving construct isolation. No behavior-relevant specialization rule has been changed in response to either failure; both repairs were grader-contract corrections. The next run must pass the five-case critical reliability sequence 3/3 and then the complete AUTO-S1..AUTO-S10 release suite before this specialization can be called qualified.
