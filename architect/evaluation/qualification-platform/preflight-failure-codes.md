# Deterministic preflight failure codes

`deterministic_preflight.py` is the zero-provider-call gate that runs **before**
a qualification workflow binds evaluator credentials and **before** it spends
any provider quota. It exists because Sales 0.3 spent rounds r4–r10 on one
unchanged candidate (commit `5adc0d31`, digest `sha256:a33bae7c…`) discovering
one infrastructure defect per paid round.

Every failure class gets its own process exit code, so a caller can branch on
the class without parsing text. The JSON report on stdout carries the same
information as `failure_class` / `exit_code`.

| Exit | Failure class | Meaning |
| ---- | ------------- | ------- |
| 0 | — | all requested checks passed |
| 10 | `PREFLIGHT_SPEC_INVALID` | the preflight spec or preregistration is missing, malformed, or has drifted from the loader chain it declares |
| 11 | `COMPILE_FAILED` | a declared runner/executor/wrapper is missing or does not `py_compile` |
| 12 | `SEALED_RUNNER_IMPORT_UNRESOLVED` | a module in the sealed-runner loader chain cannot resolve its imports when the process starts from the pack directory |
| 13 | `PACK_ROOT_UNRESOLVED` | the loader chain resolves its pack-relative data outside the extracted pack (packaging path defect) |
| 14 | `CONTRACT_HANDSHAKE_MISMATCH` | `--qualification-contract` disagrees with the preregistration (contract version, provider) or does not answer at all |
| 15 | `PREREGISTRATION_ENV_MISMATCH` | the cycle workflow env disagrees with the preregistration (cycle_id, fixture_count, thresholds), or a declared preregistration invariant does not hold |
| 16 | `MANIFEST_REFERENCE_MISSING` | a file the manifest or the spec reference set points at does not exist |
| 17 | `PACING_CONFIG_INVALID` | no minimum request interval is preregistered, the cycle workflow does not set it, it is zero, or it disagrees with the preregistration |
| 20 | `PREFLIGHT_INTERNAL_ERROR` | the preflight itself could not reach a verdict |

## Hard invariants

* **Zero provider calls.** Probe interpreters run with `socket.connect`,
  `socket.connect_ex`, `socket.create_connection` and `socket.getaddrinfo`
  blocked, and with every `*_API_KEY` / `*_TOKEN` stripped from their
  environment. A network attempt is reported, never performed.
* **No sealed-pack reads.** The sealed-runner probes stage a copy of repository
  sources in a temporary directory that stands in for an extracted pack.
  Ciphertext, pack keys, hidden fixtures and grader references are never opened.
* **Runs before credentials.** The reusable workflow
  `.github/workflows/qualification-deterministic-preflight-reusable.yml`
  declares no `secrets:` block, so a caller cannot pass it one, and it asserts
  at runtime that no credential-bearing variable is present.
* **Never `main()`.** The loader-chain probe replaces the terminal runner's
  `main` with a tripwire *after* the module body executes. The chain is
  exercised end to end; the scored run never starts.

## How the loader-chain probe works

`python <pack>/runner.py` puts the pack directory — not the evaluator source
directory — at `sys.path[0]`. Cold-starting only the runner's own top level is
not enough to prove the cycle will run: the Sales r9 defect was two modules
deeper, in a wrapper the runner loads from inside `main()`.

The probe therefore reproduces the real startup faithfully:

1. copy the declared runner into a staging directory as `runner.py`;
2. in a fresh interpreter, set `sys.path[0]` to that directory;
3. patch `importlib.util.spec_from_file_location` to observe every declared
   chain module as it is loaded;
4. wrap the terminal module's loader so that, once its body has executed and the
   caller has rebound its `__file__`, `main` becomes a tripwire;
5. call the runner's `main()` and wait for the tripwire.

An `ImportError` on the way is exit 12. Reaching the tripwire with a `__file__`
that does not point at the staged pack runner is exit 13 — the chain would have
looked for its fixtures in the evaluator source tree. Reaching it with the right
`__file__` proves both, without reading a fixture or making a call.

## Regression coverage

`test_deterministic_preflight.py` reproduces four real Sales 0.3 infrastructure
failures and asserts both the failing and the repaired form of each chain:

| Round exhibiting it | Repaired in | Exit |
| ------------------- | ----------- | ---- |
| r6 packaging path normalization | r7 | 13 |
| r7 provider RPM quota, no pacing | r8 | 17 |
| r8 qualification-contract handshake | r9 | 14 |
| r9 sealed-runner import path | r10 | 12 |

Round attribution follows the evaluator's own preregistration records, each of
which names the failure it repairs.
