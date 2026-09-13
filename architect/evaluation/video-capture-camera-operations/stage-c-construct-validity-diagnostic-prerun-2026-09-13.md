# Stage C — construct-validity diagnostic — PRE-RUN record

Date: 2026-09-13
Issue: #294
Branch: `fix/video-capture-v0.4-294`
Base commit: `9cdaf6d`
Recorded BEFORE any model call. Model calls at time of writing: **0**.

## 1. Purpose

Measure the reliability of the **first** construct-audit pass after a **proven false negative** on
`SPEECH_FALLBACK`, where the first audit returned `no_hidden_leakage: true` and a second audit of
byte-identical candidate-visible text returned `false` with a finding verified correct against the
family's own pair contract.

This diagnostic measures the **evaluator instrument**, not the candidate. No professional conclusion
about v0.4 can be drawn from it in either direction.

## 2. Classification

**`EVALUATOR_CONSTRUCT_FAIL`.**

This is explicitly **not** an additional `LOCAL_EXECUTION_FAIL` repair.

- Stage C technical repair budget: **1, consumed — not reset and not used by this diagnostic.**
- This diagnostic performs **no harness repair**, **no case repair**, and **no candidate execution**.
- `SPEECH_FALLBACK` is **not** repaired in this step.
- Frozen v0.4 is **not** touched; all five blobs re-verified as matching at `9cdaf6d`.
- Held-out cases are **not** modified; corpus digest `f8220bc2f10c7465…` is recorded and must be
  unchanged when the diagnostic ends.

## 3. Second audit pass — design

One pre-committed second audit over exactly the **11 families currently holding ACCEPT**:

`AMBIGUOUS_INTENT`, `BEAUTY_VS_PROOF`, `COVERAGE_TIME`, `DEVICE_TRAP`, `DYNAMIC_RANGE`,
`MOVING_FOCUS`, `ROUTINE_LOCATION`, `SAFETY_AUTHORITY`, `STABILIZATION_TRAP`, `TRUTH_PRESSURE`,
`WHITE_BALANCE`.

`SPEECH_FALLBACK` is excluded: it already holds REVISE and is the known defect.

### Blindness of the second auditor

Guaranteed by construction, not by instruction. Each invocation is a **fresh child process** with
`--safe-mode`, `--no-session-persistence`, no tools, no MCP, and a throwaway working directory, and
its prompt is built from exactly two inputs: the sealed family pack and the frozen audit
contract/rubric.

It therefore does not receive, and cannot reach:
- the candidate (professional model, overlay, router — none are in its prompt or its filesystem);
- any first-pass verdict;
- any first-pass finding;
- any information about the `SPEECH_FALLBACK` defect or that a diagnostic is underway.

### Instrument held constant deliberately

The second pass uses the **same auditor model (`sonnet`) and the same unmodified rubric** as the
first pass. This is test-retest reliability of the exact instrument whose output is in question.
Changing the model would measure a different instrument and would not tell us whether the first pass
can be trusted.

## 4. Execution rules, fixed before the run

1. Exactly **one** second audit per family. Eleven calls total.
2. **No repeat audit to obtain ACCEPT.** Verdict shopping would corrupt the diagnostic and the
   qualification.
3. **No defect is repaired during this pass**, whatever is found.
4. **The pass does not stop at the first REVISE.** All eleven results are required to estimate the
   false-negative rate.
5. Second-pass results are written to a **separate directory**, `heldout-v0.1/audit-pass2/`. The
   first audit in `heldout-v0.1/audit/` is **never overwritten**.
6. Candidate calls must remain **0**. Grader/scoring calls must remain **0**.

## 5. Planned calls

| step | callee | model | planned calls |
|---|---|---|---|
| second construct audit, 11 ACCEPT families | candidate-blind auditor, fresh process each | `sonnet` | 11 |
| | | **total** | **11** |

Candidate calls: **0**. Grader calls: **0**. No metered API fallback.

## 6. Deterministic comparison after the run — no model calls

- `ACCEPT -> ACCEPT` count (agreement);
- `ACCEPT -> REVISE` count (**confirmed first-pass false negatives**);
- which specific construct checks disagree, per family;
- corpus digest re-verified unchanged;
- **no professional conclusion about the candidate.**

## 7. Stop condition

After the comparison: **STOP**. No scoring, no repair, no candidate execution.

A technical failure on any of the eleven calls is recorded with its family and cause; it does not
consume the Stage C technical repair budget and does not authorize a harness fix.

## 8. Release claim — unchanged

`CANDIDATE / DEVELOPMENT_PASS / HELDOUT_NOT_EXECUTED / PRACTICAL_NOT_EXECUTED`. **Not QUALIFIED.**
