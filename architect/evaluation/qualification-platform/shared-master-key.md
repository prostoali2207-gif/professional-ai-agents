# Shared master key for sealed qualification packs

Status: qualification infrastructure.

## Problem

Per-agent repository secrets do not scale when multiple independent qualifications run in parallel. The evaluator should not need a new GitHub Actions secret for every professional candidate.

## Contract

New qualification manifests should prefer one repository secret:

`QUALIFICATION_SEALED_PACK_MASTER_KEY`

Each sealed pack declares a public, immutable derivation context in `sealed_pack.key_derivation`:

```json
{
  "scheme": "hkdf-sha256-v1",
  "master_env": "QUALIFICATION_SEALED_PACK_MASTER_KEY",
  "context": "<stable unique qualification cycle / pack id>"
}
```

The qualification preflight derives a 32-byte pack key using HKDF-SHA256 with a fixed domain-separation salt and the declared context, then encodes it as a Fernet key. Different contexts therefore receive different effective encryption keys while GitHub stores only one master secret.

The manifest continues to freeze `key_fingerprint_sha256`, but this fingerprint is now for the derived effective pack key, never the master secret.

## Integrity properties

- the master secret value is never written to the repository, manifest, logs, reports, or artifacts;
- the derivation context is public and must be unique/stable for the qualification cycle;
- changing context changes the effective pack key and invalidates the sealed transport until it is intentionally re-encrypted;
- the existing ciphertext/decrypted-pack/component digests remain required;
- candidate-facing fixtures/grader contents are unchanged by this mechanism;
- key derivation is evaluator infrastructure, not candidate behavior;
- direct per-pack `key_env` remains supported for existing frozen qualification cycles.

## Migration rule

Do not rewrite an already executed/frozen qualification merely to adopt the shared master secret. Migrate when creating a new sealed transport or when an unexecuted transport is intentionally re-encrypted without changing its underlying fixtures, grader, thresholds, candidate binding, or stochastic policy.

## Reusable workflow

`.github/workflows/qualification-preflight-reusable.yml` accepts either:

- `sealed_pack_master_key` for the preferred derived-key mode; or
- `sealed_pack_key` for legacy direct-key mode.

New callers should map `sealed_pack_master_key` to the single repository secret `QUALIFICATION_SEALED_PACK_MASTER_KEY`.
