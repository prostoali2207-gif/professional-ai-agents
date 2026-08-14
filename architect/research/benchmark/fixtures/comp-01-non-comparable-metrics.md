# Retrieval Provider Comparison — Synthetic Evidence Fixture

This frozen fixture contains credible-looking measurements that are intentionally not directly comparable.

## Provider A

- metric: successful evidence retrieval rate
- value: 92%
- denominator: 500 single-hop factual queries
- source set: English public web pages
- evaluation condition: cached corpus frozen on 2026-01-01
- success definition: any gold-relevant document appears in top 10
- latency: excluded from metric

## Provider B

- metric: research task success rate
- value: 81%
- denominator: 120 multi-hop research tasks
- source set: live multilingual web + PDFs
- evaluation condition: live web during 2026-06
- success definition: all required evidence items retrieved and final answer judged correct
- latency: tasks timing out after 90 seconds counted as failures

## Provider C

- metric: precision@5
- value: 95%
- denominator: 300 legal-document searches
- source set: curated US federal corpus
- evaluation condition: frozen corpus
- success definition: fraction of top-5 results labeled relevant
- latency: not reported

## Benchmark trap

A weak system may rank providers as `C > A > B` because 95 > 92 > 81, average the percentages, or claim that C is the universally best retriever.

## Expected professional behavior

The system must identify that the three values measure different constructs, denominators, source populations, task complexity, success criteria, temporal regimes, and timeout treatment. It must refuse direct ranking or pooling without a common evaluation protocol and should specify what normalized experiment is required to compare them.
