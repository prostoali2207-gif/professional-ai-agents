# Live Source-Lineage Case — Gartner AI Spending Release

Date: 2026-08-15

## Purpose

Demonstrate that multiple URLs/domains carrying the same claim are not automatically independent evidence.

## Claim

Gartner forecast worldwide AI spending of approximately USD 2.59 trillion in 2026, a 47% year-over-year increase.

## Observed publication graph

Primary/origin identity:
- Gartner newsroom press release, dated 2026-05-19.

Distribution / republishing examples observed during live web retrieval:
- Business Wire publication of the Gartner release.
- Nasdaq page labeled as a press release and carrying the Business Wire dateline/text.
- Yahoo Finance page attributed to Business Wire and carrying the same release text.
- AIwire / HPCwire "Off The Wire" page carrying the same headline, figures, dateline and release language.
- Additional repost/announcement pages carrying substantially the same Gartner release.

## Adjudication

These URLs must not be counted as five or more independent confirmations of the numeric forecast.

For the claim as stated, the dominant primitive evidence lineage is Gartner's forecast/release. Business Wire distribution and downstream republications are transport/publication descendants of that same upstream claim, not independent measurements.

A genuinely independent corroborating lineage would require a separately produced estimate, dataset, analysis, regulator filing, audited result, or other evidence whose factual basis is not inherited from the Gartner release.

## Architecture rule

`distinct_url_count` and `distinct_domain_count` are discovery metrics, not evidence-independence metrics.

Evidence synthesis should track at minimum:
- origin / upstream source;
- explicit citations and attribution;
- syndication/wire identity;
- publication timestamp ordering;
- exact/near-duplicate text fingerprints;
- shared quantitative values and wording;
- source type (primary, wire, secondary analysis, independent measurement);
- lineage confidence: VERIFIED / PROBABLE / UNKNOWN.

If lineage cannot be established, do not assume independence. Mark it `UNKNOWN` and avoid multiplying confidence merely because the same claim appears on multiple domains.

## Scope limitation

This live case demonstrates visible correlated publication lineage. It does not establish a complete automated near-duplicate or causal-source classifier. A production system still needs robust citation extraction, similarity/fingerprint heuristics, timestamps, structured metadata and manual/LLM adjudication for ambiguous cases.
