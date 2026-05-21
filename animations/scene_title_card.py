"""
Title card: "The Hidden Math Behind Sound"

Render:
    manim -pqh animations/scene_title_card.py TitleCardScene

Output: media/videos/scene_title_card/1080p60/TitleCardScene.mp4
"""

from manim import *

YELLOW = "#FDE724"


class TitleCardScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        subtitle = Text("the", font_size=36, color="#AAAAAA", slant=ITALIC)
        title1   = Text("Hidden Math", font_size=96, color=YELLOW, weight=BOLD)
        title2   = Text("Behind Sound", font_size=96, color=WHITE, weight=BOLD)

        subtitle.move_to(UP * 2.0)
        title1.next_to(subtitle, DOWN, buff=0.2)
        title2.next_to(title1, DOWN, buff=0.15)

        self.play(FadeIn(subtitle, shift=DOWN * 0.15), run_time=0.7)
        self.play(Write(title1), run_time=1.2)
        self.play(FadeIn(title2, shift=UP * 0.1), run_time=0.8)
        self.wait(3.0)
