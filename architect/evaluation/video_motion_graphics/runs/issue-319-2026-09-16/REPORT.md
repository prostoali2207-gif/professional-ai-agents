# Issue #319 — Motion Graphics v0.3 targeted regression + practical gate

Run date: 2026-09-16
Execution route: subscription-backed Claude Code, per the issue #319 **EXECUTION ROUTE CLARIFICATION**
(comment 5693435538, 2026-09-16T07:06:08Z), which replaced the Stage B Codex line for this execution chain.
Codex was **not** run in parallel as a second provider for this Stage B chain.

## FACT

Stage A deterministic verification passed 40/40 checks with zero model calls. All 18 visible v0.3
development cases (MG3-D01..D18) and the 6 coupled historical cases (MG-S3, S4, S5, S7, S8, S9) were run
once each against the frozen candidate and scored against the frozen `must_observe` / `reject_if`
criteria. 24/24 PASS, no P0 failure, no repeated material P1 family. Stage C verdict is
`DEVELOPMENT_PASS_VISIBLE_ONLY`. Stage D did not execute: the hash-bound historical practical source is
not available in this environment, so the verdict is `PRACTICAL_SOURCE_UNAVAILABLE` and no substitute file
was used under that fixture identity. The candidate remains `NOT_QUALIFIED`.

## CANDIDATE IDENTITY

- candidate: `motion-graphics-visual-explanation-video@0.3.0-candidate`
- freeze commit: `83fed979f9dd0c2cbed51fd2a4703a5e2f415c0d` (verified head of
  `repair/motion-graphics-v0-3-production-incident-2026-09-16`)
- candidate components, blob-verified against `candidate-freeze-v0.3.json`:
  - `professional-model-candidate-v0.3.md` → `61558427fa40a9050eb6d0d10f8a2278ea8a50a3`
  - `candidate-v0.3/SKILL.md` → `c1fad726ad06025aa148ab58acab6e8899e3045b`
- qualified parent: `video-editing-post-production@0.1.0`,
  digest `sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b`
  — recomputed independently from the manifest's documented canonical-line recipe and matched exactly;
  unmodified relative to `main`
- accessible baseline: `professional-model-candidate-v0.1.md` → `dd42a0acbb18eea77aed17147962acc384243e92`,
  single immutable blob across its whole history
- candidate status in-tree: `NOT_QUALIFIED`

## PROVENANCE STATUS

`PROVENANCE_GAP` — confirmed, not merely asserted.

An exhaustive scan of every reachable ref (1126 distinct path/blob pairs) found no `0.2` motion candidate
source artifact, no media files of any kind in history, no `.gitattributes`/git-LFS indirection, and no
blob whose content hashes to the historical digest. The digest
`sha256:55e04a52f789f42e0213d75534d9772ccca0c6a26e372b7c54d57004258f1fe6` appears only as a *reference*
inside v0.3 documents. The `0.2.0-candidate` identity is preserved as historical evidence and is not
reused; the candidate declares `NO_BYTE_INHERITANCE_CLAIM` in both its model and its router.

## TEST_ERROR

`no`.

One non-blocking cosmetic defect is recorded for post-run repair: in `MG3-D12`, a `must_observe` entry
reads `show_field_or_state evolution` (space instead of underscore). It is a label in a
human/semantically graded criterion, is not machine-parsed, and its meaning is unambiguous, so it did not
meet the "evaluator wrong or ambiguous" stop condition. Per scoring discipline the fixture was **not**
touched during the scored run.

## STAGE A

`STAGE_A_PASS` — 40/40 checks, 0 model calls, 0 paid API calls.
Verifier: `stage-a-verification.py`; full output: `stage-a-result.json`.

| Requirement | Result |
| --- | --- |
| exact branch + freeze commit | PASS |
| 18 visible v0.3 development fixtures (unique, contiguous, matching manifest) | PASS |
| exact v0.3 model/router blobs match freeze | PASS |
| preregistration + fixtures + transfer protocol predate implementation | PASS (timestamp **and** git-ancestry checks) |
| qualified parent unchanged | PASS (blob + independently recomputed digest + no diff vs `main`) |
| v0.1 accessible baseline unchanged | PASS |
| historical v0.2 identity/digest preserved and not reused | PASS |
| candidate status = `NOT_QUALIFIED` | PASS |
| frozen transfer protocol exists, still contains no hidden cases | PASS |
| coupled historical case set resolvable and exactly as preregistered | PASS |

Preregistration ordering evidence (commit timestamps on the freeze branch):
repair contract `1789540302` → visible fixtures `1789540342` → transfer protocol `1789540363` →
**implementation** `1789540406` → router `1789540425` → freeze `1789540450`. Every preregistered artifact
is also a strict git ancestor of every candidate component commit.

No generic qualification infrastructure was rebuilt. The Stage A verifier reads frozen blobs by revision
and asserts the issue's own Stage A list; it is a run record, not platform engineering.

## TARGETED REGRESSION

24 cases, run once each, no professional retries.

**Candidate isolation.** Each case ran in a fresh runtime whose readable context was exactly the four
frozen candidate-runtime files (router SKILL, qualified parent professional model, accessible v0.1
baseline, v0.3 repair model — hashes in `candidate-runtime-bundle.sha256`) plus one prompt-only task file.
The `must_observe` / `reject_if` criteria, fixture IDs, families, severities, the issue text and the
repository itself were withheld from the candidate runtime. Grading was done separately against the frozen
criteria, on observable professional decision rather than keyword match, preserving legitimate alternative
solutions.

| Case | Family | Pri | Result |
| --- | --- | --- | --- |
| MG3-D01 | CRAFT_GENERIC_UI | P1 | PASS |
| MG3-D02 | ART_DIRECTION_SELECTION | P1 | PASS |
| MG3-D03 | COMPARATIVE_CRITIQUE | P1 | PASS |
| MG3-D04 | OVERLAY_INTEGRITY | P0 | PASS |
| MG3-D05 | STRUCTURAL_EDIT_LOCK | P0 | PASS |
| MG3-D06 | TOOL_ROUTE_ASSET_SURFACE | P0 | PASS |
| MG3-D07 | REFERENCE_FIT | P1 | PASS |
| MG3-D08 | TYPOGRAPHY_CRAFT | P1 | PASS |
| MG3-D09 | SUBTITLE_SEMANTICS | P1 | PASS |
| MG3-D10 | STATE_CHANGE_EXPLANATION | P1 | PASS |
| MG3-D11 | STATE_CHANGE_EXPLANATION | P1 | PASS |
| MG3-D12 | STATE_CHANGE_EXPLANATION | P1 | PASS |
| MG3-D13 | MOTION_PURPOSE | P1 | PASS |
| MG3-D14 | LOCK_DISCIPLINE | P0 | PASS |
| MG3-D15 | MASTER_PROVENANCE | P0 | PASS |
| MG3-D16 | CRAFT_MOBILE_QC | P0 | PASS |
| MG3-D17 | REFERENCE_DERIVATIVE | P0 | PASS |
| MG3-D18 | OVERDESIGN_COMPREHENSION | P1 | PASS |
| MG-S3 | HIERARCHY | P1 | PASS |
| MG-S4 | TYPE | P0 | PASS |
| MG-S5 | MOTION | P1 | PASS |
| MG-S7 | REFERENCE | P0 | PASS |
| MG-S8 | TOOL_ROUTE | P0 | PASS |
| MG-S9 | CRITIQUE | P1 | PASS |

Per-case evidence is in `scoring-record.json`; verbatim candidate outputs are in `case-outputs/`.

MG-S1, MG-S2 and MG-S6 were **not** rerun. No new coupling evidence was documented before execution, so
the preregistered coupling set was honoured exactly.

### Required family rollup

| Family | Cases | Result |
| --- | --- | --- |
| visual-system craft | MG3-D01, MG-S9 | PASS |
| comparative judgment | MG3-D02, MG3-D03 | PASS |
| overlay integrity | MG3-D04 | PASS |
| structural workflow | MG3-D05 | PASS |
| tool/asset routing | MG3-D06, MG-S8 | PASS |
| reference selection/independence | MG3-D07, MG3-D17, MG-S7 | PASS |
| typography | MG3-D08, MG-S4 | PASS |
| caption semantics | MG3-D09 | PASS |
| state-change explanation | MG3-D10, MG3-D11, MG3-D12 | PASS |
| motion purpose | MG3-D13, MG-S5 | PASS |
| lock discipline | MG3-D14 | PASS |
| master provenance | MG3-D15 | PASS |
| mobile craft QC | MG3-D16, MG-S9 | PASS |
| overdesign/restraint | MG3-D18, MG-S3 | PASS |

Behaviour worth recording beyond the rubric, since it bears on the incident classes: MG3-D18 caught the
animated counters as an *information-integrity* failure (a count-up reads as measured magnitude without
approved data) rather than a taste issue; MG-S5 correctly escalated `CONCEPT` above the prompted
`MOTION_TIMING` symptom; MG3-D16 held `GENERIC_VISUAL_SYSTEM` as a provisional parent cause pending
re-observation instead of asserting it; MG-S4 invalidated prior craft observation on the affected ranges
and separated font-coverage causes from render-environment causes before repairing.

## P0 STATUS

10 P0 cases run (MG3-D04, D05, D06, D14, D15, D16, D17; MG-S4, S7, S8). **0 P0 failures.**
No hard-fail behaviour was observed: no silent locked-layer modification, no release approval despite
semantic overlay contradiction, no mastering from avoidably degraded material, no false execution claim
under missing authoring capability, no signature-surface imitation, no technical-pass-only release of an
observed craft failure.

## P1 FAMILY STATUS

14 P1 cases run. **0 P1 failures**, therefore no repeated material P1 family and no
`DEVELOPMENT_REVISE` trigger.

## PRACTICAL REGRESSION

`PRACTICAL_SOURCE_UNAVAILABLE` — Stage D not executed.

The required source `IMG_6502.MOV`
(`sha256:45de1fac61f9877289bca03867e3e7f91ba6685da775853466c30f43055a8209`) is absent from the filesystem
and from every reachable git ref; the repository has never contained media files and uses no LFS
indirection. Per the issue, no other file was substituted under that fixture identity, so none of the
twelve required practical steps ran: no beat map, no structural edit lock, no overlay ledger, no three
directions, no styleframes, no motion prototype, no rendered MP4, no phone-size review, no lineage check,
no VE-02/03/07/08/09/11/12 artifact checks, no calibrated comparative craft review.

This is a missing-input condition, not an infrastructure failure and not a professional failure, so it
consumes no stop-loss repair budget under `architect/methodology/qualification-stop-loss.md`.

## CRAFT REVIEW

`CRAFT_NOT_OBSERVED`.

No artifact was rendered or exported in this run, so no craft dimension — visual-system coherence,
composition/proportion/spacing, typography, shape/vector/graphic language, motion timing/curves, scene
continuity, compositing/depth, authored distinctiveness, restraint, phone-size final impression — was
inspected. Stage B evidence is decision evidence about craft reasoning; it is not craft evidence. Technical
PASS cannot substitute for craft PASS, and neither can semantic-case PASS.

## PARENT INTERACTIONS

The qualified parent was read-only throughout and is byte-identical to `main`: blob
`705485185f38c8f8ca7d154c2564e763badb0201`, digest recomputed to
`sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b`. No parent artifact was mutated.

Parent-boundary behaviour was observed only as candidate *reasoning* within Stage B — VE-02/VE-03
structural dependency (MG3-D05, MG-S5), VE-07 caption wording/timing/readability limits (MG3-D09, MG-S4),
lock respect over caption and approved layers (MG3-D14, MG-S3), delivery/QC authority remaining with the
parent (MG3-D06, MG3-D15). The artifact-level VE-02/03/07/08/09/11/12 interaction checks belong to Stage D
and **did not run**.

## GENERALIZATION STATUS

`HIDDEN_TRANSFER_NOT_RUN`.

`heldout-transfer-protocol-v0.3.md` (blob `33db146644432ac0fc6e328d7e7d377f8628c8e3`) was verified to exist,
to predate implementation, and to still carry `PREREGISTERED PROTOCOL ONLY — hidden cases do not exist yet`.
No hidden prompts were authored, and none were exposed to the candidate. Visible development evidence does
not satisfy hidden transfer. A fresh independent transfer set, authored after the freeze under the frozen
protocol by an author who has not seen candidate output, is still required, and a second materially
different real-media practical remains required before any qualification or architecture-split decision.

## MODEL/CALL ACCOUNTING

| Item | Value |
| --- | --- |
| Stage A model calls | 0 |
| Stage B candidate runs | 24 (one per case, no reruns) |
| Professional retries | 0 |
| Runner-level technical retries | 0 of the 1 permitted |
| Transient transport failures | 0 |
| Stage D model calls | 0 (not executed) |
| Hidden-transfer model calls | 0 |
| Candidate-runtime tokens (sum, 24 runs) | ~1,349,176 (mean ~56,216/case) |
| Tool calls per candidate run | 7 (5 reads + 1 write + 1 hand-back) |

No model calls were used to debug deterministic setup: Stage A, the provenance scan and the Stage D source
check are all deterministic git/filesystem work. No generic qualification-platform work was performed.

## PAID API

`0 paid API calls.`

Environment verified before Stage B: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`,
`GOOGLE_API_KEY`, `GROQ_API_KEY`, `XAI_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `AWS_BEARER_TOKEN_BEDROCK` all
unset; `CLAUDE_CODE_USE_BEDROCK` and `CLAUDE_CODE_USE_VERTEX` unset; no environment variable matching
`api_key`. `ANTHROPIC_BASE_URL` is the default `https://api.anthropic.com` with no metered credential
present — this session is authenticated through the user's Claude Code subscription, which is the route the
clarification authorises. No separately billed provider API was used as a fallback, and no second provider
was run against this Stage B chain.

## BLOCKER

Two blockers stand, in order:

1. **`PRACTICAL_SOURCE_UNAVAILABLE`** — the hash-bound `IMG_6502.MOV` must be restored to an accessible
   location before Stage D can run as specified. Substituting a different file under the same fixture
   identity is prohibited and was not done.
2. **`HIDDEN_TRANSFER_NOT_RUN`** — no generalization claim is possible until a fresh independent hidden
   set is authored and scored under the frozen protocol.

`PROVENANCE_GAP` also remains open and continues to block promotion independently.

## NEXT ACTION

1. Restore `IMG_6502.MOV` at its bound SHA-256 to an accessible path, then rerun Stage D only — Stage A and
   Stage B evidence in this record stays valid for the unchanged freeze.
2. Author the hidden transfer set under `heldout-transfer-protocol-v0.3.md`, by an author who has not read
   the Stage B outputs in `case-outputs/`, with criteria frozen before any candidate output is exposed.
3. Schedule the second materially different real-media practical task required by the transfer protocol.
4. Fix the cosmetic `MG3-D12` `must_observe` label in a post-run fixture revision under a new freeze — never
   mid-run.
5. Resolve or formally scope `PROVENANCE_GAP` before any promotion decision.

## Status ceiling

This run does **not** output `QUALIFIED`, `EXPERT-VALIDATED` or `PRODUCTION-PROVEN`.
The candidate remains `NOT_QUALIFIED`. Open promotion blockers: `PROVENANCE_GAP`,
`PRACTICAL_REGRESSION_NOT_RUN`, `HIDDEN_TRANSFER_NOT_RUN`. `TARGETED_REGRESSION_NOT_RUN` is now closed by
this record, as visible development evidence only.
