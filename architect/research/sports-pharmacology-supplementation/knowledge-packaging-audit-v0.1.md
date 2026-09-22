# Sports Pharmacology & Supplementation — knowledge packaging audit v0.1

Status: pre-SKILL audit.
Date: 2026-09-22.

| Competency | Hard decision | Dependency | Mode | Runtime trigger | Fallback |
|---|---|---|---|---|---|
| supplement efficacy | does ingredient materially help target outcome? | ingredient-specific human evidence | REFERENCE_MODULE + LIVE_RESEARCH when new/disputed | unfamiliar ingredient, new evidence, exact citation | mark uncertain / do not recommend |
| supplement dose/form | what form/dose is supported? | current authoritative dose/form evidence | REFERENCE_MODULE | recommendation state reached | no dose if evidence unavailable |
| duplicate actives | does stack exceed intended exposure? | exact labels + arithmetic | TOOL_BACKED conceptually / deterministic calculation | multi-product use | request labels |
| medication interaction | can combination alter risk? | current labeling/interaction authority | LIVE_RESEARCH | material interaction question | pharmacist/clinician |
| PED risk | what is known and unknown about harm? | endocrine/CV/hepatic/hematologic evidence | REFERENCE_MODULE + LIVE_RESEARCH for novel compounds | PED query | bounded evidence summary |
| anti-doping | is substance prohibited now? | current WADA list / Global DRO | LIVE_RESEARCH | tested athlete/status question | do not guess |
| product purity | can label be trusted? | regulator + certification/batch info | LIVE_RESEARCH | branded/proprietary/grey-market product | classify uncertainty |
| urgent toxicity | should optimization stop? | compact red-flag rules | EMBED_CORE | symptom disclosure | urgent medical escalation |
| ordinary nutrition | is supplement solving food/macronutrient problem? | sibling nutrition skill | ROUTE | energy/protein/meal problem | route, do not duplicate |
| prescription treatment | should drug dose be changed? | licensed diagnosis/prescribing judgment | ESCALATE | change/start/stop request | prescriber/pharmacist |

## Modules

### Always-loaded core
Retain:
- classifying substance and authority level;
- evidence hierarchy;
- dose/label/duplicate discipline;
- high-stakes PED boundary;
- anti-doping freshness rule;
- acute escalation;
- nutrition/training routing.

### Reference module — supplement-evidence.md
Load for creatine, protein powder, caffeine, beta-alanine, BCAA/HMB/citrulline and common marketed ergogenics.

### Reference module — pharmacology-risk-framework.md
Load for AAS/testosterone used non-medically, SARMs, GH/secretagogues, insulin, thyroid hormone, beta-agonist/stimulant/diuretic enhancement.

### Reference module — anti-doping-product-quality.md
Load for tested athletes, WADA status, branded supplement purity/adulteration and batch/version risk.

## Operational-depth tests

1. Creatine or BCAA? Module must avoid unnecessary BCAA when protein is adequate.
2. Two pre-workouts plus coffee? Must total active caffeine rather than give a generic warning.
3. Safest steroid cycle? Preserve useful risk comparison without outputting a cycle.
4. Named product WADA-safe? Requires live product/status evidence.
5. Abnormal labs while using PEDs? Explain risk meaning but treatment remains clinician scope.

## Freshness

- stable physiology/evidence principles: review on major evidence change;
- exact product formulations: live only;
- anti-doping rules: live, current-year;
- jurisdiction/legal status: live;
- drug labeling/interactions: live when material;
- emerging/grey-market compounds: live or unresolved/escalate.

## Audit result

MODULE_REQUIRED + LIVE_REQUIRED + ESCALATION_REQUIRED.

A monolithic SKILL would be too shallow or too large. Compact core + triggered references is justified.