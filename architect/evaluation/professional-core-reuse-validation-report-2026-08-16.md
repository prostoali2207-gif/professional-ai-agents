# Professional Core Reuse Validation Report — 2026-08-16

Status: **PASS with repeated-trial reliability evidence** for the Professional Core Reuse integration claim defined by `professional-core-reuse-gate.md`.

## Final qualifying sequence

The release claim is based on the repaired behavior plus an explicit reliability gate after stochastic omissions were observed.

### Reliability-sensitive regression

- Candidate SHA: `d8c7a72423fd63a36e09e0c36ad227057a457d4c`
- GitHub Actions run: `31948837687`
- Cases: PCR-S2 and PCR-S6
- Trials: 3 independent trials per case
- Result: PCR-S2 **3/3 PASS**; PCR-S6 **3/3 PASS**
- Planned/executed model calls: 6/6
- Application retries: 0
- Model/runtime: Gemini Interactions, `gemini-3.5-flash-lite`, medium thinking
- Sealed evidence artifact ID: `9264060981`
- Artifact digest: `sha256:7121724ea5b05cf7ab8c75242fd11f4bd6c31a3db3f47fb40c8af1fc33ed4ce9`

### Complete release gate

- Candidate SHA: `f18751a69813f53414d2b9e2e29d707833ed6c54`
- Behavior-relevant Architect files are unchanged from the reliability-sensitive candidate; this commit changes only the release workflow from targeted repeated cases back to the complete frozen suite.
- GitHub Actions run: `31948877370`
- Frozen cases: PCR-S1 through PCR-S6
- Result: **6/6 PASS**
- Planned/executed model calls: 6/6
- Application retries: 0
- Model/runtime: Gemini Interactions, `gemini-3.5-flash-lite`, medium thinking
- Sealed evidence artifact ID: `9264071466`
- Artifact digest: `sha256:3c2ae55a87a9d147ece84c84b77656d015340330e95e21994475420452e3aac0`

This sequence satisfies the strengthened release rule:

`deterministic preflight -> observed unstable cases 3/3 each -> complete frozen suite -> PASS`.

## Why the earlier single-run PASS was not enough

An earlier candidate SHA `cd3f9ed36fb0fca97593585822931c6cc2c1e6b4` passed the complete suite 6/6 in run `31948575248`. A later documentation-only head, with no behavior-relevant Architect changes, then failed PCR-S2 because `delta_research` was omitted while the other required ADAPT behaviors were present.

That recurrence falsified the assumption that one successful stochastic sample was sufficient evidence of reliability. The earlier 6/6 remains valid evidence for that individual run, but it is no longer used alone as the release justification.

The gate was therefore strengthened rather than repeatedly rerunning until green. PCR-S2 and PCR-S6 became reliability-sensitive fixtures because both had shown stochastic omission during development.

## What the gate proves

Within the tested runtime and fixtures, Agent Architect demonstrated the required behaviors for:

- rejecting role-title similarity as sufficient reuse evidence;
- preserving stable professional competence while refreshing stale volatile context and performing delta research;
- separating project-specific state from reusable professional cores and blocking unsafe library admission;
- refusing automatic inheritance of historical PASS after behavior-relevant runtime/tool/authority changes;
- extending a compatible proven core with delta research, retained qualifying evidence, and composition evaluation;
- rejecting cheap shallow role prompts that lack provenance and meaningful evaluation evidence.

It does not prove that every future professional core is valid or that composed applied agents inherit readiness. Each candidate still requires its own compatibility, freshness, runtime/authority, composition, and affected/new evaluation decisions.

## Failure and repair history

Executable validation exposed both real policy defects and grader defects:

- initial full run: 4/6; missing explicit regression obligation for changed runtime/tool/authority and incomplete EXTEND transfer obligations;
- second full run: 4/6; ADAPT could refresh volatile claims without explicit delta research; one duplicate grader construct was removed;
- targeted PCR-S2/PCR-S4 regression: 2/2 PASS after policy repair;
- later full run: 5/6; PCR-S6 revealed instability around explicit evaluation-evidence rejection;
- PCR-S6 passed twice on one repaired SHA;
- another full run revealed PCR-S3 grader contradicted the preregistered textual gate (`reject OR refactor`); structured expectation was corrected to allow ADAPT or REJECT while retaining project-context separation and blocked library admission;
- complete suite then passed 6/6, but a later behavior-identical run exposed recurrent PCR-S2 stochastic omission;
- release standard was upgraded to repeated-trial reliability for observed unstable fixtures;
- final reliability-sensitive gate passed S2 3/3 and S6 3/3, followed by the complete 6/6 release gate.

No fixture was weakened to excuse a real behavioral failure. Grader changes were limited to construct mismatches with the pre-existing textual gate.

## Release boundary

The qualifying behavior is the Professional Core Reuse architecture represented by the behavior-relevant contents at `f18751a69813f53414d2b9e2e29d707833ed6c54`, supported by the immediately preceding repeated-trial evidence at `d8c7a72423fd63a36e09e0c36ad227057a457d4c`.

Future behavior-relevant changes to the router, reuse methodology, semantic fixture semantics, grader, or runner require impact analysis and appropriate targeted/full reliability regression. Documentation-only changes do not inherit a new behavioral claim merely by changing the commit SHA.

After qualification, automatic model-consuming PCR execution is disabled; future PCR release runs must be deliberately invoked so documentation changes do not consume API quota.
