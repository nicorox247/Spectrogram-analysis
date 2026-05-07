"""
Compute spectrograms for all normalized WAV files and save as .npy + JSON sidecar.

Uses the canonical parameters defined in docs/audio-analysis.md. All spectrograms
in the project must use these parameters for honest comparison.
"""

from pathlib import Path
import json
import numpy as np
import librosa
import soundfile as sf

# Canonical parameters — DO NOT CHANGE without updating docs/audio-analysis.md
SAMPLE_RATE = 44100
N_FFT = 4096
HOP_LENGTH = 1024  # n_fft // 4
DB_FLOOR = -80.0

INPUT_DIR = Path("audio/normalized")
OUTPUT_DIR = Path("analysis/spectrogram_data")


def compute_spectrogram(wav_path: Path) -> tuple[np.ndarray, dict]:
    """Compute log-magnitude spectrogram and metadata for one file."""
    # Load mono at canonical sample rate
    y, sr = librosa.load(wav_path, sr=SAMPLE_RATE, mono=True)

    # Short-time Fourier transform
    S = librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH)
    S_mag = np.abs(S)
    S_db = librosa.amplitude_to_db(S_mag, ref=np.max)
    S_db = np.clip(S_db, DB_FLOOR, 0.0).astype(np.float32)

    # Metadata
    n_freq, n_time = S_db.shape
    metadata = {
        "source_file": wav_path.name,
        "sample_rate": SAMPLE_RATE,
        "n_fft": N_FFT,
        "hop_length": HOP_LENGTH,
        "db_floor": DB_FLOOR,
        "n_freq_bins": int(n_freq),
        "n_time_bins": int(n_time),
        "duration_seconds": float(len(y) / sr),
        "freq_bin_hz": float(SAMPLE_RATE / N_FFT),
        "time_bin_seconds": float(HOP_LENGTH / SAMPLE_RATE),
    }
    return S_db, metadata


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    wavs = sorted(INPUT_DIR.glob("*.wav"))
    if not wavs:
        print(f"No normalized WAVs found in {INPUT_DIR}")
        print("Run normalize_loudness.py first.")
        return

    print(f"Computing spectrograms for {len(wavs)} files...")
    for wav in wavs:
        npy_path = OUTPUT_DIR / f"{wav.stem}.npy"
        json_path = OUTPUT_DIR / f"{wav.stem}.json"

        if npy_path.exists() and json_path.exists():
            print(f"  SKIPPED (already computed): {wav.name}")
            continue

        S_db, metadata = compute_spectrogram(wav)
        np.save(npy_path, S_db)
        with json_path.open("w") as f:
            json.dump(metadata, f, indent=2)

        print(f"  {wav.name}: {S_db.shape}, {metadata['duration_seconds']:.1f}s")
    print("Done.")


if __name__ == "__main__":
    main()
