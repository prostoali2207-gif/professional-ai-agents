# Professional Agent Reuse & Landscape Discovery

## Purpose

Prevent Agent Architect from rebuilding professional agents, skills, workflows, tools, datasets, evals, or runtime components that already exist at sufficient quality.

This capability is a mandatory pre-build discipline. It is not a GitHub popularity search and it does not treat a repository name, README claim, star count, model-generated demo, or self-reported benchmark as evidence of professional competence.

The objective is:

`need -> search existing landscape -> qualify candidates -> compare against target profession model -> reuse/adapt/combine/reject/build-missing -> verify`

The default question is not `How do we build this?` but `What already exists, what evidence supports it, and what remains genuinely missing?`

## When it applies

Run this capability before materially designing or implementing an applied professional agent, and again when a major new capability is requested.

Depth scales with:

- expected implementation/research cost;
- availability of mature open-source or vendor ecosystems;
- safety or professional consequence;
- licensing/provenance risk;
- likelihood that existing benchmarks, datasets, tools, or specialist skills already exist;
- volatility of the ecosystem.

For trivial or highly bespoke tasks, a compact search may be sufficient. For common professions or agent capabilities, absence of a credible landscape search is a design defect.

## Search scope

Do not search only for repositories named after the requested profession. Search across several artifact classes:

1. **Complete specialist agents** — end-to-end systems claiming the target professional role.
2. **Professional skill packs** — reusable domain procedures, playbooks, references, prompts, scripts, schemas, and tool bindings.
3. **Workflow/SOP implementations** — explicit professional processes that may be more valuable than the surrounding agent framework.
4. **Domain tools and MCP/tool servers** — authoritative data access, calculators, databases, APIs, automation, retrieval, validation, and execution tools.
5. **Evaluation assets** — benchmarks, work samples, datasets, graders, simulation environments, rubrics, and outcome tests for the profession.
6. **Knowledge/evidence assets** — standards mappings, structured corpora, taxonomies, ontologies, official datasets, and maintained reference collections.
7. **Adjacent specialist systems** — components from neighboring professions that protect critical decisions even if they are not branded as the target role.
8. **General agent infrastructure** — orchestration, memory, tracing, sandboxing, security, retrieval, and cost-control components only when they solve a requirement that should not be rebuilt locally.

Search beyond GitHub when the strongest evidence lives in official documentation, papers, benchmarks, standards bodies, package registries, vendor repositories, or practitioner-maintained resources.

## Candidate discovery strategy

Start from the profession model and competency map, not from repository keywords alone.

For each critical competency, search for:

`profession/competency + agent`

`profession/competency + skill/workflow/SOP`

`profession/competency + benchmark/eval/dataset`

`profession/competency + tool/API/MCP`

`profession/competency + open source/reference implementation`

Also search by outputs and difficult decisions. A strong component may never call itself an `agent`.

Use live research for active ecosystems because repository status, maintenance, licensing, APIs, models, benchmarks, and platform compatibility change.

## Qualification model

A candidate is not accepted because it looks sophisticated. Qualify it on the evidence relevant to its claimed role.

### 1. Professional fidelity

Ask:

- Which real professional tasks does it perform?
- Which competencies are actually encoded?
- Does it model difficult decisions, uncertainty, exceptions, failure/recovery, and professional boundaries?
- Is it merely a role prompt over a general model?
- Are domain procedures traceable to credible professional sources or validated practice?

### 2. Behavioral evidence

Prefer direct evidence over narrative claims:

- executable tests;
- benchmark results with inspectable methodology;
- authentic work samples;
- environment/state verification;
- external or calibrated expert evaluation;
- reproducible examples;
- documented failure cases.

README adjectives, screenshots, model self-reports, and synthetic testimonials are weak evidence.

### 3. Evaluation quality

Determine whether evaluation measures the claimed professional construct rather than generic fluency.

Check:

- task authenticity;
- sample representativeness;
- scoring validity;
- baseline quality;
- leakage/contamination risk;
- reproducibility;
- variance/repeated trials where relevant;
- whether execution/tool/state behavior is observed instead of narrated.

### 4. Evidence and knowledge provenance

Check whether professional claims depend on:

- authoritative primary sources;
- standards/specifications;
- peer-reviewed or strong empirical evidence;
- maintained official datasets;
- transparent practitioner sources;
- unverifiable prompt folklore.

Do not inherit unsupported professional claims merely because they are packaged in open source.

### 5. Engineering quality

Inspect as relevant:

- architecture clarity;
- modularity;
- test coverage;
- observability/tracing;
- deterministic checks;
- error handling;
- retry/termination behavior;
- state/memory handling;
- dependency hygiene;
- portability;
- maintenance activity;
- version assumptions.

### 6. Security and trust

Third-party agent assets are untrusted supply-chain inputs.

Before executing or adopting code, skills, MCP servers, scripts, workflows, or model instructions, inspect:

- permissions and side effects;
- network access;
- secret handling;
- external downloads;
- prompt/tool injection surfaces;
- persistence/memory writes;
- arbitrary command execution;
- dependency provenance;
- install scripts and binary artifacts;
- data exfiltration risk.

Do not execute untrusted third-party code merely to evaluate its README claim. Prefer static inspection and sandboxed/minimal experiments first.

### 7. Licensing and reuse rights

Verify license and artifact-specific restrictions before copying, modifying, distributing, embedding, or deriving from a project.

Record whether the intended use is:

- direct dependency;
- source adaptation;
- conceptual benchmark only;
- evaluation reference;
- prohibited/unclear pending review.

Absence of an explicit license is not permission to copy code or substantial protected content.

### 8. Resource and operational fit

Evaluate total adoption cost, not only implementation effort:

- model/API requirements;
- paid providers;
- quota assumptions;
- compute/latency;
- human review burden;
- CI/deployment complexity;
- maintenance burden;
- vendor lock-in;
- runtime compatibility.

Use `resource-cost-engineering.md` for material trade-offs.

## Coverage matrix

Map qualified candidates against the target competency model.

For each critical competency, classify support as:

- `PROVEN` — credible behavioral/evidence support for the required use;
- `PARTIAL` — useful component but incomplete, weakly validated, or context-limited;
- `CLAIMED` — asserted but not adequately evidenced;
- `ABSENT` — not implemented;
- `INCOMPATIBLE` — conflicts with target constraints, authority, runtime, jurisdiction, safety, or evidence requirements.

Do not score one repository globally and assume every component shares the same quality.

## Decision classes

Every serious candidate should end in one of these states:

### USE AS-IS

Use only when the candidate meets the target requirement, evidence threshold, security/trust constraints, licensing conditions, and operational fit without material redesign.

### ADAPT

Use when the core is strong but requires bounded changes for domain context, runtime, jurisdiction, tools, evidence, safety, evaluation, or UX.

Record exactly what is inherited versus newly engineered.

### COMBINE

Compose multiple candidates when they cover complementary competencies and integration overhead is justified.

Do not create a multi-component system merely because many good repositories exist. Account for coordination, duplicated state, incompatible abstractions, latency, security surface, and maintenance cost.

### BENCHMARK ONLY

Use as a comparison target, source of test cases, architecture contrast, or failure-mode reference when direct reuse is unsuitable.

### REJECT

Reject when evidence, professional fidelity, maintenance, security, licensing, compatibility, or cost is inadequate.

Record the decisive reason so the same weak candidate is not repeatedly reconsidered without new evidence.

### BUILD MISSING PART

Build locally only after the landscape search shows a material gap or when adaptation cost/risk exceeds a clean implementation.

For each locally built component, state the evidence for why existing candidates were insufficient.

## Reuse must not freeze architecture

Existing repositories are evidence and components, not requirements.

Avoid these failure modes:

- copying the architecture of the most popular project before reconstructing the profession;
- letting framework boundaries define professional boundaries;
- importing prompt folklore as domain expertise;
- inheriting obsolete model/tool assumptions;
- adopting a large framework to reuse one small capability;
- equating GitHub stars with professional validity;
- confusing code quality with domain quality;
- confusing domain credentials with executable agent quality;
- accepting benchmark numbers without checking construct validity and comparability;
- importing a specialist agent when a deterministic tool or narrow skill is safer and better;
- forcing reuse when a small local implementation is simpler, more testable, and lower risk.

## Required output: Professional Reuse Dossier

Before applied-agent construction, maintain a compact dossier containing:

### Target

- target profession/work outcome;
- critical competencies and hard constraints;
- runtime/platform constraints;
- safety/jurisdiction/privacy requirements;
- resource constraints.

### Landscape

For each serious candidate:

- name/source/version or commit/date inspected;
- artifact class;
- competencies covered;
- evidence inspected;
- professional-source provenance;
- eval quality;
- security/trust findings;
- license/reuse status;
- runtime/resource dependencies;
- maintenance/freshness;
- important failure modes;
- decision class.

### Gap result

Produce:

`target competency -> strongest existing candidate(s) -> evidence strength -> residual gap -> action`

The residual-gap column is the justification for new design work.

## Minimal acceptance gate before building

Agent Architect may proceed to substantial new implementation only when it can answer:

1. What existing complete agents were searched?
2. What reusable skills/workflows/tools/evals were searched separately?
3. Which candidates were actually inspected beyond README claims?
4. How do the strongest candidates map to the target critical competencies?
5. What direct or professional evidence supports their quality?
6. What security, licensing, runtime, maintenance, and cost constraints affect reuse?
7. What is being reused, adapted, combined, benchmarked, or rejected?
8. What residual capability remains genuinely missing?
9. Why is building that missing part preferable to adapting the strongest alternative?

If these cannot be answered for a non-trivial/common profession, the build decision is premature.

## Integration with the rest of Agent Architect

This capability does not replace profession reconstruction. The profession model is required to know what to search for and how to judge candidates.

It feeds:

- competency modeling — existing components reveal candidate procedures and hidden requirements but do not define them automatically;
- research architecture — claims about candidates require source/evidence validation;
- procedural packaging — adopted components must be decomposed into the correct reusable units;
- agent architecture selection — reuse may eliminate the need for extra agents or expose justified specialist boundaries;
- security/governance — third-party artifacts expand the supply-chain and permission surface;
- evaluation — inherited components must pass the target system's own evals rather than importing upstream confidence;
- resource & cost engineering — reuse is valuable only when total lifecycle cost/risk is lower or capability is stronger.

## Post-adoption verification

Upstream quality does not transfer automatically to the new context.

After reuse/adaptation/composition:

`upstream evidence -> local integration test -> target-domain behavioral eval -> regression/edge cases -> release decision`

If local evidence contradicts upstream claims, local target-relevant evidence governs the release decision.

## Red-team questions

Before accepting the reuse plan ask:

- Would a senior practitioner recognize the reused component as professionally competent, or merely fluent?
- Would an evaluation scientist accept the evidence as measuring the claimed capability?
- Would a security engineer allow this third-party artifact into the trust boundary?
- Would a hiring manager accept the produced work sample without being told which repository generated it?
- Are we rebuilding something mature because building feels easier than researching?
- Are we reusing something weak because reuse feels cheaper than engineering it correctly?

The purpose is neither maximal reuse nor maximal originality. The purpose is the strongest justified professional system with the least unnecessary reinvention.