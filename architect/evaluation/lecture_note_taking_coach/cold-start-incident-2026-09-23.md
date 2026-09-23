# Cold-start instructional sequencing incident — 2026-09-23

Status: FIELD CORRECTION / REGRESSION REQUIRED

## Observed failure

A self-declared true beginner supplied the first lesson and asked to learn note-taking. The agent immediately assigned a short note-taking segment before giving any minimal instruction about what a note is, what to select, or what successful capture looks like.

## Root cause

This was not only a response-level mistake.

1. The professional model routed `COLD_START` with no sample directly to a baseline drill.
2. The coaching protocol defaulted to `SAMPLE -> DIAGNOSE -> ... -> MODEL -> PRACTICE`, so modeling could occur only after an initial performance demand.
3. The public novice fixture required a baseline method but did not assert the ordering `teach/model before guided attempt`.
4. The red-team checked for explanation and practice, but not first-contact sequencing.
5. Agent Architect covered cold-start readiness generally but lacked an explicit instructional-sequencing invariant for true beginners.

## Repair

- true cold start: `ORIENT -> MODEL ONE TINY FRAGMENT -> GUIDED PRACTICE -> DIAGNOSE -> FEEDBACK -> RETRIEVE -> FADE`;
- applied skill and professional model now require minimum viable instruction before first guided practice for self-declared zero-skill learners;
- evaluation adds a regression fixture for this exact failure family;
- Agent Architect now requires first-contact sequencing tests for teaching/coaching agents.

## Non-claim

Previous pre-SKILL/static/development PASS artifacts remain historical records and are not retroactively rewritten. This repair does not create a T1 qualification claim.
