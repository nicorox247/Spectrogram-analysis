# The Hidden Math Behind Sound

A final project for Music Humanities at Columbia University tracing how Joseph Fourier's early-1800s mathematics — developed to study heat conduction — became the secret foundation of nearly every form of modern sound manipulation: synthesizers, samplers, Auto-Tune, drum machines, and digital audio production.

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

# Render an animation scene (example)
manim -pqh animations/scene_title_card.py TitleCardScene
```

## Animation Scenes

| File | Scene | Description |
|------|-------|-------------|
| `scene_title_card.py` | `TitleCardScene` | Opening title card |
| `scene_fourier_buildup.py` | `FourierBuildupScene` | Sine wave decomposition buildup |
| `scene_color_unmix.py` | `ColorUnmixScene` | Timbre-as-color metaphor |
| `scene_dft_cost.py` | `DFTCostScene` | O(N²) DFT cost visualization |
| `scene_fft_speedup.py` | `FFTSpeedupScene` | FFT compression speedup |
| `scene_source_card.py` | `SourceCardScene` | Generic citation card (CLI) |
| `scene_closing_card.py` | `ClosingCardScene` | Closing credits card |

### Rendering source cards

```bash
python animations/scene_source_card.py "Author. Title. Publisher, Year."
python animations/scene_source_card.py "..." --out output/sources/custom.mp4
```

### Generating YouTube citations

```bash
# Appends Chicago-style citations to docs/bibliography.md
grep -oE 'https?://[^ ]+' docs/youtube-links.md | xargs python docs/youtube_cite.py
```

## Documentation

- `CLAUDE.md` — Persistent context for Claude Code sessions
- `docs/bibliography.md` — Full bibliography (books, articles, audio, video)
- `docs/youtube-links.md` — YouTube source URLs
- `docs/architecture.md` — Technical pipeline design
- `docs/script.md` — Video essay script (in progress)
- `docs/schedule.md` — Working schedule

## Deliverables

1. ~20 minute video essay (uploaded privately to Drive or Vimeo)
2. PDF of cited sources with link to video
3. Submitted to Canvas by **May 13, 2026**

## Course

Music Humanities, Spring 2026 — Columbia University
Prof. Garcia Orozco
