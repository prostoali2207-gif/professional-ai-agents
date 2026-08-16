# Agent Security and Trust-Boundary Engineering

Status: v0.1.

## Purpose

Tool-capable professional agents consume content and execute actions across trust boundaries. Least privilege alone is not enough. External text, webpages, retrieved documents, tool outputs, memories, skill packages, and delegated agents can carry instructions or data designed to redirect the agent.

Security must therefore model information trust and control authority separately.

## 1. Trust-boundary map

For every consequential agent identify:

- trusted system/policy instructions;
- user instructions and their authorization scope;
- external/retrieved content;
- tool outputs;
- persistent memories/state;
- third-party skills/scripts/plugins;
- delegated agents/services;
- secrets/credentials;
- network destinations;
- data stores and publication targets.

Classify which channels may provide **data**, which may provide **instructions**, and which may authorize **actions**. Do not let lower-trust content silently acquire higher-trust authority.

## 2. Indirect prompt injection and agent hijacking

Treat externally controlled content as potentially adversarial when it can influence model behavior.

Examples include:

- instructions embedded in webpages/documents/emails/issues;
- tool-returned text that asks the agent to reveal secrets or call another tool;
- retrieved content that impersonates system policy;
- malicious memory entries;
- poisoned skill/reference packages.

Required behavior:

- preserve instruction/data separation where the runtime allows it;
- constrain actions by explicit user/system authority, not by content encountered during execution;
- minimize access to secrets and write-capable tools while processing untrusted content;
- require stronger confirmation/verification before sensitive side effects;
- log security-relevant decisions and denied requests where material.

## 3. Data-flow and secret discipline

For sensitive workflows define:

- what data may enter each tool/service;
- what credentials the agent can access;
- whether credentials are scoped/ephemeral;
- permitted network destinations;
- exfiltration-sensitive fields;
- redaction/minimization rules;
- retention/logging constraints;
- cross-tenant/user isolation.

A tool may be functionally useful yet professionally unsuitable because its data or network boundary is wrong.

## 4. Sandbox and execution policy

For shell/code/browser/computer-use agents specify:

- filesystem scope;
- process/runtime isolation;
- network defaults and allowlists;
- resource/time limits;
- privilege level;
- destructive-action controls;
- download/executable handling;
- approval rules;
- rollback/recovery.

Prefer deny-by-default for capabilities whose unintended use has meaningful blast radius, then grant the narrow capability required by the task.

## 5. Skill and dependency supply chain

Procedural packages can contain executable code and trusted-seeming instructions. Before adopting third-party skills/plugins/scripts, evaluate:

- origin and maintainer;
- immutable/versioned identity when available;
- code/instruction review appropriate to risk;
- transitive dependencies;
- requested tools/permissions/network access;
- unexpected persistence or data collection;
- update mechanism and change review;
- revocation/removal path.

Do not infer trust from popularity or a familiar folder format.

## 6. Memory/state poisoning

Persistent state can convert one malicious or erroneous observation into future behavior.

Use a memory write gate with provenance, confidence, scope, sensitivity, and instruction/data classification. Security-relevant or authority-changing state should not be written solely from untrusted content.

Use `runtime-state-memory-context.md` for the full memory lifecycle.

## 7. Safe delegation

When handing work to another agent/service, pass only the permissions, data, and context required for the subtask. A subagent should not inherit broader authority merely because the parent possesses it.

Handoffs must preserve provenance and clearly distinguish upstream constraints from untrusted task content.

## 8. Security evaluation

Include representative adversarial tests such as:

- webpage/document asks agent to ignore task and reveal a secret;
- tool output contains a fake system instruction;
- retrieved source requests an unrelated write/send action;
- malicious memory tries to persist elevated authority;
- third-party skill requests unnecessary network/write permissions;
- user authorizes one action but injected content attempts a broader action;
- data must not cross a jurisdiction/tool boundary;
- compromised subagent returns a plausible result plus unauthorized side effect request;
- security prompt is paraphrased/obfuscated rather than literal;
- legitimate task requires handling untrusted content without becoming unusably defensive.

Grade both attack resistance and task completion. A system that prevents every attack by refusing all useful work is not professionally adequate.

## 9. Security incident loop

Security incidents and near-misses must feed the production-learning process with preserved evidence:

`event -> contain -> verify impact -> root cause/trust-boundary failure -> repair -> adversarial regression -> permission review -> redeploy/monitor`.

Do not patch only the exact attack string.

## Quality gate

Agent security passes only when a reviewer can identify:

1. Which inputs are trusted for data, instructions, and authority?
2. What prevents untrusted content from escalating control?
3. Where can secrets/data flow?
4. What is sandboxed or network-restricted?
5. How are third-party skills/dependencies trusted and revoked?
6. How is persistent-state poisoning prevented?
7. Which adversarial eval demonstrates useful work under attack?

Permissions without a trust-boundary model are insufficient for a professional tool-using agent.
