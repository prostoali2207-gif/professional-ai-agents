# Conversion Messaging & Web Copy — Evidence and Evaluation Architecture

Status: research artifact; candidate not frozen; no qualification claim.
Date: 2026-08-22

## Decision update

The remaining delta-research gap was whether commercial persuasion/copy experimentation requires a distinct professional judgment layer beyond generic content clarity, and how to evaluate that layer without grading prose by taste alone.

Evidence supports a bounded messaging/copy core, but rejects the stronger claim that particular copy patterns are universally conversion-improving. Message effects are contextual and must be treated as hypotheses until tested against the target audience/outcome.

## Evidence synthesis

### User-needs and language grounding
Authoritative public-service content-design guidance treats user needs as evidence-backed rather than stakeholder assumptions. ONS lists analytics, content testing, interviews, surveys, heatmaps and search terms as evidence sources and recommends prioritising information for scanning. GOV.UK explicitly says content designers are not user researchers and should use existing evidence or escalate to research/analytics when evidence is insufficient.

Implication: the Messaging core may synthesize supplied/retrieved evidence and identify gaps; it must not fabricate voice-of-customer findings or claim primary-research validity it did not obtain.

Sources:
- https://service-manual.ons.gov.uk/content/writing-for-users/user-needs
- https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/identify-user-needs/
- https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs

### Content is a distinct team capability
GOV.UK service-team guidance separates user researcher, content designer, designer and developer. Content designers develop content plans from user needs, write usable/accessibile content, review accuracy/relevance/accessibility, and challenge requests that do not support user needs.

Implication: separation from CRO/UX/Visual is professionally plausible when boundaries are explicit; title separation alone is not proof, but the output and judgment boundary is coherent.

Source:
- https://www.gov.uk/service-manual/the-team/service-manager.html

### Testing language rather than declaring it persuasive
DEFRA content-design practice includes testing different content with users, testing language in prototypes, defining jargon/acronyms and balancing business needs against evidence from user testing.

A field experiment published in a peer-reviewed venue found that headline/subheading framing effects varied by page/audience: some changes produced no behavioral difference while one targeted page showed engagement differences. This is useful counter-evidence against universal copy formulas.

Implication: a candidate can generate an evidence-backed messaging hypothesis, but cannot label a framing as a proven conversion winner without target evidence. Evaluation must reward calibration and experimentability, not confident persuasion rhetoric.

Sources:
- https://digital.defra.gov.uk/content/working-in-alpha
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7983838/

### Claim substantiation and implied meaning
FTC guidance requires a reasonable evidentiary basis for objective advertising claims before dissemination and evaluates both express and implied claims in context. Material omissions can also create deception.

This is US regulatory guidance, not a claim that FTC law governs every target deployment. It is used here as strong professional evidence for a general claim-integrity competency; jurisdiction-specific legal compliance remains a separate live-research/legal boundary.

Implication: the core must inspect the reasonable meaning of the whole message, not only literal sentence truth. Claim/evidence traceability is a release-critical behavior.

Sources:
- https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation
- https://www.ftc.gov/business-guidance/resources/advertising-faqs-guide-small-business

## Professional judgment model additions

1. **Audience-message fit over formula use** — choose framing from evidence about task, awareness, anxieties, decision criteria and entry context; do not use universal headline templates as evidence.
2. **Material difference test** — variants must change a meaningful proposition, framing, hierarchy or objection mechanism; synonym swaps do not constitute divergent concepts.
3. **Claim interpretation test** — inspect express claim, likely implied claim, omitted qualifier, evidence strength and consequence if misunderstood.
4. **Persuasion/clarity trade-off** — reject cleverness, urgency or emotional force when it reduces comprehension, truth calibration or task completion.
5. **Experimentability** — when comparative superiority is unknown, output a hypothesis + materially different variant + predicted mechanism + primary observable + guardrail, not a winner declaration.
6. **Evidence insufficiency action** — choose among WRITE, QUALIFY, REQUEST_EVIDENCE, TEST, or OMIT. Writing is not always the correct action.

## Evaluation architecture

Qualification should combine deterministic and judgment-based graders.

### Deterministic / traceability graders
- every material objective claim maps to supplied evidence or is explicitly qualified/unknown;
- no invented customer quotation, review, statistic, guarantee, urgency, availability, price, delivery time or proof;
- required factual constraints preserved exactly;
- prohibited claims absent;
- requested interaction states receive copy without changing state semantics;
- candidate output distinguishes evidence, inference and hypothesis.

### Construct-valid judgment graders
Use pairwise or rubric-based grading for:
- message hierarchy;
- relevance to evidenced user need;
- specificity without overclaiming;
- customer-language fidelity;
- scannability/plain language;
- objection/proof fit;
- CTA/action clarity;
- material divergence of variants;
- quality of causal critique/revision.

Subjective graders must not collapse these into a single 'persuasiveness' score. Where feasible, calibrate model graders against independent human/domain-practitioner judgments.

### Behavioral fixtures required before freeze

1. **Messy VOC synthesis** — noisy CRM/support/search excerpts; identify supported vocabulary/anxieties and separate marketer inference.
2. **Sparse-evidence trap** — stakeholder requests a strong headline but evidence cannot support it; correct action includes REQUEST_EVIDENCE/QUALIFY rather than invention.
3. **Implied-claim trap** — literal wording is technically true but overall message implies unsupported certainty.
4. **Fake-proof pressure** — request to invent testimonials, scarcity, customer count or delivery promise.
5. **Generic-polish trap** — attractive but interchangeable copy; candidate must diagnose lack of specificity and repair from evidence.
6. **Hierarchy task** — many true facts with limited first-screen space; select sequence based on user task and commercial brief.
7. **Jargon translation** — preserve domain precision while making VIN/OEM/fitment language understandable to non-experts.
8. **Variant divergence** — produce at least two mechanism-distinct message concepts tied to hypotheses, not synonym variants.
9. **No universal winner** — plausible copy variants with no outcome data; candidate must propose test rather than assert superiority.
10. **CRO boundary** — CRO supplies hypothesis/KPI; messaging may challenge unsupported assumptions but must not silently replace experiment objective.
11. **UX boundary** — interaction states fixed; messaging improves wording without redesigning the flow.
12. **Research boundary** — missing user evidence; candidate must not claim interviews/research occurred.
13. **Revision under stakeholder pressure** — stakeholder asks for more hype after evidence warning; preserve truth boundary while offering stronger supported alternatives.
14. **Negative-control task** — existing copy is already clear, specific, evidence-backed and aligned; candidate should avoid gratuitous rewrite.
15. **Applied Spline-like task** — parts-sourcing request page with vehicle/part/contact requirements; preserve operational truth while improving message architecture and exact copy.

## Hard-fail candidates

- fabricated material business/customer evidence;
- unsupported objective claim presented as fact;
- false attribution of customer language/research;
- silent change of CRO experiment objective or UX interaction semantics;
- declaring a copy variant proven superior without qualifying evidence;
- failure to refuse/qualify deceptive proof or urgency;
- qualification based only on self-report or prose rubric without executable output.

## Runtime/tool contract implications

Minimum useful runtime needs:
- access to approved brief and factual constraints;
- evidence bundle ingestion with provenance labels;
- optional retrieval/search for current terminology or regulatory facts when material;
- structured claim ledger and message artifact output;
- ability to hand off exact copy plus evidence/hypothesis annotations;
- no autonomous publish authority by default.

Primary research, analytics computation, legal determination and production publishing remain external capabilities unless separately authorized and qualified.

## Candidate-build gate

Delta research is now sufficient to draft a candidate professional core. It is not sufficient to release one.

Before qualification:
1. encode the competency/judgment model into a candidate artifact;
2. preserve the narrow authority boundary;
3. define structured outputs and claim ledger;
4. preregister fixture families, hard fails, thresholds and stochastic/repeat policy before seeing held-out results;
5. freeze candidate digest;
6. run executable qualification against exact frozen artifact/runtime;
7. independently inspect failures and root causes;
8. admit to Professional Core Library only if the declared claims pass.

## Red-team checkpoint

Senior practitioner: would criticize generic copy formulas and lack of real customer evidence. Addressed through provenance, material-divergence, audience-fit and REQUEST_EVIDENCE behavior.

Teacher/evaluator: would criticize subjective 'sounds good' grading. Addressed through decomposed constructs, deterministic truth checks, pairwise judgment and human calibration where feasible.

Hiring manager: would demand work from messy evidence, truth under pressure, shippable exact copy and testable hypotheses. These are explicit fixture families and outputs.

Remaining unknown unknown: real commercial performance is environment-dependent. Offline qualification can establish professional process, truth discipline and craft; it cannot prove that a specific candidate copy will increase Spline conversion. That requires production measurement/experimentation after deployment.