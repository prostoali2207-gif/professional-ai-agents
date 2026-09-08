# QRE cycle 2 — B2a authorization

Status: **AUTHORIZED**

Issue: #293  
Design-gate PR: #295  
Design-gate merge: `de9910862f97211b1930b3188bbb0f51b060bce9`  
Design-gate workflow run: `34189314101`

Frozen candidate remains:
- candidate merge: `faafd25b554bcff2c22c30f8edbf76a895f05298`;
- freeze record: `ed2e69405209813005ef08b1b4f086e011c3b2c8`.

Package identities:
- accepted source B1 pack SHA-256: `0f3742de73dce04517ed93bb81d8114bb3c0b51a0b855f45b353a91f85af1103`;
- blind bundle SHA-256: `b5773921fdcdb711bc7ea9a72bf1099055025445132c8b4f1a24b0e0eb628722`;
- judgment template SHA-256: `149db0494a7ad9c890ce0e31085fbc2eb7d89078b9026c9842344357a636144b`.

Design-gate evidence:
- deterministic rebuild of checked-in bundle/template: PASS;
- untouched template validation: PASS;
- fail-closed mutation regressions: PASS;
- no provider SDK/credential code path: PASS;
- all six PR workflows: PASS;
- candidate/model/judge/provider/API calls: 0.

Execution chain:
`qre-v01-cycle2-b2a-blind-review-r1`.

B2a resource contract:
- one fresh subscription-backed reviewer context;
- no candidate execution;
- no external/API judge calls;
- no live-provider calls;
- no metered API;
- no parallel/delegated model runs;
- no GitHub API/tool calls required for evidence generation;
- use local file I/O only;
- technical repair consumed at start: false;
- at most one bounded technical repair only for a deterministic package/runtime defect with exact regression; one eligible retry; another technical defect => STOP.

B2a is authorized to execute exactly the task in `b2a-reviewer-task.md`.

B2b, candidate scoring, Stage C and Stage D remain unauthorized until a complete 48/48 B2a judgment artifact passes validation and a canonical checkpoint seal is produced.
