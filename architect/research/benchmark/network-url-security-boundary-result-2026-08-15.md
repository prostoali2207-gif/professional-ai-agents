# Network / URL Security Boundary Result — 2026-08-15

Status: **POLICY PREFLIGHT PASS; TRANSPORT/EGRESS ISOLATION NOT YET PROVEN**

This is a research-only benchmark artifact. It does not modify `architect/SKILL.md`, Agent Architect v1.1 validation, or PR #1.

## Executed evidence

GitHub Actions workflow: `Network URL Security Boundary v0.1`

Run: `31874206272`

Head: `e5945ace26729080dff4618734d998f819748261`

Deterministic URL/SSRF policy cases: **23 / 23 passed**.

The executed policy demonstrated:

- only `https` is accepted by default;
- only port `443` is accepted;
- URL userinfo is denied;
- loopback/private/link-local/non-global IPv4 and IPv6 literals are denied;
- hostname authorization requires DNS resolution;
- every DNS answer must be globally routable; mixed public+private answers fail closed;
- DNS failures fail closed;
- redirect targets are re-authorized independently;
- redirects to HTTP, loopback, metadata/link-local, or mixed-DNS targets are denied;
- redirect depth is capped;
- public HTTPS positive controls remain usable.

## Threat-model adjudication

### Proven by this run

**URL AUTHORIZATION POLICY: PASS**

The policy correctly classifies the seeded SSRF/URL-confusion cases and fails closed for dangerous targets.

### Not proven by this run

**DNS REBINDING / TOCTOU RESISTANCE: NOT PROVEN**

A check-before-connect implementation is insufficient if the HTTP client resolves the hostname again after authorization. The address used for the real connection could differ from the address that was checked.

**HOST-LEVEL EGRESS ISOLATION: NOT PROVEN**

This Python policy does not prevent arbitrary code/subprocesses from opening sockets directly around the research adapter.

**PROXY / CDN DESTINATION TRUST: NOT PROVEN**

Provider-hosted fetchers may have their own redirect, DNS, caching, or private-network behavior. Their server-side implementation cannot be inferred from our local URL policy.

## Required production architecture control

The research layer should not expose arbitrary raw network access to the synthesis/model process.

Use a separate controlled retrieval plane:

`research/model process -> typed fetch request -> URL policy -> DNS authorization -> controlled fetch transport / egress proxy -> response sanitizer -> untrusted evidence record`

Minimum transport requirements:

1. resolve target through the controlled fetcher;
2. reject the request if any resolved address is non-global;
3. connect to an explicitly authorized resolved address rather than allowing a second unconstrained DNS lookup;
4. preserve original hostname for TLS SNI/certificate validation and HTTP `Host` semantics;
5. re-run authorization for every redirect before following it;
6. cap redirects, response size, decompression ratio, and wall-clock duration;
7. deny raw `file`, `ftp`, `gopher`, `data`, Unix socket, localhost, link-local, private, multicast, unspecified and reserved destinations;
8. keep cloud metadata endpoints and private address ranges denied independently of provider prompt instructions;
9. log requested URL, normalized host, authorized destination IP, redirect chain, timestamps and denial reason without secrets;
10. do not give the model process credentials that make private/internal destinations valuable even if another defense fails.

## P0 security conditions

Any of the following is P0 for the research architecture:

- retrieved content causes a successful request to localhost/private/link-local/metadata infrastructure;
- a redirect bypasses destination authorization;
- model/tool output causes a connection outside the controlled retrieval plane;
- DNS rebinding changes an approved public target into a private/internal destination at connection time;
- arbitrary URL schemes provide filesystem/process/network access;
- secret-bearing headers/cookies are forwarded to an untrusted cross-origin redirect.

## Professional red-team note

A security engineer would reject the statement "SSRF is solved" based only on URL parsing. URL validation is necessary but not sufficient. The security property has to be enforced at the **actual network connection boundary**, preferably by network policy/egress proxy in addition to application-level checks.

Therefore the honest verdict is:

**POLICY PREFLIGHT PASS / NETWORK ISOLATION REMAINS AN IMPLEMENTATION GATE.**
