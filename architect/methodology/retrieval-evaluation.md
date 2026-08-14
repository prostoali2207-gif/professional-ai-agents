# Retrieval and Knowledge Access Evaluation

Status: v0.1.

## Principle

A knowledge layer is useful only if the agent can retrieve the right evidence for the right decision. Storage volume is not a competency.

Evaluate retrieval separately from downstream generation.

## Retrieval failure taxonomy

- **miss**: required evidence exists but is not retrieved;
- **noise**: irrelevant material crowds out useful evidence;
- **scope error**: source is topically relevant but wrong jurisdiction/version/population/context;
- **authority error**: weaker evidence displaces a stronger claim-appropriate source;
- **freshness error**: stale evidence is used for a volatile claim;
- **reasoning-retrieval failure**: relevance requires intermediate reasoning that lexical/semantic similarity does not expose;
- **provenance loss**: retrieved synthesis cannot be traced to the underlying source;
- **prior override**: model prior is preferred despite stronger retrieved evidence;
- **retrieval overreach**: retrieved evidence is stretched beyond what it supports.

## Evaluation dimensions

For profession-specific retrieval sets measure, where applicable:

- recall of required evidence;
- precision/relevance of retrieved evidence;
- ranking quality (for example nDCG/MRR where labels support it);
- authority appropriateness;
- freshness correctness;
- scope correctness;
- citation/provenance correctness;
- downstream faithfulness to retrieved evidence;
- robustness to distractors and near-match documents;
- retrieval latency/cost when operationally material.

Do not collapse all dimensions into one score if different failure types have different professional consequences.

## Reasoning-intensive retrieval

Some professional queries cannot be solved by matching the user's wording to a document. The retrieval system may need to infer the underlying decision, decompose it into evidence needs, retrieve across multiple sources, and synthesize them.

Evaluation sets therefore need cases where:

1. the relevant source does not share obvious vocabulary with the query;
2. multiple sources are required;
3. a plausible but wrong near-match exists;
4. the newest source supersedes an older source;
5. the authoritative source conflicts with popular practitioner content.

## Gold evidence sets

For high-value competencies maintain small expert-reviewed evidence sets:

`task -> required claim(s) -> acceptable source(s) -> unacceptable distractors -> freshness/scope constraints`.

Gold sets are evaluation artifacts, not necessarily runtime retrieval corpora.

## Knowledge maintenance loop

When a source changes or becomes superseded:

1. identify dependent claims;
2. identify dependent competency units;
3. identify dependent workflows/evals;
4. update or invalidate derived knowledge;
5. rerun retrieval and downstream regression tests.

## Gate

A professional agent fails knowledge access if it produces a correct-looking answer while retrieving materially wrong, stale, out-of-scope, or non-authoritative evidence.