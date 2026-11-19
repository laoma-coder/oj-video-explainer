#!/usr/bin/env python3
"""Mix narration WAVs with a sparse plucked bed (no continuous pad)."""
import argparse
import json
import math
import wave
from pathlib import Path

import numpy as np

SR = 48000


def read_mono(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32768.0
        if w.getnchannels() > 1:
            x = x.reshape(-1, w.getnchannels()).mean(axis=1)
        return x


def highpass(x, cutoff):
    a = math.exp(-2.0 * math.pi * cutoff / SR)
    y = np.empty_like(x)
    px = py = 0.0
    for i, v in enumerate(x):
        y[i] = a * (py + v - px)
        px, py = v, y[i]
    return y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--config")
    args = ap.parse_args()

    project = Path(args.project).resolve()
    config_path = Path(args.config) if args.config else project / "audio" / "mix.json"
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    duration = float(cfg["duration"])
    n = int(SR * duration)

    voice = np.zeros(n)
    for line in cfg.get("lines", []):
        path = project / line["file"]
        if not path.exists():
            raise SystemExit(f"missing {path}; run tts_lines.py first")
        x = read_mono(path)
        start = int(float(line.get("start", 0)) * SR)
        end = min(n, start + len(x))
        voice[start:end] += x[: end - start]

    music = np.zeros(n)
    bed = cfg.get("bed", {})
    notes = bed.get("notes", [523.25, 659.25, 783.99])
    starts = bed.get("starts", [0.15])
    for i, start_s in enumerate(starts):
        start = int(float(start_s) * SR)
        length = int(0.9 * SR)
        if start + length > n:
            continue
        tt = np.arange(length) / SR
        env = (1.0 - np.exp(-tt * 90.0)) * np.exp(-tt * 6.0)
        f0 = float(notes[i % len(notes)])
        tone = np.sin(2 * math.pi * f0 * tt) + 0.18 * np.sin(2 * math.pi * f0 * 2 * tt)
        music[start:start + length] += env * tone
    music = highpass(highpass(music, 180.0), 180.0)

    # duck music under voice
    step = int(0.02 * SR)
    env = np.zeros(n)
    for i in range(0, n, step):
        seg = voice[i:i + step]
        env[i:i + step] = np.sqrt(np.mean(seg ** 2)) if len(seg) else 0.0
    k = int(0.2 * SR)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    duck = np.clip(env / 0.05, 0.0, 1.0)
    music *= 0.4 + 0.6 * (1.0 - duck)

    if np.abs(voice).max() > 0:
        voice *= 0.72 / np.abs(voice).max()
    if np.abs(music).max() > 0:
        music *= 0.09 / np.abs(music).max()

    mix = voice + music
    fo = int(1.0 * SR)
    mix[-fo:] *= np.linspace(1.0, 0.0, fo)
    if np.abs(mix).max() > 0:
        mix *= 0.89 / np.abs(mix).max()

    stereo = np.stack([mix, mix], axis=1)
    pcm = np.clip(stereo * 32767.0, -32768, 32767).astype("<i2")
    out = project / "audio" / "mix.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(pcm.tobytes())

    rms = 20 * math.log10(math.sqrt(float(np.mean(stereo ** 2))) + 1e-12)
    print(f"wrote {out} · {duration:.1f}s · rms {rms:.1f} dBFS · peak -1.0 dBFS")


if __name__ == "__main__":
    main()
