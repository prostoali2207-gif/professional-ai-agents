# Paid Media / Performance Marketing Core — Evidence and External Reuse Analysis

Status: candidate evidence record

## Reconstruction evidence

The profession model is intentionally broader than ad-account operation.

### Measurement and causal inference

- Google Ads distinguishes standard attributed conversions from Conversion Lift incremental conversions and defines lift as a treatment-vs-control causal comparison. This supports the core distinction between attribution and incrementality. Source: Google Ads Help, *Understand your Conversion Lift based on users measurement data*, accessed 2026-08-16: https://support.google.com/google-ads/answer/14102450
- Google describes randomized Conversion Lift as a controlled experiment for causal impact. Source: Google Ads Help, *About Conversion Lift*, accessed 2026-08-16: https://support.google.com/google-ads/answer/12003020
- Google Research describes randomized geo experiments as a method for measuring advertising effectiveness and informing bidding, budgeting and campaign design. Source: Vaver & Koehler, *Measuring Ad Effectiveness Using Geo Experiments* (2011): https://research.google/pubs/measuring-ad-effectiveness-using-geo-experiments/
- Chen & Au, *Robust Causal Inference for Incremental Return on Ad Spend with Randomized Paired Geo Experiments*, Annals of Applied Statistics 16(1), 2022, supports iROAS as a causal quantity and documents inference difficulty with heterogeneous geos and budget constraints: https://research.google/pubs/robust-causal-inference-for-incremental-return-on-ad-spend-with-randomized-paired-geo-experiments/
- Lewis, Rao & Reiley, *Measuring the Effects of Advertising: The Digital Frontier*, NBER Working Paper 19520 / University of Chicago Press chapter, explains why abundant digital metrics do not remove causal-identification difficulty and emphasizes experiments for true causal effects: https://www.nber.org/papers/w19520
- Google Research, *Near Impressions for Observational Causal Ad Impact*, explicitly states randomized experiments are the gold standard while observational attribution has limitations. https://research.google/pubs/near-impressions-for-observational-causal-ad-impact/

### Measurement configuration and optimization coupling

- Google Ads states that attribution-model configuration changes reported conversions and can affect automated bidding strategies that optimize against the Conversions column. This supports the rule that measurement configuration is part of the control system, not merely reporting. https://support.google.com/google-ads/answer/6259715
- Google Ads conversion-value guidance links optimization quality to conversion values and business impact, supporting value-aware rather than count-only optimization. https://support.google.com/google-ads/answer/14791574
- Meta's Conversions API documentation describes server-to-platform event connectivity for optimization and measurement and notes support for downstream/offline outcomes and lift studies. It is platform evidence for data-quality and downstream-value concerns, not a definition of the whole profession. https://www.facebook.com/business/help/AboutConversionsAPI

### Experiment design and uncertainty

- Google Ads Experiments documentation uses traffic/budget splits and warns that indeterminate results may require longer duration/data collection. This supports predeclared experiment duration and avoiding premature conclusions. https://support.google.com/google-ads/answer/10682377
- Google Conversion Lift guidance notes that smaller holdouts require more samples and that study duration must account for conversion lag. https://support.google.com/google-ads/answer/12005564
- Google Research on brand-lift measurement discusses imperfect A/B experiments, treatment noncompliance, response bias, standard errors and population slicing, supporting the need for statistical judgment beyond dashboard comparison. https://research.google/pubs/methods-for-measuring-brand-lift-of-online-ads/

### Saturation, allocation and MMM

- Google Meridian describes MMM as measuring marketing impact across channels, accounting for non-marketing factors, estimating ROI and optimizing future budget allocation. It explicitly supports calibration with experiments. This supports MMM as a specialist measurement/allocation capability, not as the entire paid-media profession. https://github.com/google/meridian
- Meta Robyn models media efficiency, adstock, saturation curves and budget allocation. It supports the professional importance of diminishing returns and allocation under saturation, while remaining an MMM tool rather than a complete practitioner model. https://github.com/facebookexperimental/Robyn
- Google Research, *Bias Correction For Paid Search In Media Mix Modeling*, documents targeting-driven selection bias and broader MMM challenges, reinforcing that observational aggregate models require identification judgment. https://research.google/pubs/bias-correction-for-paid-search-in-media-mix-modeling/

### Invalid traffic / measurement governance

- Media Rating Council publishes Invalid Traffic Detection and Filtration Guidelines, Outcomes and Data Quality Standards, and Digital Advertising Auction Transparency Standards. This supports treating invalid traffic, data quality and auction transparency as boundary-critical concerns where applicable. https://www.mediaratingcouncil.org/standards-and-guidelines

### Privacy and signal degradation

- Google Ads Data Hub explicitly uses aggregate privacy protections and documents privacy checks that can filter output; this supports treating observed advertising data as subject to privacy-induced information loss rather than assuming event-level completeness. https://developers.google.com/ads-data-hub
- Google Tag Platform privacy guidance requires privacy/consent-aware collection behavior. https://developers.google.com/tag-platform/security/concepts/privacy

## External reuse search

Search date: 2026-08-16. Candidates were evaluated as potential sources/components, not accepted based on title, stars or README claims.

### Candidate A — `amekala/ads-mcp`

Observed role: cross-platform advertising MCP/tool surface plus a performance-marketing agent prompt and skills.

Decision: **ADAPT TOOL CONTRACTS / REJECT AS PROFESSIONAL CORE**.

Why: it may be useful later as a platform execution adapter, but repository claims do not establish a qualification boundary for senior professional judgment across causal inference, unit economics, marginal allocation, measurement validity and authority. Tool breadth is not profession validity. Platform credentials and write capability also create a materially different security/authority boundary.

Import status: no code or prompt material imported. Therefore no third-party license dependency is introduced into this core.

### Candidate B — `thatrebeccarae/claude-marketing`

Observed role: broad collection of marketing skills including paid-media audits and platform-specific guidance.

Decision: **REJECT AS WHOLE CORE; POSSIBLE REFERENCE-LEVEL ADAPTATION AFTER CLAIM-BY-CLAIM VALIDATION**.

Why: breadth and checklists can improve recall, but a repository-level claim of specialist depth does not demonstrate construct-valid senior performance or causal/measurement judgment. Current platform benchmarks and dated mechanics are volatile and should not become stable core knowledge.

Import status: no content imported.

### Candidate C — `msitarzewski/agency-agents` / mirrored `CloudAIX/agency-agents`

Observed role: multiple role personas including PPC strategist, paid-media auditor, tracking specialist and creative strategist.

Decision: **REJECT AS PROFESSIONAL CORE / USE AS PROFESSION-DECOMPOSITION LEAD ONLY**.

Why: role decomposition is directionally useful, but separate personas and checklist volume are not evidence that the assembled system preserves senior integrated judgment. No inherited PASS is accepted.

Import status: no content imported.

### Candidate D — `google/meridian`

Exact revision inspected for reuse decision: `b1d875724c56fb31b07ac0fa3bf9ef53ee4fdeaf` (main head observed 2026-08-16). License: Apache-2.0 per repository metadata.

Observed role: Bayesian MMM framework for channel contribution, ROI and budget allocation with experiment calibration.

Decision: **ADAPT/EXTEND AS OPTIONAL SPECIALIST MEASUREMENT CAPABILITY; REJECT AS WHOLE PROFESSIONAL CORE**.

Why: strong first-party methodology and explicit measurement scope, but MMM is one measurement/planning method and does not cover day-to-day paid-media diagnosis, creative systems, tracking architecture, auctions, platform optimization or professional authority. It can become a later optional dependency for contexts with sufficient data and competent model validation.

Imported scope: zero source code. Concept-level evidence only.

### Candidate E — `facebookexperimental/Robyn`

Observed role: semi-automated MMM, saturation/adstock modeling and budget allocation. Repository reports MIT license.

Decision: **ADAPT AS OPTIONAL MEASUREMENT/ALLOCATION REFERENCE; REJECT AS WHOLE CORE**.

Why: useful for saturation, response curves and budget-allocation concepts, but still narrower than the profession and carries model/data assumptions requiring specialist validation.

Imported scope: zero source code.

### Candidate F — agent/skill repositories such as `realjaymes/marketingagentskills`, `gtmagents/gtm-agents`, `realkimbarrett/advertising-skills`, `cgallic/kai-cmo-harness`, `itallstartedwithaidea/advertising-hub`

Decision: **REJECT FOR DIRECT IMPORT AT THIS STAGE**.

Why: these are useful discovery leads and may contain practical workflows, but their public descriptions do not independently establish evidence provenance, frozen behavioral evaluation, transfer boundaries and qualification appropriate to this Library. Some are also broader growth/CMO systems rather than the target profession.

## Build decision

**BUILD NEW professional core, while ADAPTING evidence patterns and reserving optional specialist/tool integrations.**

Alternative considered: fork a mature paid-media skill collection and harden it. Rejected because the transformation required to supply construct-valid profession boundaries, measurement science, causal judgment, provenance, context separation, authority and behavioral qualification is sufficiently large that a fork would preserve misleading provenance and hidden assumptions.

Trade-off: BUILD NEW costs more initial research, but creates a cleaner stable-vs-live boundary and avoids coupling the Library to a specific ad-platform toolchain. Reuse remains appropriate later for measurement engines, platform adapters and domain specializations when their exact compatibility is demonstrated.

## Evidence conflicts / limits

1. Platform documentation is partly vendor guidance and may favor platform-native measurement/automation. It is used for mechanics and first-party definitions, not as sole evidence of effectiveness.
2. Randomized experiments are strongest for causal identification but may be infeasible, costly, underpowered or affected by interference. The core therefore requires decision-value and feasibility judgment rather than universal RCT mandates.
3. MMM can support channel-level planning under privacy constraints, but model specification, selection bias and calibration remain material risks. It is an optional specialist capability, not a default truth source.
4. There is no evidence that any searched open-source paid-media agent already satisfies this repository's Professional Core admission gate. Popularity is deliberately ignored as qualification evidence.