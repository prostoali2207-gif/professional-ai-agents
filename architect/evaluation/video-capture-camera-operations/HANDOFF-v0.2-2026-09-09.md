# HANDOFF — Video Capture & Camera Operations v0.2 — 2026-09-09

Issue: #294
Branch: `fix/video-capture-v0.2-294`
Status: v0.2 FROZEN / STAGE A PASS / B0 NOT YET EXECUTED ON v0.2

## Prior evidence

v0.1 B0:
- `DEV-P0-01-device-capability` -> P1_FAIL;
- candidate correctly rejected unsupported ProRes Log / 4K60;
- candidate incorrectly stalled in NEEDS_INPUT despite supplied verified 4K30 alternative;
- responsible: DV-01, consequential OP-01;
- v0.1 remains immutable.

## v0.2 targeted repair

Only escalation-vs-delivery behavior changed:

`unsupported/unverified requested capability + VERIFIED sufficient alternative -> substitute verified alternative + continue to executable plan`.

`NEEDS_INPUT` is now reserved for decision-critical missing information when no verified sufficient alternative resolves the locked intent.

No intentional change to:
- truth/disclosure;
- safety;
- framing/perspective;
- exposure/focus;
- movement/stabilization;
- audio;
- coverage;
- source QC;
- Creator/Post authority boundaries.

## Frozen v0.2

- professional model:
  `architect/evaluation/video-capture-camera-operations/professional-model-candidate-v0.2.md`
  blob `9ec8dd41b1ec25cb01001cbb9604b950b1b2f8c8`

- router:
  `architect/evaluation/video-capture-camera-operations/candidate-v0.2/SKILL.md`
  blob `6a4ee9e56bc52f0742153fa5169a10b19d22ba40`

- qualification plan unchanged:
  blob `d2bc765a7b439d271afc75e83fc0ee78d1b59d2a`

- development fixtures unchanged:
  blob `b315fcd3b4b9edc43babf6d3fef06fab3057680a`

Freeze:
`candidate-freeze-v0.2.json`

Stage A:
`stage-a-report-v0.2.md` -> PASS, zero model/provider calls.

## Claude Code transport

Use repaired subscription transport inherited from prior execution chain:
- safe-mode;
- OAuth/subscription auth;
- no metered API keys;
- no CLAUDE.md / skills / MCP / tools / repo visibility for child candidate/judge;
- candidate Sonnet;
- judge Opus.

v0.2 adapter:
`claude_candidate_adapter_v0.2.py`

v0.2 runner:
`run_stage_b_claude_v0.2.py`

Judge remains:
`claude_judge_adapter_v0.1.py`

## Exact execution

First:

```bash
python architect/evaluation/video-capture-camera-operations/run_stage_b_claude_v0.2.py --phase B0 --out /tmp/video-capture-v02-b0.json
```

Rules:
- start from fixture 1;
- do not inherit v0.1 result;
- stop on first non-PASS;
- do not mutate v0.2 before recording the professional/runtime failure;
- preserve candidate/judge call accounting.

If and only if B0 is full PASS (4/4), run:

```bash
python architect/evaluation/video-capture-camera-operations/run_stage_b_claude_v0.2.py --phase B1 --out /tmp/video-capture-v02-b1.json
```

If B1 full PASS:
- record DEVELOPMENT_PASS only;
- do not claim QUALIFIED;
- next stage is fresh independent held-out;
- after held-out, mandatory real source-media practical gate remains.

If any professional failure:
- identify exact fixture, observable, responsible capability and candidate layer;
- stop;
- do not broaden repair.

If technical/runtime failure:
- report classification, candidate calls, judge calls, retries and whether any model call occurred;
- apply current qualification-stop-loss.md.
