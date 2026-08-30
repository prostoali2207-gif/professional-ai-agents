# Analytics release closure: minimum valid closure and the cross-model protocol revision

Author: independent release evaluator, Agent Architect workflow.
Written: 2026-08-30, **before** the external pack was authored and before any candidate execution.
Subject: `growth-experimentation-measurement-v1.0-consolidated`,
digest `sha256:3f4f3e133e81b00a1536fc6c72f1f59c24ef9f7b4c50c762c3c6c5bf6c4dd63d`.

This document does two things the release cannot proceed without: it states the exact minimum
closure under current policy, and it resolves the cross-model requirement **before** execution
rather than after seeing a result.

---

## 1. Evidence taken as established

Not re-derived, not reinterpreted:

| Fact | Source |
|---|---|
| Fresh preregistered two-tier gate, run `33264418604`, **PASS** | `qualification-gate-result-v1.0-twotier-2026-09-01.md` |
| 0/70 Tier 1, 6/70 Tier 2 (max 1 on any fixture), 0 INVALID, 0 retries, no best-of-N | same |
| Candidate, grader, generator, classifier, contracts frozen and verified at run time | same |
| That PASS is **not** reusable-core release qualification | `preregistration-v1.0-twotier-2026-09-01.json`, `qualification_boundary` |
| Library entry `growth-experimentation-measurement@1.1.0` is `quarantined` | `architect/library/catalog.json` |

## 2. What the preregistration still requires

`preregistration-v1.0-twotier-2026-09-01.json` names exactly two outstanding items:

1. **an externally authored held-out set** — because "the same party wrote the generator, the
   oracle and the candidate repairs";
2. **the cross-model release protocol**.

`qualification-queue-audit-2026-08-23.md` adds the governing form of the second: *"Satisfy the
preregistered cross-model release requirement or formally revise that release protocol through an
evaluator-owned process before execution."* `final-qualification-review-2026-08-27.md` F-6 raised
the same point as a blocking finding, precisely because 1.1.0 was promoted on two families with
**no revision record**. A silent narrowing is what failed last time; this document exists so that
does not repeat.

## 3. The minimum valid release closure

Under `professional-core-library.md` (admission review E, "evaluation sufficiency"),
`eval-integrity-and-regression.md`, and SKILL Phase 10, the minimum is:

| # | Requirement | How it is met here |
|---|---|---|
| R1 | Held-out material authored independently of the party that wrote the candidate and the oracle | Scenarios authored on a different model family by an author that has never seen the candidate; see §5 |
| R2 | Expectations construct-valid and not fitted to observed output | Derived mechanically by `external_pack_contract.admit` from the authored numbers; the authoring schema has no slot for an expectation |
| R3 | Grader frozen before qualifying execution and not written alongside the new pack | `grader_v07_structural.py`, blob-identical to the one that produced the 70-trial ledger, imported unmodified |
| R4 | Thresholds, hard-fails, trial count and retry policy frozen before execution | `preregistration-external-2026-09-02.json`, committed before the run; criterion identical to the adopted stability audit |
| R5 | Candidate never receives the oracle or expectations | Runner hands the executor one candidate-facing fixture; asserted deterministically |
| R6 | Cross-model requirement satisfied or formally revised, before execution | This document, §5–§7 |
| R7 | Apparatus failure cannot be scored as candidate failure | Frozen `trial_outcome_classifier.py`; any INVALID voids the gate |
| R8 | One unambiguous repository status afterwards | §8 |

Anything beyond this list is not release closure; anything less is not either.

## 4. What is deliberately *not* required

* **Re-running the 70-trial Gemini gate.** It is valid evidence for what it measured. Repeating it
  buys nothing and `resource-cost-engineering.md` names duplicate execution on an unchanged
  candidate without a new hypothesis as a waste signal.
* **Repairing the 1.1.0 evidence chain** (findings F-3, F-4, F-5). 1.1.0 was a different artifact
  assembled from seven documents. The release here is a **new version bound to a new digest** with
  a clean evidence chain; 1.1.0's history is preserved rather than rewritten, per
  `professional-core-library.md` ("do not delete history to make the catalog look clean").
* **Any candidate change.** Out of scope by construction.

---

## 5. The cross-model requirement: what is actually executable

### 5.1 Where the three-family rule came from

Every Analytics gate from v0.1 to v0.3 preregistered `required_runtimes: ["ChatGPT", "Gemini",
"Claude"]`. Its execution method was `manual-cross-model-exam.md` (2026-08-18), which is explicit
about what it is: *"Allow a frozen Analytics candidate to be exercised in a clean Claude, Gemini,
ChatGPT, or other capable chat **without requiring API access**… This is not fully automated
qualification."* The three-family rule was a **manual copy-and-paste procedure**, viable because a
human was pasting text into three chat windows. It has never been executed as an automated gate,
and the repository has no executor or credential path that could execute it as one.

### 5.2 Eligibility of each family for the v1.0 assembly, verified

| Family | Executor in repo | Credential in repo | Verdict |
|---|---|---|---|
| Gemini | `executor_gemini.py` | `secrets.GEMINI_API_KEY` (63 workflow references) | **ELIGIBLE** |
| Groq / Qwen | `executor_groq.py` | `secrets.GROQ_API_KEY` (26 references) | **INELIGIBLE for candidate execution.** The frozen assembly is 40,544 bytes (~10.1k tokens) before the fixture. v0.5 measured HTTP 413 at 8,273 tokens against the free-tier 8,000 TPM ceiling; this assembly is larger again. |
| OpenAI / ChatGPT | `executor_responses.py` | `secrets.OPENAI_API_KEY` (20 references) | **INELIGIBLE.** Excluded by standing evaluator instruction: no OpenAI quota may be consumed for this work. |
| Claude | none | none — zero references to any Anthropic credential across all 98 provider-secret references in `.github/workflows/` | **NOT EXECUTABLE** |

Per `qualification-execution-routing.md`, subscription-backed Claude Code was considered as a
Claude-family candidate runtime and **rejected on independence grounds**, not on cost: a coding
agent executing the candidate would hold filesystem access to the very repository containing the
oracle, the grader and the expectations. The evaluator could not prove the candidate did not
receive them, and R5 is not a property that can be asserted on trust. Routing policy is explicit
that a subscription route may not substitute where independence cannot be established.

**Conclusion: exactly one model family is eligible to execute this candidate.** The three-family
protocol is `NOT_EXECUTABLE` in the sense defined by `qualification-execution-routing.md`.

### 5.3 What the rest of the library actually does

| Core | Lifecycle | Candidate runtime at qualification |
|---|---|---|
| `paid-media-performance-marketing` 1.0.0 | qualified | gemini-3.1-flash-lite |
| `video-editing-post-production` 0.1.0 | qualified | gemini-3.1-flash-lite |
| `market-competitive-intelligence` 1.0.0 | qualified | gemini-3.1-flash-lite |
| `social-content-creative` 0.1.0 | qualified | gemini-3.5-flash-lite |
| `growth-experimentation-measurement` 1.0.0 | superseded | ChatGPT, Gemini, Claude (manual chat) |

**Four of the five currently-qualified cores were released on a single Gemini candidate runtime.**
Multi-family candidate execution is not this library's release standard; it is an Analytics-local
survival from the manual-exam era. Retaining it as written would hold Analytics to a bar no other
core has met, using a method no longer available, and would leave the core permanently
quarantined for a reason unrelated to its professional content.

## 6. The revision

**Revised requirement, adopted by the evaluator, effective for this cycle and recorded before any
external case was authored or any candidate call was made:**

> The Analytics release protocol's three-runtime requirement (`ChatGPT + Gemini + Claude`) is
> replaced by:
>
> 1. **one eligible candidate runtime family**, named in the preregistration and recorded in the
>    qualification record's `environment.model_or_executor`; **and**
> 2. **evaluation-side family independence**: the held-out material must be authored by a model
>    family *different from* the candidate runtime family, by an author that has not seen the
>    candidate. Falling back to the candidate's own family for authoring aborts the cycle; it does
>    not degrade it; **and**
> 3. **an explicit portability limitation** in the qualification record: the release claim is
>    scoped to the tested runtime family, and deployment on another family is a **revalidation
>    trigger**, not an inherited PASS.

### Why this is a substitution and not a weakening

The three-family rule bought one thing: evidence that the professional behavior is a property of
the *artifact* rather than of one runtime's habits. It is unobtainable here. The revision does not
pretend to obtain it. Instead it:

* **narrows the claim** to exactly what was measured — which is what `professional-core-library.md`
  designs `environment`, `limitations` and `revalidation_triggers` for — rather than asserting
  portability on absent evidence;
* **adds a requirement Analytics did not previously carry**, in the dimension where this core's
  evidence actually failed. The 2026-08-27 review's blocking findings were about *authorship and
  selection*: best-of-run promotion (F-1, F-2), fixtures authored inside the scoring loop (F-7),
  a burned suite cited as qualifying evidence (F-4). Runtime diversity would not have caught any
  of them. Independent authorship on an independent family is aimed squarely at them.

The bar moves sideways onto the axis where this core is weak, and the claim shrinks to fit the
evidence. Neither the Tier 1 zero-tolerance, the Tier 2 caps, the trial count, the retry ban nor
the INVALID rule is touched.

### What this revision explicitly does not license

* It does not restore `qualified` by itself. It resolves a precondition; the gate still has to pass.
* It does not apply to any other core or any future Analytics version. A later cycle with an
  eligible second candidate family must use it.
* It does not permit a Gemini-authored pack. If Groq authoring is unavailable at run time, the
  cycle ends `INVALID / NOT EXECUTABLE`. The independence property is the substitution; without it
  there is nothing left standing in place of the requirement being replaced.

### Residual risk, stated rather than papered over

Cross-runtime portability of this core is **unproven**. A deployment of the released artifact on a
non-Gemini runtime carries no evidence from this cycle and must revalidate. This is a real gap in
the release, recorded as a limitation and as a revalidation trigger, and it is smaller than the
gap that would remain if the core stayed quarantined over an unexecutable procedure.

A second residual: the external author is a language model, not a human practitioner. It removes
*evaluator* authorship, not *model* authorship. Admission is therefore not a formality — each case
is re-checked against the numeric construct it claims, and cases that do not instantiate their
family are rejected with the rejection counted in the pack provenance.

## 7. Resource and cost gate for the run this authorises

Per `resource-cost-engineering.md` §"Pre-run budget gate":

| | |
|---|---|
| **Objective** | Establish that 0/70 Tier 1 was a property of the candidate, not of the evaluator's own case authorship |
| **Decision impact** | PASS closes the release; FAIL keeps the core quarantined with a named professional blocker |
| **Alternatives** | None deterministic: the claim is about behavior on unseen material |
| **Eligible route** | Authoring on Groq (small payload, eligible); candidate execution on Gemini (only eligible family) |
| **Resource estimate** | ≤ 15 Groq authoring calls; exactly 70 Gemini candidate calls |
| **Quota state** | Gemini: an identical 70-call run completed on 2026-08-29 with 0 INVALID, which is direct evidence that 70 calls fit. Groq: per-minute limited, paced; the authoring payload is ~2k tokens, far inside the ceiling that disqualifies it downstream |
| **Stop condition** | The gate's own verdict. No repair and no rerun after the result |
| **Mid-run exhaustion plan** | Provider failure classifies INVALID, the gate voids rather than mis-scoring, and the pack is preserved |
| **Verdict** | `ALLOW` |

## 8. Repository state this closure must leave behind

On PASS: publish the consolidated artifact as a new library core version with its own manifest and
a qualification record bound to its digest; move the catalog entry to `qualified` against that new
version; supersede `qualification-status-v0.3.json`; record the portability limitation and its
revalidation trigger. The quarantined 1.1.0 evidence stays where it is, superseded rather than
rewritten.

On FAIL: the core stays quarantined and the exact production-relevant blocker is recorded.

On apparatus failure: `INVALID`, the pack and the candidate are untouched, and nothing about the
candidate is claimed.
