# Knowledge and sources: Motion & Visual Art Direction v0.1

Date: 2026-10-23. Evidence grades: PRIMARY (the source states its own rule), SECONDARY (a writer reports practice), ANALYZER (automated analysis of a moving artifact, structure usable, details unverified), INFERRED (author's inference, labeled).

## What was actually read in this pass

1. Google Material Design 1, "Duration and easing" (https://m1.material.io/motion/duration-easing.html), PRIMARY. The page says Material 1 is no longer maintained and points to Material 3, so the numbers are orientation for UI transitions, not a law for vertical video.
   - Mobile transitions "typically occur over 300ms"; large complex ones up to 375ms; entering 225ms, leaving 195ms; over 400ms may feel too slow; tablet about 30% longer; desktop 150-200ms.
   - Longer duration for longer travel or larger surface change; shorter for small changes; "don't use one duration for every animation".
   - Enter = deceleration (ease out, `cubic-bezier(0,0,.2,1)`); exit = acceleration (ease in, `cubic-bezier(.4,0,1,1)`); standard ease in-out `cubic-bezier(.4,0,.2,1)`. Asymmetric curves are called more natural.
2. Adobe Blog, "Six Principles of Using Animation in UX Design", Margaret Seelie, 2019-06-19, drawing on Val Head (https://blog.adobe.com/en/publish/2019/06/19/designing-animation-six-principles-using-animation-ux), SECONDARY. Principles: timing, easing, spatial orientation, directing focus, visual continuity, clarity ("remove it if you cannot state its purpose"; stagger and overlap instead of animating everything at once). Only number: a 300ms menu slide. Qualitative otherwise.
3. Netflix Russian Timed Text Style Guide (https://partnerhelp.netflixstudios.com/hc/en-us/articles/215346638-Russian-Timed-Text-Style-Guide), PRIMARY for subtitles: up to 17 characters per second for adult programs, 42 characters per line, maximum two lines. Minimum event duration and gaps not in that page. Used here only as a ceiling for running text by analogy (INFERRED); a punchy hook plate can be read faster than a subtitle, but the ceiling is a useful alarm.
4. School of Motion, list of inspiration sources (https://www.schoolofmotion.com/blog/motion-design-inspiration-sites), SECONDARY listicle. Named curated outlets: Stash, Motionographer, Art of the Title, Behance (Motion channel), Dribbble, Abduzeedo, Ordinary Folk "Play". The article does not say which are juried. This is a starting map, not proof of quality.
5. Project evidence already in the applied repo: `evidence/market-intelligence/motion-reference-benchmark-2026-10-23.md` (PARTIAL): four references analyzed by an automated video analyzer, with the derived vocabulary (real interface from frame one, one headline, state change with badge, crop to one panel, no full-desktop letterbox).

## What was searched and not obtained

- Official Meta safe-zone specification for Reels: search returned only third-party guides. UNVERIFIED. The working rule remains the user's own: keep the bottom 20 percent clear, and verify overlays on a real phone.
- Primary writing by working motion studios on their process (BUCK, Ordinary Folk, PEDRA case studies): not read in this pass. This is the main gap in the knowledge base.
- Any evidence on what makes short-form motion *distinctive* rather than competent. Not found. The agent therefore treats distinctiveness as a human-judged gate.

## Practices adopted into the agent (with their basis)

| Practice | Basis |
|---|---|
| Reference decomposition before any concept | creative-profession-architecture 3 |
| 3 concepts that differ in mechanism, not style | creative-profession-architecture 4 |
| Every motion states purpose or is removed | Val Head via Adobe, principle 6 |
| Vary durations by distance/weight; enter ease-out, exit ease-in; no default linear | Material 1 page |
| Text reading budget, 17 cps as a ceiling, 42 chars per line, 2 lines max for running text | Netflix (analogy) |
| Directing focus: one focal element at a time | Adobe principle 4; project benchmark vocabulary |
| Continuity: show where things go (exit with motion, not a pop) | Adobe principles 3, 5 |
| Critique by contact sheet plus mid-transition frames, diagnose then prescribe | creative-profession-architecture 8 |

## Open knowledge gaps (to improve the agent next)

1. Read two or three primary studio process write-ups and a vertical music-free UI film that can be inspected.
2. A comparative taste file for the user (accepted and rejected examples with reasons).
3. An official Meta safe-zone source.
4. A repeatable frame-sheet tool (the procedure is in the SKILL; a script is not yet written).
