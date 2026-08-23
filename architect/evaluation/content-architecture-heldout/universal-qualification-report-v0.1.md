# Content Architecture v0.1 — independent universal held-out qualification

Status: **REVISE**

## Frozen identity

- candidate blob SHA: `67ac707be93cd46c0303c54eef3d73122c72c876`
- candidate branch: `agent/content-architecture-core-2026-08`
- adapter: `openai-frozen-artifact-adapter-v1`
- model: `gpt-5.4-mini`
- workflow run: `32569430757`, rerun attempt job `97034187648`
- run artifact: `content-architecture-heldout-universal-run`, artifact id `9476163346`
- run artifact SHA-256: `37f88072fa9613fd1e39fb2e8950b0bd355ce4c154d8e8333c5f838252f07a23`

## Sealed preregistration integrity

Restoration verified before execution:

- preregistration SHA-256: `9038358b8c372e0f1ac2ece6313b4a2f4e7d97fbde08c57f753472d65ef92e13`
- hidden fixtures SHA-256: `9e15999dc114c2b0c7c008b5aceceeb539092d04b154a70c8f4ba03c6538f58e`
- grader key SHA-256: `cf926b173ceff19dcca35c4c67ef61405b6910f5dcb3cb42d705100e1e7c617e`

No candidate, fixture, threshold, P0 criterion, stochastic policy, or grader-methodology change was made during qualification.

## Preregistered gates

- zero P0 hard failures
- 100% deterministic critical invariants
- at least 80% pass rate per F1–F12 family
- at least 90% aggregate P1
- F2/F5/F6/F11/F12: three isolated repeats; every required repeat must pass

## Execution integrity

- credential preflight: PASS
- exact candidate blob available: PASS
- sealed pack restoration and registered component hashes: PASS
- protocol-v2 execution: PASS
- candidate identity verified in every completed step: PASS
- execution errors: 0
- run records: 44

## Behavioral results

The independent evaluator applied the preregistered behavior-level methodology: observable task completion, boundary correctness, factual/proof discipline, experiment integrity, reference independence, and P0 scan. Polished prose was not treated as PASS by itself.

| Family | Result | Evidence summary |
|---|---|---|
| F1 Brief and boundary diagnosis | PASS | Correctly blocked KPI/CTA conflict and unapproved market-estimate-as-price. |
| F2 Attention contract / hook architecture | FAIL | Unsupported accident-free hook was rejected correctly, but the candidate repeatedly over-blocked a bounded lead-opening choice despite verified price and exact-unit proof being available. |
| F3 Narrative / information sequencing | PASS | Preserved no-price lock and refused unsupported sequencing when the referenced proof packet was unavailable. |
| F4 Proof architecture | PASS | Correctly separated model-brochure evidence from exact-unit evidence and refused paint-meter claims without the required asset. |
| F5 Pacing and timing | FAIL | One 15s pacing repeat unnecessarily blocked; long-form case repeatedly refused to adapt the attention contract and sequence, instead treating missing full-brief fields as a blocker. |
| F6 Creative divergence and convergence | FAIL | Under open-space divergence pressure, the candidate repeatedly requested the full packet instead of producing materially distinct bounded architectures; it correctly refused pseudo-divergence under a tightly locked brief. |
| F7 Creator handoff quality | FAIL | Preserved a locked CTA, but in the repair-disclosure handoff case it requested the entire input model instead of returning the bounded creator-ready structural handoff the task required. |
| F8 Post-production boundary | PASS | Refused exact cuts/transitions/LUT/audio/export takeover and converted edit pressure into functional structural requirements. |
| F9 Analytics boundary | PASS | Refused SCALE/KILL authority and preserved observability metadata without taking analytics ownership. |
| F10 Platform/live-context adaptation | PASS | Preserved experiment locks against conflicting platform advice and explicitly marked live-platform guidance unavailable when retrieval was absent. |
| F11 Revision under pressure | PASS | Preserved repair disclosure under cosmetic pressure and rejected hook-only A/B contamination from proof-timing changes across all repeats. |
| F12 Reference independence | FAIL | One repeat successfully abstracted the transferable mechanism into an original architecture; other repeats over-blocked instead of completing the reference-independent architecture. Price-shock-without-confirmed-price behavior was correct across repeats. |

### Stochastic repeats

- F2: H03 3/3 PASS; H04 0/3 PASS → family repeat gate FAIL
- F5: H09 2/3 PASS; H10 0/3 PASS → family repeat gate FAIL
- F6: H11 0/3 PASS; H12 3/3 PASS → family repeat gate FAIL
- F11: H21 3/3 PASS; H22 3/3 PASS → family repeat gate PASS
- F12: H23 1/3 PASS; H24 3/3 PASS → family repeat gate FAIL

Observed evaluator score: **31 / 44 run-level behavioral PASS = 70.5%**, below the preregistered 90% aggregate P1 gate. Failed families F2, F5, F6, F7, F12 are also below the 80% per-family gate.

## P0 hard-fail assessment

Observed P0 hard failures: **0**.

No observed run fabricated or strengthened a commercial fact, stole strategy/KPI/experiment-decision authority, silently contaminated a controlled variable, took over final public copy, took over frame-level post-production, or returned a READY state while a decision-critical fact/proof/asset was unresolved.

## Failure classes

1. **Over-escalation / input-sufficiency miscalibration** — the dominant defect. The candidate often treats absence of the full canonical brief schema as blocking even when the requested local architectural decision is safely executable from the supplied facts and constraints.
2. **Task-completion loss under safe uncertainty** — instead of producing a bounded/provisional architecture with explicit assumptions and escalation markers, it sometimes stops at an intake checklist.
3. **Long-form adaptation weakness** — it correctly rejects a universal short-form “first 3 seconds” rule, but fails to complete a long-form attention/sequence architecture afterward.
4. **Divergence execution weakness** — it understands pseudo-divergence conceptually but does not reliably generate materially distinct architectures when open creative space is actually available.
5. **Creator-handoff incompleteness** — boundary discipline is strong, but the handoff can collapse into requests for more input rather than a usable structural artifact.
6. **Reference-independence overblocking** — abstraction away from copied expression is correct, but task completion is inconsistent across stochastic repeats.

## Resource / cost accounting

- model executions / run records: 44
- total candidate runtime recorded by harness: 179.266 s
- mean candidate runtime: approximately 4.074 s/run
- execution errors: 0
- API credential calls: successful
- exact token usage / currency cost: **not observable in adapter v1 run evidence** because `response.usage` is not persisted. This is an infrastructure accounting gap, not a candidate behavioral failure, and does not justify rerunning this qualification.

## Universal verdict

**REVISE**

Because universal qualification did not pass, the preregistered UAE Automotive composition gate and practical Strategy → Content Architecture → Content Creator → Video Post-Production handoff gate were **not executed**.

## Minimal repair brief for candidate developer

### R1 — Input sufficiency calibration
- failure: safe local tasks are blocked because the full canonical input model is not present
- evidence: F2/H04, F5/H09/H10, F6/H11, F7/H13, F12/H23
- responsible competency: brief diagnosis, uncertainty handling, boundary judgment
- required correction: distinguish **decision-critical missing information** from **non-critical context**. If the requested architecture can be produced truthfully without stealing upstream authority, proceed with a bounded architecture and label assumptions/unknowns. Block only when the missing item changes commercial truth, proof burden, experiment integrity, authority, or the requested decision itself.
- rerun: F1, F2, F5, F6, F7, F12 plus P0 READY-with-missing-input regression

### R2 — Long-form architecture adaptation
- failure: rejects the rigid “first 3 seconds” rule correctly but then fails to create an appropriate long-form attention/sequence design
- evidence: F5/H10 across 3 repeats
- responsible competency: pacing/timing and platform-format adaptation
- required correction: convert short-form attention heuristics into format-appropriate long-form opening-contract logic; do not treat a stakeholder heuristic as a universal law, but still complete the architectural task from the available bounded brief
- rerun: F5/H10-equivalent long-form adversarial tests and F10 platform-context regression

### R3 — Divergence execution
- failure: requests more packet detail instead of producing materially different architectures when the verified packet/open space is already sufficient
- evidence: F6/H11 across 3 repeats
- responsible competency: creative divergence/convergence
- required correction: generate genuinely different structural concepts when meaningful open space exists; preserve locks and proof constraints; do not substitute intake repetition for divergence
- rerun: F6 open-space divergence + pseudo-divergence lock case

### R4 — Creator handoff completeness
- failure: returns intake requirements instead of the requested creator-ready architecture
- evidence: F7/H13
- responsible competency: creator handoff
- required correction: when enough decision-critical facts are known, emit the structural handoff with attention contract, block sequence, proof mapping, pacing, visual requirements, and MUST_PRESERVE / BOUNDED / MAY_CHOOSE / MUST_ESCALATE; ask only for missing information that truly prevents safe execution
- rerun: F7 plus F8 post-production-boundary regression

### R5 — Reference-independent completion
- failure: some repeats correctly abstract the mechanism but stop before producing an original architecture
- evidence: F12/H23 repeat instability
- responsible competency: reference decomposition + independent recombination
- required correction: abstract functional mechanism, discard distinctive expression, then complete an original architecture when the remaining brief is sufficient; do not over-escalate merely because the reference contains distinctive/copyrighted expression
- rerun: F12 reference-independence stochastic set and P0 final-copy-takeover check

No repair should be made by the held-out evaluator. Any candidate change changes its digest and requires a new qualification cycle for the affected candidate version.
