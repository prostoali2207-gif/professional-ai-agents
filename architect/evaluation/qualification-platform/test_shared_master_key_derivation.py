#!/usr/bin/env python3
from __future__ import annotations

import base64
import os
import unittest
from unittest import mock

from sealed_pack_keys import (
    SealedKeyError,
    derive_fernet_key,
    key_fingerprint_sha256,
    resolve_effective_key,
)


class SharedMasterKeyDerivationTests(unittest.TestCase):
    def test_same_master_and_context_is_deterministic(self) -> None:
        master = b"test-master-secret-material"
        self.assertEqual(derive_fernet_key(master, "cycle-a"), derive_fernet_key(master, "cycle-a"))

    def test_different_contexts_produce_different_pack_keys(self) -> None:
        master = b"test-master-secret-material"
        self.assertNotEqual(derive_fernet_key(master, "cycle-a"), derive_fernet_key(master, "cycle-b"))

    def test_result_is_valid_fernet_key_shape(self) -> None:
        key = derive_fernet_key(b"test-master-secret-material", "cycle-a")
        self.assertEqual(len(base64.urlsafe_b64decode(key)), 32)
        self.assertEqual(len(key), 44)

    def test_resolve_derived_key_from_one_shared_master_env(self) -> None:
        spec = {"key_derivation": {"scheme": "hkdf-sha256-v1", "master_env": "QUALIFICATION_SEALED_PACK_MASTER_KEY", "context": "content-architecture-heldout-v0.1"}}
        with mock.patch.dict(os.environ, {"QUALIFICATION_SEALED_PACK_MASTER_KEY": "one-shared-secret"}, clear=False):
            observed = resolve_effective_key(spec)
        self.assertEqual(observed, derive_fernet_key(b"one-shared-secret", "content-architecture-heldout-v0.1"))

    def test_legacy_direct_key_env_still_works(self) -> None:
        with mock.patch.dict(os.environ, {"LEGACY_PACK_KEY": "legacy-key"}, clear=False):
            self.assertEqual(resolve_effective_key({"key_env": "LEGACY_PACK_KEY"}), b"legacy-key")

    def test_missing_master_fails_closed(self) -> None:
        spec = {"key_derivation": {"scheme": "hkdf-sha256-v1", "master_env": "QUALIFICATION_SEALED_PACK_MASTER_KEY_MISSING_FOR_TEST", "context": "cycle-a"}}
        with self.assertRaises(SealedKeyError):
            resolve_effective_key(spec)

    def test_fingerprint_is_of_effective_pack_key(self) -> None:
        key = derive_fernet_key(b"master", "cycle-a")
        self.assertEqual(len(key_fingerprint_sha256(key)), 64)


if __name__ == "__main__":
    unittest.main()
