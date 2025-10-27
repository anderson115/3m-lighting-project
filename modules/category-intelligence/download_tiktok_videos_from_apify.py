#!/usr/bin/env python3
"""
Download TikTok videos from metadata URLs to local filesystem.
"""

import json
import requests
from pathlib import Path

# Load TikTok metadata
data_file = Path(__file__).parent / "data" / "tiktok_garage_consumer_insights.json"

print("Loading TikTok metadata...")
with open(data_file) as f:
    data = json.load(f)

videos = data['videos']

print(f"Found {len(videos)} TikTok videos to download")
print()

# Create output directory
video_dir = Path(__file__).parent / "data" / "tiktok_videos"
video_dir.mkdir(exist_ok=True)

downloaded = 0
failed = 0
skipped = 0

for i, video in enumerate(videos, 1):
    video_id = video['id']
    video_url = video.get('download_url') or video.get('video_url')

    if not video_url:
        print(f"[{i}/{len(videos)}] ❌ No video URL for {video_id}")
        failed += 1
        continue

    video_file = video_dir / f"{video_id}.mp4"

    if video_file.exists():
        # print(f"[{i}/{len(videos)}] ⏭️  Already exists: {video_id}.mp4")
        skipped += 1
        continue

    try:
        print(f"[{i}/{len(videos)}] 📥 Downloading: {video_id}.mp4")

        response = requests.get(video_url, timeout=60)
        if response.status_code == 200:
            with open(video_file, 'wb') as f:
                f.write(response.content)
            print(f"   ✓ Downloaded ({len(response.content) / 1024 / 1024:.1f} MB)")
            downloaded += 1
        else:
            print(f"   ❌ HTTP {response.status_code}")
            failed += 1

    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        failed += 1

    # Progress update every 25 videos
    if i % 25 == 0:
        print()
        print(f"   Progress: {downloaded} downloaded, {skipped} skipped, {failed} failed")
        print()

print()
print("="*70)
print("TIKTOK VIDEO DOWNLOAD COMPLETE")
print("="*70)
print(f"Downloaded: {downloaded}")
print(f"Failed: {failed}")
print(f"Total videos: {downloaded + failed}")
print(f"Videos saved to: {video_dir}")
print("="*70)
