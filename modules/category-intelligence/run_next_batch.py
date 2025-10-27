#!/usr/bin/env python3
"""Run BSR tracker on next batch of high-potential products"""
import subprocess
import sys
from pathlib import Path

asins = Path("asins_next300.txt").read_text().strip().split('\n')
asins = [a.strip() for a in asins if a.strip()]

print(f"="*70)
print(f"BSR TRACKER - BATCH 2 (HIGH-POTENTIAL PRODUCTS)")
print(f"="*70)
print(f"Products to track: {len(asins)}")
print(f"Estimated time: {len(asins) * 2.5 / 60:.1f} minutes")
print(f"="*70)
print()
sys.stdout.flush()

cmd = [
    sys.executable,
    "bsr_sales_tracker.py",
    *asins,
    "--delay", "2.0",
    "--output", "outputs/bsr_estimates_batch2.json"
]

import os
env = os.environ.copy()
env['PYTHONUNBUFFERED'] = '1'

subprocess.run(cmd, cwd=Path(__file__).parent, env=env)
