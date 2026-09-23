# Creative Reference Intelligence / Elite Benchmarking

Status: **CANDIDATE / NOT QUALIFIED**
Version: 0.3

## Mission

When a professional decision materially depends on nasмотренность, references, inspiration or current best-in-class practice, build a **small, current, high-precision elite benchmark** and translate it into reusable mechanisms for the accountable downstream professional core.

This capability does not replace Market & Competitive Intelligence or the creative owner. It composes them.

## Required dependencies

Load and obey:
1. Market & Competitive Intelligence 1.0.0 exact qualified contract for live research, evidence quality, freshness, comparability and bounded claims.
2. `architect/research/creative-reference-intelligence/profession-and-reuse-decision-v0.1.md`.
3. `architect/methodology/creative-profession-architecture.md` for reference literacy / anti-imitation.
4. Current downstream professional contract that will consume the benchmark.

Use live retrieval when current practice matters.

## Trigger gate

Use this skill when:
- the user explicitly asks for top/best-in-class examples, nasмотренность, references, inspiration or "how the best do it";
- current creative/category practice can materially change the recommendation;
- a new/materially changed niche creates safe-median risk;
- the downstream professional core needs external examples to calibrate taste, structure, mechanism or execution.

Skip only when reference research cannot plausibly change the decision, or an existing benchmark is current and fit for the exact task.

## Workflow

### 1. Define the benchmark question
State the exact downstream decision the benchmark must inform. Do not research "good content/design" generically.

### 2. Split reference classes
Search separately for:
- **DIRECT** — strongest current analogues in the exact or nearest relevant domain/commercial context;
- **ADJACENT_ELITE** — exceptional practitioners outside the exact niche whose mechanism/craft is transferable;
- **VOICE_STYLE_CRAFT** — references only when a specific expression/craft dimension is relevant.

Never merge these into one undifferentiated inspiration list.

### 3. Discover broadly, admit narrowly
Discovery can be broad. The accepted benchmark must be small and high precision.

Do not admit a source because it:
- has many followers;
- appears on a "top X" list;
- is famous;
- had one viral artifact;
- matches the user's first example.

Require task-relevant evidence of repeated strong current work.

### 3A. Elite admission bar

A “top”, “best-in-class”, or nasмотренность request is not satisfied by search-engine ordering or a list of famous names.

For open visual/creative direction, use this default evidence floor unless saturation or access constraints justify a narrower set:
- inspect at least 8 materially relevant artifacts across at least 3 credible sources;
- admit only 3–5 references into the elite benchmark;
- require repeated strong work or a canonical artifact with authoritative provenance;
- prefer primary/official artifact sources over reposts;
- for current practice, require recent work where recency matters;
- for historical/canonical style work, prefer museum/archive/designer/foundry collections and period artifacts over modern “in the style of” imitations.

Aggregators, social reposts, Pinterest-like boards, generic inspiration galleries, “top X” articles and search-image results may help discovery but cannot by themselves establish elite benchmark status.

For every accepted reference record why it cleared the bar:
`artifact inspected -> source authority -> recurrence/canonical status -> task relevance -> unique mechanism contributed -> limits`.

If this bar cannot be met, return `RESEARCH_REQUIRED` or `PARTIAL`; do not compensate with model intuition.

### 3B. Pre-generation lock

When this skill is triggered to calibrate a visual/art-direction decision, the downstream creative owner must not generate or implement the style-dependent artifact before the benchmark handoff is `READY` or explicitly bounded `PARTIAL`.

When the user explicitly sequences the task as "first benchmark / nasмотренность, then create", the benchmark handoff must be **user-visible before generation** unless the user explicitly asks not to see it. Surface only:
- the admitted elite references (normally 3–5);
- why each source cleared the elite bar;
- the concrete mechanisms to ADOPT / ADAPT / REJECT;
- clichés or drift risks the generation must avoid.

Do not treat an internal search, hidden moodboard, or raw image-search result set as satisfying this checkpoint.

The handoff should include usable reference assets/links/identifiers when tooling supports them so the downstream generation step can be grounded in the accepted benchmark rather than in textual style labels alone.

### 4. Inspect artifacts, not reputation
Inspect actual recent artifacts for every accepted source.

For each source identify:
- recurring mechanism(s);
- what job each mechanism performs;
- evidence of recurrence vs one-off;
- contextual constraints;
- observable strengths;
- important weaknesses or limits;
- which elements are transferable;
- which are surface/style and should not be copied.

If actual work cannot be inspected and this matters, mark the source unverified for benchmark use.

### 5. Extract mechanisms
Translate examples into mechanism-level findings, e.g.:
- opening / attention contract;
- proof architecture;
- pacing / information density;
- visual hierarchy / composition;
- narrative sequencing;
- demonstration pattern;
- CTA / commercial logic;
- recurring production language;
- distinctive departures from category convention.

Do not output "copy X creator's style."

### 6. Calibrate breadth
Add sources only while they contribute a new mechanism, counterexample, boundary condition or materially better evidence.

Stop when additional references are repetitive and no longer change the downstream decision.

### 7. Handoff
Return:
- `benchmark_status: READY | RESEARCH_REQUIRED | PARTIAL`;
- exact decision supported;
- accepted DIRECT set;
- accepted ADJACENT_ELITE set;
- accepted VOICE_STYLE_CRAFT set if relevant;
- sampled artifact evidence and freshness;
- usable reference assets/links/identifiers for downstream grounding when available;
- generation_allowed: YES | BOUNDED | NO;
- recurring mechanisms;
- distinctive elite deviations;
- category clichés / weak median patterns to avoid;
- transferable principles;
- non-transferable / imitation-risk elements;
- uncertainties;
- bounded implications;
- downstream owner.

## Quality rules

- Precision over volume.
- Current artifacts over reputation.
- Repeated excellence over one viral hit.
- Mechanisms over surface aesthetics.
- Direct analogues for market/category truth; adjacent elite references for inspiration.
- Distinctiveness must be evaluated against the benchmark, not guessed from model priors.
- The benchmark is evidence, not strategy authority.

## Hard failures

FAIL if the output:
- substitutes generic advice for a missing benchmark;
- calls sources elite based mainly on followers/popularity;
- gives a broad random inspiration dump;
- infers practice from reputation without inspecting work;
- mixes direct analogues with unrelated inspiration without labels;
- copies distinctive surface expression;
- converts observational benchmark evidence into causal performance claims;
- lets Market Intelligence choose final strategy/creative execution;
- ignores an explicit user request for top-level nasмотренность when it is materially relevant;
- treats search ranking, fame, a moodboard, or model memory as sufficient evidence of elite quality;
- allows style-dependent generation before the benchmark is READY or explicitly bounded PARTIAL;
- skips the visible benchmark checkpoint when the user explicitly requested "first benchmark, then create";
- hands downstream only vague style labels when usable inspected reference artifacts are available.

## Downstream consumption rule

A downstream creative/strategy core must not merely receive creator names. It must receive mechanism-level findings and explicitly decide what to:
- adopt;
- adapt;
- reject;
- test.

If a recommendation materially depends on benchmark evidence, the final professional answer must be traceable to that evidence rather than assistant intuition.
