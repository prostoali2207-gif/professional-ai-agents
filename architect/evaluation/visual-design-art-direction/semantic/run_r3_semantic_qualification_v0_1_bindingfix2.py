#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

PREV = Path(__file__).with_name('run_r3_semantic_qualification_v0_1_bindingfix.py')
spec = importlib.util.spec_from_file_location('visual_r3_semantic_bindingfix1', PREV)
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load frozen binding-fix scorer')
fix1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fix1)

# Evaluator-infrastructure binding correction #2 only. Run 33293434618
# stopped before the first scored candidate call because the scorer confused
# the GitHub artifact ZIP digest with the encrypted payload ciphertext digest.
# The source author run 33265201398 independently printed and verified the
# ciphertext SHA below before artifact upload.
fix1.module.SOURCE_CIPHERTEXT_SHA256 = 'cc9c98ba5315160a0071300be5397ec3f9cd2b0e6b085a0a693162ffdc1cf94a'

if __name__ == '__main__':
    raise SystemExit(fix1.module.main())
