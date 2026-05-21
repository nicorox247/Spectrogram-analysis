"""
Closing card.

Render:
    manim -pqh animations/scene_closing_card.py ClosingCardScene

Output: media/videos/scene_closing_card/1080p60/ClosingCardScene.mp4
"""

from manim import *

YELLOW = "#FDE724"


class ClosingCardScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        name       = Text("Nick Felix",              font_size=64, color=YELLOW,    weight=BOLD)
        course     = Text("Music Humanities",        font_size=36, color=WHITE)
        semester   = Text("Spring 2026",             font_size=32, color="#AAAAAA")
        professor  = Text("Prof. Garcia Orozco",     font_size=32, color="#AAAAAA")
        university = Text("Columbia University",     font_size=28, color="#777777")

        name.move_to(UP * 1.6)
        course.next_to(name,      DOWN, buff=0.45)
        semester.next_to(course,  DOWN, buff=0.18)
        professor.next_to(semester, DOWN, buff=0.18)
        university.next_to(professor, DOWN, buff=0.35)

        self.play(FadeIn(name, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(course),    run_time=0.5)
        self.play(FadeIn(semester),  run_time=0.4)
        self.play(FadeIn(professor), run_time=0.4)
        self.play(FadeIn(university, shift=DOWN * 0.05), run_time=0.5)
        self.wait(4.0)
