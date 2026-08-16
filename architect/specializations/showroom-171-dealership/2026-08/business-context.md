# Showroom 171 Dealership Paid Media Business Context

Status: candidate 2026-08

Parents:
- `paid-media-performance-marketing@1.0.0`
- `automotive-paid-media@1.0.0`
- `uae-meta-whatsapp-automotive/2026-08`

Snapshot date: 2026-08-16

## Boundary

This is an organization-specific operating layer for the used-car showroom currently represented in project context as **Ajman Auto Market, Showroom 171**. It does not replace the qualified professional core, automotive specialization, or UAE/Meta/WhatsApp live-context layer. It supplies only dealership facts, local operating constraints, unresolved business inputs, and decision policies that depend on this organization.

It is not a Toyota Yaris campaign and contains no vehicle-specific launch plan.

## Verified / established business facts

The following are treated as established project facts for this snapshot:
- business type: used-car showroom / automotive retail;
- physical market: Ajman, UAE; showroom context: Ajman Auto Market, Showroom 171;
- Instagram is the primary current social/acquisition surface;
- WhatsApp is the primary direct lead/conversation destination discussed for paid acquisition;
- the business is early-stage on Instagram rather than an account with mature first-party paid-media history;
- human approval/publishing remains part of the current operating system;
- the separate `auto-sales-growth-system` repository is designed to connect market/content experiments to qualified leads, appointments and vehicle sales, but its current main explicitly describes the system as contract-ready rather than production-ready and says verified inventory/commercial facts plus publication/attribution/inquiry/outcome data still need to be connected.

## DEALER-01 No invented economics

Current project context does **not** establish a durable dealership-level value for:
- gross profit per sold vehicle;
- contribution margin after reconditioning, commissions, finance costs, logistics, warranty or other variable costs;
- acceptable CAC / cost per qualified lead / cost per appointment;
- daily or monthly paid-media budget;
- cash-flow constraint;
- maximum marginal CAC for a specific unit;
- authority limit for spend changes.

Therefore no practitioner may infer profitability from cheap message CPL, cheap lead CPA, list price, or expected sale price alone.

Before material scale, require the minimum economics needed for the decision. If exact margin is unavailable, define a bounded test with an explicit learning budget and human approval instead of manufacturing ROI.

## DEALER-02 Inventory is unit-specific and authoritative inventory is unresolved until supplied

Every direct-sale campaign must be attached to a verified current vehicle record. The dealership layer must not treat a prior reel, old caption, chat message, or previous experiment as authoritative inventory merely because it already contains a price/specification.

For each vehicle, obtain or verify at execution time where material:
- exact identity/model/year/trim/spec;
- current availability/status;
- current approved sellable price;
- mileage;
- GCC/import status;
- condition/repair/accident disclosures that materially affect the offer;
- finance/warranty claims if any;
- approved media and current vehicle state.

Sold, reserved, repriced or materially changed vehicles invalidate previous execution assumptions.

## DEALER-03 Lead quality hierarchy

For this showroom, platform conversation/message count is a proxy only. Prefer, when trustworthy data exists:

`sale / gross contribution -> qualified lead -> appointment/test drive -> show -> qualified WhatsApp conversation -> raw message/conversation start`

Do not scale because Instagram/Meta reports cheaper conversations if qualification, appointment or sale quality degrades.

## DEALER-04 Current measurement maturity

Because the growth-system repository is not yet production-ready and its README states that verified inventory/commercial facts and publication/attribution/inquiry/outcome data still need connection, the default assumption is **measurement incompleteness**, not end-to-end attribution readiness.

Operational implications:
- do not claim reliable sale attribution until the experiment can be reconstructed from publish/source through lead and outcome records;
- preserve vehicle context and source in WhatsApp/CRM handoff;
- do not overwrite original acquisition source;
- manually reconcile paid leads and downstream outcomes if necessary for an early experiment;
- treat missing attribution as a measurement limitation, not as zero sales or proof of campaign failure.

## DEALER-05 Capacity and response-time unknowns

Current project context does not establish stable values for:
- number of salespeople handling paid leads;
- business-hour response SLA;
- simultaneous WhatsApp lead capacity;
- appointment/test-drive capacity;
- after-hours ownership;
- language coverage by sales staff.

Do not scale lead volume beyond observed handling capacity. Before a material increase, verify response time, ownership, backlog, appointment capacity and actual lead follow-up quality. **Before any `SCALE` decision expected to increase lead volume, explicitly confirm that current sales/appointment handling capacity is adequate; do not treat capacity as implicitly satisfied merely because economics are attractive.**

## DEALER-06 Geography and language remain hypotheses until internal evidence

The showroom is physically in Ajman, but that does not prove that Ajman-only, all-UAE, English-only, Arabic-only, Russian-only or CIS-oriented targeting is optimal.

Use actual serviceability, buyer travel behavior, delivery/export capability, language handling and lead-to-sale evidence. Small bounded geography/language tests are allowed when evidence is weak. Large-scale targeting by habit is not.

## DEALER-07 Commercial truth and approval

A vehicle price, finance/payment claim, warranty, accident/paint status, GCC/import status, mileage, availability, shipping/export promise or condition statement is a commercial fact requiring current evidence and business approval.

A number proposed by the user, prior chat, prior creative, salesperson memory or another agent is not automatically approved truth.

If a material fact is unverified, the next action is to verify/hold/iterate, not to convert uncertainty into persuasive copy.

## DEALER-08 Experiment-budget discipline

Until dealership economics are connected, paid media should operate as bounded learning experiments rather than open-ended scaling.

Each experiment must define:
- decision question;
- maximum approved spend or stop-loss supplied by business authority;
- primary downstream success metric;
- minimum tracking required to make the result interpretable;
- stop / iterate / scale rule;
- what new evidence the test is expected to produce.

The practitioner must not invent a numeric budget. If no budget is supplied, recommend the information needed and keep the decision blocked at execution authority.

## DEALER-09 Cross-repo operating handoff

`professional-ai-agents` owns this professional/business decision layer. `auto-sales-growth-system` owns the dealership growth workflow and experiment artifacts. Do not duplicate its orchestration agents here.

When this layer is used operationally, hand off only verified organization-specific facts, decision constraints and approved experiment parameters. Preserve source revision and evidence status.

## DEALER-10 Authority

The practitioner may recommend media structure, measurement, experiments and budget changes, but may not silently decide dealership commercial facts or spend authority.

Human/business authority is required for at least:
- approved selling price and offer terms;
- vehicle truth when records conflict;
- material spend ceiling / stop-loss;
- finance/warranty/condition claims;
- customer-data use where organizational approval is required;
- operational commitments such as delivery/export promises.

## DEALER-11 Mandatory scale checklist

A dealership-context recommendation to `SCALE` is invalid unless the practitioner explicitly confirms all three of the following in the decision:
1. **marginal business value** — expected marginal acquisition economics remain favorable using verified business economics, not average platform CPA alone;
2. **delegated authority** — the proposed spend increase is within an explicit approved authority limit;
3. **operational capacity** — current lead-response and appointment handling can absorb the expected incremental volume without degrading downstream quality.

If any one of these is unknown, do not label the decision `SCALE`. Use HOLD / EXPERIMENT / ITERATE / ESCALATE as appropriate until the missing evidence is resolved.

## Explicit unknowns that block confident scale

Until supplied and verified, treat these as unknown:
- dealership gross/contribution economics;
- approved paid-media budget and delegated spend authority;
- trustworthy end-to-end paid lead -> appointment -> sale attribution;
- sales-team response/capacity baselines;
- stable audience/geography/language winner;
- authoritative live inventory integration.

Unknowns do not block every experiment. They block only decisions that require them. Use the smallest bounded experiment capable of resolving the decision without hiding uncertainty.

## Revalidation triggers

Revalidate this layer when the showroom identity/location, sales team, lead workflow, budget authority, inventory system, CRM/attribution stack, languages served, delivery/export capability or business economics change materially.

## Explicit exclusions

No Toyota Yaris campaign, no exact Yaris price, no vehicle-specific creative, no invented ad budget, no invented margin, and no assumption that the current Instagram/WhatsApp path is permanently optimal.