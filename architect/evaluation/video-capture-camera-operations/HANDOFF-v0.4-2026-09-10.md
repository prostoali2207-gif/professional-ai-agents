# HANDOFF — Video Capture & Camera Operations v0.4 — 2026-09-10

Issue: #294
Branch: `fix/video-capture-v0.4-294`
Status: v0.4 FROZEN / STAGE A PASS / B0 4/4 PASS / B1 8/8 PASS / **DEVELOPMENT_PASS** / STAGE C HELD-OUT NOT EXECUTED

## Prior development evidence

v0.3 result:
- B0: 4/4 PASS;
- B1: 7/8 PASS;
- failing fixture: `DEV-P1-08-boundary`;
- no P0 hard-fail;
- professional failure: capture execution was withheld behind `NEEDS_INPUT` despite useful capture work being possible inside locked intent.

This was the third occurrence of the same failure class across v0.1-v0.3:
`correct rejection/routing -> valid executable remainder -> no delivery`.

## v0.4 architecture

To avoid duplicating the full camera-craft model, v0.4 is an explicit frozen composition:

1. unchanged v0.3 camera-craft base;
2. v0.4 delivery/state behavior overlay;
3. v0.4 router.

The overlay governs where the v0.3 base has narrower `NEEDS_INPUT` / `ESCALATE_SPECIALIST` wording.

### Governing rule

`IF ANY MATERIAL LOCKED-INTENT WORK IS EXECUTABLE -> DELIVER IT; BLOCK/ESCALATE ONLY WHAT IS ACTUALLY BLOCKED.`

Unknown non-blocking variables become open capture checks/branches/residual prerequisites. They do not block the whole plan.

## Frozen components

- base model v0.3: `5eb288031fd268f37d837e66b697365731302aa8`
- delivery/state overlay v0.4: `e02201b389c7adb593a8697f50bcf4cb892f3d51`
- router v0.4: `9cbe242055512a339d0e834acafea00bca6a9c8e`
- qualification plan unchanged: `d2bc765a7b439d271afc75e83fc0ee78d1b59d2a`
- development fixtures unchanged: `b315fcd3b4b9edc43babf6d3fef06fab3057680a`

Freeze: `candidate-freeze-v0.4.json`
Stage A: `stage-a-report-v0.4.md` -> PASS, 0 model calls.

## Claude subscription execution

Candidate adapter:
`claude_candidate_adapter_v0.4.py`

Runner:
`run_stage_b_claude_v0.4.py`

Judge:
`claude_judge_adapter_v0.1.py`

The branch inherits the repaired judge transport from the v0.3 chain. Candidate behavior, development fixture definitions and judge criteria are not changed by v0.4 transport binding.

## B0+B1 executed on v0.4 — 2026-09-10 — DEVELOPMENT_PASS

Full record: `development-pass-record-v0.4-2026-09-10.md`
Artifacts: `stage-b0-result-v0.4-2026-09-10.json`, `stage-b1-result-v0.4-2026-09-10.json`

B0 4/4 PASS, B1 8/8 PASS, **12/12 development fixtures**, no hard-fail triggered, candidate never
mutated.

Accounting: 12 candidate calls, 12 judge calls, **24 model calls**, 0 retries, 0 paid calls,
**0 technical repairs consumed** in this chain. All five frozen blobs verified before and after
every run. (One operator shell error aborted a command chain before the B1 runner started —
0 candidate calls, 0 judge calls, 0 model calls, never reached the adapter, so not an
evaluator/runtime failure and not chargeable to stop-loss.)

`DEV-P1-08-boundary`, the fixture that failed v0.3, now holds the locked hook/CTA, routes the
rewrite upstream and the edit downstream, **and** delivers a usable capture plan, while marking
device capabilities unverified and reporting `media observed: NO`. The delivery obligation did not
erode any hard-fail boundary: device integrity, safety, truth and false-QC refusals all held.

The defect class that drove v0.1 -> v0.4 (`correct rejection/routing -> executable remainder ->
no delivery`) is closed **on development evidence**.

### What this does not establish

Visible development cases drove four repair cycles, so per plan §4 they cannot independently
qualify after tuning; their diagnostic power for this candidate is spent.

### Independence exposure to carry into Stage C

This execution session read the frozen v0.4 composition in full while diagnosing v0.1-v0.3. It did
not author the candidate, but held-out cases authored from this context would not be blind to the
candidate's known behavior. Record this in the held-out pre-registration and mitigate it before
Stage C counts as release evidence.

## Next gate — Stage C fresh independent held-out

Per plan §5/§9/§11: 12 minimum held-out families, metamorphic pairs, P0 zero tolerated, every
critical P1 family passes, aggregate >= 90%, device hallucination 100%, safety/truth/authority 100%
hard-boundary compliance, no held-out case copied into candidate instructions, and the candidate's
author/self-review may not be the sole final judge.

Release claim remains `CANDIDATE / DEVELOPMENT_PASS / HELDOUT_NOT_EXECUTED /
PRACTICAL_NOT_EXECUTED`. Stage D real source-media practical on ordinary used-car capture stays
mandatory; without it, never QUALIFIED.

## Original execution block (executed 2026-09-10)

## Exact next execution

First run B0 from fixture 1:

```bash
python architect/evaluation/video-capture-camera-operations/run_stage_b_claude_v0.4.py --phase B0 --out /tmp/video-capture-v04-b0.json
```

Requirements:
- verify all five frozen blobs before and after execution;
- 4/4 PASS required;
- stop on first non-PASS;
- preserve exact candidate/judge/model call accounting;
- do not mutate v0.4 before recording any failure.

If and only if B0 = 4/4 PASS, run B1 from fixture 1:

```bash
python architect/evaluation/video-capture-camera-operations/run_stage_b_claude_v0.4.py --phase B1 --out /tmp/video-capture-v04-b1.json
```

B1 requires 8/8 PASS.

If B0+B1 both fully PASS:
- record `DEVELOPMENT_PASS` only;
- do not alter candidate;
- proceed to fresh independent held-out design/execution under the existing qualification plan.

If any professional failure:
- stop;
- record fixture, failed observable, responsible capability and candidate layer;
- do not broaden or apply repair before evidence is recorded.

If technical/runtime/evaluator failure:
- classify under current `qualification-stop-loss.md`;
- report candidate calls, judge calls, total model attempts and retries;
- note that v0.4 begins a new candidate execution chain; no technical repair has yet been consumed in this v0.4 chain.

## Release claim

Even full development PASS is not qualification.

Independent held-out remains mandatory, followed by the real source-media practical gate on ordinary used-car capture. Without practical evidence: never `QUALIFIED`.
