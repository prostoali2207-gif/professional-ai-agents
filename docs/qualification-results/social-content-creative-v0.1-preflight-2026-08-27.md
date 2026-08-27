# Social Content Creative 0.1.0 — qualification preflight record, 2026-08-27

Status: **QUALIFICATION_NOT_EXECUTABLE** (infrastructure). No professional
verdict was produced, and none may be inferred from this record.

## Frozen candidate

| Field | Value |
| ----- | ----- |
| Core | `social-content-creative` 0.1.0 (lifecycle: candidate) |
| Commit | `163f68671288fe5035a8d09197334ec9df728b93` |
| Artifact digest | `sha256:ce5f537d336e6a6396f47c1ae492a687c4dc4b30ade8ab37bb4abb94d6251c0f` |
| Branch | `architect/social-content-creative-core-2026-08-23` |
| Cycle | `social-content-creative-0.1.0-heldout-2026-08-23` |

The digest was recomputed independently from the two immutable artifact paths
and matches both the preregistration and the core manifest. The candidate, the
competency matrix, the frozen qualification protocol, the hard-fail rules and
the pass thresholds were **not** modified.

## What ran

All checks below are deterministic and were executed offline. **Zero provider
calls were made and zero paid quota was consumed.**

| Stage | Result |
| ----- | ------ |
| `py_compile` of executor / sealed runner / author | PASS |
| Frozen candidate commit availability | PASS |
| Frozen artifact digest recomputation | PASS |
| `--qualification-contract` handshake vs. preregistration | PASS |
| `paid_workflow_guard.py` on the candidate branch | PASS (47 workflows, 2 exceptions) |
| Manifest schema validation (`qualification_preflight --phase static`) | PASS |
| Timeout arithmetic (120 < 180 < 2400) | PASS |
| Sealed transport, key fingerprint, AEAD, pack + component digests | PASS *(after repair)* |
| Fixture/grader cardinality and family structure (12 × 12 × 1) | PASS *(after repair)* |
| Sealed-runner cold start (`sealed_runner_startup_preflight`) | PASS |
| Sealed runner control flow, scoring, report shape (stubbed judges) | PASS |
| Sanitized report validation + release ledger | PASS |
| Candidate canary | NOT RUN — no credential |
| Scored held-out qualification | NOT RUN |
| Judgment evaluation | NOT RUN |

Method: the cycle was rehearsed end to end in a throwaway worktree with the
authoring call stubbed out and obvious synthetic placeholder fixtures. The
rehearsal harness is committed under `repairs/` so the finding is reproducible
without a credential. Its outputs are **not** qualification evidence.

## Blocking failure SCC-INFRA-1 — deterministic, repairable

```
{"status": "FAIL", "failure_class": "RUNTIME_CONTRACT_MISMATCH",
 "message": "freeze record model differs from runtime model"}
```

Root cause: `author_sealed_pack_v0_1.py` writes the freeze-record key
`candidate_model`, while `qualification_preflight.verify_sealed_pack` requires

```python
if freeze.get("model") != m["runtime"]["model"]:
    fail("RUNTIME_CONTRACT_MISMATCH", "freeze record model differs from runtime model")
```

The key is simply absent, so the comparison is `None != "gemini-3.5-flash-lite"`
and the sealed preflight fails on **every** run. The convention in the cycles
that do reach a verdict (`growth_strategy_experiment_portfolio`,
`sales-lead-conversion`) is `"model"`; Social Content Creative and
`conversion_messaging_web_copy` are the two that drifted.

Cost of not catching it deterministically: the failure lands *after* the paid
Gemini held-out authoring call, which is exactly the class
`paid-execution-policy.md` exists to prevent.

Repair: `architect/evaluation/social_content_creative/repairs/freeze-record-model-key-2026-08-27.patch`
— adds `"model"` to the freeze record and lifts the model literal into a single
`CANDIDATE_MODEL` constant. It touches no fixture, grader, threshold, hard-fail
rule or candidate artifact. With the patch applied the sealed preflight, the
runner cold start and the full stubbed dry run all pass.

**The patch is not yet landed.** It applies to
`architect/social-content-creative-core-2026-08-23`, which is the branch the
qualification workflow checks out. Landing it there requires explicit
permission to push to that branch.

## Blocking failures SCC-ENV-1 / SCC-ENV-2 — environment

* `GEMINI_API_KEY`, `GROQ_API_KEY` and `QUALIFICATION_SEALED_PACK_MASTER_KEY`
  are GitHub Actions repository secrets and are not bound to this interactive
  remote session.
* `api.groq.com` is denied by this session's egress policy (gateway answered
  403 to CONNECT). The frozen protocol requires two independent calibrated
  judges, one of which is Groq/Qwen, so the judgment stage cannot run here even
  if a credential were supplied. `generativelanguage.googleapis.com` is
  reachable but returns 403 without a key.

## Runtime substitution — considered and rejected

Running the candidate or the judges on the Claude runtime available in this
session was considered and rejected:

1. the frozen executor declares `provider: gemini-interactions-api` and the
   contract handshake is bound to it, so a provider swap needs a new executor
   and a new cycle preregistration — that is a new test, not the frozen one;
2. no Anthropic/Claude executor adapter is preregistered anywhere in the
   repository (`architect/evaluation/harness/adapters/` has OpenAI, Gemini and
   Copilot adapters only);
3. evaluator independence would collapse: one model would author the held-out
   pack, answer as the candidate, and serve as both "independent" judges.

## Resource accounting

| Item | Value |
| ---- | ----- |
| Paid provider calls made | 0 |
| Completion calls made | 0 |
| Provider credentials used | none |
| Unauthenticated reachability probes | 2 (no completion generated) |
| Runtime | Claude Code remote session, Python 3.11.15, local venv |

If the cycle is authorized after the repair lands, the real envelope is
**29 Gemini completion calls** (1 author + 1 canary + 24 candidate + 1
calibration + 2 judge) and **3 Groq/Qwen calls** (1 calibration + 2 judge). The
workflow's own pre-run budget gate still claims a 29-call total; it predates the
move of the author to Gemini and the addition of judge calibration, and
under-counts by three calls.

## Adjacent findings on `main`

Both were introduced by `71add9a`, the current head of `main`.

* **PLATFORM-1 (repaired here).**
  `architect/evaluation/qualification-platform/validate_sanitized_report.py`
  contained `def walk(value, path="$": str):` — a `SyntaxError`. The shared
  validator could not be imported and
  `tests/test_validate_sanitized_report.py` could not even be collected, so the
  qualification-platform suite was red for every cycle. Fixed to
  `def walk(value, path: str = "$") -> None:`; the suite now collects.

* **PLATFORM-2 (not repaired).** `.github/workflows/sales-0-3-gemini-r10.yml`
  lost its reusable deterministic-preflight job and its `QUALIFICATION_*`
  preregistration mirrors, which were replaced by inline checks inside the
  credential-bearing job — undoing the #136 pre-credential gate for that cycle.
  `test_deterministic_preflight.py::test_repaired_r10_passes` fails with
  `PREREGISTRATION_ENV_MISMATCH` (exit 15). This is outside the Social Content
  Creative path and re-integrating #136 for r10 is an evaluator decision, so it
  is reported rather than changed.

## Evidence integrity

No held-out pack exists for this cycle yet — it is authored fresh at run time.
No hidden fixture, grader key or expected answer was read, written or modified;
no sealed ciphertext was opened. The rehearsal used synthetic placeholders whose
`id`s are prefixed `REHEARSAL-`.

---

# Execution attempt, 2026-08-27 (two authorized paid runs)

Final verdict: **NOT EXECUTABLE**, blocked on `SCC-QUOTA-1`.

## Run 33058365193 — repair SCC-INFRA-1 confirmed

Head `118287e`. Deterministic preflight, static preflight, **sealed transport and
pack preflight**, and the **exact-runtime candidate canary** all passed — the
first time this cycle has ever reached the scored stage. That is production
confirmation of the freeze-record repair.

The scored runner then stopped at Groq judge calibration:

```
Groq judge HTTP 400: json_validate_failed ... "failed_generation": ""
```

Zero candidate calls. No scored evidence.

## Run 33058895070 — repair SCC-INFRA-2 confirmed, quota wall reached

Head `a65998f`, carrying the judge-transport repair. The `json_validate_failed`
class is gone; the run reached a different, later error:

```
Groq judge HTTP 413: Request too large for model `qwen/qwen3.6-27b`
service tier `on_demand` on tokens per minute (TPM): Limit 8000, Requested 12680
```

Two things are true here, and both matter.

**Partly self-inflicted.** `12680` is input plus `max_completion_tokens`.
Calibration input measures ~644 tokens, so the 12000-token budget I carried over
from the author path is what pushed *this particular request* over the ceiling.
Corrected to 4000 in `1200a01`.

**The real blocker is independent of that.** The batched held-out judge call
sends 12 cases, each carrying task, hidden reference and the full candidate
answer. Measured offline against the runner's exact payload shape:

| Case sizing | Held-out input tokens | vs. 8000 TPM ceiling |
| ----------- | --------------------- | -------------------- |
| lean | ~8,182 | exceeds |
| typical | ~14,782 | exceeds |
| rich | ~23,182 | exceeds |

Every one exceeds the ceiling **on input alone, before any completion budget**.
No value of `max_completion_tokens` makes the frozen batched two-judge design
executable on this Groq tier.

## SCC-QUOTA-1 — account eligibility constraint, evaluator decision required

This is not a code defect and I did not attempt a third run for it. Phase 6A
requires verifying account-specific quota from live evidence rather than
assuming it, and the policy on quota exhaustion is to stop and preserve
evidence rather than infer anything from partial completion.

Four resolutions exist, and three of them touch the grading apparatus, so none
is mine to take unilaterally:

1. raise the Groq account tier so the batched call fits;
2. split the batched judge call with TPM-aware pacing — changes how grading is batched;
3. substitute the second judge with a provider that accepts the batched payload — changes which model grades;
4. accept NOT EXECUTABLE and record it.

## Accounting for both runs

| Item | Value |
| ---- | ----- |
| Paid completion calls | 6 (2 × [1 author + 1 canary + 1 Gemini calibration]) |
| Groq requests | 2, both rejected before completion |
| **Candidate calls** | **0** |
| Scored evidence produced | none |
| Actions runs consumed | 2 |

Two held-out packs were authored and sealed in CI. The candidate never received
a single fixture, so no held-out case was consumed, no scored evidence exists,
and there is no PASS/REVISE to report. Nothing was tuned to make a test pass.
