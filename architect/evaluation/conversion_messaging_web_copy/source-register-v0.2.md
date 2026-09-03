# Conversion Messaging & Web Copy v0.2 — source register

Status: development evidence register; not qualification evidence.

Retrieved/reviewed: 2026-09-03.

| ID | Source | Category | Claim / competency supported | Freshness | Applicability / limitations |
|---|---|---|---|---|---|
| GADS-MATCH-1 | Google Ads Help — `Optimize your ads and landing pages` — https://support.google.com/google-ads/answer/6238826 | official product/platform documentation | D1: users expect a landing page relevant to the ad; landing page should closely match ad/keywords and mirror the advertised CTA/offer | volatile/versioned | Authoritative for Google Ads/search landing-page expectations, not a universal causal estimate of conversion lift and not authority for non-Google channels |
| GADS-MATCH-2 | Google Ads Help — `Using Quality Score to improve your performance` — https://support.google.com/google-ads/answer/13738235 | official product/platform documentation | D1: ad relevance and landing-page experience are separate diagnostic components; Google recommends messaging consistency from ad to landing page | volatile/versioned | Diagnostic/platform guidance. Do not treat Quality Score as the core's optimization target or as causal proof of conversion improvement |
| WCAG-LINK | W3C WAI WCAG 2.2 Understanding SC 2.4.4 — https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html | standard/official specification guidance | D2: link purpose must be determinable from link text or programmatically determined context | slow/versioned | Normative accessibility interpretation. Copy alone cannot establish full conformance because markup/context implementation also matters |
| WCAG-LABEL | W3C WAI Understanding SC 3.3.2 — https://www.w3.org/WAI/WCAG21/Understanding/labels-or-instructions.html | standard/official specification guidance | D2: labels/instructions are required when user input is required; wording should tell users what information is expected | slow/versioned | UX determines what input is required; copy operates inside that supplied control/state contract |
| WCAG-ERROR | W3C WAI WCAG 2.2 Understanding SC 3.3.1 — https://www.w3.org/WAI/WCAG22/Understanding/error-identification | standard/official specification guidance | D2: detected input errors must identify the item in error and describe the error in text | slow/versioned | Does not authorize the copy practitioner to invent validation logic or correction rules |
| W3C-I18N-QT | W3C Internationalization Quick Tips — https://www.w3.org/International/quicktips/ | official standards-body guidance | D3: simple/concise text, translatability, cultural bias, local form formats, target-language navigation, RTL considerations | slow | Broad authoring guidance; implementation-specific i18n remains Frontend/UX responsibility |
| W3C-I18N-LOC | W3C `Localization vs. Internationalization` — https://www.w3.org/International/questions/qa-i18n | official standards-body guidance | D3: localization is adaptation to language/cultural/market requirements and is more than UI translation | stable/slow | Definition/boundary evidence, not a translation-quality rubric for a specific language |
| W3C-LANG | W3C `Language on the Web` — https://www.w3.org/International/getting-started/language.en.html | official standards-body guidance | D3 boundary: language metadata/preferences affect language-sensitive tools and multilingual navigation | slow | Primarily implementation/context evidence; copy practitioner should surface requirements but not take over HTML/server configuration |
| GOV-UI | GOV.UK Service Manual — `Writing for user interfaces` — https://www.gov.uk/service-manual/design/writing-for-user-interfaces | recognized public-sector professional guidance | D2/D3 supporting practice: clear/direct wording, user language, reduced cognitive load, inclusion for limited-English users | slow | Strong content-design practice evidence, not a universal legal standard or commercial conversion framework |
| HOME-LIMITED-EN | Home Office UCD Manual — `Designing for people with limited English` — https://design.homeoffice.gov.uk/design-and-content/content/designing-for-limited-english | recognized public-sector professional guidance | D3 supporting practice: check translatability, avoid idioms/phrasal ambiguity, test important UI wording with target users | slow | Context is public services/limited-English populations; transferable as risk pattern, not a universal style mandate |

## Source-to-decision synthesis

### D1

The official Google sources support a bounded professional requirement: when an approved ad/search message is the entry context, landing copy should preserve the user's material expectation, offer and next-action continuity. They do **not** support a guaranteed-lift claim. Therefore v0.2 encodes message continuity as a diagnostic/craft responsibility while experiment outcomes remain empirical.

### D2

WCAG provides directly observable text requirements for the exact area v0.1 already claims to own: link/action wording, labels/instructions and error microcopy inside approved states. The core must encode those requirements without claiming that wording alone certifies WCAG conformance.

### D3

W3C Internationalization establishes that localization is broader than literal translation and that language/culture/formats/directionality can affect web content. The core therefore needs a contextual localization/translatability decision layer, but language-specific correctness and implementation remain review/handoff responsibilities where not independently verifiable.

## Runtime freshness policy

- Google Ads/platform behavior: retrieve live when a platform-specific claim materially affects current work.
- WCAG/W3C standards guidance: store stable principles with version awareness; retrieve live for exact current conformance/technique claims when material.
- Locale/customer language: never freeze project-specific vocabulary into the reusable core; use authorized target-language evidence and current local review/research at runtime.
