"""
Generate preview PNGs of all computed spectrograms for visual comparison.

Use this to pick canonical tracks: lay out the previews side by side and choose
the ones whose spectrograms most clearly visualize the argument for their section.
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

DATA_DIR = Path("analysis/spectrogram_data")
PREVIEW_DIR = Path("analysis/previews")

# Display parameters — these match the values that will be used in the final video
F_MIN = 20
F_MAX = 8000
CMAP = "magma"


def render_preview(npy_path: Path, json_path: Path, output_path: Path) -> None:
    """Render one spectrogram as a PNG preview."""
    S_db = np.load(npy_path)
    with json_path.open() as f:
        meta = json.load(f)

    fig, ax = plt.subplots(figsize=(16, 6))
    img = librosa.display.specshow(
        S_db,
        sr=meta["sample_rate"],
        hop_length=meta["hop_length"],
        x_axis="time",
        y_axis="log",
        fmin=F_MIN,
        fmax=F_MAX,
        cmap=CMAP,
        ax=ax,
    )
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    ax.set_title(meta["source_file"])
    ax.set_ylim(F_MIN, F_MAX)

    # Reference lines for key frequencies
    for hz, label in [(30, "30 Hz"), (60, "60 Hz"), (100, "100 Hz")]:
        ax.axhline(hz, color="white", alpha=0.3, linestyle="--", linewidth=0.8)
        ax.text(0.02, hz, label, color="white", alpha=0.7, fontsize=8,
                transform=ax.get_yaxis_transform(), va="bottom")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    npy_files = sorted(DATA_DIR.glob("*.npy"))
    if not npy_files:
        print(f"No spectrogram data in {DATA_DIR}")
        print("Run compute_spectrograms.py first.")
        return

    print(f"Rendering {len(npy_files)} previews...")
    for npy in npy_files:
        json_path = npy.with_suffix(".json")
        if not json_path.exists():
            print(f"  SKIPPED (no metadata): {npy.name}")
            continue
        out_path = PREVIEW_DIR / f"{npy.stem}.png"
        if out_path.exists():
            print(f"  SKIPPED (already rendered): {npy.name}")
            continue
        render_preview(npy, json_path, out_path)
        print(f"  {npy.name} -> {out_path.name}")
    print("Done.")


if __name__ == "__main__":
    main()
