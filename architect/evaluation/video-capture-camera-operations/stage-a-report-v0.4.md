# Video Capture & Camera Operations — v0.4 Stage A / repair freeze

Status: **PASS / ZERO-MODEL**
Issue: #294
Candidate: `video-capture-camera-operations-v0.4`

## Why v0.4 exists

v0.3 passed all 4 P0 development fixtures and 7 of 8 P1 fixtures. `DEV-P1-08-boundary` exposed the third instance of the same failure class seen in v0.1/v0.2:

`correct refusal/routing -> executable capture work still exists -> no delivery`.

The candidate correctly preserved the locked hook/CTA and routed creative rewrite/editing to their owners, but then returned `NEEDS_INPUT` and withheld all capture execution because exact device/location/operator details were absent.

## v0.4 repair

The camera-craft base remains frozen at v0.3. v0.4 adds one governing behavior overlay:

`IF ANY MATERIAL LOCKED-INTENT WORK IS EXECUTABLE -> DELIVER IT; BLOCK/ESCALATE ONLY WHAT IS ACTUALLY BLOCKED.`

Unknown non-blocking capture variables remain explicit inside the plan as on-location checks, bounded branches, or residual prerequisites. They do not suppress the whole plan.

The rule governs both `NEEDS_INPUT` and `ESCALATE_SPECIALIST` and does not expand authority or lower safety/truth/QC requirements.

## Frozen identity

- v0.3 camera-craft base: `5eb288031fd268f37d837e66b697365731302aa8`
- v0.4 delivery/state overlay: `e02201b389c7adb593a8697f50bcf4cb892f3d51`
- v0.4 router: `9cbe242055512a339d0e834acafea00bca6a9c8e`
- qualification plan unchanged: `d2bc765a7b439d271afc75e83fc0ee78d1b59d2a`
- development fixtures unchanged: `b315fcd3b4b9edc43babf6d3fef06fab3057680a`

## Static result

PASS:
- candidate remains NOT QUALIFIED;
- base camera craft is unchanged;
- development tests and thresholds are unchanged;
- `NEEDS_INPUT` cannot suppress executable work merely because non-blocking variables are unknown;
- `ESCALATE_SPECIALIST` remains residual/minimal when in-scope work is executable;
- device capabilities still may not be invented;
- unsafe capture remains forbidden;
- truth/disclosure remains mandatory;
- source-ready state still requires actual media observation;
- real source-media practical gate remains mandatory.

Provider/model calls: 0.
Paid API calls: 0.
Retries: 0.

## Next gate

Rerun B0 from fixture 1 using v0.4. No v0.3 PASS is inherited across candidate identity change. Full B0 PASS is required before B1; full B1 PASS is required before fresh independent held-out.
