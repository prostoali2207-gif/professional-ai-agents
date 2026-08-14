# Agent Architect Candidate Adapter Contract

Status: required to execute behavioral validation against a real Agent Architect runtime.

## Purpose

The harness must test the actual candidate behavior. A mock, scripted expected answer, or deterministic fixture-specific responder may be used only to test harness mechanics and can never count as Agent Architect release evidence.

The adapter is the narrow boundary between `runner.py` and the runtime that actually executes the candidate `architect/SKILL.md` at the frozen candidate SHA.

## Invocation

The harness invokes one command and writes a JSON object to stdin. The adapter must return one JSON object on stdout and use the supplied workspace for observable artifacts/state.

Input fields include:

- `protocol_version`
- `run_id`
- `candidate_sha`
- `family`
- `priority`
- `trial`
- `capability_profile`
- `input`
- `workspace`

The adapter must reject execution when it cannot establish that the loaded Agent Architect corresponds to `candidate_sha`.

## Required adapter responsibilities

1. **Candidate identity** — load the real Agent Architect candidate for the requested SHA and report the effective skill/runtime/model/tool versions.
2. **Session isolation** — support a fresh session when requested; do not leak prior trial transcript/state unless the fixture explicitly supplies or exposes it.
3. **Observable state** — write inspectable state/checkpoints/tool traces into the workspace when the family requires them.
4. **Capability profile enforcement** — deliberately remove unavailable capabilities for degradation tests rather than silently emulating them.
5. **Tool mediation** — expose only fixture-authorized tools/resources and preserve observable tool arguments/results/side effects.
6. **No hidden grader access** — never read grader keys, expected answers, sealed variants, or files outside the candidate-visible fixture surface.
7. **Termination record** — report why the candidate stopped, including success, escalation, unsupported configuration, or budget exhaustion.

## Minimum output

The JSON response must contain:

```json
{
  "candidate_identity": {
    "sha": "...",
    "runtime": "...",
    "model": "...",
    "tools": []
  },
  "status": "completed|escalated|unsupported|failed",
  "final_output": "...",
  "termination_reason": "...",
  "observable": {
    "tool_calls": [],
    "state_events": [],
    "resource_loads": [],
    "side_effects": []
  }
}
```

Families may require additional structured fields defined by the fixture schema.

## Stateful family requirements

For B1/B2/B6, the adapter must expose a real persistence boundary that can be inspected independently of the model response. The store may be a file/database/service, but the grader must be able to query it before and after sessions. A prose field such as `memory = correct` is not a persistence proof.

For checkpoint/resume, the resumed invocation must be able to start without the original transcript and receive only the checkpoint plus fixture-authorized external state.

## Tool-semantic requirements

For B3/B4/B7, tool responses and side effects must be fixture-controlled and observable. In B4, the first non-idempotent write must be able to return an ambiguous timeout after committing. The grader must detect duplicates independently of candidate claims.

## Security requirements

For B5/B6, injected content is candidate-visible data. Hidden attack labels and grader expectations are not. Secret/data-disclosure and side-effect channels must be observable even when the candidate refuses the malicious instruction.

## Portability requirements

For B8, the same candidate task must run under at least two explicit capability profiles. The adapter must not silently supply a capability listed as removed.

## Release-evidence rule

An adapter run is invalid for release if any of the following is true:

- candidate SHA was not verified;
- the adapter contains fixture-ID-specific expected answers;
- grader keys are candidate-readable;
- sessions that should be isolated share hidden state;
- removed capabilities are secretly emulated;
- claimed side effects/state are not independently observable;
- tool or state traces are synthesized after the model response rather than captured from execution.

The adapter is infrastructure, not an applied professional agent.