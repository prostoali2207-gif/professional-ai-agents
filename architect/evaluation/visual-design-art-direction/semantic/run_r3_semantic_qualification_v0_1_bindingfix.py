#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

BASE = Path(__file__).with_name('run_r3_semantic_qualification_v0_1.py')
spec = importlib.util.spec_from_file_location('visual_r3_semantic_frozen', BASE)
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load frozen semantic runner')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Evaluator-infrastructure binding correction only. Run 33293275507 proved the
# previously recorded payload hash was wrong before credentials/candidate calls.
# Scoring, judges, thresholds, P0, R3 corpus and runtime remain byte-identical.
module.R3_CALIBRATION_REPORT_SHA256 = '56136e59e216da4a773a943d7dcc30c9d045b2d899165cb68e2060283ea11131'

if __name__ == '__main__':
    raise SystemExit(module.main())
