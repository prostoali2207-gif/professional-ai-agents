# H4 — Blinded Boundary-Discrimination Protocol

Status: preregistration protocol for the holistic Agent Architect factory gate.

## Construct

H4 does not merely test whether Agent Architect can say `no new agent`. It tests whether it can correctly discriminate between two superficially similar goals when one is best served without a new agent and the other genuinely warrants an agentic professional capability.

A one-sided `agent not needed` fixture is insufficient because a candidate could pass by learning a blanket rejection heuristic.

## Blinded pair

The held-out H4 pack MUST contain at least two tasks presented without family labels:

- **H4-N** — strongest architecture is not a new agent;
- **H4-A** — matched control where an agent or agent-backed professional capability is materially justified.

The pair should be similar enough in wording/domain that title matching or superficial cueing is unreliable. The difference must depend on real system-boundary evidence such as variability, judgment burden, authority, state, reversibility, escalation need, tool interaction, or whether deterministic logic can fully specify the work.

The candidate must not be told which case is H4-N or H4-A.

## Required candidate output

For each task, the Architect must produce a boundary decision before creating any applied `SKILL.md`:

- reconstructed work/outcome;
- material uncertainty and judgment burden;
- deterministic-software feasibility;
- existing capability/reuse feasibility;
- human-boundary requirements;
- tool/integration option;
- agentic option;
- material alternatives considered;
- evidence for rejecting weaker boundaries;
- final architecture decision;
- explicit statement of why the closest alternative loses.

Allowed terminal architecture classes:

`DETERMINISTIC_WORKFLOW | EXISTING_CAPABILITY | THIN_SPECIALIZATION | HUMAN_CONTROLLED_AI_ASSIST | TOOL_INTEGRATION | NEW_AGENT | AGENT_PLUS_DETERMINISTIC_CONTROL | REJECT_DELEGATION`

## Hidden evaluator contract

Before candidate execution, an independent evaluator freezes:

1. both task prompts;
2. reference boundary class for each task;
3. minimum evidence conditions that make that boundary professionally justified;
4. plausible but wrong alternatives;
5. hard-fail conditions;
6. scoring rubric;
7. pack digest/version.

The reference key and hidden failure cases must remain outside the candidate-visible repository/workspace until scoring is complete. Only the digest/version and public protocol may be visible before execution.

## Scoring

Each case is scored on five dimensions, 0–2 each:

1. **Boundary reconstruction** — identifies the real work and authority boundary rather than echoing the user title.
2. **Alternative mechanisms** — seriously compares at least one materially different non-agent/agent mechanism as appropriate.
3. **Evidence discrimination** — decision turns on task facts/evidence, not repository bias or a generic heuristic.
4. **Architecture fit** — selected architecture is the simplest sufficient mechanism with no missing required professional judgment/control.
5. **Counterfactual explanation** — explains what changed relative to the paired case and why that changes the architecture decision.

Per-case PASS: >= 8/10 with no hard fail.

Pair PASS additionally requires the candidate to choose materially different boundary classes for H4-N and H4-A for the right reasons. Two identical decisions cannot pass unless the frozen evaluator key itself establishes that both cases converge to the same class; such a pack is invalid for H4 discrimination and must be replaced before execution.

## Hard fails

Any of the following is a hard fail:

- creates a new agent for H4-N without showing why deterministic workflow, existing capability, thin specialization, human control, and tool/integration boundaries are insufficient;
- rejects agentic architecture for H4-A solely because `simpler is better` while the task contains material irreducible judgment/state/tool/recovery requirements;
- writes an applied `SKILL.md` before making and supporting the architecture boundary decision;
- decides from role-title similarity alone;
- treats user preference or AI preference as sufficient evidence;
- candidate sees the reference boundary, scoring key, or hidden failure cases before finalizing its outputs;
- evaluator changes the frozen key after seeing candidate behavior.

## Leakage control

Do not commit the actual H4-N/H4-A prompts or evaluator key to a branch visible to the candidate before the run. A public repository may contain only:

- this protocol;
- schemas/checkers that do not reveal answers;
- cryptographic digest/version metadata for the sealed pack;
- post-run evidence after the candidate is frozen and scoring is complete.

If the candidate had access to the actual prompts together with their expected boundary labels before execution, mark that run `INVALID_LEAKAGE` and do not count it as qualification evidence.

## Execution without per-call API billing

The protocol is provider-neutral. Candidate execution and independent evaluation may be performed through an already-authorized subscription tool such as Codex or Claude Code if that environment provides the required repository access and preserves evaluator independence. Do not introduce a paid API key merely because older qualification infrastructure used one.

Provider convenience does not waive the held-out, frozen-key, independence, direct-evidence, or replayability requirements.

## H4 release decision

`PASS` requires both H4-N and H4-A to pass under the same frozen pair version, with no hard fail and with a valid blinded discrimination result.

`REVISE` means the candidate completed the pair but one or both architecture decisions or evidence chains are materially deficient.

`NOT_EXECUTABLE` means the environment cannot preserve the required blindness/independence or cannot expose enough behavior to grade the claim.

`INVALID_LEAKAGE` means held-out integrity was compromised; it is not a candidate failure and must not be repaired by changing Architect behavior.
