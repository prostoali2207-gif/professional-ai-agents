# Sports Pharmacology & Supplementation — reuse decision v0.1

Status: pre-SKILL compatibility record.
Date: 2026-09-22.

## Candidates inspected

### low-appetite-muscle-gain-nutrition@0.1.0-candidate
Compatibility:
- strong overlap for ordinary food/protein/energy decisions;
- some supplement boundary and creatine knowledge;
- explicitly excludes anabolic steroids/PED protocols;
- below-T1 applied candidate, not a qualified Professional Core.

Decision:
- **ROUTE / SIBLING DEPENDENCY** for ordinary nutrition questions.
- **REJECT as inherited pharmacology competence**.
- Do not copy its food/macronutrient logic into this skill.

### hypertrophy-training@0.1.0
Compatibility:
- provides training-goal context and explicitly recognizes PEDs as outside training-programming scope.
- no drug-interaction, toxicology, pharmacokinetic, anti-doping or supplement-product-quality competence.

Decision:
- **CONTEXTUAL ROUTE ONLY**; not a pharmacology core.

### qualified Professional Core Library
Current library contains no pharmacist, clinical pharmacology, sports medicine, toxicology, anti-doping or sports-supplement core.

Decision:
- no eligible core for REUSE / ADAPT / EXTEND.

## Formal decision

**BUILD NEW applied capability**, while composing with existing project fitness skills by routing rather than inheritance.

Rationale:
1. pharmacology/PED queries carry materially higher health consequences than ordinary nutrition;
2. current nutrition capability explicitly excludes PED protocols;
3. no repository core owns drug identity, interactions, adverse-effect reasoning or anti-doping status;
4. falsely inheriting competence from nutrition or hypertrophy programming would create unsafe authority expansion.

## Reused methodology, not professional qualification

Reuse:
- Agent Architect evidence/source rules;
- high-stakes profession architecture;
- intake/decision-readiness;
- runtime state and escalation;
- professional-core reuse discipline;
- knowledge packaging;
- evaluation integrity and qualification stop-loss.

## Composition boundary

The new skill must route:
- food, calorie surplus, macros, meal volume -> low-appetite-muscle-gain-nutrition;
- programming, volume, RIR, exercise selection -> hypertrophy-training / exercise skills;
- supplements, stimulant stacking, product labels, interactions, anti-doping status, PED evidence/risks -> sports-pharmacology-supplementation;
- diagnosis/treatment/prescribing -> clinician/pharmacist.

## Required regressions

Evaluate:
- no duplication of ordinary nutrition logic;
- correct routing between protein powder as a convenience food vs supplement claim;
- safe handling of creatine/caffeine in healthy users;
- duplicate stimulant detection;
- refusal to turn PED analysis into a personalized cycle/PCT;
- current WADA retrieval requirement;
- product contamination uncertainty;
- medication interaction/escalation;
- emergency red-flag behavior.