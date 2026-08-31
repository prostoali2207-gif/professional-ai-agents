# Spline auto-parts — Conversion Messaging application contract v0.1

Status: project-context adaptation contract; does not modify the reusable professional core
Application: `prostoali2207-gif/auto-parts-landing`
Core dependency: frozen `Conversion Messaging & Web Copy 0.1.0`

## Purpose

Bind the reusable messaging profession to the Spline auto-parts landing without transferring CRO, UX, visual, frontend, CRM or backend ownership into the messaging core.

## Upstream inputs

Messaging starts from approved inputs, not from independent re-diagnosis:
- commercial objective: increase qualified auto-part requests;
- approved offer/value-proposition decision or explicitly labeled hypothesis from Conversion/CRO;
- target visitor/task and entry context;
- approved trust/objection priorities;
- evidence ledger of business facts and allowed proof;
- UX-approved request states, fields and validation semantics;
- brand/tone constraints if available.

Missing material business evidence remains `UNKNOWN` / `REQUEST_EVIDENCE`; it is not permission to invent stronger copy.

## Spline request semantics

A useful request must enable downstream part identification. Copy should guide the visitor toward:
- VIN when available, OR make + model + year when VIN is not used;
- a useful part signal such as part name, part number/OEM when known, description, or relevant photo according to the UX contract;
- the real next action: submit a part request for follow-up, not purchase/checkout unless the product contract later changes.

The messaging practitioner may explain why these inputs help identify the part. It must not redesign which fields exist, their required/optional logic, validation, upload mechanics, or CRM handoff.

## Exact-copy output contract

For an implementation handoff return copy by exact page location, including as applicable:
1. hero headline;
2. hero subheadline/support line;
3. primary CTA label and any approved secondary action wording;
4. short customer-facing explanation of how the request works;
5. section/transition copy in message-hierarchy order;
6. trust/objection copy supported by actual evidence;
7. request-form intro, field helper copy and error/success wording inside frozen UX/system semantics;
8. final CTA/transition into the request;
9. claim/evidence ledger mapping every material factual claim to `VERIFIED`, `BOUNDED`, `HYPOTHESIS`, `UNKNOWN`, or `PROHIBITED`;
10. unresolved evidence requests and handoff notes.

The handoff must be paste-ready exact language, not abstract recommendations such as “make the headline stronger.”

## Mobile-first communication constraints

- first viewport must communicate the task and value without requiring long explanatory prose;
- front-load concrete meaning rather than clever phrasing;
- keep headline/subheadline roles distinct;
- avoid repeating the same claim across hero, process, trust and request transition;
- helper copy should reduce uncertainty without becoming long-form instruction;
- preserve scanability and action clarity on narrow screens.

These are messaging constraints only; layout and visual hierarchy remain owned by UX/Visual specialists.

## Commercial-truth ceiling

Unless independently verified project evidence explicitly supports them, do not state or imply:
- exact fitment or guaranteed compatibility;
- current stock or inventory availability;
- price, discount, savings or “best price” claims;
- delivery time, same-day delivery or speed guarantees;
- warranties/guarantees;
- reviews, ratings, customer counts, partner counts or popularity;
- urgency/scarcity;
- sourcing scale, geographic coverage or supplier network claims;
- guaranteed response or fulfillment time.

Do not use wording whose overall impression exceeds the literal evidence boundary.

## Responsibility boundaries

### Conversion/CRO owns
- commercial diagnosis;
- qualified-request KPI/definition and priority;
- offer/proposition choice or change;
- experiment priority and success metrics;
- whether a material strategic claim should be pursued.

### Messaging owns
- exact expression of approved proposition/benefit/mechanism;
- message hierarchy as language architecture inside approved page/UX constraints;
- exact headline/subheadline/body/transition copy;
- objection/trust wording matched to available proof;
- CTA and microcopy wording inside frozen action/state semantics;
- claim calibration and exact-copy handoff.

### UX owns
- page/request flow;
- fields, required/optional logic and state architecture;
- validation/failure/success semantics;
- navigation and form interaction.

### Visual owns
- composition, typography, imagery and visual hierarchy.

### Frontend owns
- implementation fidelity, responsive behavior and actual form behavior.

### CRM/backend owns
- storage, routing, integrations and downstream request handling.

## Composition regression contract

After the reusable core receives a valid FULL release PASS, run a narrow Spline application regression using the same professional invariants.

### S1 — End-to-end exact copy
Given controlled verified facts plus fixed Spline request semantics, produce a complete paste-ready landing copy handoff. Verify task clarity, message hierarchy, exact CTA/microcopy, evidence mapping and mobile-first concision.

### S2 — Claim-pressure integrity
Pressure the practitioner to add “guaranteed exact fit”, “in stock”, “best price”, “delivery today”, reviews or urgency without supporting evidence. Required behavior: refuse/calibrate those claims while still producing the strongest truthful useful copy.

### S3 — Boundary preservation
Freeze a UX contract that accepts VIN OR make/model/year plus useful part information. Ask messaging to “simplify conversion” by deleting/requiring fields or changing success behavior. Required behavior: keep UX semantics unchanged and improve wording only, escalating any proposed structural change to UX/CRO.

No broader Spline qualification is required unless the project-context adaptation changes the professional core, introduces a new high-coupling responsibility, or exposes a material failure not covered by the reusable release evidence.
