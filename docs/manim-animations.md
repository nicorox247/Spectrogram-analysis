# Manim Animations

## Strategy

Manim is reserved for the **showpiece** scenes where its strengths matter:
1. **The "what is a spectrogram" explainer** — needs smooth morphing between waveform, frequency-domain, and spectrogram representations. Manim is built for this.
2. **The final four-way comparison** — needs polished simultaneous animations and clean typography.

Everything else (per-track spectrograms with sweeping playheads) uses **matplotlib** instead. See `matplotlib_fallback/` for those.

This split is deliberate. Manim renders slowly and has a steeper iteration cycle. Matplotlib's `FuncAnimation` is faster to build and adequate for routine visualizations.

## Installation

```bash
pip install manim
# Verify
manim --version
```

System dependencies (needed by manim and ffmpeg):
- macOS: `brew install ffmpeg cairo pango`
- Ubuntu: `sudo apt install ffmpeg libcairo2-dev libpango1.0-dev`
- Windows: easiest path is WSL2 + Ubuntu instructions above

If installation has problems, the [manim Community docs](https://docs.manim.community) have platform-specific guides.

## First Verification

Before committing to manim for any scene, render the included `scene_smoke_test.py`. If it produces a video, your install works. If it doesn't, fix the install before doing anything else.

```bash
manim -pql animations/scene_smoke_test.py SmokeTest
```

`-p` previews after rendering, `-ql` is low quality (fast iteration).

## Render Quality Flags

| Flag | Resolution | Use case |
|------|-----------|----------|
| `-ql` | 480p15 | Iteration |
| `-qm` | 720p30 | Review |
| `-qh` | 1080p60 | Final |
| `-qk` | 4K60 | Don't bother for this project |

Always iterate with `-ql`. Bump to `-qh` only when a scene is finalized.

## Loading Pre-Computed Spectrograms

Spectrograms are computed in stage 2 of the pipeline and saved as `.npy` files. Load them in manim like this:

```python
import numpy as np
from manim import *

class MySpectrogramScene(Scene):
    def construct(self):
        # Load pre-computed data
        S_db = np.load("analysis/spectrogram_data/future_mask_off.npy")
        # S_db shape: (n_freq_bins, n_time_bins), dtype float32, values in [-80, 0] dB
        
        # Convert to displayable image
        # ... see image rendering pattern below
```

## Patterns

### Pattern: Display a spectrogram as an ImageMobject

The simplest way to get a spectrogram on screen in manim is to render it to a PNG with matplotlib first, then load that PNG as an `ImageMobject`. This avoids fighting with manim's color-mapping pipeline.

```python
# In a separate prep script or notebook
import matplotlib.pyplot as plt
import librosa.display
S_db = np.load("analysis/spectrogram_data/track.npy")
fig, ax = plt.subplots(figsize=(16, 9))
librosa.display.specshow(S_db, sr=44100, hop_length=1024,
                         x_axis='time', y_axis='log',
                         fmin=20, fmax=8000, cmap='magma', ax=ax)
plt.savefig("animations/assets/track_spectrogram.png", dpi=200, bbox_inches='tight')

# Then in manim
from manim import *
class TrackScene(Scene):
    def construct(self):
        spec = ImageMobject("animations/assets/track_spectrogram.png")
        spec.scale_to_fit_width(config.frame_width * 0.9)
        self.play(FadeIn(spec))
```

### Pattern: Sweeping playhead synced to audio

```python
class SpectrogramWithPlayhead(Scene):
    def construct(self):
        spec = ImageMobject("animations/assets/track.png")
        spec.scale_to_fit_width(12)
        self.add(spec)
        
        # Playhead is a vertical line that traverses the spectrogram width
        left_edge = spec.get_left()[0]
        right_edge = spec.get_right()[0]
        top = spec.get_top()[1]
        bottom = spec.get_bottom()[1]
        
        playhead = Line(
            start=[left_edge, bottom, 0],
            end=[left_edge, top, 0],
            color=YELLOW,
            stroke_width=3,
        )
        
        # Animate left-to-right over the audio duration
        AUDIO_DURATION = 15.0  # seconds
        self.add_sound("audio/normalized/track.wav")
        self.add(playhead)
        self.play(
            playhead.animate.shift(RIGHT * (right_edge - left_edge)),
            run_time=AUDIO_DURATION,
            rate_func=linear,
        )
```

### Pattern: Annotation that appears at a specific time

```python
def annotate_at(scene, time, mobject, duration=2.0):
    """Show an annotation at a given time offset from scene start."""
    scene.wait(time)
    scene.play(FadeIn(mobject), run_time=0.3)
    scene.wait(duration)
    scene.play(FadeOut(mobject), run_time=0.3)
```

For more complex synchronization, manage the timeline explicitly with `self.wait()` calls between events.

### Pattern: Side-by-side comparison

```python
class FourWayComparison(Scene):
    def construct(self):
        tracks = [
            ("Bach", "bach_passacaglia.png"),
            ("Zeppelin", "zeppelin_levee.png"),
            ("Scientist", "scientist_dub.png"),
            ("Future", "future_mask_off.png"),
        ]
        
        images = []
        for label, path in tracks:
            img = ImageMobject(f"animations/assets/{path}")
            img.scale_to_fit_width(3)
            images.append(img)
        
        group = Group(*images).arrange_in_grid(rows=2, cols=2, buff=0.3)
        labels = VGroup(*[Text(t[0], font_size=24) for t in tracks])
        for label, img in zip(labels, images):
            label.next_to(img, UP, buff=0.1)
        
        self.play(*[FadeIn(img) for img in images], FadeIn(labels))
        # ... add highlighting animations as needed
```

## Known Manim Quirks

- **API drift:** Manim's API has shifted across versions. If a code snippet from older tutorials doesn't work, check the current docs at docs.manim.community. Common gotchas: `ShowCreation` was renamed to `Create`; `TextMobject` was renamed to `Tex`; `add_updater` syntax has been stable but examples vary.
- **Caching:** Manim caches partial renders aggressively. If a change isn't appearing, delete the `media/` folder and re-render.
- **Coordinate system:** Default frame is roughly 14 units wide × 8 units tall. Use `config.frame_width` and `config.frame_height` instead of magic numbers.
- **Image scaling:** `ImageMobject.scale_to_fit_width()` and `scale_to_fit_height()` are usually what you want, not raw `.scale()`.
- **Audio sync:** `self.add_sound()` is the official way to add audio to a manim scene, but for the final video, you'll often add audio in the editor instead. The manim scenes should focus on the visuals.

## Fallback Strategy

If manim is fighting you on a specific scene, drop down to matplotlib. The video editor is happy to composite MP4 segments from any source. The argument is what matters; whether each frame was rendered by manim or matplotlib is invisible to the viewer.

The two scenes I most strongly recommend keeping in manim are the spectrogram explainer and the final comparison, because those are the moments where polished animation reads as care and rigor. Track-by-track spectrograms with playheads are equally effective in matplotlib.
