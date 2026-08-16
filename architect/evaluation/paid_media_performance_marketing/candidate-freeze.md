# Paid Media Professional Core — Candidate Freeze

Release candidate: 1.0.0

Behavior-relevant professional-core artifact digest: `sha256:882477d8941c09538576096fbe93cd286584a77d040eecf1d8c266ffab3a9179`.

Frozen behavioral fixtures: PM-S1 through PM-S13.

Frozen critical reliability subset: PM-S1, PM-S2, PM-S3, PM-S11, PM-S13.

Frozen thresholds: 3/3 independent PASS per critical fixture, then 13/13 PASS across the complete suite, with zero application retries. Infrastructure failures are BLOCKED, not behavioral failures. Any behavioral miss requires REVISE rather than rerun-until-green.

Qualification runtime: `gemini-3.1-flash-lite`, thinking level `medium`; complete-suite structured requests are bounded to five fixtures per request due the previously observed oversized-schema API rejection.

The professional model now requires an explicit delegated-authority check before any spend-increasing execution decision; this is a behavior repair after a prior PM-S13 reliability miss, not a grader relaxation.

No Automotive, UAE, Meta-only, dealership, or Toyota specialization is in scope for this candidate.