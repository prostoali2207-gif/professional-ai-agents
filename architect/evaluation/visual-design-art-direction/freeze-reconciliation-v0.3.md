# Visual Design / Art Direction v0.3 — pre-score freeze reconciliation

Date: 2026-08-31
Issue: #158
Status: bookkeeping/integrity correction before any v0.3 held-out or scored provider call

## What happened

PR #213 contained two pre-merge refinement commits after the first `candidate-freeze-v0.3.json` content had been drafted:
- `b024390bf7393bdc8106dc93cc6f1a8a15e8bf1e` — aligned the v0.3 repair with the exact sanitized R4 P0 taxonomy;
- `6d319abab355da9bcb8b7451c499ca6e43cf756a` — added contrastive v0.3 development non-regression cases.

Both refinements landed **before** PR #213 was merged. The merged candidate behavior is therefore the final PR #213 state, but the original freeze metadata still pointed to earlier blobs.

No v0.3 held-out corpus had been authored, no v0.3 calibration had run, and no v0.3 candidate outcome had been scored when this mismatch was discovered.

## Resolution

Do not alter the merged v0.3 professional behavior. Reconcile `candidate-freeze-v0.3.json` to the exact merged PR #213 component identities and preserve candidate version `0.3.0-candidate`.

Exact merged candidate commit:
`b4793a66172d4de7fe0ade1b0001bc2621829db2`

Exact candidate component blobs:
- `candidate/SKILL.md` — `bee4ee67a8aff43016e158f37a6f421cd079581a`
- `professional-model-candidate-v0.1.md` — `bbea595e299445cf79f798ed1e86eecd0b53cd50`
- `professional-model-p0-repair-v0.2.md` — `bad4e815a3898dd19c7dfc0a07dd4c1aeeab3d50`
- `professional-model-p0-repair-v0.3.md` — `dd42d50f07b804c1ddd3c93b96704e0c6256440c`

Exact v0.3 development fixture blob:
- `fixtures-v0.3-targeted-regression.json` — `9f1249638c07a59336961a20b0518d6cc8c116a4`

The exact sanitized reference P0 identifier is `REFERENCE_IMITATION_AS_SOLUTION`.

## Integrity consequence

This is not post-outcome tuning and not a candidate repair. It is a pre-score identity correction to make the freeze describe the already-merged candidate exactly.

R4 remains historical v0.2 failure evidence only. Fresh independent R5 held-out evidence must be authored only after this reconciliation is merged and preregistered.

Current verdict: `NOT_QUALIFIED`.
