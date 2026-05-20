"""
Download a YouTube video, optionally trimmed to a specific time range.

Usage:
    python download_video.py <url>
    python download_video.py <url> --start 10 --end 45
    python download_video.py <url> --start 1:30 --end 2:00 --out audio/raw/moog_clip.mp4
"""

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Download a YouTube video.")
    p.add_argument("url",               help="YouTube URL")
    p.add_argument("--start",           help="Start time (seconds or MM:SS)", default=None)
    p.add_argument("--end",             help="End time (seconds or MM:SS)", default=None)
    p.add_argument("--out",             help="Output file path (default: audio/raw/<title>.mp4)", default=None)
    return p.parse_args()


def to_seconds(t):
    """Convert MM:SS or plain seconds string to float."""
    if t is None:
        return None
    if ":" in t:
        parts = t.split(":")
        return int(parts[0]) * 60 + float(parts[1])
    return float(t)


def main():
    args = parse_args()

    out_dir = Path("../Media/Videos")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Download full video first
    tmp_path = out_dir / "_tmp_download.mp4"
    print(f"Downloading: {args.url}")
    result = subprocess.run([
        sys.executable, "-m", "yt_dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "-o", str(tmp_path),
        "--no-playlist",
        args.url,
    ])
    if result.returncode != 0:
        print("Download failed.")
        sys.exit(1)

    # Determine output path
    if args.out:
        out_path = Path(args.out)
    else:
        # Get title for filename
        title_result = subprocess.run([
            sys.executable, "-m", "yt_dlp",
            "--get-title", "--no-playlist", args.url,
        ], capture_output=True, text=True)
        title = title_result.stdout.strip().replace("/", "-").replace(":", "—") or "download"
        out_path = out_dir / f"{title}.mp4"

    # Trim if start/end provided, otherwise just rename
    start = to_seconds(args.start)
    end   = to_seconds(args.end)

    if start is not None or end is not None:
        cmd = ["ffmpeg", "-y", "-i", str(tmp_path)]
        if start is not None:
            cmd += ["-ss", str(start)]
        if end is not None:
            duration = (end - (start or 0))
            cmd += ["-t", str(duration)]
        # Re-encode audio to avoid sync loss from keyframe misalignment;
        # video stream is copied (fast) while audio is re-encoded (accurate).
        cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(out_path)]
        print(f"Trimming to {args.start or '0'}s — {args.end or 'end'}...")
        subprocess.run(cmd, check=True)
        tmp_path.unlink()
    else:
        tmp_path.rename(out_path)

    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
