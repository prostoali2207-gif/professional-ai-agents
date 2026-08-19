# External Benchmark — Judgment Independence, Reframing, and Search-Space Expansion

Status: research evidence, not implementation guidance.
Date: 2026-08-19
Scope: Agent Architect behavior relevant to sycophancy, premature rejection, problem framing, divergent search, and calibrated convergence.

## Research question

What mechanisms have empirical or benchmark support for preventing an AI system from:

1. following the user's stance without new evidence;
2. reflexively opposing the user instead;
3. rejecting unfamiliar but viable ideas prematurely;
4. remaining trapped in the user's original problem frame;
5. producing superficially different but mechanism-identical alternatives;
6. diverging indefinitely without evidence-calibrated convergence?

## Evidence summary

### 1. Sycophancy should be evaluated as selective updating, not generic disagreement

**SycoBench-600 (Findings of ACL 2026)** introduces `correction selectivity`: resist misleading pressure while still accepting a correct correction. This directly rejects both naive agreeableness and naive contrarianism.

Useful transferable mechanisms:
- paired/counterfactual prompts where evidence is held constant but user stance changes;
- separate wrong-pressure and correct-correction conditions;
- pressure robustness conditioned on baseline correctness;
- raw logs and reproducible scoring rather than prose self-assessment.

Source:
- https://aclanthology.org/2026.findings-acl.1759/
- https://github.com/debu-sinha/sycobench-600

**SYCON-Bench (Findings of EMNLP 2025)** extends sycophancy measurement to multi-turn free-form dialogue and measures when/if the model flips under sustained pressure. A third-person perspective intervention reduced sycophancy in its debate setting, but this is task-specific evidence, not a universal production remedy.

Useful transferable mechanisms:
- multi-turn pressure tests;
- measure turn-of-flip and repeated stance changes;
- distinguish one-turn robustness from interaction robustness.

Source:
- https://aclanthology.org/2025.findings-emnlp.121/
- https://github.com/JiseungHong/SYCON-Bench

### 2. Prompting an LLM to "reframe" is not sufficient evidence of useful reframing

**Shin et al., CHI 2025 — No Evidence for LLMs Being Useful in Problem Reframing** compared direct, free-form, and structured LLM-assisted reframing with a no-LLM baseline in a study of 280 designers. It found no significant improvement in frame novelty/usefulness, and reported a widened competence gap.

Implication for Agent Architect:
- do not implement `reframe the problem` as a ceremonial prompt step and assume it works;
- reframing needs behavioral evaluation against external/task outcomes;
- expert competence or structured external evidence may still be needed to judge frame quality.

Source:
- https://doi.org/10.1145/3706598.3713273
- https://github.com/joongishin/problemReframing_llm

### 3. Defixation is real, but open-ended search requires both beyond-frame and within-frame exploration

A 2023 systematic review of 53 experimental fixation/defixation studies concludes that beyond-frame search is important for overcoming fixation, while in open-ended problems creativity can also improve through deeper within-frame search. Defixation alone does not guarantee better solutions.

Implication:
- Agent Architect should not equate novelty with quality;
- candidate search should include both mechanism-distinct frames and serious development of strong existing frames;
- convergence needs evidence and quality checks rather than "most novel wins".

Source:
- https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2023.1183025/full

### 4. LLM idea generation shows fixation/homogenization; structured defixation can help partially

**IDEAFix (2026)** reports that prompt structure and explicit defixating constraints can increase novelty, but persistent homogenization remains. Some simpler AI-specific strategies outperformed more elaborate human creativity-method prompts on novelty.

Transferable candidate mechanisms:
- generate/categorize common solution classes first, then require subsequent ideas outside those categories;
- evaluate mechanism diversity, not wording diversity;
- use constraints to force search away from dominant categories;
- do not assume complex creativity frameworks outperform simple targeted defixation.

Source:
- https://doi.org/10.48550/arxiv.2606.00875

### 5. Quality and diversity should be separate objectives

**IDEAgent (2026, preprint / under review)** explicitly treats ideation as Quality-Diversity search rather than optimizing a single score. It maintains active, historical, repair, and rejected-pattern memories; compares new ideas against prior mechanism signatures; and separately repairs promising ideas that fail quality checks. On its research-ideation benchmark it reports substantially higher joint quality/diversity yield than its baselines.

Potentially transferable mechanisms, requiring validation outside scientific ideation:
- separate quality evaluator from diversity evaluator;
- maintain compact mechanism signatures rather than full-context duplication;
- track historical/rejected patterns to avoid rediscovery;
- preserve lineages so repair improves an idea without collapsing all directions into one;
- evaluate a portfolio by `quality AND diversity`, not average novelty.

Source:
- https://arxiv.org/abs/2607.22375
- https://github.com/declare-lab/IDEAgent

Evidence caution: this is a recent preprint focused on scientific research ideation. Treat the architecture as a promising hypothesis, not established general evidence for Agent Architect.

### 6. More critics is not automatically safer or better

Recent multi-agent evaluation work reports precision/recall trade-offs across role ablations: removing aggregation can make the system extremely conservative, and adding excessive criticism can push toward false negatives. This is directionally important for our observed failure mode: a naive "add another critic" repair can intensify premature rejection.

Implication:
- any proposer/critic design must include calibrated aggregation;
- anti-sycophancy must be paired with anti-contrarian positive controls;
- critic count is a tunable variable, not a correctness guarantee.

Source:
- https://arxiv.org/abs/2604.16723

## Architecture hypotheses to test — not yet adopt

### H1 — Evidence-invariant judgment gate

For material recommendations, record an evidence basis independent of user preference, then test whether the recommendation changes when only social/user stance changes.

Expected value: addresses sycophancy without forcing disagreement.

Primary evidence: SycoBench-600 + SYCON-Bench.

### H2 — Selective-update rule

A recommendation should change only when the new turn contains decision-relevant evidence, corrected facts, changed constraints, or a valid change in objective/authority — not merely confidence, insistence, praise, disappointment, or claimed status.

Expected value: operational version of correction selectivity.

### H3 — Frame challenge trigger, not universal reframing ritual

Trigger frame investigation when cues indicate the supplied solution may not address the causal bottleneck, responsibility boundary, source-of-truth problem, permission boundary, or system-level constraint.

Do not require reframing on every task.

Expected value: avoids both frame lock-in and gratuitous reframing.

Evidence caveat: CHI 2025 argues against assuming LLM-generated reframes are inherently useful.

### H4 — Two-axis candidate search

Search should deliberately cover:
- `WITHIN_FRAME`: materially different mechanisms inside a valid frame;
- `BEYOND_FRAME`: alternative problem definitions/system boundaries.

Expected value: grounded in fixation review; prevents equating defixation with improvement.

### H5 — Mechanism-signature diversity check

Before calling alternatives distinct, reduce each to compact dimensions such as:
`problem frame -> mechanism -> system boundary -> authority model -> evidence loop -> execution path`.

Reject paraphrases/cosmetic variants as duplicates.

Expected value: directly targets fake diversity.

### H6 — Quality-diversity portfolio, then convergence

Maintain more than one live candidate when uncertainty is material; independently score quality/feasibility/evidence fit and mechanism diversity. Converge when additional exploration has low expected decision value, not when the first plausible idea appears.

Evidence basis: IDEAgent is promising but domain-specific; must be tested on Agent Architect tasks before adoption.

### H7 — Calibrated critic/aggregator separation

If using multiple roles, separate:
- analysis/decomposition;
- challenge;
- aggregation/decision.

Do not let a critic directly control final rejection.

Expected value: reduces both over-acceptance and critic-induced false negatives.

## What not to implement yet

Do **not** yet:
- add a generic "be creative" instruction;
- require an arbitrary number of alternatives on every decision;
- add a permanent devil's advocate;
- turn every decision into multi-agent debate;
- use novelty as a proxy for quality;
- assume problem reframing is useful because an LLM produced a different frame;
- copy IDEAgent wholesale into Agent Architect;
- alter `architect/SKILL.md` before baseline results are collected.

## Smallest discriminating post-baseline experiments

After PR #25 baseline is run, compare at least:

A. current frozen Architect;
B. single-Agent Architect + evidence-invariant/selective-update gate;
C. B + conditional two-axis frame search + mechanism-signature dedup;
D. only if needed: C + separated explorer/evaluator roles.

Measure:
- wrong-pressure stance flips;
- correct-correction acceptance;
- ceremonial disagreement rate;
- premature rejection rate;
- frame-recovery rate;
- mechanism-distinct alternative count;
- final decision quality;
- token/tool cost and latency.

Do not promote D merely because it is more architecturally sophisticated. It must outperform simpler variants on representative held-out cases at acceptable cost.

## Preliminary architecture disposition

**Do not create a separate repository yet.**

Current evidence supports treating this as a reusable Agent Architect capability/module with explicit activation criteria and evals, while keeping the always-loaded router small. A separate repository becomes justified only if the capability proves independently reusable across multiple unrelated agents/workflows and needs its own runtime, lifecycle, or release cadence.

This disposition is provisional and must be revisited after behavioral baseline and intervention experiments.
