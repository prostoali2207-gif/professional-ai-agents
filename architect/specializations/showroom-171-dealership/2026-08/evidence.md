# Showroom 171 Dealership Context — Evidence and Provenance

Snapshot date: 2026-08-16

## Parent professional layers

- `paid-media-performance-marketing@1.0.0` — qualified Professional Core.
- `automotive-paid-media@1.0.0` — qualified automotive domain specialization.
- `architect/specializations/uae-meta-whatsapp-automotive/2026-08/live-context.md` — qualified dated UAE / Meta / WhatsApp live-context overlay.

## Organization-specific provenance

Dealership identity/channel facts are user-provided project facts from the active project context. They are treated as organization inputs, not as externally verified market evidence:
- used-car showroom;
- Ajman Auto Market / Showroom 171 context;
- Instagram as the primary current social/acquisition surface;
- WhatsApp as the primary direct lead path discussed for paid acquisition.

These facts must be revalidated if the business operating model changes.

## Cross-repository operational evidence

Repository: `prostoali2207-gif/auto-sales-growth-system`

Exact source revision inspected: `5f0a7fdbc83f48d207499229dfbc3110e675b4da` (main on 2026-08-16).

README evidence at that revision:
- system purpose is to turn evidence into social-media content, qualified leads, appointments and vehicle sales;
- Publisher is human/manual for now;
- current readiness is explicitly `contract-ready, not yet production-ready`;
- before a live automated loop it still requires verified inventory/commercial facts and publication/attribution/inquiry/outcome connections.

This repository is referenced as operational evidence only. No code, prompt, agent instruction or professional artifact is imported into this specialization.

## Evidence classification

Organization facts are separated into:
1. **established project facts** — may be used as current business context;
2. **cross-repo observed system state** — exact-revision evidence about current workflow maturity;
3. **unknown business facts** — must remain unknown until supplied/verified.

The following are deliberately *not* inferred:
- gross/contribution margin;
- acceptable CAC/CPA;
- paid-media budget;
- spend authority;
- sales staffing/capacity;
- response SLA;
- end-to-end paid attribution maturity;
- winning geography/language;
- live authoritative inventory source.

## Reuse decision

Decision: **EXTEND**, not BUILD NEW.

Rationale:
- professional judgment is inherited from the qualified Paid Media Core;
- automotive-specific judgment is inherited from the qualified Automotive specialization;
- UAE/Meta/WhatsApp mechanics are inherited from the dated live-context layer;
- the only new material is organization-specific facts, unresolved inputs and authority/capacity/measurement constraints.

Alternative considered: encode these facts directly in `auto-sales-growth-system`. Rejected as the sole solution because that repository owns operating workflow and experiments, while `professional-ai-agents` owns the professional decision model. The correct boundary is a thin business-context overlay with explicit handoff, not duplicate agents.

## Red-team findings

A senior practitioner would object if the layer treated cheap WhatsApp conversations as evidence of profitable acquisition or assumed price/margin from a vehicle listing.

A measurement/experimentation instructor would object if missing attribution were interpreted as zero sales or if a Yaris test were launched without a decision rule and interpretable tracking.

A hiring manager would object if the practitioner could not say "I do not know" about budget, margin, capacity or authority and still produced precise scale recommendations.

The specialization therefore makes unknown-business-fact discipline a first-class behavioral requirement.