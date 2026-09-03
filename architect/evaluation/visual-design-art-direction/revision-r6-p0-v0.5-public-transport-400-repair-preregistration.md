# Visual Design / Art Direction v0.5 public-development transport repair — polling HTTP 400

Date: 2026-09-03
Issue: #256
Canonical failed run: `33728944822`
Status: preregistered before repair implementation and before any retry/provider execution

## Failure classification

This is the first technical failure in the NEW v0.5 structural-controller PUBLIC development execution chain.

Canonical evidence:
- run `33728944822` on merge `77667bac0af975308f8279df38428c935362cd6b`;
- zero-provider preflight PASS;
- credentials PASS;
- progress artifact id `9883077747`, digest `sha256:37b9700c3b5820117e941ba76f845b5610337fbffed388a9d62e2094bf76bb3f`;
- public details artifact id `9883078348`, digest `sha256:c3ede3c79dcb1dc972a95761eda1ecdca8bcd5d3c25049120977b709167d2792`;
- candidate completed case calls: `0`;
- candidate completed model passes: `0`;
- Gemini judge calls: `0`;
- Groq judge calls: `0`;
- terminal status: `INFRASTRUCTURE_FAILURE`;
- exact boundary error: background Interaction creation returned an `in_progress` interaction id, then retrieval failed `POLL_TRANSPORT_FAILED: HTTP 400 ... {"code":"invalid_request","message":"Request contains an invalid argument."}`.

Classification: `LOCAL_EXECUTION_FAIL` at the public-development provider transport adapter. There is no professional evidence from this run and therefore no professional PASS/FAIL inference.

## Evidence for repair scope

Current Google background-execution documentation still specifies the same retrieval mechanism used by the adapter:
`GET /v1beta/interactions/{interaction_id}` with the API key and `Api-Revision: 2026-05-20`.

The generic background helper introduced in #253 was verified with deterministic mocked HTTP regressions only; #253 explicitly authorized no provider/model calls. Therefore the first live use exposed a retrieval-boundary behavior that those mocks could not establish.

The repair must not change the documented GET shape merely to guess around the provider. Instead it may recover only an already-created interaction when the provider returns the exact generic post-create `400 invalid_request` with no parameter-specific diagnostic. Recovery is idempotent GET-only and bounded; the creation POST is never repeated.

## Bounded repair

Add a v0.5-local retrieval recovery path around the existing background helper:

1. normal background helper remains the first path;
2. recovery is eligible only when all are true:
   - helper error code is `POLL_TRANSPORT_FAILED`;
   - a concrete `interaction_id` is present;
   - provider response is HTTP 400;
   - response contains code `invalid_request` and the generic message `Request contains an invalid argument.`;
3. recovery performs only official-shape GETs against that same existing interaction id;
4. no POST/model creation retry is allowed;
5. poll interval: 10 seconds;
6. maximum recovery grace window: 60 seconds, additionally bounded by the candidate-pass overall deadline;
7. 408/429/5xx/network timeout during recovery remain bounded transient GET failures;
8. parameter-specific 400, 401, 403, 404, or any other non-transient response fails closed immediately;
9. completed returns the interaction; in_progress continues; all other terminal states fail closed.

This is a transport repair only. Candidate professional components, structural-controller semantics/schema, fixtures, judges, thresholds and strict 6/6 public development gate remain unchanged.

## Regression requirement

Before provider retry, deterministic zero-provider regression must prove:
- exact generic 400 after a successful created interaction can recover by GET-only polling;
- recovery performs zero POSTs;
- a parameter-specific 400 is not retried;
- recovery grace is bounded/fails closed;
- exact v0.3 professional blob identity and v0.5 controller contract remain unchanged.

## Stop-loss budget

This repair consumes the single bounded technical-repair allowance for the v0.5 public-development execution chain.

After regression + merge, exactly one eligible retry may be executed.

If that retry encounters another non-professional technical defect in this same chain, the chain is terminal `NOT_EXECUTABLE / STOP`; no second repair is authorized.

If the retry produces a professional fixture FAIL, do not rerun for a better outcome.

If the retry produces strict 6/6 public PASS, proceed to candidate freeze and a fresh independent held-out release cycle; public evidence remains non-release evidence.
