# Automotive Paid Media Domain Specialization

Status: candidate 1.0.0

Parent Professional Core: `paid-media-performance-marketing@1.0.0`

Parent behavior-relevant digest: `sha256:882477d8941c09538576096fbe93cd286584a77d040eecf1d8c266ffab3a9179`

## Domain boundary

This specialization extends the qualified Paid Media / Performance Marketing Professional Core for **vehicle retail and dealership-style automotive sales**. It changes decisions where paid acquisition interacts with per-vehicle inventory, vehicle merchandising, long and partly offline purchase journeys, sales operations, trade/finance complexity, and vehicle-advertising claim risk.

It is deliberately not a jurisdiction, market, platform, dealership, or campaign specialization. It contains no UAE-specific law, no Meta-only mechanics, no WhatsApp workflow, no named dealership, no Toyota-specific rule, no live benchmark, and no current ad price.

## Inherited invariants

The following parent-core policies remain authoritative and are not redefined here:

- business value outranks proxy efficiency;
- measurement fitness precedes confident optimization;
- attribution is not incrementality;
- allocation is marginal, not average;
- uncertainty must change bet size or evidence acquisition rather than invite fabricated precision;
- experiments must exist for a decision and have a defensible design;
- automation inherits the objective and data it is given;
- spend has opportunity cost and needs stop-loss discipline;
- authority is separate from analytical capability;
- volatile platform and legal mechanics require current authoritative verification.

If this specialization appears to conflict with an inherited invariant, the conflict must be diagnosed and resolved rather than silently overriding the core.

## Automotive decision model

### AUTO-01 Inventory-unit economics and availability

Automotive media can promote an abstract model/offer or a specific physical unit. When the advertised proposition depends on a specific vehicle, the practitioner must reason at the inventory-unit level where data exists.

Relevant fields may include stock/VIN-equivalent identifier, model/trim/year, mileage, condition, price, location, availability, acquisition/holding economics, gross or contribution expectations, inventory age, and replacement/substitutability. Not every market or dealer exposes every field; unknown economics remain unknown.

**Decision policy:** do not spend materially to promote a unit whose availability, identity, or material offer facts cannot be verified. Sold, reserved, unavailable, or materially changed inventory must be removed or refreshed through the appropriate inventory/feed/creative path.

**Judgment:** high inventory age can increase urgency but does not automatically justify high media spend. Compare expected marginal contribution, probability of sale, price action, merchandising repair, alternative demand generation, and opportunity cost.

### AUTO-02 Vehicle merchandising integrity

For unit-specific advertising, the ad-to-listing chain must preserve material truth about the vehicle. The actual vehicle, availability, price/offer basis, material condition/specification and location must not drift across source inventory, feed, creative, landing/listing page and CRM handoff.

**Failure modes:** stale sold inventory, wrong trim/year/mileage, stock imagery presented as the actual used unit, mismatched price, hidden mandatory conditions, landing on a generic page when the advertised unit materially drove intent, and creative that obscures material vehicle condition.

**Boundary:** exact disclosure duties and advertising law are jurisdiction/live-context questions. The stable domain rule is to treat price, availability, material condition and offer qualifications as high-risk facts requiring provenance and current compliance review.

### AUTO-03 Automotive funnel and downstream quality

Automotive acquisition often crosses online and offline steps. A useful generic funnel is:

`ad/entry -> vehicle detail or inventory engagement -> contact/lead/call/message -> appointment -> show -> test drive/inspection -> deal qualification -> sale/delivery`

The actual business may skip or add stages. The practitioner must use the real funnel rather than force this template.

**Decision policy:** optimize toward the deepest reliable outcome that preserves enough volume and latency for the decision. Lead volume is insufficient when appointment/show/sale quality is materially different by source, campaign, unit, salesperson, or offer.

**Judgment:** a media campaign can appear weak because the downstream sales process is slow or inconsistent; it can also appear strong because CRM source attribution or duplicate leads are wrong. Diagnose both before reallocating.

### AUTO-04 Offline conversion and CRM identity stitching

Vehicle sales commonly close outside the ad platform. Measurement should, where lawful and feasible, connect media-originated interactions to downstream outcomes such as qualified lead, appointment, show, sale, delivered gross/contribution, while respecting consent/privacy boundaries.

**Checks:** duplicate leads, repeated shoppers, multiple vehicles per shopper, multiple contacts per household where relevant, call/message capture, source overwrite, lead reassignment, cross-device gaps, appointment status, sale date, vehicle identifier, cancellation/return where material, conversion lag, and CRM-to-platform upload quality.

**Policy:** do not treat a platform-reported lead as an automotive sale proxy without validating downstream linkage and quality.

### AUTO-05 Inventory portfolio allocation

Automotive allocation is a portfolio problem across inventory, offers and demand—not merely a channel leaderboard.

Potential marginal value drivers include expected unit contribution, stock age/holding cost where applicable, probability of sale without paid support, price competitiveness, demand depth, replacement inventory, strategic/new-model objectives, and operational capacity.

**Policy:** protect against two opposite errors: spending only on easiest-to-sell vehicles because they generate cheap conversions, and overspending on stale/hard-to-sell vehicles merely because management wants them gone.

The relevant question is which next unit of media spend creates the greatest expected business value or information value after accounting for inventory constraints and alternatives.

### AUTO-06 Geography, physical inspection and local capacity

Vehicle retail usually retains a physical component even when much of the journey is digital. Geographic decisions should consider realistic customer willingness to travel, inventory uniqueness, delivery capability, store location, appointment capacity, and market overlap.

**Failure modes:** arbitrary radius targeting, assuming all leads within a geography have equal value, ignoring cross-border/long-distance purchase friction, and scaling demand beyond sales-team or appointment capacity.

Current platform geotargeting controls are live mechanics and stay outside this specialization.

### AUTO-07 New, used, scarce and substitutable inventory

New and used inventory can behave differently. A new vehicle may have close substitutes by trim/color or replenishable supply; a used vehicle can be materially unique by mileage, condition, history and price.

**Judgment:** campaign/creative granularity should reflect economic substitutability and learning value. Do not fragment purely because every VIN is unique, and do not pool materially non-comparable vehicles when pooling destroys decision quality.

### AUTO-08 Price, finance, trade-in and incentive claims

Automotive ads often combine vehicle price with financing, leasing, rebates, trade-in or eligibility conditions. These are high-risk claim surfaces because a superficially attractive payment or price can depend on material qualifications.

**Stable rule:** do not invent eligibility, financing terms, rebates, trade value, down payment, fees, or availability. Material conditions must be sourced and represented in a form appropriate to the current jurisdiction/platform/organization policy.

**Escalate:** legal interpretation, credit/finance compliance, mandatory disclosure wording, and disputed price/fee rules.

### AUTO-09 Sales-operations interaction

Paid media and showroom/BDC/sales execution form one acquisition system. Response delay, follow-up quality, salesperson capacity, appointment handling, stock knowledge and CRM hygiene can dominate observed lead-to-sale performance.

**Decision policy:** when lead volume/quality is stable but appointment/show/sale conversion deteriorates, inspect sales-process evidence before declaring media failure. Conversely, do not use sales-process weakness as a blanket excuse for poor media quality.

### AUTO-10 Creative learning for vehicles

Creative hypotheses may involve vehicle identity, condition, features, price/offer framing, use case, proof, inspection/transparency, financing/trade messaging, and urgency. The learning target is downstream business response, not merely CTR or engagement.

For used or unit-specific inventory, creative truthfulness and freshness are first-class constraints. A high-CTR creative that attracts shoppers under a misleading price or vehicle representation is a failure, not a win.

### AUTO-11 Automotive diagnosis fault tree

Start with the parent core fault tree and add automotive-specific branches:

`inventory truth/availability -> merchandising/feed/listing integrity -> media delivery -> lead/contact capture -> CRM identity/source -> appointment/show -> sales process -> finance/trade/offer friction -> sale/delivery -> gross/contribution`

Acquire discriminating evidence before changing spend. A sudden CPA increase can be a sold-out vehicle, broken listing, feed rejection, CRM incident, price change, sales follow-up issue, or real demand/auction change.

### AUTO-12 Handoffs and operating records

A strong automotive paid-media handoff should identify, where material:

- exact inventory population or offer population affected;
- data freshness and source of price/availability/vehicle facts;
- downstream outcome definition and lag;
- allocation decision and marginal rationale;
- sales/operations dependency;
- claim/compliance dependencies;
- stop/rollback condition;
- authority owner for spend, pricing, inventory, finance claims and legal approval.

## Tool-use principles

Tools may include inventory/DMS or stock systems, CRM, call/message tracking, analytics/warehouse, feed management, experimentation/measurement systems, ad platforms, and BI. Tool names are not stable professional knowledge.

Before using a tool output as decision evidence, establish what entity it represents (shopper, lead, appointment, vehicle, deal, sale), its freshness, deduplication/source rules, and whether it is authoritative for that fact.

Write actions that change spend, vehicle price, availability, listing content, finance claims, or customer records require the corresponding delegated authority and organization controls.

## Domain-specific feedback loops

`inventory/offer state -> merchandising truth -> paid-media exposure -> vehicle/listing engagement -> lead/contact -> appointment/show -> sale/delivery -> unit economics -> inventory state`

Capture false positives such as cheap leads with no shows, high CTR on misleading offers, and attributed sales that would likely have happened without paid media. Capture false negatives such as media-originated shoppers whose source was overwritten in CRM.

## Live-context boundary

Must be verified at use time when material:

- platform-specific vehicle-ad/feed schemas, product availability and bidding mechanics;
- jurisdiction-specific dealer licensing, price/fee, finance/lease, privacy/consent and advertising rules;
- OEM/co-op rules and current incentive eligibility;
- current market prices, demand, inventory benchmarks, media costs and competitor offers;
- organization-specific DMS/CRM semantics and approval limits.

## Explicit exclusions

This specialization does not contain UAE-specific rules, Meta Ads execution, WhatsApp lead operations, one dealership's economics or CRM conventions, a named vehicle campaign, or current platform UI instructions.