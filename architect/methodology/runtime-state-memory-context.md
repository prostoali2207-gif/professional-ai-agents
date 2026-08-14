# Runtime State, Memory, and Context Engineering

Status: v0.1.

## Purpose

A professional agent that works across multiple steps or sessions needs more than retrieval. It needs an explicit policy for what state exists, what enters context, what may persist, what must expire, and how state is recovered after interruption.

Do not treat a larger context window, transcript history, vector database, or notes file as equivalent to reliable memory.

## 1. Separate state classes

Model at least the state classes that materially exist for the target work:

- **working context** — information required for the current decision/action;
- **session state** — task progress, decisions, tool results, unresolved items, and artifacts needed across turns in one run;
- **episodic memory** — prior incidents/cases whose circumstances and outcomes may inform later work;
- **semantic memory** — durable facts/principles that remain valid beyond one episode;
- **procedural memory** — reusable workflows, skill instructions, scripts, schemas, and operating procedures;
- **external source of truth** — authoritative records that should be re-read rather than memorized when correctness depends on current state.

Not every agent needs every class. Absence or persistence must be an architecture decision.

## 2. Memory lifecycle

For every persistent memory path define:

`candidate observation -> write gate -> representation -> storage -> retrieval -> use -> update/conflict resolution -> expiry/forgetting -> audit/deletion`.

A memory write is a consequential transformation, not a free by-product of conversation.

### Write gate

Persist only information with an identified future use. Check:

- provenance/source;
- confidence and whether it is observed, reported, inferred, or contested;
- scope and applicability;
- sensitivity/privacy;
- expected lifetime;
- contradiction with existing state;
- whether the authoritative source should be queried live instead.

Do not convert a user statement, model inference, or one incident into durable fact merely because it appeared in context.

## 3. Context assembly

The active context should be decision-relevant, not a dump of everything known.

Define:

- mandatory invariant/constraint context;
- current task state;
- evidence needed for the next decision;
- retrieved knowledge/memory;
- tool schemas and procedural resources;
- context-budget priority;
- what can be omitted or summarized safely.

When context is compacted or summarized, preserve decision-critical constraints, unresolved uncertainty, provenance references, state transitions, and commitments. Evaluate compaction for semantic loss rather than token reduction alone.

## 4. State consistency

Long-running work requires explicit consistency rules.

Track when material:

- facts established vs assumptions/hypotheses;
- decisions already made and their rationale;
- actions already executed;
- expected vs observed downstream state;
- stale observations;
- concurrent or conflicting updates;
- ownership of shared state across agents/handoffs.

If two memories conflict, do not silently select the most recent text. Determine whether the conflict is supersession, scope difference, bad evidence, or unresolved disagreement.

## 5. Checkpoint and resume

For interruptible or long-horizon work, define a resumable checkpoint containing enough information to continue safely without replaying hidden assumptions.

A checkpoint may include:

- task objective and preserved constraints;
- current plan/progress state;
- established facts and evidence references;
- unresolved uncertainties;
- completed side effects and downstream verification;
- pending actions;
- permissions/approvals already granted and their scope;
- relevant artifact/version identifiers;
- termination/recovery state.

Do not assume a textual conversation summary is a sufficient checkpoint for consequential work.

## 6. Memory security and privacy

Persistent memory expands the trust boundary.

Evaluate:

- sensitive-data retention and minimization;
- memory poisoning by untrusted content;
- instruction-like text stored as data;
- cross-user/session leakage;
- unauthorized durable preferences/claims;
- provenance loss;
- deletion/forgetting requirements;
- whether retrieved memory can influence tool authority.

External content must not become trusted system instruction merely because it was stored previously.

Use `agent-security-and-trust.md` for the broader threat model.

## 7. Memory evaluation

Stateful agents require evaluation beyond single-turn correctness. Include as relevant:

- extraction of a decision-relevant fact from an earlier interaction;
- multi-session reasoning over several compatible observations;
- temporal reasoning and supersession;
- correction when a previous fact becomes outdated;
- contradiction detection;
- abstention when the required memory was never established;
- resistance to distractor memories;
- context-compaction preservation of critical constraints;
- correct forgetting/deletion behavior;
- restart/checkpoint recovery;
- prevention of cross-session/user leakage;
- memory-poisoning adversarial cases.

Measure both retrieval of the right state and whether the agent uses it correctly.

## 8. Portability rule

Describe memory requirements as capabilities, not one vendor service. An applied agent should declare which capabilities are required, optional, or replaceable:

- session persistence;
- long-term memory;
- structured state;
- semantic retrieval;
- compaction;
- checkpoint/resume;
- deletion/retention controls.

If the target runtime lacks a required capability, define a fallback or declare the architecture unsupported rather than pretending portability.

## Quality gate

Runtime state/memory architecture passes only when a reviewer can answer:

1. What state exists and why?
2. What may become durable, under what write gate?
3. What enters the active context for each decision?
4. How are contradictions, staleness, and compaction handled?
5. How does the agent safely resume after interruption?
6. How are privacy, poisoning, and deletion handled?
7. Which stateful/multi-session eval proves the design works?

A professional agent with material long-horizon or multi-session work is incomplete when these questions are left implicit.
