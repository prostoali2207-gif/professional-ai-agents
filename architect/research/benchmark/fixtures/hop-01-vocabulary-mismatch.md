# HOP-01 fixture — Vocabulary mismatch / reasoning-intensive retrieval

Status: frozen conceptual fixture for testing retrieval across terminology gaps.

## User-facing task

A user asks:

> Find evidence about why a search system can miss the right document even when the document is conceptually relevant, because the user and document use different wording. Compare what lexical and semantic retrieval each contribute and what hybrid strategy is defensible.

The prompt deliberately avoids specialist terminology such as `vocabulary mismatch`, `query expansion`, `candidate recall`, `reasoning-intensive retrieval`, `semantic evidence`, or `hybrid retrieval`.

## Required inferred concepts

A competent retriever should infer and search for at least some of:

- vocabulary mismatch;
- lexical retrieval / BM25;
- semantic retrieval;
- query expansion;
- candidate-set recall;
- hybrid / fusion retrieval;
- reasoning-intensive retrieval.

## Gold evidence families

At least one credible source should support each of these distinct claims:

1. lexical retrieval can fail when relevant evidence uses different wording;
2. semantic retrieval can bridge vocabulary gaps but is not universally superior;
3. no reranker can recover a relevant document that never enters the candidate set;
4. retrieval performance depends on query-generation style and task regime;
5. hybrid / ensemble retrieval is therefore an empirical design hypothesis rather than a universal rule.

## Hard negatives

- generic SEO articles that say “semantic search understands meaning” without empirical evidence;
- vendor pages claiming universal superiority of their own retriever;
- benchmark results from one corpus generalized to all retrieval tasks;
- downstream answer-quality scores used as a substitute for retrieval recall.

## Query-trace scoring

Record the original query and all reformulations.

Pass requires visible terminology evolution rather than repeated paraphrases of the user wording.

Strong behavior:

`operational wording -> inferred IR concept -> evidence-seeking query -> contrary-evidence query -> synthesis`

Weak behavior:

`operational wording -> five near-identical natural-language searches`

## Evidence discipline

The system must preserve the tension between empirical findings. For example, one benchmark may show BM25 outperforming tested LLM retrievers under keyword-oriented agent subqueries, while another method may show gains from semantic evidence or query expansion. These are scope-dependent findings, not a contradiction to erase.

## Critical failures

P1:

- never infers the specialist concept and misses the relevant literature;
- presents one retriever family as universally superior based on a single benchmark;
- uses provider marketing as decisive evidence.

## Architectural implication

Query decomposition is a professional research capability. Retrieval adapters alone cannot solve hidden terminology gaps unless the research layer can infer intermediate concepts and evolve queries.
