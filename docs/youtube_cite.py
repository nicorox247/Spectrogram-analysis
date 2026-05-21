"""
Generate Chicago Notes-Bibliography citations from YouTube URLs.

Usage:
    python docs/youtube_cite.py https://youtu.be/abc123
    python docs/youtube_cite.py url1 url2 url3
    python docs/youtube_cite.py --append url1 url2   # appends to docs/bibliography.md
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import yt_dlp


def clean_url(url: str) -> str:
    """Strip playlist/radio parameters, keep only the video ID."""
    import urllib.parse as up
    p = up.urlparse(url)
    qs = up.parse_qs(p.query)
    v = qs.get("v", [None])[0]
    if v:
        return f"https://www.youtube.com/watch?v={v}"
    return url


def fetch_metadata(url: str) -> dict:
    url = clean_url(url)
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "socket_timeout": 15,
        "retries": 1,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info


def format_duration(seconds: int) -> str:
    if not seconds:
        return ""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def chicago_citation(info: dict) -> str:
    """
    Chicago Notes-Bibliography style for online video:
    Uploader. "Title." YouTube video, D:SS. Month DD, YYYY. URL.
    """
    title    = info.get("title", "Untitled")
    uploader = info.get("uploader") or info.get("channel") or "Unknown"
    url      = info.get("webpage_url") or info.get("original_url", "")
    duration = format_duration(info.get("duration"))

    upload_str = ""
    raw_date = info.get("upload_date")  # YYYYMMDD
    if raw_date:
        try:
            dt = datetime.strptime(raw_date, "%Y%m%d")
            upload_str = dt.strftime("%B %-d, %Y")
        except ValueError:
            upload_str = raw_date

    parts = [f'{uploader}. "{title}." YouTube video']
    if duration:
        parts[-1] += f", {duration}"
    parts[-1] += "."
    if upload_str:
        parts.append(f"{upload_str}.")
    parts.append(url)

    return " ".join(parts)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("urls", nargs="+", help="YouTube URLs")
    p.add_argument("--out", default="docs/bibliography.md",
                   help="File to append citations to (default: docs/bibliography.md)")
    args = p.parse_args()

    out_path = Path(args.out)
    citations = []
    for url in args.urls:
        print(f"Fetching: {url}", file=sys.stderr)
        try:
            info = fetch_metadata(url)
            cite = chicago_citation(info)
            citations.append(cite)
            print(f"  OK: {info.get('title', '')[:60]}", file=sys.stderr)
        except Exception as e:
            print(f"  ERROR {url}: {e}", file=sys.stderr)

    if citations:
        with open(out_path, "a") as f:
            f.write("\n")
            for cite in citations:
                f.write(f"{cite}\n\n")
        print(f"\nAppended {len(citations)} citation(s) to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
