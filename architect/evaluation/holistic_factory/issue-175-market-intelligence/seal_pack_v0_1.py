#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plaintext", required=True)
    parser.add_argument("--sealed-out", required=True)
    parser.add_argument("--key-out", required=True)
    args = parser.parse_args()

    plain = Path(args.plaintext).read_bytes()
    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    aad = b"issue-175-market-intelligence-codex-v0.1"
    ciphertext = AESGCM(key).encrypt(nonce, plain, aad)
    envelope = {
        "format": "aes-256-gcm-v1",
        "aad": aad.decode("ascii"),
        "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
    }
    sealed = (json.dumps(envelope, sort_keys=True, separators=(",", ":")) + "\n").encode()
    Path(args.sealed_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.sealed_out).write_bytes(sealed)
    Path(args.key_out).write_bytes(key)
    print(json.dumps({
        "plaintext_sha256": hashlib.sha256(plain).hexdigest(),
        "ciphertext_file_sha256": hashlib.sha256(sealed).hexdigest(),
        "plaintext_length": len(plain),
        "sealed_length": len(sealed),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

