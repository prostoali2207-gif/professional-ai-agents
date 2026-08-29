# Visual Design / Art Direction 0.1.0 — exact R3 corpus pre-score calibration preregistration

Status: **PRE-SCORE / candidate execution forbidden**  
Issue: #158

## Immutable inputs

Frozen professional candidate remains unchanged and unobserved:
- commit `e8be839b02f181193afe076839c6ae94fb477a9b`
- candidate `SKILL.md` blob `9d251d97a84e16ade91c8ced07425f9208f9f900`
- professional-model blob `bbea595e299445cf79f798ed1e86eecd0b53cd50`
- candidate calls before this calibration: `0`

The only eligible held-out corpus is the first successful sealed R3 pack:
- source run: `33265201398`
- source head: `af43f2d12187e1825c596239a7313fd8b7e5da63`
- GitHub artifact id: `9718569692`
- artifact name: `visual-design-art-direction-v0-1-encrypted-heldout-pack-r3`
- artifact digest: `sha256:04edc998022ae2ec524cec2e366c2644e46964c052030c5faddec320c7e94f1b`
- semantic cycle id inside the pack: `visual-design-art-direction-0.1.0-independent-2026-08-29-r3-semantic`
- required cardinality: 20 cases / 10 families / 5 declared contrastive pairs

No alternate, regenerated, repaired, edited, substituted or cherry-picked held-out content is eligible in this qualification cycle.

## Frozen release-judge calibration and policy

Authoritative release-judge calibration remains run `33262394565` = `CALIBRATION_PASS`, with frozen calibration ciphertext SHA256 `7ff98e8a9eb8bb82edb0c0a8ebde78553dd40f08487b1eb85f0412ac291ddeb1`.

Judge identities/configuration remain:
- Gemini `gemini-3.5-flash-lite`
- Groq `openai/gpt-oss-120b`
- blind A/B comparative judgment
- Groq minimum interval 60 seconds
- one bounded transient 5xx retry per provider request, matching the already-qualified calibration runtime class

Frozen calibration pass thresholds remain unchanged:
- each judge expected-winner rate >= `0.80`
- combined expected-winner rate >= `0.90`
- pair disagreement rate <= `0.25`

FULL scope, professional criteria, P0 hard-fails, family requirements, judge policy, retry/stop policy and later release thresholds are unchanged.

## Purpose of this corpus-specific calibration

The exact R3 pack was authored and construct-audited after the general release judges had already calibrated. Before any candidate outcome is visible, perform a blind corpus-specific discrimination check to establish that the frozen judges can validly distinguish practitioner-strength work from the competent-generic baseline on the exact sealed R3 construct.

This stage is evaluator calibration only. It does not score or invoke the frozen candidate and cannot produce a professional PASS/REVISE/FAIL.

## Calibration procedure

For each of the 20 exact sealed R3 cases, without changing any case field:

1. Use the case's sealed `brief`, `context`, `constraints`, `professional_criteria` and optional `p0_guardrail` to generate one **ephemeral practitioner anchor** with Gemini `gemini-3.5-flash-lite`.
2. The anchor must answer the supplied professional situation directly, satisfy all stated constraints, remain within Visual Design / Art Direction authority, and avoid every preregistered P0 behavior. It is temporary evaluator material, not a replacement fixture and not persisted publicly.
3. Groq `openai/gpt-oss-120b` performs an independent anchor-validity audit against the same sealed case facts. The audit may only accept/reject; it may not rewrite the hidden case, baseline, criteria or anchor.
4. If the anchor is rejected, the calibration stage stops `CALIBRATION_NOT_EXECUTABLE_ANCHOR_VALIDITY`. It does not regenerate or repair that case/anchor to seek a passing calibration result.
5. For an accepted anchor, compare it blindly against the case's already-sealed `competent_generic_baseline`. A/B position is deterministic from calibration cycle id + case id and is hidden from judges.
6. Both frozen judges independently choose the professionally stronger output. No scalar grading or post-hoc adjudication is introduced.
7. Expected winner is the independently accepted practitioner anchor. Calibration rates/disagreement are computed over all 20 exact cases.

The anchor is calibration evidence derived from an immutable fixture, not a new held-out fixture. The sealed R3 fixture identity and candidate-visible fields remain unchanged.

## Independence and leakage controls

Before `CALIBRATION_PASS`, forbidden:
- any candidate execution, candidate-output inspection or candidate scoring;
- publishing hidden R3 case text, professional criteria, P0 triggers, baselines or practitioner anchors;
- editing/replacing/regenerating R3 cases;
- changing judges, models, thresholds, FULL scope, P0, family semantics or professional criteria after observing calibration outcomes;
- rerunning a completed `CALIBRATION_FAIL` merely to seek a better stochastic outcome.

Only public-safe aggregate/counter evidence may be uploaded: exact artifact binding, item/family counts, judge identities, per-judge expected-winner rates, combined rate, disagreement rate, provider call counts, candidate call count, failure class and status.

## Infrastructure / retry / resume policy

Before provider calls, deterministic no-secret checks must prove:
- runner compiles;
- exact R3 source run/head/artifact id/name/digest constants are bound;
- candidate executor/output paths are absent;
- pass thresholds and judge identities match this preregistration;
- hidden content is not printed.

Metered execution is explicit issue-command/manual only; it may not run automatically on pull request or push.

Provider/transport/quota failures remain evaluator infrastructure failures. Each individual provider request may use at most the existing single transient 5xx retry. The runner checkpoints after every completed anchor audit and judge decision using only opaque case IDs and provider outcomes. If a workflow is interrupted for infrastructure reasons, a resume run may continue only the missing calls from that exact checkpoint and exact R3 artifact. Completed calls are not repeated unless their result was never durably checkpointed.

A completed `CALIBRATION_FAIL` is terminal for candidate scoring under this configuration. An anchor-validity rejection is `CALIBRATION_NOT_EXECUTABLE_ANCHOR_VALIDITY`, not a candidate failure, and receives no outcome-seeking regeneration.

## Gate

Candidate scoring remains forbidden unless the exact-R3 corpus calibration produces `CALIBRATION_PASS` under the frozen thresholds above.

After `CALIBRATION_PASS`, exact release configuration must be frozen publicly **before any candidate outcome is generated**, binding at minimum: frozen candidate identity, exact R3 artifact identity, authoritative general calibration identity, exact-R3 corpus calibration identity, judge/model configuration, thresholds, P0, FULL scope, family set, retry/resume/stop policy, semantic scoring runtime and mandatory rendered P1–P4 gate.
