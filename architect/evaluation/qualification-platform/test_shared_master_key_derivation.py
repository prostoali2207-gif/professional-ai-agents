#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import os
import unittest

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


DOMAIN_SALT = b"professional-ai-agents/qualification-sealed-pack/v1"


def derive_fernet_key(master: bytes, context: str) -> bytes:
    raw = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=DOMAIN_SALT,
        info=context.encode("utf-8"),
    ).derive(master)
    return base64.urlsafe_b64encode(raw)


class SharedMasterKeyDerivationTests(unittest.TestCase):
    def test_same_master_and_context_is_deterministic(self) -> None:
        master = b"test-master-secret-material"
        self.assertEqual(
            derive_fernet_key(master, "cycle-a"),
            derive_fernet_key(master, "cycle-a"),
        )

    def test_different_contexts_produce_different_pack_keys(self) -> None:
        master = b"test-master-secret-material"
        self.assertNotEqual(
            derive_fernet_key(master, "cycle-a"),
            derive_fernet_key(master, "cycle-b"),
        )

    def test_result_is_valid_fernet_key_shape(self) -> None:
        key = derive_fernet_key(b"test-master-secret-material", "cycle-a")
        self.assertEqual(len(base64.urlsafe_b64decode(key)), 32)
        self.assertEqual(len(key), 44)


if __name__ == "__main__":
    unittest.main()
