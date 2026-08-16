# Professional Core Reuse Validation Report — 2026-08-16

Status: **PASS** for the Professional Core Reuse integration claim defined by `professional-core-reuse-gate.md`.

## Qualifying candidate

- Candidate SHA: `cd3f9ed36fb0fca97593585822931c6cc2c1e6b4`
- GitHub Actions run: `31948575248`
- Workflow: `Agent Architect Professional Core Reuse Gate`
- Runtime/model: Gemini Interactions, `gemini-3.5-flash-lite`, medium thinking
- Frozen semantic cases: PCR-S1 through PCR-S6
- Planned model calls: 6
- Executed model calls: 6
- Application retries: 0
- Result: **6/6 PASS**
- Sealed evidence artifact ID: `9263994621`
- Artifact digest: `sha256:f106a591bc30e0875b4cb472fa6bfe3644e9b4259f843a3e1ce49f97bb909ff5`

The same candidate SHA also completed the `Agent Architect Research + RCE Gate` and `Agent Architect RCE Mechanical Gate` with success.

## What the gate proves

The candidate demonstrated the tested behaviors for:

- rejecting role-title similarity as sufficient reuse evidence;
- preserving stable professional competence while refreshing stale volatile context;
- separating project-specific state from reusable professional cores and blocking unsafe library admission;
- refusing automatic inheritance of historical PASS after behavior-relevant runtime/tool/authority changes;
- extending a compatible proven core with delta research, retained qualifying evidence, and composition evaluation;
- rejecting cheap shallow role prompts that lack provenance and meaningful evaluation evidence.

This PASS does not prove that every future professional core is valid or that every composed applied agent inherits readiness. Each candidate still requires compatibility, freshness, runtime/authority, and affected/new evaluation decisions as specified by the methodology.

## Failure and repair history

The release was not declared from the first successful-looking narrative. Earlier executable runs exposed real and evaluation-layer defects.

### Initial full run

The first six-case run passed 4/6. It exposed two real transfer-policy gaps: changed runtime/tool/authority scope did not reliably produce an explicit affected/new regression obligation, and EXTEND did not reliably preserve qualifying evidence for unchanged invariants while separately evaluating new composition interactions.

The methodology was repaired at the responsible layer rather than weakening those requirements.

### Second full run

The next full run again passed 4/6. PCR-S2 exposed a real remaining ADAPT defect: volatile refresh could be selected without explicit delta research. That policy was repaired.

PCR-S4 also revealed a grader construct duplication: `composition_eval` and `evaluate_new_interactions` represented the same required construct. The duplicate observable was removed instead of demanding two synonymous flags.

### Affected regression

PCR-S2 and PCR-S4 then passed together on candidate SHA `ac7b57795b2215330693689bcf17ad4e6fca4577`: 2/2 PASS, zero application retries. Evidence artifact ID `9263938015`, digest `sha256:51697ba422d71c8cbfb568752a863e8682f9bf356a463f1f11d08714229f0734`.

### S6 reliability defect

A later full run passed 5/6 and exposed instability in PCR-S6: the candidate correctly rejected a cheap unevidenced prompt but did not always make the missing meaningful evaluation evidence explicit. The methodology was strengthened so missing evaluation evidence for material professional claims is a hard reuse/library-admission signal, not an optional documentation detail.

PCR-S6 then passed twice on the same repaired candidate through the targeted reliability workflow before returning to the full suite.

### S3 grader correction

A subsequent full run passed 5/6 because PCR-S3 chose `ADAPT` while also producing both required safety behaviors: `separate_project_context` and `block_library_admission`. The preregistered textual gate had always required `reject OR refactor those facts into organization/project context before library admission`, while the structured grader incorrectly allowed only `REJECT` despite the fixture explicitly stating that the candidate boundary was recoverable.

The structured expectation was corrected to allow `ADAPT | REJECT` while retaining the same hard requirements: no REUSE, project-context separation, and blocked admission until refactoring. This was a construct-validity correction consistent with the pre-existing gate, not a relaxation after failure.

## Final release result

After the policy repairs and grader construct corrections, the complete PCR-S1–S6 suite ran on one exact candidate SHA and passed 6/6 with zero application retries. No earlier partial run is used as the release claim.

## Release boundary

This report qualifies the Professional Core Reuse behavior represented by candidate SHA `cd3f9ed36fb0fca97593585822931c6cc2c1e6b4` and the frozen gate used in run `31948575248`.

Documentation-only commits after that SHA may record this result without inheriting a new behavioral qualification. Any behavior-relevant change to the router, reuse methodology, semantic fixtures/grader semantics, or runner requires impact analysis and appropriate affected/full regression before the PASS claim is extended to that new behavior.
