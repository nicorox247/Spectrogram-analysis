"""
Generic source card — types out any citation in the same style.

Usage:
    python animations/scene_source_card.py "Sethares, William A. Tuning, Timbre, Spectrum, Scale. 2nd ed. Springer, 2005."
    python animations/scene_source_card.py "Chowning, John. ..." --out output/sources/chowning.mp4
    python animations/scene_source_card.py "..." --quality l   # fast preview

Output: output/sources/<slugified_first_word>.mp4  (or --out path)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

_TEXT = os.environ.get("SOURCE_TEXT", "")


class SourceCardScene:
    pass


# ── Manim scene (only executed when manim imports this file) ──────────────────

if _TEXT:
    import textwrap
    from manim import *

    class SourceCardScene(Scene):
        def construct(self):
            self.camera.background_color = BLACK

            label = Text("Source:", font_size=32, color="#AAAAAA")
            wrapped = "\n".join(textwrap.wrap(_TEXT, width=62))
            citation = Text(
                wrapped,
                font_size=28,
                color=WHITE,
                line_spacing=1.4,
            )

            label.to_edge(LEFT, buff=1.0).shift(UP * 0.2)
            citation.next_to(label, DOWN, buff=0.3).align_to(label, LEFT)

            self.play(Write(label), run_time=0.6)
            self.play(AddTextLetterByLetter(citation), run_time=max(2.0, len(_TEXT) * 0.04))
            self.wait(2.5)


# ── CLI wrapper ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("text",      help="Full citation text (wrap in quotes)")
    p.add_argument("--out",     help="Output path (default: output/sources/<slug>.mp4)", default=None)
    p.add_argument("--quality", default="h", choices=["l", "m", "h", "k"])
    args = p.parse_args()

    # Derive a filename slug from the first word of the citation (usually last name)
    slug = re.sub(r"[^a-zA-Z0-9]", "", args.text.split()[0].lower()) or "source"
    out_path = Path(args.out) if args.out else Path(f"output/sources/{slug}.mp4")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["SOURCE_TEXT"] = args.text

    result = subprocess.run([
        sys.executable, "-m", "manim",
        f"-pq{args.quality}",
        "--media_dir", "media",
        "--output_file", slug,
        __file__, "SourceCardScene",
    ], env=env)

    if result.returncode == 0:
        quality_dir = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
        src = Path("media/videos/scene_source_card") / quality_dir[args.quality] / f"{slug}.mp4"
        if src.exists():
            shutil.move(str(src), str(out_path))
            print(f"\nSaved: {out_path}")

    sys.exit(result.returncode)
