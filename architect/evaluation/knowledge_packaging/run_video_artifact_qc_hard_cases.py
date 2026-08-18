#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".tmp/knowledge-packaging/video-artifact-qc"


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=check)


def require_tools() -> None:
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            raise SystemExit(f"BLOCKED: {binary} unavailable")


def probe(path: Path) -> dict:
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]).stdout)


def decode_ok(path: Path) -> bool:
    p = run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], check=False)
    return p.returncode == 0 and not p.stderr.strip()


def has_long_black(path: Path) -> bool:
    p = run(["ffmpeg", "-hide_banner", "-i", str(path), "-vf", "blackdetect=d=0.8:pix_th=0.02", "-an", "-f", "null", "-"], check=False)
    return "black_start" in p.stderr


def has_long_silence(path: Path) -> bool:
    p = run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "silencedetect=noise=-45dB:d=0.8", "-vn", "-f", "null", "-"], check=False)
    return "silence_start" in p.stderr


def stream_types(meta: dict) -> set[str]:
    return {s.get("codec_type") for s in meta.get("streams", [])}


def main() -> int:
    require_tools()
    OUT.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="kp-ve11-") as td:
        work = Path(td)

        good = work / "good.mp4"
        run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30:duration=4",
            "-f", "lavfi", "-i", "sine=frequency=700:sample_rate=48000:duration=4",
            "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(good)
        ])

        # Case 1: control artifact should pass baseline mechanical QC.
        good_meta = probe(good)
        checks = {
            "decode": decode_ok(good),
            "video_and_audio_present": stream_types(good_meta) >= {"video", "audio"},
            "no_long_black": not has_long_black(good),
            "no_long_silence": not has_long_silence(good),
        }
        results.append({"id": "KP-VE11-01", "expected": "PASS", "detected": "PASS" if all(checks.values()) else "FAIL", "checks": checks})

        # Case 2: one-second black interval must be detected.
        black = work / "black-gap.mp4"
        run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30:duration=4",
            "-f", "lavfi", "-i", "sine=frequency=700:sample_rate=48000:duration=4",
            "-vf", "drawbox=x=0:y=0:w=iw:h=ih:color=black:t=fill:enable='between(t,1.4,2.6)'",
            "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(black)
        ])
        detected = has_long_black(black)
        results.append({"id": "KP-VE11-02", "expected": "REJECT", "detected": "REJECT" if detected else "MISS", "checks": {"long_black_detected": detected}})

        # Case 3: one-second silence interval must be detected.
        silent = work / "silence-gap.mp4"
        run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30:duration=4",
            "-f", "lavfi", "-i", "sine=frequency=700:sample_rate=48000:duration=4",
            "-af", "volume=enable='between(t,1.4,2.6)':volume=0",
            "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(silent)
        ])
        detected = has_long_silence(silent)
        results.append({"id": "KP-VE11-03", "expected": "REJECT", "detected": "REJECT" if detected else "MISS", "checks": {"long_silence_detected": detected}})

        # Case 4: missing audio stream must be detected.
        no_audio = work / "no-audio.mp4"
        run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30:duration=4",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(no_audio)
        ])
        meta = probe(no_audio)
        detected = "audio" not in stream_types(meta)
        results.append({"id": "KP-VE11-04", "expected": "REJECT", "detected": "REJECT" if detected else "MISS", "checks": {"missing_audio_detected": detected}})

        # Case 5: truncated/corrupt file must not decode cleanly.
        corrupt = work / "corrupt.mp4"
        data = good.read_bytes()
        corrupt.write_bytes(data[: max(1024, len(data) // 3)])
        detected = not decode_ok(corrupt)
        results.append({"id": "KP-VE11-05", "expected": "REJECT", "detected": "REJECT" if detected else "MISS", "checks": {"decode_failure_detected": detected}})

    passed = all(r["detected"] == r["expected"] for r in results)
    summary = {
        "status": "PASS" if passed else "FAIL",
        "scope": "Deterministic VE-11 hard-case gate for artifact observability. It verifies detection of injected mechanical defects; it does not qualify perceptual/editorial judgment.",
        "results": results,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
