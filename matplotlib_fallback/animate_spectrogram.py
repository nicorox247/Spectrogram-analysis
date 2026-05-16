"""
Animate a spectrogram segment with a sweeping playhead.
Loads pre-computed .npy data — do not recompute here.
"""

from pathlib import Path
import argparse
import json
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import librosa.display

AUDIO_DIR = Path("audio/normalized")

DATA_DIR = Path("analysis/spectrogram_data")
OUTPUT_DIR = Path("output/spectrogram")

F_MIN = 0
F_MAX = 17000
CMAP  = "cividis"
FPS   = 30


def main() -> None:
    parser = argparse.ArgumentParser(description="Animate a spectrogram segment.")
    parser.add_argument("track", help="Track name (must match filename in analysis/spectrogram_data/, without extension)")
    parser.add_argument("start", type=float, help="Start time in seconds")
    parser.add_argument("end", type=float, help="End time in seconds")
    args = parser.parse_args()

    TRACK   = args.track
    T_START = args.start
    T_END   = args.end

    OUTPUT_DIR.mkdir(exist_ok=True)

    npy_path  = DATA_DIR / f"{TRACK}.npy"
    json_path = DATA_DIR / f"{TRACK}.json"

    S_db = np.load(npy_path)
    with json_path.open() as f:
        meta = json.load(f)

    sr         = meta["sample_rate"]
    hop        = meta["hop_length"]
    secs_per_bin = hop / sr

    col_start = int(T_START / secs_per_bin)
    col_end   = int(T_END   / secs_per_bin)
    S_slice   = S_db[:, col_start:col_end]
    n_cols    = S_slice.shape[1]

    fig, ax = plt.subplots(figsize=(14, 5), facecolor="black")
    ax.set_facecolor("black")

    img = librosa.display.specshow(
        S_slice,
        sr=sr,
        hop_length=hop,
        x_axis="time",
        y_axis="log",
        fmin=F_MIN,
        fmax=F_MAX,
        cmap=CMAP,
        ax=ax,
    )
    img.set_clim(-80, 0)

    ax.set_xlabel("Time", color="white")
    ax.set_ylabel("Hz", color="white")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("white")

    for hz, label in [(30, "30 Hz"), (60, "60 Hz"), (100, "100 Hz")]:
        ax.axhline(hz, color="black", alpha=0.6, linestyle="--", linewidth=0.8)
        ax.text(0.01, hz, label, color="black", alpha=0.9, fontsize=8,
                transform=ax.get_yaxis_transform(), va="bottom")

    fig.colorbar(img, ax=ax, format="%+2.0f dB").ax.yaxis.set_tick_params(color="white", labelcolor="white")
    fig.tight_layout()

    # Black rectangle covering the unrevealed right portion
    # Use actual axis limits, not F_MIN/F_MAX, so the mask always covers the full plot
    x_max = n_cols * secs_per_bin
    y_min, y_max = ax.get_ylim()
    from matplotlib.patches import Rectangle
    mask = Rectangle((0, y_min), x_max, y_max - y_min, color="black", zorder=3)
    ax.add_patch(mask)

    playhead = ax.axvline(0, color="white", linewidth=1.5, alpha=0.85, zorder=4)

    n_frames = int((T_END - T_START) * FPS)

    def update(frame):
        t = (frame / n_frames) * (T_END - T_START)
        # Shrink the mask: move its left edge to t, cover only what's ahead
        mask.set_x(t)
        mask.set_width(x_max - t)
        playhead.set_xdata([t, t])
        return mask, playhead

    ani = animation.FuncAnimation(
        fig, update, frames=n_frames, interval=1000 / FPS, blit=True
    )

    out_path = OUTPUT_DIR / f"{TRACK}_{int(T_START)}s-{int(T_END)}s.mp4"
    silent_path = OUTPUT_DIR / f"{TRACK}_{int(T_START)}s-{int(T_END)}s_silent.mp4"

    writer = animation.FFMpegWriter(
        fps=FPS, bitrate=4000,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    ani.save(silent_path, dpi=150, writer=writer)

    # Mux the matching audio clip from the normalized WAV
    audio_path = AUDIO_DIR / f"{TRACK}.wav"
    if audio_path.exists():
        duration = T_END - T_START
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(silent_path),
            "-ss", str(T_START), "-t", str(duration), "-i", str(audio_path),
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(out_path),
        ], check=True, capture_output=True)
        silent_path.unlink()
        print(f"Saved (with audio): {out_path}")
    else:
        silent_path.rename(out_path)
        print(f"Saved (no audio found): {out_path}")


if __name__ == "__main__":
    main()
