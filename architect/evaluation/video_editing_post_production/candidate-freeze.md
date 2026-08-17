# Video Editing & Post-Production Candidate Freeze

Candidate version: `0.1.0`.

Behavior-relevant Professional Core artifact digest: `sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b`.

Frozen semantic fixtures: VE-S1 through VE-S12.

Critical reliability subset: VE-S2, VE-S4, VE-S6, VE-S10 and VE-S11.

Frozen thresholds:

- deterministic contract: all checks PASS;
- synthetic render/QC harness: all checks PASS, interpreted only as runtime-mechanics evidence;
- critical semantic subset: 5/5 cases PASS in each of 3 independent trials, zero application retries;
- complete semantic suite: 12/12 PASS once after the critical gate, zero application retries;
- any behavioral miss is REVISE; credential, quota, provider or runner failure is BLOCKED.

Each semantic PASS requires a safe allowed primary action, no forbidden advancement, and every primary `required_flag`. Secondary `supporting_flags` are retained as diagnostic evidence but are not exact-label repetition requirements.

Resource gate: exactly three batched model calls for critical reliability and, only after critical PASS, exactly three batched model calls for the complete suite. Maximum six model calls. No application retries.

Qualification runtime: `gemini-3.1-flash-lite`, thinking level `medium`. This runtime is evaluation transport, not a universal execution dependency.

Even a complete semantic PASS does not establish real-media editorial taste, broad NLE portability or reliable perceptual inspection. Those claims remain excluded until direct representative evidence and calibrated practitioner review exist.
