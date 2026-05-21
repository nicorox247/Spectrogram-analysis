"""
FFT speedup visualisation — companion to scene_dft_cost.py.

Takes the filled N=32 DFT grid and compresses it from N² rows down to
N·log₂(N) rows, showing exactly how much work the FFT eliminates.
Ends with the real-world (N=44,100) reduction factor.

Render:
    manim -pqh animations/scene_fft_speedup.py FFTSpeedupScene

Output: media/videos/scene_fft_speedup/1080p60/FFTSpeedupScene.mp4
"""

import numpy as np
from manim import *

YELLOW  = "#FDE724"
FFT_C   = "#00FFAA"    # teal-green for FFT labels
DIM_BG  = "#111111"
GRID_LN = "#2D2D2D"
G_CTR   = [0, 0.4, 0]

N         = 32
LOG_N     = int(np.log2(N))   # 5
CELL_SIZE = 0.125              # 32 × 0.125 = 4.0 total side length


def make_grid_lines(n, cell_size, center):
    total = n * cell_size
    cx, cy = center[0], center[1]
    sw = max(0.25, 1.0 / n)
    grp = VGroup()
    for i in range(n + 1):
        y = cy + total / 2 - i * cell_size
        grp.add(Line([cx - total/2, y, 0], [cx + total/2, y, 0],
                     stroke_width=sw, color=GRID_LN))
    for j in range(n + 1):
        x = cx - total / 2 + j * cell_size
        grp.add(Line([x, cy + total/2, 0], [x, cy - total/2, 0],
                     stroke_width=sw, color=GRID_LN))
    return grp


class FFTSpeedupScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        total    = N * CELL_SIZE          # 4.0
        cx, cy   = G_CTR[0], G_CTR[1]
        bot_y    = cy - total / 2         # −1.6  — fixed bottom edge throughout
        fft_h    = LOG_N * CELL_SIZE      # 0.625 — FFT target height

        # ── 1. Full DFT grid ──────────────────────────────────────────────────
        bg    = Rectangle(width=total, height=total,
                          fill_color=DIM_BG, fill_opacity=1, stroke_width=0).move_to(G_CTR)
        fill  = Rectangle(width=total, height=total,
                          fill_color=YELLOW, fill_opacity=0.85, stroke_width=0).move_to(G_CTR)
        lines = make_grid_lines(N, CELL_SIZE, G_CTR)

        top_lbl  = Text("frequency bins →", font_size=18, color="#777777").next_to(bg, UP,   buff=0.22)
        left_lbl = Text("time\nsamples",     font_size=18, color="#777777").next_to(bg, LEFT, buff=0.20)
        n_lbl    = Text(f"N = {N}",          font_size=42, color=YELLOW  ).next_to(bg, DOWN, buff=0.45)

        dft_ops = MathTex(
            f"\\text{{DFT: }} N^2 = {N}^2 = {N*N:,}\\text{{ ops}}",
            font_size=32, color=WHITE,
        ).next_to(n_lbl, DOWN, buff=0.18)

        self.play(FadeIn(bg), FadeIn(fill), FadeIn(lines),
                  FadeIn(top_lbl), FadeIn(left_lbl), run_time=0.5)
        self.bring_to_front(lines)
        self.play(Write(n_lbl), run_time=0.4)
        self.play(FadeIn(dft_ops), run_time=0.4)
        self.wait(1.5)

        # ── 2. Switch fill to always_redraw so we can animate its height ──────
        height_tracker = ValueTracker(total)

        def make_block():
            h = height_tracker.get_value()
            r = Rectangle(width=total, height=h,
                          fill_color=YELLOW, fill_opacity=0.85, stroke_width=0)
            r.move_to([cx, bot_y + h / 2, 0])   # bottom edge pinned at bot_y
            return r

        dyn_fill = always_redraw(make_block)
        self.add(dyn_fill)
        self.remove(fill)
        self.bring_to_front(lines)

        # Prepare FFT labels (hidden for now)
        fft_ops = MathTex(
            f"\\text{{FFT: }} N\\log_2 N = {N} \\times {LOG_N} = {N*LOG_N:,}\\text{{ ops}}",
            font_size=32, color=FFT_C,
        ).next_to(n_lbl, DOWN, buff=0.18)

        speedup_val = N * N / (N * LOG_N)   # 6.4
        speedup_lbl = MathTex(
            f"\\mathbf{{{speedup_val:.1f}\\times\\text{{ faster}}}}",
            font_size=52, color=FFT_C,
        ).next_to(fft_ops, DOWN, buff=0.28)

        # ── 3. Compress: grid lines fade, block shrinks to FFT height ─────────
        self.play(FadeOut(lines), FadeOut(top_lbl), FadeOut(left_lbl), run_time=0.35)

        self.play(
            height_tracker.animate.set_value(fft_h),
            FadeOut(dft_ops, shift=DOWN * 0.05),
            run_time=2.0, rate_func=smooth,
        )

        # ── 4. Label the result ───────────────────────────────────────────────
        self.play(FadeIn(fft_ops, shift=DOWN * 0.05), run_time=0.5)
        self.play(Write(speedup_lbl), run_time=0.6)
        self.wait(2.0)

        # ── 5. Real-world numbers ─────────────────────────────────────────────
        dyn_fill.clear_updaters()
        self.play(
            FadeOut(VGroup(bg, dyn_fill, n_lbl, fft_ops, speedup_lbl)),
            run_time=0.5,
        )

        r_title = MathTex(r"N = 44{,}100",
                          font_size=52, color=YELLOW).shift(UP * 2.1)
        r_dft   = MathTex(r"\text{DFT:}\ N^2 \approx 2{,}000{,}000{,}000\text{ ops}",
                          font_size=38, color=WHITE).shift(UP * 0.7)
        r_fft   = MathTex(r"\text{FFT:}\ N\log_2 N \approx 680{,}000\text{ ops}",
                          font_size=38, color=FFT_C).shift(DOWN * 0.4)
        r_sp    = MathTex(r"\approx 2{,}850\times\ \text{faster}",
                          font_size=56, color=FFT_C).shift(DOWN * 1.8)

        self.play(Write(r_title), run_time=0.7)
        self.play(FadeIn(r_dft),  run_time=0.5)
        self.play(FadeIn(r_fft),  run_time=0.5)
        self.play(Write(r_sp),    run_time=0.7)
        self.wait(3.5)
