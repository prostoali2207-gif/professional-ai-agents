# Content Architecture v0.4 evaluation-integrity decision

Status: NOT EXECUTABLE — original targeted qualification cycle is retired for release evidence.

Candidate remains frozen and unchanged:

- artifact blob SHA: `5d440e1bf3e20fbd35c6ab276310a904e36cc06d`

## Confirmed defect

The original Content Architecture sealed transport restores and SHA-256-verifies a frozen `grader-key-v0.1.json`, but the restored protocol fixtures do not include a mechanical grader and no evaluator-owned executable external grader contract is supplied to the harness.

The generic harness therefore correctly emits `PENDING_EXTERNAL_GRADER` when no `mechanical_grader` checks exist. The 35 successful candidate executions from run `32635329000` are execution evidence only; they are not scored qualification evidence. H20 is additionally missing because the pinned Gemini runtime returned HTTP 429.

Creating an interpreter for `grader-key-v0.1.json` now from guesses, phrase matching, or a new LLM judge would change grading semantics after candidate execution and would violate evaluation integrity.

## Integrity decision

Do not:

- reinterpret the frozen grader key;
- invent a grader implementation for the old cycle;
- treat the 35 `PENDING_EXTERNAL_GRADER` rows as PASS/FAIL evidence;
- run H20 merely to complete an unscorable cycle;
- modify candidate v0.4 to accommodate this infrastructure defect.

The old run and its 35 successful records remain retained as diagnostic execution evidence only.

## Correct recovery path

A new evaluator-owned qualification cycle may be created for the same still-frozen candidate, provided it is independent of candidate repair and is preregistered before any candidate execution. The new cycle must bind all of the following before execution:

1. candidate identity;
2. hidden fixture corpus identity;
3. executable grader/verifier implementation and version;
4. grader calibration/validation evidence appropriate to the judgment type;
5. thresholds and P0 hard-fail rules;
6. stochastic/repeat policy;
7. provider/runtime eligibility constraints;
8. replayable run-record schema;
9. cost/budget gate and checkpoint/resume policy.

For subjective creative/professional judgment, follow `architect/SKILL.md`: prefer calibrated comparative or multi-judge review over one unvalidated scalar judge. Mechanical checks should cover only mechanically observable invariants.

The executable evidence chain must exist before the first scored candidate call:

`claim -> executable fixture -> observable actions/state -> grader/verifier -> frozen threshold -> run record`

## Fail-closed rule for legacy workflows

The legacy v0.4 Gemini targeted and H20-resume workflows must refuse provider-backed candidate execution unless the restored corpus exposes either:

- at least one executable `mechanical_grader` check for every scored fixture; or
- an explicitly versioned external grader contract plus executable grader implementation whose identity is preregistered and integrity-verified.

Until that requirement is satisfied by a new valid cycle, the Content Architecture v0.4 release status remains `NOT QUALIFIED / NOT EXECUTABLE` rather than PASS or REVISE.
