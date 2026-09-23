# Islamic lesson specialization — design note v0.1

Status: DOMAIN SPECIALIZATION
Date: 2026-09-23
Parent: `lecture-note-taking-coach@0.1.0-candidate`

## Why specialization is necessary

General lecture note-taking optimizes selection, compression, organization and retrieval. Islamic lessons add a material **transmission-fidelity problem**: a learner may later confuse revelation, hadith, athar, scholarly statement, teacher explanation and personal inference.

Therefore ordinary compression rules are insufficient without explicit attribution and verification behavior.

## Additional professional responsibilities

1. Preserve source identity when it affects meaning or authority.
2. Distinguish quotation from paraphrase.
3. Avoid inventing Qur'an/hadith references, authenticity grades, scholar attributions, consensus or tarjih.
4. Preserve conditions/exceptions and material disagreement.
5. Adapt note structure to tafsir, hadith, fiqh, 'aqidah, seerah and usul.
6. Make uncertainty visible and route material items to verification before sharing.
7. Keep the learner's own reflection separate from transmitted tafsir or scholarly explanation.

## Additional failure modes

- SOURCE_LAYER_MIXING;
- ATTRIBUTION_ERROR;
- QUOTE_PARAPHRASE_CONFUSION;
- UNVERIFIED_REFERENCE_AS_FACT;
- KHILAF_COLLAPSE;
- CONDITION_LOSS;
- PERSONAL_REFLECTION_AS_TAFSIR;
- TEACHER_TARJIH_AS_CONSENSUS.

## Evidence basis

### Qur'an 17:36
Principle: do not follow or assert what is not known.
Operational implication: uncertainty must be marked rather than silently filled.

### Jami' al-Tirmidhi 2656, Zayd ibn Thabit
Text includes the Prophet's supplication for one who hears, preserves and conveys the report; al-Tirmidhi called the hadith hasan.
Operational implication: source fidelity matters in transmitted Prophetic material.

### Sahih Muslim, Introduction, report of Muhammad ibn Sirin
"Indeed this knowledge is religion, so look from whom you take your religion."
Operational implication: provenance is part of the knowledge object, not optional metadata.

### Sahih al-Bukhari 110 / Sahih Muslim 3
Warning against deliberately lying about the Prophet ﷺ.
Operational implication: never manufacture or confidently attribute Prophetic wording.

## Design decision

**EXTEND parent skill with a staged specialization module.**

Do not create a separate autonomous agent:
- the cognitive coaching loop is the same;
- the same learner progression/state is required;
- only domain-specific fidelity, structure and verification rules differ.

## Specialization quality dimensions

Add to general note quality:
- SOURCE FIDELITY — correct layer/attribution;
- QUOTATION INTEGRITY — exact vs paraphrase is explicit;
- EVIDENCE CHAIN — dalil is attached to the right claim;
- CONDITION PRESERVATION — qualifications/exceptions survive compression;
- DISAGREEMENT FIDELITY — views and tarjih are not collapsed;
- SHARE READINESS — unresolved attributions are marked before external use.

## Scope boundary

This module teaches how to **record** an Islamic lesson. It does not independently issue fatwas, authenticate hadith, determine creed rulings, or resolve scholarly disagreement unless another qualified Islamic-answering capability is explicitly performing that task.
