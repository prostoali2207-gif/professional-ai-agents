# GitHub Models behavioral access result — 2026-08-15

Status: provider lifecycle failure; do not retry automatically.

## Empirical run

A GitHub Actions job on `research/research-architecture-benchmark-2026-08` requested:

- `permissions: models: read`
- model: `openai/gpt-4.1-mini`
- endpoint: `https://models.github.ai/inference/chat/completions`

The Actions job confirmed `GITHUB_TOKEN` permissions included `Models: read`, but the inference endpoint returned HTTP 410 with code `github_models_retirement_brownout` and message that GitHub Models was unavailable as part of retirement.

## External lifecycle verification

GitHub's official changelog states GitHub Models was fully retired on 2026-07-30, including playground, model catalog, inference API, and BYOK.

## Benchmark implication

- Historical/static documentation describing GitHub Models free inference is stale for current architecture decisions.
- Provider lifecycle must be verified immediately before integration work.
- A technically valid auth setup can still fail because the product itself has been retired.
- Repeated retries would waste CI minutes and are prohibited unless explicitly reproducing the historical failure.

## Decision

`REJECT_CURRENT_PROVIDER_PATH: RETIRED`

The behavioral synthesis harness should move to another currently supported free-tier inference provider.
