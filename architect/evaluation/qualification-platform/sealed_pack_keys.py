#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import os
from typing import Any

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


DOMAIN_SALT = b"professional-ai-agents/qualification-sealed-pack/v1"
SUPPORTED_SCHEME = "hkdf-sha256-v1"


class SealedKeyError(RuntimeError):
    pass


def derive_fernet_key(master: bytes, context: str) -> bytes:
    if not master:
        raise SealedKeyError("master sealed-pack secret is empty")
    if not context:
        raise SealedKeyError("sealed-pack derivation context is empty")
    raw = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=DOMAIN_SALT,
        info=context.encode("utf-8"),
    ).derive(master)
    return base64.urlsafe_b64encode(raw)


def resolve_effective_key(sealed_pack: dict[str, Any]) -> bytes:
    derivation = sealed_pack.get("key_derivation")
    if derivation is not None:
        if not isinstance(derivation, dict):
            raise SealedKeyError("key_derivation must be an object")
        scheme = derivation.get("scheme")
        if scheme != SUPPORTED_SCHEME:
            raise SealedKeyError(f"unsupported sealed-pack key derivation scheme: {scheme!r}")
        master_env = str(derivation.get("master_env", ""))
        context = str(derivation.get("context", ""))
        master = os.environ.get(master_env, "").encode().strip()
        if not master:
            raise SealedKeyError(f"sealed-pack master secret missing: {master_env}")
        return derive_fernet_key(master, context)

    key_env = str(sealed_pack.get("key_env", ""))
    key = os.environ.get(key_env, "").encode().strip()
    if not key:
        raise SealedKeyError(f"sealed pack key missing: {key_env}")
    return key


def key_fingerprint_sha256(key: bytes) -> str:
    return hashlib.sha256(key).hexdigest()
