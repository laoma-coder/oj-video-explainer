#!/usr/bin/env python3
"""Generate Mandarin narration lines with edge-tts and convert to 48 kHz WAV."""
import argparse
import asyncio
import json
import subprocess
from pathlib import Path


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", str(path)
    ], text=True).strip()
    return float(out)


def to_wav(mp3: Path, wav: Path) -> None:
    subprocess.check_call([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(mp3), "-ar", "48000", "-ac", "1", str(wav)
    ])


async def synth(text: str, voice: str, rate: str, out: Path) -> None:
    import edge_tts
    com = edge_tts.Communicate(text, voice, rate=rate)
    await asyncio.wait_for(com.save(str(out)), timeout=45)


async def main_async(args) -> None:
    project = Path(args.project).resolve()
    config = Path(args.config) if args.config else project / "audio" / "lines.json"
    data = json.loads(config.read_text(encoding="utf-8"))
    lines_dir = project / "audio" / "lines"
    lines_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for line in data:
        name = line["id"]
        mp3 = lines_dir / f"{name}.mp3"
        wav = lines_dir / f"{name}.wav"
        voice = line.get("voice", args.voice)
        rate = line.get("rate", args.rate)
        await synth(line["text"], voice, rate, mp3)
        to_wav(mp3, wav)
        dur = ffprobe_duration(wav)
        rows.append((name, float(line.get("start", 0)), dur))

    print(f"{'id':<6}{'start':>8}{'dur':>8}{'end':>8}")
    for name, start, dur in rows:
        print(f"{name:<6}{start:>8.2f}{dur:>8.2f}{start + dur:>8.2f}")

    rows_sorted = sorted(rows, key=lambda r: r[1])
    for (n1, s1, d1), (n2, s2, d2) in zip(rows_sorted, rows_sorted[1:]):
        if s1 + d1 > s2 + 0.01:
            print(f"WARN overlap: {n1} ends {s1+d1:.2f}, {n2} starts {s2:.2f}")
    print("done")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--config")
    ap.add_argument("--voice", default="zh-CN-XiaoxiaoNeural")
    ap.add_argument("--rate", default="+2%")
    args = ap.parse_args()
    try:
        asyncio.run(main_async(args))
    except ModuleNotFoundError:
        raise SystemExit("edge-tts is missing: pip install edge-tts")


if __name__ == "__main__":
    main()
