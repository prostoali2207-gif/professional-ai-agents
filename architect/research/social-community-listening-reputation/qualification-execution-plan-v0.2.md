# Social Community, Listening & Reputation Management Core
## Qualification execution plan v0.2

Status: canonical sequencing amendment for qualification of candidate `social-community-listening-reputation@0.1.0`.

This document supersedes only the qualification-sequencing language in `evaluation-plan-v0.1.md` and `cg-06-heldout-evaluation-protocol-v0.1.md` where those documents imply either (a) that a non-executable Professional Core artifact can itself demonstrate runtime behavior, or (b) that the decisive held-out fixture must already exist before the Professional Core artifact is authored. All unchanged construct, severity, competency, grader, evidence and anti-gaming requirements remain in force.

## 1. Qualification subject

The Professional Core artifact and an executable implementation are different evidence subjects.

The core artifact contains profession knowledge, judgment policies, boundaries, evidence provenance, context separation, authority requirements and runtime contracts. Static/schema/content review can evaluate those properties directly.

Behavioral claims involving tool trajectories, persistent state, approvals, side effects, degraded capabilities, retries, cross-turn supersession or recovery cannot be established by prose files alone. They require an executable **qualification bundle** tied to the exact core artifact digest.

Therefore:

`core candidate -> artifact freeze -> qualification bundle freeze -> independent held-out fixture -> executable runs -> qualification record -> production/applied skill`

A qualification bundle is test infrastructure, not a production release and not permission to use the candidate operationally.

## 2. Freeze boundary

Before any decisive held-out fixture is authored or revealed:

1. freeze the Professional Core content digest;
2. freeze the qualification bundle digest and its loader/runtime contract;
3. record candidate commit SHA, core digest, bundle digest, model/runtime profile and public grader/threshold versions;
4. prohibit behavior-relevant changes to the frozen core or bundle until the scored run completes.

A documentation-only change outside the scored subject may occur only if it cannot change candidate behavior or grader expectations and is recorded.

Any behavior-relevant repair after observing a held-out result invalidates that fixture as the sole release holdout for the repaired candidate.

## 3. Held-out timing and independence

Two valid anti-contamination patterns are allowed:

### Pattern A — precommitted holdout

An independent evaluator authors and seals the fixture/grader before candidate implementation and publishes only immutable commitments.

### Pattern B — post-freeze holdout

The candidate core and qualification bundle are frozen first. Only then does an independent evaluator author and seal a fresh fixture/grader without allowing candidate authors to inspect its decisive details before scoring.

Pattern B is the required path for `social-community-listening-reputation@0.1.0`, because no valid CG-06 commitment existed before candidate authoring. This is not retroactive preregistration: the holdout must be newly authored after the freeze and the candidate must remain unchanged until scoring.

The evaluator must not have written or repaired the scored qualification bundle. The evaluator records a contamination declaration and retains hidden fixture/grader artifacts outside the candidate-readable repository/runtime surface.

## 4. Qualification bundle contract

The test-only bundle must:

- load the exact frozen core artifact identified by digest;
- load only declared public schemas/contracts and a scoped live-context packet;
- expose trusted instructions separately from untrusted comments, DMs, retrieved posts, links, screenshots and tool output;
- interact only through controlled state, approval, social-platform/listening and notification adapters supplied by the harness;
- emit schema-valid observable outputs and action proposals/calls;
- never gain authority merely because a tool capability exists;
- capture model/runtime/tool versions, loaded artifact digest and capability profile;
- support full and degraded capability profiles without silent substitution.

The bundle must not contain fixture-specific wording, hidden grader anchors, gold actions or attack strings.

## 5. What can be qualified

A passing record may support only claims demonstrated by the frozen bundle in the recorded environment. It does not prove that every future production skill derived from the core behaves identically.

A production/applied skill must therefore:

1. reference the qualified core artifact and qualification record;
2. document implementation deltas from the qualification bundle;
3. rerun affected P0/P1 regression for behavior-relevant deltas;
4. undergo target-specific compatibility/composition evaluation.

Unchanged profession-level invariants may reuse prior evidence only when transfer assumptions hold.

## 6. CG-06 release rule for this candidate

For `social-community-listening-reputation@0.1.0`, CG-06 can produce release evidence only when all are true:

- the exact core artifact digest is frozen;
- an executable qualification bundle is frozen and separately digested;
- an independent evaluator authors a new sealed CG-06 fixture after that freeze;
- the evaluator does not expose decisive fixture/grader details to the candidate author before scoring;
- full-profile and degraded-profile runs capture inspectable state, tool/approval traces and side-effect ledger;
- zero P0 failures and zero P1 failures occur under the preregistered criteria;
- critical stochastic profiles pass at least three isolated trials;
- judgment-heavy criteria receive independent calibrated review;
- any repair after a failure is followed by a fresh held-out variant and affected-family regression.

Without these conditions the result remains `candidate / NOT QUALIFIED`; schema validity or narrative review cannot substitute.

## 7. Production gate

No production Skill for the three target businesses is admitted merely because this document exists or because static checks pass.

The next executable steps are:

1. build and freeze the qualification bundle;
2. have an independent reviewer create/seal the fresh CG-06 fixture and grader outside the repository;
3. execute the public + held-out suites through a harness that satisfies `architect/evaluation/behavioral-validation-harness.md`;
4. record the exact evidence in a qualification record;
5. only on PASS, derive and regression-test the production/applied skills.
