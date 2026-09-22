# Sports Pharmacology & Supplementation — decision model v0.1

Status: pre-SKILL research artifact.
Date: 2026-09-22.

## Entry controller

For each request:

1. IDENTIFY — exact substance/product, active ingredients, form, serving size and intended effect.
2. CLASSIFY — food | supplement | OTC medication | prescription therapy | non-medical PED | unknown/grey-market.
3. SCOPE — general education vs personalized recommendation vs medical treatment.
4. READINESS — recover known context; acquire only decision-changing safety facts.
5. EVIDENCE — stored stable evidence vs required live research.
6. DECIDE — recommend / optional / low-value / avoid / clinician-pharmacist review / urgent escalation.
7. VERIFY — product version, units, duplicate actives, current anti-doping/jurisdiction status where relevant.
8. OBSERVE — if an ordinary supplement is started, change one variable when feasible and track intended outcome + side effects.

## Decision-critical intake

### Ordinary supplement
Safety-critical / decision-changing as relevant:
- adult vs minor;
- goal and training context;
- exact supplement and planned amount;
- other supplements/pre-workouts/energy drinks that may duplicate actives;
- relevant disease, pregnancy, medication or prior adverse reaction;
- caffeine timing/sleep/anxiety/cardiovascular sensitivity for stimulants;
- tested-sport status when applicable.

Calibration-only:
- brand preference;
- flavor;
- exact meal timing when unrelated to effect;
- optional biometrics not tied to the decision.

### Prescription therapy
Need:
- exact medication and prescribed indication;
- prescriber-directed regimen as reported;
- question being asked;
- relevant co-medications/conditions where interaction is at issue.

The skill may explain, organize questions, and interpret general evidence. It must not override the prescriber or change treatment.

### Non-medical PED
Need only what is required for the requested informational/risk analysis. Do not conduct an intake whose purpose is to optimize a cycle.

If the user already uses PEDs, useful non-enabling support includes:
- exact substance identity when known;
- symptoms/adverse effects;
- medical diagnoses/medications relevant to risk;
- whether there is a current clinician;
- current testing-sport context.

Do not request detailed cycle optimization data unless necessary to understand a medical risk already presented.

## Supplement decision states

### RECOMMEND
Use when:
- evidence for the target outcome is meaningful;
- expected benefit is relevant;
- healthy-adult safety context is adequate;
- form/dose is identifiable;
- interaction/product-quality risk is acceptable.

### OPTIONAL
Use when evidence supports a small/context-specific effect but it is not necessary for the user's goal.

### LOW_VALUE
Use when:
- adequate diet/training already supplies the relevant substrate;
- outcome evidence is weak/inconsistent;
- marketing claim exceeds human outcome evidence.

### AVOID / DO NOT RECOMMEND
Use when:
- meaningful risk exceeds plausible benefit;
- identity/formulation is unreliable;
- compound is a non-medical drug/PED beyond recommendation authority;
- product creates a material interaction or contamination concern.

### ESCALATE
Use when:
- acute toxicity/red flags;
- material disease/medication complexity;
- pregnancy/minor;
- abnormal clinical findings needing diagnosis/treatment;
- prescription changes;
- endocrine/fertility management after PED use.

## Evidence hierarchy

For supplement efficacy:
1. current authoritative evidence summaries / professional consensus;
2. systematic reviews/meta-analyses;
3. randomized human trials;
4. mechanistic data;
5. anecdote/marketing.

For current status:
1. regulator / WADA / official medication database;
2. current product label/manufacturer documentation;
3. reputable secondary source;
4. never rely on old memory when status is versioned.

## Dose logic for ordinary supplements

A dose recommendation must state:
- active ingredient, not just brand;
- form when it changes evidence;
- daily vs pre-event use;
- whether loading is optional or required;
- upper/side-effect considerations relevant to the user;
- target benefit;
- why more is not expected to improve the target.

Avoid stacking multiple new supplements simultaneously unless there is a clear reason.

## PED information model

For any PED, structure the answer as:
- WHAT IT IS / CLASS;
- EFFECT EVIDENCE;
- MAJOR RISKS;
- UNCERTAINTY;
- INTERACTION / CONTRAINDICATION CONCERNS;
- ANTI-DOPING / LEGAL STATUS when relevant and live-verified;
- WHAT REQUIRES A CLINICIAN.

Do not append a cycle, dose schedule, injection procedure or PCT.

## Monitoring principle

Monitoring can detect some harms; it cannot prove absence of harm or transform supraphysiologic non-medical PED exposure into a safe intervention.

When discussing labs:
- explain what a marker can and cannot indicate;
- do not diagnose from one abnormal value;
- do not prescribe treatment to fix a marker so a cycle can continue;
- clinically significant abnormalities route to a clinician.

## Minimal-change principle

For ordinary supplementation:
- first verify nutrition/training need;
- add at most one high-value change when possible;
- specify expected outcome and observation window;
- stop/adjust for adverse effects;
- do not keep adding supplements merely because progress is slow.