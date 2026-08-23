#!/usr/bin/env python3
from __future__ import annotations
import fcntl, os, re, time
from pathlib import Path

MIN_INTERVAL_SECONDS=float(os.environ.get('GEMINI_MIN_INTERVAL_SECONDS','6.0'))
PACE_FILE=Path(os.environ.get('GEMINI_PACE_FILE','/tmp/sales-gemini-qualification-pace'))


def pace() -> None:
    PACE_FILE.parent.mkdir(parents=True,exist_ok=True)
    with PACE_FILE.open('a+') as f:
        fcntl.flock(f.fileno(),fcntl.LOCK_EX)
        f.seek(0); raw=f.read().strip()
        last=float(raw) if raw else 0.0
        delay=MIN_INTERVAL_SECONDS-(time.monotonic()-last)
        if delay>0: time.sleep(delay)
        f.seek(0); f.truncate(); f.write(str(time.monotonic())); f.flush()
        fcntl.flock(f.fileno(),fcntl.LOCK_UN)


def retry_delay_seconds(headers, body: str) -> float:
    value=headers.get('Retry-After') if headers else None
    if value:
        try: return min(90.0,max(1.0,float(value)))
        except ValueError: pass
    m=re.search(r'retry in\s+([0-9.]+)s',body,re.I)
    if m: return min(90.0,max(1.0,float(m.group(1))+1.0))
    return 65.0
