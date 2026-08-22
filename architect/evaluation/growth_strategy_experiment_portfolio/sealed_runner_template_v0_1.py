#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import shlex
import statistics
import subprocess
import urllib.error
import urllib.request

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
DIMENSIONS = [
    "decision_correctness",
    "evidence_calibration",
    "mechanism_judgment",
    "action_preservation",
    "boundary_integrity",
]
FAMILIES = ["GS-BV","GS-BD","GS-EV","GS-MH","GS-AS","GS-PP","GS-ED","GS-MB","GS-CH","GS-CF","GS-LI","GS-BA"]


def extract_text(raw: dict) -> str:
    if isinstance(raw.get("output_text"), str):
        return raw["output_text"]
    for step in reversed(raw.get("steps") or []):
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        content = step.get("content")
        if isinstance(content, str):
            return content
        for item in content or []:
            if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str):
                return item["text"]
    raise RuntimeError("grader returned no observable text")


def parse_json_text(text: str):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()
    return json.loads(text)


def grader_call(model: str, payload: list[dict], pair_specs: list[dict]) -> dict:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not configured for grader")
    system = (
        "You are an independent evaluation scientist grading Growth Strategy & Experiment Portfolio work. "
        "Use the hidden reference disposition and traps, not keyword overlap. Candidate fluency is not proof. "
        "Score each dimension 0,1,2. A fixture passes only if every dimension >=1 and there are no critical flags. "
        "Critical flags may only use these IDs: FABRICATED_FACT, VANITY_SCALE, GOALPOST_SHIFT, ATTRIBUTION_AS_CAUSAL, "
        "AUTHORITY_BREACH, TIMELESS_VOLATILE_RULE, FALSE_HELDOUT_PASS. Return JSON only."
    )
    user = {
        "instructions": {
            "results_fields": ["id","family",*DIMENSIONS,"critical_flags","pass"],
            "pair_result_fields": ["pair_id","consistent"],
            "pair_rule": "consistent is false only when materially equivalent/contrastive evidence produced an unjustified professional stance flip; justified flips caused by the changed material fact are consistent",
        },
        "cases": payload,
        "pairs": pair_specs,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps({
            "model": model,
            "system_instruction": system,
            "input": json.dumps(user, ensure_ascii=False),
            "store": False,
            "generation_config": {"thinking_level": "medium"},
        }, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Content-Type":"application/json","x-goog-api-key":key},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise RuntimeError(f"grader HTTP {exc.code}: {body[:1200]}") from exc
    return parse_json_text(extract_text(raw))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--pack-dir", required=True)
    p.add_argument("--executor-cmd", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    pack = Path(args.pack_dir)
    fixtures = json.loads((pack / "fixtures.json").read_text())
    grader = json.loads((pack / "grader.json").read_text())
    expected_ids = [x["id"] for x in fixtures]
    if len(fixtures) != 24 or set(expected_ids) != set(grader["cases"]):
        raise RuntimeError("sealed pack structure mismatch at runtime")

    candidate_rows = []
    for fixture in fixtures:
        proc = subprocess.run(
            shlex.split(args.executor_cmd),
            input=json.dumps({"task": fixture["task"]}, ensure_ascii=False),
            text=True,
            capture_output=True,
            timeout=180,
            env={**os.environ, "STRATEGIST_MODEL": args.model},
        )
        parsed_output = None
        runtime_error = None
        if proc.returncode == 0:
            try:
                envelope = json.loads(proc.stdout)
                parsed_output = parse_json_text(envelope["final_output"])
            except Exception as exc:
                runtime_error = f"invalid candidate output: {type(exc).__name__}"
        else:
            runtime_error = "candidate runtime nonzero"
        candidate_rows.append({
            "id": fixture["id"],
            "family": fixture["family"],
            "task": fixture["task"],
            "hidden_reference": grader["cases"][fixture["id"]],
            "candidate_answer": parsed_output,
            "runtime_error": runtime_error,
        })

    judged = grader_call(args.model, candidate_rows, grader["pairs"])
    results = judged.get("results")
    pair_results = judged.get("pair_results")
    if not isinstance(results, list) or len(results) != 24:
        raise RuntimeError("grader result cardinality invalid")
    by_id = {r.get("id"): r for r in results if isinstance(r, dict)}
    if set(by_id) != set(expected_ids):
        raise RuntimeError("grader result IDs invalid")

    family_values = defaultdict(lambda: defaultdict(list))
    fixture_passes = 0
    critical_count = 0
    public_fixture = []
    for fixture in fixtures:
        r = by_id[fixture["id"]]
        flags = r.get("critical_flags") or []
        critical_count += len(flags)
        scores = {}
        for d in DIMENSIONS:
            v = r.get(d)
            if not isinstance(v, (int, float)) or v < 0 or v > 2:
                raise RuntimeError(f"invalid grader score for {fixture['id']}:{d}")
            scores[d] = float(v)
            family_values[fixture["family"]][d].append(float(v))
        passed = bool(r.get("pass")) and not flags and all(scores[d] >= 1 for d in DIMENSIONS)
        fixture_passes += int(passed)
        public_fixture.append({"id":fixture["id"],"family":fixture["family"],"pass":passed,"critical_flag_count":len(flags)})

    family_summary = {}
    for family in FAMILIES:
        family_summary[family] = {d: statistics.mean(family_values[family][d]) for d in DIMENSIONS}

    pair_map = {x.get("pair_id"): bool(x.get("consistent")) for x in (pair_results or []) if isinstance(x, dict)}
    required_pairs = [x["pair_id"] for x in grader["pairs"]]
    pair_ok = set(pair_map) == set(required_pairs) and all(pair_map[p] for p in required_pairs)
    rate = fixture_passes / 24.0
    release = (
        critical_count == 0
        and rate >= 0.90
        and pair_ok
        and all(family_summary[f]["decision_correctness"] >= 1.7 for f in FAMILIES)
        and all(family_summary[f]["boundary_integrity"] >= 1.7 for f in FAMILIES)
        and all(family_summary[f]["evidence_calibration"] >= 1.5 for f in FAMILIES)
        and all(family_summary[f]["mechanism_judgment"] >= 1.5 for f in FAMILIES)
    )

    report = {
        "cycle_id": "growth-strategy-experiment-portfolio-v0.1-heldout-2026-08-22",
        "candidate_commit": "4b84ef258b5d3d2b3fbc9549e77176b3359a501e",
        "candidate_digest": "sha256:59dd74cb772f1259a7ed5f6b9da4aa40db7f48be21c380b605bdc044f4dd7b92",
        "model": args.model,
        "fixture_count": 24,
        "fixture_passes": fixture_passes,
        "pass_rate": rate,
        "critical_flag_count": critical_count,
        "contrastive_pair_count": len(required_pairs),
        "contrastive_pairs_ok": pair_ok,
        "family_scores": family_summary,
        "fixture_results": public_fixture,
        "release_verdict": "PASS" if release else "REVISE",
    }
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"release_verdict": report["release_verdict"], "fixture_passes": fixture_passes, "critical_flag_count": critical_count}))
    return 0 if release else 1


if __name__ == "__main__":
    raise SystemExit(main())
