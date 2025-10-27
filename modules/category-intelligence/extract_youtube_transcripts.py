#!/usr/bin/env python3
"""
Download videos and extract transcripts from collected YouTube data.
Uses yt-dlp for download and Whisper for transcription.
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

# Load collected video data
data_file = Path(__file__).parent / "data" / "youtube_garage_consumer_insights.json"
with open(data_file) as f:
    data = json.load(f)

videos = data['videos']

print("="*70)
print("YOUTUBE TRANSCRIPT EXTRACTION")
print(f"Videos to process: {len(videos)}")
print("="*70)
print()

# Create output directory for transcripts
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

        model = whisper.load_model("base")  # Use base model for speed
        result = model.transcribe(str(audio_path))

        transcript = result["text"]

        # Save transcript
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcript)

        print(f"   ✓ Transcript saved ({len(transcript)} characters)")

        # Clean up video and audio to save space
        Path(video_path).unlink(missing_ok=True)
        Path(audio_path).unlink(missing_ok=True)

        successful += 1

        # Progress update every 10 videos
        if i % 10 == 0:
            print()
            print(f"   Progress: {successful} successful, {failed} failed, {skipped} skipped")
            print()

    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        failed += 1
        continue

print()
print("="*70)
print("TRANSCRIPT EXTRACTION COMPLETE")
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

metadata_file = Path(__file__).parent / "data" / "transcript_metadata.json"
with open(metadata_file, 'w') as f:
    json.dump(transcript_metadata, f, indent=2)

print(f"\nMetadata saved to: {metadata_file}")
