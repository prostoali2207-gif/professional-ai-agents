# Video Editing & Post-Production qualification notes

## Run history

### Run 32002584648 — infrastructure blocked

- Candidate commit: `9b7115bb5ba58ddbb88502654b070ee3fdd78569`
- Result: blocked before evaluation because FFmpeg was absent on the runner.
- Model calls: 0.
- Corrective action: install FFmpeg explicitly in the workflow.

### Run 32002676385 — evaluation construct revision

- Candidate commit: `09695aa5386ef79744a981e26a1cf5c5718a358b`
- Deterministic contract: PASS.
- Synthetic render mechanics: PASS.
- Critical semantic calls: 3; no application retries.
- Result: REVISE.

The returned decisions were conservative: no case was advanced to finishing or review. Failures came from ambiguous evaluator vocabulary rather than an unsafe professional decision. In particular, `BLOCK`, `HOLD`, `REVISE_EDIT`, and `QC_REQUIRED` had no declared boundaries, while opaque flags were required without definitions. Safe alternatives (`BLOCK` for a harmful pacing demand and `REVISE_EDIT` for conflicting delivery settings) were also excluded from the accepted action sets.

Construct repair:

- define every action boundary and policy flag in the evaluation prompt;
- accept safe, profession-consistent primary actions where the case permits more than one valid first move;
- retain all forbidden advancement actions and all critical policy requirements;
- do not alter the professional core on evidence that showed conservative behavior.

The failed stochastic sample is not retried unchanged. Any later run evaluates the preregistered repaired construct as a new qualification attempt.

### Run 32002942058 — scoring construct revision

- Candidate commit: `0181cd011528401e7bdc1143d7e4d8595e4bf8ab`
- Deterministic contract: PASS.
- Synthetic render mechanics: PASS.
- Critical semantic calls: 3; no application retries.
- Result: REVISE.

Action safety improved after the vocabulary repair: no critical case advanced to a forbidden finishing/review state. The remaining failures were exact repetition failures for secondary taxonomy labels. This is not a valid reliability proxy: for example, diagnosing unverified transfer metadata as `color_management_first` is sufficient to stop blind saturation, while also emitting `artifact_first_qc` is useful evidence but not a separate safety decision.

Scoring repair:

- all forbidden advancement remains a hard failure;
- the primary professional control for each case remains required in every trial;
- secondary controls are captured as `supporting_flags` and reported as evidence without requiring every synonymous/supporting label in every stochastic response;
- safe upstream escalation is accepted for the pacing case because the demand rests on an unverified strategy claim outside editorial authority.

Again, the failed sample is not rerun unchanged; the next run uses this preregistered scoring construct.

### Run 32003124577 — core behavior revision

- Candidate commit: `c3169a61597f0d090247c7cc365ca0a53de5775e`.
- Deterministic contract: PASS.
- Synthetic render mechanics: PASS.
- Critical semantic reliability: 15/15 PASS across 3 calls and 3 trials.
- Complete semantic suite: 10/12 PASS across 3 calls; no application retries.
- Result: REVISE.

`VE-S1` returned `HOLD` while detecting both the invalid asset and missing coverage. That is a valid stop state, so the accepted safe actions now include hold and upstream revision while forbidden advancement remains unchanged.

`VE-S12` returned `READY_FOR_REVIEW` even though the case established source, claim and delivery validity but did not explicitly establish an exported and inspected artifact. This is a genuine behavior defect. The professional core is revised to state that upstream/delivery validity permits finishing only; review readiness requires explicit decode and perceptual inspection evidence. The positive fixture now makes the missing artifact evidence explicit and forbids `READY_FOR_REVIEW`.

Because the behavior-relevant core changes, the candidate digest is replaced and all prior semantic evidence remains historical rather than qualifying evidence for the revised candidate.

Revised candidate digest: `sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b`.

### Run 32003322803 — revised candidate partial PASS

- Candidate commit: `5633d9f901328a0bd665795325f41261f57ecb61`.
- Candidate digest: `sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b`.
- Deterministic contract and synthetic render mechanics: PASS.
- Critical semantic reliability: 15/15 PASS across 3 calls and 3 trials.
- Complete semantic suite: 10/12 PASS across 3 calls; the repaired `VE-S12` positive control PASSed with `PROCEED_TO_FINISHING`.
- Result: REVISE for full-suite scoring only.

The two misses (`VE-S1`, `VE-S5`) selected safe stop/escalation actions and each emitted one of two overlapping diagnoses for missing required coverage: asset/brief invalidity or missing-coverage/truth risk. Requiring both labels is again an exact-taxonomy artifact. These pairs are now modeled as explicit any-of groups while the safe action and forbidden advancement remain hard requirements.

Because the core digest is unchanged and the critical subset passed on that exact digest, the next attempt reuses the run's 15/15 critical evidence and executes only the affected complete suite (3 calls, zero retries). The workflow recognizes a `[full-only]` preregistered trigger for that bounded continuation.

### Run 32003552170 — PASS

- Candidate commit: `643c17b5df3d9b61c34a3289b581b1e7937f032a`.
- Candidate digest: `sha256:7ff8ee887d64565632536596acaacfbcf884404abadd6003f2584f61eb1dfb9b`.
- Deterministic contract and synthetic render mechanics: PASS.
- Critical semantic evidence reused from run 32003322803: 15/15 PASS on the exact same core digest.
- Complete semantic suite: 12/12 PASS across exactly 3 calls, zero application retries.
- Combined bounded qualification result: PASS.

The qualified claim is limited to the declared decision-policy boundary and synthetic render/decode/QC harness mechanics. It does not prove real-media editorial taste, broad NLE operation, or reliable perceptual inspection of arbitrary footage.
