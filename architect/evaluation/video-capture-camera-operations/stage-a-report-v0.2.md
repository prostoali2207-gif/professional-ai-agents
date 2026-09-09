# Video Capture & Camera Operations — v0.2 Stage A / repair freeze

Status: PASS / ZERO-MODEL
Issue: #294
Candidate: video-capture-camera-operations-v0.2

## Why v0.2 exists

v0.1 failed `DEV-P0-01-device-capability` with a valid professional P1 failure:
it correctly rejected unsupported ProRes Log / 4K60, but stalled in `NEEDS_INPUT` despite a verified sufficient 4K30 alternative.

## Targeted repair

Only the responsible escalation-versus-delivery rule changed:
- unsupported/unverified requested capability + verified sufficient alternative that satisfies locked intent => substitute and continue;
- `MISSING/BLOCKING` / `NEEDS_INPUT` only when a decision-critical unknown remains and no verified sufficient alternative resolves it.

The v0.2 router binds to this repaired professional model and repeats the same invariant.

## Frozen identity

- professional model: `9ec8dd41b1ec25cb01001cbb9604b950b1b2f8c8`
- router: `6a4ee9e56bc52f0742153fa5169a10b19d22ba40`
- qualification plan unchanged: `d2bc765a7b439d271afc75e83fc0ee78d1b59d2a`
- development fixtures unchanged: `b315fcd3b4b9edc43babf6d3fef06fab3057680a`

## Static result

PASS:
- candidate remains NOT QUALIFIED;
- unsupported capability is still forbidden from being invented;
- verified fallback substitution is now explicit;
- truth, safety, source-QC, Creator/Post boundaries remain present;
- practical release gate remains unchanged.

Provider/model calls: 0.
Paid API calls: 0.
Retries: 0.

## Next action

Rerun B0 from `DEV-P0-01` against v0.2. No prior v0.1 professional result is inherited for this fixture.
