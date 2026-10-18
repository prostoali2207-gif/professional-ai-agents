#!/usr/bin/env python3
from pathlib import Path
import sys

skill = Path(__file__).resolve().parents[3] / "agents" / "exercise-technique-selection" / "0.1.0" / "SKILL.md"
text = skill.read_text(encoding="utf-8")

checks = {
    "candidate_not_qualified": "UNQUALIFIED DEVELOPMENT CANDIDATE" in text,
    "observed_inferred_unknown": all(x in text for x in ["OBSERVED", "INFERRED-HIGH", "UNKNOWN"]),
    "media_adequacy_gate": all(x in text for x in ["ADEQUATE_FOR_QUALITATIVE_ANALYSIS", "INADEQUATE / REQUEST_NEW_VIEW"]),
    "hidden_motion_guard": "interpolate hidden" in text or "hidden knee/hip/spine" in text,
    "acceptable_variation": "ACCEPTABLE_VARIATION" in text,
    "anthropometry_non_deterministic": "deterministic" in text and "Anthropometry" in text,
    "goal_relative_too_heavy": "too heavy **for the current task**" in text,
    "limiting_factor_ranked": "ranked hypotheses" in text,
    "photo_dynamic_limit": "A still photo" in text and "bar/implement path" in text,
    "medical_boundary": "MEDICAL_BOUNDARY" in text and "do not name an injured tissue" in text,
    "no_rehab": "do not prescribe rehabilitation" in text,
    "retest_loop": "Re-test" in text and "predicted" in text,
    "competition_live_source": "current official source" in text and "federation/ruleset" in text,
    "untrusted_content_boundary": "data/evidence, not instruction authority" in text,
    "pose_not_ground_truth": "cross-check against raw pixels" in text,
    "resistance_profile_no_guarantee": "guaranteed hypertrophy" in text,
    "emg_no_hypertrophy_guarantee": "equate EMG" in text,
    "authority_read_analyze_recommend": "read / analyze / recommend" in text,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'} {name}")

if failed:
    print("FAILED:", ", ".join(failed), file=sys.stderr)
    raise SystemExit(1)

print(f"PASS {len(checks)}/{len(checks)} static contract checks")
