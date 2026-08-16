# Automotive Paid Media Specialization — Evidence and Inheritance Record

## Reuse decision

Target: automotive vehicle-retail paid media practitioner.

Candidate: qualified `paid-media-performance-marketing@1.0.0`, digest `sha256:882477d8941c09538576096fbe93cd286584a77d040eecf1d8c266ffab3a9179`.

Decision: **EXTEND**.

Reason: the parent profession, outputs, measurement/causal/economic judgment, resource discipline and authority boundaries transfer. Automotive adds material domain constructs around per-vehicle inventory, merchandising truth, offline dealership funnel, CRM identity stitching, inventory portfolio allocation, sales-operations interaction, vehicle offer/finance claim risk, and physical/local purchase friction. Rebuilding the parent profession would duplicate qualified capability; simple REUSE would under-specialize the domain.

Evidence retained for unchanged invariants: parent qualification record under `architect/library/qualifications/paid-media-performance-marketing/...` and its associated 15/15 critical reliability plus 13/13 complete release evidence.

New/affected evaluation required: automotive-specific fixtures must test inventory truth, downstream sale quality, stale/sold inventory, CRM/offline conversion linkage, inventory allocation, sales-process confounding, claim integrity, and composition with parent policies. Historical parent PASS is not sufficient for these added interactions.

## External reuse search

Search covered public automotive/dealership agents, CRMs and inventory applications plus platform vehicle-ad documentation. Public repositories found were primarily dealership chatbots, CRUD/inventory systems, lead-management CRMs or generic lead automation. These can be tool candidates in a future organization layer but do not provide evidenced senior paid-media judgment or automotive marketing evaluation sufficient for inheritance.

Disposition:

- dealership chatbot / CRM / inventory repositories: **REJECT as professional specialization source**; potentially useful future tool integrations only;
- Google Vehicle Ads documentation: **ADAPT as live/platform evidence**, not as the profession definition;
- Cox Automotive buyer-journey research: **ADAPT as domain evidence** for omnichannel purchase behavior;
- FTC automotive advertising material: **ADAPT as evidence of claim-risk classes**, while exact legal requirements remain jurisdiction/live context.

No third-party code, prompt, or professional artifact is imported.

## Evidence register

### Qualified parent core

- repository: `prostoali2207-gif/professional-ai-agents`
- core: `paid-media-performance-marketing@1.0.0`
- digest: `sha256:882477d8941c09538576096fbe93cd286584a77d040eecf1d8c266ffab3a9179`
- status: qualified

### Google Vehicle Ads documentation

Official Google Ads documentation establishes that vehicle advertising can be inventory-driven; vehicle offers expose attributes such as make/model/price/mileage and are intended to support both online and offline outcomes. Google also requires accurate vehicle-feed data and prominent availability/vehicle details for participating vehicle-ad experiences.

Use in specialization: supports the domain importance of inventory truth, feed/listing consistency, location, availability and offline conversion measurement. Platform-specific availability, schemas and policy details remain live-context knowledge rather than invariant rules.

Sources reviewed 2026-08-16:

- Google Ads Help — Vehicle ads overview: https://support.google.com/google-ads/answer/11189169
- Google Ads Help — Vehicle ads policies: https://support.google.com/google-ads/answer/11544533
- Google Ads Help — Vehicle ads activation/data-quality requirements: https://support.google.com/google-ads/answer/15312145
- Google Ads Help — Integration considerations for vehicle advertisers: https://support.google.com/google-ads/answer/15786784

### Cox Automotive Car Buyer Journey

The 2025 Car Buyer Journey study, published January 2026, surveyed more than 2,300 recent new/used vehicle buyers and reports that vehicle purchase remains strongly omnichannel: most buyers still combine digital and dealership activity rather than completing the entire transaction online.

Use in specialization: supports explicit online/offline funnel modeling and the need to join media evidence with showroom/sales-process outcomes rather than treating a web lead as the terminal outcome.

Source reviewed 2026-08-16:

- Cox Automotive — 2025 Car Buyer Journey Study findings: https://www.coxautoinc.com/insights/cox-automotive-car-buyer-journey-study-finds-efficiency-digital-tools-and-ai-drive-record-satisfaction/

### Automotive advertising claim risk

FTC consumer-protection materials and enforcement actions repeatedly identify automotive advertising failure classes involving unavailable vehicles, advertised prices not honored, undisclosed mandatory conditions/fees, financing qualifications and misleading rebates/incentives.

Use in specialization: supports a stable professional control that vehicle availability, price and material offer qualifications are high-risk claims requiring provenance and compliance review. The specialization does not encode US law as universal; exact legal duties remain jurisdiction/live context.

Sources reviewed 2026-08-16:

- FTC Consumer Advice — Car Dealer Ads and Promotions: https://consumer.ftc.gov/articles/car-dealer-ads-and-promotions-know-you-go
- FTC — March 2026 warning to auto dealership groups on deceptive pricing: https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-warns-97-auto-dealership-groups-about-deceptive-pricing

## Alternatives considered

### REUSE parent core unchanged

Rejected. It would preserve general paid-media competence but miss automotive-specific entity semantics and failure modes: a vehicle can sell out, a VIN/listing can go stale, the media signal can be separated from offline sale by CRM/source handling, and sales operations can confound apparent media performance.

### FORK the Paid Media core into an automotive copy

Rejected. Most parent competencies remain unchanged, so a fork would duplicate evidence and create drift risk. Extension preserves parent qualification while making the delta explicit.

### BUILD NEW automotive marketer from scratch

Rejected. It would unnecessarily rebuild measurement, experimentation, marginal allocation, causal reasoning, automation and authority disciplines already qualified in the parent core.

## Red-team findings

Senior-practitioner gap: automotive marketing cannot be modeled only as lead generation; it needs inventory truth, per-unit economics, appointment/show/sale outcomes, sales-process diagnosis and stale/sold inventory controls.

Educator/researcher gap: domain expertise must not collapse attribution into sales causality; offline matching and CRM source data remain measurement evidence with error modes, not automatic incrementality.

Hiring-manager gap: a useful automotive performance marketer must know when **not** to spend on a stale unit, when a media decline is actually a listing/CRM/sales-ops defect, and when strong lead metrics hide poor showroom/sale outcomes.

Systems gap: specialization must reference the parent artifact rather than copy it, and volatile platform/legal details must remain outside the invariant layer.