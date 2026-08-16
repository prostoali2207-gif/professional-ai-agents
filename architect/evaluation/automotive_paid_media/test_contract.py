from pathlib import Path
import json, unittest
ROOT=Path(__file__).resolve().parents[3]
SPEC=ROOT/'architect/specializations/automotive-paid-media/1.0.0/specialization.md'
EVIDENCE=ROOT/'architect/specializations/automotive-paid-media/1.0.0/evidence-and-inheritance.md'
CASES=Path(__file__).resolve().parent/'semantic_cases.json'

class AutomotivePaidMediaContract(unittest.TestCase):
    def setUp(self):
        self.spec=SPEC.read_text(); self.evidence=EVIDENCE.read_text(); self.cases=json.loads(CASES.read_text())
    def test_parent_binding(self):
        self.assertIn('paid-media-performance-marketing@1.0.0',self.evidence)
        self.assertIn('882477d8941c09538576096fbe93cd286584a77d040eecf1d8c266ffab3a9179',self.spec+self.evidence)
        self.assertIn('EXTEND',self.evidence)
    def test_delta_constructs(self):
        for x in ['Inventory-unit economics','Vehicle merchandising integrity','Automotive funnel','CRM identity stitching','Inventory portfolio allocation','Sales-operations interaction','Price, finance, trade-in and incentive claims']:
            self.assertIn(x.lower(),self.spec.lower())
    def test_context_boundary(self):
        for x in ['UAE-specific','Meta Ads execution','WhatsApp','named vehicle campaign']:
            self.assertIn(x,self.spec)
    def test_cases_complete_and_balanced(self):
        self.assertEqual([f'AUTO-S{i}' for i in range(1,11)],[c['id'] for c in self.cases])
        self.assertTrue(any(c['allowed_actions']==['SCALE'] for c in self.cases))
        self.assertTrue(any('SCALE' in c['forbidden_actions'] for c in self.cases))
        for c in self.cases:
            self.assertTrue(c['required_flags'])
    def test_truthfulness_and_legal_escalation_are_separate_constructs(self):
        s5=next(c for c in self.cases if c['id']=='AUTO-S5')
        s7=next(c for c in self.cases if c['id']=='AUTO-S7')
        self.assertEqual(['merchandising_truth'],s5['required_flags'])
        self.assertIn('claim_risk_escalated',s7['required_flags'])
        self.assertIn('offer_claim_provenance',s7['required_flags'])
    def test_no_third_party_import(self):
        self.assertIn('No third-party code, prompt, or professional artifact is imported',self.evidence)

if __name__=='__main__': unittest.main()
