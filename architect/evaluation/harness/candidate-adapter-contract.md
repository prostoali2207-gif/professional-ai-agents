# Agent Architect Candidate Adapter Contract

Status: required to execute behavioral validation against a real Agent Architect runtime.

## Purpose

The harness must test the actual candidate behavior. A mock, scripted expected answer, or deterministic fixture-specific responder may be used only to test harness mechanics and can never count as Agent Architect release evidence.

The adapter is the narrow boundary between `runner.py` and the runtime that actually executes the candidate `architect/SKILL.md` at the frozen candidate SHA.

## Protocol v2 invocation

The harness invokes one command per fixture step and writes a JSON object to stdin. Steps from one trial share the same workspace so real persisted state/checkpoints can survive process/session boundaries. The adapter returns one JSON object on stdout.

Input fields include:

- `protocol_version = 2`;
- `operation` (`run`, `resume`, or a fixture-defined supported operation);
- `run_id` and `step_id`;
- `candidate_sha`;
- `family`, `priority`, and `trial`;
- `session_id`;
- `reset_session`;
- `capability_profile`;
- `input`;
- `workspace`.

The adapter must reject execution when it cannot establish that the loaded Agent Architect corresponds to `candidate_sha`.

## Required adapter responsibilities

1. **Candidate identity** — load the real Agent Architect candidate for the requested SHA and report the effective skill/runtime/model/tool versions.
2. **Session semantics** — preserve state only through explicit persistence boundaries. Different `session_id` values must not silently share transcript context. `reset_session=true` must start without prior session transcript.
3. **Observable state** — write inspectable state/checkpoints/tool traces into the supplied workspace when the family requires them.
4. **Capability profile enforcement** — deliberately remove unavailable capabilities for degradation tests rather than silently emulating them.
5. **Tool mediation** — expose only fixture-authorized tools/resources and preserve observable tool arguments/results/side effects.
6. **No hidden grader access** — never read grader keys, expected answers, sealed variants, or files outside the candidate-visible fixture surface.
7. **Termination record** — report why the candidate stopped, including success, escalation, unsupported configuration, or budget exhaustion.

## Minimum output

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

For B1/B2/B6, the adapter must expose a real persistence boundary that can be inspected independently of the model response. The store may be a file/database/service, but the grader must be able to query it before and after sessions. A prose field such as `memory = correct` is not persistence proof.

For B2, the resumed step must be able to execute under a new/reset session without receiving the original transcript; only the checkpoint and fixture-authorized external state may bridge the interruption.

## Tool-semantic requirements

For B3/B4/B7, tool responses and side effects must be fixture-controlled and observable. In B4, the first non-idempotent write must be able to return an ambiguous timeout after committing. The grader must detect duplicates independently of candidate claims.

## Security requirements

For B5/B6, injected content is candidate-visible data. Hidden attack labels and grader expectations are not. Secret/data-disclosure and side-effect channels must remain observable even when the candidate resists the malicious instruction.

## Portability requirements

For B8, fixture steps may override the base `capability_profile`. The same architecture task must run under full and deliberately degraded profiles. The adapter must not silently supply a capability listed as removed.

## Mechanical evidence

The runner may inspect JSON or other artifacts under `workspace`. Therefore adapter artifacts must reflect actual execution state, not values synthesized after reading the candidate's final prose. The runner may also grade nested structured output fields across steps.

## Release-evidence rule

An adapter run is invalid for release if any of the following is true:

- candidate SHA was not verified;
- the adapter contains fixture-ID-specific expected answers;
- grader keys are candidate-readable;
- sessions that should be isolated share hidden transcript/state;
- removed capabilities are secretly emulated;
- claimed side effects/state are not independently observable;
- tool or state traces are synthesized after the model response rather than captured from execution.

The adapter is infrastructure, not an applied professional agent.