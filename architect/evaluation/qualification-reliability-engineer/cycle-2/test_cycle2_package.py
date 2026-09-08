#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, importlib.util, json, sys, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import validate_blind_judgments as v

BUNDLE=HERE/"blind-bundle-v0.2.json"
TEMPLATE=HERE/"blind-judgment-template-v0.2.json"

FORBIDDEN={"expected_decision_properties","unacceptable_shortcuts","applicable_p0_triggers","mechanism","title","legitimate_disagreement_boundary","competencies","deterministic_assertions","judgment_dimensions","author_level"}

def walk(value):
    if isinstance(value,dict):
        for k,val in value.items():
            yield k
            yield from walk(val)
    elif isinstance(value,list):
        for x in value:
            yield from walk(x)

def valid_filled():
    d=json.loads(TEMPLATE.read_bytes())
    for j in d["judgments"]:
        j["predicted_level"]="MECHANICAL_SHALLOW"
        j["p0_triggers"]=[]
        j["material_strengths"]=["bounded judgment"]
        j["material_failures"]=["material depth not established"]
        j["uncertainty"]="none"
        j["release_eligible"]=False
    return d

class Cycle2Tests(unittest.TestCase):
    def test_bundle_surface(self):
        b=json.loads(BUNDLE.read_bytes())
        self.assertEqual(set(b),{"version","cycle","source_pack_sha256","p0_rules","rubric","cases"})
        self.assertEqual(len(b["cases"]),12)
        refs=[r["reference_id"] for c in b["cases"] for r in c["reference_exemplars"]]
        self.assertEqual(len(refs),48)
        self.assertEqual(len(set(refs)),48)
        self.assertTrue(FORBIDDEN.isdisjoint(set(walk(b))))

    def test_template_valid(self):
        d=json.loads(TEMPLATE.read_bytes())
        self.assertEqual(v.validate_template(d)["judgments"],48)

    def test_valid_filled(self):
        self.assertEqual(v.validate(valid_filled())["status"],"PASS")

    def test_missing_reference_rejected(self):
        d=valid_filled(); d["judgments"].pop()
        with self.assertRaises(v.ValidationError): v.validate(d)

    def test_duplicate_reference_rejected(self):
        d=valid_filled(); d["judgments"][-1]["reference_id"]=d["judgments"][0]["reference_id"]
        with self.assertRaises(v.ValidationError): v.validate(d)

    def test_unknown_reference_rejected(self):
        d=valid_filled(); d["judgments"][0]["reference_id"]="R999"
        with self.assertRaises(v.ValidationError): v.validate(d)

    def test_illegal_level_rejected(self):
        d=valid_filled(); d["judgments"][0]["predicted_level"]="SUPER_PASS"
        with self.assertRaises(v.ValidationError): v.validate(d)

    def test_illegal_p0_rejected(self):
        d=valid_filled(); d["judgments"][0]["p0_triggers"]=["P0-99"]
        with self.assertRaises(v.ValidationError): v.validate(d)

    def test_wrong_bundle_rejected(self):
        d=valid_filled(); d["source_bundle_sha256"]="0"*64
        with self.assertRaises(v.ValidationError): v.validate(d)

    def test_contaminated_context_rejected(self):
        d=valid_filled(); d["reviewer"]["author_key_seen"]=True
        with self.assertRaises(v.ValidationError): v.validate(d)

    def test_incomplete_placeholder_rejected(self):
        d=valid_filled(); d["judgments"][0]["release_eligible"]=None
        with self.assertRaises(v.ValidationError): v.validate(d)

if __name__=="__main__":
    unittest.main()
