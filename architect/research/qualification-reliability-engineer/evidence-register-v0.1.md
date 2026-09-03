# Qualification Reliability Engineer — evidence register v0.1

Status: Architect research artifact. Not a SKILL.
Issue: #265
Date checked: 2026-09-03

## Evidence policy

Material professional claims use primary/authoritative sources where available plus direct repository incidents. Volatile provider behavior remains LIVE_RESEARCH at runtime.

| ID | Claim / decision consumed | Source | Evidence type | Freshness / scope | Decision |
|---|---|---|---|---|---|
| E01 | Harness/environment/setup materially affect evaluation result and must be reported | OpenAI, *A shared playbook for trustworthy third party evaluations*, 2026-05-29, https://openai.com/index/trustworthy-third-party-evaluations-foundations/ | Primary developer guidance | Current 2026 frontier/agentic eval guidance | SUPPORTS separate harness-reliability ownership |
| E02 | Evaluation budgets should include turns, tokens, attempts/retries, wall-clock and inference cost | Same OpenAI source | Primary developer guidance | Current 2026 | SUPPORTS QR-08 budget/accounting |
| E03 | Validity checks and tested-system/harness details are necessary to interpret claims | Same OpenAI source | Primary developer guidance | Current 2026 | SUPPORTS QR-01/QR-10 |
| E04 | AI evaluation is measurement science requiring tasks/testbeds/tools/metrics/context and limitations | NIST AI Measurement and Evaluation, https://www.nist.gov/ai-measurement-and-evaluation | Government measurement authority | Stable principle; page current | SUPPORTS measurement-validity boundary |
| E05 | AI TEVV should be customized to explicit objectives and contexts | NIST TEVV-Athlon initial public draft, Aug 2026, https://www.nist.gov/artificial-intelligence/ai-research/tevv-athlon-framework-evaluating-ai-systems | Government draft framework | Fresh; draft, not final standard | SUPPORTS no universal one-size-fits-all reliability checklist |
| E06 | Test sets, metrics and TEVV tool details should be documented; reliable measurement depends on measurement process | NIST AI RMF Measure Playbook, https://airc.nist.gov/airmf-resources/playbook/measure/ | Government guidance | Current | SUPPORTS readiness/run artifacts |
| E07 | Reliability confidence is established by testing; system/integration/configuration tests cover different uncertainties | Google SRE, *Testing for Reliability*, https://sre.google/sre-book/testing-reliability/ | Established SRE professional literature | Stable | SUPPORTS deterministic + system/live evidence layering |
| E08 | Passing tests do not prove reliability absolutely; failing tests demonstrate absent reliability and realistic probes matter | Same Google SRE source | Established SRE practice | Stable | SUPPORTS conservative readiness claims |
| E09 | Canary should be small, representative and attributable; testing cannot perfectly reproduce production | Google SRE Workbook, *Canarying Releases*, https://sre.google/workbook/canarying-releases/ | Established SRE practice | Stable | SUPPORTS QR-06 representative canary judgment |
| E10 | Long reasoning can exceed ordinary HTTP connection lifetime; Gemini supports background Interactions/polling | Google Gemini API, *Background execution*, https://ai.google.dev/gemini-api/docs/background-execution | Current provider documentation | VOLATILE; checked 2026-09-03 | SUPPORTS transport live-research and provider-supported route |
| E11 | Recent Visual v0.5 final retry created no completed candidate cases/model passes and no judge calls; terminal provider-transport failure | Repo issue #256 comment 5522420833 / run 33729878083 | Direct repository incident | Exact 2026-09-03 incident | SUPPORTS infrastructure vs professional-result separation |
| E12 | Visual first v0.5 live run encountered post-create background retrieval HTTP 400; one bounded repair was attempted | PR #258 + issue #256 comment 5522383886 | Direct repository incident | Exact 2026-09-03 | SUPPORTS need for live-path proof beyond deterministic regression |
| E13 | Issue #129 places generic platform in maintenance mode and defines reopen criteria | Repository governance, issue #129 + `qualification-stop-loss.md` | Internal authoritative governance | Current | CONSTRAINS QR-13/QR-16 |
| E14 | Repository qualification platform already owns deterministic preflight, pack/runtime/report controls | `architect/evaluation/qualification-platform/README.md` | Internal implementation contract | Current | REUSE rather than build new platform |
| E15 | Historical Sales qualification exposed distributed timeout/runtime/path/import/configuration defects | Repository qualification platform incident history and merged PRs #57/#68/#117/#119/#123/#125 | Direct repository incidents | Historical but directly relevant | SUPPORTS cross-profession recurrence and generic-control value |

## Important evidence conflicts / limits

### Deterministic tests vs live proof
Google SRE supports extensive testing but explicitly recognizes that test environments differ from production. Repository evidence reinforces this: deterministic background-transport regressions passed while the real Visual path still failed. Therefore neither `all local tests pass` nor `one live call worked` is sufficient universally. Evidence layer must match the claim.

### New professional core vs software-only enforcement
Most mechanical failure modes can and should be enforced by code. However OpenAI/NIST/SRE evidence leaves judgment-heavy questions: what claim the evaluation supports, whether the harness elicits the relevant behavior, whether canary signals are representative, whether a runtime change alters comparability, and how much live evidence is necessary. Therefore a software-only guard is insufficient as the entire professional system.

### Provider documentation vs observed provider behavior
Provider docs describe intended contracts; live API behavior may diverge due to versioning, rollout, undocumented constraints or local misuse. Treat provider docs as authoritative contract evidence, not proof that the exact caller implementation works. The role must discriminate local defect from provider incompatibility.

## Knowledge packaging classification

### EMBED_CORE
- harness is part of evaluation validity;
- evidence-layer selection logic;
- deterministic-before-paid principle when valid;
- idempotency/ambiguous-create caution;
- canary representativeness principle;
- infrastructure/professional result separation;
- stop-loss semantics.

### PROCEDURAL_MODULE
- readiness review;
- fault-injection design;
- live incident diagnosis;
- budget/accounting;
- regression closure.

### REFERENCE_MODULE
- repository failure taxonomy;
- qualification platform contracts;
- sanitized historical incidents.

### LIVE_RESEARCH
- provider endpoints/API revisions;
- supported models/features;
- retention/storage semantics;
- quota/rate limits;
- current pricing/credits where cost decision depends on them.

### TOOL_BACKED
- Git/workflow/code inspection;
- CI logs/artifacts;
- deterministic validators;
- fault-injection tests;
- run accounting.

## Evidence still needed before candidate freeze

1. Current official guidance on idempotency/retry semantics for each provider route intended for qualification use.
2. A portable definition of canary equivalence dimensions, validated against at least two different provider/runtime mechanisms.
3. Concrete readiness-report schema tested on historical incidents.
4. Evidence that the proposed deterministic guard catches representative high-cost escaped defects without generating excessive false blocks.
5. Independent review of boundary between Reliability Engineer and Independent Evaluator for measurement-validity questions.
