from __future__ import annotations
import json, pathlib, sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
base = root / "architect/evaluation/training-recovery-fatigue-management"
schema = json.loads((base / "candidate/state.schema.json").read_text(encoding="utf-8"))
fx = json.loads((base / "stateful-practical-fixtures-v0.1.json").read_text(encoding="utf-8"))

obs_props = schema["properties"]["observations"]["items"]["properties"]
assert "sleep_start" in obs_props and "sleep_end" in obs_props, "sleep timing fields must be explicit"

session_exercises = schema["properties"]["sessions"]["items"]["properties"]["exercises"]
assert session_exercises.get("items", {}).get("type") == "object", "exercise entries must be structured"
exercise_props = session_exercises["items"]["properties"]
for key in ["exercise", "variant", "order", "sets"]:
    assert key in exercise_props, f"exercise schema missing {key}"

anchor = schema["properties"]["performance_anchors"]["items"]
assert "anchor_id" in anchor["properties"], "performance anchors need stable ids for compaction/restart"

load_history = schema["properties"]["load_history"]
assert load_history.get("items", {}).get("type") == "object", "load history must be structured"
for key in ["week_start", "hard_sets_by_muscle", "frequency_by_muscle", "failure_sets", "notable_changes"]:
    assert key in load_history["items"]["properties"], f"load history missing {key}"

try:
    import jsonschema
except Exception as exc:
    raise SystemExit(f"NOT_EXECUTABLE jsonschema unavailable: {exc}")
jsonschema.Draft202012Validator(schema).validate(fx["full_state"])
jsonschema.Draft202012Validator(schema).validate(fx["compacted_state"])

comp = fx["compacted_state"]
assert set(fx["must_preserve"]["performance_anchor_ids"]) <= {x["anchor_id"] for x in comp["performance_anchors"]}
assert set(fx["must_preserve"]["intervention_ids"]) <= {x["intervention_id"] for x in comp["interventions"]}
assert set(fx["must_preserve"]["load_week_starts"]) <= {x["week_start"] for x in comp["load_history"]}

print("TRFM_STATEFUL_PRACTICAL_PASS")
print("state_schema_validation=PASS")
print("compaction_preservation=PASS")
print("provider_calls=0")
print("qualification_claim=false")
