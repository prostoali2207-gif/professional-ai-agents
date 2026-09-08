# Stage B0 execution record — Video Capture & Camera Operations #294 — 2026-09-08

Status: **B0 = REVISE (professional fail)** / B1 NOT EXECUTED / candidate NOT mutated

Branch: `research/video-capture-camera-operations-294`
Execution chain: candidate v0.1 frozen + Stage B development semantic + Claude Code subscription transport
Result artifact: `stage-b0-result-2026-09-08.json`

## 1. Transport repair consumed before valid evidence (LOCAL_EXECUTION_FAIL)

The first B0 attempt produced no professional evidence.

- classification: `LOCAL_EXECUTION_FAIL`
- candidate calls: 0
- judge calls: 0
- retries: 0
- provider/paid calls: 0

Defect: `claude_candidate_adapter_v0.1.py` and `claude_judge_adapter_v0.1.py` invoked the child
Claude Code process with `--bare`. In Claude Code >= 2.1.x `--bare` restricts Anthropic auth to
`ANTHROPIC_API_KEY` / `apiKeyHelper` and never reads OAuth. That is mutually exclusive with this
route's preregistered subscription-only, no-metered-key contract, so every child invocation
terminated with `Authentication error` before any model call.

Secondary defects in the same code path:
- the adapter preflight reported `PASS` because it probed only `claude --version` and
  `claude auth status`, never the actual invocation flag set;
- on child failure the adapter surfaced only `stderr`, but the CLI prints the auth error on
  `stdout`, so the runner reported an empty, undiagnosable `LOCAL_EXECUTION_FAIL`.

Bounded repair applied under `architect/methodology/qualification-stop-loss.md`
(one bounded local repair, then one eligible retry). Transport only:

- `--bare` replaced by `--safe-mode`, which supplies the isolation `--bare` was selected for
  (CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands/agents disabled) while
  leaving subscription auth intact;
- `--strict-mcp-config` and `--permission-prompts none` added;
- preflight now deterministically rejects any contract-violating flag set and asserts
  `loggedIn` + non-API-key `authMethod` before any model call;
- child failures now surface `stdout` when `stderr` is empty.

Isolation was verified empirically before the retry. A probe under the repaired flag set reported
`{"claude_md_loaded": false, "skills_count": 0, "mcp_server_count": 0, "tools_available": [],
"repo_files_visible": false}`, satisfying the preregistered nested-isolation requirement.

Regression reproducing the exact defect (0 provider calls):
`test_claude_transport_contract_v0.1.py`.

Frozen candidate blobs re-verified unchanged before the retry:
- `professional-model-candidate-v0.1.md` -> `65ccc214418d269a27042dda2b83adf53bb59c5b`
- `candidate/SKILL.md` -> `8b64d280b8b1fe01969bf804212ab0e6ca37a7a8`
- `qualification-plan-v0.1.md` -> `d2bc765a7b439d271afc75e83fc0ee78d1b59d2a`

The bounded technical repair for this execution chain is now **consumed**. Another non-professional
technical defect in this chain triggers the stop-loss repair-chain stop rule.

## 2. B0 professional result

- classification: `PROFESSIONAL_FAIL`
- phase status: `REVISE`
- candidate model: `sonnet` (subscription)
- development judge: `opus` (subscription, independent of candidate authoring)
- candidate calls: 1
- judge calls: 1
- retries: 0
- paid/metered API calls: 0
- fixtures executed: 1 of 4 (bounded runner stops on first non-PASS)

Failing fixture: `DEV-P0-01-device-capability` (severity P0, competency DV-01)
Judge decision: `P1_FAIL` — no P0 hard-fail triggered.

### What the candidate got right

Both DV-01 hard-fail conditions were avoided:
- it did not invent or prescribe ProRes Log or 4K60;
- it did not base any plan on an unsupported device capability;
- it marked the requested mode UNVERIFIED against the supplied Samsung packet and correctly cited
  the documented UHD 4K/30fps ceiling.

Rubric R4 (evidence/device integrity) passes.

### The specific failure

Expected observable failed:
> "Still provides a feasible capture route instead of blanket refusal."

The supplied evidence already established a verified usable mode (4K30) sufficient to execute the
approved smooth vertical exterior reveal. Instead of substituting the verified mode and proceeding,
the candidate:
- declared the fallback spec `MISSING—BLOCKING`;
- returned `STATE: NEEDS_INPUT`;
- left `CAPTURE PLAN` "Not finalized";
- emitted operator instructions containing no capture route — only a directive to go read menu
  options and report back.

This is a functional stall on information the fixture already supplied. Rubric R3 (operator
executability) fails: no concrete physical instruction, no movement path, no exposure or
stabilization guidance was delivered.

### Responsible capability

Primary: **DV-01 Device capability routing.**
The candidate executes the refusal half of DV-01 correctly but not the substitution half —
"uses verified device options" is not performed when the requested capability is unsupported.

Consequential: **OP-01 Non-professional operator coaching** — the stall suppressed the executable
instruction set that OP-01 owes the human operator.

### Responsible candidate layer (recorded, not repaired)

`professional-model-candidate-v0.1.md`:
- §1 sorts unresolved items into a `MISSING/BLOCKING` bucket;
- §13 defines `NEEDS_INPUT` as "a decision-critical shot intent, device/location constraint or
  evidence is missing".

Neither layer states that an *unsupported requested capability* whose *verified alternative is
already supplied* is not missing evidence, and that the correct completion state is
`READY_TO_CAPTURE` on the verified mode with the unsupported request flagged. The frozen model
therefore permits — and the candidate chose — escalation over delivery.

This is a candidate design gap, not a fixture, rubric, judge or transport defect. The fixture's
third observable is explicit, and the judge applied it correctly.

## 3. Bounded-execution consequences

- B1 **not executed**. The preregistered gate runs B1 only on B0 PASS.
- The frozen candidate is **not mutated**. Any repair of the §1/§13 escalation-vs-delivery rule is
  behavior-relevant and opens a new candidate cycle with a new freeze record, per the mutation rule
  in `HANDOFF-2026-09-08.md`.
- Fixtures `DEV-P0-02` through `DEV-P0-04` remain unexecuted, so P0 coverage is incomplete: this
  record establishes one failure, not the full P0 profile.

## 4. Release claim

Unchanged and explicitly not advanced by this run.

`CANDIDATE / DEVELOPMENT_B0_REVISE`.

Development fixtures cannot qualify this profession. Even a full B0+B1 PASS would still require
fresh independent held-out evaluation and then the mandatory practical gate on real ordinary
used-car footage before any QUALIFIED claim.
