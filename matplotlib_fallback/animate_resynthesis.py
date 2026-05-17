"""
Additive resynthesis animation.

Visualizes how a sound is built from its top K sinusoidal components.
A scrolling window shows the individual sine waves oscillating in real time
as the audio plays, with their running sum shown below.

Opening:  sum only (k components, no individual waves shown)
Versions: individual waves revealed progressively
Closing:  sum only (k_close components — more than k for better fidelity)

Structure:
  [opening: sum, k] → [transition] → [v1] → ... → [vN] → [transition] → [closing: sum, k_close]

Usage:
    python matplotlib_fallback/animate_resynthesis.py <track> <start> <end> [--k K] [--n N] [--window W] [--k_close KC]

Example:
    python matplotlib_fallback/animate_resynthesis.py violin_c_note 0 2 --k 20 --n 3 --window 0.02 --k_close 50
"""

from pathlib import Path
import argparse
import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import librosa
import soundfile as sf

SR         = 44100
FPS        = 30
TRANS_SECS = 2.0
AUDIO_DIR  = Path("audio/normalized")
OUTPUT_DIR = Path("output/resynthesis")


def parse_args():
    p = argparse.ArgumentParser(description="Additive resynthesis animation.")
    p.add_argument("track",      help="Track name (audio/normalized/<track>.wav, no extension)")
    p.add_argument("start",      type=float, help="Start time in seconds")
    p.add_argument("end",        type=float, help="End time in seconds")
    p.add_argument("--k",        type=int,   default=30,  help="Number of components for versioned segments")
    p.add_argument("--n",        type=int,   default=3,   help="Number of versions")
    p.add_argument("--window",   type=float, default=0.02, help="Scrolling window width in seconds")
    p.add_argument("--k_close",  type=int,   default=50,  help="Number of components for closing (sum only, higher fidelity)")
    return p.parse_args()


# ---------------------------------------------------------------------------
# Audio processing
# ---------------------------------------------------------------------------

def load_clip(track, t_start, duration):
    path = AUDIO_DIR / f"{track}.wav"
    y, _ = librosa.load(str(path), sr=SR, offset=t_start, duration=duration, mono=True)
    return y


def extract_components(y, k):
    """Top K sinusoidal components via FFT, sorted by descending amplitude. Excludes sub-20 Hz."""
    Y      = np.fft.rfft(y)
    freqs  = np.fft.rfftfreq(len(y), d=1.0 / SR)
    amps   = np.abs(Y) * 2.0 / len(y)
    phases = np.angle(Y)
    amps[freqs < 20] = 0.0
    top = np.argsort(amps)[::-1][:k]
    return [(float(freqs[b]), float(amps[b]), float(phases[b])) for b in top]


def make_waves(components, t_arr):
    """Return (K, T) array — one sine wave per row."""
    out = np.zeros((len(components), len(t_arr)), dtype=np.float32)
    for i, (f, a, phi) in enumerate(components):
        out[i] = (a * np.cos(2.0 * np.pi * f * t_arr + phi)).astype(np.float32)
    return out


def build_audio(waves_audio, waves_audio_close, versions_m, k, k_close):
    """Full audio track: each segment uses its own reconstruction; transitions are silence."""
    silence = np.zeros(int(TRANS_SECS * SR), dtype=np.float32)

    closing_audio = waves_audio_close[:k_close].sum(axis=0)

    # Timeline: v1, silence, v2, silence, ..., vN, silence, closing
    parts = []
    for m in versions_m:
        parts += [waves_audio[:m].sum(axis=0), silence]
    parts.append(closing_audio)

    full = np.concatenate(parts)
    peak = np.abs(full).max()
    if peak > 0:
        full = full / peak * 0.8
    return full.astype(np.float32)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def setup_figure():
    fig      = plt.figure(figsize=(14, 8), facecolor='black', dpi=150)
    ax_waves = fig.add_axes([0.09, 0.20, 0.87, 0.72])
    ax_sum   = fig.add_axes([0.09, 0.04, 0.87, 0.12])
    return fig, ax_waves, ax_sum


def style_ax(ax):
    ax.set_facecolor('black')
    ax.tick_params(colors='white', labelsize=7)
    for sp in ax.spines.values():
        sp.set_edgecolor('#444444')


def get_window(reveal_frac, duration, window_secs):
    """Return (t_start, t_end) for the scrolling window at this reveal fraction."""
    t_current = reveal_frac * duration
    t_start   = max(0.0, min(t_current - window_secs, duration - window_secs))
    return t_start, t_start + window_secs


def draw_frame(fig, ax_waves, ax_sum,
               waves_by_amp, components, wave_colors,
               display_indices, t_plot, n_plot,
               window_start, window_end,
               spacing, amp_scale, title,
               show_components=True):
    """
    Draw one frame.
    display_indices: amplitude-rank indices to show, sorted by frequency (low→high).
    show_components=False: sum fills ax_waves (big panel), ax_sum hidden.
    show_components=True:  individual waves in ax_waves, sum in ax_sum.
    """
    ax_waves.clear()
    ax_sum.clear()
    style_ax(ax_waves)
    style_ax(ax_sum)

    duration  = float(t_plot[-1])
    i_start   = int(window_start / duration * (n_plot - 1))
    i_end     = int(window_end   / duration * (n_plot - 1)) + 1
    i_start   = max(0, min(i_start, n_plot - 1))
    i_end     = max(i_start + 1, min(i_end, n_plot))
    t_win     = t_plot[i_start:i_end]

    m = len(display_indices)

    if not show_components:
        # Sum-only mode (opening and closing): draw sum in the big panel, hide small panel
        if m > 0:
            sum_wave = waves_by_amp[np.array(display_indices), i_start:i_end].sum(axis=0)
            ax_waves.plot(t_win, sum_wave, color='#00FFFF', linewidth=1.5, alpha=0.95)
            ax_waves.axhline(0, color='white', alpha=0.10, linewidth=0.5)
            full_sum = waves_by_amp[np.array(display_indices), :].sum(axis=0)
            y_lim    = max(float(np.abs(full_sum).max()) * 1.15, 1e-6)
            ax_waves.set_ylim(-y_lim, y_lim)
        ax_waves.set_xlim(window_start, window_end)
        ax_waves.set_xticks([])
        ax_waves.set_yticks([])
        ax_waves.set_title(title, color='white', fontsize=10, pad=3)
        ax_sum.set_visible(False)
        return

    # Normal mode: individual waves in ax_waves, sum in ax_sum
    ax_sum.set_visible(True)

    for i_display, amp_rank in enumerate(display_indices):
        y_offset = i_display * spacing
        wave     = waves_by_amp[amp_rank, i_start:i_end] * amp_scale
        ax_waves.plot(t_win, y_offset + wave,
                      color=wave_colors[amp_rank], linewidth=0.7, alpha=0.9)

    if m > 0:
        sum_wave = waves_by_amp[np.array(display_indices), i_start:i_end].sum(axis=0)
        ax_sum.plot(t_win, sum_wave, color='#00FFFF', linewidth=1.3, alpha=0.95)
    ax_sum.axhline(0, color='white', alpha=0.10, linewidth=0.5)

    ax_waves.set_xlim(window_start, window_end)
    ax_waves.set_ylim(-spacing * 0.55, max(1, m - 0.45) * spacing)
    ax_waves.set_xticks([])
    ax_waves.set_title(title, color='white', fontsize=10, pad=3)

    if 0 < m <= 20:
        y_ticks  = [i * spacing for i in range(m)]
        y_labels = [f'{components[amp_rank][0]:.0f} Hz' for amp_rank in display_indices]
        ax_waves.set_yticks(y_ticks)
        ax_waves.set_yticklabels(y_labels, fontsize=5.5, color='white')
        ax_waves.set_ylabel('Components', color='white', fontsize=8)
    else:
        ax_waves.set_yticks([])
        ax_waves.tick_params(left=False)

    if m > 0:
        full_sum = waves_by_amp[np.array(display_indices), :].sum(axis=0)
        y_lim    = max(float(np.abs(full_sum).max()) * 1.15, 1e-6)
    else:
        y_lim = 1.0
    ax_sum.set_xlim(window_start, window_end)
    ax_sum.set_ylim(-y_lim, y_lim)
    ax_sum.set_xticks([])
    ax_sum.set_yticks([])
    ax_sum.set_ylabel('Sum', color='white', fontsize=8)


def render_to_rgb(fig):
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    buf  = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8).reshape(h, w, 4)
    return buf[:, :, :3].copy()


def blend(a, b, alpha):
    return ((1.0 - alpha) * a + alpha * b).astype(np.uint8)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def animate(track, t_start, t_end, k, n, window_secs, k_close):
    OUTPUT_DIR.mkdir(exist_ok=True)
    duration = t_end - t_start

    y = load_clip(track, t_start, duration)

    # Extract enough components to cover both versioned segments and the closing
    k_max      = max(k, k_close)
    components = extract_components(y, k_max)

    versions_m = [max(1, round(k ** (i / n))) for i in range(1, n + 1)]
    versions_m[0] = 1
    versions_m[-1] = k
    print(f"Components per version: {versions_m} (out of k={k}), closing: {k_close}")

    # Audio-rate waves
    t_audio          = np.arange(int(duration * SR), dtype=np.float32) / SR
    waves_audio      = make_waves(components, t_audio)   # shape (k_max, T)
    full_audio       = build_audio(waves_audio, waves_audio, versions_m, k, k_close)

    audio_tmp = OUTPUT_DIR / f"{track}_resyn_tmp_audio.wav"
    sf.write(str(audio_tmp), full_audio, SR)

    # High-res plot-rate waves
    n_plot       = max(8192, int(duration * 6000))
    t_plot       = np.linspace(0, duration, n_plot, dtype=np.float32)
    waves_by_amp = make_waves(components, t_plot)   # shape (k_max, n_plot)

    # Colors based on the versioned-segment components only (first k)
    all_freqs   = [components[i][0] for i in range(k)]
    f_lo, f_hi  = min(all_freqs), max(all_freqs)
    cmap        = plt.get_cmap('plasma')
    norm_f      = lambda f: 0.5 + 0.5 * (f - f_lo) / max(1.0, f_hi - f_lo)
    wave_colors = [cmap(norm_f(c[0])) for c in components]

    max_amp   = max(components[i][1] for i in range(k)) if k > 0 else 1.0
    spacing   = 1.0
    amp_scale = 0.38 * spacing / max_amp

    def display_order(m):
        return sorted(range(m), key=lambda r: components[r][0])

    fig, ax_waves, ax_sum = setup_figure()
    fig.canvas.draw()
    W, H = fig.canvas.get_width_height()

    seg_f   = int(duration * FPS)
    trans_f = int(TRANS_SECS * FPS)

    timeline = [('version', versions_m[0], seg_f)]
    for i, m in enumerate(versions_m[1:], start=1):
        timeline.append(('transition', i, trans_f))
        timeline.append(('version', m, seg_f))
    timeline.append(('transition', 'closing', trans_f))
    timeline.append(('closing', k_close, seg_f))

    total_frames = sum(t[2] for t in timeline)

    silent_path = OUTPUT_DIR / f"{track}_resyn_silent.mp4"
    out_path    = OUTPUT_DIR / f"{track}_{int(t_start)}s-{int(t_end)}s_resyn_k{k}_n{n}.mp4"

    cmd = [
        'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
        '-s', f'{W}x{H}', '-pix_fmt', 'rgb24', '-r', str(FPS),
        '-i', '-', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '4000k',
        str(silent_path),
    ]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    frame_idx = 0
    for seg_type, seg_data, n_frames_seg in timeline:
        for f in range(n_frames_seg):
            progress = f / max(1, n_frames_seg - 1)

            if seg_type == 'opening':
                w_start, w_end = get_window(progress, duration, window_secs)
                draw_frame(fig, ax_waves, ax_sum, waves_by_amp, components,
                           wave_colors, display_order(k), t_plot, n_plot,
                           w_start, w_end, spacing, amp_scale,
                           f'Reconstruction — {k} components',
                           show_components=False)
                frame = render_to_rgb(fig)

            elif seg_type == 'closing':
                w_start, w_end = get_window(progress, duration, window_secs)
                draw_frame(fig, ax_waves, ax_sum, waves_by_amp, components,
                           wave_colors, display_order(k_close), t_plot, n_plot,
                           w_start, w_end, spacing, amp_scale,
                           f'Reconstruction — {k_close} components',
                           show_components=False)
                frame = render_to_rgb(fig)

            elif seg_type == 'version':
                m = seg_data
                w_start, w_end = get_window(progress, duration, window_secs)
                draw_frame(fig, ax_waves, ax_sum, waves_by_amp, components,
                           wave_colors, display_order(m), t_plot, n_plot,
                           w_start, w_end, spacing, amp_scale,
                           f'Top {m} of {k} components',
                           show_components=True)
                frame = render_to_rgb(fig)

            elif seg_type == 'transition':
                w_start, w_end = get_window(1.0, duration, window_secs)

                if seg_data == 0:
                    m_from, show_from = k,              False
                    m_to,   show_to   = versions_m[0],  True
                    title_from = f'Reconstruction — {k} components'
                    title_to   = f'Top {versions_m[0]} of {k} components'
                elif seg_data == 'closing':
                    m_from, show_from = versions_m[-1], True
                    m_to,   show_to   = k_close,        False
                    title_from = f'Top {versions_m[-1]} of {k} components'
                    title_to   = f'Reconstruction — {k_close} components'
                else:
                    m_from, show_from = versions_m[seg_data - 1], True
                    m_to,   show_to   = versions_m[seg_data],     True
                    title_from = f'Top {versions_m[seg_data - 1]} of {k} components'
                    title_to   = f'Top {versions_m[seg_data]} of {k} components'

                draw_frame(fig, ax_waves, ax_sum, waves_by_amp, components,
                           wave_colors, display_order(m_from), t_plot, n_plot,
                           w_start, w_end, spacing, amp_scale, title_from,
                           show_components=show_from)
                frame_from = render_to_rgb(fig)

                draw_frame(fig, ax_waves, ax_sum, waves_by_amp, components,
                           wave_colors, display_order(m_to), t_plot, n_plot,
                           w_start, w_end, spacing, amp_scale, title_to,
                           show_components=show_to)
                frame_to = render_to_rgb(fig)

                frame = blend(frame_from, frame_to, progress)

            pipe.stdin.write(frame.tobytes())
            frame_idx += 1
            if frame_idx % FPS == 0:
                print(f"  {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.0f}%)",
                      end='\r')

    pipe.stdin.close()
    pipe.wait()
    print(f"\n  Rendered {total_frames} frames")
    plt.close(fig)

    subprocess.run([
        'ffmpeg', '-y',
        '-i', str(silent_path),
        '-i', str(audio_tmp),
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-shortest', str(out_path),
    ], check=True, capture_output=True)

    silent_path.unlink()
    audio_tmp.unlink()
    print(f"Saved: {out_path}")


if __name__ == '__main__':
    args = parse_args()
    animate(args.track, args.start, args.end, args.k, args.n, args.window, args.k_close)
