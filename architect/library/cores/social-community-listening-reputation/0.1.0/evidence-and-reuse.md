# Social Community, Listening & Reputation Management Core — Evidence and Reuse Decision

Status: candidate evidence record. Accessed 2026-08-17.

## Reconstruction evidence

- The US Federal Trade Commission's guidance for review platforms requires fair treatment of positive and negative reviews and transparency about moderation practices. It supports review-integrity and anti-suppression failure classes, not UAE legal interpretation: https://www.ftc.gov/business-guidance/resources/featuring-online-customer-reviews-guide-platforms
- Meta's Transparency Center describes contextual human review and platform enforcement actions. It supports the need for contextual review and demonstrates volatile action semantics; it is not a universal business moderation policy: https://transparency.meta.com/enforcement/detecting-violations/how-review-teams-work/ and https://transparency.meta.com/enforcement/taking-action/
- UNIDO's Social Media Moderation Guidelines provide an authoritative organizational example of restrained, proportionate moderation. They are practice evidence, not a universal standard: https://www.unido.org/more/social-media-moderation-guidelines
- ISO 31000:2018 establishes a general risk-management process. ISO 22361:2022 is the closer subject-matched crisis-management standard and supports crisis leadership, decision complexity, communication, training and learning. The official abstracts do not establish one universal escalation ladder or numeric score: https://www.iso.org/standard/65694.html and https://www.iso.org/standard/50267.html
- The CDC Crisis & Emergency Risk Communication manual supports early, accurate and credible communication, explicit uncertainty, protective action and an update cadence under incomplete information. It informs holding-response and information-vacuum policies without creating an organization-specific approval threshold: https://www.cdc.gov/cerc/php/cerc-manual/index.html
- The UK Government Communication Service RESIST 3 guide supports assessment before responding to disinformation and recognizes that intervention can amplify a low-impact falsehood. It informs monitored non-response and escalation triggers: https://www.communications.gov.uk/publications/resist-3-a-quick-reference-guide/
- Le et al., “When is silence golden?”, Corporate Communications: An International Journal 24(1), DOI 10.1108/CCIJ-10-2018-0108, distinguishes planned strategic delay from avoidance or hiding. The study is exploratory, uses eight cases and cannot justify universal numeric thresholds: https://www.emerald.com/ccij/article/24/1/162/19904/When-is-silence-golden-The-use-of-strategic
- Olteanu et al., “Social Data: Biases, Methodological Pitfalls, and Ethical Boundaries,” supports explicit coverage, selection, measurement and inference limits for social data. It does not prohibit using platform observations as detection signals: https://pmc.ncbi.nlm.nih.gov/articles/PMC7931947/
- The systematic review of social-media data complementing surveys supports triangulation and warns against substituting observed platform samples for representative population measurement: https://link.springer.com/article/10.1007/s11042-022-12101-0
- W3C PROV-O supplies a vendor-neutral vocabulary for source, derivation and activity lineage. The core uses those concepts without claiming a particular storage implementation: https://www.w3.org/TR/prov-o/
- NIST AI RMF supports risk-aware governance and lifecycle monitoring. OpenAI's agent-safety guidance demonstrates prompt-injection and tool-authority failure classes. The trust-boundary policy remains vendor-portable and stronger than any single implementation guide: https://www.nist.gov/itl/ai-risk-management-framework and https://developers.openai.com/api/docs/guides/agent-builder-safety

## Evidence interpretation

The stable policies are a bounded synthesis, not a claim that one source specifies the whole profession. FTC material is US guidance; Meta action names and account capabilities are live platform context; ISO abstracts do not supply organization owners, response clocks or universal severity weights; CDC and RESIST support different response conditions whose thresholds must be bound and tested locally; strategic-silence evidence has limited generalizability; social-data research constrains inference beyond observed samples rather than ordinary signal detection.

Accordingly, the core retains intent-level moderation actions, multidimensional risk, explicit response modes, provenance, uncertainty, authority and escalation structure. Jurisdiction, platform mappings, named recipients, numerical SLAs, anomaly baselines, language competence and incident facts remain live context.

## Repository reuse search

The trusted catalog contains `paid-media-performance-marketing@1.0.0` and `video-editing-post-production@0.1.0`. Neither owns community queues, moderation, social-listening validity, reputation assessment or crisis communication governance.

The inspected downstream `auto-sales-growth-system` already has Strategist, Content Analyst, Content Creator, Publisher, Analytics, Sales/Lead Conversion and Market Intelligence responsibilities, structured handoffs, evidence classes and verified fact packets. Targeted inspection found no dedicated community moderation, social-listening or reputation/crisis-governance package. The new core therefore integrates with those roles instead of absorbing or duplicating them.

Reusable repository invariants retained include `BLOCKED_MISSING_FACT`, explicit uncertainty, evidence provenance, untrusted-content separation, least privilege, approval for side effects, typed handoffs, acknowledgment/fallback, direct execution verification and correct-layer regression. These are architectural dependencies, not evidence that the new profession has already passed behavioral evaluation.

## Decision

`Social Community, Listening & Reputation Management -> current catalog and downstream architecture -> no compatible profession core -> BUILD NEW`.

A generic SMM parent is rejected because it would duplicate content strategy, planned publishing, measurement and market-intelligence ownership while obscuring community/reputation failure ownership. Sales/Lead Conversion is rejected as a parent because a DM may be a lead source, but lead closure does not cover public moderation, listening validity, complaint continuity or crisis governance. Market Intelligence and Analytics remain downstream consumers of bounded signals, not owners of community interaction.

Initial composition remains one modular core. A split into separate Community, Listening or Crisis agents is justified only by evaluation evidence of conflicting expertise, authority boundaries, context load or independent-review needs.

Unchanged qualification evidence retained from an existing Professional Core: none.

Required new qualification: schema/contract tests plus behavioral, adversarial and timed tabletop evaluation of the exact artifact digest. The sealed CG-06 release fixture must remain unavailable to the candidate author and be run independently after the artifact is frozen. Until those gates pass, lifecycle remains `candidate` and no behavioral PASS is claimed.

## Known gaps and non-transferable context

- No representative deployment has yet demonstrated platform writes, read-after-write verification, durable case state, approval acknowledgment or fallback under outage.
- The candidate has not yet passed the independent sealed CG-06 tabletop or repeated-trial reliability gate.
- UAE and other jurisdiction-specific legal/privacy/disclosure obligations require current competent review.
- Exact Meta and other platform actions, APIs and account permissions require live verification.
- Arabic dialect/cultural judgment, organization voice, named owners, SLAs, anomaly baselines, monitoring tools and cost thresholds require specialization and evaluation.
- Subjective language, proportionality and crisis-timing judgments require calibrated graders; schema validity alone is insufficient.
