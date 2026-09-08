# QRE v0.1 — qualification cycle 2 packaged calibration preregistration

Issue: #293  
Status: **DESIGN GATE — ZERO PROVIDER/MODEL CALLS**  
Frozen candidate: `faafd25b554bcff2c22c30f8edbf76a895f05298`  
Freeze record: `ed2e69405209813005ef08b1b4f086e011c3b2c8`

## Prior cycle boundary

Issue #269 is terminal `NOT_EXECUTABLE / STOP`. Its Stage-B chain `qre-v01-independent-stage-b-calibration-r1` is not reopened and its repair budget is not reset.

Cycle 2 is a materially different evaluator architecture. It removes issue-comment discovery, reviewer-authored presentation construction, same-context unblind, and reviewer dependence on GitHub API calls.

## Reused evidence

Permitted reuse:
- exact Stage-A deterministic evidence from #269 after identity compatibility checks;
- independently authored B1 calibration pack from PR #280 **only as calibration material**.

Prohibited reuse:
- B1 pack as Stage-C candidate evidence;
- any old B2 attempt as calibration judgment evidence;
- any candidate output from the prior cycle.

Accepted source calibration pack SHA-256:
`0f3742de73dce04517ed93bb81d8114bb3c0b51a0b855f45b353a91f85af1103`.

Generated blind bundle SHA-256:
`b5773921fdcdb711bc7ea9a72bf1099055025445132c8b4f1a24b0e0eb628722`.

## Evaluator architecture

`deterministic packager -> blind-only bundle -> B2a blind reviewer -> validated/sealed judgment artifact -> B2b fresh unblind adjudicator -> threshold freeze`

### B2a blind reviewer

Execution chain: `qre-v01-cycle2-b2a-blind-review-r1`.

The reviewer receives only:
- `blind-bundle-v0.2.json`;
- `blind-judgment-template-v0.2.json`;
- `b2a-reviewer-task.md`;
- `validate_blind_judgments.py`;
- `seal_blind_checkpoint.py`.

The reviewer must not read issue comments, the old calibration reference/key, hidden author fields, QRE candidate outputs, or candidate behavior files.

The reviewer uses local file I/O only for the review. No GitHub API/tool call is part of B2a evidence generation.

Budget:
- fresh subscription-backed reviewer contexts: max 1;
- candidate calls: 0;
- external/API judge calls: 0;
- live-provider calls: 0;
- metered API calls: 0;
- parallel/delegated model runs: 0;
- technical repair at chain start: false;
- one bounded technical repair only if a deterministic packaging/runtime defect is encountered and exact regression is possible; then one eligible retry; another technical defect => STOP.

Output:
- complete `blind-judgments-v0.2.json` with 48/48 unique reference IDs;
- validator PASS;
- canonical checkpoint SHA-256 from `seal_blind_checkpoint.py`.

The checkpoint is considered frozen by the reviewer final response containing both the complete JSON artifact and canonical seal hash. B2a never sees the author key, so it cannot post-unblind retune its judgments.

### B2b unblind adjudicator

Execution chain: `qre-v01-cycle2-b2b-unblind-adjudication-r1`.

Use a **different fresh subscription-backed context**.

Before reading the author key, B2b must:
1. receive the complete B2a judgment JSON and reported canonical seal hash;
2. run the validator against the packaged blind bundle;
3. recompute the canonical hash and prove it matches the B2a seal.

Only then may B2b read:
- `stage-b/calibration-reference-v0.1.md`;
- `compare_calibration.py`;
- public construct/rubric documentation needed for adjudication.

Budget:
- fresh adjudicator contexts: max 1;
- candidate calls: 0;
- metered API calls: 0;
- parallel/delegated model runs: 0;
- technical repair at chain start: false, separately tracked from B2a.

B2b must freeze before any candidate output:
- candidate competency floor(s);
- aggregate threshold if used;
- P0 max = 0;
- practical P1-P5 mandatory rule;
- disagreement/adjudication rule;
- repeat/stochastic policy;
- Stage-C resource/stop conditions.

Final B2b verdict:
`B2_CALIBRATED_PASS | B2_CALIBRATION_FAIL | NOT_EXECUTABLE`.

## Design-gate acceptance

Before B2a is authorized:
- source pack raw SHA-256 matches accepted B1 pack;
- checked-in blind bundle exactly reproduces deterministic build;
- forbidden author fields are absent recursively;
- exactly 12 cases / 48 unique references are present;
- no author quality labels appear in the blind bundle;
- template is bound to exact blind-bundle SHA-256;
- pure-stdlib validator rejects missing, duplicate, unknown IDs, illegal labels, illegal P0s, wrong bundle identity and contaminated reviewer flags;
- seal script validates before hashing;
- no provider SDK/credential path exists in cycle-2 scripts;
- CI is zero-provider.

No B2a/B2b/candidate execution is authorized until this design gate is merged and recorded.
