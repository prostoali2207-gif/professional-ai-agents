# Issue #175 — Market Intelligence holistic factory qualification

Status: preregistered fresh subscription-backed Codex qualification cycle.

This cycle reuses the exact frozen Market & Competitive Intelligence v0.3
assembly and tests it on a fresh evaluator-owned pack. It does not alter the
candidate, the historical Gemini graders, or generic qualification-platform
infrastructure.

## Route

`deterministic/no-model -> compatible prior evidence -> isolated Codex CLI canary -> fresh scored Codex qualification -> sanitized report -> release verdict`

The historical Gemini PASS remains calibration/prior evidence only because its
provider-backed workflow ran on `pull_request`, which is not eligible under the
current paid-execution policy. The fresh release decision is therefore made on
the Codex cycle recorded here.

## Isolation

The held-out plaintext and evaluator key remain evaluator-owned. The repository
contains only encrypted pack transport and its frozen digests before candidate
execution. Each candidate trial is a fresh ephemeral Codex CLI session with:

- the exact frozen base + overlay injected as the role contract;
- only candidate-visible task fields supplied;
- expected decisions omitted;
- an isolated empty working directory;
- read-only sandbox, no web search, no MCP/plugin configuration, and no API key;
- schema-constrained final output and an observable event trace.

## Stages

1. `--preflight`: compile runner, verify candidate blobs/assembly digest,
   preregistration, encrypted transport digest, authenticated decryption,
   plaintext digest, fixture cardinality/families, schemas, CLI version and
   ChatGPT login status. Zero model calls.
2. `--canary`: one public unscored task through the exact Codex runtime.
3. `--run`: three isolated trials of all twelve single-decision families and
   three isolated trials of the fresh practical/adversarial case. Zero scored
   retries; first scored mismatch ends the run as `REVISE`.
4. Emit a sanitized report containing identities, aggregate/family results,
   runtime evidence and verdict, but no held-out prompts or expected keys.

## Rendered gate

Not applicable. The qualified profession produces analytical evidence packets,
not visual or media artifacts. Its observable produced-output gate is the fresh
end-to-end structured evidence packet; visual/media production is explicitly
outside this core's authority.

