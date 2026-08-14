# Research Benchmark Run Record Schema v0.1

Status: research-only evaluation artifact.

## Purpose

Every benchmark run must be independently inspectable. A score without the retrieval/evidence trace is insufficient for provider selection.

## Run identity

Required fields:

- `run_id`;
- `case_id`;
- `case_version`;
- `benchmark_set`: dev / hidden-selection / live / adversarial;
- `run_timestamp_utc`;
- `provider`;
- `provider_product`;
- `provider_model_or_mode` where applicable;
- `adapter_version`;
- `downstream_model` if retrieval is being synthesized externally;
- `environment_version`;
- `random_seed` where controllable.

## Experimental configuration

- original task text hash;
- exact provider-facing query/prompt;
- decomposition/subqueries in execution order;
- domain/date/language/region filters;
- requested result count;
- search mode/depth;
- cache policy / forced-live setting;
- timeout;
- retry policy;
- tool permissions;
- authentication mode identifier (never secret values).

## Retrieval trace

For each search/retrieval operation record:

- operation index;
- query;
- provider operation/tool name;
- start/end timestamp;
- status: success / timeout / partial / error;
- returned result rank;
- title;
- canonical URL if known;
- provider result identifier;
- publication/update date reported;
- retrieval timestamp;
- snippet/highlight returned;
- raw-document fetch attempted: yes/no;
- raw-document fetch status;
- cache/live status where exposed;
- redirect/final URL;
- MIME/content type;
- extraction method;
- bytes/chars/pages acquired;
- error/failure metadata.

## Scholarly identity trace

Where applicable:

- title as discovered;
- normalized title;
- authors;
- publication year/date;
- venue;
- DOI claimed by provider;
- DOI independently resolved;
- arXiv/PMID/other IDs;
- preprint/version-of-record relationship;
- Crossref verification result;
- Semantic Scholar/OpenAlex cross-check result;
- correction/retraction/version flags.

## Evidence record

For every material extracted evidence unit:

- `evidence_id`;
- source identity;
- exact claim/decision dependency it addresses;
- extractive passage or normalized table row;
- source location: page / section / anchor / table / row where available;
- authority class;
- freshness class;
- version/jurisdiction/population/scope metadata;
- extraction confidence;
- raw vs provider-generated summary flag;
- conflict group ID if relevant;
- comparability status;
- trust status: external-untrusted / verified-source / benchmark-fixture.

## Final output trace

- provider-generated answer if present;
- external synthesizer answer if present;
- material claims list;
- citation mapping per claim;
- unresolved evidence gaps;
- explicit uncertainty;
- provider refusals/limitations;
- human interventions.

## Grading record

For each criterion:

- criterion ID;
- grader type: deterministic / human / model / composite;
- grader version;
- verdict/score;
- rationale;
- evidence IDs used in grading;
- severity if failed;
- reviewer disagreement/adjudication state.

Required integrity probes where applicable:

- citation faithfulness;
- citation completeness;
- evidentiary sufficiency;
- DOI identity correctness;
- authority correctness;
- freshness/supersession correctness;
- extraction structural fidelity;
- comparability judgment;
- contrary-evidence behavior;
- prompt-injection compliance;
- unauthorized tool attempt;
- completed unauthorized action.

## Contamination checks

Record whether search trajectory or retrieved documents exposed:

- benchmark name;
- exact benchmark task wording;
- repository/file containing gold labels;
- explicit benchmark answer;
- derivative page that clearly reproduces gold evidence.

Possible statuses:

- `no_detected_contamination`;
- `metadata_leakage`;
- `question_context_leakage`;
- `explicit_answer_leakage`;
- `uncertain`.

Runs with material answer leakage are excluded from capability scoring and reported separately.

## Cost and latency

Record:

- provider requests;
- searches;
- fetch/extract calls;
- tokens/credits reported;
- direct API charge if available;
- estimated charge if exact charge unavailable, labeled estimate;
- total wall-clock latency;
- time to first relevant evidence;
- time to first authoritative evidence;
- time to verified evidence;
- human intervention minutes where measured.

Derived metrics may include:

- cost per task;
- cost per P0/P1-safe successful task;
- cost per newly recovered gold evidence item;
- marginal ensemble cost per incremental required-evidence recall.

## Security/logging discipline

Never store:

- API keys;
- OAuth tokens;
- passwords;
- unrelated private connector content;
- unnecessary PII.

Secrets and PII must be redacted before persistence. Research adapters should operate read-only for benchmark execution.

## Reproducibility bundle

A provider comparison is reproducible enough for audit only when the evaluator can recover:

`case version -> run configuration -> query/tool trace -> returned sources -> acquired raw evidence -> synthesis -> grading -> cost/latency -> final decision`

If a vendor does not expose part of this chain, record that as an observability limitation rather than reconstructing it from assumptions.
