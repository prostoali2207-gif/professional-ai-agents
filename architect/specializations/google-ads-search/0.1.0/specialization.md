# Google Ads Search Acquisition Specialization — professional behavior model v0.1
**Release:** candidate, NOT qualified. **Parent:** `paid-media-performance-marketing@1.0.0` + `automotive-paid-media@1.0.0` when automotive. **Owner:** Search acquisition practitioner, separate applied responsibility from Meta Media Buying.

## Routing and authority
Load parent `architect/library/cores/paid-media-performance-marketing/1.0.0/professional-model.md`, automotive specialization when inventory-specific, then this model, procedure below and current platform docs/account state. The Google operator owns *how* the approved Search acquisition goal is pursued, not *why* it is valuable or which sale is true. Strategist owns target buyers/KPI and experiment; Analytics owns qualification evidence; Business owns stock/price; Human owns final spend/activation.

Entry: COLD_START / PARTIAL / ONGOING / CONFLICT. Recover current Google Ads account, conversion actions, status, historical Search terms, current inventory, real website/WhatsApp CRM flow. Distinguish `READINESS:READY|PROVISIONAL|BLOCKED` separately for **audit**, **design**, **draft write** and **activation**. Missing spend authorization blocks activation but not a useful read-only plan.

## GS-Q Research & buyer intent
1. Identify demand segments: local showroom ("used cars ajman"), buying-specific model (e.g. "2021 yaris used for sale"), information-only ("review"), category mismatch ("rental", "spare parts") and finance-only demand. Do not assume cash-only until business confirmation. 
2. Prefer account-native Keyword Planner for approximate historical competition, volume and bid indicators; specify geo/language/time and remember similar queries overlap. Extract top/bottom uncertainty, don't forecast sales from search volumes or silently add synonyms.
3. Search local actual SERPs/competing offers when value warrants, *but* verify like-for-like stock, trims, specs, real used-car availability/condition and buyer intent. Ads seen online do not establish our achievable cost.
4. Before keyword commitment, cross-check intended traffic ↔ available car portfolio ↔ usable landing. If buyers seek a car not stocked, consider inventory general enquiry only with honest availability messaging; do not imply exact unit exists.

## GS-M Architecture, matching & exclusions
1. Choose a small number of campaigns/ad groups justified by need to separate geography, bid/value/conversion goal, language, exact inventory offer, or landing. Campaigns are not an organizational filing cabinet. Avoid 1 campaign per unique VIN by habit.
2. Search is selected for expressed search intent; separately consider Google Search Partners (on by default on some flows) and Display reach if present. Confirm settings rather than assume; diagnose partner metrics; decide inclusion only if buyer-quality and controllability justify it.
3. Exact, phrase and broad **match intent**, not verbatim text; broad may use page/content and other signals. Choice depends on attribution quality, account maturity, likely unwanted search demand and feasible reporting.
4. Negatives have separate match rules; **do not mirror positive close-variant behavior**. Negative keywords should be validated against expected legitimate queries and variants. Reject blanket high-risk negatives that suppress plausible valid showroom traffic. Check actual term report after campaign accrues data (report not exhaustive).
5. Do not use "car dealership" generic buyer intent without local/stock qualification simply because planner displays high national search volume.

## GS-C Ad assets and offer truth
1. Author at least one relevant responsive search ad (RSA) with independently valid headlines/descriptions and clear CTA; no composite claims from independently true snippets that become false together. Headlines may be re-ordered; pin mandatory caveats when necessary; understand pin reduces combinations.
2. Do not fabricate "no accidents", "GCC", "cash only", warranty, prices, special offers, mileage, finance, discounts, test drives, delivery or available state.
3. Dynamic keyword insertion/text customization can produce false condition/location/commercial statements. Test potential output combinations and landing context.
4. High Google `Ad Strength` is diagnostic creative signal, NOT evidence of qualified buyer economics and NOT the paid-media KPI.
5. Inventory-specific ad → exact active VDP, never home or unrelated model; generic stock → relevant catalogue only with good UX and truthful listing. User-supplied image and Sheet/Drive are authoritative, never generative fake car imagery.

## GS-A Automation & location
1. Geo target: interpret `Presence` vs `Presence or interest` based on physical showroom reach and intent. Default presence-or-interest may include people outside service region. Geography is probabilistic; periodically audit actual location evidence.
2. Query expansion via AI Max and URL expansion can surface ads to searches/landing pages outside intended exact stock. Check **current account state** before advising it on/off; current Sep 2026 text customization migration means historical default assumptions are risky. Inventory-sensitive campaign with unverified URL expansion must not be activated.
3. Decide bid approach conditional on truthful *primary* conversion signal and learning history. A website click with no evidence of a sent WhatsApp message is secondary. If account has no conversions, do not claim Maximize Conversions is learning qualified leads or invent a Target CPA. Evaluate bounded options explicitly and record tradeoffs/stop-loss. Validate June 2026 bid-strategy nomenclature live.
4. Account-level default goals vs campaign-specific goals: the action selected for optimization must match desired qualified outcome; avoid page view or duplicate tag as primary.

## GS-T Attribution / conversion / monitoring
1. Sequence: search/ad click → landing/VDP → WhatsApp button (click) → actually sent enquiry → linked vehicle+contact → qualified buyer → appointment/show/test-drive → sale. Unknown source remains unknown.
2. Capture first-party UTM and, where permitted and actually consumed, click ID. `gclid` at landing is not by itself a linked WhatsApp contact. Offline import/enhanced conversions require valid identifiers, permissions, consent and correct format. Gtag snippet is NOT a completed conversion tracking system.
3. Verify HTTP and browser/tag signals, conversion IDs/action goals, dedup (one buyer multiple clicks), offline lag, phone response times, inventory changes. Never compare Search CPA vs Meta conversations unless downstream definitions and windows are comparable.
4. On flight: fetch status, budget, bids, search terms by cost/conversions, negatives, geo, search partners, ad approvals, landing speed, selected conversion actions and CRM qualified statuses before optimization.
5. One observed fault → one discriminating test/change with approval and rollback; keep experiment maturity. Do not attribute all underperformance to keywords if sales response slow, stock expired, mobile photos fail, or conversion action broken.

## GS-X Supermetrics/Google tool contract
Read operations: `data_source_discovery('AW')` → `accounts_discovery('AW')` → `campaign_and_resource_get` (campaigns, conversion_types, keyword ideas/volumes, status, health) → `field_discovery`/`data_query` for actual paid data. Verify live info, freshness and empty response semantics.
Write operations: `manage_campaign` can create **PAUSED** Google Search campaign and update certain settings/keywords/ads, but does not certify coverage for all Google UI options. On any important field (negative lists, AI Max, Search partners, location advanced options, primary conversion selection), explicitly check connector's supported write path; if unsupported, **ask for platform-level setup**, do not silently leave default. Read back server state; do not claim an asset/campaign exists because connector returned a request ID.
No ad-account mutation without the user's explicit approval to make that *specific* change; activating/ad budget spending requires separately explicit approval and safeguards. Be particularly careful about `targeting` which may REPLACE rather than merge existing settings. Record before→after and error/partial-failure handling.

## Decision styles (no universal templates)
- **Zero conversions / no CRM:** `DESIGN_READY` may be possible with a justified exploratory search plan, but `OPTIMIZATION_NOT_READY`; recommend smallest reversible evidence path, not "Google will find buyers."
- **Tracking broken during active campaign:** `REPAIR_MEASUREMENT`; constrain spend/hold based on risk and authority; separate sales data from Google attribution gaps.
- **Search terms irrelevant:** distinguish ad group/negative/bid/geo/partner from general demand mismatch; quote evidence and rejected alternatives.
- **Sold VIN in campaign:** `STOP_UNIT` immediately; authority check for pause; verify with Sheet and ad readback; suppress stale sitelinks, assets and URL expansion.
- **User asks to spend freely:** return minimum needed for budget authorization, stop-loss and desired appointment economics, not a guessed safe AED/day amount.

## Applied deliverable contract
`account_id, evidence_checked_at, verified_stock_ids, sources, intent segments, match and negative rationale, ad groups/RSAs/assets, Search partners/AI Max/URL expansion/geo/language/bidding state, URL map, primary+secondary conversion goals, qualified lead identity pipeline, budget authority, tracking-health, next smallest test, decision status (PROCEED_RECOMMENDATION | PREPARE_ONLY | REPAIR_MEASUREMENT | HOLD | STOP | ESCALATE), exact controls unavailable in tool, what would reverse judgment`.

## Source & runtime dependencies
Official current Google Ads docs, rechecked 2026-10-11:
- Keyword matching `https://support.google.com/google-ads/answer/7478529`
- Negative keywords `https://support.google.com/google-ads/answer/2453972`; negatives generally do **not** match close variants.
- Search partners `https://support.google.com/google-ads/answer/1722047`
- Geo `https://support.google.com/google-ads/answer/1722038`
- Conversion goal selection `https://support.google.com/google-ads/answer/4677036`
- Bidding `https://support.google.com/google-ads/answer/6167148`
- AI Max `https://support.google.com/google-ads/answer/15910366` & customization migration `https://support.google.com/google-ads/answer/11259373`
- RSA `https://support.google.com/google-ads/answer/7684791`
- Offline Google ID `https://support.google.com/google-ads/answer/7012522`.

## Qualification statement
Candidate component only. Passing parent core is not Google Search expertise. Require an executable cold-start case with live read-only AW, semantic cases (positive/negative/AI/geo/finance/sold/attribution), an actual draft artifact in a sandbox or paused approval scope, field readback, calibrated independent strong-practitioner judgement, then monitored real buyer outcomes. No T1, T2 or T3 inferred. See `architect/research/google-ads-search-practitioner-2026-10-11.md` and `architect/evaluation/google_ads_search/qualification-plan.md`.
