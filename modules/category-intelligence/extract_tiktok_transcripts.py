#!/usr/bin/env python3
"""
Extract transcripts from downloaded TikTok videos using Whisper.
"""

import os
import json
from pathlib import Path
import whisper

# Load TikTok metadata
data_file = Path(__file__).parent / "data" / "tiktok_garage_consumer_insights.json"

if not data_file.exists():
    print("❌ TikTok data file not found. Run collect_tiktok_apify.py first.")
    exit(1)

with open(data_file) as f:
    data = json.load(f)

videos = data['videos']

print("="*70)
print("TIKTOK TRANSCRIPT EXTRACTION")
print(f"Videos to process: {len(videos)}")
print("="*70)
print()

# Create output directory for transcripts
transcript_dir = Path(__file__).parent / "data" / "tiktok_transcripts"
transcript_dir.mkdir(exist_ok=True)

video_dir = Path(__file__).parent / "data" / "tiktok_videos"

# Load Whisper model
print("Loading Whisper model (base)...")
model = whisper.load_model("base")
print("✓ Model loaded")
print()

# Track progress
successful = 0
failed = 0
skipped = 0

for i, video in enumerate(videos, 1):
    video_id = video['id']
    caption = video.get('text', '')[:50]

    print(f"[{i}/{len(videos)}] Processing: {caption}")
    print(f"   Video ID: {video_id}")

    # Check if transcript already exists
    transcript_file = transcript_dir / f"{video_id}.txt"
    if transcript_file.exists():
        print(f"   ⏭️  Transcript already exists, skipping")
        skipped += 1
        continue

    # Check if video file exists
    video_path = video_dir / f"{video_id}.mp4"
    if not video_path.exists():
        print(f"   ❌ Video file not found")
        failed += 1
        continue

    try:
        # Transcribe with Whisper
        print(f"   📝 Transcribing...")
        result = model.transcribe(str(video_path))
        transcript = result["text"]

        # Combine caption + transcript
        full_text = f"CAPTION: {video.get('text', '')}\n\nTRANSCRIPT: {transcript}"

        # Save transcript
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(full_text)

        print(f"   ✓ Saved ({len(transcript)} chars)")
        successful += 1

        # Progress update every 25 videos
        if i % 25 == 0:
            print()
            print(f"   Progress: {successful} successful, {failed} failed, {skipped} skipped")
            print()

    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        failed += 1
        continue

print()
print("="*70)
print("TIKTOK TRANSCRIPT EXTRACTION COMPLETE")
print("="*70)
print(f"Successful: {successful}")
print(f"Failed: {failed}")
print(f"Skipped (already existed): {skipped}")
print(f"Total transcripts: {successful + skipped}")
print()
print(f"Transcripts saved to: {transcript_dir}")
print("="*70)

# Save transcript metadata
transcript_metadata = {
    "total_videos": len(videos),
    "successful": successful,
    "failed": failed,
    "skipped": skipped,
    "transcript_directory": str(transcript_dir)
}

metadata_file = Path(__file__).parent / "data" / "tiktok_transcript_metadata.json"
with open(metadata_file, 'w') as f:
    json.dump(transcript_metadata, f, indent=2)

print(f"\nMetadata saved to: {metadata_file}")
