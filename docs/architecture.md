# Architecture

## Pipeline Overview

The project is structured as three independent stages connected by serialized intermediate data. This separation matters because each stage has different speed and iteration characteristics.

```
[Raw WAV files]
       │
       ▼
[Stage 1: Normalize loudness] ──> normalized WAVs
       │
       ▼
[Stage 2: Compute spectrograms] ──> .npy arrays + metadata JSON
       │
       ▼
[Stage 3: Animate]
       ├── manim (showpiece scenes) ──> MP4 segments
       └── matplotlib (routine scenes) ──> MP4 segments
       │
       ▼
[Stage 4: Composite in video editor]
       │
       ▼
[Final video MP4]
```

## Why this separation

- **Audio analysis is fast and well-debugged.** librosa runs in seconds. Don't redo it just because you're tweaking a visual.
- **Manim rendering is slow.** A 30-second high-quality manim render can take many minutes. You want to render only the visual pipeline, not the audio analysis pipeline, when you iterate.
- **Different tools have different strengths.** The video editor is the right place to assemble final output, sync voiceover, and add titles. Don't try to make manim do compositing.

## Stage 1: Loudness Normalization

**Why:** Master loudness varies enormously across eras. A 2015 trap track is mastered ~10 dB louder than a 1971 rock recording. Without normalization, the trap track's spectrogram will look brighter everywhere — including in frequency regions where it doesn't actually have more content. This makes comparisons dishonest.

**Approach:** Use `pyloudnorm` to measure integrated LUFS for each track and apply gain to bring all tracks to -23 LUFS (broadcast standard). Save normalized WAVs to a separate folder; never overwrite originals.

**Output:** `audio/normalized/{track_id}.wav`

## Stage 2: Spectrogram Computation

**Why:** Centralize the FFT settings so every spectrogram in the video uses the same parameters. The comparison only works if the parameters are identical.

**Approach:** For each normalized WAV, compute STFT using librosa with the canonical parameters from `audio-analysis.md`. Save the resulting magnitude array as `.npy` plus a JSON sidecar with metadata (sample rate, hop length, n_fft, frequency bins, time bins, source filename).

**Output:**
- `analysis/spectrogram_data/{track_id}.npy` — 2D float32 array of dB values
- `analysis/spectrogram_data/{track_id}.json` — metadata sidecar

## Stage 3: Animation

Two parallel paths:

**Manim (showpiece scenes):**
- The "what is a spectrogram" explanatory section
- The final four-way comparison

These benefit from manim's smooth transformations and polished math/text rendering.

**Matplotlib (routine scenes):**
- Each track's spectrogram with a sweeping playhead and annotations

These are visually simpler — a static spectrogram with a vertical line moving across — and matplotlib's `FuncAnimation` exports MP4 directly via ffmpeg. Much faster iteration than manim.

## Stage 4: Final Compositing

Use a video editor (DaVinci Resolve recommended; iMovie or Premiere also fine) to:
- Place voiceover audio on the timeline
- Sync animation MP4s to the voiceover
- Insert audio examples (kept under 2 minutes total per rubric)
- Add title cards, section headers, and any text overlays
- Export final MP4

## Coordinate Conventions

When working with spectrogram arrays:
- `S[freq_bin, time_bin]` — librosa's standard layout
- Frequency bin 0 is DC (0 Hz)
- Use `librosa.fft_frequencies()` to get bin → Hz mapping
- Use `librosa.frames_to_time()` to get bin → seconds mapping

When passing to visualization:
- Always plot with origin at bottom-left (low frequency at bottom)
- Time on x-axis (left to right)
- Frequency on y-axis (log scale)
- Color/intensity for amplitude (dB)

## Performance Notes

- Spectrograms for full-length tracks can be large. For final animation, you usually want a 15-30 second representative segment, not the full track. Compute the full spectrogram once, then slice for animation.
- Manim render times scale with quality flag: `-ql` (low) for iteration, `-qm` (medium) for review, `-qh` (high) for final. Use `-ql` until you're happy, then bump up.
- If manim is unbearably slow on your machine, render at low quality and upscale in the video editor — the difference is rarely visible at YouTube/Vimeo bitrates.
