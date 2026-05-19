"""
A4 fundamental and its first 3 harmonics — Russian stacking doll reveal.

Each harmonic emerges from the previous one: starts tiny at the parent's
position, then scales up and moves to its own spot.

Render:
    manim -pqh animations/scene_harmonics.py HarmonicsScene

Output: media/videos/scene_harmonics/1080p60/HarmonicsScene.mp4
"""

from manim import *

HARMONICS = [
    #  freq   font_size   color       y
    (  440,      80,    "#FDE724",  -2.1 ),   # fundamental — cividis yellow
    (  880,      62,    "#FCA636",  -0.6 ),   # 2nd harmonic
    ( 1320,      48,    "#E06448",   0.7 ),   # 3rd
    ( 1760,      38,    "#B12A90",   1.8 ),   # 4th
]


class HarmonicsScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        labels = []
        for freq, size, color, y in HARMONICS:
            lbl = Text(f"{freq} Hz", font_size=size, color=color)
            lbl.move_to([0, y, 0])
            labels.append(lbl)

        # Fundamental appears
        self.play(Write(labels[0]), run_time=1.2)
        self.wait(1.0)

        # Each harmonic emerges from its parent
        for i in range(1, len(labels)):
            ghost = labels[i].copy()
            ghost.move_to(labels[i - 1].get_center())
            ghost.scale(0.01)
            self.add(ghost)
            self.play(
                ReplacementTransform(ghost, labels[i]),
                run_time=1.2,
                rate_func=smooth,
            )
            self.wait(0.8)

        self.wait(2.0)
