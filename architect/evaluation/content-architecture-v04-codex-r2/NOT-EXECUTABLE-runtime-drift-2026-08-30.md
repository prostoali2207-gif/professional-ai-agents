# Content Architecture v0.4 Codex r2 — NOT_EXECUTABLE

Status: `NOT_EXECUTABLE`

Reason: the preregistered runtime eligibility pinned Codex CLI `0.151.0-alpha.7.1`, but the self-hosted runner's authenticated Codex Desktop runtime resolved to `codex-cli 0.151.0-alpha.7.2` before any scored r2 candidate call.

Evidence:
- GitHub Actions run `33308687443` reached the exact runtime identity check.
- Codex CLI was found on the self-hosted Windows runner.
- ChatGPT subscription authentication was valid (`Logged in using ChatGPT`).
- Observed CLI identity was `codex-cli 0.151.0-alpha.7.2`.
- r2 scored candidate calls: `0`.

Integrity decision: do not mutate the preregistered r2 runtime identity after dispatch. Burn r2 and create a fresh r3 cycle bound to the observed `0.151.0-alpha.7.2` runtime before any scored call. Candidate, grader semantics, thresholds, P0 policy, repeat policy, and r1 evidence remain unchanged.
