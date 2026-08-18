#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_adapter(adapter_cmd: list[str], fixture: dict) -> dict:
    proc = subprocess.run(
        adapter_cmd,
        input=json.dumps(fixture),
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"candidate adapter failed ({proc.returncode}): {proc.stderr.strip()}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"candidate adapter returned invalid JSON: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture")
    parser.add_argument("--adapter", nargs=argparse.REMAINDER, required=True)
    args = parser.parse_args()
    if not args.adapter:
        raise SystemExit("--adapter requires a command")

    fixture = load_json(args.fixture)
    result = run_adapter(args.adapter, fixture)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
