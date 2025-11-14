#!/usr/bin/env python3
"""
Batch 1 Processing Runner
Processes 5 priority videos for verification
"""

from config import PATHS

import sys
from pathlib import Path
MODULE_ROOT = Path(__file__).resolve().parent
if str(MODULE_ROOT) not in sys.path:
    sys.path.append(str(MODULE_ROOT))

from process_batch import process_batch

# Batch 1: 5 videos for verification
# Priority: Activity 8 (Pain Points) + diverse formats
BATCH_1_VIDEOS = [
    {
        "path": "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos/MarkR_Activity8PainPoints_2025-06-30_115448_1.mov",
        "participant": "MarkR",
        "activity": "Activity8_PainPoints"
    },
    {
        "path": "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos/TylrD_Activity8PainPoints_2025-06-30_052938_1.MOV",
        "participant": "TylrD",
        "activity": "Activity8_PainPoints"
    },
    {
        "path": "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos/GeneK_Activity8PainPoints_2025-06-30_010218_1.webm",
        "participant": "GeneK",
        "activity": "Activity8_PainPoints"
    },
    {
        "path": "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos/FarahN_Activity8PainPoints_2025-07-02_083153_1.MOV",
        "participant": "FarahN",
        "activity": "Activity8_PainPoints"
    },
    {
        "path": "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos/FrederickK_Activity7ToolsandMaterials_2025-07-03_042614_1.mp4",
        "participant": "FrederickK",
        "activity": "Activity7_ToolsandMaterials"
    }
]

OUTPUT_DIR = Path(PATHS["processed"])

if __name__ == "__main__":
    print("=" * 70)
    print("PPS VIDEO PROCESSOR - BATCH 1")
    print("=" * 70)
    print(f"Videos to process: {len(BATCH_1_VIDEOS)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 70)
    print("\n")
    
    results = process_batch(BATCH_1_VIDEOS, OUTPUT_DIR)
    
    print("\n")
    print("=" * 70)
    print("BATCH 1 COMPLETE")
    print("=" * 70)
    
    # Summary
    successful = sum(1 for v in results["videos"] if all(
        status == "success" for status in v["status"].values()
    ))
    
    print(f"\nResults: {successful}/{results['total_videos']} videos fully successful")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Logs: {OUTPUT_DIR}/processing.log")
    print(f"Summary: {OUTPUT_DIR}/batch_summary.json")
    
    sys.exit(0 if successful == results['total_videos'] else 1)
