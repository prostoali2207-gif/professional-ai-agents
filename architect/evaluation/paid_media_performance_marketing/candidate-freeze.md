# Paid Media Professional Core — Candidate Freeze

Release candidate: 1.0.0

Behavior-relevant professional-core artifact digest: `sha256:8eb6469b1f04aa836549f70ab50544b7dc97a5b43fa68c93ede5f4e2bf6a8235`.

Frozen behavioral fixtures: PM-S1 through PM-S13.

Frozen critical reliability subset: PM-S1, PM-S2, PM-S3, PM-S11, PM-S13.

Frozen thresholds: 3/3 independent PASS per critical fixture, then 13/13 PASS across the complete suite, with zero application retries. Infrastructure failures are BLOCKED, not behavioral failures. Any behavioral miss requires REVISE rather than rerun-until-green.

Qualification runtime: `gemini-3.1-flash-lite`, thinking level `medium`; complete-suite structured requests are bounded to five fixtures per request due the previously observed oversized-schema API rejection.

No Automotive, UAE, Meta-only, dealership, or Toyota specialization is in scope for this candidate.