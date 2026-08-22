#!/usr/bin/env python3
"""Fail closed when provider-backed GitHub workflows can auto-run without review.

This is a mechanical Resource & Cost Engineering control. It does not decide
whether a paid run is professionally necessary; it prevents ordinary push/PR
triggers from silently spending provider quota unless a reviewed exception
proves that the automatic path itself does not perform paid generation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

PROVIDER_SECRET_RE = re.compile(
    r"\$\{\{\s*secrets\.[A-Z0-9_]*(?:OPENAI|GEMINI|ANTHROPIC|PERPLEXITY|TAVILY|EXA)[A-Z0-9_]*\s*\}\}",
    re.IGNORECASE,
)
AUTO_TRIGGER_RE = re.compile(r"^\s{2}(push|pull_request):(?:\s|$)", re.MULTILINE)


def extract_on_block(text: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line == "on:":
            start = i + 1
            break
    if start is None:
        return ""

    out: List[str] = []
    for line in lines[start:]:
        if line and not line.startswith((" ", "\t")):
            break
        out.append(line)
    return "\n".join(out)


def is_provider_backed(text: str) -> bool:
    return bool(PROVIDER_SECRET_RE.search(text))


def has_automatic_repo_trigger(text: str) -> bool:
    return bool(AUTO_TRIGGER_RE.search(extract_on_block(text)))


def load_exceptions(path: Path) -> Dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1:
        raise ValueError("paid-workflow exception file must have version=1")
    exceptions = data.get("automatic_provider_workflow_exceptions")
    if not isinstance(exceptions, dict):
        raise ValueError("automatic_provider_workflow_exceptions must be an object")
    return exceptions


def validate_exception(path: str, text: str, rule: dict) -> List[str]:
    errors: List[str] = []
    reason = rule.get("reason")
    required = rule.get("required_substrings")
    if not isinstance(reason, str) or len(reason.strip()) < 20:
        errors.append(f"{path}: exception reason is missing or too weak")
    if not isinstance(required, list) or not required or not all(isinstance(x, str) and x for x in required):
        errors.append(f"{path}: exception must declare non-empty required_substrings")
        return errors
    for needle in required:
        if needle not in text:
            errors.append(f"{path}: reviewed exception invariant missing: {needle!r}")
    return errors


def evaluate(workflow_texts: Dict[str, str], exceptions: Dict[str, dict]) -> List[str]:
    errors: List[str] = []
    seen_exception_paths = set()

    for path, text in sorted(workflow_texts.items()):
        provider = is_provider_backed(text)
        automatic = has_automatic_repo_trigger(text)
        if not (provider and automatic):
            continue

        rule = exceptions.get(path)
        if rule is None:
            errors.append(
                f"{path}: provider credential + push/pull_request trigger is not allowed; "
                "make paid execution manual-only or add a narrowly reviewed no-generation exception"
            )
            continue

        seen_exception_paths.add(path)
        errors.extend(validate_exception(path, text, rule))

    for path in sorted(exceptions):
        if path in seen_exception_paths:
            continue
        text = workflow_texts.get(path)
        if text is None:
            errors.append(f"{path}: stale exception references a missing workflow")
        elif not (is_provider_backed(text) and has_automatic_repo_trigger(text)):
            errors.append(f"{path}: stale exception is no longer required; remove it")

    return errors


def collect_workflows(root: Path) -> Dict[str, str]:
    workflow_dir = root / ".github" / "workflows"
    result: Dict[str, str] = {}
    for pattern in ("*.yml", "*.yaml"):
        for path in workflow_dir.glob(pattern):
            rel = path.relative_to(root).as_posix()
            result[rel] = path.read_text(encoding="utf-8")
    return result


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--exceptions",
        default="architect/evaluation/qualification-platform/paid-workflow-exceptions.json",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    root = Path(args.repo_root).resolve()
    exception_path = root / args.exceptions
    try:
        exceptions = load_exceptions(exception_path)
        workflows = collect_workflows(root)
        errors = evaluate(workflows, exceptions)
    except Exception as exc:
        print(f"PAID_WORKFLOW_GUARD_ERROR: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("PAID_WORKFLOW_GUARD_FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PAID_WORKFLOW_GUARD_PASS workflows={len(workflows)} exceptions={len(exceptions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
