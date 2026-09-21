# Muscle Gain Progress Analysis — root-cause repair record v0.1

## Failure 1 — LOCAL_EXECUTION_FAIL
Initial development runner loaded the procedure with `importlib` without registering the module in `sys.modules`; dataclass/import machinery failed before valid professional evidence.

Repair: register the module before execution. One bounded runner repair; no professional threshold changed.

## Failure 2 — PROFESSIONAL_FAIL
First valid professional run: 13/14. The body-composition hydration/glycogen case failed. The written knowledge model correctly described the confound, but the executable decision procedure did not route it to an insufficient-data/measurement-repair state.

Root cause: knowledge -> procedure compilation gap.

Repair:
- add explicit `hydration_or_glycogen_confound` branch;
- add supplied method-resolution/MDC branch;
- add neighboring regression case so the repair covers the failure family rather than one phrase.

Post-repair: practical suite passed.

## Failure 3 — EVALUATOR_CONSTRUCT_FAIL
A static check required one exact phrase despite the SKILL containing behavior-equivalent wording. This was a brittle evaluator-string issue, not absent competence.

Repair: static checks target semantic anchors/invariants rather than arbitrary one-phrase spelling.

No qualification threshold, hard fail, profession scope, held-out independence requirement or trust-tier requirement was weakened.
