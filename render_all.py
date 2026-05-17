"""
Render all spectrogram and resynthesis videos defined in configs/renders.json.

Usage:
    python render_all.py               # render everything
    python render_all.py --type spec   # spectrogram only
    python render_all.py --type resyn  # resynthesis only
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"ERROR: command failed (exit {result.returncode})")


def render_spectrogram(job):
    run([
        sys.executable,
        "matplotlib_fallback/animate_spectrogram.py",
        job["track"],
        str(job["start"]),
        str(job["end"]),
    ])


def render_resynthesis(job):
    run([
        sys.executable,
        "matplotlib_fallback/animate_resynthesis.py",
        job["track"],
        str(job["start"]),
        str(job["end"]),
        "--k",       str(job.get("k",       30)),
        "--n",       str(job.get("n",        3)),
        "--window",  str(job.get("window", 0.02)),
        "--k_close", str(job.get("k_close",  50)),
    ])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--type", choices=["spec", "resyn", "all"], default="all",
                   help="Which render type to run (default: all)")
    args = p.parse_args()

    config_path = Path("configs/renders.json")
    with config_path.open() as f:
        config = json.load(f)

    spec_jobs  = config.get("spectrogram", [])
    resyn_jobs = config.get("resynthesis", [])

    def ready(job):
        if job.get("_status", "") == "file not yet acquired":
            print(f"  SKIPPED (file not acquired): {job['track']}")
            return False
        return True

    if args.type in ("spec", "all"):
        print(f"\n=== Spectrogram renders ({len(spec_jobs)} jobs) ===")
        for job in spec_jobs:
            if ready(job):
                render_spectrogram(job)

    if args.type in ("resyn", "all"):
        print(f"\n=== Resynthesis renders ({len(resyn_jobs)} jobs) ===")
        for job in resyn_jobs:
            if ready(job):
                render_resynthesis(job)

    print("\nAll done.")


if __name__ == "__main__":
    main()
