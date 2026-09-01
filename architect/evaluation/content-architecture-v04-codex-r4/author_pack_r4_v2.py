#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

BASE = Path(__file__).with_name("author_pack_r4.py")
spec = importlib.util.spec_from_file_location("author_pack_r4_base", BASE)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

# Pre-score construct tightening. No candidate/scored r4 call existed when this wrapper was authored.
# F6: only PROOF_TIMING is open, so changing any locked dimension must not pass.
for c in base.CASES:
    if c["family"] == "F6" and c.get("repeat"):
        c["expect"].pop("changed_dimensions_contains", None)
        c["expect"]["changed_dimensions_exact"] = ["PROOF_TIMING"]

# F9: make metric-threshold exclusion an explicit visible decision rather than permitting a
# forbidden metadata member that a contains-only check could accidentally tolerate.
for c in base.CASES:
    if c["family"] == "F9" and "metadata_fields" in c["contract"]:
        c["contract"]["metadata_fields"]["allowed_items"] = [
            "ARCHITECTURE_ID", "HOOK_FAMILY", "BLOCK_ORDER", "PROOF_POSITION", "TESTED_VARIABLES"
        ]
        c["contract"]["metric_threshold_action"] = base.S("EXCLUDE", "INCLUDE")
        c["expect"]["metric_threshold_action"] = ["EXCLUDE"]

if __name__ == "__main__":
    base.main()
