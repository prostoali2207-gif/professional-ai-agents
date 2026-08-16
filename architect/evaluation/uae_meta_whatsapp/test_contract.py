from pathlib import Path
import json, unittest
ROOT=Path(__file__).resolve().parents[3]
LIVE=ROOT/'architect/specializations/uae-meta-whatsapp-automotive/2026-08/live-context.md'
EVIDENCE=ROOT/'architect/specializations/uae-meta-whatsapp-automotive/2026-08/evidence.md'
CASES=Path(__file__).resolve().parent/'semantic_cases.json'

class LiveContextContract(unittest.TestCase):
    def setUp(self):
        self.live=LIVE.read_text(); self.evidence=EVIDENCE.read_text(); self.cases=json.loads(CASES.read_text())
    def test_parent_layers(self):
        self.assertIn('paid-media-performance-marketing@1.0.0',self.live.lower())
        self.assertIn('automotive-paid-media@1.0.0',self.live.lower())
    def test_live_not_durable(self):
        for x in ['Snapshot date: 2026-08-16','reverified','Revalidation triggers','live account']:
            self.assertIn(x.lower(),self.live.lower())
    def test_scope_exclusions(self):
        for x in ['No named dealership','no exact budget','no Toyota/Yaris rules','no launch campaign']:
            self.assertIn(x.lower(),self.live.lower())
    def test_uae_boundaries(self):
        self.assertIn('Federal Decree-Law No. 45 of 2021',self.live)
        self.assertIn('Cabinet Resolution No. 56 of 2024',self.live)
        self.assertIn('DNCR',self.live)
        self.assertIn('09:00–18:00',self.live)
    def test_platform_constructs(self):
        for x in ['Special Ad Category','Advantage+','vehicle inventory','Conversions API','click to WhatsApp']:
            self.assertIn(x.lower(),self.live.lower())
    def test_cases_complete_and_balanced(self):
        self.assertEqual([f'LIVE-S{i}' for i in range(1,11)],[c['id'] for c in self.cases])
        self.assertTrue(any(c['allowed_actions']==['SCALE'] for c in self.cases))
        self.assertTrue(any('SCALE' in c['forbidden_actions'] for c in self.cases))
        for c in self.cases: self.assertTrue(c['required_flags'])
    def test_construct_isolation_repairs(self):
        by={c['id']:c for c in self.cases}
        self.assertEqual(['data_use_lawful_basis'],by['LIVE-S3']['required_flags'])
        self.assertIn('STOP',by['LIVE-S5']['allowed_actions'])
        self.assertIn('SCALE',by['LIVE-S5']['forbidden_actions'])
    def test_no_third_party_import(self):
        self.assertIn('No third-party code, prompt, agent, or professional artifact is imported',self.evidence)
    def test_whatsapp_volatile_rules_not_frozen(self):
        self.assertIn('were not frozen as durable rules',self.evidence)
        self.assertIn('live official verification',self.evidence)

if __name__=='__main__': unittest.main()