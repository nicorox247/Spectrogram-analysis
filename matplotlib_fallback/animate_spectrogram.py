"""
Animate a spectrogram segment with a sweeping playhead.
Loads pre-computed .npy data — do not recompute here.
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import librosa.display

DATA_DIR = Path("analysis/spectrogram_data")
OUTPUT_DIR = Path("output")

TRACK = "Bach_Fugue_in_C-minor"
T_START = 56.0   # seconds
T_END   = 77.0   # seconds

F_MIN = 20
F_MAX = 8000
CMAP  = "magma"
FPS   = 30


def main() -> None:
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
        ax.axhline(hz, color="white", alpha=0.3, linestyle="--", linewidth=0.8)
        ax.text(0.01, hz, label, color="white", alpha=0.6, fontsize=8,
                transform=ax.get_yaxis_transform(), va="bottom")

    fig.colorbar(img, ax=ax, format="%+2.0f dB").ax.yaxis.set_tick_params(color="white", labelcolor="white")
    fig.tight_layout()

    # Black rectangle covering the unrevealed right portion
    x_max = n_cols * secs_per_bin
    from matplotlib.patches import Rectangle
    mask = Rectangle((0, F_MIN), x_max, F_MAX - F_MIN, color="black", zorder=3)
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
    writer = animation.FFMpegWriter(
        fps=FPS, bitrate=4000,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    ani.save(out_path, dpi=150, writer=writer)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
