#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('visual_heldout_author_v01',HERE/'author_sealed_heldout_v0_1.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
original_validate=mod.validate

def normalized_validate(cases):
    if not isinstance(cases,list) or len(cases)!=20:
        raise RuntimeError('heldout cardinality invalid')
    fam=Counter(x.get('family') for x in cases)
    if set(fam)!=set(mod.FAMILIES) or any(v!=2 for v in fam.values()):
        raise RuntimeError(f'family structure invalid {dict(fam)}')
    seen=Counter()
    for case in cases:
        family=case['family']; seen[family]+=1
        case['id']=f'{family}-{seen[family]:02d}'
        case['pair_id']=mod.PAIR_IDS.get(family)
    return original_validate(cases)

mod.validate=normalized_validate
if __name__=='__main__':
    mod.main()
