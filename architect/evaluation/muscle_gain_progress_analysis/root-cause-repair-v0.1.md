# Muscle Gain Progress Analysis — root-cause repair record v0.1

## Failure 1 — LOCAL_EXECUTION_FAIL
Initial development runner loaded the procedure with `importlib` without registering the module in `sys.modules`; import machinery failed before valid professional evidence.

Repair: register the module before execution. One bounded runner repair; no professional threshold changed.

## Failure 2 — PROFESSIONAL_FAIL
First valid professional run exposed a body-composition hydration/glycogen case gap. The written knowledge model described the confound, but the executable decision procedure did not route it to insufficient-data / measurement-repair behavior.

Root cause: knowledge -> procedure compilation gap.

Repair:
- explicit `hydration_or_glycogen_confound` branch;
- supplied method-resolution/MDC branch;
- neighboring regression case so the repair covers the failure family rather than one phrase.

## Failure 3 — EVALUATOR_CONSTRUCT_FAIL
A static check required one exact phrase despite the SKILL containing behavior-equivalent wording.

Repair: static checks target semantic anchors/invariants rather than arbitrary spelling.

## Failure 4 — PROFESSIONAL_FAIL discovered on exact committed candidate
The exact candidate initially returned `HOLD` when performance improved but body-mass rate was above an explicitly supplied target. The generic performance-progress branch executed before the target-rate branch, so a decision-relevant constraint was ignored.

Root cause: decision-ordering conflict between a generic positive performance signal and an explicit user/program target.

Repair:
- evaluate explicit target-rate deviations before the generic performance-only branch;
- preserve the valid progress claim when performance is improving;
- still return `CHANGE_ONE_VARIABLE` because the observed rate is above the explicit target;
- update the fixture expectation from `NO_MATERIAL_CHANGE` to `PROGRESS`, because the original verdict expectation incorrectly discarded the valid performance signal.

No qualification threshold, hard fail, profession scope, held-out independence requirement or trust-tier requirement was weakened.
