# Video Editing & Post-Production Candidate Evaluation

Status: prerelease evaluation design; no PASS claimed.

The first gate is deterministic contract validation. The semantic/practical gate must then test VE-S1..VE-S12 without exposing expected decisions to the candidate. Render-capable claims additionally require real source media, produced artifacts, metadata probes, representative-frame/audio inspection and calibrated human comparative review.

Required release order:

1. validate manifest, evidence links and frozen fixture structure with zero model calls;
2. run the critical decision subset repeatedly: VE-S2, VE-S4, VE-S6, VE-S10 and VE-S11;
3. run all frozen semantic cases;
4. run practical render cases on at least two materially different runtimes/toolchains or narrow portability claims;
5. calibrate subjective craft grading against domain-practitioner judgments;
6. freeze exact artifact digest and qualifying environment;
7. only then add a qualification record and promote catalog lifecycle.

Infrastructure failure is BLOCKED, not behavioral PASS/FAIL. A polished self-report, edit plan, command log or timeline screenshot is not evidence that the exported video is correct.
