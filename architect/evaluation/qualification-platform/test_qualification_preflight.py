import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("qualification_preflight", HERE / "qualification_preflight.py")
qp = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qp)


def base_manifest():
    return {
        "version": 2,
        "cycle_id": "test-cycle",
        "candidate": {"commit": "0" * 40, "digest": "sha256:" + "0" * 64, "manifest_path": "x.json"},
        "runtime": {
            "executor_path": str(HERE / "qualification_preflight.py"),
            "executor_cmd": "python qualification_preflight.py",
            "protocol": "test-v1",
            "provider": "test-provider",
            "model": "test-model",
            "credential_env": "TEST_API_KEY",
            "candidate_timeout_seconds": 20,
            "model_timeout_seconds": 10,
            "workflow_timeout_seconds": 60,
            "contract_probe_argv": ["python3", "-c", "import json; print(json.dumps({'contract_version':1,'candidate_commit':'" + "0" * 40 + "','candidate_digest':'sha256:" + "0" * 64 + "','provider':'test-provider','input_protocol':'test-v1','tool_protocol':'tools-v1','state_protocol':'state-v1','observable_protocol':'obs-v1'}))"],
            "tool_protocol": "tools-v1",
            "state_protocol": "state-v1",
            "observable_protocol": "obs-v1",
            "canary_required": False,
        },
        "sealed_pack": {
            "parts_dir": "parts",
            "part_count": 1,
            "ciphertext_length": 1,
            "ciphertext_sha256": "0" * 64,
            "key_env": "TEST_SEALED_KEY",
            "key_fingerprint_sha256": "0" * 64,
            "decrypted_zip_sha256": "0" * 64,
            "pack_digest": "sha256:" + "0" * 64,
            "required_files": ["fixtures.json", "grader.json", "runner.py", "freeze-record.json"],
        },
        "evaluation": {
            "fixture_count": 1,
            "family_count": 1,
            "per_family": 1,
            "fixtures_file": "fixtures.json",
            "grader_file": "grader.json",
            "runner_file": "runner.py",
            "freeze_record_file": "freeze-record.json",
        },
        "report": {
            "sanitized_required": True,
            "artifact_required": True,
            "validator_path": str(HERE / "validate_sanitized_report.py"),
            "release_ledger_required": True,
        },
        "verdict": {
            "runner_exit_zero_required": True,
            "missing_report_is_failure": True,
            "report_validation_required": True,
            "artifact_upload_required": True,
        },
    }


class QualificationPreflightTests(unittest.TestCase):
    def test_manifest_schema_rejects_open_release_gate(self):
        m = base_manifest()
        m["verdict"]["missing_report_is_failure"] = False
        with self.assertRaises(qp.PreflightError) as ctx:
            qp.validate_manifest_schema(m, HERE / "qualification-manifest.schema.json")
        self.assertEqual(ctx.exception.code, "RUNTIME_CONTRACT_MISMATCH")

    def test_timeout_nesting_is_rejected_before_api(self):
        m = base_manifest()
        m["runtime"]["model_timeout_seconds"] = 30
        m["runtime"]["candidate_timeout_seconds"] = 20
        with self.assertRaises(qp.PreflightError) as ctx:
            qp.verify_runtime_static(m, False)
        self.assertEqual(ctx.exception.code, "TIMEOUT_INCOMPATIBLE")

    def test_missing_runtime_secret_is_classified_without_call(self):
        m = base_manifest()
        os.environ.pop("TEST_API_KEY", None)
        with self.assertRaises(qp.PreflightError) as ctx:
            qp.verify_runtime_static(m, True)
        self.assertEqual(ctx.exception.code, "CREDENTIAL_MISSING")

    def test_contract_probe_passes_without_runtime_credential(self):
        m = base_manifest()
        os.environ.pop("TEST_API_KEY", None)
        qp.verify_runtime_contract_probe(m)

    def test_contract_probe_detects_protocol_drift(self):
        m = base_manifest()
        m["runtime"]["tool_protocol"] = "tools-v2"
        with self.assertRaises(qp.PreflightError) as ctx:
            qp.verify_runtime_contract_probe(m)
        self.assertEqual(ctx.exception.code, "RUNTIME_CONTRACT_MISMATCH")

    def test_safe_extract_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as td:
            zpath = Path(td) / "bad.zip"
            with zipfile.ZipFile(zpath, "w") as zf:
                zf.writestr("../escape.txt", "x")
            with zipfile.ZipFile(zpath) as zf:
                with self.assertRaises(qp.PreflightError) as ctx:
                    qp.safe_extract(zf, Path(td) / "out")
            self.assertEqual(ctx.exception.code, "PACK_INTEGRITY_INVALID")


if __name__ == "__main__":
    unittest.main()
