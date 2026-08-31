# Frozen professional artifact qualification flow

Status: evaluation infrastructure. This is not a professional core and must not change candidate behavior.

## Purpose

Allow the existing Agent Architect protocol-v2 behavioral runner to execute an immutable professional candidate whose identity is a Git **blob SHA**, rather than requiring the candidate to be the repository `HEAD` or `architect/SKILL.md`.

This closes an infrastructure gap exposed by held-out qualification attempts for professional cores represented as frozen markdown artifacts.

## Components

- existing runner: `architect/evaluation/harness/runner.py`
- generic adapter: `architect/evaluation/harness/adapters/openai_frozen_artifact_adapter.py`
- evaluator-owned manifest and sealed fixtures outside candidate-visible surfaces

## Integrity model

The manifest's `candidate_sha` is the exact frozen Git blob SHA.

The adapter:

1. resolves `candidate_sha` using `git cat-file`;
2. rejects non-blob objects;
3. loads the blob directly, never a mutable working-tree candidate path;
4. executes one fixture step in one fresh adapter process;
5. exposes only evaluator-authorized tools/resources;
6. rejects evaluation/grader/held-out resource reads through `read_resource`;
7. captures tool traces and side effects during execution;
8. reports the exact candidate blob SHA, runtime adapter version and model.

The existing runner independently verifies that returned `candidate_identity.sha` equals the manifest `candidate_sha`, hashes each fixture before execution, creates isolated trial workspaces, and writes replayable run records.

## Required checkout preparation

The Git object database must contain the frozen candidate blob. The candidate file does **not** need to exist in the infrastructure branch working tree.

Before qualification, fetch the immutable candidate ref that contains the blob. Example:

```bash
git fetch origin agent/content-architecture-core-2026-08
```

Then verify:

```bash
git cat-file -t 67ac707be93cd46c0303c54eef3d73122c72c876
git cat-file -p 67ac707be93cd46c0303c54eef3d73122c72c876 >/dev/null
```

The first command must print `blob`.

## Invocation

The evaluator creates its own sealed protocol-v2 manifest and fixtures. Do not commit hidden fixtures or grader keys into candidate branches.

Example command shape:

```bash
python architect/evaluation/harness/runner.py \
  --manifest /sealed/content-architecture/manifest.json \
  --candidate-command 'python architect/evaluation/harness/adapters/openai_frozen_artifact_adapter.py' \
  --out /sealed/content-architecture/run-output
```

Runtime environment requires `OPENAI_API_KEY`. `FROZEN_ARTIFACT_MODEL` may be set by the preregistration/evaluator; the resulting model name is recorded in every candidate result.

## Fixture surface

A normal fixture step passes an `input` object with at least:

```json
{
  "task": "candidate-visible held-out assignment"
}
```

Optional evaluator-controlled fields:

- `allowed_resources`: explicit public/non-evaluation repository resources candidate may read;
- `fixture_tools`: deterministic evaluator-controlled tool responses/side effects;
- `observed_state`: candidate-visible independently observed state;
- `max_tool_rounds`: bounded tool loop limit.

The adapter never loads grader keys or expected answers.

## Isolation and stochastic repeats

`runner.py` starts a separate adapter process for every fixture step and creates a new temporary workspace for each fixture trial. Repeated trials therefore have no hidden transcript continuity. Any cross-step state must be explicitly represented in the trial workspace or evaluator-controlled fixture surface.

For stateless professional-core qualification, prefer one-step fixtures unless a competency genuinely requires multi-step interaction.

## What this infrastructure proves — and does not prove

A successful adapter/harness smoke test proves only that the exact frozen candidate can be invoked reproducibly and observed under the registered protocol.

It does **not** prove professional qualification. Qualification still requires the preregistered held-out/adversarial pack, frozen thresholds, graders, required repeats and composition/practical gates.

Do not treat infrastructure PASS as candidate PASS.
