# Growth Experimentation & Measurement 1.2.0 — evidence and reuse

## What this version is

One consolidated runtime document. It replaces the seven-document assembly that 1.1.0 shipped
(base v0.1 plus six overlays) with a single coherent statement, and it carries two repairs made
after externally authored held-out evidence showed the previous expressions failing on unseen
material.

## Qualifying evidence

| Cycle | Run | Candidate | Result |
|---|---|---|---|
| Two-tier held-out, evaluator-generated suite | `33264418604` | v1.0 consolidated | PASS — 0 tier-1 in 70 |
| External held-out, independently authored | `33293694601` | v1.0 consolidated | INVALID (one Gemini HTTP 500); 15 tier-1 observed in 69 measured |
| External held-out | `33299723985` | v1.1 | FAIL — 6 tier-1 in 70, 0 INVALID |
| **External held-out** | **`33304743788`** | **v1.2** | **PASS — 0 tier-1 in 70, 1 tier-2, 0 INVALID** |

The release rests on the last row. The three cycles before it are recorded because they are what
the release claim has to survive, not because they support it.

## What the external cycles changed about the claim

Every gate before `33293694601` drew its cases from a generator the evaluator wrote. That suite
returned 0 tier-1 in 70 for v1.0. An independently authored pack, on the same frozen grader and the
same criterion, returned 15. The difference was not the bar; it was that the evaluator's own
vocabulary was doing work the candidate had been credited with.

Two repairs followed, and they are the substance of this version:

* **the comparison-level identifier is recognised structurally** — the declared identifier that
  keys no per-arm outcome block is the comparison as a whole. Before this, the candidate could
  only find it when the evaluator happened to call it `experiment`. This took the scope-target
  failure class from 11 to 0.
* **the identification ledger** — five defect questions answered from declared design facts,
  closed before any outcome count is read, with the four fields thin counts may touch named
  explicitly. Before this, sparsity was still being written into the causal channel on a
  randomised, window-complete design. This took the remaining tier-1 count from 6 to 0.

A third change was made and did **not** work, and it is recorded because the negative result is
part of the evidence: gathering already-stated rules into section 6.3 as emit-time invalidity
conditions moved its failure classes from 4 to 6. Adding a procedure changed behavior; restating a
rule did not.

## Boundary of the claim

**Runtime.** Qualified on the Gemini candidate runtime family (`gemini-3.5-flash-lite`,
temperature 0, thinking level medium). Cross-runtime portability is **untested by this cycle** and
is a revalidation trigger, not an inherited PASS. The three-runtime protocol that governed 1.0.0
was formally revised before execution — it is not executable in this repository, and the revision
substituted evaluation-side family independence for it rather than dropping the requirement. See
`external/release-closure-and-cross-model-revision-2026-09-02.md`.

**Independence.** The held-out pack was authored on Groq `openai/gpt-oss-120b` by an author that
never saw the candidate, was not told it had been repaired, and was given a scenario schema with no
field capable of carrying an expected answer. Expectations were derived by a frozen oracle from the
authored numbers. This removes evaluator authorship, not model authorship: the author is a language
model, not a human practitioner.

**Stability.** Seven independent trials per fixture, zero retries, no best-of-N, every trial
recorded. The criterion is the one adopted in `stability-criterion-audit-2026-08-31.md` and has not
been changed in any cycle since.

## Reuse

Reuse is licensed for the exact artifact digest only. A paraphrased or edited copy is not covered.
Composition and specialization require compatibility checks and affected-behavior evaluation; the
UAE automotive specialization in particular has never been assessed against this core.

The core supplies professional judgment. It does not supply organization-specific truth, live
platform mechanics, legal interpretation, campaign execution authority, or statistical methods
beyond its qualified computation boundary.
