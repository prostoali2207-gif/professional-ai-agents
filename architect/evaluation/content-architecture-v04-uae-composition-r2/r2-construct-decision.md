# Content Architecture v0.4 — UAE composition r2 construct decision

Status: **CONSTRUCT_INVALID / RETIRED FOR RELEASE EVIDENCE**.

Failure class: `EVALUATOR_CONSTRUCT_FAIL`.

Gate: `content-architecture-v0.4-uae-composition-2026-09-01-r2`

Scored run: `33598479167`

Postmortem run: `33601016054`

## Decision basis

This decision is about evaluator construct validity, not about whether the observed candidate answer was convenient to score.

The frozen professional model separates two constructs:

1. **Public commercial/proof propositions.** CA-04 asks, for every material explicit or implied proposition, whether public-facing use is allowed given source/scope/evidence.
2. **Strategy / experiment locks.** CA-01, CA-06 and CA-10 require approved audience/mechanism/action/destination/tested and controlled variables to be preserved; a crossing change is routed upstream rather than treated as a commercial-evidence claim.

The frozen UAE specialization uses the same separation: unit/offer claims require authoritative business evidence before they become content claims, while the approved funnel role, CTA destination and experiment variable/controls must be preserved unchanged.

The r1 retirement decision explicitly required the replacement gate to grade strategy/CTA/experiment decisions by **explicit lock preservation** rather than by commercial-fact semantics. The r2 preregistration repeated that requirement: strategy, CTA and experiment lock decisions were to be graded by explicit lock preservation, with evidence-basis checks only where provenance is materially part of the commercial-truth/proof construct.

However, the frozen r2 candidate-visible contract and mechanical verifier required a boolean `public_use` value for **every** decision row, including `STRATEGY_LOCK` and `EXPERIMENT_LOCK`, and the hidden expectations mechanically compared that field for those internal lock decisions. This makes one field carry two non-equivalent meanings:

- `public_use` = whether a material proposition may enter public-facing content; versus
- `public_use` = whether an internal strategy/experiment change is allowed while preserving a lock.

Those are not the same professional construct. The latter is already directly represented and mechanically checked by `lock_results[].preserved` and by the professional experiment-integrity assessment.

Therefore a mismatch on `public_use` for an internal strategy/experiment decision is not valid evidence of a Content Architecture professional failure when lock preservation itself is correct.

## Observed evidence

The scored r2 run completed 8 candidate calls and 8 judge calls. The professional judge gave release PASS on every case, aggregate mean `3.0`, and zero judge hard failures. Mechanical hard failures were also zero. The frozen aggregate gate returned `REVISE` only because mechanical case pass rate was `7/8`.

The no-new-model-call postmortem isolated exactly one remaining mechanical mismatch. Its class was `public_use` on an internal strategy/experiment decision; evidence-basis and lock-preservation checks were satisfied. The postmortem correctly did not auto-retire the gate and instead left this construct-validity question for explicit methodology review.

The construct review now resolves that question: the failing field was outside the valid construct for that decision class.

## Integrity decision

Do not:

- reinterpret r2 as PASS;
- reinterpret r2 as a professional REVISE signal against the frozen candidate;
- patch r2 fixtures, expectations, runner, threshold or report after scored calls;
- mutate the universal core or UAE specialization from this result;
- reopen generic qualification-platform engineering.

The r2 gate identity is burned and retained as diagnostic evidence only.

## Stop-loss classification

Under `architect/methodology/qualification-stop-loss.md`, this is a profession-specific `EVALUATOR_CONSTRUCT_FAIL`, not a provider/runtime failure, local execution failure or generic-platform blind spot.

Allowed recovery is one bounded profession-specific evaluator repair. No generic platform work is authorized. If the fresh replacement composition gate encounters another material evaluator/infrastructure defect, stop and perform explicit stop-loss review rather than creating another serial repair chain by default.

## Fresh replacement gate requirement

Create a fresh UAE composition gate with a new identity. Preserve unchanged:

- universal candidate blob `5d440e1bf3e20fbd35c6ab276310a904e36cc06d`;
- UAE specialization blob `7f41c2d1ba40c3b4c59e3eba2fb264c04162c320`;
- professional judge identity unless independently invalidated;
- frozen release thresholds;
- frozen Codex runtime contract.

The replacement contract must separate constructs mechanically:

- `COMMERCIAL_CLAIM`, `UNIT_FACT` and `PROOF_SCOPE` rows may be graded for `public_use`, resolution and materially relevant evidence provenance;
- strategy/CTA/experiment constraints must be graded through explicit lock preservation / allowed-change semantics, without forcing proposition-style `public_use` semantics onto internal lock decisions;
- unsafe unsupported public commercial use and explicit lock breaches remain hard failures;
- free-form architecture quality and boundary judgment remain with the calibrated professional assessor.

Fresh scenarios must be authored from the frozen specialization obligations and preregistered construct, not from candidate answer text.

After a valid UAE composition PASS, the remaining release-critical stage is `PRACTICAL_HANDOFF`. Only after that gate passes may Content Architecture / Content Analyst v0.4 be declared fully QUALIFIED.
