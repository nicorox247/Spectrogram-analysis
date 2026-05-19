"""
Scrolling waveform animation — oscilloscope-style window that advances through the audio.
Matches the visual style of the resynthesis videos.

Usage:
    python animations/scene_waveform.py <audio_file>
    python animations/scene_waveform.py audio/violin_A4.wav
    python animations/scene_waveform.py audio/violin_A4.wav --start 0 --end 1.0
    python animations/scene_waveform.py audio/violin_A4.wav --window 0.05

Output: output/waveform/<stem>.mp4
"""

import argparse
import subprocess
import sys
from pathlib import Path

import librosa
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

FPS            = 60
SR             = 44100
WAVEFORM_COLOR = "#FDE724"   # cividis yellow — matches spectrogram palette
BG_COLOR       = "black"
AXIS_COLOR     = "#555555"
OUTPUT_DIR     = Path("output/waveform")

FIG_W, FIG_H = 16, 9        # inches
DPI          = 120           # → 1920×1080


def parse_args():
    p = argparse.ArgumentParser(description="Render scrolling waveform animation.")
    p.add_argument("audio",          help="Path to audio file")
    p.add_argument("--start", "-s",  type=float, default=0,    help="Clip start (s)")
    p.add_argument("--end",   "-e",  type=float, default=None, help="Clip end (s)")
    p.add_argument("--window", "-w", type=float, default=0.05,
                   help="Visible time window in seconds (default: 0.05)")
    return p.parse_args()


def render_frame(fig):
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    buf = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8).reshape(h, w, 4)
    return buf[:, :, :3].copy()


def main():
    args = parse_args()
    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"ERROR: file not found: {audio_path}")
        sys.exit(1)

    duration_arg = (args.end - args.start) if args.end is not None else None
    y, sr = librosa.load(str(audio_path), sr=SR, mono=True,
                         offset=args.start, duration=duration_arg)
    duration     = len(y) / SR
    win_samples  = int(args.window * SR)
    total_frames = int(duration * FPS)

    # Normalize
    peak = np.abs(y).max()
    if peak > 0:
        y = y / peak

    # ── Figure ────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, args.window * 1000)   # display in ms
    ax.set_ylim(-1.1, 1.1)

    # Axis styling
    ax.axhline(0, color=AXIS_COLOR, linewidth=0.8, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors="white", labelsize=11)
    ax.yaxis.set_visible(False)
    ax.set_xlabel("ms", color="#888888", fontsize=12)
    ax.xaxis.label.set_color("#888888")
    fig.tight_layout(pad=1.5)

    t_ms = np.linspace(0, args.window * 1000, win_samples)
    (line,) = ax.plot(t_ms, np.zeros(win_samples),
                      color=WAVEFORM_COLOR, linewidth=1.2, antialiased=True)

    # ── ffmpeg pipe ───────────────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stem     = audio_path.stem
    out_path = OUTPUT_DIR / f"{stem}.mp4"

    px_w = int(FIG_W * DPI)
    px_h = int(FIG_H * DPI)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{px_w}x{px_h}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "pipe:0",
        "-i", str(audio_path.resolve()),
        "-ss", str(args.start),
        *([ "-t", str(duration_arg) ] if duration_arg else []),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(out_path),
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    print(f"Rendering {total_frames} frames ({duration:.2f}s) …")
    for frame in range(total_frames):
        i_start = int(frame / FPS * SR)
        i_end   = i_start + win_samples

        if i_end <= len(y):
            chunk = y[i_start:i_end]
        else:
            chunk = np.zeros(win_samples)
            avail = max(0, len(y) - i_start)
            chunk[:avail] = y[i_start:i_start + avail]

        line.set_ydata(chunk)
        proc.stdin.write(render_frame(fig).tobytes())

        if frame % (FPS * 5) == 0:
            print(f"  {frame}/{total_frames}  ({frame / FPS:.1f}s)")

    proc.stdin.close()
    proc.wait()
    plt.close(fig)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
