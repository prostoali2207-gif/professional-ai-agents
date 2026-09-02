# Gemini Interactions long-running transport decision — 2026-09-02

Issue: #253
Parent governance: issue #129, `architect/methodology/qualification-stop-loss.md`

## Observed incident

Visual Design / Art Direction #158 canonical continuation run `33611906609` passed static/checkpoint gates, then failed at the candidate executor boundary with `The read operation timed out` before any new candidate/judge output was obtained.

Public-safe incident facts:
- continuation candidate calls recorded as `0`;
- continuation Gemini judge calls `0`;
- continuation Groq judge calls `0`;
- previously completed public-development checkpoint R30–R33 remained 4/4 PASS by both development judges;
- the stopped execution chain remains `NOT_EXECUTABLE / STOP` and is not reopened by this infrastructure work.

## Mechanism

The Visual public-development executor used Gemini Interactions synchronously:
- model `gemini-3.7-flash`;
- `thinking_level=medium`;
- direct `urllib.request.urlopen(..., timeout=180)`;
- outer subprocess timeout `240` seconds.

The provider read timeout therefore fires before the outer process budget. The timeout-only repair in PR #249 allowed a single repeat, but that repeat used the same synchronous mechanism and timed out again.

Repository search also found the same direct synchronous Gemini Interactions pattern in evaluator code for Conversion Messaging, Social Content Creative, Growth Strategy / Experiment Portfolio, and Visual authoring/calibration paths. This does not prove each path has failed identically, but it establishes duplicated exposure to the same transport mechanism.

## External evidence

Checked 2026-09-02 against current Google documentation:

1. Background execution — https://ai.google.dev/gemini-api/docs/background-execution
   - ordinary HTTP requests can be interrupted by connection timeouts;
   - background execution is intended for long-running and long-reasoning work;
   - `gemini-3.7-flash` supports background execution;
   - create returns an interaction ID and completion can be polled.
2. Interactions API reference — https://ai.google.dev/api/interactions-api-v1
   - POST `/v1beta/interactions` supports `background` and `store`;
   - interaction state is retrievable by ID.
3. Interactions overview — https://ai.google.dev/gemini-api/docs/interactions-overview
   - Interaction objects are stored by default for state/background features;
   - callers can opt out with `store=false` for non-background/stateless cases;
   - retention differs by tier, so storage compatibility is a material routing constraint.

## Alternatives considered

### A. Increase synchronous timeout
Rejected as the primary fix. It extends waiting but retains the connection-lifetime failure mode identified by the provider documentation.

### B. Add more blind retries
Rejected. An ambiguous create timeout can occur after the server accepted the model call, so blind POST retries can duplicate spend/execution. PR #249 also demonstrated that repeating the same transport does not remove the mechanism.

### C. Streaming only
Potentially useful for incremental output, but a long-lived stream can still disconnect. Background execution provides a stable interaction ID that can be polled/reconnected and is the provider-documented mechanism for long reasoning.

### D. Background interaction + polling
Adopted for eligible long-running Gemini evaluation calls. Create is single-submit; polling uses bounded idempotent GETs.

## Storage/privacy trade-off

Background execution depends on retrievable server-side Interaction state. Therefore the reusable helper requires explicit `store=true` rather than silently changing a caller from `store=false`.

Consequences:
- public/development fixtures may use background transport only after explicit retention/storage acceptance;
- hidden/sealed material is not automatically eligible;
- if the secrecy/privacy contract forbids provider storage, use another eligible transport or return `NOT_EXECUTABLE`.

## Closure

Implemented reusable primitive:
`architect/evaluation/qualification-platform/gemini_background_transport.py`

Deterministic zero-provider regressions cover:
- single create -> polling -> completed;
- transient polling timeout without duplicate POST;
- ambiguous create timeout with no automatic retry;
- terminal non-completed statuses fail closed;
- bounded overall deadline;
- explicit storage opt-in;
- non-transient polling failure without retry.

No Visual #158 candidate, fixture, judge, threshold or stopped continuation runner is modified. No model/provider call is authorized by this change.

After these regressions pass, issue #253 is complete and generic/provider infrastructure returns to maintenance mode. A future Visual execution must be separately authorized under the current stop-loss policy; this document is not permission to resume R34/R39 in the stopped chain.