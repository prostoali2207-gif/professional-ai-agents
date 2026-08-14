# Operational Governance for Professional Agents

Status: v0.1.

## Goal

Ensure that an agent is not judged only by cognitive quality. A deployable professional agent must also have bounded authority, acceptable operating economics, reproducible execution assumptions, and accountable escalation.

## 1. Capability vs authority

An agent may be technically capable of an action without being authorized to perform it autonomously.

For each meaningful action classify:

- read/observe;
- propose;
- draft;
- write/modify;
- publish/send;
- delete/destruct;
- deploy/release;
- spend/commit resources;
- approve/authorize.

Define the maximum autonomous level separately from competence.

## 2. Permission and blast radius

Use least-required permissions.

For each tool/action define:

- resources accessible;
- read/write scope;
- reversibility;
- external side effects;
- potential blast radius;
- confirmation requirement;
- rollback path;
- audit/log requirement.

High-impact irreversible actions require stronger evidence, explicit authority, or human approval than low-impact reversible actions.

## 3. Cost and latency economics

Agent architecture is not better merely because it performs more reasoning or uses more agents/tools.

Track when material:

- end-to-end latency;
- model/token cost;
- tool/API cost;
- human review time;
- operational complexity;
- failure/retry cost;
- coordination overhead.

A more complex architecture must demonstrate enough quality/risk benefit to justify these costs on representative tasks.

## 4. Environment and reproducibility

Record execution assumptions that materially affect behavior:

- model/model family or capability class;
- required tools/connectors;
- repository/project state;
- runtime and relevant versions;
- access permissions;
- network/live-research availability;
- external-service dependencies;
- locale/jurisdiction when relevant.

Do not claim that a skill is portable across environments unless it has been tested across those environments or the differences are bounded.

## 5. Accountable ownership

For consequential systems define:

- who owns the agent's deployment;
- who owns domain correctness;
- who receives escalations;
- who can stop/rollback/decommission the agent;
- which decisions cannot be delegated organizationally even if technically automatable.

Autonomous capability does not remove organizational accountability.

## 6. Decision matrix

Before enabling a tool-capable agent, evaluate each action by:

`impact x reversibility x uncertainty x evidence quality x authorization`.

Higher impact, lower reversibility, greater uncertainty, weaker evidence, or weaker authorization should push toward narrower permissions, confirmation, specialist review, or abstention.

## 7. Release gate

A professional agent is not deployment-ready unless:

- necessary permissions are known and no broader than required;
- irreversible actions have safeguards;
- rollback/recovery is feasible where appropriate;
- operating cost/latency is measured where material;
- environment assumptions are documented;
- accountable owner/escalation path is clear;
- evals cover the actual permissioned workflow, not only simulated prose responses.

## Anti-patterns

Avoid:

- granting broad write access because a tool makes it convenient;
- confusing model confidence with authorization;
- multi-agent expansion without cost accounting;
- evaluating in a privileged sandbox unlike production;
- hiding human review burden from performance claims;
- making autonomous organizational decisions with no accountable owner.

## Quality gate

Operational governance passes when a reviewer can explain not only what the agent can do, but what it is allowed to do, under which environment, at what operational cost, with what blast radius, and who is accountable when it fails.