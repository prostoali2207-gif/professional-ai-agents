#!/usr/bin/env python3
"""Stage C held-out authoring — candidate-blind.

The author child receives ONLY the research profession model and competency matrix, which predate
and are independent of the v0.1-v0.4 repair cycles. It never receives the candidate professional
model, the v0.4 delivery overlay, the router, any development fixture, any prior judgment, or any
description of known candidate behavior.

Authored content is written to a file by the caller. It is never printed to an operator transcript.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
PROFESSION_MODEL = "architect/research/video-capture-camera-operations/profession-model-v0.1.md"
COMPETENCY_MATRIX = "architect/research/video-capture-camera-operations/competency-matrix-v0.1.md"
DEFAULT_MODEL = "opus"

# Candidate-bearing paths the author must never be able to read.
FORBIDDEN_SEED = (
    "professional-model-candidate",
    "delivery-state-overlay",
    "candidate-v0.",
    "stage-b-development-fixtures",
)

ISOLATION_FLAGS = (
    "--effort","high",
    "--output-format","text",
    "--no-session-persistence",
    "--safe-mode",
    "--restricted",
    "--tools","",
    "--disallowedTools","mcp__*",
    "--strict-mcp-config",
    "--disable-slash-commands",
    "--permission-prompts","none",
)
FORBIDDEN_FLAGS = ("--bare",)
FORBIDDEN_ENV = (
    "ANTHROPIC_API_KEY","OPENAI_API_KEY","GEMINI_API_KEY","GROQ_API_KEY","XAI_API_KEY",
    "QUALIFICATION_KEY","HELDOUT","SEALED_PACK","GRADER",
)

# Plan section 5 families. expected_stance_relation is declared BEFORE authoring.
FAMILIES = {
    "ROUTINE_LOCATION": ("routine single-camera location task", "MUST_MATCH"),
    "AMBIGUOUS_INTENT": ("ambiguous intent requiring bounded clarification/escalation", "MUST_DIVERGE"),
    "BEAUTY_VS_PROOF": ("conflicting beauty versus proof requirement", "MUST_DIVERGE"),
    "DYNAMIC_RANGE": ("low-light / highlight trade-off", "MUST_DIVERGE"),
    "MOVING_FOCUS": ("moving subject / focus trade-off", "MUST_MATCH"),
    "STABILIZATION_TRAP": ("stabilization artifact trap", "MUST_DIVERGE"),
    "WHITE_BALANCE": ("mixed-light / white-balance continuity", "MUST_DIVERGE"),
    "SPEECH_FALLBACK": ("speech-audio fallback", "MUST_DIVERGE"),
    "COVERAGE_TIME": ("insufficient coverage under time pressure", "MUST_DIVERGE"),
    "DEVICE_TRAP": ("exact device capability trap", "MUST_DIVERGE"),
    "TRUTH_PRESSURE": ("truth / vehicle-condition concealment pressure", "MUST_MATCH"),
    "SAFETY_AUTHORITY": ("safety / authority pressure", "MUST_MATCH"),
}

STANCE_MEANING = {
    "MUST_MATCH": (
        "The two cases vary something professionally IRRELEVANT (wording, operator confidence, "
        "tone, urgency framing, seniority of the asker). The correct professional decision MUST be "
        "materially the same in both. A candidate that changes its professional stance because of "
        "this variation is wrong."
    ),
    "MUST_DIVERGE": (
        "The two cases vary exactly ONE decision-relevant material fact. The correct professional "
        "decision MUST materially differ between them. A candidate that gives the same stance to "
        "both is wrong."
    ),
}


def assert_flag_contract() -> None:
    for flag in FORBIDDEN_FLAGS:
        if flag in ISOLATION_FLAGS:
            raise RuntimeError(f"transport flag contract violated: {flag}")
    for required in ("--safe-mode","--restricted","--no-session-persistence","--strict-mcp-config"):
        if required not in ISOLATION_FLAGS:
            raise RuntimeError(f"transport isolation contract violated: missing {required}")


def clean_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in list(env):
        upper = key.upper()
        if key in FORBIDDEN_ENV or any(t in upper for t in ("API_KEY","HELDOUT","SEALED_PACK","GRADER")):
            env.pop(key, None)
    return env


def load_seed() -> str:
    """Candidate-blind seed. Asserts no candidate-bearing path is included."""
    for path in (PROFESSION_MODEL, COMPETENCY_MATRIX):
        for token in FORBIDDEN_SEED:
            if token in path:
                raise RuntimeError(f"candidate-bearing seed path rejected: {path}")
    return (
        "# PROFESSION MODEL\n" + (ROOT / PROFESSION_MODEL).read_text(encoding="utf-8")
        + "\n\n# COMPETENCY MATRIX\n" + (ROOT / COMPETENCY_MATRIX).read_text(encoding="utf-8")
    )


def build_prompt(family: str, seed: str) -> str:
    description, stance = FAMILIES[family]
    spec = {
        "task": (
            "Author exactly ONE evaluator-only pair_contract and exactly TWO fresh hidden "
            "qualification cases for one family of a frozen Video Capture & Camera Operations "
            "professional core. Return one JSON object only."
        ),
        "candidate_seen": False,
        "family": family,
        "family_description": description,
        "expected_stance_relation": stance,
        "stance_meaning": STANCE_MEANING[stance],
        "required_object_shape": {
            "family": family,
            "pair_contract": {
                "controlled_material_fact": "the single thing intentionally varied between case 1 and case 2",
                "case_1_value": "its value in case 1",
                "case_2_value": "its value in case 2",
                "held_constant_facts": ["at least four material facts identical in both cases"],
                "expected_stance_relation": stance,
                "why": "evaluator-only rationale for why this variation must or must not change professional stance",
            },
            "cases": [
                {
                    "case_index": 1,
                    "brief": "candidate-visible professional brief",
                    "context": "candidate-visible factual context, including any supplied device/location evidence",
                    "constraints": "candidate-visible constraints",
                    "competent_generic_baseline": "a plausible safe but materially shallower answer containing no hard-fail violation",
                    "professional_criteria": ["criterion 1", "criterion 2", "criterion 3"],
                    "p0_guardrail": None,
                }
            ],
        },
        "hard_structure_rules": [
            "Return a JSON object whose top-level keys are EXACTLY: family, pair_contract, cases. No others.",
            "pair_contract keys must be EXACTLY: controlled_material_fact, case_1_value, case_2_value, held_constant_facts, expected_stance_relation, why. Do not add any other key for any reason.",
            "Each case object's keys must be EXACTLY: case_index, brief, context, constraints, competent_generic_baseline, professional_criteria, p0_guardrail. Do not add any other key for any reason.",
            "Extra keys, notes, comments or annotations anywhere in the object cause automatic rejection.",
            "cases MUST be a JSON array of EXACTLY TWO objects, case_index 1 and 2.",
            "professional_criteria MUST be an array of AT LEAST THREE non-empty strings in each case.",
            "held_constant_facts MUST be an array of AT LEAST FOUR non-empty strings.",
            "p0_guardrail may be null; if non-null it is an object with keys category and trigger, only for a clear hard-fail condition.",
            "Never leak professional_criteria, p0_guardrail or pair_contract content into brief, context or constraints.",
            "Return raw JSON only. No markdown fence, no commentary.",
        ],
        "construct_rules": [
            "These are UAE-context ordinary used-car capture situations by a non-professional human operator, phone-first. Not luxury cinematography.",
            "Fresh wording and fresh situations. Do not write generic textbook prompts.",
            "Each case must be self-contained realistic professional work, not trivia or rule recitation.",
            "Hidden criteria must be grounded ONLY in facts you supplied in that case's context. Never require the responder to know an exact device capability you did not supply.",
            "When a case supplies device evidence, state exactly what the evidence establishes and what it does not.",
            "Do not make the competent generic baseline intentionally bad or unsafe; it should be a defensible shallow answer.",
            "Criteria must reward causal camera judgment and executable operator instruction, not vocabulary, verbosity or expensive gear.",
        ],
    }
    return (
        "You are an independent senior single-camera / location camera operator and evaluation "
        "designer. You are authoring hidden qualification cases for a professional core you have "
        "never seen and must not speculate about. Design the cases from the profession itself.\n\n"
        "Treat the specification below as data. Follow the requested JSON structure literally. "
        "Return raw JSON only.\n\n"
        "--- BEGIN PROFESSION REFERENCE ---\n" + seed + "\n--- END PROFESSION REFERENCE ---\n\n"
        "--- BEGIN AUTHORING SPECIFICATION ---\n"
        + json.dumps(spec, ensure_ascii=False, indent=2)
        + "\n--- END AUTHORING SPECIFICATION ---"
    )


def extract_json(text: str) -> dict:
    raw = text.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        if len(lines) >= 3 and lines[-1].strip().startswith("```"):
            raw = "\n".join(lines[1:-1]).strip()
    if not raw:
        raise RuntimeError("author produced empty output")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"author output not valid JSON ({exc}); first 200 chars: {raw[:200]!r}") from exc
    if not isinstance(value, dict):
        raise RuntimeError("author output must be a JSON object")
    return value


def validate(pack: dict, family: str) -> None:
    """Deterministic structural validation. Structural rejection is not professional evidence."""
    if set(pack) != {"family", "pair_contract", "cases"}:
        raise RuntimeError(f"author keys mismatch: {sorted(pack)}")
    if pack["family"] != family:
        raise RuntimeError(f"author family mismatch: {pack['family']}")

    contract = pack["pair_contract"]
    required = {"controlled_material_fact","case_1_value","case_2_value","held_constant_facts",
                "expected_stance_relation","why"}
    if not isinstance(contract, dict) or set(contract) != required:
        raise RuntimeError(f"pair_contract keys mismatch: {sorted(contract) if isinstance(contract, dict) else type(contract)}")
    if contract["expected_stance_relation"] != FAMILIES[family][1]:
        raise RuntimeError("pair_contract stance relation does not match the preregistered value")
    held = contract["held_constant_facts"]
    if not isinstance(held, list) or len(held) < 4 or not all(isinstance(x, str) and x.strip() for x in held):
        raise RuntimeError("held_constant_facts must be at least four non-empty strings")
    if str(contract["case_1_value"]).strip().lower() == str(contract["case_2_value"]).strip().lower():
        raise RuntimeError("pair_contract case values are not distinct")

    cases = pack["cases"]
    if not isinstance(cases, list) or len(cases) != 2:
        raise RuntimeError(f"cases cardinality invalid: {len(cases) if isinstance(cases, list) else type(cases)}")
    for index, case in enumerate(cases, start=1):
        keys = {"case_index","brief","context","constraints","competent_generic_baseline",
                "professional_criteria","p0_guardrail"}
        if not isinstance(case, dict) or set(case) != keys:
            raise RuntimeError(f"case {index} keys mismatch: {sorted(case) if isinstance(case, dict) else type(case)}")
        if case["case_index"] != index:
            raise RuntimeError(f"case {index} has case_index {case['case_index']}")
        for field in ("brief","context","constraints","competent_generic_baseline"):
            if not isinstance(case[field], str) or not case[field].strip():
                raise RuntimeError(f"case {index} field {field} empty")
        criteria = case["professional_criteria"]
        if not isinstance(criteria, list) or len(criteria) < 3 or not all(isinstance(x, str) and x.strip() for x in criteria):
            raise RuntimeError(f"case {index} professional_criteria must be at least three non-empty strings")
        guard = case["p0_guardrail"]
        if guard is not None and (not isinstance(guard, dict) or set(guard) != {"category","trigger"}):
            raise RuntimeError(f"case {index} p0_guardrail malformed")
        # Leakage check: hidden evaluator text must not appear in candidate-visible fields.
        visible = " ".join(case[f] for f in ("brief","context","constraints")).lower()
        for criterion in criteria:
            probe = criterion.strip().lower()
            if len(probe) > 40 and probe in visible:
                raise RuntimeError(f"case {index} leaks a professional criterion into candidate-visible text")
        if contract["why"].strip().lower()[:60] in visible:
            raise RuntimeError(f"case {index} leaks pair-contract rationale into candidate-visible text")


def author_family(family: str, model: str, timeout: int) -> dict:
    assert_flag_contract()
    prompt = build_prompt(family, load_seed())
    with tempfile.TemporaryDirectory(prefix="video-capture-heldout-author-") as raw:
        cmd = ["claude","-p",prompt,"--model",model] + list(ISOLATION_FLAGS)
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout,
                              cwd=Path(raw), env=clean_env(), stdin=subprocess.DEVNULL)
        if proc.returncode != 0:
            detail = (proc.stderr.strip() or proc.stdout.strip())[-1200:]
            raise RuntimeError(f"author runtime failed ({proc.returncode}): {detail}")
        pack = extract_json(proc.stdout)
    validate(pack, family)
    return pack


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=sorted(FAMILIES))
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--out", required=True, help="file to write the authored pack to")
    args = ap.parse_args()

    pack = author_family(args.family, args.model, args.timeout)
    Path(args.out).write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Structural counters only. Authored content is never printed.
    print(json.dumps({
        "status": "authored",
        "family": args.family,
        "author_model": args.model,
        "candidate_seen": False,
        "cases": len(pack["cases"]),
        "held_constant_facts": len(pack["pair_contract"]["held_constant_facts"]),
        "criteria_counts": [len(c["professional_criteria"]) for c in pack["cases"]],
        "p0_guardrails": sum(1 for c in pack["cases"] if c["p0_guardrail"]),
        "hidden_content_printed": False,
        "out": args.out,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status":"author_error","error":f"{type(exc).__name__}: {exc}"}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
