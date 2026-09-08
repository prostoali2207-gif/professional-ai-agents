# B2b unblind adjudicator task — QRE cycle 2

Status: **NOT AUTHORIZED UNTIL A VALID B2a SEALED CHECKPOINT EXISTS**.

Use a fresh context different from B2a.

Inputs supplied to you must include:
- complete `blind-judgments-v0.2.json` from B2a;
- B2a reported canonical SHA-256 seal.

Before reading the author key:
1. save the supplied blind JSON locally;
2. run `python validate_blind_judgments.py <file>`;
3. run `python seal_blind_checkpoint.py <file>`;
4. verify the recomputed canonical hash exactly equals the supplied B2a seal.

If it does not, STOP.

Only after seal verification may you read:
- `../stage-b/calibration-reference-v0.1.md`;
- `compare_calibration.py`.

Run deterministic comparison with the exact seal. Then professionally adjudicate mismatches and legitimate disagreements. Do not change the blind judgment artifact.

Before any candidate output is viewed, freeze:
- competency floor(s);
- aggregate threshold if used;
- P0 max = 0;
- P1-P5 mandatory practical rule;
- disagreement/adjudication policy;
- repeat/stochastic policy;
- Stage-C resource and stop conditions.

Final verdict must be:
`B2_CALIBRATED_PASS | B2_CALIBRATION_FAIL | NOT_EXECUTABLE`.

Do not execute/inspect the QRE candidate, Stage C or Stage D. No metered API or parallel/delegated model runs.
