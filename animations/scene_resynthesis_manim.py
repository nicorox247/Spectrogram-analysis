"""
Manim resynthesis animation — vector-rendered version of animate_resynthesis.py.

Same structure and audio as the matplotlib version:
  [v1] → [fade to black / silence] → [v2] → ... → [vN] → [fade to black] → [closing: sum only]

Usage:
    python animations/scene_resynthesis_manim.py <track> <start> <end>
    python animations/scene_resynthesis_manim.py violin_A4 0 1.0 --k 20 --n 3 --window 0.02 --k_close 150
    python animations/scene_resynthesis_manim.py violin_A4 0 1.0 --quality l   # fast preview

Output: output/resynthesis/<track>_..._manim.mp4
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import librosa
import soundfile as sf
import matplotlib
matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from manim import *

# ── Constants ─────────────────────────────────────────────────────────────────
SR         = 44100
TRANS_SECS = 2.0
AUDIO_DIR  = Path("audio/normalized")
OUTPUT_DIR = Path("output/resynthesis")

# Scene layout (Manim coords: x ∈ [-7.1, 7.1], y ∈ [-4, 4])
WAVES_TOP    =  3.2
WAVES_BOTTOM = -0.8
SUM_TOP      = -1.2
SUM_BOTTOM   = -3.2
X_LO, X_HI  = -6.5, 6.5
N_DISP       = 300          # points per wave path (keep low for Manim performance)
SUM_COLOR    = "#00FFFF"
DIV_COLOR    = "#333333"

# ── Env vars (set by __main__ wrapper) ───────────────────────────────────────
_TRACK     = os.environ.get("RESYN_TRACK",     "")
_START     = float(os.environ.get("RESYN_START",    "0"))
_END       = float(os.environ.get("RESYN_END",      "1"))
_K         = int(os.environ.get("RESYN_K",         "20"))
_N         = int(os.environ.get("RESYN_N",          "3"))
_WINDOW    = float(os.environ.get("RESYN_WINDOW",  "0.02"))
_K_CLOSE   = int(os.environ.get("RESYN_K_CLOSE",   "50"))
_AUDIO_TMP = os.environ.get("RESYN_AUDIO_TMP", "")


# ── Audio helpers (shared with matplotlib version) ────────────────────────────

def load_clip(track, t_start, duration):
    path = AUDIO_DIR / f"{track}.wav"
    y, _ = librosa.load(str(path), sr=SR, offset=t_start, duration=duration, mono=True)
    return y


def extract_components(y, k):
    Y      = np.fft.rfft(y)
    freqs  = np.fft.rfftfreq(len(y), d=1.0 / SR)
    amps   = np.abs(Y) * 2.0 / len(y)
    phases = np.angle(Y)
    amps[freqs < 20] = 0.0
    top = np.argsort(amps)[::-1][:k]
    return [(float(freqs[b]), float(amps[b]), float(phases[b])) for b in top]


def make_waves(components, t_arr):
    out = np.zeros((len(components), len(t_arr)), dtype=np.float32)
    for i, (f, a, phi) in enumerate(components):
        out[i] = (a * np.cos(2.0 * np.pi * f * t_arr + phi)).astype(np.float32)
    return out


def build_audio(waves_audio, versions_m, k, k_close):
    silence       = np.zeros(int(TRANS_SECS * SR), dtype=np.float32)
    closing_audio = waves_audio[:k_close].sum(axis=0)
    parts = []
    for m in versions_m:
        parts += [waves_audio[:m].sum(axis=0), silence]
    parts.append(closing_audio)
    full = np.concatenate(parts)
    peak = np.abs(full).max()
    if peak > 0:
        full = full / peak * 0.8
    return full.astype(np.float32)


def get_window(reveal_frac, duration, window_secs):
    t_current = reveal_frac * duration
    t_start   = max(0.0, min(t_current - window_secs, duration - window_secs))
    return t_start, t_start + window_secs


def display_order(m, components):
    return sorted(range(m), key=lambda r: components[r][0])


def compute_colors(components, k):
    freqs  = [components[i][0] for i in range(k)]
    f_lo, f_hi = min(freqs), max(freqs)
    cmap   = plt.get_cmap("plasma")
    norm_f = lambda f: 0.5 + 0.5 * (f - f_lo) / max(1.0, f_hi - f_lo)
    return [mcolors.to_hex(cmap(norm_f(c[0]))) for c in components]


# ── Manim scene ───────────────────────────────────────────────────────────────

class ResynthesisSceneManim(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        duration  = _END - _START
        y         = load_clip(_TRACK, _START, duration)
        k_max     = max(_K, _K_CLOSE)
        components = extract_components(y, k_max)

        versions_m = [max(1, round(_K ** (i / _N))) for i in range(1, _N + 1)]
        versions_m[0]  = 1
        versions_m[-1] = _K

        n_plot       = max(8192, int(duration * 6000))
        t_plot       = np.linspace(0, duration, n_plot, dtype=np.float32)
        waves_by_amp = make_waves(components, t_plot)   # (k_max, n_plot)
        wave_colors  = compute_colors(components, _K)

        waves_height = WAVES_TOP - WAVES_BOTTOM
        sum_height   = SUM_TOP - SUM_BOTTOM
        max_amp      = max(components[i][1] for i in range(_K)) if _K > 0 else 1.0

        # ── Layout helpers ────────────────────────────────────────────────────
        def amp_scale(m):
            return 0.38 * (waves_height / max(m, 1)) / max_amp

        def y_center(i_disp, m):
            spacing = waves_height / max(m, 1)
            return WAVES_BOTTOM + (i_disp + 0.5) * spacing

        def window_slice(rev_frac):
            w_s, w_e = get_window(rev_frac, duration, _WINDOW)
            i_s = max(0, int(w_s / duration * (n_plot - 1)))
            i_e = min(n_plot, int(w_e / duration * (n_plot - 1)) + 1)
            return i_s, i_e

        # ── Display factories (always_redraw) ─────────────────────────────────
        def make_components_factory(m, tracker):
            disp = display_order(m, components)
            a_sc = amp_scale(m)
            disp_arr = np.array(disp)
            full_sum_all = waves_by_amp[disp_arr, :].sum(axis=0)
            y_lim = max(float(np.abs(full_sum_all).max()) * 1.15, 1e-6)
            s_center = (SUM_TOP + SUM_BOTTOM) / 2
            s_scale  = 0.7 * sum_height / 2 / y_lim

            def _draw():
                rv = tracker.get_value() / max(duration, 1e-9)
                i_s, i_e = window_slice(rv)
                seg = waves_by_amp[:, i_s:i_e]
                L   = i_e - i_s
                xs  = np.linspace(X_LO, X_HI, min(N_DISP, L))
                idx = np.linspace(0, L - 1, min(N_DISP, L), dtype=int)

                grp = VGroup()
                for i_d, ar in enumerate(disp):
                    yc  = y_center(i_d, m)
                    ys  = yc + seg[ar, idx] * a_sc
                    pts = np.column_stack([xs, ys, np.zeros(len(xs))])
                    ln  = VMobject(stroke_width=0.8, stroke_color=wave_colors[ar])
                    ln.set_points_as_corners(pts)
                    grp.add(ln)

                sv    = seg[disp_arr, :][:, idx].sum(axis=0)
                ys_s  = s_center + sv * s_scale
                pts_s = np.column_stack([xs, ys_s, np.zeros(len(xs))])
                sl    = VMobject(stroke_width=1.5, stroke_color=SUM_COLOR)
                sl.set_points_as_corners(pts_s)
                grp.add(sl)
                return grp

            return always_redraw(_draw)

        def make_closing_factory(tracker):
            disp = display_order(_K_CLOSE, components)
            disp_arr = np.array(disp)
            full_sum_all = waves_by_amp[disp_arr, :].sum(axis=0)
            y_lim   = max(float(np.abs(full_sum_all).max()) * 1.15, 1e-6)
            s_scale = 2.5 / y_lim

            def _draw():
                rv = tracker.get_value() / max(duration, 1e-9)
                i_s, i_e = window_slice(rv)
                seg = waves_by_amp[:, i_s:i_e]
                L   = i_e - i_s
                xs  = np.linspace(X_LO, X_HI, min(N_DISP, L))
                idx = np.linspace(0, L - 1, min(N_DISP, L), dtype=int)
                sv  = seg[disp_arr, :][:, idx].sum(axis=0)
                pts = np.column_stack([xs, sv * s_scale, np.zeros(len(xs))])
                ln  = VMobject(stroke_width=1.8, stroke_color=SUM_COLOR)
                ln.set_points_as_corners(pts)
                return ln

            return always_redraw(_draw)

        # ── Static chrome ─────────────────────────────────────────────────────
        div_line = Line([X_LO, SUM_TOP + 0.05, 0], [X_HI, SUM_TOP + 0.05, 0],
                        color=DIV_COLOR, stroke_width=0.8)
        zero_sum = Line([X_LO, (SUM_TOP + SUM_BOTTOM) / 2, 0],
                        [X_HI, (SUM_TOP + SUM_BOTTOM) / 2, 0],
                        color="#222222", stroke_width=0.5)

        def make_title(text):
            return Text(text, font_size=26, color=WHITE).move_to([0, WAVES_TOP + 0.45, 0])

        # Black overlay for transitions (always on top)
        overlay = Rectangle(
            width=config.frame_width + 0.2,
            height=config.frame_height + 0.2,
            fill_color=BLACK, fill_opacity=0, stroke_width=0,
        )

        # ── Audio ─────────────────────────────────────────────────────────────
        if _AUDIO_TMP:
            self.add_sound(_AUDIO_TMP, time_offset=0)

        # ── Animate ───────────────────────────────────────────────────────────
        self.add(div_line, zero_sum)
        self.bring_to_front(overlay)

        cur_display = None
        cur_title   = None

        for i, m in enumerate(versions_m):
            tracker = ValueTracker(0)
            display = make_components_factory(m, tracker)
            title   = make_title(f"Top {m} of {_K} components")

            if i == 0:
                self.add(display, title)
                self.bring_to_front(overlay)
            else:
                # Fade to black → swap → fade in
                self.play(overlay.animate.set_fill(BLACK, opacity=1),
                          run_time=TRANS_SECS / 2)
                self.remove(cur_display, cur_title)
                self.add(display, title)
                self.bring_to_front(overlay)
                self.play(overlay.animate.set_fill(BLACK, opacity=0),
                          run_time=TRANS_SECS / 2)

            self.play(tracker.animate.set_value(duration),
                      run_time=duration, rate_func=linear)

            cur_display = display
            cur_title   = title

        # Closing
        tracker_close = ValueTracker(0)
        closing = make_closing_factory(tracker_close)
        title_close = make_title(f"Reconstruction — {_K_CLOSE} components")

        self.play(overlay.animate.set_fill(BLACK, opacity=1),
                  run_time=TRANS_SECS / 2)
        self.remove(cur_display, cur_title, div_line, zero_sum)
        self.add(closing, title_close)
        self.bring_to_front(overlay)
        self.play(overlay.animate.set_fill(BLACK, opacity=0),
                  run_time=TRANS_SECS / 2)
        self.play(tracker_close.animate.set_value(duration),
                  run_time=duration, rate_func=linear)
        self.wait(0.3)


# ── CLI wrapper ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("track")
    p.add_argument("start",     type=float)
    p.add_argument("end",       type=float)
    p.add_argument("--k",       type=int,   default=20)
    p.add_argument("--n",       type=int,   default=3)
    p.add_argument("--window",  type=float, default=0.02)
    p.add_argument("--k_close", type=int,   default=50)
    p.add_argument("--quality", default="h", choices=["l", "m", "h", "k"])
    args = p.parse_args()

    # Pre-build synthesized audio so we can pass it to the scene
    duration   = args.end - args.start
    audio_path = AUDIO_DIR / f"{args.track}.wav"
    y, _       = librosa.load(str(audio_path), sr=SR, offset=args.start,
                               duration=duration, mono=True)
    k_max      = max(args.k, args.k_close)
    components = extract_components(y, k_max)
    versions_m = [max(1, round(args.k ** (i / args.n))) for i in range(1, args.n + 1)]
    versions_m[0]  = 1
    versions_m[-1] = args.k
    t_audio     = np.arange(int(duration * SR), dtype=np.float32) / SR
    waves_audio = make_waves(components, t_audio)
    full_audio  = build_audio(waves_audio, versions_m, args.k, args.k_close)

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, full_audio, SR)
    tmp.close()

    stem = (f"{args.track}_{int(args.start)}s-{int(args.end)}s"
            f"_resyn_k{args.k}_n{args.n}_manim")

    env = os.environ.copy()
    env.update({
        "RESYN_TRACK":     args.track,
        "RESYN_START":     str(args.start),
        "RESYN_END":       str(args.end),
        "RESYN_K":         str(args.k),
        "RESYN_N":         str(args.n),
        "RESYN_WINDOW":    str(args.window),
        "RESYN_K_CLOSE":   str(args.k_close),
        "RESYN_AUDIO_TMP": tmp.name,
    })

    result = subprocess.run([
        sys.executable, "-m", "manim",
        f"-pq{args.quality}",
        "--media_dir", "media",
        "--output_file", stem,
        __file__, "ResynthesisSceneManim",
    ], env=env)

    Path(tmp.name).unlink(missing_ok=True)

    if result.returncode == 0:
        quality_dir = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
        src = (Path("media/videos/scene_resynthesis_manim")
               / quality_dir[args.quality] / f"{stem}.mp4")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        if src.exists():
            dest = OUTPUT_DIR / f"{stem}.mp4"
            shutil.move(str(src), str(dest))
            print(f"\nSaved: {dest}")
        else:
            print(f"\nWARNING: expected output not at {src} — check media/")

    sys.exit(result.returncode)
