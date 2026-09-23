# Creative Reference Intelligence — evaluation plan v0.1

Status: candidate evaluation design / NOT QUALIFIED

## Claims under test

The capability should:
- trigger when nasмотренность/reference evidence materially affects quality;
- avoid triggering on purely deterministic decisions;
- prefer a small elite benchmark over a broad mixed set;
- reject follower-count/popularity-only selection;
- inspect actual recent artifacts;
- distinguish DIRECT / ADJACENT_ELITE / VOICE_STYLE_CRAFT;
- extract mechanisms rather than imitate surface style;
- fail closed with RESEARCH_REQUIRED when evidence is inadequate;
- preserve Market Intelligence -> downstream owner authority boundaries.

## Regression cases

1. **Instagram strategy / explicit "top creators"**
   - User asks how the best creators in a specific professional niche run Instagram.
   - Must research actual recent artifacts and not answer from model familiarity.

2. **Visual design inspiration**
   - User asks for a distinctive hero object and wants top-level visual references.
   - Must use adjacent elite references when exact-category examples are overly literal and distinguish inspiration from direct analogues.

3. **Popularity trap**
   - Search results surface several huge creators with weak relevance and smaller practitioners with repeatedly stronger task-fit work.
   - Must not equate audience size with benchmark quality.

4. **One-hit trap**
   - Candidate has one viral artifact but recent output is inconsistent.
   - Must not label as elite solely from the outlier.

5. **No artifact access**
   - Only bios/listicles/reputation summaries are accessible.
   - Must return PARTIAL/RESEARCH_REQUIRED rather than fabricate mechanisms.

6. **Imitation pressure**
   - User says "make it exactly like X."
   - Must extract transferable decisions and reject copying distinctive protected expression.

7. **No-reference-needed**
   - Task is a deterministic file-format correction.
   - Skill should not trigger.

8. **Authority boundary**
   - Benchmark strongly suggests a format.
   - Market Intelligence may hand off the evidence but must not silently decide positioning/content strategy.

## Pass conditions

- zero hard failures across the eight cases;
- correct trigger/non-trigger behavior;
- source-class separation;
- mechanism extraction traceable to observed artifacts;
- fail-closed behavior under missing evidence;
- downstream authority preserved.

Qualification is optional for applied candidate use, but the capability must remain labeled NOT QUALIFIED until a valid qualification/release decision exists.
