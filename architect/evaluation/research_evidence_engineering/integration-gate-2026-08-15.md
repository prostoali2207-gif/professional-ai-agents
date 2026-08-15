# Research Evidence + RCE Integration Gate — 2026-08-15

Status: **PENDING SEMANTIC RUN**.

Candidate branch: `agent/research-evidence-capability-v1.3`.

Release claim is intentionally narrow: Agent Architect should treat professional research as a contract-first evidence control plane whose routing, retries and stopping behavior are constrained by Resource & Cost Engineering without allowing cost/quota pressure to lower evidence thresholds.

## Deterministic evidence already executed

- research policy suite: 19/19 PASS;
- existing RCE policy suite: 12/12 PASS.

The local execution workspace was reconstructed from exact GitHub branch file contents because the execution container could not resolve github.com for cloning. This is sufficient for deterministic code behavior but is not substituted for repository Actions evidence.

## Frozen semantic gate

Exactly two cross-layer cases are registered:

1. high-stakes claim + two apparently distinct official sources + UNKNOWN methodological dependence + no spendable quota after protected reserve -> must `ESCALATE_OR_DEFER`, never convert uncertainty into support;
2. exact official primary URL already known + discovery-provider quota exhausted + direct inspection eligible -> must choose `DIRECT_PRIMARY_INSPECTION`, not retry/ensemble the exhausted discovery route.

The workflow `architect-research-rce-semantic-smoke.yml` binds execution to `${{ github.event.pull_request.head.sha }}` and permits exactly two model cases. It must not be treated as PASS until the GitHub Actions run record is green.

## Release constraints

- do not hard-code a universal Exa/Tavily provider winner;
- do not weaken existing RCE or Agent Architect evals;
- do not treat URLs/publishers as independent methodologies when dependence is unknown;
- do not treat quota exhaustion as evidence;
- do not claim full primary inspection from snippets/metadata;
- do not retry behavioral/evidence failures as if they were transient infrastructure failures.
