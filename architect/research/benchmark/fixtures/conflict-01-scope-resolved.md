# CONFLICT-01 fixture — apparent conflict resolved by scope

Status: synthetic frozen fixture for deterministic evaluation.

## Research question

"Which research retriever is more accurate: Retriever A or Retriever B?"

## Source A

A controlled benchmark reports Retriever A at 70% evidence recall on English technical documentation using short keyword-oriented queries and passage-level retrieval.

## Source B

A separate controlled benchmark reports Retriever B at 78% evidence recall on multilingual scholarly documents using natural-language questions and document-level retrieval.

## Trap

Both sources are credible and both percentages are accurate, but they do not measure the same retrieval condition.

## Required behavior

The research system must identify at least these comparability differences:

- corpus/domain;
- language regime;
- query formulation;
- retrieval unit;
- benchmark/task distribution.

It must refuse to conclude `B > A` globally from `78 > 70`.

## Acceptable conclusion

The evidence supports only condition-specific statements. A direct winner requires a matched evaluation on the same corpus, queries, retrieval unit, relevance judgments and scoring protocol.

## Failures

P1:

- ranks B above A solely from the percentages;
- averages the scores;
- omits the scope mismatch while making a general recommendation.
