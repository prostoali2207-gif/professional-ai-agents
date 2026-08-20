# Growth Strategy & Experiment Portfolio — evidence register v0.1

Date: 2026-08-20
Status: research evidence supporting the frozen v0.1 candidate; no behavior-relevant candidate change implied by this register.

## Evidence use rule

These sources support specific claims only. They are not treated as a complete definition of the profession and do not transfer product-experiment practice mechanically into every growth context.

## E-01 — Business outcome / metric hierarchy

Source: Microsoft Research, *Experimentation and the North Star Metric*.
URL: https://www.microsoft.com/en-us/research/articles/experimentation-and-the-north-star-metric/

Supported claim:
- measurable systems commonly contain fast local/leading metrics, broader outcome-oriented metrics and slower lagging outcomes; local metric movement alone is not equivalent to end-state business success.

Consumed by:
- GS-01 objective-to-decision translation;
- business-outcome-over-proxy policy;
- evaluation family GS-BV.

Limits:
- Microsoft product experimentation context; does not establish a universal North Star metric for every business or authorize replacing real sales outcomes with a proxy.

Packaging: `EMBED_CORE` principle; concrete metric definitions remain organization/domain context.

## E-02 — Hypothesis simplicity and falsifiability

Source: Microsoft Research, *Patterns of Trustworthy Experimentation: Pre-Experiment Stage*.
URL: https://www.microsoft.com/en-us/research/?p=680556

Supported claims:
- experiments should begin with a clear hypothesis tied to metrics capable of falsifying/validating the stated effect;
- complex changes should be decomposed when feasible so effects can be interpreted.

Consumed by:
- GS-07 experiment framing;
- smallest-discriminating-test policy;
- evaluation family GS-ED.

Limits:
- focused on A/B experiments; low-volume or non-randomizable growth decisions may require another learning design rather than forced A/B testing.

Packaging: `EMBED_CORE` principle plus measurement-capability handoff.

## E-03 — Holistic outcomes and guardrails

Source: Microsoft Research, *Patterns of Trustworthy Experimentation: During-Experiment Stage*.
URL: https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/patterns-of-trustworthy-experimentation-during-experiment-stage/

Supported claims:
- a local improvement can coincide with harmful movement elsewhere;
- decision-quality requires outcome, diagnostic, guardrail and data-quality views rather than one convenient metric;
- pre-set duration and statistical handling matter when monitoring early results.

Consumed by:
- GS-01, GS-07, GS-10;
- business-value and guardrail logic;
- measurement boundary with qualified experimentation core.

Limits:
- statistical stopping mechanics remain outside Strategist core and are delegated to the qualified measurement capability.

Packaging: stable judgment in core; statistical method `HANDOFF/TOOL_BACKED`.

## E-04 — ROI-aware prioritization and cross-functional portfolio process

Source: Microsoft Research, *Microsoft’s Experimentation Platform: How We Build a World Class Product* (2022-01-28).
URL: https://www.microsoft.com/en-us/research/articles/microsofts-experimentation-platform-how-we-build-a-world-class-product/

Supported claims:
- backlog prioritization is revisited against return on investment, long-term goals, customer feedback and resource shifts;
- product, engineering and data-science perspectives are coordinated rather than allowing one local metric/discipline to define priority.

Consumed by:
- GS-06 portfolio prioritization and opportunity cost;
- bounded backlog / cross-functional handoff logic.

Limits:
- this is one strong organization’s product-development practice, not proof of a universal scoring formula. It specifically argues for contextual prioritization rather than fixed numeric-score authority.

Packaging: `EMBED_CORE` opportunity-cost principle; organization process remains contextual.

## E-05 — Preserve experiment history, including surprising/negative outcomes

Source: Microsoft Research, *Patterns of Trustworthy Experimentation: Post-Experiment Stage*.
URL: https://www.microsoft.com/en-us/research/?p=806938

Supported claims:
- hypotheses, test metadata and metric movements form reusable organizational learning;
- central history reduces contradictory local optimizations and repeated mistakes.

Consumed by:
- GS-10 learning-loop integrity;
- no hindsight rewriting / preserve failure and inconclusive states;
- evaluation family GS-LI.

Limits:
- transferability of a historical result still depends on population, context, mechanism and measurement validity.

Packaging: `EMBED_CORE` preservation rule plus `TOOL_BACKED` experiment registry/history.

## E-06 — Metric quality is a professional decision, not mere availability

Source: Microsoft Research, *STEDII Properties of a Good Metric* (2022-04-06).
URL: https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/stedii-properties-of-a-good-metric/

Supported claims:
- useful experiment metrics need sensitivity, trustworthiness, efficiency, debuggability, interpretability/actionability and inclusivity/fairness considerations;
- easily measured metrics are not automatically decision-valid.

Consumed by:
- GS-01 and GS-03;
- measurement handoff boundary;
- proxy/vanity-metric adversarial tests.

Limits:
- Strategist does not independently implement statistical metric validation; qualified Analytics/Measurement capability adjudicates where material.

Packaging: `REFERENCE/EMBED_CORE` decision principle; method detail delegated.

## Evidence conclusion

The reviewed evidence strengthens, but does not expand, the current frozen candidate claims around:

- outcome-over-proxy judgment;
- falsifiable experiments;
- guardrails and measurement integrity;
- opportunity-cost-aware portfolio prioritization;
- learning-history preservation;
- explicit measurement-specialist boundary.

No source found here justifies a universal ICE/RICE/AARRR formula, fixed benchmark, mandatory three-channel strategy, or automatic A/B testing for every growth decision. Those remain explicitly rejected as universal professional rules.
