"""
Fourier series construction — a complex waveform revealed as the sum of three sines.

f(x) = sin(x)  +  ½ sin(2x)  +  ⅓ sin(3x)
        [blue]      [orange]       [pink]   →  [yellow composite]

Each sine is introduced with its own labeled equation line.  The two lines then
animate toward each other and merge into the composite equation before the
individual graph curves vanish and the composite curve is drawn.

Render:
    manim -pqh animations/scene_fourier_buildup.py FourierBuildupScene

Output: media/videos/scene_fourier_buildup/1080p60/FourierBuildupScene.mp4
"""

import numpy as np
from manim import *

C1   = "#5B9BD5"   # blue   — sin(x)
C2   = "#ED7D31"   # orange — ½ sin(2x)
C12  = "#70AD47"   # green  — sin(x) + ½ sin(2x)
C3   = "#FF6B9D"   # pink   — ⅓ sin(3x)
C123 = "#FDE724"   # cividis yellow — final composite

AX_C = "#444444"
FS   = 38          # equation font size


def f1(x):   return np.sin(x)
def f2(x):   return 0.5 * np.sin(2 * x)
def f12(x):  return np.sin(x) + 0.5 * np.sin(2 * x)
def f3(x):   return (1 / 3) * np.sin(3 * x)
def f123(x): return np.sin(x) + 0.5 * np.sin(2 * x) + (1 / 3) * np.sin(3 * x)


# ── y-positions for the two equation lines (below the axes) ───────────────────
EQ1_Y  = -2.05    # first / upper equation line
EQ2_Y  = -2.95    # second / lower equation line
EMID_Y = (EQ1_Y + EQ2_Y) / 2   # merge target


class FourierBuildupScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        ax = Axes(
            x_range=[0, 2 * np.pi, np.pi / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=11.0,
            y_length=4.2,
            axis_config={
                "color": AX_C,
                "stroke_width": 1.5,
                "tip_width":    0.15,
                "tip_height":   0.15,
            },
        ).shift(UP * 0.75)

        def at(mob, y):
            """Centre mob at x=0, y=y."""
            mob.move_to([0, y, 0])
            return mob

        def merge_equations(scene, eq_top, eq_bot, eq_result):
            """Animate two stacked equations converging to a composite line."""
            scene.play(
                eq_top.animate.move_to([0, EMID_Y, 0]).set_opacity(0.35),
                eq_bot.animate.move_to([0, EMID_Y, 0]).set_opacity(0.35),
                run_time=0.65, rate_func=smooth,
            )
            scene.play(
                FadeOut(eq_top),
                FadeOut(eq_bot),
                FadeIn(eq_result),
                run_time=0.5,
            )

        # ── 1. Mystery waveform ───────────────────────────────────────────────
        mystery = ax.plot(f123, color=C123, stroke_width=2.2)
        q_lbl   = at(Text("What is this waveform?", font_size=30, color="#AAAAAA"), EMID_Y)

        self.play(Create(ax), run_time=0.8)
        self.play(Create(mystery), run_time=1.8)
        self.play(FadeIn(q_lbl, shift=UP * 0.1), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(mystery), FadeOut(q_lbl), run_time=0.5)
        self.wait(0.3)

        # ── 2. f₁ = sin(x) ───────────────────────────────────────────────────
        c1  = ax.plot(f1, color=C1, stroke_width=2.2)
        eq1 = at(MathTex(r"f_1(x) = \sin(x)", font_size=FS, color=C1), EQ1_Y)

        self.play(Create(c1), run_time=1.4)
        self.play(Write(eq1), run_time=0.7)
        self.wait(1.4)

        # ── 3. Introduce f₂ = ½ sin(2x) ──────────────────────────────────────
        c2  = ax.plot(f2, color=C2, stroke_width=2.2)
        eq2 = at(MathTex(r"f_2(x) = \tfrac{1}{2}\sin(2x)", font_size=FS, color=C2), EQ2_Y)

        self.play(Create(c2), run_time=1.2)
        self.play(FadeIn(eq2, shift=UP * 0.1), run_time=0.6)
        self.wait(1.2)

        # ── 4. Merge equations, then curves ───────────────────────────────────
        eq12 = at(MathTex(r"f(x) = ", r"\sin(x) + \tfrac{1}{2}\sin(2x)", font_size=FS), EMID_Y)
        eq12[1].set_color(C12)

        merge_equations(self, eq1, eq2, eq12)   # equations converge → composite eq appears
        self.wait(0.3)

        # Individual curves fade out first …
        self.play(
            c1.animate.set_stroke(opacity=0),
            c2.animate.set_stroke(opacity=0),
            run_time=0.7,
        )
        self.remove(c1, c2)

        # … then composite curve draws in
        c12 = ax.plot(f12, color=C12, stroke_width=2.8)
        self.play(Create(c12), run_time=1.2)
        self.wait(1.3)

        # ── 5. Introduce f₃ = ⅓ sin(3x) ─────────────────────────────────────
        # Lift composite equation to the upper slot to make room
        self.play(eq12.animate.move_to([0, EQ1_Y, 0]), run_time=0.35)

        c3  = ax.plot(f3, color=C3, stroke_width=2.2)
        eq3 = at(MathTex(r"f_3(x) = \tfrac{1}{3}\sin(3x)", font_size=FS, color=C3), EQ2_Y)

        self.play(Create(c3), run_time=1.2)
        self.play(FadeIn(eq3, shift=UP * 0.1), run_time=0.6)
        self.wait(1.2)

        # ── 6. Final merge → cividis yellow ───────────────────────────────────
        eq_final = at(MathTex(
            r"f(x) = ", r"\sin(x) + \tfrac{1}{2}\sin(2x) + \tfrac{1}{3}\sin(3x)",
            font_size=FS,
        ), EMID_Y)
        eq_final[1].set_color(C123)

        merge_equations(self, eq12, eq3, eq_final)
        self.wait(0.3)

        self.play(
            c12.animate.set_stroke(opacity=0),
            c3.animate.set_stroke(opacity=0),
            run_time=0.7,
        )
        self.remove(c12, c3)

        c123 = ax.plot(f123, color=C123, stroke_width=2.8)
        self.play(Create(c123), run_time=1.4)
        self.wait(3.5)
