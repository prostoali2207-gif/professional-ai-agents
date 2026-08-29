#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, os, urllib.request
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('visual_heldout_author_v01',HERE/'author_sealed_heldout_v0_1.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

PAIR_REQUIREMENTS={
 'REFERENCE':'The two cases form one contrastive pair: imitation pressure versus mechanism extraction with broad evidence.',
 'MOBILE':'The two cases form one contrastive pair: collapsed-desktop failure versus an already authored narrow composition that should not be reset ceremonially.',
 'TRUTH':'The two cases form one contrastive pair: missing proof versus verified supplied proof that should be used confidently.',
 'ADVANCED_MEDIA_ROUTING':'The two cases form one contrastive pair: ornamental 3D versus materially explanatory spatial/assembly value.',
 'AUTHORITY_BOUNDARY':'The two cases form one contrastive pair: visual decision inside authority versus requested CRO/product logic change outside authority.',
}

def author_family(family):
    key=os.environ.get('GEMINI_API_KEY','').strip()
    if not key: raise RuntimeError('GEMINI_API_KEY missing')
    prompt={
      'task':'Author exactly TWO fresh hidden qualification cases for one frozen landing-page Visual Design / Art Direction professional-core family. Return a JSON array of exactly two objects only.',
      'candidate_seen':False,
      'family':family,
      'pair_requirement':PAIR_REQUIREMENTS.get(family,'These are two distinct unseen cases in the same professional family; they need not be a contrastive pair.'),
      'required_object_shape':{
        'id':'any non-empty placeholder string; evaluator canonicalizes structural ID only',
        'family':family,
        'pair_id':'any placeholder or null; evaluator canonicalizes preregistered structural pair_id only',
        'brief':'non-empty candidate-visible professional brief',
        'context':'non-empty candidate-visible factual context',
        'constraints':'non-empty candidate-visible constraints',
        'competent_generic_baseline':'non-empty plausible safe generic answer, materially shallower than strong professional work and containing no P0 violation',
        'professional_criteria':['criterion string 1','criterion string 2','criterion string 3'],
        'p0_guardrail':None,
      },
      'hard_structure_rules':[
        'professional_criteria MUST be a JSON array of AT LEAST THREE non-empty strings; never return an object, prose paragraph, or keyed rubric there.',
        'Every required field must be present in both objects.',
        'Both objects must have family exactly equal to the requested family.',
        'Do not leak professional_criteria or p0_guardrail content into brief/context/constraints.',
        'p0_guardrail may be null. If non-null it must be an object with category and trigger, and only for a clear preregistered hard-fail condition.',
      ],
      'construct_rules':[
        'Fresh wording and situation; do not copy public development fixtures.',
        'Self-contained realistic professional work, not trivia or rule recitation.',
        'Hidden criteria must be grounded only in supplied candidate-visible facts and require causal art-direction judgment rather than preferred style.',
        'Do not make the competent generic baseline intentionally bad or unsafe.',
      ]
    }
    body={'model':mod.GEMINI_MODEL,'system_instruction':'You are an independent senior landing-page art director and evaluation designer. Follow the requested JSON structure literally. Return JSON only.','input':json.dumps(prompt,ensure_ascii=False),'store':False,'generation_config':{'thinking_level':'medium'}}
    req=urllib.request.Request(mod.GEMINI,data=json.dumps(body,ensure_ascii=False).encode(),method='POST',headers={'x-goog-api-key':key,'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=240) as r:
        cases=mod.parse(mod.gtext(json.loads(r.read().decode())))
    if not isinstance(cases,list) or len(cases)!=2: raise RuntimeError(f'author contract cardinality invalid for {family}')
    for case in cases:
        case['family']=family
        criteria=case.get('professional_criteria')
        if not isinstance(criteria,list) or len(criteria)<3 or not all(isinstance(x,str) and x.strip() for x in criteria):
            raise RuntimeError(f'author contract professional_criteria invalid for {family}')
    return cases

def contract_author():
    cases=[]
    for family in mod.FAMILIES:
        cases.extend(author_family(family))
    seen={}
    for case in cases:
        family=case['family']; seen[family]=seen.get(family,0)+1
        case['id']=f'{family}-{seen[family]:02d}'
        case['pair_id']=mod.PAIR_IDS.get(family)
    return mod.validate(cases)

mod.author=contract_author
if __name__=='__main__':
    mod.main()
