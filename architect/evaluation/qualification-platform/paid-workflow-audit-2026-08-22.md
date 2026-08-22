# Paid Workflow Trigger Audit — 2026-08-22

## Scope

Repository: `prostoali2207-gif/professional-ai-agents`.

Objective: identify GitHub Actions workflows that can consume model/provider quota as a side effect of ordinary `push` or `pull_request` events, and remove that accidental-spend path without weakening required release evidence.

## Evidence rule

A workflow is considered materially spend-capable when it invokes a provider-backed candidate, semantic gate, held-out authoring/grading, or scored qualification using credentials such as `OPENAI_API_KEY` or `GEMINI_API_KEY`.

Automatic deterministic/static checks and no-API sealed preflight remain allowed.

## Auto-paid workflows found and repaired

The following workflows previously combined automatic repository events with provider-backed execution and are now manual-only with explicit paid-run authorization:

- `.github/workflows/sales-model-cost-comparison.yml`
- `.github/workflows/paid-media-professional-core-gate.yml`
- `.github/workflows/external-automotive-video-qualification.yml`
- `.github/workflows/video-editing-post-production-qualification.yml`
- `.github/workflows/uae-market-intelligence-applied-qualification.yml`
- `.github/workflows/strategist-v0_1-sealed-qualification.yml`

Previously repaired in the immediately preceding cost-safety change:

- `.github/workflows/sales-0-2-runtime-smoke.yml`
- `.github/workflows/sales-0-3-fresh-independent-qualification.yml` — automatic events retain only no-API preflight; paid runtime/scored jobs require explicit manual authorization.

## Reviewed but not classified as accidental paid generation

- `.github/workflows/qualification-platform-static.yml` is deterministic/static and does not execute model generation.
- `.github/workflows/architect-research-rce-semantic-smoke.yml` runs semantic generation only on `workflow_dispatch`; its pull-request path performs deterministic checks plus a model-availability probe without generation.
- Existing workflows that are already `workflow_dispatch`-only remain manual release actions; they do not create paid side effects from ordinary pushes/PRs.

## Result

Ordinary repository development should no longer start the identified provider-backed qualification/model-generation workloads merely because code was pushed or a PR was opened.

This change modifies execution authorization only. It does not change frozen candidates, hidden fixtures, graders, thresholds, model/runtime identity, or the professional evidence required for a release PASS.

## Remaining control

Future provider-backed workflows must follow `paid-execution-policy.md`: no paid generation from ordinary automatic repository events; deterministic/static/no-API gates first; then explicit authorization for the paid stage.
