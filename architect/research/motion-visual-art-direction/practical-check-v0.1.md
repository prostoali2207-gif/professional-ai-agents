# Practical check record: Motion & Visual Art Direction v0.1

Date: 2026-10-23
Artifact: `agents/motion-visual-art-direction/0.1.0/SKILL.md` (branch `agent/motion-visual-art-direction-v0.1`)
Declared scope: concept, visual system, motion spec and critique for short vertical business/personal-brand video, supervised by the user. No authority to publish.
Label: CANDIDATE / NOT QUALIFIED. This is not formal qualification.

## Limitation of this check

Single author, single session, one real case, hindsight: the case was chosen because the user had already rejected the output. The check shows that the procedure *finds the defects*; it does not show that the agent *produces* distinctive work. That needs the next real task and the user's comparative judgement. No independent grader.

## Case 1: real artifact, the rejected "request-status" demo Reel (v2, Remotion, 16 s)

Method: SKILL section 7 applied to the rendered file. A contact sheet at 1 frame per second (16 frames) and the source code were reviewed. Not checked: motion feel on a phone, the real Instagram interface.

Process finding (before the artifact): the reference gate (section 2) was not cleared. The project's benchmark record said PARTIAL / BOUNDED and the video was rendered anyway. With this agent the outcome would have been `BOUNDED`, stop.

Defects found in the artifact:

| Layer | Defect | Evidence |
|---|---|---|
| Concept distinctiveness | Genre default: dark rounded cards, one coloured banner, status badge. Nothing ties it to this author or could not be swapped for another brand. | contact sheet, all frames |
| Pacing | About 9 of 16 one-second frames are the same dimmed board. The only moving things are the plate text and a small cursor. | frames 3-8 and 9-13 |
| Colour roles | The same status word "В работе" is green in the other rows and blue in the focus row. Amber means both "problem" and the banner and the menu highlight. The plate stays amber after the problem is solved. | frames 1, 9, 12 |
| Logic | The counter says "Зависших: 1" while the row already reads "В работе". | frames 9-10 |
| Motion purpose and easing | Pointer path uses linear interpolation (code lines 60-61); text plate swaps pop in with no exit. | `Demo.tsx` |
| Safe area | Pointer is scripted to leave to y=1560 of 1920, inside the bottom 20 percent that was to stay clear. | `Demo.tsx` line 58 |
| End card | Faint ghost text of the dimmed rows remains behind the handle. | last frames |
| Reading budget | The last plate has 32 characters, fully visible about 1.7 s, about 19 characters per second, above the 17 ceiling. | arithmetic from the code |

Result: the procedure finds eight concrete defects that were present, and the process violation. Expected behavior (BOUNDED stop) is satisfied by the text. PASS against expectation for diagnosis; NOT evidence of generative quality.

## Case 2 and 3: not executed

- Adversarial: "just make it look premium, skip references". Rule exists (Hard rule 1, Hard rule 2). Reviewed, not executed.
- Boundary: "write the hook and the claim for it". Hands off to Social Content Creative. Reviewed, not executed.

## Defects found in the agent itself

- The reading-budget ceiling is borrowed from subtitle practice and may be too strict for hook plates; marked as a ceiling by analogy, to be calibrated on real pieces.
- The contact-sheet procedure has no script. Added to open gaps.

## Follow-up route

First real use: reference gate on curated sources, then three concepts for the same brief, user compares in one sentence, record the reaction, repair root causes in the SKILL, add regression cases here.
