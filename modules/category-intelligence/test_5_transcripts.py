#!/usr/bin/env python3
"""
Quick test with 5 videos to verify the fixed script works with existing audio files.
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / '.env')

# Add core to path
sys.path.insert(0, str(project_root / 'core'))

from data_sources.youtube import YouTubeDataSource

# Load test data
data_file = Path(__file__).parent / "data" / "youtube_garage_test_5.json"
with open(data_file) as f:
    data = json.load(f)

videos = data['videos']

print("="*70)
print("YOUTUBE TRANSCRIPT EXTRACTION - 5 VIDEO TEST")
print(f"Videos to process: {len(videos)}")
print("="*70)
print()

# Use same directories as main script
transcript_dir = Path(__file__).parent / "data" / "youtube_transcripts"
transcript_dir.mkdir(exist_ok=True)

video_dir = Path(__file__).parent / "data" / "youtube_videos"
video_dir.mkdir(exist_ok=True)

audio_dir = Path(__file__).parent / "data" / "youtube_audio"
audio_dir.mkdir(exist_ok=True)

# Initialize YouTube data source
yt = YouTubeDataSource()

# Track progress
successful = 0
failed = 0
skipped = 0

for i, video in enumerate(videos, 1):
    video_id = video['video_id']
    title = video['title'][:60]

    print(f"\n[{i}/{len(videos)}] Processing: {title}")
    print(f"   Video ID: {video_id}")

    # Check if transcript already exists
    transcript_file = transcript_dir / f"{video_id}.txt"
    if transcript_file.exists():
        print(f"   ⏭️  Transcript already exists, skipping")
        skipped += 1
        continue

    try:
        # Check if audio file already exists (from previous run)
        audio_file = audio_dir / f"{video_id}.wav"
        if audio_file.exists():
            print(f"   ✓ Audio file already exists")
            audio_path = audio_file
        else:
            # Download video
            print(f"   📥 Downloading video...")
            video_path = yt.download_video(
                video_id=video_id,
                output_dir=str(video_dir)
            )

            if not video_path or not Path(video_path).exists():
                print(f"   ❌ Download failed")
                failed += 1
                continue

            print(f"   ✓ Downloaded: {Path(video_path).name}")

            # Extract audio
            print(f"   🎵 Extracting audio...")
            audio_path = yt.extract_audio(
                video_path=video_path,
                output_dir=str(audio_dir)
            )

            if not audio_path or not Path(audio_path).exists():
                print(f"   ❌ Audio extraction failed")
                failed += 1
                continue

            print(f"   ✓ Audio extracted: {Path(audio_path).name}")

        # Transcribe with Whisper
        print(f"   📝 Transcribing with Whisper...")
        import whisper

        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path))

        transcript = result["text"]

        # Save transcript
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcript)

        print(f"   ✓ Transcript saved ({len(transcript)} characters)")

        successful += 1

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        failed += 1
        continue

print()
print("="*70)
print("5-VIDEO TEST COMPLETE")
print("="*70)
print(f"Successful: {successful}")
print(f"Failed: {failed}")
print(f"Skipped (already existed): {skipped}")
print()

if failed == 0:
    print("✅ TEST PASSED - Ready for full run!")
else:
    print(f"⚠️  {failed} videos failed")
