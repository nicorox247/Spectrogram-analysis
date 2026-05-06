# CLAUDE.md

This file gives Claude Code persistent context for this project. Read it at the start of every session.

## Project Summary

This is a final project for a Music Humanities course at Columbia. The deliverable is a ~20-minute video essay arguing that the audible floor of popular music has descended by roughly an octave over the past fifty years, enabled by electronic sound generation and subwoofer-capable playback technology. The argument is supported by spectral analysis (Fourier-based spectrograms) of canonical recordings from four traditions: acoustic classical, rock, dub/electronic, and hip-hop.

**Deadline: May 13, 2026.**

## Working Thesis

The lower edge of music's audible spectrum has descended by roughly an octave over the past fifty years, from the ~40 Hz floor of acoustic instruments to the sub-30 Hz territory routine in contemporary popular music. This shift is technological, not stylistic, and it has been aesthetically interpreted differently by rock, dub/electronic music, and hip-hop. The spectrograms reveal three distinct theories of what bass is and what it does.

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

- ~20 minutes of video, mostly voiceover discourse with synchronized spectrogram visualizations
- Audio examples total no more than 2 minutes (per rubric)
- Cited 5+ scholarly sources (see `docs/sources.md`)
- PDF of sources with embedded link to private video on Google Drive or Vimeo
- Submitted to Canvas by May 13, 2026

## Things to Avoid

- Don't recompute spectrograms inside manim's render loop (slow, wasteful)
- Don't use linear frequency scale (compresses bass into invisibility)
- Don't compare unnormalized tracks (dishonest)
- Don't use lossy audio sources (Spotify rips have artifacts that show up in spectrograms)
- Don't try to fully animate every spectrogram in manim — fall back to matplotlib for routine cases
- Don't bite off more than you can chew with manim — the project's argument is more important than maximally polished animations

## Open Questions / Decisions Pending

- Final track selection per genre (testing phase, see `docs/tracks.md`)
- Whether to use a Bach organ piece or Beethoven symphony as primary acoustic baseline (probably both, briefly)
- Voiceover recording setup (room, mic)

## When in Doubt

The argument is the project. Spectrograms are evidence for the argument. Animations are presentation of the evidence. If a technical decision is taking too long, choose the path that lets the argument come through clearly and move on.
