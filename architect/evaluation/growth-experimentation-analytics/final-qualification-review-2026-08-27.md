# Analytics Professional Core — final qualification review, 2026-08-27

Subject: `growth-experimentation-measurement` **1.1.0**
Artifact digest: `sha256:41431ad825ba231a326fab109762712c3737cad150ef8449c0a815a0be18393b`
Qualification record under review: `architect/library/qualifications/growth-experimentation-measurement/41431ad825ba231a326fab109762712c3737cad150ef8449c0a815a0be18393b/growth-experimentation-measurement-1-1-0-20260823.json`
Reviewed at repository HEAD `71add9a` (identical to `origin/main`).

## Verdict

**FAIL — the recorded `pass` is not supported at its own claimed boundary.**

The professional content of the core was not falsified by this review. What fails is the
evidence chain: the runs cited as qualifying PASS are best-of-repeated-attempt results on a
behavior the repository's own run history shows to be stochastically unstable, two cited
evaluation artifacts do not exist, one cited fixture's only execution was a behavioral
failure, and the three-model-family release protocol that governed every prior Analytics
gate was dropped without a revision record.

Lifecycle moved `qualified` -> `quarantined` in `architect/library/catalog.json` and
`architect/library/cores/growth-experimentation-measurement/1.1.0/manifest.json`.
Quarantine is the library's reversible "evaluation under investigation" state, not a
revocation: a preregistered repeated-trial re-run that passes restores `qualified`.

Per the instruction governing this review, the UAE automotive specialization was **not**
assessed. Core confirmation is a precondition and it did not hold. (No Analytics
specialization exists yet in any case; `architect/specializations/` contains only
`automotive-paid-media/1.0.0`.)

## Checks that pass

| Check | Result |
|---|---|
| Artifact content digest recomputed from `artifact.paths` git blobs at HEAD | matches declared digest |
| Frozen v0.3 assembly (v0.1 base + v0.2 + v0.3 overlays) blob SHAs at HEAD | unchanged; assembly digest `sha256:9e50360…46db` matches `candidate-freeze-v0.3.json` and `qualification-status-v0.3.json` |
| `catalog.json` <-> manifest <-> qualification record cross-references | consistent (`test_library_contract.py`, 7/7) |
| Manifest, qualification record and catalog against their JSON Schemas | 0 violations each |
| Existence of every cited GitHub Actions run and job | all present; each cited job concluded `success` |
| Paid-trigger policy on the three Analytics workflows | `workflow_dispatch` only; `paid_workflow_guard.py` tests 5/5 |

Candidate integrity is therefore intact. No frozen component was edited to chase a PASS.

## Blocking findings

### F-1 (P0, reliability) — the cited OpenAI held-out PASS is 1 of 3 executions

At SHA `7daede327f8316df3c4d3896d7830ff37df004cc`, with the identical frozen candidate,
fixture `fixtures/heldout-v0.3-decision-sufficiency.json` and grader
`grader_heldout_decision_sufficiency_v03.py`:

| Execution | Result |
|---|---|
| run `32563283125` (push), job `97008067505` | **FAIL** — `H-DS-01: "missing continued-spend cost"`; H-DS-02 PASS |
| run `32563284789` attempt 1, job `97008071502` | **FAIL** |
| run `32563284789` attempt 2, job `97008206844` | PASS — **this is the run cited as qualifying evidence** |

`H-DS-01`'s failed assertion is the continued-spend / cost-of-waiting requirement, i.e.
substantive GEM-C7 behavior, not a formatting nit.

`methodology/eval-integrity-and-regression.md`: "single-run success is weak evidence…
Do not quote a best run as system reliability", and lists "unbounded retry/reflection that
eventually gets lucky" as an anti-gaming target.
`qualification-platform/paid-execution-policy.md`: "do not rerun an unchanged professional
failure merely to seek a better stochastic result… Professional failure: revise the
candidate or follow an explicitly preregistered repeated-trial policy."

No repeated-trial policy was preregistered for v0.3 (see F-7). The candidate was not revised.

### F-2 (P0, reliability) — a P0 claim passed and failed at one identical commit on Gemini

At SHA `e9d1ae41221ae589cdfef21de22830ddc79f53cc`, same fixture suite
(`fixtures/heldout-v0.3-gemini-post-scorer-repair.json`), same grader, 26 seconds apart:

| Execution | Result |
|---|---|
| run `32621515986` (push), job `97150254130` | PASS (H-GDS-01, H-GDS-02) |
| run `32621517714` (pull_request), job `97150258494` | **FAIL** — `H-GDS-02: "missing refusal to SCALE from confounded evidence"` |

The failed assertion is **GEM-C2**, a P0 claim ("Blocks unsupported causal winner and SCALE
decisions when experiment or measurement integrity is materially unresolved").

`evidence-and-reuse.md` classifies all earlier Gemini attempts as having "exposed grader
construct defects". That classification cannot cover this pair: the grader blob was
identical across the passing and the failing execution, so the variance is in the candidate's
output, not in the scorer. This is stochastic instability in a mandatory behavior.

`architect/README.md` maintenance rule: "Once stochastic instability is observed in a
mandatory behavior, a single later PASS is not enough to restore a reliability claim; use
repeated trials appropriate to consequence and cost." The Professional Core Reuse precedent
for this repository is 3/3 independent trials with zero application retries.

The record's `evaluation.reliability_trials: 2` denotes two **model families**, not repeated
trials of the unstable behavior. On each family the qualifying suite was executed to a PASS
exactly once.

### F-3 (P0, evidence chain) — two cited evaluation artifacts have never existed

`evaluation.fixture_refs` and `evaluation.grader_refs` cite:

- `architect/evaluation/growth-experimentation-analytics/fixtures/heldout-v0.3-gemini-final-downstream-fresh.json`
- `architect/evaluation/growth-experimentation-analytics/grader_heldout_gemini_final_downstream_fresh_v03.py`

Neither path exists at HEAD, and `git log --all --diff-filter=A` shows neither has ever
existed. The artifacts actually executed in cited run `32621655293` are the same names
without the `-fresh` segment. A digest-bound attestation must not carry unresolvable
evidence pointers.

### F-4 (P0, evidence chain) — a burned fixture is listed as qualifying evidence

`fixtures/heldout-v0.3-gemini-final-fresh.json` and
`grader_heldout_gemini_final_fresh_v03.py` are listed among the qualifying fixtures and
graders. Their only execution — runs `32621592421` / `32621594325` at SHA `4277a5db` — ended
in a behavioral failure: `H-GF-02: "must KILL current A configuration"`. No passing run for
that suite exists, and no run reference for it appears in `evidence.run_refs`.

`H-GF-01`'s PASS is asserted in `evidence-and-reuse.md` with no run reference at all; it in
fact comes from that same failing run.

The `H-GF-02` -> `H-GFD-01` transition may well be a defensible construct repair — the
replacement grader broadens the accepted label from `KILL` alone to `{KILL, ITERATE}` while
preserving the stop-A action, causal ceiling, downstream-economics and exact-arithmetic
assertions. But that repair has no burn record. The v0.2 cycle set the standard here:
`q10-invalidation-and-q11-preregistration-v0.2.json` states the invalid construct, the
reason, and that Q-10 "is not used as candidate failure evidence", and
`qualification-result-v0.2.json` carries an explicit `burned_non_scored_cases` block. Neither
exists for `H-GF-02` or `H-GDS-02`.

### F-5 (P1, evidence chain) — cited run without its fixture/grader

`evidence.run_refs` cites run `32563140932` (targeted regression), but its fixture
`fixtures/regression-v0.3-decision-sufficiency.json` and grader
`grader_decision_sufficiency_v03.py` appear in neither `fixture_refs` nor `grader_refs`.

### F-6 (P0, release protocol) — the three-family gate was dropped without a revision record

Every prior Analytics gate preregistered `required_runtimes: ["ChatGPT", "Gemini", "Claude"]`:
`heldout-final-gate-preregistration-v0.1.json` (Q-05/Q-06),
`heldout-final-gate-preregistration-v0.2.json` (Q-07/Q-08),
`heldout-v0.2-preregistration.json` (Q-09/Q-10),
`q10-invalidation-and-q11-preregistration-v0.2.json` (Q-11).
`qualification-result-v0.2.json` records 3/3 families for both scored cases.

`qualification-status-v0.3.json` restates the same gate, marks Claude `NOT_EXECUTABLE`, and
sets the claim boundary: "Do not describe v0.3 as qualified, released, or library-admitted."
`qualification-platform/qualification-queue-audit-2026-08-23.md` — written the same day as the
promotion — repeats that v0.3 stays candidate/not library-admitted until the cross-model
requirement "is satisfied or formally revised through an evaluator-owned process".

1.1.0 was promoted on two families. No revision record exists. The word "Claude" does not
appear in the 1.1.0 manifest, in `evidence-and-reuse.md`, or in the qualification record.

`qualification-scope-policy.md`: "A preregistered full release qualification cannot be
replaced by `REUSE` or `TARGET`."

### F-7 (P1, process) — no v0.3 preregistration; graders revised against observed output

v0.1 and v0.2 each bound fixture and grader **blob SHAs before execution**. No equivalent
record exists for v0.3 or for the 1.1.0 release.

The Gemini qualification sequence — 15 workflow runs — was authored, executed, revised and
re-executed between 05:51:51 and 05:58:03 UTC on 2026-08-23, with fixture and grader commits
interleaved between scored executions ("Add final fresh Gemini Analytics grader" ->
"Run final fresh Gemini Analytics heldout" -> FAIL -> "Add final fresh downstream Gemini
Analytics case" -> "Add final downstream Gemini Analytics grader" -> "Run final downstream
Gemini Analytics heldout" -> PASS). Held-out material authored and adjusted inside the
scoring loop is development evidence under this harness's own
"Development vs qualification — hard separation" rule, unless each burn is recorded.

### F-8 (P1, repository state) — unreconciled contradictory status record

`qualification-status-v0.3.json` still carries `CANDIDATE_NOT_LIBRARY_ADMITTED` /
`DO_NOT_PROMOTE` and was never reconciled with the promotion. On this review's evidence its
verdict was correct, so it is left unchanged.

## Findings outside the Analytics scope

### F-9 (blocking, platform) — `validate_sanitized_report.py` did not compile — **fixed here**

`origin/main` HEAD `71add9a` shipped a `SyntaxError` at line 17
(`def walk(value, path="$": str):`). This failed the shared deterministic preflight's
`compile` check (exit 11, `COMPILE_FAILED`) for **every** candidate, and would have crashed
the r10 release gate's "Validate sanitized report" step. Repaired to
`def walk(value, path: str = "$") -> None:`; the module's 8 unit tests now run and pass
(they could not previously be imported).

### F-10 (blocking, platform) — r10 deterministic preflight baseline is red — **not fixed**

The same commit `71add9a` removed the workflow-level `env:` mirrors from
`.github/workflows/sales-0-3-gemini-r10.yml` (including
`QUALIFICATION_CRITICAL_HARD_FAILS_MAX`) and removed the reusable `preflight` job, while
`architect/evaluation/sales-lead-conversion/preflight/sales-0_3-r10-gemini.json` still binds
that variable. `test_deterministic_preflight.py::test_repaired_r10_passes` — the test
asserting "the r10 spec as committed must pass every check" — now fails with exit 15,
`PREREGISTRATION_ENV_MISMATCH`.

Left unrepaired deliberately: either the spec or the workflow is the intended source of
truth after the `--preregistration` refactor, and that is the Sales cycle owner's call.

## Root cause of the instability

Investigated separately and recorded in
`instability-root-cause-2026-08-27.md`: every qualified P0/P1 claim was asserted by regex
over free prose, so a verdict tracked phrasing rather than the decision. The gate failed a
correct H-DS-01 answer over word order and passed the P0 SCALE assertion on a sentence that
refuses nothing. Repaired in candidate v0.4 by moving the decision onto a structured
contract, with a deterministic regression locking paraphrase invariance and contrastive
discrimination. That repair is development evidence and does not lift this quarantine.

## What would restore `qualified`

No paid execution was performed for this review, and none should be authorized without the
pre-run budget gate required by `paid-execution-policy.md`.

1. Preregister a 1.1.x held-out gate **before** execution, binding fixture and grader blob
   SHAs, the required model families, and an explicit repeated-trial rule.
2. Execute the exact frozen v0.3 assembly for at least 3 independent trials per family with
   zero retries on each cited fixture, and record every trial, not the best one.
3. Either execute the Claude family or record a reviewed, evaluator-owned revision narrowing
   the release protocol to two families, with its rationale.
4. Write burn records for `H-GF-02` and `H-GDS-02` in the form used by
   `q10-invalidation-and-q11-preregistration-v0.2.json`.
5. Correct `fixture_refs` / `grader_refs` to the artifacts actually executed (F-3, F-5) and
   remove the burned suite from qualifying evidence (F-4).
6. Reconcile or supersede `qualification-status-v0.3.json`.

Only after the core is confirmed on that evidence should any UAE automotive Analytics
specialization be designed or assessed.
