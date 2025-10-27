#!/usr/bin/env python3
"""
Progress tracker for social media data collection and transcript extraction.
Shows visual progress bars for all running tasks.
"""

import json
from pathlib import Path
from datetime import datetime

def progress_bar(current, total, width=40, label=""):
    """Create a visual progress bar."""
    if total == 0:
        percentage = 0
    else:
        percentage = min(100, int(100 * current / total))

    filled = int(width * current / total) if total > 0 else 0
    bar = '█' * filled + '░' * (width - filled)

    return f"{label:30s} [{bar}] {current:3d}/{total:3d} ({percentage:3d}%)"

def check_youtube_transcripts():
    """Check YouTube transcript extraction progress."""
    transcript_dir = Path(__file__).parent / "data" / "youtube_transcripts"

    # Total videos expected
    data_file = Path(__file__).parent / "data" / "youtube_garage_consumer_insights.json"
    if not data_file.exists():
        return 0, 0, "Not started"

    with open(data_file) as f:
        data = json.load(f)
    total = data['video_count']

    # Count completed transcripts
    if transcript_dir.exists():
        completed = len(list(transcript_dir.glob("*.txt")))
    else:
        completed = 0

    if completed == 0:
        status = "In progress..."
    elif completed == total:
        status = "✅ Complete"
    else:
        status = f"Processing... ({completed}/{total})"

    return completed, total, status

def check_tiktok_videos():
    """Check TikTok video download progress."""
    video_dir = Path(__file__).parent / "data" / "tiktok_videos"

    # Total videos expected
    data_file = Path(__file__).parent / "data" / "tiktok_garage_consumer_insights.json"
    if not data_file.exists():
        return 0, 0, "Not started"

    with open(data_file) as f:
        data = json.load(f)
    total = data['video_count']

    # Count downloaded videos
    if video_dir.exists():
        completed = len(list(video_dir.glob("*.mp4")))
    else:
        completed = 0

    if completed == 0:
        status = "In progress..."
    elif completed == total:
        status = "✅ Complete"
    else:
        status = f"Downloading... ({completed}/{total})"

    return completed, total, status

def check_tiktok_transcripts():
    """Check TikTok transcript extraction progress."""
    transcript_dir = Path(__file__).parent / "data" / "tiktok_transcripts"

    # Total videos expected
    data_file = Path(__file__).parent / "data" / "tiktok_garage_consumer_insights.json"
    if not data_file.exists():
        return 0, 0, "Not started"

    with open(data_file) as f:
        data = json.load(f)
    total = data['video_count']

    # Count completed transcripts
    if transcript_dir.exists():
        completed = len(list(transcript_dir.glob("*.txt")))
    else:
        completed = 0

    if completed == 0:
        status = "⏳ Waiting for video download"
    elif completed == total:
        status = "✅ Complete"
    else:
        status = f"Processing... ({completed}/{total})"

    return completed, total, status

def main():
    print()
    print("="*80)
    print("SOCIAL MEDIA CONSUMER INSIGHTS COLLECTION - PROGRESS REPORT")
    print("="*80)
    print()

    # YouTube metadata (already complete)
    print("✅ YouTube Metadata Collection")
    print("   119 videos | 46.3M views | 1.08M likes")
    print("   File: youtube_garage_consumer_insights.json")
    print()

    # YouTube transcripts
    yt_completed, yt_total, yt_status = check_youtube_transcripts()
    print(progress_bar(yt_completed, yt_total, label="YouTube Transcripts"))
    print(f"   Status: {yt_status}")
    print()

    # TikTok metadata (already complete)
    print("✅ TikTok Metadata Collection")
    print("   301 videos | 335.9M views | 16.1M likes")
    print("   File: tiktok_garage_consumer_insights.json")
    print()

    # TikTok videos
    tt_vid_completed, tt_vid_total, tt_vid_status = check_tiktok_videos()
    print(progress_bar(tt_vid_completed, tt_vid_total, label="TikTok Video Downloads"))
    print(f"   Status: {tt_vid_status}")
    print()

    # TikTok transcripts
    tt_trans_completed, tt_trans_total, tt_trans_status = check_tiktok_transcripts()
    print(progress_bar(tt_trans_completed, tt_trans_total, label="TikTok Transcripts"))
    print(f"   Status: {tt_trans_status}")
    print()

    # Overall progress
    print("="*80)
    print("OVERALL PROGRESS")
    print("="*80)

    total_tasks = yt_total + tt_vid_total + tt_trans_total
    completed_tasks = yt_completed + tt_vid_completed + tt_trans_completed

    print(progress_bar(completed_tasks, total_tasks, width=60, label="Total Progress"))
    print()

    # Summary stats
    pending = total_tasks - completed_tasks
    if pending == 0:
        print("🎉 ALL TASKS COMPLETE!")
        print()
        print("Final Dataset:")
        print(f"  • 420 total videos (119 YouTube + 301 TikTok)")
        print(f"  • 382.2M combined views")
        print(f"  • Full transcripts for all videos")
        print(f"  • Rich metadata (titles, captions, hashtags, engagement)")
    else:
        print(f"Tasks remaining: {pending}")
        print(f"Estimated completion: 2-4 hours")

        # Breakdown of what's left
        if yt_completed < yt_total:
            print(f"  • YouTube transcripts: {yt_total - yt_completed} remaining")
        if tt_vid_completed < tt_vid_total:
            print(f"  • TikTok videos: {tt_vid_total - tt_vid_completed} remaining")
        if tt_trans_completed < tt_trans_total and tt_vid_completed == tt_vid_total:
            print(f"  • TikTok transcripts: {tt_trans_total - tt_trans_completed} remaining")

    print()
    print("="*80)
    print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print()

if __name__ == "__main__":
    main()
