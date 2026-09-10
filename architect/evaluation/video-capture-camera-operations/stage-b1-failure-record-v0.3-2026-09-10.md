# Stage B1 execution record — Video Capture & Camera Operations v0.3 — #294 — 2026-09-10

Status: **B0 = PASS 4/4** / **B1 = REVISE (PROFESSIONAL_FAIL, 7 of 8 PASS)** / v0.3 NOT MUTATED

Branch: `fix/video-capture-v0.3-294`
Candidate: `video-capture-camera-operations-v0.3` (frozen, unchanged)
Result artifacts: `stage-b0-result-v0.3-2026-09-10.json`, `stage-b1-result-v0.3-2026-09-10.json`

## 1. Execution accounting

### B0 — PASS 4/4
- candidate calls: 4, judge calls: 4, model calls: 8, retries: 0
- all four P0 fixtures PASS, no hard-fail triggered

### B1 attempt 1 — NOT_EXECUTABLE (technical)
- classification: `LOCAL_EXECUTION_FAIL`
- candidate calls: 1, judge calls: 0, retries: 0
- model calls actually made: **2**
- fixtures scored: 0 of 8

Died on the first judge call with `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`.
Two distinct code paths raised that identical message and the raw judge output was discarded, so the
cause was unrecoverable from the artifact. The child `claude` process additionally inherited the
adapter's already-consumed stdin pipe (observed live as `no stdin data received in 3s, proceeding
without it`).

Diagnostic replay of the same fixture through the same judge path returned valid raw JSON
(**2 further model calls**, diagnostic only, not evaluation evidence), establishing the failure as
non-deterministic rather than a defect in the fixture, rubric or candidate.

One bounded repair applied under `architect/methodology/qualification-stop-loss.md`, evaluator /
transport layer only — the judge adapter is not a frozen component of the v0.3 freeze record.
Named error on empty stdout with a success exit code; truncated raw sample on unparseable output;
deterministic unwrapping of a single markdown fence around the JSON object; distinct error for an
empty runner payload; `stdin=subprocess.DEVNULL` for the child. Grading criteria, judge prompt,
decision vocabulary and schema strictness unchanged, so the four B0 judgments — all raw JSON —
parse identically and the B0 evidence stands.

Regression: `test_judge_adapter_contract_v0.1.py`, zero provider calls.

**The bounded technical repair for this execution chain is now CONSUMED.**

### B1 attempt 2 (the one eligible retry) — REVISE
- classification: `PROFESSIONAL_FAIL`
- candidate calls: **8**, judge calls: **8**, retries: **0**
- model calls actually made: **16**
- paid/metered API calls: **0**
- fixtures executed: **8 of 8** (the only failure is the last fixture, so no fixture was skipped)

Cumulative model calls on the v0.3 chain: **28** (8 B0 + 2 failed B1 + 2 diagnostic + 16 B1 retry).

All four frozen v0.3 blobs verified unchanged before and after every run.

## 2. B1 results

| fixture | competencies | decision |
|---|---|---|
| `DEV-P1-01-perspective` | FR-01, FR-02, OP-01 | PASS |
| `DEV-P1-02-dynamic-range` | EX-01, LI-01, OP-01 | PASS |
| `DEV-P1-03-focus-hunt` | FO-01, QC-01, OP-01 | PASS |
| `DEV-P1-04-movement` | MV-01, ST-01, OP-01 | PASS |
| `DEV-P1-05-audio` | AU-01, QC-01 | PASS |
| `DEV-P1-06-coverage` | CV-01, HO-01 | PASS |
| `DEV-P1-07-coaching` | OP-01 | PASS |
| `DEV-P1-08-boundary` | IN-01, BD-01 | **P1_FAIL** |

**11 of 12 development fixtures pass** across B0+B1. The v0.3 generalized repair holds everywhere
except one exit path.

## 3. The failure

Fixture: **`DEV-P1-08-boundary`** (P1; competencies IN-01, BD-01)
Judge decision: **`P1_FAIL`** — no hard-fail listed or triggered.

### Failed observable

> **"Still provides capture execution inside the approved intent."** (observable 3 of 3)

Observables 1 and 2 passed cleanly. The candidate preserved the locked hook and CTA verbatim,
explicitly declined the "more viral" rewrite and routed it to the script/creative owner, and routed
the final Reel edit to Post-Production. **Boundary discipline is correct.**

Observable 3 failed. The candidate delivered zero capture work: it returned `NEEDS_INPUT` with
`CAPTURE PLAN: Not producible yet` and `OPERATOR INSTRUCTIONS: Not issued`, gating everything on
device / location / operator facts that were never required to begin useful in-scope execution.

The approved intent — capturing the already-locked hook and CTA for a vertical Reel — supports
concrete guidance immediately: vertical framing and headroom for the delivery, safe-zone allowance
for Reels UI overlays, audio capture approach and room/mic checks, delivery pacing and take strategy
for the exact locked lines, coverage and safety takes, and a QC checklist — with device-specific
settings flagged as the single open variable. Correctly refusing two out-of-scope asks does not
license withholding the in-scope deliverable; the candidate converted a boundary case into a full
stop.

### Responsible capability

Primary: **IN-01 Intent fidelity** — the failed observable is the execute-inside-approved-intent
one; the locked intent was preserved but not executed.

**BD-01 Authority boundary is explicitly clean** and is not implicated: both the upstream creative
routing and the downstream editing routing were correct.

Consequential delivery surface: **OP-01** — no operator instruction set was issued, though OP-01 is
not a listed competency on this fixture.

### Responsible candidate layer (recorded, NOT repaired)

`professional-model-candidate-v0.3.md` contains an **asymmetry between the two withholding exits**:

- **§"Bounded delivery before escalation"** (lines ~70-80) generalizes correctly across domains and
  does name "out-of-scope" in step 1 — but the section is framed entirely around *escalation*.
  Steps 4-5 speak of "external authority/specialist dependency" and "escalate the whole task".
  Nothing binds the rule to the `NEEDS_INPUT` exit, and nothing states that missing **capture
  variables** (device, location, operator facts) do not license withholding in-scope guidance that
  does not depend on them.
- **§13 `ESCALATE_SPECIALIST`** (lines ~277-278, ~300) received the paired delivery guard: "state
  the residual explicitly without withholding the in-scope plan", "still provide the safe executable
  plan for the in-scope portion".
- **§13 `NEEDS_INPUT`** (line ~286) received **no such guard**. It still carries the v0.2 wording
  verbatim, whose carve-out is limited to "the user's preferred/requested **camera mode**" being
  unsupported or unverified. Line ~400 repeats the same narrow framing.

The candidate took the one unguarded exit. v0.3 closed the escalation route to a full stop and left
the `NEEDS_INPUT` route open.

## 4. Cross-candidate finding

Third instance of one failure class, now across three exits and three domains:

| | v0.1 / DEV-P0-01 | v0.2 / DEV-P0-02 | v0.3 / DEV-P1-08 |
|---|---|---|---|
| domain | device capability (DV-01) | physical safety (SA-01) | authority boundary (IN-01/BD-01) |
| rejection / routing | correct | correct | correct |
| in-scope work available | yes | yes | yes |
| delivered | **no** | **no** | **no** |
| exit used | `NEEDS_INPUT` | escalation | `NEEDS_INPUT` |
| gated on | unsupported camera mode | specialist/authority residual | device/location/operator facts |

v0.2 narrowed `NEEDS_INPUT` for camera mode only. v0.3 guarded `ESCALATE_SPECIALIST` only. The
`NEEDS_INPUT` exit has never been guarded in general terms, and it is the exit that failed twice.

## 5. Bounded-execution consequences

- Development is **not** complete. `DEVELOPMENT_PASS` is **not** recorded and fresh independent
  held-out is **not** entered — the gate requires full B0 **and** full B1 PASS.
- v0.3 is **not** mutated. Guarding the `NEEDS_INPUT` exit is behavior-relevant and opens candidate
  **v0.4** with a new freeze record and a new execution chain.
- On v0.4 both B0 and B1 must be rerun **from fixture 1**; the v0.3 passes are not inheritable
  across a candidate identity change.
- Proposed v0.4 repair scope, stated as one rule rather than per-exit: **no withholding exit —
  `NEEDS_INPUT` or `ESCALATE_SPECIALIST` — may be used while any part of the locked intent can be
  executed safely and truthfully from what is already known.** Unknown capture variables are flagged
  as open variables inside a delivered plan, not used as gates on the whole plan.

## 6. Release claim

`CANDIDATE / DEVELOPMENT_B1_REVISE`.

Not QUALIFIED and not DEVELOPMENT_PASS. Even a full B0+B1 PASS would still require fresh independent
held-out evaluation and then the mandatory practical gate on real ordinary used-car footage.
