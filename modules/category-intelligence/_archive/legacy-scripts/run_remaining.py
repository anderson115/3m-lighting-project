#!/usr/bin/env python3
"""Run BSR tracker on remaining ASINs"""
import subprocess
import sys
from pathlib import Path

asins = Path("asins_remaining.txt").read_text().strip().split('\n')
asins = [a.strip() for a in asins if a.strip()]

cmd = [
    sys.executable,
    "bsr_sales_tracker.py",
    *asins,
    "--delay", "2.0",
    "--output", "outputs/bsr_estimates_remaining.json"
]

print(f"Processing {len(asins)} remaining products...")
sys.stdout.flush()

import os
env = os.environ.copy()
env['PYTHONUNBUFFERED'] = '1'

subprocess.run(cmd, cwd=Path(__file__).parent, env=env)
