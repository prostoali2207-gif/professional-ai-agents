# Landing Messaging / Content Professional Gap Analysis

Status: research artifact — not a SKILL, not a qualification, not production-ready.
Date: 2026-08-21
Target applied system: `prostoali2207-gif/auto-parts-landing`
Architect method: reconstruct work first; do not create a role from title matching.

## 1. Observed target-system gap

The current landing repository routes work across Conversion, UX Architecture, Visual Taste / Visual Direction, Frontend, UI Guard, QA, plus a separate Brand Identity agent that is currently not present in the main AGENTS.md routing list.

The current Conversion Agent explicitly owns commercial funnel diagnosis, value-proposition/CTA/trust/objection decisions, prioritization, metrics and change contracts. It does not currently own production of final customer-facing copy as a distinct professional craft. UX Architecture owns interaction and field/helper/error behavior; Visual roles own visual hierarchy/art direction; Frontend owns implementation.

Material work therefore lacks a clearly accountable owner for:
- turning evidence and customer language into final page messaging;
- headline / subhead / proof / objection / CTA wording;
- message hierarchy and information sequencing at sentence/section level;
- voice-of-customer language mining and terminology choice;
- distinguishing persuasion copy from unsupported claims;
- creating materially different message concepts before convergence;
- copy critique and revision against comprehension, credibility, relevance and action;
- copy-specific experimental variants and acceptance criteria;
- handoff of exact approved copy without taking over CRO strategy, UX interaction or visual design.

This is not equivalent to generic 'write better copy'.

## 2. Profession reconstruction

The closest real work is a bounded combination of:
- conversion copywriting;
- content design / UX writing;
- message strategy / customer-language research.

The professional output is not merely prose. It is a message system that translates an evidence-backed commercial proposition and user task into exact customer-facing language that is understandable, credible, differentiated, scannable and action-oriented.

A strong practitioner must separate:
- business claim / proposition;
- evidence supporting the claim;
- user need and entry context;
- customer vocabulary;
- information hierarchy;
- persuasive framing;
- interaction microcopy;
- factual / legal / operational constraints;
- testable variants.

## 3. Hidden and boundary-critical competencies

### CORE
1. Customer-language evidence extraction
   - identify recurring vocabulary, anxieties, desired outcomes and decision criteria from customer conversations, search/query data, CRM notes, reviews or other valid evidence;
   - distinguish direct evidence from marketer inference.

2. Message hierarchy
   - decide what the visitor must understand first, what earns belief next, what objections need answering, and what action follows;
   - preserve scannability and mobile comprehension.

3. Value-proposition expression
   - express a CRO-approved proposition clearly without silently changing the commercial strategy.

4. Persuasive copy craft
   - headlines, subheads, proof framing, objection handling, CTA labels, transition copy and concise body copy;
   - vary mechanism and framing, not only synonyms.

5. Evidence / claim integrity
   - no fabricated proof, urgency, guarantees, availability, prices, fitment certainty, delivery times or social proof;
   - calibrate language to evidence strength.

6. Critique and revision
   - diagnose weak specificity, abstraction, jargon, claim inflation, buried value, cognitive load, genericness and mismatch with user language;
   - revise causally rather than cosmetically.

7. Copy experiment design
   - produce variants tied to a falsifiable messaging hypothesis, primary metric and guardrail supplied by or aligned with CRO.

### BOUNDARY-CRITICAL
8. UX microcopy compatibility
   - exact labels/helper/error/success text must match the interaction model and not contradict UX states.

9. Accessibility / plain-language compatibility
   - comprehensible wording, familiar terms, readable scanning structure, no reliance on cleverness that obscures action.

10. Brand / tone compatibility
   - express the brand without replacing message clarity with tone theatre.

11. Domain terminology judgment
   - automotive parts language such as VIN, OEM / part number, fitment and part identification requires correct simplification and alternatives for non-experts.

## 4. Evidence reviewed

### External professional evidence
- GOV.UK Content Design guidance: content starts from valid user needs and should help users quickly find what they need to know or do. It recommends grounding needs in evidence such as analytics, support/call-centre data and prior research, and writing in language users recognize.
  - https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/understand-content-design/
  - https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/identify-user-needs/
- Nielsen Norman Group: web users scan rather than read linearly; web writing should be succinct and scannable; interface language should use words and concepts familiar to users.
  - https://www.nngroup.com/articles/be-succinct-writing-for-the-web/
  - https://media.nngroup.com/media/articles/attachments/Heuristic_Summary_Letter_compressed.pdf
- Baymard research: field labels and microcopy materially affect comprehension and abandonment; labels should remain understandable in context and explanations can reduce confusion/anxiety around requested information.
  - https://baymard.com/learn/form-design
  - https://baymard.com/learn/ux-writing

### Internal evidence
- `auto-parts-landing/AGENTS.md`: current routing gives Conversion commercial ownership, UX interaction ownership, Visual aesthetic ownership, Frontend implementation, UI Guard rendered visual gate and QA release gate.
- `auto-parts-landing/.agents/skills/conversion-agent/SKILL.md`: defines diagnosis, hypothesis, prioritization and change-contract responsibility, but not a dedicated craft/evaluation model for final customer-facing copy.
- `auto-parts-landing/.agents/skills/ux-architect/SKILL.md`: includes labels/helper/error behavior as part of interaction design, creating a boundary that a messaging practitioner must respect rather than duplicate.
- `auto-parts-landing/DESIGN.md`: current visual contract already requires headline/CTA communication and concise process copy, but it is a design contract, not a professional copy system.
- Professional Core Library currently contains qualified cores for paid media, video post-production and growth experimentation/measurement; no plausible copy/content/messaging core is available for direct reuse.

## 5. Alternatives considered

### Alternative A — EXTEND the current Conversion Agent
Benefits:
- fewer agents and handoffs;
- commercial diagnosis and copy remain tightly coupled;
- lower coordination/context cost.

Risks:
- conflates deciding what commercial behavior/message should change with the distinct craft of producing and critiquing exact language;
- broadens the Conversion role toward a 'super-agent';
- makes independent critique of messaging harder;
- current Conversion qualification would no longer support the expanded behavior without new targeted evaluation.

### Alternative B — BUILD a bounded reusable Messaging / Conversion Copy professional core
Benefits:
- coherent output boundary: exact customer-facing message system;
- reusable across landing pages and campaigns without inheriting Spline-specific facts;
- permits independent craft evaluation and pairwise copy critique;
- clean handoff: CRO decides commercial problem/hypothesis; Messaging produces language; UX owns interaction; Visual owns presentation.

Risks:
- extra handoff/context cost;
- possible overlap with UX writing and CRO unless authority is explicit;
- subjective quality requires stronger evaluation than a prose rubric.

### Alternative C — no AI professional; use templates/rules only
Useful for deterministic constraints such as banned claims, character limits, required labels or terminology checks. Insufficient for evidence synthesis, message hierarchy, divergent framing and contextual copy judgment.

## 6. Provisional architecture decision

`BUILD NEW`, provisionally, as a bounded reusable professional core tentatively named **Conversion Messaging & Web Copy Practitioner**.

This is not yet permission to implement a production SKILL. The case for a distinct core is stronger than simply extending Conversion because the work has its own coherent artifacts, tacit craft, critique loop and evaluation needs. The boundary must remain narrow enough to avoid becoming a second CRO or UX agent.

### Proposed authority boundary
Messaging owns:
- customer-language synthesis;
- message hierarchy within an approved commercial intent;
- exact headline/body/proof/objection/CTA/microcopy proposals;
- copy variants and copy critique;
- copy handoff and copy-specific acceptance criteria.

Messaging does not own:
- KPI selection, CRO root-cause diagnosis or experiment priority;
- user-flow/form architecture;
- visual design;
- frontend implementation;
- fabricated business claims;
- autonomous publishing.

## 7. Knowledge packaging candidates

EMBED_CORE:
- claim/evidence discipline;
- message hierarchy principles;
- customer-language vs marketer-language distinction;
- copy critique model;
- divergence/convergence rules;
- boundary contracts with CRO/UX/brand.

PROCEDURAL_MODULE:
- voice-of-customer evidence mining;
- landing-page message architecture;
- headline/value-proposition exploration;
- objection/proof copy;
- CTA and microcopy design;
- copy experiment construction;
- critique/revision.

LIVE_RESEARCH / TOOL_BACKED when material:
- current customer/search language;
- market/category terminology;
- competitor messaging as pattern evidence only;
- regulated or volatile claims;
- real analytics/CRM/customer evidence.

## 8. Evaluation implications

A credible qualification must not grade only whether prose 'sounds persuasive'. It should include:
- customer-language evidence grounding;
- unsupported-claim traps;
- weak/generic value proposition diagnosis;
- jargon-to-user-language tasks;
- materially different message concepts;
- mobile/scannability constraints;
- CRO/UX boundary tests;
- adversarial stakeholder requests for fake urgency/social proof;
- copy critique and revision;
- artifact-first comparison of alternative landing copy;
- deterministic checks for prohibited claims and required facts;
- calibrated comparative/human review for subjective craft dimensions.

## 9. Red-team

Senior practitioner criticism to guard against:
- 'This is just a copywriter prompt with a fancy name.' -> require evidence mining, message architecture, critique, experiment linkage and observable artifacts.
- 'The CRO already owns this.' -> preserve CRO ownership of commercial diagnosis and hypothesis; messaging owns exact language craft.
- 'UX writing already covers microcopy.' -> keep interaction semantics under UX; messaging supplies wording within the approved state/interaction model.

Teacher criticism:
- competency labels without observable tasks are insufficient -> each material competence needs eliciting fixtures and graders.
- subjective writing quality is not reliably captured by one LLM rubric -> use pairwise/comparative evaluation and calibrated expert review where feasible.

Hiring-manager criticism:
- a strong copy practitioner must show ability to work from messy customer evidence, not just write from a clean brief;
- must preserve truth under pressure;
- must produce copy that can actually be tested and shipped.

## 10. Unknowns before candidate build

- Need a deeper source/evidence pass on conversion copy / content design craft and customer-language research methods.
- Need to inspect any existing research artifacts in the landing repository that may already cover voice-of-customer or messaging.
- Need to determine whether Spline has enough real customer/CRM/search evidence to evaluate customer-language synthesis now; if not, qualification must include controlled evidence fixtures rather than inventing business facts.
- Need a separate routing decision for the existing Brand Identity Agent, which currently exists but is omitted from top-level AGENTS.md routing.

No production agent should be declared ready from this document alone.
