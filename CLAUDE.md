# CLAUDE.md

This file gives Claude Code persistent context for this project. Read it at the start of every session.

## Project Summary

This is a final project for a Music Humanities course at Columbia. The deliverable is a ~20-minute video essay tracing how Joseph Fourier's early-1800s mathematics — developed to study heat conduction — became the secret foundation of nearly every form of modern sound manipulation: synthesizers, samplers, Auto-Tune, drum machines, and digital audio production.

**Deadline: May 13, 2026.**

## Working Thesis

Joseph Fourier's work on heat conduction, made computationally practical by the Cooley-Tukey FFT algorithm in 1965, became the mathematical foundation for synthesizers, samplers, Auto-Tune, MP3 compression, and digital audio workstations. The video traces this lineage by analyzing the spectrograms of acoustic instruments and contrasting them with synthesized and digitally processed sounds. Tone is pedagogical and warm — closer to 3Blue1Brown than to an academic essay.

**Narrative arc:** Hook → Establish the FT as an *analytical* tool only → Use it as a microscope on acoustic instruments → Pivot: the FFT arrives and you can run the process *in reverse* → Cascade of consequences (synthesis, sampling, Auto-Tune) → Reflection → Close.

## Project Structure

```
spectral-history/
├── CLAUDE.md                  # This file — read first
├── README.md                  # Human-facing project overview
├── docs/
│   ├── architecture.md        # Technical pipeline design
│   ├── audio-analysis.md      # librosa / spectrogram conventions
│   ├── manim-animations.md    # Animation patterns and gotchas
│   ├── tracks.md              # Canonical recordings and timing
│   ├── sources.md             # Scholarly sources for citations
│   ├── script.md              # Full video script (drafted as project develops)
│   └── schedule.md            # Day-by-day working plan
├── audio/                     # WAV files (gitignored — too large)
├── analysis/
│   ├── compute_spectrograms.py  # Pre-compute all spectrograms
│   ├── normalize_loudness.py    # LUFS normalization step
│   └── spectrogram_data/        # Saved .npy arrays
├── animations/
│   ├── scene_intro.py
│   ├── scene_what_is_spectrogram.py
│   ├── scene_acoustic.py
│   ├── scene_rock.py
│   ├── scene_dub.py
│   ├── scene_hiphop.py
│   ├── scene_conclusion.py
│   └── shared/                  # Reusable components (playhead, axes, etc.)
├── matplotlib_fallback/         # Backup plots if manim hits walls
└── output/                      # Rendered video files
```

## Critical Conventions

**Spectrogram parameters MUST be consistent across all tracks** for the comparison to be honest. Use these defaults everywhere:
- Sample rate: 44100 Hz (resample if needed)
- `n_fft`: 4096
- `hop_length`: 1024 (n_fft // 4)
- Window: Hann (default)
- Frequency scale: log
- Display range: 20 Hz to 8000 Hz
- dB floor: -80 dB (clipped)
- Color map: `magma`

**Loudness normalization is required.** Use `pyloudnorm` to normalize all tracks to -23 LUFS before computing spectrograms. Without this, comparisons are dishonest because louder masters look spectrally denser regardless of actual content.

**Pipeline separation.** librosa computes spectrograms, saves to `.npy`. manim loads `.npy` and animates. NEVER recompute spectrograms inside manim — rendering is too slow.

## Toolchain

- Python 3.11+
- librosa (audio analysis)
- numpy (array math)
- matplotlib (prototyping and fallback animations)
- pyloudnorm (LUFS normalization)
- manim Community Edition — install via `pip install manim` (NOT the 3Blue1Brown original repo)
- ffmpeg (system dependency for manim and audio handling)

## Hybrid Animation Strategy

Manim is used for showpiece moments only:
1. The "what is a spectrogram" explanatory section (waveform → FFT → spectrogram morphing)
2. The final side-by-side comparison of all four tracks

Routine "spectrogram with sweeping playhead" sections use matplotlib `FuncAnimation` exported as MP4, then composited in the video editor. This is faster to iterate and less risky than rendering everything in manim.

## What "Done" Looks Like

- ~20 minutes of video, mostly voiceover with synchronized spectrogram visualizations
- Audio examples total no more than 2 minutes (per rubric) — ~8 short clips planned
- Cited 5+ scholarly sources (see `docs/sources.md`)
- PDF of sources with embedded link to private video on Google Drive or Vimeo
- Submitted to Canvas by May 13, 2026

## Things to Avoid

- Don't recompute spectrograms inside manim's render loop (slow, wasteful)
- Don't use linear frequency scale (compresses harmonics into invisibility)
- Don't compare unnormalized tracks (dishonest)
- Don't use lossy audio sources (Spotify rips have artifacts that show up in spectrograms)
- Don't try to fully animate every spectrogram in manim — fall back to matplotlib for routine cases
- Don't introduce the synthesis/reverse-FT concept before Section 4 — the dramatic reveal depends on the viewer not seeing it coming

## Open Questions / Decisions Pending

- Final audio example selection per section (bar is "clearly illustrates the point," not "canonically iconic")
- Voiceover recording setup (room, mic)

## When in Doubt

The narrative is the project. Spectrograms are the visual evidence. Animations are presentation of that evidence. If a technical decision is taking too long, choose the path that lets the story come through clearly and move on.
