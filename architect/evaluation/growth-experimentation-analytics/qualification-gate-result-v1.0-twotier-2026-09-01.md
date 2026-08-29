# Analytics v1.0 two-tier held-out gate — result record

Recorded: 2026-08-29
Gate id: `analytics-v1.0-twotier-heldout-2026-09-01`
Preregistration: `preregistration-v1.0-twotier-2026-09-01.json`
Candidate: `growth-experimentation-measurement-v1.0-consolidated`
Candidate digest: `sha256:3f4f3e133e81b00a1536fc6c72f1f59c24ef9f7b4c50c762c3c6c5bf6c4dd63d`
Provider/model: Gemini / `gemini-3.5-flash-lite`
Run: `33264418604`
Job: `99131840075`
Artifact: `9718747815` (`analytics-v1-0-twotier-gemini`)
Commit executed: `68f7da48abc04094abd891dd65f9182a58d7d854`

## Observed verdict

**PASS** under the preregistered two-tier stability criterion.

Observed ledger:

- total trials: 70
- Tier 1 professional-judgment failures: 0
- Tier 2 contract-invalid outputs: 6/70
- maximum Tier 2 count on any fixture: 1/7
- INVALID apparatus failures: 0
- retries: 0
- best-of-N: no

The runner emitted:

`GATE VERDICT: PASS`

`REASON: no tier-1 failure; tier-2 within both caps`

All 10 held-out fixtures retained at least 6 judgment-gradable passes out of 7; the preregistered minimum implied by the Tier 2 cap was 5.

## Integrity observations

Before candidate execution, deterministic checks passed and the run verified the frozen candidate, output contract, generator, grader, classifier and two-tier runner. The run used preregistered seed `20260901` and the frozen tier-map digest `sha256:11f18a82f63493528d281adc69ac3cf50325fd084ebc40b9d96e04f2054f40e4`.

No provider/apparatus failure occurred, so the gate was valid rather than INVALID.

The six Tier 2 events were structural output failures only: malformed JSON or frozen-schema violations. They were not counted as judgment passes and did not exceed either preregistered cap.

## Qualification boundary

This record does **not** promote or unquarantine `growth-experimentation-measurement@1.1.0` by itself.

The preregistration explicitly states that a PASS on this gate is fresh held-out evidence on one model family, not a full reusable-core release qualification. It also records that library admission still requires an externally authored held-out set and the cross-model release protocol.

Accordingly, the current evidence supports:

- consolidated Analytics candidate v1.0: **two-tier held-out gate PASS**;
- professional judgment on this gate: **0 Tier 1 failures in 70 trials**;
- reusable library lifecycle: **unchanged pending the remaining release requirements**.

Do not retroactively reinterpret older failed or quarantined qualification records from this result. Do not alter the frozen candidate, grader, generator, contracts, tier map, thresholds or this gate's ledger after the result.
