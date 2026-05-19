"""
Visualizes the O(N²) cost of the DFT — grid fill animation.

Every cell in the N×N grid = one multiplication:
"for this frequency bin, check this time sample."

Render:
    manim -pqh animations/scene_dft_cost.py DFTCostScene

Output: media/videos/scene_dft_cost/1080p60/DFTCostScene.mp4
"""

from manim import *

YELLOW  = "#FDE724"
DIM_BG  = "#111111"
GRID_LN = "#2D2D2D"
G_CTR   = [0, 0.4, 0]   # grid center — shifted up to leave label space


# ── Helpers ───────────────────────────────────────────────────────────────────

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


# ── Scene ─────────────────────────────────────────────────────────────────────

class DFTCostScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        self._phase_intro(n=8,  cell_size=0.50)
        self._phase_fast (n=16, cell_size=0.25, ops_str="256",    fill_time=1.6)
        self._phase_fast (n=32, cell_size=0.125, ops_str="1,024", fill_time=1.2)
        self._realworld()

    # ── Shared builders ───────────────────────────────────────────────────────

    def _base(self, n, cell_size):
        total = n * cell_size
        cx, cy = G_CTR[0], G_CTR[1]
        bg = Rectangle(
            width=total, height=total,
            fill_color=DIM_BG, fill_opacity=1.0, stroke_width=0,
        ).move_to(G_CTR)
        lines = make_grid_lines(n, cell_size, G_CTR)
        return bg, lines, total, cx, cy

    def _axis_labels(self, bg):
        top  = Text("frequency bins →", font_size=18, color="#777777").next_to(bg, UP,   buff=0.22)
        left = Text("time\nsamples",     font_size=18, color="#777777").next_to(bg, LEFT, buff=0.20)
        return top, left

    def _sweep(self, fill_tracker, total, cx, cy):
        """always_redraw fill rectangle that grows downward."""
        def _draw():
            h = max(1e-4, fill_tracker.get_value() * total)
            r = Rectangle(width=total, height=h,
                          fill_color=YELLOW, fill_opacity=0.85, stroke_width=0)
            r.move_to([cx, cy + total / 2 - h / 2, 0])
            return r
        return always_redraw(_draw)

    # ── Phase 1 — N=8, slow row-by-row to show the concept ───────────────────

    def _phase_intro(self, n, cell_size):
        bg, lines, total, cx, cy = self._base(n, cell_size)
        top_lbl, left_lbl = self._axis_labels(bg)
        n_lbl   = Text(f"N = {n}",               font_size=42, color=YELLOW).next_to(bg, DOWN, buff=0.45)
        ops_lbl = Text(f"{n*n:,} operations",     font_size=30, color=WHITE ).next_to(n_lbl, DOWN, buff=0.18)

        self.play(FadeIn(bg), FadeIn(lines), FadeIn(top_lbl), FadeIn(left_lbl), run_time=0.6)
        self.play(Write(n_lbl), run_time=0.5)
        self.wait(0.4)

        fill_tracker = ValueTracker(0)
        fill = self._sweep(fill_tracker, total, cx, cy)
        self.add(fill)
        self.bring_to_front(lines)

        # First 3 rows slow (so viewer sees the row-scanning motion), rest fast
        for row_i in range(n):
            t = 0.38 if row_i < 3 else 0.11
            self.play(fill_tracker.animate.set_value((row_i + 1) / n),
                      run_time=t, rate_func=linear)

        self.play(FadeIn(ops_lbl, shift=UP * 0.08), run_time=0.35)
        self.wait(1.0)

        fill.clear_updaters()
        self.play(FadeOut(VGroup(bg, lines, top_lbl, left_lbl, n_lbl, ops_lbl, fill)),
                  run_time=0.4)

    # ── Phases 2+ — fast wipe ─────────────────────────────────────────────────

    def _phase_fast(self, n, cell_size, ops_str, fill_time):
        bg, lines, total, cx, cy = self._base(n, cell_size)
        top_lbl, left_lbl = self._axis_labels(bg)
        n_lbl   = Text(f"N = {n}",                   font_size=42, color=YELLOW).next_to(bg, DOWN, buff=0.45)
        ops_lbl = Text(f"{ops_str} operations",       font_size=30, color=WHITE ).next_to(n_lbl, DOWN, buff=0.18)

        self.play(FadeIn(bg), FadeIn(lines), FadeIn(top_lbl), FadeIn(left_lbl), FadeIn(n_lbl),
                  run_time=0.40)

        fill_tracker = ValueTracker(0)
        fill = self._sweep(fill_tracker, total, cx, cy)
        self.add(fill)
        self.bring_to_front(lines)

        self.play(fill_tracker.animate.set_value(1), run_time=fill_time, rate_func=linear)
        self.play(FadeIn(ops_lbl, shift=UP * 0.08), run_time=0.35)
        self.wait(0.8)

        fill.clear_updaters()
        self.play(FadeOut(VGroup(bg, lines, top_lbl, left_lbl, n_lbl, ops_lbl, fill)),
                  run_time=0.4)

    # ── Real-world numbers ────────────────────────────────────────────────────

    def _realworld(self):
        n_eq   = MathTex(r"N = 44{,}100",
                         font_size=54, color=YELLOW).shift(UP * 2.1)
        sq_eq  = MathTex(r"N^2 \ =\ 44{,}100^2",
                         font_size=46, color=WHITE).shift(UP * 0.7)
        result = MathTex(r"\approx\ 2{,}000{,}000{,}000",
                         font_size=58, color=YELLOW).shift(DOWN * 0.65)
        unit   = Text("operations — for every second of audio",
                      font_size=26, color="#AAAAAA").shift(DOWN * 1.6)

        self.play(Write(n_eq), run_time=0.7)
        self.wait(0.25)
        self.play(Write(sq_eq), run_time=0.7)
        self.wait(0.2)
        self.play(FadeIn(result, shift=UP * 0.12), run_time=0.6)
        self.play(FadeIn(unit), run_time=0.4)
        self.wait(3.5)
