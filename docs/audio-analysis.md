# Audio Analysis Conventions

All spectrograms in this project must be computed with identical parameters. The argument depends on honest comparison, which requires consistent analysis.

## Canonical Parameters

```python
SAMPLE_RATE = 44100
N_FFT = 4096
HOP_LENGTH = 1024  # n_fft // 4
WINDOW = 'hann'    # librosa default
```

## Why These Values

**Sample rate (44100 Hz):** Standard CD quality. Matches the source material. Captures up to 22050 Hz (Nyquist), which is more than enough for our 8 kHz display ceiling.

**FFT size (4096):** Frequency resolution at 44.1 kHz with n_fft=4096 is ~10.77 Hz. This matters because the project's argument hinges on distinguishing 30 Hz from 40 Hz from 50 Hz — differences that are tiny in absolute terms but huge perceptually. Smaller FFT sizes (e.g., 1024) would smear these together.

The cost is time resolution: with hop_length=1024, each spectrogram column represents ~23ms of audio. That's fine for music — fast enough to capture transients like kick drums, slow enough that the visualization isn't jittery.

**Hop length (n_fft // 4):** Standard 75% overlap between windows. Smooth visualization without wasting computation.

## Loudness Normalization

Use `pyloudnorm` and target -23 LUFS:

```python
import pyloudnorm as pyln
import soundfile as sf

data, rate = sf.read(input_path)
meter = pyln.Meter(rate)
loudness = meter.integrated_loudness(data)
normalized = pyln.normalize.loudness(data, loudness, -23.0)
sf.write(output_path, normalized, rate)
```

**Critical:** Do this BEFORE computing spectrograms. Save normalized WAVs to a separate directory. Don't overwrite originals.

## Display Settings

When converting magnitude spectrograms to dB for display:

```python
import librosa
import numpy as np

S = librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH)
S_mag = np.abs(S)
S_db = librosa.amplitude_to_db(S_mag, ref=np.max)

# Clip floor for clean visualization
S_db = np.clip(S_db, -80, 0)
```

**Frequency display range:** 20 Hz to 8000 Hz. Below 20 Hz is inaudible (and noise-prone in recordings). Above 8 kHz is mostly cymbals and noise — not where this project's argument lives, and showing it wastes vertical space that could go to the bass region.

**Frequency scale:** Logarithmic, always. Linear frequency scale puts every octave in a smaller and smaller band as you go up, which makes the bass register (where this project lives!) compressed into the bottom 5% of the image. Log scale gives each octave equal visual space, matching how human pitch perception works.

**Color map:** `magma`. It's perceptually uniform (so brightness genuinely tracks intensity), reads well on video, and looks contemporary. Avoid `jet` — it's perceptually misleading and looks dated. `viridis` is also fine.

## Reference Frequencies for Annotations

When annotating spectrograms in the video, these reference points are worth marking:

| Frequency | Reference |
|-----------|-----------|
| 20 Hz | Bottom of human hearing |
| 27.5 Hz | A0 — lowest note on standard piano |
| 30 Hz | Approximate floor of 808 sub-bass |
| 41 Hz | E1 — lowest note on bass guitar (standard tuning) |
| 65 Hz | C2 — common kick drum fundamental region |
| 110 Hz | A2 — bottom of male vocal range |
| 220 Hz | A3 — middle of vocal range |
| 440 Hz | A4 — concert pitch |
| 1000 Hz | Reference 1 kHz |

## Test Workflow for Track Selection

When picking which track per genre to use as the canonical example:

1. Drop 3-4 candidates per genre into `audio/raw/`
2. Run normalization on all of them
3. Run spectrogram computation on all of them
4. Generate matplotlib PNG previews side by side
5. Choose based on which spectrograms most clearly show the argument

The goal is visual clarity in service of the argument. A track you love won't help if its spectrogram is a muddle, and a track you're neutral on can carry the project if its spectrogram tells the cleanest story.

## Common Gotchas

- **MP3 sources** have low-pass filtering above ~16 kHz and other artifacts. Use WAV or FLAC.
- **YouTube rips** are double-lossy if the original was already compressed. Avoid.
- **Stereo vs mono:** Sum to mono for spectrogram analysis (`librosa.load` does this by default with `mono=True`). Stereo spectrograms are visually confusing for this purpose.
- **Clipping:** Some loud masters are already clipping. Normalization down to -23 LUFS will help, but check waveforms for hard clipping artifacts that will show up as broadband noise in the spectrogram.
- **Silence at start/end** of tracks affects LUFS measurement. If a track has a long fade-in, consider trimming before normalizing.
