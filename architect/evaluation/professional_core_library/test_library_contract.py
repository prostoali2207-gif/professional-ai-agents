import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
LIB = ROOT / "architect" / "library"
METHODOLOGY = ROOT / "architect" / "methodology" / "professional-core-library.md"


class ProfessionalCoreLibraryContractTests(unittest.TestCase):
    def test_catalog_is_valid_and_starts_empty(self):
        catalog = json.loads((LIB / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["schema_version"], "1.0.0")
        self.assertEqual(catalog["library_status"], "active")
        self.assertIsInstance(catalog["entries"], list)
        self.assertEqual(catalog["entries"], [], "Infrastructure phase must not smuggle in unqualified example cores")

    def test_catalog_schema_defines_discovery_not_trust(self):
        schema = json.loads((LIB / "catalog.schema.json").read_text(encoding="utf-8"))
        entry = schema["properties"]["entries"]["items"]
        required = set(entry["required"])
        self.assertTrue({"id", "version", "lifecycle", "artifact_digest", "manifest_path", "qualification_refs", "search_facets"}.issubset(required))
        facets = set(entry["properties"]["search_facets"]["required"])
        self.assertTrue({"responsibilities", "outputs", "competencies", "authority_levels", "runtime_features"}.issubset(facets))
        self.assertNotIn("trust_score", entry["properties"])
        self.assertNotIn("popularity", entry["properties"])

    def test_manifest_schema_has_non_negotiable_contract(self):
        schema = json.loads((LIB / "professional-core-manifest.schema.json").read_text(encoding="utf-8"))
        required = set(schema["required"])
        expected = {
            "id", "version", "lifecycle", "profession", "scope", "artifact",
            "maintainers", "competency_contract", "context_boundary", "provenance",
            "dependencies", "runtime_contract", "authority_and_security", "freshness",
            "limitations", "qualification_refs"
        }
        self.assertTrue(expected.issubset(required))
        lifecycle = set(schema["properties"]["lifecycle"]["enum"])
        self.assertEqual(lifecycle, {"candidate", "qualified", "deprecated", "quarantined", "revoked"})
        digest_pattern = schema["properties"]["artifact"]["properties"]["content_digest"]["pattern"]
        self.assertIn("sha256", digest_pattern)

    def test_qualification_is_separate_and_digest_bound(self):
        schema = json.loads((LIB / "qualification-record.schema.json").read_text(encoding="utf-8"))
        required = set(schema["required"])
        for field in {"core_id", "core_version", "artifact_digest", "claims", "evaluation", "environment", "evidence", "limitations", "freshness"}:
            self.assertIn(field, required)
        evaluation_required = set(schema["properties"]["evaluation"]["required"])
        self.assertTrue({"fixture_refs", "grader_refs", "thresholds", "reliability_trials", "result"}.issubset(evaluation_required))

    def test_methodology_blocks_catalog_as_trust_signal(self):
        text = METHODOLOGY.read_text(encoding="utf-8")
        self.assertIn("Library presence is a discovery fact, not a trust verdict", text)
        self.assertIn("Core artifact", text)
        self.assertIn("Qualification record", text)
        self.assertIn("Catalog entry", text)
        self.assertIn("candidate -> qualified", text)
        self.assertIn("Open-source repositories and third-party agent/skill libraries are **candidate sources**, not trusted cores", text)

    def test_reliability_and_lifecycle_fail_closed(self):
        text = METHODOLOGY.read_text(encoding="utf-8")
        self.assertIn("repeated-trial requirements", text)
        self.assertIn("quarantined", text)
        self.assertIn("revoked", text)
        self.assertIn("Historical", (LIB / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
