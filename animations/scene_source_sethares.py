"""
Source card: Sethares citation.

Render:
    manim -pqh animations/scene_source_sethares.py SourceSetharesScene
"""

from manim import *


class SourceSetharesScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        label = Text("Source:", font_size=32, color="#AAAAAA")
        citation = Text(
            "Sethares, William A. Tuning, Timbre, Spectrum, Scale.\n"
            "2nd ed. Springer, 2005.",
            font_size=28,
            color=WHITE,
            line_spacing=1.4,
        )

        label.to_edge(LEFT, buff=1.0).shift(UP * 0.2)
        citation.next_to(label, DOWN, buff=0.3).align_to(label, LEFT)

        self.play(Write(label), run_time=0.6)
        self.play(AddTextLetterByLetter(citation), run_time=3.5)
        self.wait(2.5)
