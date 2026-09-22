# Sports Pharmacology & Supplementation — profession reconstruction v0.1

Status: pre-SKILL research artifact.
Date: 2026-09-22.

## Target outcome

Provide evidence-based decision support for an adult resistance-training user asking about sports supplements, medications relevant to training, and performance/appearance-enhancing drugs (PEDs), while preserving a hard boundary between ordinary supplement coaching and high-stakes medical/pharmacological decisions.

The capability must be useful for hypertrophy and performance decisions without pretending that non-medical drug use can be made "safe" by a protocol.

## Reconstructed professional model

The closest real professional model is a **sports-pharmacology information specialist** combining bounded competencies from:

- pharmacist / clinical-pharmacology reasoning: substance identity, pharmacologic class, mechanism, interactions, contraindications, adverse effects, route/formulation relevance, medication reconciliation;
- sports nutrition: efficacy and practical use of evidence-supported dietary supplements;
- sports medicine boundary recognition: red flags, medical supervision needs, lab/clinical context;
- anti-doping practice: current prohibited-status verification and supplement contamination risk;
- evidence appraisal: distinguishing mechanistic plausibility, acute performance effects, long-term outcome evidence, observational harm signals, and marketing claims.

A general nutrition coach is insufficient because drug interactions, endocrine/cardiovascular toxicity, prescription status, and anti-doping rules require different competence. A physician is not reconstructed into the agent: diagnosis, prescribing, medication changes, treatment of adverse effects, and management of endocrine recovery remain outside authority.

## Substance classes

Every query is first classified into one or more classes:

1. **FOOD / ORDINARY NUTRITION** — route to the project's nutrition capability.
2. **DIETARY / SPORTS SUPPLEMENT** — direct evidence-based decision support when within healthy-adult scope.
3. **OTC MEDICATION** — information + interaction/contraindication screening; recommend clinician/pharmacist review when material.
4. **PRESCRIPTION MEDICATION / PRESCRIBED HORMONE THERAPY** — explanation and monitoring support; do not independently start, stop, or change dosing.
5. **NON-MEDICAL PED / APED** — anabolic-androgenic steroids, SARMs, growth hormone/secretagogues, insulin, thyroid drugs, stimulants, diuretics and similar enhancement use. Provide evidence, risks, interaction analysis, red flags, and current anti-doping/legal context; do not generate a personalized non-medical cycle, stack, titration, injection plan, or post-cycle treatment regimen.
6. **UNKNOWN / GREY-MARKET / RESEARCH CHEMICAL** — identity uncertainty is itself a high-risk condition; require verified product/substance identity and current evidence or escalate.

## Professional responsibilities

1. Identify exactly what substance/product the user means before evaluating it.
2. Separate intended effect from demonstrated outcome evidence.
3. Classify evidence quality for hypertrophy, strength, endurance, recovery, body composition, or deficiency correction.
4. For supplements, recommend only when expected benefit, dose/form, tolerability, cost and product-quality risk justify use.
5. Reconcile duplicate active ingredients across pre-workouts, energy drinks, multivitamins, powders and medications.
6. Detect meaningful interaction and contraindication risks.
7. Distinguish supplement from drug/PED status; a product sold as a supplement is not proof that every ingredient is a lawful supplement.
8. Treat non-medical PED use as high-stakes: surface known organ-system risks, uncertainty, fertility/endocrine consequences, polypharmacy risks and red flags.
9. Use live authoritative sources for anti-doping status, jurisdiction-sensitive legality, recalls, product warnings and current labeling.
10. Keep ordinary nutrition with the dedicated nutrition skill rather than duplicating it.
11. Escalate symptoms, abnormal clinical findings, pregnancy/minor status, complex disease, suspected toxicity, or medication changes to an appropriate clinician/pharmacist.
12. Never convert population-level harm-reduction observations into a claim that a PED regimen is safe.

## Expert cues

A strong practitioner notices:

- "natural", "test booster", "prohormone", "research chemical", and "SARM" are marketing/category labels, not safety evidence;
- a supplement may contain undeclared or prohibited ingredients, so label review alone cannot guarantee eligibility for tested sport;
- multiple branded products can silently duplicate caffeine, niacin, vitamin D, stimulants or other actives;
- creatine-related scale gain can reflect water as well as tissue and must not be misclassified as fat;
- protein powder is a food-convenience tool, not a superior anabolic drug;
- a mechanistic increase in a hormone or biomarker does not establish meaningful hypertrophy or performance benefit;
- trial evidence from healthy adults does not automatically transfer to people with cardiovascular, renal, hepatic, endocrine, psychiatric, pregnancy or medication complexities;
- non-medical AAS use can suppress the hypothalamic-pituitary-gonadal axis and affect fertility; recovery after cessation is variable;
- AAS cardiovascular risk is shaped by exposure duration, dose, compound properties, blood pressure, lipids, hematocrit and polypharmacy, but no monitoring panel converts supraphysiologic use into a low-risk intervention;
- anti-doping rules are versioned: current-list verification is mandatory for athletes subject to testing;
- supplement regulation and product composition vary by jurisdiction and batch.

## Scope

### CORE
- substance/product identification and classification;
- evidence appraisal for sports supplements;
- practical supplement selection for hypertrophy/performance;
- duplicate-ingredient and basic interaction screening;
- adverse-effect recognition;
- distinction between supplement, medication and PED;
- evidence/risk explanation for PEDs;
- minimal-effective-use principle for optional supplements;
- source freshness and product-quality reasoning.

### BOUNDARY-CRITICAL
- prescription medication interaction;
- endocrine/cardiovascular/hepatic/renal/fertility risk;
- stimulant stacking;
- contaminated/adulterated supplements;
- current anti-doping status;
- jurisdiction-dependent legal/medical status;
- abnormal symptoms or labs.

### CONTEXTUAL
- training goal and phase;
- caffeine tolerance and sleep;
- diet sufficiency;
- budget;
- sport federation/testing status;
- religious/ingredient constraints;
- product availability.

### ESCALATION
- chest pain, syncope, severe dyspnea, neurologic deficit, severe headache with marked hypertension, jaundice, dark urine with systemic illness, severe agitation/psychosis, suspected overdose or acute toxicity;
- prescription changes;
- pregnancy or minors;
- known significant cardiovascular, renal, hepatic, endocrine or psychiatric disease when the substance materially interacts with the condition;
- clinically abnormal labs requiring diagnosis/treatment;
- fertility treatment or endocrine recovery after non-medical AAS/PED exposure;
- suspected eating disorder or substance-use disorder;
- uncertain identity/contamination where a medical decision depends on the product.

### OUT OF SCOPE
- prescribing or diagnosing;
- individualized non-medical steroid/SARM/GH/insulin/clenbuterol/thyroid/diuretic cycles;
- injection technique for non-medical PEDs;
- PCT or ancillary-drug protocols intended to enable a cycle;
- instructions to evade anti-doping detection;
- claims that monitoring makes non-medical PED use safe;
- procurement of prescription/PED substances.

## Authority model

- Supplements in a generally healthy adult: **recommendation support** is permitted when evidence and inputs are sufficient.
- OTC/prescription medications: **information/analytical support**; medication changes remain with pharmacist/clinician.
- Non-medical PEDs: **information/analytical and risk-support only**; no autonomous regimen design.
- Anti-doping: factual current-status support from live authoritative sources; never guess.

## Architecture implication

Use one modular applied skill with task-triggered reference modules. Multi-agent architecture is unnecessary. The skill routes ordinary food/macronutrient questions to the existing nutrition skill, while retaining pharmacology, supplement efficacy, interaction, product-quality and anti-doping decisions locally.