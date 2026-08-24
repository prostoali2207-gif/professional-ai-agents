# External Qualification Tooling Gap Analysis — 2026-08-24

## Purpose

Evaluate whether DeepEval / Confident AI, Promptfoo, Braintrust, SWE-bench, or E2B should replace, complement, or be rejected for the current Professional Agent Qualification Platform.

This analysis follows Agent Architect evidence rules and the existing qualification lifecycle. Product claims were checked against current official documentation on 2026-08-24.

## Existing platform invariants that must not be weakened

The repository already requires a hybrid qualification architecture with profession-specific construct ownership and a generic lifecycle:

`candidate freeze -> static validation -> no-API preflight -> optional exact-runtime canary -> sealed held-out verification -> scored qualification -> sanitized report -> release verdict`

The platform also requires fail-closed stages, immutable candidate identity/digests, evaluator-owned sealed transport, explicit runtime contracts, infrastructure/professional failure separation, and manual authorization before any stage that can consume paid provider quota.

Therefore an external tool is acceptable only if it preserves these invariants or is used as a subordinate module behind them.

## Decision matrix

| Tool | Strong evidence-backed capabilities | Gap against our platform | Decision |
|---|---|---|---|
| **DeepEval (OSS)** | Local-first; pytest-style CI evaluation; agent end-to-end, component, tool-use, multi-turn and trajectory evaluation; tracing; custom metrics/models; can run without Confident AI cloud. | Does not natively establish our evaluator-owned freeze/digest/sealed-pack lifecycle, hidden-pack confidentiality contract, release manifest, independent qualification ownership, or paid-run authorization policy. LLM metrics still require separate judge-provider eligibility/calibration decisions. | **ADAPT / PILOT** as an optional execution + trace adapter under the existing qualification platform. Do not make it the qualification authority. |
| **Confident AI** | Cloud reports, regression tracking, tracing/observability, datasets, shared evaluation workflows. Free tier exists but current free limits include 2 seats, 1 project and 5 test runs/week; paid Starter is currently $200/month. | Cloud dependence adds external retention/governance surface; free run limits are restrictive for our qualification queue; does not replace sealed evaluator ownership or release protocol. | **DEFER**. Not justified while local artifacts + GitHub Actions are sufficient. Re-evaluate only if cross-run observability/human annotation becomes a bottleneck. |
| **Promptfoo** | GitHub/CI evals, JSON/JUnit outputs, quality gates, caching, adversarial generation, red-team plugins/strategies, prompt injection/hijacking/excessive-agency and custom policy testing; custom Python/HTTP/executable targets. | Generic red-team generation is not profession-construct validation and must not redefine hidden held-out suites. Generated adversarial probes can consume model quota and must obey our paid gate. | **EXTEND** qualification security evaluation as an optional adversarial/security module, especially for tool-capable agents. Keep profession-specific hard-fails and held-out fixtures evaluator-owned. |
| **Braintrust** | PR eval gates, experiment comparison, tracing, token/cost tracking and hosted reports. Starter currently has $0 platform fee, $10 model credits, 1 GB processed data and 10k scores, with 14-day retention. | Overlaps substantially with existing GitHub Actions + artifact/report layer; hosted score/trace storage creates another dependency and confidentiality surface. Does not supply our sealed independent qualification protocol. | **DEFER / REJECT AS CORE**. Possible later observability UI, not a current infrastructure replacement. |
| **SWE-bench** | Authentic software-engineering benchmark design around repo issues/tests. | Construct is coding-agent performance, not the dominant profession class in this repository. Importing its benchmark structure as universal qualification would create construct invalidity. | **REJECT AS GENERAL PLATFORM**. Consider only for coding-agent specializations. |
| **E2B** | Isolated agent/code sandboxes for executable workloads. | Adds runtime/vendor complexity when no untrusted code execution is required. Does not itself provide professional construct evaluation. | **CONDITIONAL TOOL** only for agents whose valid qualification requires sandboxed code/terminal execution. |

## Evidence

### DeepEval

Official documentation states that DeepEval is open-source and local-first, integrates with pytest-style unit testing, supports CI/CD, and supports end-to-end, trajectory-based and component-level agent evaluation, tracing, tool-use and multi-turn evaluation.

Sources:
- https://deepeval.com/docs/introduction
- https://deepeval.com/docs/getting-started-agents
- https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd
- https://deepeval.com/docs/evaluation-trajectory-based-llm-evals

### Confident AI

Current official pricing lists Free at $0 with 2 users, 1 project and 5 test runs/week, Starter at $200/month, and Team at $2,000/month. Confident AI is optional for DeepEval local execution and adds shared reports, datasets, tracing and observability.

Sources:
- https://www.confident-ai.com/pricing
- https://www.confident-ai.com/docs

### Promptfoo

Official documentation supports GitHub Actions, CI/CD quality gates, cache reuse, JSON/JUnit outputs, adversarial red-team generation, prompt-injection/hijacking/security testing, and custom application targets through Python, HTTP, JavaScript or executable adapters.

Sources:
- https://www.promptfoo.dev/docs/integrations/github-action/
- https://www.promptfoo.dev/docs/integrations/ci-cd/
- https://www.promptfoo.dev/docs/red-team/configuration/
- https://www.promptfoo.dev/docs/guides/llm-redteaming/

### Braintrust

Official documentation describes PR evaluation gates, experiment comparisons, tracing/cost tracking and hosted eval workflows. Current Starter pricing is $0 platform fee with included limits; Pro is $249/month.

Sources:
- https://www.braintrust.dev/learn/ci-cd/v0
- https://www.braintrust.dev/pricing
- https://www.braintrust.dev/foundations/comparing-experiments

## Architecture decision

Do **not** replace the current qualification platform with a third-party eval framework.

Preferred architecture:

`Agent Architect profession/eval design`
`-> current qualification manifest + freeze/sealed/preflight/budget/release gates`
`-> evaluator-owned runner`
`-> optional DeepEval adapter for tracing/trajectory/component execution`
`-> optional Promptfoo security module for selected threat families`
`-> sanitized artifact/report`
`-> evaluator-owned release verdict`

DeepEval and Promptfoo are subordinate mechanisms, not authorities over construct validity, release scope, hidden fixtures, grader policy, or release verdicts.

## Why not adopt Braintrust/Confident AI now

The strongest current need is not another dashboard. The observed failures were distributed implicit configuration, runtime incompatibility, secrets, checkout depth, timeout arithmetic, sealed transport, and repeated paid diagnostic runs. The existing qualification-platform directly addresses those root causes. Hosted UI platforms mainly improve observability, collaboration and report comparison; they do not eliminate the evaluator-owned transport/runtime/release obligations that caused the incidents.

Adding them now would increase integration surface before proving that the remaining bottleneck is observability rather than execution correctness.

## Smallest discriminating experiment

Before any broad integration, run one **non-release pilot** on a candidate whose existing evaluator fixtures and verdict logic already work.

Pilot constraints:

1. Preserve the exact existing candidate, fixtures, grader and thresholds.
2. Keep sealed pack handling, freeze/digest verification, scope gate, paid authorization and final verdict outside DeepEval.
3. Instrument only the executor path with DeepEval local tracing.
4. Compare old runner vs instrumented runner on the same public/dev fixtures first; no new held-out paid run.
5. Require semantic/result equivalence and verify that tracing exposes useful tool/trajectory evidence without leaking hidden fixture content.
6. Measure additional installation complexity, workflow time, artifact size and any extra model calls.
7. If the adapter adds model-judge calls by default, disable them unless explicitly required by the evaluator.
8. Do not adopt if the same evidence can be obtained deterministically from the current runner at lower complexity.

Only after this pilot passes should a sealed held-out integration be considered.

## Promptfoo admission rule

Promptfoo should not be globally enabled on every candidate. Apply it only when the threat model makes its adversarial families relevant, for example agents that consume untrusted external content, call tools, operate with meaningful authority, or expose RAG/MCP/application endpoints.

Generated probes are development/security evidence. A release claim still requires the evaluator's preregistered held-out security fixtures where mandated.

## Cost implications

Potential savings from these tools are mainly indirect:

- DeepEval can standardize tracing and reduce custom diagnosis work, but does not inherently remove provider calls required by valid qualification.
- Promptfoo caching can avoid repeated identical prompt calls during development, but generated red-team scans can add many calls if not scope-gated.
- Braintrust/Confident AI can centralize reports but introduce hosted-platform usage limits/costs and do not remove model-provider cost for the candidate/judge paths.

Therefore cost reduction should continue to come first from the existing Resource & Cost Engineering controls: deterministic preflight, evidence reuse, targeted regressions, bounded canary, manual paid authorization and one-at-a-time release runs.

## Expert-gap discovery

`What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?`

A strong evaluation-platform engineer would require **adapter-equivalence testing** before trusting a new framework: instrumentation itself can alter timeouts, concurrency, exceptions, state propagation, tool wrappers, serialization and observable trajectory. A new tracing framework must therefore be treated as a runtime change until equivalence is demonstrated.

A security engineer would also require a strict hidden-data boundary: no raw held-out prompt, answer key, grader rubric, secrets or disclosive trace may be uploaded to an external SaaS by default.

A measurement specialist would object to importing built-in LLM metrics as if they were valid professional constructs. Every material metric still needs construct mapping and calibration against evaluator/professional reference judgments.

## Red-team

### Senior practitioner

Criticism: adopting DeepEval because it provides many metrics could create metric-driven false confidence and duplicate runner complexity.

Repair: use it first only for instrumentation/trajectory capture; evaluator-owned metrics remain authoritative unless individually validated.

### Competency assessor / educator

Criticism: generic relevance/completeness/safety metrics may not measure the actual professional competency being qualified.

Repair: preserve `competency -> observable evidence -> eliciting task -> grader/verifier`; built-in metrics are admitted only where construct validity is explicit.

### Hiring/release owner

Criticism: a polished cloud dashboard can make weak evidence look operationally mature.

Repair: release PASS remains tied to frozen held-out evidence and current platform verdict enforcement, not platform UI.

### Reliability engineer

Criticism: adding instrumentation to a working runtime can introduce new failure modes.

Repair: require public/dev adapter-equivalence regression before any sealed run and preserve an escape path to the original executor.

### Security reviewer

Criticism: cloud tracing can leak held-out evaluation content and grader structure.

Repair: local-first default; SaaS export disabled for sealed qualification unless an explicit sanitized-data contract is proven.

## Final decision

- **Keep current qualification-platform as the governing architecture.**
- **Pilot DeepEval locally as an optional executor/tracing adapter, not as a replacement.**
- **Add Promptfoo only as a scoped security/adversarial capability where threat-model evidence requires it.**
- **Do not integrate Braintrust or Confident AI yet.**
- **Do not generalize SWE-bench/E2B beyond coding/sandbox-requiring agents.**

The next implementation task, if approved by repository review, is a zero-paid-call DeepEval adapter-equivalence prototype against public/dev fixtures only.