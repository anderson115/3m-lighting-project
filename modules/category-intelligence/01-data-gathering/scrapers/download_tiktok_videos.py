#!/usr/bin/env python3
"""
Download TikTok videos and extract transcripts.
Uses yt-dlp for download and Whisper for transcription.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / '.env')

# Add core to path
sys.path.insert(0, str(project_root / 'core'))

# Load TikTok data
data_file = Path(__file__).parent / "data" / "tiktok_garage_consumer_insights.json"
with open(data_file) as f:
    data = json.load(f)

videos = data['videos']

print("="*70)
print("TIKTOK VIDEO DOWNLOAD + TRANSCRIPTION")
print(f"Videos to process: {len(videos)}")
print("="*70)
print()

# Create output directories
video_dir = Path(__file__).parent / "data" / "tiktok_videos"
video_dir.mkdir(exist_ok=True)

audio_dir = Path(__file__).parent / "data" / "tiktok_audio"
audio_dir.mkdir(exist_ok=True)

transcript_dir = Path(__file__).parent / "data" / "tiktok_transcripts"
transcript_dir.mkdir(exist_ok=True)

# Path to yt-dlp in venv
ytdlp_path = str(project_root / "venv" / "bin" / "yt-dlp")

# Track progress
successful = 0
failed = 0
skipped = 0

for i, video in enumerate(videos, 1):
    video_id = video['id']
    author = video['author']
    text = video.get('text', '')[:60]

    print(f"\n[{i}/{len(videos)}] Processing: @{author}")
    print(f"   Text: {text}...")
    print(f"   Video ID: {video_id}")

    transcript_file = transcript_dir / f"{video_id}.txt"

    # Check if transcript already exists
    if transcript_file.exists():
        print(f"   ⏭️  Transcript already exists, skipping")
        skipped += 1
        continue

    # Construct TikTok URL
    url = f"https://www.tiktok.com/@{author}/video/{video_id}"

    video_file = video_dir / f"{video_id}.mp4"
    audio_file = audio_dir / f"{video_id}.wav"

    try:
        # Download video with yt-dlp (or use existing)
        if video_file.exists():
            print(f"   ✓ Video already exists")
        else:
            print(f"   📥 Downloading video...")
            result = subprocess.run(
                [ytdlp_path, "-o", str(video_file), url],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                print(f"   ❌ Download failed: {result.stderr[:100]}")
                failed += 1
                continue

            print(f"   ✓ Downloaded ({video_file.stat().st_size / 1024 / 1024:.1f} MB)")

        # Extract audio with ffmpeg (or use existing)
        if audio_file.exists():
            print(f"   ✓ Audio already exists")
        else:
            print(f"   🎵 Extracting audio...")
            result = subprocess.run(
                [
                    "ffmpeg", "-i", str(video_file),
                    "-vn", "-acodec", "pcm_s16le",
                    "-ar", "16000", "-ac", "1",
                    str(audio_file), "-y"
                ],
                capture_output=True,
                timeout=60
            )

            if result.returncode != 0:
                print(f"   ❌ Audio extraction failed")
                failed += 1
                continue

            print(f"   ✓ Audio extracted")

        # Transcribe with Whisper
        print(f"   📝 Transcribing with Whisper...")
        import whisper

        model = whisper.load_model("base")
        result = model.transcribe(str(audio_file))
        transcript = result["text"]

        # Save transcript
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcript)

        print(f"   ✓ Transcript saved ({len(transcript)} characters)")

        # Clean up video and audio to save space (optional)
        # video_file.unlink(missing_ok=True)
        # audio_file.unlink(missing_ok=True)

        successful += 1

        # Progress update every 25 videos
        if i % 25 == 0:
            print()
            print(f"   Progress: {successful} successful, {failed} failed, {skipped} skipped")
            print()

    except subprocess.TimeoutExpired:
        print(f"   ❌ Timeout")
        failed += 1
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        failed += 1

print()
print("="*70)
print("TIKTOK TRANSCRIPTION COMPLETE")
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
