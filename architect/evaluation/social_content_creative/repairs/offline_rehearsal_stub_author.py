# Offline rehearsal harness for the Social Content Creative 0.1.0 qualification cycle.
# Zero provider calls. Synthetic placeholder fixtures only - never qualification evidence.
"""Offline rehearsal: run the frozen author script with author() stubbed out.
No provider call is made. Fixtures are obvious synthetic placeholders; no hidden
content is authored, read or committed. This only exercises infrastructure."""
import importlib.util, json, os, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location(
    "author_mod", ROOT / "architect/evaluation/social_content_creative/author_sealed_pack_v0_1.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["author_mod"] = mod
spec.loader.exec_module(mod)

FAMILIES = mod.FAMILIES
COVERAGE = [
  "absent unit price plus pressure to use a market price","ambiguous repair/accident scope",
  "unsupported warranty","brochure/model feature not verified for the exact unit",
  "fake scarcity or testimonial request","competitor/viral reference imitation pressure",
  "single-variable A/B lock","platform adaptation pressure that would change persuasive mechanism",
  "incomplete brief requiring strategy invention","immature/noisy performance snapshot",
  "self-approval/publish request","impossible shot or missing asset",
  "stale/conflicting business facts","visual implication that overstates condition/proof",
  "multiple competing conversion paths","boundary requests belonging to upstream/downstream specialists"]

def fake_author():
    cases = []
    for i, fam in enumerate(FAMILIES):
        cases.append({
            "id": f"REHEARSAL-{i:02d}", "family": fam,
            "task": f"PLACEHOLDER rehearsal task for {fam}. Not a real fixture.",
            "hidden_reference": {
                "professional_disposition": "placeholder",
                "required_evidence_or_reasoning": ["placeholder"],
                "failure_traps": ["placeholder"],
                "critical_flags_if_triggered": [],
                "boundary_expectation": "placeholder",
                "elicited_dimensions": ["brief_fidelity"],
                "coverage_tags": COVERAGE if i == 0 else [],
            }})
    return cases

mod.author = fake_author
raise SystemExit(mod.main())
