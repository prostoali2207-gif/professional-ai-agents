# Current-main check — 2026-08-23

Before qualification, Agent Architect `architect/SKILL.md` and `architect/evaluation/qualification-platform/README.md` were reread from current `main`.

Material change since this candidate branch was opened: current main now requires the reusable qualification lifecycle `candidate freeze -> static validation -> no-API preflight -> optional exact-runtime canary -> sealed held-out verification -> scored qualification -> sanitized report -> release verdict`, fail-closed and with infrastructure failures separated from professional failure.

Therefore the Social Content Creative qualification must NOT use the older ad-hoc plan directly. Candidate work must be rebased/recreated on current main and migrated onto the generic qualification platform before any scored API run.