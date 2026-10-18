# Non-obvious Qualification Mechanisms Audit — 2026-08-24

## Purpose

Extend qualification-infrastructure discovery beyond products marketed as LLM/agent evaluation tools. This audit follows the current Agent Architect requirement to search adjacent professions/mechanisms, prefer evidence over opinion, and optimize resource use without weakening independent held-out evidence.

This document does **not** authorize paid model runs and does **not** replace the existing sealed held-out qualification lifecycle.

## Existing platform boundary

The current Professional Agent Qualification Platform remains the governing lifecycle:

`candidate freeze -> static validation -> no-API preflight -> optional exact-runtime canary -> sealed held-out verification -> scored qualification -> sanitized report -> release verdict`

The question in this audit is narrower: which mechanisms from adjacent fields can strengthen one or more lifecycle stages, lower diagnostic cost, improve failure discovery, or improve validity?

---

## 1. Inspect AI — evaluation runtime / sandbox / replayable execution layer

### Underlying problem

Our platform has evaluator-owned qualification semantics but still needs robust execution machinery for tool-using and long-horizon agents: agent/tool orchestration, sandboxing, logs/traces, retries/resume, execution limits, and external-agent integration.

### Evidence

UK AI Security Institute's open-source Inspect framework supports datasets, agents, tools and scorers; agent evaluations; external agents; Docker and other sandbox backends; evaluation sets with retry/resume; execution limits for time/messages/tokens/cost; tracing; and web-based log inspection.

Primary documentation:
- https://inspect.aisi.org.uk/
- https://inspect.aisi.org.uk/running.html
- https://inspect.aisi.org.uk/agents.html
- https://inspect.aisi.org.uk/extensions-sandboxes.html

### Why it is materially different from DeepEval

DeepEval is primarily attractive as an evaluation/testing library and tracing layer. Inspect is closer to an **agent-evaluation execution substrate**: agent protocol, tool execution, sandboxes, checkpoints/recovery-oriented running controls, and external-agent bridges are first-class.

### Alternative

Keep our current bespoke runners and add DeepEval only for scoring/tracing.

### Risks

- migrating the runner can change timing, concurrency, retries, exception surfaces, state propagation, and tool semantics;
- Inspect's dataset/scorer abstractions must not become a universal profession schema;
- built-in caching/retry/resume must not accidentally reuse evidence in a way that violates a frozen held-out protocol;
- its logs/traces can expose hidden fixtures or grader information if publication boundaries are not explicitly enforced.

### Decision

**PILOT / ADAPT**, not replace.

Pilot Inspect as an optional execution substrate against public/dev fixtures and compare observable semantics against the existing executor. If equivalence is demonstrated, it may replace selected bespoke runner/sandbox plumbing while the repository's freeze, sealed-pack, evaluator ownership, publication, and release-verdict contracts remain authoritative.

Priority: **higher than DeepEval** for tool-capable / long-horizon agent qualification because its execution and sandbox capabilities overlap more directly with our observed infrastructure burden.

---

## 2. Property-based + stateful testing (Hypothesis) — free infrastructure attack surface expansion

### Underlying problem

The Sales incidents showed that hand-authored happy-path preflight tests did not cover combinations of chunk corruption, SHA availability, timeout arithmetic, missing credentials, state transitions, path handling and runner contract mismatches.

### Evidence

Hypothesis generates inputs across declared domains and shrinks failures to a minimal counterexample. Its stateful testing can generate sequences of operations against a state machine rather than only independent values.

Primary documentation:
- https://hypothesis.readthedocs.io/en/latest/
- https://hypothesis.readthedocs.io/en/latest/stateful.html

### High-value qualification applications

Use it against deterministic infrastructure only, for example:

- malformed or incomplete qualification manifests;
- boundary timeout combinations (`inner`, `executor`, `job`);
- reordered/missing/duplicated sealed-pack chunks;
- ciphertext length/digest mismatch combinations;
- candidate history availability / shallow checkout conditions using fixtures;
- unsafe archive paths and extraction edge cases;
- verdict/report state-machine transitions;
- retry/resume state transitions;
- rejected secrets / missing provider metadata;
- incompatible fixture/grader cardinality declarations.

### Cost effect

These tests can run with **zero model/API calls** and can discover combinations that hand-authored regression fixtures may miss.

### Risks

- properties must encode real invariants; a wrong property creates false confidence;
- stochastic generation is not a substitute for frozen professional fixtures;
- stateful exploration can become expensive in CI if bounds are not controlled.

### Decision

**ADOPT for qualification-platform deterministic infrastructure.**

This is the strongest immediate non-obvious mechanism found because it directly addresses our historical failure class while consuming no model quota.

---

## 3. Mutation testing (mutmut) — test the tests

### Underlying problem

A deterministic regression suite can be green while being too weak to detect meaningful defects in preflight, scope gates, report validation or verdict enforcement.

### Evidence

`mutmut` systematically introduces small source-code mutations and checks whether the existing test suite detects them. It supports incremental execution and targeted mutation scopes.

Primary documentation:
- https://mutmut.readthedocs.io/en/latest/
- https://github.com/boxed/mutmut

### Qualification applications

Mutate deterministic platform code to verify that tests fail when, for example:

- `<=` becomes `<` in timeout boundaries;
- a mismatch check is bypassed;
- fail-closed changes to fail-open;
- verdict enforcement is inverted;
- a report-presence condition is removed;
- digest/cardinality checks are weakened.

### Cost effect

For deterministic infrastructure tests, model cost is **zero**. The cost is CI CPU/time.

### Risks

- do not treat mutation score as professional-agent quality;
- mutating agent prompts/skills would require model calls and changes the construct; that is not the initial use case;
- equivalent mutants can create noise.

### Decision

**PILOT**, scoped to `qualification-platform` deterministic Python modules.

Use mutation testing as a meta-evaluation of the platform's regression suite, not as a release gate for professional agents unless calibrated later.

---

## 4. HTTP record/replay (VCR.py pattern) — eliminate repeated provider calls during infrastructure debugging

### Underlying problem

Historically, API calls were repurchased while diagnosing plumbing failures after the provider boundary: parsing, timeout mapping, report generation, retry logic, error taxonomy and artifact publication.

### Evidence

VCR.py records HTTP interactions on the first live run and replays them from local cassettes on subsequent test runs. Replay-only mode can ensure no new network request is made.

Primary documentation:
- https://github.com/kevin1024/vcrpy
- https://vcrpy.readthedocs.io/

### Valid use

After a deliberately captured **public/dev non-held-out** provider interaction, replay it to test:

- response parsing;
- SDK adapter behavior outside cryptographic/TLS details;
- report construction;
- error classification;
- deterministic post-call state transitions;
- selected retry/termination plumbing.

### Critical boundary

A replayed response is **never fresh professional evidence** and must never count toward a held-out release PASS. Hidden fixture prompts, expected answers, secrets and sensitive headers must not be recorded into reusable cassettes.

### Cost effect

Potentially removes most repeated paid calls from debugging code **after** an already-observed provider interaction.

### Risks

- stale recordings conceal provider/API drift;
- sensitive data leakage into cassette files;
- replay cannot prove current model availability or current behavior;
- streaming/tool-call protocols may require careful matching and sanitization.

### Decision

**PILOT for development/repair only**, with a hard policy boundary excluding release evidence and hidden qualification cases.

---

## 5. Fault injection / chaos testing (Toxiproxy) — prove timeout, retry and resume behavior without spending on model quality

### Underlying problem

Timeout mismatch and interrupted execution were observed infrastructure failure modes. Happy-path live provider calls do not prove recovery or termination behavior under latency, dropped connections or partial network failure.

### Evidence

Shopify's Toxiproxy is designed for deterministic/randomized manipulation of network conditions in tests and CI. It can inject latency, timeouts, connection outages, bandwidth constraints and related faults.

Primary source:
- https://github.com/Shopify/toxiproxy

### Qualification applications

Between a local test executor and a stub/replay provider endpoint, inject:

- latency exceeding nested timeout boundaries;
- connection reset;
- slow close;
- temporary outage;
- partial/unavailable service conditions.

Verify bounded retry, failure classification, checkpoint preservation, sanitized-report behavior and termination semantics.

### Cost effect

Can exercise many reliability cases with **zero live model calls** when paired with a stub or replay endpoint.

### Risks

- network fault simulation is not provider semantic simulation;
- fault models must correspond to plausible runtime failures;
- do not overfit infrastructure to one proxy's behavior.

### Decision

**PILOT for runtime-contract reliability tests** once record/replay or a realistic local stub exists.

---

## 6. Psychometrics / professional assessment design — improve validity, not merely automation

### Underlying problem

A technically flawless runner can still produce a bad qualification if fixtures under-sample the profession, graders are inconsistent, thresholds are arbitrary, or the test teaches to the benchmark rather than measuring the construct.

### Evidence

The *Standards for Educational and Psychological Testing* are jointly produced by AERA, APA and NCME and are a recognized authority for test validity, reliability and assessment practice.

Primary source:
- https://ncme.org/resources/books/testing-standards/

### Qualification applications

Add explicit assessment-science checks to profession qualifications:

- construct representation / underrepresentation;
- construct-irrelevant variance;
- rater/grader agreement where judgment is subjective;
- calibration evidence for LLM judges against professional judgments;
- item/family coverage relative to competency claims;
- threshold rationale;
- repeated-trial reliability where stochasticity matters;
- evidence that a PASS predicts acceptable target-job behavior rather than benchmark-specific proficiency.

### Cost effect

This does not automatically lower API cost. It can **prevent wasting paid runs on invalid tests**, which is a higher-order resource saving.

### Decision

**ADOPT as evaluation-design discipline**, not as a software dependency.

This is an expert-gap repair: current architecture already addresses construct validity conceptually, but professional assessment science should be treated as an explicit source discipline when designing/calibrating qualification suites.

---

## 7. Mechanisms not yet admitted

### Metamorphic testing

Potentially useful when no exact oracle exists: transform a fixture in a way that should preserve or predictably change the result. This could multiply public/dev coverage from a small set of seed scenarios. However, adoption is deferred until a sufficiently authoritative evidence review and profession-specific valid metamorphic relations are defined. Bad relations would test the transformation author's assumptions rather than professional competence.

### Differential testing

Potentially useful for comparing executor implementations or graders against a trusted reference. It does not establish correctness by itself when both implementations may share the same error. Keep as a secondary mechanism, not a source of truth.

### Formal/model checking

Potentially useful for small deterministic state machines (release verdict, retry states, authorization gates), but likely disproportionate for current scope unless property/stateful tests reveal state-space complexity that justifies it.

---

## Updated priority stack

### Priority A — zero-paid-call infrastructure strengthening

1. **Hypothesis property/stateful tests — ADOPT.**
2. **Mutation testing of deterministic qualification-platform modules — PILOT.**
3. **Record/replay development harness — PILOT.**
4. **Fault injection around executor/provider boundary — PILOT after replay/stub substrate exists.**

These mechanisms attack the exact class of failures that previously consumed paid qualification attempts while requiring no professional-agent model calls.

### Priority B — agent execution substrate

5. **Inspect AI — PILOT before DeepEval as the higher-fit execution/sandbox candidate.**
6. **DeepEval — retain as a narrower scoring/tracing candidate if Inspect does not cover the required adapter use cases cleanly.**

### Priority C — evaluation validity

7. **Psychometric/assessment-science calibration — ADOPT as design discipline.**
8. Promptfoo remains a scoped security/adversarial candidate where the threat model requires it.

### Defer

Braintrust / Confident AI remain convenience/hosted-platform candidates and should not be added until a concrete missing capability justifies operational/vendor cost.

---

## Proposed experiments before implementation

All experiments below are zero-paid-call unless explicitly changed by a later budget gate.

### Experiment 1 — property-based preflight attack

Choose 3 deterministic platform modules with the highest incident relevance. Encode invariants and generate malformed/boundary inputs. Success criterion: discovers at least one previously untested edge condition or demonstrates materially broader invariant coverage with bounded CI cost.

### Experiment 2 — mutation adequacy

Run mutation testing against the same modules. Success criterion: critical fail-closed, digest, timeout, report and verdict mutations are killed by the existing/augmented tests. Surviving material mutants become test-gap evidence.

### Experiment 3 — replay debugging

Capture one sanitized public/dev provider response or use a synthetic equivalent, then exercise executor post-call/report/error paths repeatedly with network disabled. Success criterion: deterministic reproduction of plumbing behavior with zero provider calls and no secret/held-out leakage.

### Experiment 4 — Inspect adapter equivalence

Run a public/dev fixture through current executor and an Inspect adapter with no paid model requirement (stub/local test model where possible). Compare tool/state/transcript/error/termination/report semantics. Only if equivalent enough should a real provider canary ever be considered.

### Experiment 5 — reliability fault injection

Using local stub/replay endpoint, inject timeout/reset/latency and verify existing failure taxonomy, bounded retry, checkpoint/report behavior. No scored qualification call is eligible.

---

## Expert-gap discovery

**What would a strong practitioner of this profession notice is missing, even though the user does not know to ask for it?**

A strong evaluation/reliability practitioner would notice that the previous search over-focused on tools that evaluate model outputs. The largest historical waste came from **qualification infrastructure faults before or around the model call**, so the highest-value mechanisms are often classic testing/reliability tools rather than LLM-eval products.

They would also distinguish three different quality questions that should not be collapsed:

1. Does the qualification platform itself fail closed and behave correctly?
2. Does the execution substrate faithfully expose the candidate's behavior?
3. Does the qualification suite validly measure professional competence?

Each requires different evidence and often different tools.

## Red-team

### Senior ML evaluator

Criticism: replay, fuzzing and mutation tests can create the illusion of evaluation rigor while proving nothing about professional competence.

Repair: explicitly confine these mechanisms to infrastructure/meta-evaluation and preserve fresh sealed held-out professional release evidence.

### Reliability/test engineer

Criticism: current hand-authored preflight regressions are likely underexploring combinatorial failure states.

Repair: adopt property/stateful testing and mutation adequacy checks before adding more hosted LLM-eval infrastructure.

### Psychometrician / assessment designer

Criticism: a sophisticated runner cannot rescue a test with weak construct validity, unstable grading or unjustified thresholds.

Repair: make assessment validity/calibration an explicit design discipline and evidence source.

### Cost/release owner

Criticism: paying for more observability SaaS while deterministic test gaps remain is backwards prioritization.

Repair: zero-paid-call property/mutation/replay/fault-injection experiments precede any new paid or hosted integration.

---

## Decision summary

The wide search changes the earlier tooling priority.

The highest immediate leverage is **not** another LLM-eval SaaS. It is:

`property/stateful testing + mutation testing + replay + fault injection`

for the qualification infrastructure, plus a serious **Inspect AI pilot** for the execution/sandbox layer and explicit **assessment-science calibration** for qualification validity.

The existing Agent Architect qualification lifecycle remains the authority. External mechanisms are admitted only where they strengthen a specific layer without weakening freeze, independence, held-out secrecy, evaluator ownership or release evidence.
