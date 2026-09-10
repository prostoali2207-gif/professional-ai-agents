# HANDOFF — Video Capture & Camera Operations v0.4 — 2026-09-10

Issue: #294
Branch: `fix/video-capture-v0.4-294`
Status: v0.4 FROZEN / STAGE A PASS / B0+B1 NOT YET EXECUTED ON v0.4

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
