"""
Scrolling waveform animation — Manim version (vector-rendered, Cairo).
Compare with scene_waveform.py (matplotlib) to choose your preferred look.

Usage:
    python animations/scene_waveform_manim.py audio/violin_A4.wav
    python animations/scene_waveform_manim.py audio/violin_A4.wav --window 0.05
    python animations/scene_waveform_manim.py audio/violin_A4.wav --quality l   # fast preview

Output: output/waveform/<stem>.mp4
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import librosa
from manim import *

_AUDIO_FILE = os.environ.get("WAVEFORM_AUDIO", "")
_CLIP_START = float(os.environ.get("WAVEFORM_START", "0"))
_CLIP_END   = float(os.environ.get("WAVEFORM_END")) if os.environ.get("WAVEFORM_END") else None
_WINDOW     = float(os.environ.get("WAVEFORM_WINDOW", "0.05"))

SR             = 44100
N_DISPLAY      = 400          # points per frame — keep low for Manim performance
WAVEFORM_COLOR = "#FDE724"
AXIS_COLOR     = "#555555"
X_LO, X_HI    = -6.5, 6.5
WAVE_HEIGHT    = 2.8


class WaveformSceneManim(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        if not _AUDIO_FILE:
            raise RuntimeError("WAVEFORM_AUDIO env var not set — use the CLI wrapper.")

        duration_arg = (_CLIP_END - _CLIP_START) if _CLIP_END is not None else None
        y, sr = librosa.load(_AUDIO_FILE, sr=SR, mono=True,
                             offset=_CLIP_START, duration=duration_arg)
        duration    = len(y) / SR
        win_samples = int(_WINDOW * SR)

        peak = np.abs(y).max()
        if peak > 0:
            y = y / peak

        # ── Zero line ─────────────────────────────────────────────────────────
        zero_line = Line(np.array([X_LO, 0, 0]), np.array([X_HI, 0, 0]),
                         color=AXIS_COLOR, stroke_width=1)
        self.add(zero_line)

        # ── Scrolling waveform via ValueTracker + always_redraw ───────────────
        tracker = ValueTracker(0)

        def make_wave():
            t       = tracker.get_value()
            i_start = int(t * SR)
            i_end   = i_start + win_samples
            chunk   = y[i_start:i_end] if i_end <= len(y) else np.pad(
                y[i_start:], (0, win_samples - max(0, len(y) - i_start))
            )
            idx = np.linspace(0, len(chunk) - 1, N_DISPLAY, dtype=int)
            xs  = np.linspace(X_LO, X_HI, N_DISPLAY)
            ys  = chunk[idx] * WAVE_HEIGHT
            pts = np.column_stack([xs, ys, np.zeros(N_DISPLAY)])
            wave = VMobject(stroke_width=2.0, stroke_color=WAVEFORM_COLOR)
            wave.set_points_as_corners(pts)
            return wave

        wave = always_redraw(make_wave)
        self.add(wave)

        # ── Audio + animate ───────────────────────────────────────────────────
        self.add_sound(_AUDIO_FILE, time_offset=0)
        self.play(tracker.animate.set_value(duration),
                  run_time=duration, rate_func=linear)
        self.wait(0.2)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("audio")
    p.add_argument("--start",   "-s", type=float, default=0)
    p.add_argument("--end",     "-e", type=float, default=None)
    p.add_argument("--window",  "-w", type=float, default=0.05)
    p.add_argument("--quality",       default="h",
                   choices=["l", "m", "h", "k"])
    args = p.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"ERROR: file not found: {audio_path}")
        sys.exit(1)

    env = os.environ.copy()
    env["WAVEFORM_AUDIO"]  = str(audio_path.resolve())
    env["WAVEFORM_START"]  = str(args.start)
    env["WAVEFORM_WINDOW"] = str(args.window)
    if args.end is not None:
        env["WAVEFORM_END"] = str(args.end)

    result = subprocess.run([
        sys.executable, "-m", "manim",
        f"-pq{args.quality}",
        "--media_dir", "media",
        "--output_file", audio_path.stem,
        __file__, "WaveformSceneManim",
    ], env=env)

    if result.returncode == 0:
        quality_dir = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
        src = (Path("media/videos/scene_waveform_manim")
               / quality_dir[args.quality] / f"{audio_path.stem}.mp4")
        out_dir = Path("output/waveform")
        out_dir.mkdir(parents=True, exist_ok=True)
        if src.exists():
            dest = out_dir / f"{audio_path.stem}_manim.mp4"
            shutil.move(str(src), str(dest))
            print(f"\nSaved: {dest}")

    sys.exit(result.returncode)
