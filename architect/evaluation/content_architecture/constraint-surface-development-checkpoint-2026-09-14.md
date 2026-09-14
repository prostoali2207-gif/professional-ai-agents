# Content Architecture v0.5 constraint-surface — visible development checkpoint

date: 2026-09-14
issue: #306
status: DEVELOPMENT PASS / CANDIDATE NOT QUALIFIED

## Exact assembly

- qualified parent: Content Architecture v0.4 blob `5d440e1bf3e20fbd35c6ab276310a904e36cc06d`
- candidate overlay: `74942d09593f73d0a9a23be068d3bbf3a0b8c06d`
- frozen protocol: `d90c9daab6256fce3388025db7a656dc06489f1a`
- candidate status remains `CANDIDATE / NOT QUALIFIED / NOT LIBRARY-ADMITTED`

## Visible regressions

| Case | Expected | v0.5 rule | Verdict |
|---|---|---|---|
| CA-CML-01 | landing→CRM guard stays internal | negative constraint defaults INTERNAL_ONLY | PASS |
| CA-CML-02 | no AI-first guard stays internal | negative constraint defaults INTERNAL_ONLY | PASS |
| CA-CML-03 | claim-safety guard stays internal | omit unsupported claim, no public disclaimer | PASS |
| CA-CML-04 | explicit public request may surface | PUBLIC_MESSAGE_CANDIDATE | PASS |
| CA-CML-05 | required safety/legal disclosure surfaces | PUBLIC_MESSAGE_REQUIRED | PASS |
| CA-CML-06 | complaint is failure evidence, not copy | user-feedback firewall | PASS |

Static/contract conformance: **6/6 PASS**.

## Applied practical

PBGS ORIENTATION-01 production incident was replayed after the repair:
- service-independence remained a silent HARD / INTERNAL_ONLY constraint;
- it disappeared from public information order;
- public architecture retained only the independent communication job.

Applied practical verdict: **PASS**.

## Evidence boundary

This proves the candidate contract contains the required repair and the known production incident is handled correctly in applied development.

It does NOT establish held-out/stochastic reliability or qualification.

## Current professional judgment

Use v0.5 in PBGS applied work with explicit candidate status.
Do not mutate qualified v0.4 in place.
Do not promote v0.5 to qualified until independent targeted compatibility/held-out evidence exists.