#!/usr/bin/env python3
"""
Fast batch processor for 82 consumer videos
Processes transcripts only - frames on-demand later
Batches of 8 for error monitoring
"""
import json
import time
from pathlib import Path
from process_fast import process_video

ALL_VIDEOS = [
    # Q1 Screening Videos (15)
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/AlanG_Q1_2025-06-23_092217_1.mov",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/AlysonT_Q1_2025-06-23_021844_1.mov",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/CarrieS_Q1_2025-06-22_033645_1.mov",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/ChristianL_Q1_2025-06-17_065739_1.mp4",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/DianaL_Q1_2025-06-16_031723_1.mov",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/EllenB_Q1_2025-06-22_064429_1.mp4",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/FarahN_Q1_2025-06-20_064419_1.mov",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/FrederickK_Q1_2025-06-18_065110_1.mp4",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/GeneK_Q1_2025-06-20_045554_1.mov",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/MarkR_Q1_2025-06-17_020436_1.mov",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/RachelL_Q1_2025-06-20_083945_1.MOV",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/RobinL_Q1_2025-06-24_073537_1.mp4",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/TiffanyO_Q1_2025-06-19_112125_1.mov",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/TylrD_Q1_2025-06-20_075938_1.mov",
    "/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/WilliamS_Q1_2025-06-16_052959_1.MOV",
]

def get_core_videos():
    """Dynamically get all core videos"""
    core_dir = Path("/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos/core videos")
    videos = []
    for ext in ["*.mov", "*.MOV", "*.mp4", "*.webm"]:
        videos.extend(sorted(core_dir.glob(ext)))
    return [str(v) for v in videos]

def create_batches(videos, batch_size=8):
    """Split videos into batches"""
    batches = []
    for i in range(0, len(videos), batch_size):
        batches.append(videos[i:i + batch_size])
    return batches

def process_batch(batch_number, videos):
    """Process a single batch of videos"""
    print(f"\n{'#'*80}")
    print(f"# BATCH {batch_number}: {len(videos)} videos")
    print(f"{'#'*80}\n")

    batch_start = time.time()
    results = []

    for i, video_path in enumerate(videos, 1):
        print(f"[{i}/{len(videos)}] ", end="")
        try:
            result = process_video(video_path)
            results.append(result)
        except Exception as e:
            print(f"ERROR: {Path(video_path).name}: {e}")
            results.append({
                "source_video": {"filename": Path(video_path).name, "full_path": str(video_path)},
                "status": {"error": str(e)}
            })

    batch_time = time.time() - batch_start

    print(f"\n{'='*80}")
    print(f"BATCH {batch_number} COMPLETE")
    print(f"Time: {batch_time/60:.1f} min ({batch_time:.0f}s) | Avg: {batch_time/len(videos):.1f}s/video")
    print(f"{'='*80}\n")

    # Save batch summary
    batch_summary = {
        "batch_number": batch_number,
        "videos_processed": len(videos),
        "batch_time_seconds": round(batch_time, 2),
        "average_time_per_video": round(batch_time / len(videos), 2),
        "results": results
    }

    summary_path = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data") / f"batch_{batch_number}_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w") as f:
        json.dump(batch_summary, f, indent=2)

    return batch_summary

if __name__ == "__main__":
    import sys

    # Get all videos
    all_videos = ALL_VIDEOS + get_core_videos()
    print(f"Total videos: {len(all_videos)}")

    # Create batches
    batches = create_batches(all_videos, batch_size=8)
    print(f"Batches: {len(batches)} × 8 videos each\n")

    # Process specified batch (or first batch by default)
    batch_number = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    if batch_number > len(batches):
        print(f"Error: Only {len(batches)} batches available")
        sys.exit(1)

    batch_videos = batches[batch_number - 1]
    process_batch(batch_number, batch_videos)
