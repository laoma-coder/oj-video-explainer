#!/usr/bin/env python3
"""Copy a template into a working project."""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["statement", "solution"])
    ap.add_argument("target")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    src = ROOT / "templates" / args.kind / "index.html"
    dst = Path(args.target).resolve()
    if not src.exists():
        raise SystemExit(f"template not found: {src}")
    if (dst / "index.html").exists() and not args.force:
        raise SystemExit(f"{dst}/index.html already exists (use --force to overwrite)")

    dst.mkdir(parents=True, exist_ok=True)
    (dst / "audio" / "lines").mkdir(parents=True, exist_ok=True)
    (dst / "fonts").mkdir(exist_ok=True)
    (dst / "out").mkdir(exist_ok=True)
    shutil.copy2(src, dst / "index.html")

    lines = dst / "audio" / "lines.json"
    if not lines.exists():
        lines.write_text(json.dumps([
            {"id": "l1", "text": "第一句旁白。", "start": 0.7,
             "rate": "+2%", "voice": "zh-CN-XiaoxiaoNeural"}
        ], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    mix = dst / "audio" / "mix.json"
    if not mix.exists():
        mix.write_text(json.dumps({
            "duration": 60 if args.kind == "statement" else 90,
            "lines": [{"file": "audio/lines/l1.wav", "start": 0.7}],
            "bed": {"notes": [523.25, 659.25, 783.99], "starts": [0.15]}
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"created {dst}")
    print("next: edit index.html, audio/lines.json, audio/mix.json")


if __name__ == "__main__":
    main()
