# Brand Naming Practitioner — evidence register v0.1

Status: Architect research artifact. Not a SKILL.
Issue: #275
Date checked: 2026-09-04

## Evidence policy

Use official/legal sources for trademark boundaries, empirical literature for linguistic/cognitive claims, current professional practice for naming workflow/tacit craft, and external agent repositories only as discovery candidates.

| ID | Claim / decision consumed | Source | Evidence type | Freshness / scope | Decision |
|---|---|---|---|---|---|
| E01 | Naming begins from brand essence/target audience and is a strategic process, not random ideation | Lexicon Branding, Brand Naming: 5 Step Process, updated 2026-03-25, https://www.lexiconbranding.com/brand-naming-process/ | Current specialist practice | Current 2026 | SUPPORTS BN-01/02 |
| E02 | Memorability/processing, trademarkability, linguistic implications and research are distinct naming concerns | Lexicon, same source | Specialist practice + cited research synthesis | Current | SUPPORTS BN-06/07/10/11/12 |
| E03 | Semantics, structure and sound all contribute; sound should not be reduced to semantics alone | Lexicon, same source | Specialist practice | Current | SUPPORTS linguistic craft cluster |
| E04 | Naming process includes strategy, creative directions, brainstorming, availability screening and final decision | Catchword, Just Name It guide, https://catchwordbranding.com/catchthis/just-name-it-catchwords-comprehensive-naming-guide/ | Established specialist practice | Stable | SUPPORTS workflow |
| E05 | Great names involve trade-offs across magnetism, distinctiveness, fit, accessibility, longevity, conciseness, euphony, appropriateness, consistency and protectability | Catchword, 10 criteria for great brand names, https://catchwordbranding.com/wp-content/uploads/2014/10/CW_NamingGuide_100914.pdf | Specialist framework | Older but stable; not treated as universal weights | SUPPORTS criteria families |
| E06 | Screening should include trademark, domain and social-handle checks; exact handle/domain parity is not always required | Catchword, Create the Perfect Brand Name, current page, https://catchwordbranding.com/catchthis/create-the-perfect-brand-name/ | Specialist practice | Current | SUPPORTS BN-09 and workaround judgment |
| E07 | Professional naming process separates discovery, ideation, legal/market screening and presentation | NameStormers, https://www.namestormers.com/capabilities/naming-development-process/ | Current specialist practice | Current | CORROBORATES workflow |
| E08 | Linguistic screening includes slang/phonetic/cultural associations, pronunciation, spelling and current-event risk; native/in-country review has value | NameStormers, https://www.namestormers.com/capabilities/linguistic-screening/ | Current specialist practice | Current | SUPPORTS BN-11 / escalation |
| E09 | Trademark confusion can arise from similarity in sound, appearance, meaning or commercial impression, conditioned on related goods/services | USPTO Likelihood of Confusion, https://www.uspto.gov/trademarks/search/likelihood-confusion | US government authority | Current guidance | SUPPORTS BN-10 |
| E10 | Comprehensive clearance search uses multiple sources; federal database search alone is not conclusive | USPTO Federal Trademark Searching + comprehensive clearance guidance, https://www.uspto.gov/trademarks/search/federal-trademark-searching | US government authority | Current | SUPPORTS legal boundary |
| E11 | Distinctiveness is fundamental to trademark protection; personal names can function as marks depending on distinctiveness/use | WIPO trademark protection + personal-name materials, https://www.wipo.int/en/web/trademarks/protection and https://www.wipo.int/en/web/amc/processes/process2/report/html/report | International IP authority | Stable principle; jurisdiction-specific application | SUPPORTS distinctiveness/personal-name mode |
| E12 | Sound symbolism in brand names has systematic connotative associations but remains contextual | Motoki et al., Journal of Business Research 150 (2022), DOI 10.1016/j.jbusres.2022.06.013 | Peer-reviewed systematic review/framework | Stable | SUPPORTS bounded BN-06 |
| E13 | Sound-symbolism effects can generalize across languages in experimental settings | Shrum et al., International Journal of Research in Marketing 29(3) (2012), DOI 10.1016/j.ijresmar.2012.03.002 | Peer-reviewed experiments | Stable; transfer limits apply | SUPPORTS cross-language phonetic relevance |
| E14 | Spelling characteristics of auditorily presented brand names can affect spelling accuracy and later recall | Journal of Consumer Psychology 23(1) (2013), DOI 10.1016/j.jcps.2012.02.003 | Peer-reviewed experiments | Stable | SUPPORTS BN-07 |
| E15 | External Brand Naming skill: criteria-before-generation, multiple archetypes, linguistic/availability checks | SkillMedev/skills brand-naming SKILL | External open-source candidate | Current; no local qualification | DISCOVERY ONLY; no REUSE |
| E16 | External Quaere naming skill: brief, metaphor territories, large internal pool, tool-verified availability, no guessing | haru0416-dev/quaere naming skill (MIT) | External open-source candidate | Current; no local qualification | DISCOVERY ONLY; useful contrastive ideas |
| E17 | External brand-naming Codex/Studio skills demonstrate repeated packaging of naming as a standalone capability | fcoury/brand-naming-codex-skill; SevenAILab/brand-naming-studio-skill | External open-source candidates | Current | SUPPORTS packaging plausibility only |
| E18 | Spline applied Brand Identity skill states naming was a prior separate decision and is out of current visual-identity work | prostoali2207-gif/auto-parts-landing/.agents/skills/brand-identity-agent/SKILL.md | Direct internal project evidence | Current repo state | SUPPORTS boundary separation |
| E19 | Personal Brand applied decision found naming not owned by existing cores and required a distinct capability | prostoali2207-gif/personal-brand-growth-system/decisions/personal-brand-naming-capability-2026-09-04.md | Direct applied architecture evidence | Current | SUPPORTS repeated cross-project need |

## Evidence conflicts and limits

### Professional-practice frameworks are not universal law
Lexicon, Catchword and NameStormers use different proprietary processes and emphasis. Their overlap supports the construct; no single agency framework becomes the canonical skill.

### Volume is not competence by itself
Professional firms may generate hundreds or thousands of candidates, while external skills prescribe 20–50. The invariant is adequate divergence before convergence, not a frozen minimum count for every task.

### Sound symbolism is real but bounded
Empirical effects justify phonetic sensitivity. They do not justify universal sound-to-meaning recipes across all categories/languages.

### Trademark screening vs clearance
USPTO supports broad preliminary searching, but registrability and infringement are legal determinations. Candidate must stop at risk triage and handoff.

### Personal names
WIPO materials establish that personal names can function as marks, but exact protection depends on jurisdiction, use and distinctiveness. Do not encode a global legal rule.

## Knowledge packaging audit

### EMBED_CORE
- strategy/brief before naming;
- criteria and hard fails before convergence;
- divergent territory principle;
- semantic/phonetic/spelling/accessibility/long-horizon trade-offs;
- preliminary screening != legal clearance;
- uncertainty and source freshness;
- handoff boundaries.

### PROCEDURAL_MODULE
- naming brief construction;
- territory development;
- candidate generation/filtering;
- shortlist comparison;
- spoken/written context stress test;
- personal-brand handle mode.

### REFERENCE_MODULE
- naming construction families/examples;
- linguistic risk prompts;
- trademark similarity dimensions;
- screening ledger schema.

### LIVE_RESEARCH
- competitor/category names;
- domains/social handles;
- trademark status/search;
- platform username rules;
- current cultural/news associations.

### TOOL_BACKED
- web search;
- domain/handle/registry checks;
- exact-string/phonetic normalization helpers where available;
- candidate deduplication;
- screening ledger validation.

### ESCALATE
- legal clearance;
- high-stakes native linguistic/cultural certification;
- upstream positioning;
- final visual identity.

## Evidence still required before qualification PASS

1. Independent practitioner/assessor calibration for shortlist quality and trade-off judgments.
2. Fresh held-out cases authored separately from candidate drafting.
3. At least one tool-failure case proving UNVERIFIED behavior.
4. At least one legal-confusion case graded against explicit USPTO-derived boundary.
5. At least one personal-brand case and one company/product case.
6. Evaluation of external candidate baseline vs local candidate to justify BUILD NEW value.
