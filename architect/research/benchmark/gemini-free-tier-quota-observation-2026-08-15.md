# Gemini free-tier quota observation — 2026-08-15

Status: operational evidence; not a behavioral verdict.

## Observation

Perturbation A attempted to start after the frozen behavioral smoke had been adjudicated PASS. The first model call was rejected before inference with HTTP `429 RESOURCE_EXHAUSTED`.

Provider response identified:

- metric: `generativelanguage.googleapis.com/generate_content_free_tier_requests`
- quota id: `GenerateRequestsPerDayPerProjectPerModel-FreeTier`
- model: `gemini-3.5-flash`
- quota value observed: `20`
- location dimension: `global`

GitHub Actions run: `31872992194`.

No behavioral case completed. Therefore Perturbation A is **NOT_RUN / QUOTA_BLOCKED**, not FAIL.

## Cost-engineering decision

Do not:
- spin on retries after an explicit daily-project-model quota violation;
- switch to a second user key/project merely to evade the intended free-tier cap;
- enable billing only to complete a non-urgent research perturbation;
- treat quota exhaustion as model-quality evidence.

Resume the controlled perturbation after quota renewal or only after an explicit evidence-based decision that paid execution is necessary.

## Architecture implication

Research adapters must expose and classify `RATE_LIMIT`, `DAILY_QUOTA`, `CAPACITY_UNAVAILABLE`, and behavioral/model failures separately. Retry policy must depend on the failure class; generic exponential retry is wasteful for hard daily quota exhaustion.
