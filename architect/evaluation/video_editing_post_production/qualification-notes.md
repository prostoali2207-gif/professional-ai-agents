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
