# Stage C — pre-run / stop-loss accounting before FINAL eligible technical retry

Date: 2026-09-13
Issue: #294
Branch: `fix/video-capture-v0.4-294`
Execution chain: **Stage C held-out author / review / seal**
Recorded BEFORE any model call. Model calls made at the time of writing: **0**.

## 1. Mandatory pre-run record (`qualification-stop-loss.md` §"Pre-run enforcement")

| field | value |
|---|---|
| candidate / cycle | `video-capture-camera-operations-v0.4`, frozen, unchanged |
| execution chain | Stage C held-out author/review/seal |
| prior technical repairs in this chain | **1 — consumed** |
| candidate call budget | 0 spent / 24 maximum (scoring not started) |
| judge (grader) call budget | 0 spent / 24 maximum |
| stop condition | another non-professional technical defect -> `NOT_EXECUTABLE`, no further harness repair |

Frozen v0.4 blobs re-verified at the time of writing — all five match:
`5eb28803…`, `e02201b3…`, `9cbe2420…`, `d2bc765a…`, `b315fcd3…`.

## 2. Failure class being resumed from

- **failure class: `LOCAL_EXECUTION_FAIL`**
- cause: malformed / truncated JSON returned by the author when **re-authoring the whole
  `SPEECH_FALLBACK` family**. Three consecutive attempts failed — one malformed at ~4KB, two
  truncated at ~16KB.
- **candidate calls: 0**
- **judge calls: 0**
- the original `SPEECH_FALLBACK` sealed artifact was **never damaged**: the harness writes only
  after successful structural validation. Verified at 16192 bytes, sha256 `06765ffc72a01f39…`.

A separate `PROVIDER_RUNTIME_FAIL` (subscription session limit) then halted the first attempt to
execute the narrow repair. That is a different failure class and is not charged to the local repair
budget.

## 3. Bounded technical repair — CONSUMED

The narrow **field-only repair path** — the author revises exactly one field of one case in response
to the construct auditor's finding, returning a small object instead of a whole family — is hereby
recorded as **the one bounded local repair of this execution chain**. It is now **consumed**.

It was chosen over an operator edit for a reason that is not convenience: authorship must stay with
the candidate-blind author. This session has read the frozen candidate, so held-out content written
here by hand would destroy the independence model preregistered for Stage C.

## 4. Status of the next model execution

The next model execution on this chain is the **FINAL eligible technical retry**.

If a new technical defect occurs on it:
- **STOP**;
- record `NOT_EXECUTABLE` for this execution chain;
- make **no further harness repairs**;
- preserve the corpus and all counters;
- do not infer any professional result about the candidate.

## 5. Planned calls for the final retry

| step | callee | model | planned calls |
|---|---|---|---|
| targeted field repair, `SPEECH_FALLBACK` case 2 `competent_generic_baseline` | candidate-blind author | `opus` | 1 |
| re-audit of `SPEECH_FALLBACK` only | candidate-blind auditor | `sonnet` | 1 |
| | | **total** | **2** |

Candidate calls in this step: **0**. Grader calls: **0**. No metered API fallback is permitted.

Scoring of the candidate begins only if `SPEECH_FALLBACK` reaches `ACCEPT` and the whole corpus is
then sealed.

## 6. Deterministic regression precondition

Before the final retry, the narrow repair path is covered by a deterministic regression that makes
**zero model calls**: `test_heldout_revision_path_v0.1.py`. It must pass first.

## 7. Claim ceiling — unchanged

Stage C cannot yield `QUALIFIED` under any outcome. After a `HELDOUT_PASS`, the Stage D real
ordinary used-car practical gate remains mandatory.
