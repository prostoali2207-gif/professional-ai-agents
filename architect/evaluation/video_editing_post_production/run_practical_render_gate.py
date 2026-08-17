#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".tmp/video-editing-post-production/practical-render"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=True)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            raise SystemExit(f"BLOCKED: {binary} unavailable")
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ve-practical-") as directory:
        work = Path(directory)
        first, second = work / "source-a.mp4", work / "source-b.mp4"
        render = OUT / "synthetic-review-render.mp4"
        run(["ffmpeg","-y","-f","lavfi","-i","testsrc2=size=360x640:rate=30:duration=2","-f","lavfi","-i","sine=frequency=440:sample_rate=48000:duration=2","-shortest","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac",str(first)])
        run(["ffmpeg","-y","-f","lavfi","-i","color=c=0x235789:size=360x640:rate=30:duration=2","-f","lavfi","-i","sine=frequency=660:sample_rate=48000:duration=2","-shortest","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac",str(second)])
        concat = work / "concat.txt"
        concat.write_text(f"file '{first}'\nfile '{second}'\n", encoding="utf-8")
        run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),"-vf","drawbox=x=20:y=40:w=320:h=100:color=black@0.55:t=fill,drawtext=text='REVIEW FIXTURE':x=(w-text_w)/2:y=70:fontcolor=white:fontsize=24","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-movflags","+faststart",str(render)])
        metadata = json.loads(run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(render)]).stdout)
        video = next(stream for stream in metadata["streams"] if stream["codec_type"] == "video")
        audio = next(stream for stream in metadata["streams"] if stream["codec_type"] == "audio")
        decode = subprocess.run(["ffmpeg","-v","error","-i",str(render),"-f","null","-"], text=True, capture_output=True)
        black = subprocess.run(["ffmpeg","-hide_banner","-i",str(render),"-vf","blackdetect=d=0.5:pix_th=0.01","-an","-f","null","-"], text=True, capture_output=True)
        checks = {
            "decode_pass": decode.returncode == 0 and not decode.stderr.strip(),
            "video_stream": video["codec_name"] == "h264" and int(video["width"]) == 360 and int(video["height"]) == 640,
            "audio_stream": audio["codec_name"] == "aac" and int(audio["sample_rate"]) == 48000,
            "duration": 3.8 <= float(metadata["format"]["duration"]) <= 4.3,
            "no_long_black_interval": "black_start" not in black.stderr,
            "lineage_hashes": all(len(digest(path)) == 64 for path in (first, second, render))
        }
        summary = {
            "status": "PASS" if all(checks.values()) else "FAIL",
            "scope": "Synthetic fixture validates render/decode/metadata/hash QC mechanics only; it does not qualify editorial taste or real-media perception.",
            "ffmpeg_version": run(["ffmpeg","-version"]).stdout.splitlines()[0],
            "source_sha256": {"source-a":digest(first),"source-b":digest(second)},
            "render_sha256": digest(render), "checks": checks, "probe": metadata
        }
        (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(json.dumps({"status":summary["status"],"checks":checks}, indent=2))
        return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
