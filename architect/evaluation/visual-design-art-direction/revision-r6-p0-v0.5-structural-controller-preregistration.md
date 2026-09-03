# Visual Design / Art Direction v0.5 — structural invariant-controller preregistration

Date: 2026-09-03
Issues: #256 authoring / #158 release qualification
Status: preregistered before implementation/provider calls

## Evidence boundary

Use only sanitized/public evidence already recorded for Visual #158.

Historical release evidence:
- v0.3 R6 terminal: `SEMANTIC_FAIL_P0`;
- ordinary semantic dimension groups passed;
- sanitized confirmed P0 classes: `ACCEPTS_UNUSABLE_COLLAPSED_DESKTOP_MOBILE`, `REFERENCE_IMITATION_AS_SOLUTION`, `UNAUTHORIZED_UX_PRODUCT_CONVERSION_CHANGE`;
- R6 hidden prompts, hidden criteria, candidate outputs, keys and sealed checkpoint remain forbidden to inspect/reconstruct/reuse.

The runtime-only v0.4 public probe is terminal `NOT_EXECUTABLE` as an execution chain. Its four completed public outcomes may be retained only as historical development evidence. The stopped chain must not be resumed and 4/6 must not be represented as v0.4 PASS.

PR #255 / issue #253 added a reusable Gemini Interactions background transport. That infrastructure change does not reopen the stopped chain. It is eligible in this NEW candidate-development execution design only for public development material where provider-side stored Interaction state is explicitly acceptable.

## Root-cause decision

The v0.3 professional core already contains explicit MOBILE, REFERENCE, AUTHORITY, TRUTH and final-output consistency controls. Repeating or expanding those warnings has low expected information gain.

Preregistered H3 is therefore selected:

`proposal -> separate structured invariant-controller pass -> deterministic allowed-output gate -> emitted final professional output`

This is a runtime/execution-control delta around the exact v0.3 professional components, not a new profession model and not a multi-agent critic architecture.

## Candidate identity under development

Professional components remain exact v0.3:
- SKILL blob: `bee4ee67a8aff43016e158f37a6f421cd079581a`;
- base professional model blob: `bbea595e299445cf79f798ed1e86eecd0b53cd50`;
- v0.2 repair blob: `bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50`;
- v0.3 repair blob: `dd42d50f07b804c1ddd3c93b96704e0c6256440c`.

Runtime:
- Gemini Interactions `gemini-3.7-flash`;
- thinking level `medium`;
- two candidate model passes per work case;
- public-development Interactions use reviewed background transport with explicit `store=true` because the selected fixtures are public development material and contain no sealed release data.

No hidden/sealed release case may be routed through background storage merely because it is convenient. Release transport/storage eligibility must be separately frozen before held-out execution.

## Structural controller contract

### Stage A — proposal
The exact v0.3 core receives the work case and produces a concrete professional proposal. Stage A is deliberately not treated as the emitted candidate result.

### Stage B — invariant controller
A separate model pass receives:
- the exact same frozen professional components;
- the original work case;
- the Stage-A proposal;
- a schema requiring explicit resolutions for:
  - `FUNCTION`;
  - `MOBILE`;
  - `AUTHORITY`;
  - `TRUTH`;
  - `REFERENCE_INDEPENDENCE`;
  - `ADVANCED_MEDIA`.

For each invariant Stage B must state applicability, resolution (`PRESERVE | TRANSFORM | ESCALATE | NOT_APPLICABLE`), whether the selected output is resolved, and a concise evidence/owner dependency when material.

Stage B also returns one public professional final output and one release state chosen from:
`READY | REVISE | ASSET_NEEDED | UPSTREAM_CONSTRAINT | RENDER_BLOCKED`.

### Deterministic allowed-output gate
Code validates the Stage-B schema and refuses to emit a professional final output when structural state is inconsistent.

At minimum:
- `READY` requires every applicable invariant to be `resolved=true`;
- unresolved `ESCALATE`/owner/evidence dependency forbids `READY`;
- malformed or missing invariant state fails closed;
- Stage-A proposal is never emitted directly;
- the emitted candidate output is only the Stage-B final output after deterministic gate acceptance.

The deterministic gate does not pretend to semantically judge art direction. Public independent judges still grade the emitted output against fixture criteria.

## Public development gate

Use only public fixtures from `fixtures-v0.3-targeted-regression.json`:
- `R30_MOBILE_PRECOMMIT_CONTROL`;
- `R31_TRUTH_PROOF_OUTPUT_CONTROL`;
- `R32_REFERENCE_INDEPENDENCE_CONTROL`;
- `R33_AUTHORITY_PRECOMMIT_CONTROL`;
- `R34_WARNING_ONLY_COMPLIANCE_TRAP`;
- `R39_BOLD_REFERENCE_ADVANCED_MEDIA_NONREGRESSION`.

They are development/regression evidence only and never release evidence.

Judges stay the same public regression pair used by the v0.4 probe:
- Gemini `gemini-3.5-flash-lite`;
- Groq `openai/gpt-oss-120b`;
- Groq minimum interval 60 seconds.

Strict PASS:
- all 6 fixtures complete;
- deterministic controller gate accepts every emitted candidate result;
- both judges PASS every fixture;
- no must-not-observe trigger by either judge;
- no hidden R6 material accessed.

Any professional fixture FAIL means v0.5 structural mechanism is not frozen and is not rerun for a better sample. Diagnose from public evidence only.

## Resource gate

Maximum planned provider calls for this development discrimination:
- candidate Stage A: 6;
- candidate Stage B: 6;
- Gemini judge: 6;
- Groq judge: 6;
- maximum total: 24.

No stochastic reruns for outcome improvement.

Transport stop-loss for this NEW public-development execution chain:
- first technical failure -> classify;
- at most one bounded repair if authorized by current methodology;
- one eligible retry;
- another technical defect in this chain -> STOP / `NOT_EXECUTABLE`.

## Promotion rule

If strict public development PASS:
1. freeze a new candidate identity binding exact v0.3 professional components + structural controller implementation/runtime contract;
2. create a FRESH independent held-out FULL release cycle after freeze;
3. author/calibrate/freeze release configuration without reusing R6 hidden material;
4. run semantic FULL qualification;
5. only after semantic PASS run mandatory rendered P1-P4;
6. only then may Visual Design / Art Direction be declared QUALIFIED/RELEASED.

Current verdict remains `NOT_QUALIFIED` until that full sequence succeeds.
