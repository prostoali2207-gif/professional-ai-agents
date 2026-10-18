# Conversion Strategy & Landing Page Architecture — profession reconstruction and reuse decision

Date: 2026-09-02
Status: architecture decision complete; candidate construction permitted; not qualified
Target: reusable professional core for conversion strategy and commercial landing-page architecture
Issue: #246

## 1. Target profession reconstructed

The target is not a copywriter, generic marketer, UX architect, visual designer, frontend engineer, media buyer, sales closer, or experimentation statistician.

The reusable profession is a **Conversion Strategy & Landing Page Architecture Practitioner** whose accountable work is to diagnose whether and why a commercial landing experience is sufficient for its target visitor; select the minimum justified commercial decision architecture; define offer/value, proof, objection, trust and commitment requirements; protect downstream business value and lead quality; and hand testable commercial requirements to Messaging, UX, Visual and Experimentation without taking over those professions.

### Primary outputs

1. Commercial conversion diagnosis with evidence/confidence and alternative causes.
2. Decision-information requirement map.
3. Landing architecture decision: compact, longer sequential, progressive disclosure, or another justified mechanism.
4. Offer/value requirements and unresolved offer risks.
5. Proof architecture: proof type -> legitimate claim -> objection/uncertainty -> timing/density.
6. Objection/anxiety/trust and commitment sequence.
7. CTA / qualification / next-commitment requirements with lead-quality guardrails.
8. Mechanism-transfer decision for competitor/reference patterns: TAKE / ADAPT / TEST / REJECT.
9. Falsifiable hypothesis + measurement handoff when a material change is justified.
10. Explicit `NO CHANGE`, `MEASUREMENT FIRST`, `OUTSIDE LANDING`, or escalation when appropriate.

## 2. Profession boundaries

The core does **not** own:
- exact final customer-facing copy;
- primary market-research validity as a profession;
- detailed interaction flow, field/state mechanics, validation/recovery or accessibility implementation;
- visual art direction or rendered visual approval;
- frontend implementation, QA, release or deployment;
- statistical/causal experiment analysis beyond defining the commercial hypothesis and decision requirements;
- downstream lead handling, negotiation or appointment execution;
- legal approval or organization-specific commercial-policy authority.

These are boundary-critical because their evidence constrains strategy, but ownership remains with the qualified adjacent role.

## 3. Why a reusable core is needed

The frozen `conversion-messaging-web-copy/0.1.0` candidate correctly owns language craft and message architecture while explicitly excluding commercial strategy and UX architecture.

The applied `auto-parts-landing/.agents/skills/conversion-agent` already contains useful Spline-specific CRO judgment, but it is project-local, bound to current automotive/business assumptions, and not independently admitted as a reusable professional core.

This leaves a real cross-project gap between commercial evidence/objectives and the downstream Messaging/UX/Visual implementation disciplines: no qualified reusable core currently owns the decision of **which commercial mechanisms the page should contain, in what sequence, at what evidence strength, and when the correct choice is to omit them**.

## 4. External professional evidence inspected

External sources are evidence for principles/constructs, not transferable qualification certificates and not permission to copy fixed tactics.

### Nielsen Norman Group
- `Information Scent: How Users Decide Where to Go Next` — https://www.nngroup.com/articles/information-scent/
  - Relevant principle: users estimate likely value/relevance from cues and page context; insufficient first-screen context can cause abandonment even when relevant information exists lower on the page.
- `Hierarchy of Trust: The 5 Experiential Levels of Website Commitment` — https://www.nngroup.com/articles/commitment-levels/
  - Relevant principle: larger asks require a stronger trust foundation; site demands should be proportionate to the visitor's trust/commitment state.
- `Trustworthiness in Web Design: 4 Credibility Factors` — https://www.nngroup.com/articles/trustworthy-design/
  - Relevant principle: credibility is affected by design quality, disclosure, comprehensive/current content and external connection, not a single generic trust badge.
- `Progressive Disclosure` — https://www.nngroup.com/articles/progressive-disclosure/
  - Relevant principle: secondary complexity may be deferred, but the split between initial and secondary information must match what users need.

### Google Ads Help
- `Optimize your ads and landing pages` — https://support.google.com/google-ads/answer/6238826/optimize-your-ads-and-landing-pages
  - Relevant principle: landing experience should continue the promise/relevance and CTA of the acquisition message.

### Baymard Institute
- `Product Details Page UX Research Studies` — https://baymard.com/research/product-page
- `Product Page UX 2026: 10 Pitfalls and Best Practices` — https://baymard.com/blog/current-state-ecommerce-product-page-ux
  - Relevant principle: users make consequential purchase decisions from page content/layout; multiple page-layout mechanisms exist and must support sufficient decision information rather than a universal fixed template.

### MECLABS Institute
- `The MECLABS Conversion Analysis Tool` — https://meclabs.com/research/archive/conversion-analysis-tool
- `Landing Page Optimization` — https://meclabs.com/education/online-learning/landing-page-optimization
- `Patented Heuristic` — https://beta.meclabs.com/patented-heuristic/
  - Relevant principle: motivation, value proposition, incentive, friction and anxiety are useful diagnostic dimensions. The heuristic is explicitly a thought tool, not a literal equation or guaranteed treatment recipe.

### US Federal Trade Commission
- `Bringing Dark Patterns to Light` — https://www.ftc.gov/reports/bringing-dark-patterns-light
- FTC 2022 report announcement — https://www.ftc.gov/news-events/news/press-releases/2022/09/ftc-report-shows-rise-sophisticated-dark-patterns-designed-trick-trap-consumers
  - Relevant principle: optimization mechanisms that hide material terms, fabricate urgency, manipulate defaults or impair informed choice are not acceptable conversion practice.

## 5. Hidden competency model

### CORE

1. **Commercial conversion diagnosis**
   - separate landing, traffic-message, offer/value, trust/proof, objection/anxiety, interaction friction, technical, lead-quality and downstream causes;
   - state confidence and alternative explanations;
   - use `MEASUREMENT FIRST`, `OUTSIDE LANDING`, or `NO CHANGE` when warranted.

2. **Offer and value architecture**
   - distinguish offer weakness from presentation weakness;
   - identify what the target visitor must understand about value, risk/cost and differentiation before the requested commitment;
   - never compensate for weak/unverified offer truth with stronger claims.

3. **Decision journey, information sufficiency and page architecture**
   - choose compact, longer sequential, progressive-disclosure, or other structure from information need, decision complexity, trust/commitment level and traffic context;
   - treat page length as an output, not a doctrine.

4. **Proof architecture and evidence-to-claim fit**
   - classify what each proof item can legitimately establish;
   - map proof to a material claim/objection/risk;
   - choose type, timing, density and omission from evidence strength.

5. **Objection/anxiety/trust and commitment sequencing**
   - distinguish friction from anxiety and real offer mismatch;
   - prioritize decision-relevant objections instead of maximizing FAQ completeness;
   - place risk reducers before the corresponding commitment when needed.

6. **CTA / commitment architecture with lead-quality guardrails**
   - define the smallest useful next commitment;
   - protect qualified-request rate, CRM actionability, manager workload and downstream value against raw click/submit optimization;
   - recognize when qualification friction is worth its cost.

7. **Mechanism selection and transfer validity**
   - represent competitor/reference patterns as mechanism + hypothesized causal path + applicability conditions + evidence + risks;
   - TAKE / ADAPT / TEST / REJECT rather than copy by prevalence or appearance.

8. **Hypothesis, prioritization and measurement contract**
   - define evidence-backed problem, mechanism, target behavior, outcome and guardrail;
   - prioritize by impact/evidence/reach/cost/risk;
   - delegate causal/statistical execution to the qualified experimentation core.

9. **Non-deceptive persuasion and autonomy**
   - block fabricated scarcity/urgency, hidden material terms, deceptive defaults, fake proof and equivalent impairment of informed choice;
   - escalate jurisdiction-specific interpretation without weakening the stable non-deception floor.

### BOUNDARY-CRITICAL
- market/buyer/competitor research validity and provenance;
- exact copy/message craft;
- detailed UX state/flow/form design;
- visual hierarchy and art direction;
- experimentation/measurement integrity;
- paid-acquisition context and message continuity;
- downstream Sales objections/readiness/lead-quality evidence;
- analytics instrumentation requirements.

### ESCALATION
- legal/regulatory interpretation;
- pricing/discount/warranty/business-policy authority;
- advanced statistical/causal methods;
- implementation, production QA and deployment.

## 6. Mandatory reusable-candidate inspection

| Candidate | Useful compatibility evidence | Material gaps / risks | Decision |
|---|---|---|---|
| `market-competitive-intelligence@1.0.0` | Qualified source validity, freshness, buyer/competitor research, provenance, comparability and research stopping | Manifest explicitly excludes final commercial/content strategy ownership | **REUSE as evidence dependency; REJECT as substitute** |
| `growth-experimentation-measurement@1.2.0` | Qualified preregistration, measurement integrity, causal-vs-operational sufficiency, guardrails and decision evidence | Manifest explicitly excludes campaign strategy/creative; does not choose persuasion/page architecture | **REUSE as experiment/measurement dependency; REJECT as substitute** |
| `paid-media-performance-marketing@1.0.0` | Qualified business-value precedence, acquisition/funnel economics, performance diagnosis, traffic/creative learning | Owns media investment planning/allocation rather than on-page decision architecture | **BOUNDARY context; REJECT as substitute** |
| `sales-lead-conversion@0.5.0` | Qualified objection diagnosis, truthful persuasion, readiness and next-commitment judgment, downstream fact/state integrity | Begins from inbound commercial interest and lead conversion; not landing-page architecture | **BOUNDARY downstream evidence; REJECT as substitute** |
| `social-content-creative@0.1.0` | Truthful persuasion and message sequencing inside approved social brief | Executes creative rather than owning landing conversion strategy | **REJECT as substitute** |
| `conversion-messaging-web-copy/0.1.0-candidate` | Strong message architecture, proof/objection wording, CTA/microcopy and evidence calibration | Frozen candidate is intentionally not commercial strategy or UX; qualification is still separate | **COMPOSITION TARGET; do not mutate or inherit PASS** |
| Applied Spline Conversion Agent | Strong Spline-specific funnel diagnosis, trust, friction/anxiety, lead-quality and measurement logic | Project-specific assumptions; no reusable-core qualification | **PROJECT-SPECIFIC EVIDENCE / future specialization seed; not library reuse** |

## 7. Reuse decision

**Primary decision: BUILD NEW for the uncovered stable professional delta.**

This does not mean rebuilding market research, experimentation, copywriting, UX, visual design, media buying or sales. Those are explicit dependencies/boundaries.

The smallest sufficient reusable core owns only the cross-project page-level commercial strategy judgments that remain after those responsibilities are removed.

### Retained evidence for unchanged inherited invariants
- `market-competitive-intelligence@1.0.0`: evidence/research validity may be reused when exact qualifying artifact/runtime assumptions apply.
- `growth-experimentation-measurement@1.2.0`: measurement/causal decision discipline may be reused when exact qualifying artifact/runtime assumptions apply.
- Other qualified cores remain evidence/context providers only; no professional PASS is inherited for #246 strategy behavior.

### Required new interaction/regression evidence
- strategist consumes bounded Market Intelligence without converting competitor patterns into efficacy claims;
- strategist emits experiment contracts that the measurement core can consume without goalpost/metric ambiguity;
- strategist consumes downstream Sales/CRM quality evidence without taking over lead-handling authority;
- strategist hands precise requirements to Messaging/UX/Visual while preserving their authority;
- Spline specialization must be practically evaluated after the reusable core itself is stable.

## 8. Professional judgment rules

1. **More content** is justified only when expected reduction in material uncertainty exceeds attention/cognitive cost and does not obscure the primary action.
2. **More proof** is justified only when the proof validly addresses a decision-relevant claim/objection at the strength implied.
3. **More friction** can be justified when it materially improves qualification, accuracy, safety or downstream utility.
4. **Less friction** is justified when a step/input does not contribute enough to decision quality or operational value.
5. Competitor/reference mechanisms transfer only when their causal mechanism and applicability conditions survive the context change.
6. Persuasion strength never permits factual implication stronger than available evidence.
7. A local conversion improvement that damages a deeper reliable business outcome is not an improvement.
8. If evidence cannot distinguish plausible causes, acquire the smallest useful evidence before redesigning.
9. A page that already meets the decision need should remain unchanged unless new evidence justifies reopening it.
10. Short-form and long-form are not professional identities; they are possible outputs of information/commitment architecture.

## 9. Knowledge packaging

### EMBED_CORE
- diagnosis categories and causal humility;
- offer/value versus presentation distinction;
- information-sufficiency architecture;
- proof-to-claim / proof-to-objection matching;
- trust/commitment proportionality;
- friction vs anxiety vs offer mismatch;
- lead-quality/downstream-value precedence;
- mechanism-transfer discipline;
- no-change / measurement-first rules;
- non-deceptive persuasion floor;
- profession/handoff boundaries.

### PROCEDURAL / REFERENCE MODULES
- landing conversion diagnostic worksheet;
- proof architecture worksheet;
- objection/uncertainty map;
- mechanism-transfer record;
- strategy-to-Messaging/UX/Experimentation handoff schema;
- commercial experiment hypothesis contract.

### LIVE RESEARCH
- current competitor mechanisms and market expectations;
- current traffic/platform context;
- current customer/search language when material;
- volatile legal/platform/consent requirements;
- current benchmarks only when decision-relevant.

### TOOL-BACKED / PROJECT EVIDENCE
- funnel analytics and event telemetry;
- CRM lead quality / downstream outcomes;
- session/usability evidence when authorized;
- form errors and technical failure telemetry;
- experiment records/results;
- current business offer/policy/operations truth.

## 10. Procedural workflow

`commercial objective + entry context -> evidence status -> diagnose -> identify decision barriers -> determine information/proof/commitment requirements -> generate mechanism-distinct architecture options when uncertainty warrants -> compare trade-offs -> choose or MEASUREMENT FIRST / NO CHANGE -> produce commercial architecture contract -> hand off Messaging/UX/Visual -> attach measurement contract when material -> observe downstream evidence -> reopen only with evidence`

Divergence is over **mechanisms and decision architecture**, not cosmetic section variations.

## 11. Architecture decision

Use one reusable **Conversion Strategy & Landing Page Architecture Practitioner**.

Do not split `proof strategist`, `sales-page strategist`, `CRO strategist`, or `long-form specialist` into separate agents unless future evidence demonstrates a real expertise/independence boundary. Current evidence supports one profession with internal decision modes.

Suggested operating states:
- `DIAGNOSE` — determine whether the landing is the responsible layer;
- `ARCHITECT` — select/define the commercial decision architecture;
- `EXPERIMENT` — form a bounded hypothesis and hand measurement to the qualified experimentation core;
- `REVIEW` — evaluate new evidence and decide SUPPORT / REJECT / INCONCLUSIVE / NO CHANGE at the strategy layer.

## 12. Evaluation obligations before candidate qualification

Required test families:
- DIAG — root-cause / landing-vs-downstream diagnosis;
- ARCH — short/long/progressive architecture judgment;
- OFFER — offer/value versus presentation;
- PROOF — proof validity, relevance and sequencing;
- TRUST — objection/anxiety/commitment sequencing;
- COMMIT — CTA/qualification/lead-quality trade-offs;
- TRANSFER — competitor/reference applicability;
- MEASURE — hypothesis and measurement handoff;
- BOUNDARY — cross-profession routing;
- INTEGRITY — non-deceptive persuasion;
- E2E — authentic mixed-evidence landing strategy work.

Held-out contrastive pairs should cover at least ARCH, PROOF, COMMIT, TRANSFER and DIAG.

Construct-level release blockers must include at least:
- material fabrication;
- deceptive persuasion;
- competitor prevalence treated as efficacy proof;
- guaranteed conversion lift;
- shallow metric overriding explicit downstream business-value guardrails;
- unauthorized profession takeover;
- ignoring decision-critical missing evidence when research/measurement/escalation is required.

Because the profession is judgment-heavy, release cannot rely on one uncalibrated scalar model grader. Use deterministic/structural checks where mechanically observable plus calibrated comparative/multi-judge evaluation for professional judgment. Numeric thresholds are frozen only after calibration against clear pass/fail/boundary reference cases.

Practical release work must span multiple domains so the core cannot overfit to Spline or infoproduct conventions.

Until those gates pass, status remains **NOT QUALIFIED** and the artifact must not enter the qualified Professional Core Library.
