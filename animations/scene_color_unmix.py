"""
Color unmixing metaphor for timbre.

A single blended color separates into its primary components —
the way a spectrogram decomposes an instrument's timbre into
its constituent frequencies.

Render:
    manim -pqh animations/scene_color_unmix.py ColorUnmixScene

Output: media/videos/scene_color_unmix/1080p60/ColorUnmixScene.mp4
"""

from manim import *

MIXED  = "#A0673A"   # warm brown  — the blended timbre
C_RED  = "#E05252"   # red
C_YEL  = "#D4A820"   # yellow
C_BLU  = "#4A72E0"   # blue


class ColorUnmixScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Mixed color circle ─────────────────────────────────────────────────
        mixed = Circle(radius=1.6, fill_color=MIXED, fill_opacity=1, stroke_width=0)
        mixed.shift(UP * 0.6)

        lbl_mixed = Text("timbre", font_size=36, color=WHITE, slant=ITALIC)
        lbl_mixed.next_to(mixed, DOWN, buff=0.35)

        self.play(FadeIn(mixed), run_time=0.7)
        self.play(Write(lbl_mixed), run_time=0.6)
        self.wait(1.8)

        # ── Component circles (born at the mixed circle's center) ─────────────
        R = 0.85
        c_red = Circle(radius=R, fill_color=C_RED, fill_opacity=0, stroke_width=0)
        c_yel = Circle(radius=R, fill_color=C_YEL, fill_opacity=0, stroke_width=0)
        c_blu = Circle(radius=R, fill_color=C_BLU, fill_opacity=0, stroke_width=0)

        for c in (c_red, c_yel, c_blu):
            c.move_to(mixed.get_center())

        self.add(c_red, c_yel, c_blu)

        # ── Unmix: components spread out as mixed fades ────────────────────────
        Y_COMP = -1.6
        SEP    =  3.0

        self.play(
            mixed.animate.set_opacity(0),
            FadeOut(lbl_mixed, shift=UP * 0.1),
            c_red.animate.move_to([-SEP, Y_COMP, 0]).set_fill(C_RED, opacity=1),
            c_yel.animate.move_to([   0, Y_COMP, 0]).set_fill(C_YEL, opacity=1),
            c_blu.animate.move_to([ SEP, Y_COMP, 0]).set_fill(C_BLU, opacity=1),
            run_time=1.4, rate_func=smooth,
        )
        self.remove(mixed)

        # ── Component labels ───────────────────────────────────────────────────
        lbl_r = Text("red",    font_size=30, color=C_RED).next_to(c_red, DOWN, buff=0.28)
        lbl_y = Text("yellow", font_size=30, color=C_YEL).next_to(c_yel, DOWN, buff=0.28)
        lbl_b = Text("blue",   font_size=30, color=C_BLU).next_to(c_blu, DOWN, buff=0.28)

        self.play(FadeIn(lbl_r), FadeIn(lbl_y), FadeIn(lbl_b), run_time=0.6)
        self.wait(3.0)
