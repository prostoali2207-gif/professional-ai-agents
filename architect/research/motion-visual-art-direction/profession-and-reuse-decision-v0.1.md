# Motion & Visual Art Direction Practitioner: profession reconstruction and reuse decision v0.1

Date: 2026-10-23
Status: practical candidate research (NOT QUALIFIED). Follows `architect/methodology/practical-use-and-optional-qualification.md` (BUILD -> CHECK -> USE -> LEARN) and `architect/methodology/creative-profession-architecture.md`.
Trigger: applied project `personal-brand-growth-system` records "standalone Motion Design core" as a GAP (PBGS-MCI-MOTION-002). On 2026-10-23 the project's own first music-free demo Reel (Remotion render, "request-status") was produced without that competence and the user rejected it as generic and embarrassing. This record is the repair.

## 1. The real profession

An art director / motion designer for short vertical video made for a small business or personal brand: decides how a piece should look and move so that one message lands in 12-30 seconds with sound off. The recurring work:

- turning a communication job into a visual concept (what is the one thing the viewer must understand and feel);
- collecting and decomposing strong references, then deciding what to adopt, adapt and reject;
- exploring genuinely different concept families before choosing;
- building a small visual system (type, grid, colour roles, motion grammar) instead of styling each frame;
- writing a motion spec per beat (purpose, timing, easing, hierarchy);
- reviewing the rendered artifact critically and revising with reasons, not decoration;
- knowing when work is only competent and not distinctive, and saying so.

## 2. Decisions that separate a strong practitioner from an average one

| Decision | Average behavior | Strong behavior | Evidence basis |
|---|---|---|---|
| Starting point | opens the editor / writes code at once | reference decomposition and concept alternatives first | creative-profession-architecture sections 3-4 |
| Concept | the default look for the genre (dark UI, accent banner, fade-ups) | a concept with one idea that could not be swapped for another brand | the v2 failure; creative architecture section 5 (distinctiveness) |
| Motion purpose | animation because it looks alive | every movement states what it directs, shows or confirms; removed if it cannot | Adobe/Val Head principle 6 |
| Timing and easing | one duration, default or linear interpolation | durations vary with distance and weight; ease-out on enter, ease-in on exit; asymmetric curves | Material 1 duration-easing page; Val Head |
| Text on screen | whatever fits | reading-time budget per text event; one claim per event | Netflix timed-text guide (17 cps Russian) used as a ceiling by analogy |
| Review | looks at three frames | contact sheet at fixed intervals plus mid-transition frames, diagnosis before prescription | creative architecture section 8 |
| Quality claim | declares "premium" | states that taste needs a human comparative check and labels output DRAFT FOR TASTE REVIEW | creative architecture section 6 |

## 3. Reuse classification (existing library)

| Existing core | What it covers | Overlap with this role | Decision |
|---|---|---|---|
| Social Content Creative 0.1.0 | story, hook, copy, claims, post structure | owns the message, not the look or motion | REUSE as upstream owner of copy and claims; hand off |
| Video Editing & Post-Production 0.1.0 | assembly, finish, artifact-first QC of files | owns technical QC and edit, not art direction | REUSE as downstream owner of assembly and QC; hand off |
| Market & Competitive Intelligence 1.0.0 | evidence-graded research | useful for reference discovery method | REUSE the method for reference gathering |
| Conversion Messaging & Web Copy (agents/) | web copy | no overlap with motion | REJECT |
| Creative Reference Intelligence v0.4 (applied) | reference analysis method | partial | ADAPT its gate; this role adds the motion decisions |

Result: **BUILD NEW** as a bounded practical candidate. Reason: none of the existing cores owns the decisions in section 2 (concept distinctiveness, motion grammar, timing/easing, visual system, motion critique). Escalation upstream to a qualified core is optional and not required for use.

## 4. Boundaries

Owns: visual concept alternatives, reference decomposition decisions, visual system, motion spec, styleframe and motion review criteria, critique of rendered frames.

Does not own: message strategy and claims (Social Content Creative), offer and pricing, final assembly and technical QC (Video Editing), publishing authority (the user), rights clearance, music licensing.

## 5. Known hard limits

- The agent cannot watch motion. It sees extracted frames and its own spec. Motion quality claims are therefore spec-derived or frame-sampled, never "observed smoothness".
- Taste cannot be certified by the author of the output. A human comparative judgement is a required gate.
- Reference quality is bounded by tool reach (see knowledge file).
