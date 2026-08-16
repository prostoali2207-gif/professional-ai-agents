from pathlib import Path
import json, unittest
ROOT=Path(__file__).resolve().parents[3]
CTX=ROOT/'architect/specializations/showroom-171-dealership/2026-08/business-context.md'
EVIDENCE=ROOT/'architect/specializations/showroom-171-dealership/2026-08/evidence.md'
CASES=Path(__file__).resolve().parent/'semantic_cases.json'

class DealerContract(unittest.TestCase):
    def setUp(self):
        self.ctx=CTX.read_text(); self.evidence=EVIDENCE.read_text(); self.cases=json.loads(CASES.read_text())
    def test_parent_layers(self):
        for x in ['paid-media-performance-marketing@1.0.0','automotive-paid-media@1.0.0','uae-meta-whatsapp-automotive/2026-08']:
            self.assertIn(x,self.ctx)
    def test_dealership_identity_and_scope(self):
        for x in ['Ajman Auto Market','Showroom 171','Instagram','WhatsApp','No Toyota Yaris campaign']:
            self.assertIn(x.lower(),self.ctx.lower())
    def test_unknowns_not_invented(self):
        for x in ['gross/contribution economics','paid-media budget','spend authority','sales-team response/capacity','authoritative live inventory integration']:
            self.assertIn(x.lower(),self.ctx.lower())
    def test_scale_requires_explicit_capacity_check(self):
        self.assertIn('Before any `SCALE` decision expected to increase lead volume, explicitly confirm',self.ctx)
    def test_cross_repo_exact_revision(self):
        self.assertIn('5f0a7fdbc83f48d207499229dfbc3110e675b4da',self.evidence)
        self.assertIn('No code, prompt, agent instruction or professional artifact is imported',self.evidence)
    def test_cases_complete_balanced(self):
        self.assertEqual([f'D-S{i}' for i in range(1,11)],[c['id'] for c in self.cases])
        self.assertTrue(any(c['allowed_actions']==['SCALE'] for c in self.cases))
        self.assertTrue(any('SCALE' in c['forbidden_actions'] for c in self.cases))
        for c in self.cases: self.assertTrue(c['required_flags'])
    def test_construct_isolation(self):
        by={c['id']:c for c in self.cases}
        self.assertEqual(['downstream_quality_required'],by['D-S1']['required_flags'])
        self.assertEqual(['missing_data_not_zero'],by['D-S8']['required_flags'])
    def test_positive_scale_requires_business_evidence(self):
        c={x['id']:x for x in self.cases}['D-S7']
        self.assertEqual(['SCALE'],c['allowed_actions'])
        for f in ['marginal_business_value','authority_respected','capacity_verified']:
            self.assertIn(f,c['required_flags'])
    def test_measurement_unknown_not_zero(self):
        c={x['id']:x for x in self.cases}['D-S8']
        self.assertIn('missing_data_not_zero',c['required_flags'])
        self.assertIn('STOP',c['forbidden_actions'])

if __name__=='__main__': unittest.main()