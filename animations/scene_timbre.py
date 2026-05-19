"""
Manim scene: "timbre" title card with concise definition.

Render:
    manim -pqh animations/scene_timbre.py TimbreScene

Output: media/videos/scene_timbre/1080p60/TimbreScene.mp4
"""

from manim import *


class TimbreScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Word ──────────────────────────────────────────────────────────────
        word = Text("timbre", font_size=96, color="#FDE724", slant=ITALIC)
        word.move_to(UP * 0.6)

        # ── Underline ─────────────────────────────────────────────────────────
        underline = Line(
            word.get_left()  + DOWN * 0.15,
            word.get_right() + DOWN * 0.15,
            color="#FDE724", stroke_width=2,
        )

        # ── Definition ────────────────────────────────────────────────────────
        defn = Text(
            "the tone quality that makes instruments\nsound distinct at the same pitch",
            font_size=32,
            color=WHITE,
            line_spacing=1.4,
        ).move_to(DOWN * 1.2)

        # ── Animate ───────────────────────────────────────────────────────────
        self.play(Write(word), run_time=1.4)
        self.play(Create(underline), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(defn, shift=UP * 0.15), run_time=1.0)
        self.wait(3.0)
