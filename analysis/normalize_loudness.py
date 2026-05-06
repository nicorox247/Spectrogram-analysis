"""
Normalize loudness of all WAV files in audio/raw/ to -23 LUFS.

This is critical for honest spectrogram comparison: louder masters look spectrally
denser regardless of actual content. Always run this before computing spectrograms.

Outputs go to audio/normalized/ with the same filenames.
"""

from pathlib import Path
import soundfile as sf
import pyloudnorm as pyln
import numpy as np

TARGET_LUFS = -23.0  # Broadcast standard

INPUT_DIR = Path("audio/raw")
OUTPUT_DIR = Path("audio/normalized")


def normalize_file(input_path: Path, output_path: Path) -> None:
    """Normalize one WAV file to TARGET_LUFS."""
    data, rate = sf.read(input_path)

    # If stereo, measure on the stereo signal but keep stereo for output
    meter = pyln.Meter(rate)
    loudness = meter.integrated_loudness(data)

    if np.isinf(loudness):
        print(f"  SKIPPED (silent or too short): {input_path.name}")
        return

    normalized = pyln.normalize.loudness(data, loudness, TARGET_LUFS)
    sf.write(output_path, normalized, rate)
    print(f"  {input_path.name}: {loudness:+.1f} LUFS -> {TARGET_LUFS:+.1f} LUFS")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    wavs = sorted(INPUT_DIR.glob("*.wav")) + sorted(INPUT_DIR.glob("*.flac"))
    if not wavs:
        print(f"No audio files found in {INPUT_DIR}")
        return

    print(f"Normalizing {len(wavs)} files to {TARGET_LUFS} LUFS...")
    for wav in wavs:
        out = OUTPUT_DIR / f"{wav.stem}.wav"
        normalize_file(wav, out)
    print("Done.")


if __name__ == "__main__":
    main()
