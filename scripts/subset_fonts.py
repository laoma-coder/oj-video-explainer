#!/usr/bin/env python3
"""Download a Noto Sans SC subset containing exactly the characters used by a page."""
import argparse
import re
import urllib.parse
import urllib.request
from pathlib import Path

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36")
PUNCT = "，。：、；！“”‘’（）《》—…·→←"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("outdir")
    ap.add_argument("--weights", default="400;600;800")
    args = ap.parse_args()

    html = Path(args.html).read_text(encoding="utf-8", errors="ignore")
    chars = sorted({c for c in html
                    if "\u4e00" <= c <= "\u9fff" or c in PUNCT})
    if not chars:
        raise SystemExit("no CJK characters found")
    text = "".join(chars)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    family = f"Noto Sans SC:wght@{args.weights}"
    query = urllib.parse.urlencode({"family": family, "text": text, "display": "block"})
    req = urllib.request.Request(
        "https://fonts.googleapis.com/css2?" + query,
        headers={"User-Agent": UA})
    css = urllib.request.urlopen(req, timeout=30).read().decode()

    blocks = re.findall(r"@font-face\s*\{.*?\}", css, re.S)
    saved = 0
    for block in blocks:
        weight = re.search(r"font-weight:\s*(\d+)", block)
        url = re.search(r"url\((https://[^)]+)\)", block)
        if not (weight and url):
            continue
        data = urllib.request.urlopen(url.group(1), timeout=30).read()
        path = outdir / f"sans-{weight.group(1)}.woff2"
        path.write_bytes(data)
        print(f"wrote {path} ({len(data)} bytes)")
        saved += 1

    if not saved:
        raise SystemExit("no font files downloaded; check network or weights")
    print(f"{len(chars)} CJK chars, {saved} weights")


if __name__ == "__main__":
    main()
