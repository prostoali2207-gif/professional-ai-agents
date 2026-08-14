# EXTRACT-02 fixture — NIST AI RMF PDF structural fidelity

Status: frozen extraction fixture derived from NIST AI RMF 1.0.

## Source

NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0), January 2023.

Canonical publication DOI: `10.6028/NIST.AI.100-1`.

The fixture intentionally targets a PDF table continuation where flat text extraction can preserve words but lose row/column structure.

## Gold region

Target visual page: PDF page showing the continuation of Table 1, followed by section `5.2 Map`.

Expected structural units:

- table title: `Table 1: Categories and subcategories for the GOVERN function. (Continued)`;
- left-column category `GOVERN 5: Processes are in place for robust engagement with relevant AI actors.`;
- associated right-column subcategories `GOVERN 5.1` and `GOVERN 5.2`;
- left-column category `GOVERN 6: Policies and procedures are in place to address AI risks and benefits arising from third-party software and data and other supply chain issues.`;
- associated right-column subcategories `GOVERN 6.1` and `GOVERN 6.2`;
- table boundary must end before heading `5.2 Map`;
- page provenance must remain recoverable.

## Why this is adversarial

A flattened extractor may:

- preserve all words while losing which subcategory belongs to which category;
- merge the final table rows into the following prose section;
- omit the `(Continued)` state and therefore lose cross-page table continuity;
- confuse document page numbering with PDF page indexing;
- drop repeated headers/footers without recording their page-location role;
- reorder multi-column text.

## Scoring

### Content recall

Required gold strings must be present without semantic substitution.

### Structural fidelity

Must preserve:

`table -> category -> subcategory relation`

for GOVERN 5 and GOVERN 6.

### Boundary fidelity

`5.2 Map` must be recognized as the next prose section, not as a table cell.

### Provenance

Every extracted gold unit must retain source identifier and page location.

### Hallucination

Zero invented category/subcategory relationships.

## Critical failures

P0:

- fabricated table cells;
- assigning a subcategory to the wrong parent while presenting it as exact extraction.

P1:

- losing table structure so that claim-bearing relationships cannot be reconstructed;
- claiming exact PDF inspection when only a secondary text representation was available.

## Benchmark implication

Extraction quality is not equivalent to text presence. Provider evaluation must score structural and provenance fidelity separately from raw token recall.
