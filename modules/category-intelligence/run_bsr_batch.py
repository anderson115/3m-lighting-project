#!/usr/bin/env python3
"""
BSR Batch Runner
Reads ASINs from file and runs BSR tracker on all of them.
"""
import subprocess
import sys
from pathlib import Path

def main():
    # Read ASINs from file
    asins_file = Path(__file__).parent / "asins_top100.txt"
    asins = [line.strip() for line in asins_file.read_text().splitlines() if line.strip()]

    print(f"Read {len(asins)} ASINs from {asins_file}")

    # Run BSR tracker with all ASINs
    cmd = [
        sys.executable,
        "bsr_sales_tracker.py",
        *asins,
        "--delay", "2.0",
        "--output", "outputs/bsr_estimates_top100.json"
    ]

    print(f"Running BSR tracker on {len(asins)} products...")
    print(f"Estimated time: {len(asins) * 2.5 / 60:.1f} minutes")
    print()
    sys.stdout.flush()

    # Execute with unbuffered output
    import os
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'

    result = subprocess.run(cmd, cwd=Path(__file__).parent, env=env)

    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
