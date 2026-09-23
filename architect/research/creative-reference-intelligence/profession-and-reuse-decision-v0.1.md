# Creative Reference Intelligence / Elite Benchmarking — profession and reuse decision v0.1

Status: candidate capability design / NOT QUALIFIED
Date: 2026-09-23

## Problem

Creative, brand, content, visual, naming, capture and interface decisions can become generic when a practitioner relies only on abstract rules or model familiarity. The missing work is not another creative profession. It is the disciplined acquisition and translation of current elite reference evidence into a downstream professional brief.

## Agent Architect classification

Decision: **CAPABILITY / procedural skill**, not a new professional core.

Primary owner:
- qualified **Market & Competitive Intelligence 1.0.0** owns live benchmark research, source quality, freshness, comparability, provenance and bounded implications.

Consumers:
- strategy / positioning;
- Content Architecture;
- Social Content Creative;
- Visual Design / Art Direction when present;
- naming, capture, UX/product-design or other creative owners when the task materially depends on reference literacy.

Existing reusable method:
- `architect/methodology/creative-profession-architecture.md` — reference literacy, divergence, anti-imitation and taste calibration.
- `architect/methodology/procedural-skill-packaging.md` — capability packaging.

Rejected:
- BUILD NEW professional core: no separate stable profession boundary is demonstrated.
- Social Content Creative as research owner: its boundary excludes market intelligence.
- follower-count / reputation lookup as deterministic substitute: insufficient evidence of elite current practice.
- broad inspiration scraping: raises noise and anchoring risk.

## Trigger

Load this capability when one or more are true:
- the user asks for "top", "best-in-class", "nasмотренность", references, inspiration, how leading practitioners do it, or a benchmark;
- creative quality materially depends on current domain practice or tacit taste;
- the task is in a new/materially changed niche and generic model familiarity risks safe-median output;
- a downstream creative owner needs evidence of current mechanisms, conventions, anti-patterns or distinctiveness.

Do not load merely because a task is creative when references cannot plausibly change the decision.

## Core principle

**Small elite benchmark > large mixed corpus.**

The capability must optimize benchmark precision, not source count. It must distinguish:
1. direct domain/commercial analogues;
2. adjacent elite mechanism references;
3. voice/style/craft references.

These sets are not interchangeable.

## "Elite" acceptance

No single proxy proves elite status. Follower count alone is insufficient.

A source belongs in the benchmark only when current evidence supports strong fit on the dimensions relevant to the task, such as:
- repeatedly strong recent artifacts, not one viral outlier;
- recognized craft / category influence / professional reputation where relevant;
- observable execution quality or distinctive mechanism;
- commercial/category relevance for direct analogues;
- clear reason the source is informative for the exact decision.

SEO listicles, generic "top creators" pages, repost/aggregation accounts and popularity-only selections are discovery leads, not benchmark evidence.

## Artifact sampling

Do not infer a creator/practitioner method from bio, reputation, one screenshot or one famous artifact.

Inspect actual recent work. Sample enough artifacts to distinguish a recurring mechanism from a one-off. Expand only while additional sampling has decision value.

Record:
- what was observed;
- recurrence;
- context;
- mechanism;
- transferable principle;
- non-transferable surface expression;
- uncertainty / access limits.

## Inspiration without copying

Adjacent inspiration is allowed when direct analogues are too narrow or would cause imitation.

For every borrowed mechanism separate:
`reference -> underlying decision/mechanism -> why it works there -> what transfers -> what does not -> adaptation constraint`.

Do not copy distinctive expression, composition, wording, identity devices or protected surface style.

## Fail-closed behavior

Return `RESEARCH_REQUIRED` when:
- current elite benchmark is absent and materially needed;
- source access only exposes reputation/metadata but not actual work;
- candidate set is broad/popular but not demonstrably high-quality/relevant;
- benchmark purpose differs materially from the current decision.

Do not replace a failed benchmark with generic assistant advice.

## Handoff contract

Output:
- research question / decision to support;
- benchmark scope and freshness;
- accepted direct analogues;
- accepted adjacent elite references;
- rejected/noisy candidates and reason when material;
- observed recurring mechanisms;
- high-value deviations / anti-patterns;
- transferable principles;
- non-transferable surface features;
- evidence strength / uncertainty;
- downstream implications, bounded to evidence;
- explicit handoff to owning strategy/creative core.

Market Intelligence supplies evidence and bounded implications. It does **not** choose final positioning, concept, script, design or content strategy.
