# Spectral History: A Video Essay on Bass and Technology

A final project for Music Humanities arguing that the audible floor of popular music has descended by roughly an octave in the past fifty years, traced through spectrograms of canonical recordings from acoustic classical, rock, dub/electronic, and hip-hop traditions.

## Quick Start

```bash
# Set up environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Verify manim install
manim --version

# Place WAV files in audio/ (gitignored)
# Then run the analysis pipeline
python analysis/normalize_loudness.py
python analysis/compute_spectrograms.py

# Render an animation scene
manim -pql animations/scene_what_is_spectrogram.py SpectrogramExplainer
```

## Documentation

- `CLAUDE.md` — Persistent context for Claude Code sessions
- `docs/architecture.md` — Technical pipeline design
- `docs/audio-analysis.md` — Spectrogram parameters and conventions
- `docs/manim-animations.md` — Animation patterns
- `docs/tracks.md` — Canonical recordings and timing decisions
- `docs/sources.md` — Scholarly bibliography
- `docs/script.md` — Video essay script (in progress)
- `docs/schedule.md` — Working schedule through May 13

## Deliverables

1. ~20 minute video essay (uploaded privately to Drive or Vimeo)
2. PDF of cited sources with link to video
3. Submitted to Canvas by **May 13, 2026**
