# Video Capture Stage B — pre-run gate v0.1

Status: READY_FOR_EXECUTION / NOT YET EXECUTED

## Candidate
- id: video-capture-camera-operations-v0.1
- model blob: 65ccc214418d269a27042dda2b83adf53bb59c5b
- skill blob: 8b64d280b8b1fe01969bf804212ab0e6ca37a7a8
- qualification plan blob: d2bc765a7b439d271afc75e83fc0ee78d1b59d2a

## Execution chain
`candidate v0.1 + Stage B development semantic + evaluator/transport TBD`

No technical repair has been consumed because no Stage B model execution has occurred.

## Smallest discriminating route

Phase B0:
- execute only DEV-P0-01 through DEV-P0-04;
- candidate calls: max 4;
- judge calls: max 4 if an external calibrated judge is used;
- stop immediately on any P0 failure.

Phase B1 only if B0 passes:
- execute the 8 P1 development fixtures;
- candidate calls: max 8;
- judge calls: max 8 if required.

No paid/provider calls are authorized merely to discover a configuration defect that a deterministic preflight could detect.

## Eligibility

The executor must be able to load the exact frozen candidate components and case context without silently substituting a different prompt/core.

A judge must not be the sole self-review that authored the candidate if its result is being treated as evaluation evidence.

If no eligible executor/judge path is available, return NOT_EXECUTED / RUNTIME_UNAVAILABLE rather than weakening independence or building generic qualification infrastructure.

## Stop condition

- P0 semantic failure -> stop and classify PROFESSIONAL_FAIL;
- evaluator defect -> EVALUATOR_CONSTRUCT_FAIL;
- provider/runtime failure -> classify under qualification-stop-loss;
- local runner failure -> at most the bounded repair allowed for this execution chain;
- do not proceed to independent held-out/practical qualification based only on self-review.
