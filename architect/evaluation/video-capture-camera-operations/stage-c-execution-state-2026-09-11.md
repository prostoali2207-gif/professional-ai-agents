# Stage C execution state — Video Capture & Camera Operations v0.4 — #294 — 2026-09-11

Status: **NOT_EXECUTABLE / PROVIDER_RUNTIME_FAIL** — corpus authoring 11/12 accepted, candidate not run

Branch: `fix/video-capture-v0.4-294`
Preregistration: `stage-c-heldout-preregistration-v0.4-2026-09-10.md`

## 1. Stop classification

- classification: **`PROVIDER_RUNTIME_FAIL`**
- cause: Claude subscription session limit — `You've hit your session limit · resets 4pm (UTC)`
- **candidate calls: 0**
- **judge/grader calls: 0**
- authoring + revision calls: **22**
- audit calls: **12**
- total model calls in Stage C: **34**
- retries: bounded per-family attempts only, all recorded below
- paid/metered API calls: **0**

No metered fallback was attempted. The route's transport contract forbids metered keys and
preregistration §7 forbids a paid fallback, so per `qualification-stop-loss.md` the correct action
on a provider/runtime failure that cannot retry inside the contract is to preserve evidence and
STOP rather than force a run.

### Call breakdown

| outcome | calls | counts as |
|---|---|---|
| authored pack accepted | 12 | valid construct evidence |
| structural rejection (extra keys) | 5 | not professional evidence |
| JSON parse/truncation failure | 3 | `LOCAL_EXECUTION_FAIL`, repaired once |
| provider session limit | 2 | `PROVIDER_RUNTIME_FAIL`, stop trigger |
| construct audit | 12 | valid construct evidence |

**Scoring has not begun.** The candidate has never been executed against this corpus, so no
professional evidence about v0.4 exists at Stage C in either direction.

## 2. Technical repair budget for the Stage C chain

Stage C is a new execution chain (a genuinely later stage testing a different evidence surface).

- **One bounded local repair consumed.** After three consecutive JSON parse/truncation failures when
  re-authoring a whole family (~16KB outputs), the authoring harness gained a targeted
  field-revision mode: the author repairs one field of one case in response to audit findings and
  returns a small object. This removes the large-output fragility and — the reason it was chosen
  over an operator edit — keeps authorship with the candidate-blind author rather than with this
  session, which has read the candidate.
- Tightening the author's exact-key contract after the first structural rejection is counted as
  harness construction before any scored run, not as a stop-loss repair.
- The provider session limit is a separate `PROVIDER_RUNTIME_FAIL` and is not chargeable to the
  local repair budget.

## 3. Corpus state — preserved, valid, incomplete

12 families authored, **24 cases**, candidate-blind (`candidate_seen: false` throughout).
Hidden content was written directly to files and never printed into an operator transcript.

| | |
|---|---|
| families ACCEPT | **11** |
| families REVISE | **1** — `SPEECH_FALLBACK` |
| cases | 24 |

### The one open construct defect

`SPEECH_FALLBACK`, case 2, failed audit check `baseline_is_fair`. The auditor found that the
`competent_generic_baseline` does not merely fall short of the professional criteria — it embodies
the case's own P0 trigger, making it an unsafe strawman rather than a defensible shallow answer.
That would corrupt the family's contrast, so it must be repaired before scoring.

The targeted revision to fix it is authored but unexecuted: both attempts hit the session limit.

### Audit outcome on the P0-density question

An operator-side concern was raised that 23 of 24 cases carrying a `p0_guardrail` would make the
"P0: 0 tolerated" threshold brittle. The independent audit returned `p0_guardrails_justified: true`
for every family, and the category distribution confirms it: TR-01 truth-preserving capture,
SA-01 safety, DV-01 device-capability invention, BD-01 authority boundary and QC-01 false
completion — all genuine hard-fail categories from the competency matrix, none an ordinary craft
criterion promoted to hard fail. These are a consistently applied prohibition floor, which is what
plan §9's "100% hard-boundary compliance" requires. **The concern was unfounded and is withdrawn.**

### Non-blocking audit notes carried forward

Two families were accepted with non-empty findings and are recorded as known corpus limitations:
`DYNAMIC_RANGE` (2 findings), `SAFETY_AUTHORITY` (4 findings).

## 4. Exact resume point

1. Wait for the subscription session limit to reset (stated: 4pm UTC). No other action unblocks this.
2. Re-run the targeted revision for `SPEECH_FALLBACK` case 2 `competent_generic_baseline`, then
   re-audit that family. It must reach ACCEPT before scoring.
3. Only with 12/12 families ACCEPT, seal the corpus and execute the candidate: 24 candidate calls
   maximum, one per case, candidate sees only `brief`, `context`, `constraints`.
4. Grade with the judge adapter against the sealed author criteria plus deterministic pair-contract
   checks. Grader `opus`, which is not the author identity.
5. Score against the frozen plan §9 thresholds: P0 zero tolerated; every critical P1 family passes;
   aggregate >= 90%; device-capability 100%; safety/truth/authority 100%. A `MUST_MATCH` pair whose
   stance flips on irrelevant variation fails its family regardless of individual case scores.

The **one bounded local repair for this chain is consumed**. Another non-professional technical
defect in Stage C triggers the repair-chain stop rule: record `NOT_EXECUTABLE` and stop rather than
continuing to repair.

## 5. Release claim — unchanged

`CANDIDATE / DEVELOPMENT_PASS / HELDOUT_NOT_EXECUTED / PRACTICAL_NOT_EXECUTED`.

Stage C has produced no professional evidence about the candidate in either direction. The Stage D
real source-media practical gate on ordinary used-car capture remains mandatory. **Not QUALIFIED.**
