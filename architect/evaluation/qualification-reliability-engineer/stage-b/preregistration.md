# QRE v0.1 — Stage B calibration preregistration

Status: **PREREGISTERED BEFORE INDEPENDENT AUTHOR OUTPUTS OR CANDIDATE SCORING**  
Issue: #269  
Execution chain: `qre-v01-independent-stage-b-calibration-r1`  
Frozen candidate: `faafd25b554bcff2c22c30f8edbf76a895f05298`  
Freeze record: `ed2e69405209813005ef08b1b4f086e011c3b2c8`  
Stage-A evidence merge: `88eccf02809a0d26a152663496e39839f08ea1d3`

## Purpose

Establish a defensible independent calibration instrument before any scored QRE candidate outcome is visible.

Stage B is evaluation-design work, not candidate scoring. A PASS here means only that the evaluator/rubric can discriminate materially different reliability judgments. It does not qualify the QRE candidate.

## Independence boundary

The candidate-authoring/architecture context that produced v0.1 is **not eligible** to author the fresh calibration cases, reference solutions, or final calibration judgments.

B1 must be authored in a fresh independent evaluator context. Preferred route: one subscription-backed Codex session with repository access. Metered API is not authorized.

The B1 author may read:
- current `AGENTS.md`;
- current `architect/SKILL.md`;
- current methodology files for stop-loss, eval integrity, calibration and resource-cost engineering;
- `architect/evaluation/qualification-reliability-engineer/qualification-plan-v0.1.md`;
- `architect/evaluation/qualification-reliability-engineer/candidate-freeze-v0.1.json` for identity only;
- public profession/competency research under `architect/research/qualification-reliability-engineer/` as construct documentation.

The B1 author must **not** inspect candidate responses, candidate scored outputs, hidden prior profession packs, or tune cases after seeing QRE candidate behavior. To reduce wording contamination, do not use the candidate `SKILL.md` as an authoring source; use the profession construct and qualification plan instead.

## B1 — fresh calibration pack authoring

Create a fresh sealed/private-to-evaluator calibration pack after this preregistration. The public repository may contain only sanitized metadata/contracts until independence-sensitive work is complete.

Minimum calibration mechanisms:
1. deterministic blocker hidden behind pressure to run a paid/live canary;
2. ambiguous non-idempotent create timeout with duplicate-execution risk;
3. safe idempotent retrieval retry contrast;
4. materially non-representative canary that superficially looks convincing;
5. hidden/held-out storage-retention conflict;
6. stale/cross-run evidence falsely implying readiness;
7. same-stage stop-loss reset disguised by provider/issue/branch change;
8. true cross-profession generic blind spot that can satisfy #129 reopen;
9. one-off local/provider defect that must *not* reopen generic platform;
10. overengineering trap where simple deterministic evidence is sufficient;
11. negative control where `GO` is the correct decision;
12. ambiguous provider error where root cause is not established.

Each case must bind:
- facts/observables;
- unknowns and misleading cues;
- decision-relevant variables;
- required professional decision properties;
- unacceptable shortcuts;
- applicable P0 hard-fail triggers;
- mechanical assertions, if any, that can be checked deterministically;
- judgment dimensions requiring professional review.

Do not encode an exact preferred prose answer.

## Required calibration exemplars

Across the calibration set, provide blinded reference exemplars representing at least:
- `UNSAFE_NAIVE` — materially unsafe/invalid, including at least one P0;
- `MECHANICAL_SHALLOW` — catches obvious mechanics but misses material judgment/validity;
- `STAFF_STRONG` — evidence-based, bounded, discriminating, preserves semantics and resources;
- `OVERENGINEERED` — technically cautious but adds unjustified process/tools/tests or blocks a valid run;
- `CORRECT_GO_CONTROL` — correctly allows execution when material blockers are absent.

Reference levels must differ in decision quality, not merely verbosity/style.

## Rubric dimensions to calibrate

At minimum:
1. evidence-path / runtime-contract completeness;
2. failure classification accuracy;
3. deterministic-first evidence routing;
4. retry/idempotency safety;
5. canary representativeness judgment;
6. comparability / measurement-validity boundary;
7. evidence preservation and resume discipline;
8. privacy/retention handling;
9. resource/budget/stop-condition quality;
10. stop-loss and #129 reopen correctness;
11. smallest discriminating experiment quality;
12. sufficiency vs overengineering;
13. readiness verdict correctness;
14. factual uncertainty discipline.

P0 policy remains exactly the ten hard fails preregistered in issue #269. Stage B may operationalize observable indicators but may not weaken, remove or average away a P0.

## Calibration acceptance rule

Before candidate scoring is authorized, the frozen calibration instrument must demonstrate all of the following on reference exemplars/cases:
- every `UNSAFE_NAIVE` P0 exemplar is rejected as release-ineligible;
- `MECHANICAL_SHALLOW` is distinguishable from `STAFF_STRONG` on at least one material judgment dimension rather than style;
- `OVERENGINEERED` does not outscore `STAFF_STRONG` merely for more process/tests/tooling;
- `CORRECT_GO_CONTROL` is not failed for lacking unnecessary defensive work;
- mechanically observable assertions agree with deterministic verifiers;
- difficult judgment cases expose disagreement explicitly instead of hiding it in an average;
- a defensible candidate-scoring threshold/floor can be frozen from the observed calibration separation.

If these conditions cannot be established without changing cases after seeing candidate outputs, Stage B is `NOT_EXECUTABLE` / evaluation-design incomplete.

## Threshold policy

No numeric candidate threshold is invented here. After B1/B2 calibration evidence, and **before first scored candidate output**, the independent evaluator must freeze:
- competency floor(s);
- any aggregate threshold if used;
- P0=0 hard rule;
- mandatory practical-gate rule;
- disagreement/adjudication rule;
- repeated-trial policy where stochastic variance matters;
- early-stop/stop-loss conditions.

A threshold chosen after viewing candidate scores is invalid.

## Resource contract

### B1 authoring
- candidate calls: `0`;
- judge calls: `0`;
- live provider/API calls: `0`;
- metered API calls: `0`;
- independent authoring route: at most `1` subscription-backed evaluator session by default;
- parallel model runs: prohibited;
- technical repair consumed at start: `false`.

### B2 calibration review
Before B2 begins, record its exact independent reviewer/judge route and maximum call/session budget. Prefer deterministic checks plus one sufficient independent subscription-backed professional review route. Do not ensemble by default.

## Stop-loss

Stage-B execution-chain rule:
`technical failure -> classify -> at most one bounded repair when authorized -> exact regression -> one eligible retry -> STOP on another technical defect`.

A new evaluator session, branch, provider or issue does not reset the same B-stage failure budget.

## Authorization

This preregistration authorizes:
- deterministic validation of the Stage-B contracts/harness;
- one independent B1 calibration-pack authoring pass under the resource/independence rules above.

It does **not** authorize candidate scoring, Stage C, Stage D, metered API calls, live provider canaries, or candidate changes.
