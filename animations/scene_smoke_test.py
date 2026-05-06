"""
Smoke test for manim install.

Run with:
    manim -pql animations/scene_smoke_test.py SmokeTest

If this produces a video, your manim install works. If it doesn't, fix install
before doing anything else with manim.
"""

from manim import *


class SmokeTest(Scene):
    def construct(self):
        title = Text("Spectral History", font_size=48)
        subtitle = Text("Manim is working", font_size=28).next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))
