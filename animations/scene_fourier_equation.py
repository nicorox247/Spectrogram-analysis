"""
Manim scene for Section 2b — Fourier transform equation.

The equation appears, then each term is highlighted in sequence
as the voiceover explains what it means. Designed as b-roll:
generous pauses between highlights give room for syncing in Resolve.

Render:
    manim -pqh animations/scene_fourier_equation.py FourierEquation

Output lands in media/videos/scene_fourier_equation/1080p60/
"""

from manim import *


class FourierEquation(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Equation ──────────────────────────────────────────────────
        eq = MathTex(
            r"F(f)",           # 0 — output: frequency fingerprint
            r"=",              # 1
            r"\int_{-\infty}^{\infty}",  # 2 — integral: average over time
            r"x(t)",           # 3 — your signal
            r"\,e^{-2\pi i f t}",        # 4 — pure sine at frequency f
            r"\,dt",           # 5 — (part of integral)
            font_size=64,
        )
        eq.set_color(WHITE)
        eq.move_to(ORIGIN + UP * 0.5)

        # ── Appear ────────────────────────────────────────────────────
        self.play(Write(eq), run_time=2.5)
        self.wait(2.0)

        # ── x(t): your signal ─────────────────────────────────────────
        lbl_xt = Text("your signal", font_size=30, color=YELLOW)
        lbl_xt.next_to(eq[3], DOWN, buff=1.0)
        line_xt = Line(
            eq[3].get_bottom() + DOWN * 0.15,
            lbl_xt.get_top() + UP * 0.15,
            color=YELLOW, stroke_width=1.5
        )
        self.play(
            eq[3].animate.set_color(YELLOW),
            Create(line_xt),
            FadeIn(lbl_xt, shift=DOWN * 0.2),
        )
        self.wait(3.5)

        # ── e^{-2πift}: pure sine at frequency f ──────────────────────
        lbl_exp = Text("pure sine at frequency f", font_size=30, color=BLUE_B)
        lbl_exp.next_to(eq[4], UP, buff=1.0)
        line_exp = Line(
            eq[4].get_top() + UP * 0.15,
            lbl_exp.get_bottom() + DOWN * 0.15,
            color=BLUE_B, stroke_width=1.5
        )
        self.play(
            eq[4].animate.set_color(BLUE_B),
            Create(line_exp),
            FadeIn(lbl_exp, shift=DOWN * 0.2),
        )
        self.wait(3.5)

        # ── ∫ ... dt: average over time ───────────────────────────────
        lbl_int = Text("average over time", font_size=30, color=GREEN_B)
        lbl_int.next_to(eq[2], UP, buff=1.0)
        line_int = Line(
            eq[2].get_top() + UP * 0.15,
            lbl_int.get_bottom() + DOWN * 0.15,
            color=GREEN_B, stroke_width=1.5
        )
        self.play(
            eq[2].animate.set_color(GREEN_B),
            eq[5].animate.set_color(GREEN_B),
            Create(line_int),
            FadeIn(lbl_int, shift=UP * 0.2),
        )
        self.wait(3.5)

        # ── F(f): frequency fingerprint ───────────────────────────────
        lbl_Ff = Text("frequency fingerprint", font_size=30, color=RED_B)
        lbl_Ff.next_to(eq[0], DOWN, buff=1.0)
        line_Ff = Line(
            eq[0].get_bottom() + DOWN * 0.15,
            lbl_Ff.get_top() + UP * 0.15,
            color=RED_B, stroke_width=1.5
        )
        self.play(
            eq[0].animate.set_color(RED_B),
            Create(line_Ff),
            FadeIn(lbl_Ff, shift=UP * 0.2),
        )
        self.wait(4.0)

        # ── Hold full annotated equation ──────────────────────────────
        self.wait(2.0)

        self.play(
            FadeOut(VGroup(eq, lbl_xt, lbl_exp, lbl_int, lbl_Ff,
                           line_xt, line_exp, line_int, line_Ff)),
            run_time=1.5
        )
