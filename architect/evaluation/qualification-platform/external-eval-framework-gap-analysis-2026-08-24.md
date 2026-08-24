# External Agent Eval Framework Gap Analysis — 2026-08-24

Status: evidence-based architecture review. No external framework is approved as a replacement for the qualification platform. No paid scored run was authorized by this review.

## Question

Can DeepEval, Promptfoo, Braintrust, or related agent-evaluation products materially improve the current Professional Agent Qualification Platform while preserving independent held-out qualification, frozen-candidate integrity, sealed fixtures, profession-specific construct validity, deterministic grading where possible, and Resource & Cost Engineering controls?

## Existing qualification contract that must be preserved

The current platform is already deliberately hybrid. Generic infrastructure owns candidate freeze/digest verification, runtime and timeout contracts, sealed-pack reconstruction and integrity, static/no-API gates, optional exact-runtime canary, sanitized reporting, artifact publication, release-verdict enforcement, and infrastructure failure classification. Evaluators continue to own profession-specific constructs, fixtures, adversarial cases, grader calibration, hard-fail policy, state/tool semantics, authority boundaries, and repeated-trial requirements.

Critical behavioral evidence still requires the chain:

`claim -> executable fixture -> observable actions/state -> grader/verifier -> frozen threshold -> run record`

A framework that offers tracing, datasets, scores, or CI integration does not by itself prove session isolation, persistent-state correctness, checkpoint sufficiency, side-effect safety, capability loading, hidden-fixture integrity, construct validity, or release independence.

## Live evidence checked

### DeepEval

Official DeepEval documentation shows:
- agent evaluations can run end-to-end and at component level using traces/spans;
- agent/tool/retriever/sub-agent execution can be instrumented and inspected;
- it integrates with pytest-style unit testing and CI/CD via `deepeval test run`;
- repeated test execution is supported;
- trajectory and tool-use evaluation are first-class concepts;
- cloud storage/inspection through Confident AI is optional for many local workflows.

This is real overlap with our current execution/diagnostic layer, not with our freeze/sealing/release-control plane.

Decision: **ADAPT / PILOT** as an internal development/regression execution and trace adapter. Do not make DeepEval's default metrics, dataset model, cloud experiment state, or official-run concept authoritative for release qualification.

Important cost constraint: an LLM-based task-completion/trajectory metric can add judge calls. Therefore DeepEval must not be assumed to reduce API spend. A first pilot must use only existing deterministic fixtures/graders and tracing, with zero additional judge calls, then measure whether it reduces engineering/debugging time and duplicated harness code.

### Promptfoo

Official Promptfoo documentation shows:
- local/self-hosted open-source evaluation and red teaming;
- CI/CD integration;
- dynamic adversarial generation across prompt injection, poisoning, excessive agency, privilege/access and other agent-security classes;
- a Community tier with red-team probe allowance, while some dynamic generation/grading requires inference.

This directly overlaps our security/adversarial-development needs, but generated attacks are not automatically independent held-out evidence. If candidate developers see or tune against generated probes, those probes become development/regression evidence.

Decision: **EXTEND / PILOT LATER** as an adversarial-case generator and security regression tool. Fresh release-held-out attacks must remain evaluator-owned and sealed after candidate freeze, or be generated inside an evaluator-controlled sealed process that prevents leakage and freezes the resulting pack before scored execution.

### Braintrust

Official Braintrust material shows strong experiment management, tracing, scoring, CI/CD release gates, cost/latency visibility, and PR-oriented workflows. Its current Starter offering also includes limited free processed data/scores/model credits and short data retention, with paid tiers adding more capacity and controls.

Those strengths target observability and workflow UX. They do not remove our need for candidate freeze/digest binding, sealed hidden transport, evaluator-owned scope gates, deterministic preflight, sanitized publication boundaries, or independent profession-specific graders. Default cloud use would also introduce another data-retention/credential/hidden-trace boundary that must be explicitly validated before any held-out material is uploaded.

Decision: **DEFER** for the release path. Reconsider only if measured operator/debugging burden shows a material observability gap that DeepEval/local artifacts cannot satisfy. Hidden held-out payloads must not be exported to a third-party service merely for UI convenience.

### SWE-bench / E2B class tools

A coding benchmark or generic code sandbox is not a general replacement for professional-agent qualification. Sandboxed code execution becomes relevant only for agents whose claimed competence requires executing untrusted code, shell commands, repositories, browsers, or comparable environments.

Decision: **CONDITIONAL CAPABILITY**, not baseline qualification infrastructure.

## Architecture decision

Keep the current qualification platform as the **control plane**:

`candidate freeze -> scope/cost gate -> static preflight -> sealed preflight -> exact runtime -> scored execution -> sanitized report -> release verdict`

Allow pluggable **measurement/execution adapters** beneath that contract:

`qualification manifest -> candidate adapter -> normalized observable trace -> mechanical/environment grader -> optional calibrated semantic grader -> sanitized run record`

An external framework may implement tracing, test iteration, red-team generation, or experiment visualization, but it must not silently redefine the qualification construct, thresholds, hidden-data boundary, release semantics, or failure taxonomy.

## First pilot — zero additional scored API spend

Pilot DeepEval only on a **public development/regression fixture set**, never on a fresh held-out pack.

Requirements:
1. Same frozen/public candidate and same fixtures as the existing runner.
2. Existing deterministic/mechanical grader remains authoritative.
3. DeepEval is used only for trace/span capture and test orchestration; no LLM judge metric in phase 1.
4. No Confident AI/cloud upload of candidate-private or held-out payloads.
5. Capture current and pilot values for provider calls, tokens, CI wall time, dependency/setup time, trace completeness, failure-localization quality, and human debugging effort.
6. Verify that tool calls, state mutations, termination reason and any side effects required by the current behavioral harness remain externally observable.
7. Map every failure back to the existing qualification failure taxonomy; framework-specific success must never override a platform failure.

Pilot acceptance requires all of:
- no loss of deterministic verdict fidelity;
- no hidden-data or telemetry leakage;
- zero extra model calls in phase 1;
- improved trace completeness or materially lower harness/debugging burden;
- reproducible local/CI run artifacts;
- pinned framework/runtime version in the evidence record;
- clean removal path with no candidate-format lock-in.

If these conditions are not met, retain the bespoke runner for release qualification.

## Promptfoo follow-up pilot

Only after the DeepEval measurement pilot, run Promptfoo against a public security-development target. Generated attacks become public regression material, not release-held-out evidence. Measure unique vulnerability coverage, false positives, duplicate cases, provider/probe consumption, and whether professionally material attacks are discovered beyond the existing evaluator-authored set.

## Cost conclusion

No evidence currently supports a claim that adopting one of these frameworks will automatically lower API cost. The defensible cost hypothesis is narrower:

- deterministic-first grading can prevent unnecessary LLM judge calls;
- better tracing may reduce failed diagnostic reruns and human debugging time;
- Promptfoo may lower adversarial-case authoring effort;
- Braintrust may lower operator/analysis time but adds platform/data cost and governance surface;
- semantic metrics can increase model calls if used indiscriminately.

Therefore any adoption must be justified by measured **total constrained resource use**, not vendor pricing or nominally free tiers.

## Professional gap discovery

Question: `What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?`

Material gaps identified and incorporated:
- **construct validity:** framework metrics cannot substitute for profession-specific competency evidence;
- **grader calibration/drift:** built-in semantic scores must be calibrated against expert or mechanical reference judgments before release use;
- **trace completeness:** a tracing SDK observes only what is instrumented; persistent state, checkpoint sufficiency and external side effects still require explicit harness exposure;
- **hidden-data leakage:** tracing, cloud dashboards, caches and telemetry are additional exfiltration surfaces for held-out fixtures and expected answers;
- **supply-chain/version drift:** the framework and actions become part of the evaluated environment and must be version-pinned/captured;
- **framework lock-in:** run evidence should use a neutral normalized event/run-record contract so release claims remain portable;
- **cost multiplication:** candidate inference plus judge inference plus red-team generation can silently multiply calls;
- **independence contamination:** generated adversarial cases lose held-out status once exposed during development.

## Red-team review

### Senior evaluator / practitioner

Criticism: adopting a popular eval framework can create a false sense of rigor while replacing construct-valid profession tests with generic task-completion scores.

Repair: platform construct ownership, mechanical graders, hard-fail rules and evaluator calibration remain authoritative.

### Competency assessor / educator

Criticism: tool-use and trajectory metrics may show procedural neatness without establishing real professional competence.

Repair: external metrics are diagnostic unless explicitly mapped through `competency -> observable evidence -> eliciting task -> calibrated grader`.

### Hiring/operator perspective

Criticism: a better dashboard is not valuable if qualification lead time, false releases, debugging effort and operational failure detection do not improve.

Repair: require measured pilot deltas in debugging effort, trace completeness, run reliability and total resource consumption before adoption.

### Security / reliability perspective

Criticism: cloud traces can leak hidden qualification content; dependencies/actions can change; automatic CI evals can create unapproved provider spend.

Repair: local-first pilot, version pinning, no hidden cloud export, explicit paid-stage authorization, and preservation of the existing fail-closed lifecycle.

## Incidental control defect discovered during this review

The repository currently contains `.github/workflows/analytics-v0-3-decision-sufficiency-heldout-gemini.yml` with `push` and `pull_request` triggers and a provider-backed Gemini scored job. The current paid-execution policy says provider-paid scored execution must require explicit manual authorization, and the current exception registry lists only the RCE semantic smoke workflow and Sales 0.3 qualification workflow. This Analytics workflow therefore requires a separate policy-compliance repair or explicit evidence that the job is non-paid/non-generative; from its current workflow body it appears generative.

This defect is independent of the DeepEval/Promptfoo/Braintrust decision and should be repaired without changing frozen professional evidence.

## Decision summary

- Current Professional Agent Qualification Platform: **KEEP as authoritative control plane**.
- DeepEval: **ADAPT / zero-extra-call public regression pilot**.
- Promptfoo: **EXTEND later for adversarial development/security regression**.
- Braintrust: **DEFER**; optional future observability layer, not release authority.
- SWE-bench/E2B class tooling: **conditional by profession/runtime need**.
- Full platform replacement: **REJECT** because it weakens or fails to prove existing freeze, sealing, independence, construct-validity, state/side-effect and release-control requirements.

## Sources checked 2026-08-24

Repository:
- `architect/SKILL.md`
- `architect/methodology/eval-integrity-and-regression.md`
- `architect/methodology/resource-cost-engineering.md`
- `architect/evaluation/behavioral-validation-harness.md`
- `architect/evaluation/qualification-platform/README.md`
- `architect/evaluation/qualification-platform/qualification-manifest.schema.json`
- `architect/evaluation/qualification-platform/qualification-scope-policy.md`
- `architect/evaluation/qualification-platform/paid-execution-policy.md`
- `architect/evaluation/qualification-platform/paid-workflow-exceptions.json`

External primary documentation:
- DeepEval Agent Evaluation Quickstart: https://deepeval.com/docs/getting-started-agents
- DeepEval LLM Tracing: https://deepeval.com/docs/evaluation-llm-tracing
- Promptfoo GitHub Actions: https://www.promptfoo.dev/docs/integrations/github-action/
- Promptfoo Red Team Quickstart: https://www.promptfoo.dev/docs/red-team/quickstart/
- Promptfoo Pricing: https://www.promptfoo.dev/pricing/
- Braintrust agent evaluation: https://www.braintrust.dev/learn/ai-agent-evaluation/v0
- Braintrust CI/CD: https://www.braintrust.dev/learn/ci-cd/v0
- Braintrust pricing: https://www.braintrust.dev/pricing
