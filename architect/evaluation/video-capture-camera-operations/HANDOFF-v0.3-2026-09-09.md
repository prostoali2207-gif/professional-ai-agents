# HANDOFF — Video Capture & Camera Operations v0.3 — 2026-09-09

Issue: #294
Branch: `fix/video-capture-v0.3-294`
Status: v0.3 FROZEN / STAGE A PASS / B0 NOT YET EXECUTED ON v0.3

## Why v0.3 exists

v0.1 and v0.2 independently exposed the same failure class:

`correct rejection -> correct alternative -> no delivery`.

v0.3 generalizes the repair rather than adding another domain-specific exception.

## Frozen v0.3

- model: `professional-model-candidate-v0.3.md`
  blob `5eb288031fd268f37d837e66b697365731302aa8`
- router: `candidate-v0.3/SKILL.md`
  blob `0c24a630146dba2ce934c6d7371cc8e82ff11d43`
- qualification plan unchanged:
  `d2bc765a7b439d271afc75e83fc0ee78d1b59d2a`
- development fixtures unchanged:
  `b315fcd3b4b9edc43babf6d3fef06fab3057680a`

Freeze: `candidate-freeze-v0.3.json`
Stage A: `stage-a-report-v0.3.md` -> PASS, zero model calls.

## Repair rule

Across any domain:
1. reject unsafe/unsupported/unverified/out-of-scope requested path;
2. identify a safe, truthful, in-competence alternative preserving locked intent;
3. if one exists, deliver executable plan/instructions for it;
4. isolate external specialist/authority needs as residual prerequisites;
5. escalate the whole task only if the residual blocks every safe truthful route.

Safety authority is not expanded.

## Execution

Use repaired Claude subscription transport.

Candidate adapter:
`claude_candidate_adapter_v0.3.py`

Runner:
`run_stage_b_claude_v0.3.py`

Judge:
`claude_judge_adapter_v0.1.py`

Run:

```bash
python architect/evaluation/video-capture-camera-operations/run_stage_b_claude_v0.3.py --phase B0 --out /tmp/video-capture-v03-b0.json
```

Requirements:
- start from fixture 1;
- full B0 requires 4/4 PASS;
- stop on first non-PASS;
- preserve exact candidate/judge call accounting;
- do not mutate v0.3 before recording any failure.

If full B0 PASS:

```bash
python architect/evaluation/video-capture-camera-operations/run_stage_b_claude_v0.3.py --phase B1 --out /tmp/video-capture-v03-b1.json
```

Only full B1 PASS permits moving to fresh independent held-out.

Do not claim QUALIFIED after development PASS. Real source-media practical remains mandatory.
