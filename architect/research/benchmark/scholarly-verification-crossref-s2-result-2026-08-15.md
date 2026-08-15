# Scholarly Verification — Crossref + Semantic Scholar — 2026-08-15

Status: **architecture evidence PASS; provider limitations observed; original workflow FAIL_P0 was not a valid final adjudication.**

## Why the first workflow was red

Run `31874813956` produced real useful evidence, but the v0.1 grader incorrectly classified a missing Crossref title field as a P0 integrity failure. Missing metadata is a coverage/completeness limitation; it is not equivalent to a fabricated or incorrect identity.

The run also observed an unauthenticated Semantic Scholar `429` on the second S2 request. That is an operational/rate-limit event, not a bibliographic-content failure.

No additional API calls were made for adjudication. The workflow was changed to manual-only before further grader changes so that repository edits cannot accidentally consume public API quota.

## Empirical observations

### Crossref — exact BERT DOI

Request for `10.18653/v1/N19-1423` returned HTTP 200 in ~0.272 s.

Observed:

- DOI: exact/correct;
- type: `proceedings-article`;
- publication year: 2019;
- authors: Devlin, Chang, Lee, Toutanova — all correct;
- **title field: empty** for this Crossref record.

Interpretation:

Crossref is strong evidence for DOI identity and deposited metadata, but field completeness is deposit-dependent. Therefore the architecture must not assume that Crossref alone can verify every bibliographic field. Missing fields require another source rather than hallucinated completion.

### Semantic Scholar — same BERT DOI

First unauthenticated S2 request returned HTTP 200 in ~0.232 s.

Observed:

- title: `BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding`;
- authors: Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova;
- DOI: `10.18653/v1/N19-1423`;
- ACL ID: `N19-1423`;
- arXiv ID: `1810.04805`;
- year: 2019;
- venue: NAACL.

This is a useful complement to Crossref on this case: richer identity/version metadata was available where Crossref's title field was absent.

### Semantic Scholar — immediate arXiv follow-up

The next unauthenticated request for `ARXIV:1810.04805` returned HTTP `429`.

Interpretation:

The no-key S2 route is useful for low-volume opportunistic verification/discovery but is not a reliable high-throughput production assumption. The research router needs explicit rate-limit handling, caching/batching where supported, and either a key or graceful fallback if Semantic Scholar becomes a default scholarly adapter.

No retry was issued in this stage because the rate event itself was the needed operational evidence.

### Crossref — retraction/update provenance

Request for `10.1177/17588359231172420` returned HTTP 200 in ~0.253 s.

Crossref returned `update-to` retraction relationships pointing to `10.1177/1758835920922055`, with two provenance entries:

- `source: retraction-watch`;
- `source: publisher`.

Both identify the relation as `type: retraction` with the same update date.

This materially strengthens Crossref's proposed role in the architecture: it is not only a DOI resolver; it can expose post-publication integrity/update evidence and the provenance of that update signal.

## Corrected role verdicts

### Crossref

**Recommended role: DOI/identifier + deposited bibliographic metadata + post-publication update/retraction verification.**

Do not treat missing fields as proof that a work lacks that field. Crossref metadata completeness is not uniform. For absent/critical fields, inspect publisher/venue metadata and cross-check with scholarly graphs.

### Semantic Scholar

**Recommended role: scholarly discovery, graph enrichment, citation/version identity cross-check.**

Do not make it the sole canonical authority for all bibliographic fields. The first live case was strong, but unauthenticated rate behavior is an operational limitation and wider field/discipline coverage still needs evaluation.

### Combined architecture

This live gate directly supports the multi-layer design:

`Crossref identity/integrity metadata + Semantic Scholar enrichment + publisher/venue/full-text inspection`

is stronger than either service alone.

## Eval-design lesson

The original v0.1 severity model conflated:

- **wrong/fabricated metadata** — integrity failure;
- **missing metadata** — coverage limitation;
- **HTTP 429** — operational/rate-limit failure.

These must be separate failure classes. A professional benchmark must not label all three as the same kind of FAIL.

## Cost/resource consequence

- Crossref required no paid credential.
- Semantic Scholar first unauthenticated request succeeded; the second was rate-limited.
- No retries were spent after the rate-limit signal.
- The workflow is now manual-only to prevent edits from causing quota-consuming reruns.

This is the intended Resource & Cost Engineering behavior: preserve the evidence from the first run, correct the grader deterministically, and avoid repeated external calls that cannot change the observed fact.
