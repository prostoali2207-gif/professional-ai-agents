# Manual cross-model exam package

Status: development/qualification support artifact.
Date: 2026-08-18.

## Purpose

Allow a frozen Analytics candidate to be exercised in a clean Claude, Gemini, ChatGPT, or other capable chat without requiring API access.

This is not fully automated qualification. It is a portable execution method for cross-model validation.

## Rules

1. Freeze the candidate instructions first. Record the exact source repository, path, ref/blob SHA, and a local digest if available.
2. Do not paste grader answers, expected decisions, hard-fail rules, or hidden qualification cases into the candidate chat.
3. Start a clean chat with no prior project discussion when possible.
4. Paste exactly the candidate instructions, execution prompt, output contract, and one fixture.
5. Ask for JSON only. Do not coach or correct the model mid-run.
6. Save the raw response unchanged.
7. Grade outside the candidate chat with `grader.py` or an independent reviewer using the separate answer key.
8. If the model asks for missing decision-critical facts, preserve that behavior; do not invent them.
9. Public development fixtures are not final held-out qualification evidence.
10. For a stronger cross-model check, run the same frozen candidate and same fixture on at least two independent model families and compare both against the same deterministic grader.

## Copy/paste execution prompt

Use this block AFTER the frozen Analytics instructions and BEFORE the fixture:

---

You are executing a frozen Analytics candidate under evaluation.

Evaluate exactly one experiment fixture using only the candidate instructions and the facts inside the fixture.

Do not use outside assumptions to fill missing business or experiment facts. Do not change the declared KPI, threshold, population, denominator, test window, or decision rule after seeing results.

Return JSON only with this shape:

{
  "fixture_id": "string",
  "recommendation": "CONTINUE | ITERATE | SCALE | KILL | INCONCLUSIVE",
  "data_integrity_findings": ["string"],
  "computations": [
    {
      "name": "string",
      "inputs": {"key": "value"},
      "method": "string",
      "result": "number or string",
      "unit": "string or null"
    }
  ],
  "claim_boundaries": ["string"],
  "confounders": [
    {
      "name": "string",
      "severity": "NONE_OBSERVED | LOW | MATERIAL | FATAL",
      "effect": "string"
    }
  ],
  "rationale": "string",
  "next_action": "string"
}

Do not include Markdown fences or prose outside the JSON object.

---

## What the user does manually

For a manual Claude/Gemini run:

1. Open a new clean chat.
2. Paste the frozen Analytics instructions.
3. Paste the execution prompt above.
4. Paste ONE fixture with no expected answer.
5. Copy the raw JSON response back to the grader/reviewer.

The user should not need to understand the statistical answer key.

## What must remain separate

Never include in the candidate chat:
- `development-fixtures-v0.1.md` sections labelled Expected behavior / Hard fail if those exact same fixtures are being used;
- sealed held-out answer keys;
- grader implementation details that reveal expected labels;
- previous failed attempts and corrections for the same held-out case.

For public development fixtures, exposure to expected answers makes the run useful only for debugging, not qualification.

## Recommended cross-model protocol

Development:
- use public fixtures;
- iterate freely;
- Claude/Gemini/ChatGPT runs can expose weaknesses but do not certify the candidate.

Qualification:
- freeze candidate;
- create fresh sealed cases after freeze;
- keep answer key separate;
- run the exact same candidate package in clean independent chats;
- capture raw outputs and model/version/date;
- grade with deterministic rules first;
- count a PASS only if required critical competencies pass without hard-fail behavior.

## Important limitation

A manual chat run is less reproducible than an API run because model versions, hidden system instructions, chat product behavior, and sampling may differ. Cross-model agreement is useful evidence, but it is not proof by itself. A later API/runtime-backed run can provide stronger reproducibility if needed.