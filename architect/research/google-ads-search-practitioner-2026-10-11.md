# Google Ads Search acquisition practitioner — profession reconstruction and reuse decision
Date: 2026-10-11. Phase: research/design. Status: candidate, no expert-validation claim.

## Actual work, user and context
Buyer is a UAE used-car showroom with roughly a dozen unique, changing used-car units; website catalogue and specific VDPs; lead capture mostly on WhatsApp, offline showroom appointments and sales. The goal is **attributable qualified inquiries → appointments → sales at sustainable marginal cost**, not account setup, impressions, cheap clicks, ad strength, or `click to WhatsApp` counts.

Google Search professional != Meta Ads UI operator. The practitioner interprets live searches, auction/bidding, search query/match semantics, negative keyword harm, current auto-generated ad/URL behavior, local intent, conversion action semantics, small sample inference and account-billing/authority limits.

### Representative decisions and tacit cues
- A new account with **zero conversion actions**: refuse to imply Google will optimize for qualified buyers. Classify tracking readiness and consider explicit bounded acquisition-only test versus waiting for conversion signals; never label page loads or clicks a qualified lead.
- A Keyword Planner row with 720 average searches for `used cars ajman`: this is a forecast-like historical estimate for the entered targeting/settings, **not 720 unique buyers, zero-variance local demand, or 720 incremental inquiries**. Overlap with `second hand cars ajman`; don't add volumes.
- A broad/AI Max search query with expensive clicks but off-target geography/financing: confirm actual search terms, geo presence/interest, click IDs and qualification before suggesting mass exclusions; distinguish waste by query and lead quality, not CTR.
- A superficially great responsive search ad that generates a misleading condition/finance claim through text customization: freeze or remove the incompatible asset, verify current platform auto-generation and inventory truth, avoid performance-first justification.
- A reserved/sold one-off used car: immediately hold delivery on that unit; do not redirect to another vehicle without appropriately truthful intent/offer; obtain live authoritative Sheet state rather than trusting landing cache.
- Sparse conversions: resist universal bidding defaults, artificial target CPA, statistically uninformative early optimizations; bound risk and identify next discriminating evidence.
- A broad suggested `free` negative blocks only irrelevant free-guide intent? Validate if it would also block `free car inspection included` when a verified offer exists; apply exact/phrase/broad negative semantics deliberately. Cross-check all proposed negatives against positive buyer-intent queries.
- Google suggests enabling AI Max/Final URL expansion: check whether new destinations could include sold VDP, blank-photo car, legally unsupported condition, or mismatched listing; no unexamined automation.

### Entry-state prerequisites by decision
| Decision | Safety-critical / decision-changing | Can stay provisional |
|---|---|---|
| Recommend platform priority | existing customer/lead quality, unit stock, budget sensitivity, market evidence | exact future CPC |
| Design Search campaign | current inventory & VDP availability, target geo/language, search intent, actual conversion definition, policy/account constraints | perfect volume forecast |
| Select bid strategy | actual conversion action, primary/secondary, value quality, history, spend tolerance | stable future auction cost |
| Author ad | approved business claims, actual landing page, language/policy | exact user conversion probability |
| Create **PAUSED** draft | explicit approval for writing to ad account, target account, validated campaign parameters, budget cap, rollback | future sale count |
| Activate/spend/change spend | explicit current human approval; account cost cap; active valid offer; tracking & response owner | future statistical significance |
| Interpret results | search terms, cost, attributed actual inquiries, qualified lead/appointment join, delays, source completeness | unavailable long-run sale if appropriately caveated |

Entry states: COLD_START, PARTIAL_BASELINE, ONGOING, FOLLOW_UP, CONFLICTING_STATE. Recover current state first; ask only missing decision-changing question. Conflict between Sheet and ad/site → verify authority and pause affected offer until reconciled.

## Professional responsibilities and boundaries
Senior Search practitioner owns: account audit and setup spec; query demand and SERP research; campaign/ad group/keyword architecture; Search network/partner settings; match types and negatives; geo/language; responsive search ads and dynamic text guardrails; destination, tracking and consent handoff; conversion/Smart Bidding rationale; query/auction/quality diagnostics; pacing/stop-loss; experiments and operational reporting.

Not owned: user/business final pricing/discount/financing/warranty, jurisdiction-specific legal interpretation, making/editing Sheet stock facts, website code deployment, qualified-sales classification without evidence, choice of whole-business strategy, or unapproved spend. Hand off to Market Intelligence, Strategist, Engineering/Analytics, Sales and Publisher when required.

## Reuse compatibility decision: EXTEND
- **Parent:** `paid-media-performance-marketing@1.0.0` qualified (manifest/library digest `sha256:882477d8941c09538576096fbe93cd286584a77d040eecf1d8c266ffab3a9179`), qualified for analytical judgment/budget/measurement governance, NOT Google Search mechanics or live use.
- **Domain:** `automotive-paid-media@1.0.0` inherits parent; per-unit stock, exact-offer integrity and offline funnel; does not contain Search platform skills.
- **Delta:** Google Search intent taxonomy, auction/query mechanics, negative types, geographic options, Search campaign hierarchy and ads/assets, AI Max auto-generation, platform conversion rules, account-level and campaign-goal semantics, data acquisition and read/write verification. Preserve parent business-value/budget/causal decisions unchanged.
- **Alternatives:** BUILD NEW duplicate universal marketer = rejected (duplication/drift and weakened core provenance); reuse Meta specialization alone = rejected (fundamentally different auction/placement and user intent); mere checklist = rejected (no observable judgment/eval); EXTEND Google-specific separate module with applied project entrypoint = selected.
- **Compatibility caveat:** connector `Supermetrics AW` API is not the native Google Ads UI; inspect actual operations and read back any output. Some settings (AI Max, networks, presence/interest, negative keywords, conversion action creation) may NOT be writable through connector. Unsupported operation → manual/native UI or approved other adapter, not pretend success.
- **Evals:** inherited pass remains evidence only for unchanged core competencies; added Google competencies and plugin interactions require practical/adversarial evaluation, independent validation for expert-level claim (T2), field evidence for production-proven (T3). Until then **candidate / unqualified**, no professional-equivalence claim.

## Observable competency/evidence model
| ID | Competency and discriminator | Observable task/evidence | Hard fail / verification |
|---|---|---|---|
| GS-01 | Query intent/context discrimination vs impressions-only planner | Classify 15 mixed search terms, overlap & source targeting, budget-aware shortlist | treating overlapping estimates as additive; keyword volume as leads |
| GS-02 | Search architecture & match decisions vs one-keyword-per-campaign | Design minimal campaign/ad group/match map, explain false positives/learning density | endless micro campaigns, arbitrary broad as default |
| GS-03 | Negative keyword safety vs naive blanket blocklist | Simulate effect of 10 negatives on buyer-intent positives + marginal queries | suppresses valid showroom queries without recognizing conflict |
| GS-04 | Local/language reach vs defaults | Identify presence vs interest risk and choose based on showroom reach | assume geo targeting perfectly accurate |
| GS-05 | RSA copy/asset discipline | Produce compliant diverse headlines/descriptions under verified inventory + test dynamic combinations | invent price/finance/warranty/stock; score Ad Strength as sales |
| GS-06 | AI Max, text customization and Final URL expansion | Detect hidden auto-generated promise or sold-unit destination risk, specify allowable controls and test | assume inactive feature or let AI select arbitrary sold VDP |
| GS-07 | Conversion architecture & bidding | Separate page/CTA/inbound/qualified/appointment/sale and primary vs secondary; decide bidding conditional on signal | calls clicks qualified leads, fabricates conversion ID or target CPA |
| GS-08 | Measurement/experiment diagnosis | Audit missingness, dedup, click IDs, time lag; identify one changing variable | claim Search beats Meta on platform conversations |
| GS-09 | Budget/pacing and auction diagnosis | Compare spend by term and qualified lead with counterfactual/response-time alternatives | spend increase without authority/economic threshold |
| GS-10 | Inventory and ad-to-VPD integrity | Match exact unit IDs/status/offer to real pages and suppress sold/reserved | advertises reserved car or leaves stale copy after stock change |
| GS-11 | Platform tools, governance, verification | Read live account, make dry plan, prove write/readback and rollback on mock account | create/spend without approval, unsupported setting silently assumed |
| GS-12 | Cold-start senior intake | Account with zero conversions, unclear budget: bounded evidence request & safe next action | user forced to guess campaign setting or arbitrary budget |

Each GS task needs: input/expected invariants/observable artifact/grader (deterministic for truths, independent practitioner for judgment)/freshness. Passing static contract checks is not Google campaign competence.

## Knowledge packaging audit
- `EMBED_CORE`: value > proxy, no guessed commercial claims, capability != spend authority.
- `PROCEDURAL_MODULE`: search-intent selection + negatives collision test + RSA ad-to-landing audit + geo/bid/measurement decision tree + post-launch search-term root-cause.
- `REFERENCE_MODULE`: meaning of match options, campaign hierarchy, asset configurations, data integrity definitions; keep references brief.
- `LIVE_RESEARCH`: 2026 Google Ads AI Max and bidding label changes, current UAE ad policies/eligibility, live account and settings, auction competition, Google's product docs.
- `TOOL_BACKED`: Supermetrics read-only `accounts_discovery`, `campaign_and_resource_get`, `field_discovery`, `data_query`, marketing utilities; Google Sheet current stock; URL/site checks; Sales WhatsApp evidence.
- `ESCALATE`: billing, regulated financing, ambiguous legal disclosure, account access, unavailable API controls, expert validation, UI actions outside tool capability.
- Retrieval triggers and no-data: missing `Search terms` on new account → keyword planner estimates only; missing conversion actions → blocking conversion strategy choice for live campaign; missing account settings → do not infer current network, geo, AI Max flags.

## Current evidence and limitation (2026-10-11)
Observed connected Google Ads account `Am motors` (ID `2470160660`) via Supermetrics; campaign and conversion-type lists empty. Google Keyword Planner can retrieve volumes for seeded queries, subject to query settings; early estimate `used cars ajman` ~720 monthly at medium competition is **not** a validated local performance forecast. Authoritative Google Sheet current inventory includes `В наличии`, `Резерв`, `Продана`, therefore strict status gate. Website has UTM prefill to WhatsApp; no proof that CTA clicks are sent inquiries.

Official source set fetched 2026-10-11:
- Match types: https://support.google.com/google-ads/answer/7478529 (exact/phrase not literal and overlap).
- Search term/keyword match behavior: https://support.google.com/google-ads/answer/14996023 .
- Location options: https://support.google.com/google-ads/answer/1722038 (presence vs presence-or-interest; approximate).
- Smart Bidding strategy choice: https://support.google.com/google-ads/answer/6167148 (Jun 2026 labels changed; business-goal fit).
- Primary conversion goals: https://support.google.com/google-ads/answer/4677036 (goals direct bidding).
- AI Max: https://support.google.com/google-ads/answer/15910366 (query expansion, assets, final URL), https://support.google.com/google-ads/answer/11259373 (text customization upgrade starting Sep 2026).
- RSA: https://support.google.com/google-ads/answer/7684791 (asset combinations and pinning; dynamic combinations).
- Offline GCLID/enhanced leads: https://support.google.com/google-ads/answer/7012522 .
Sources document behavior, **not proof** that any specific campaign/strategy will sell cars in Ajman. Google case studies are provider aggregate evidence, not AM Motors causal effects.

## Expert-gap red-team
Senior practitioner: what if broad auto-matching targets parts/rentals/financing, or Google Search Partners hide low-quality inventory? Check actual segment before spend.
Competency assessor: can agent reject a seductive cheap CPC plan, simulate negatives collisions, and catch wrong conversion action in real settings?
Hiring manager: would I trust the operator with money on a new account? Not until it has independently reviewable artifacts, strong Search Ads skill, demonstrated live tool handling, accurate outcomes and approval controls.
Measurement specialist: Google auto-imported conversion goals can silently optimize to page view or wrong event; first verify the account-default primary actions, not merely add a tag.
Security: Supermetrics permission to create paused drafts is still external write; require specific authorization, log exact action and verify server state. No secrets/PII in artifacts.

## Resource/risk gates
Minimum evidence acquisition before configuration; review stock and account directly once, live official platform docs for volatile flags, restrict keyword research to differentiating groups. Avoid expensive or redundant experiments until lead attribution and mobile experience are usable. No unapproved daily budget. Study sample/window and conversion lag before statistical winner claims.

**Release status:** RESEARCH COMPLETE FOR CANDIDATE; not T1/T2/T3. Source set and design do not replace practical behavioral evaluation or independent practitioner review.
