#!/usr/bin/env python3
"""Zero-model regression for held-out pair-structure repair."""
from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("author_sealed_pack_v0_1.py")
spec = importlib.util.spec_from_file_location("messaging_author", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def case(case_id: str, family: str, pair_id=None):
    return {
        "id": case_id,
        "family": family,
        "pair_id": pair_id,
        "task": "Synthetic structural regression only.",
        "context": {},
        "constraints": [],
        "hidden_reference": {},
    }


def build_valid_family_shape():
    cases = []
    for family in module.FAMILIES:
        cases.append(case(f"{family}-A", family, "WRONG"))
        cases.append(case(f"{family}-B", family, None))
    return cases


def main():
    cases = build_valid_family_shape()
    module.validate(cases, require_pair_structure=False)
    repaired = module.canonicalize_pair_ids(cases)
    module.validate(repaired, require_pair_structure=True)

    for item in repaired:
        expected = module.FAMILY_PAIRS.get(item["family"])
        assert item["pair_id"] == expected

    broken = repaired[:-1]
    try:
        module.validate(broken, require_pair_structure=False)
    except RuntimeError:
        pass
    else:
        raise AssertionError("cardinality drift must fail closed")

    print("PASS: messaging author pair-structure regression; model_calls=0")


if __name__ == "__main__":
    main()
