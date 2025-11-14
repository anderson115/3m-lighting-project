#!/usr/bin/env python3
"""
Download and transcribe teardown videos - FIXED VERSION
Improvements:
- 300 second timeout (was 60)
- Retry logic (3 attempts)
- Load Whisper model once
- Better error handling
"""
import json
import subprocess
from pathlib import Path
import time
import whisper

def download_audio(url, output_path, max_retries=3):
    """Download audio with retry logic."""
    for attempt in range(max_retries):
        try:
            subprocess.run([
                'yt-dlp',
                '-f', 'bestaudio',
                '-x',
                '--audio-format', 'wav',
                '--audio-quality', '0',
                '-o', str(output_path),
                url
            ], check=True, capture_output=True, timeout=300)  # 5 minute timeout

            # Check if file exists and has content
            if output_path.exists() and output_path.stat().st_size > 1000:
                return True

        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                print(f"      Timeout, retry {attempt + 1}/{max_retries}")
                time.sleep(2)
            continue
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"      Error, retry {attempt + 1}/{max_retries}")
                time.sleep(2)
            continue

    return False

def main():
    # Load search results
    search_results = json.loads(Path("outputs/teardown_videos_search_results.json").read_text())

    # Create directories
    videos_dir = Path("data/teardown_videos")
    audio_dir = Path("data/teardown_audio")
    transcripts_dir = Path("data/teardown_transcripts")

    for dir_path in [videos_dir, audio_dir, transcripts_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Collect all unique videos
    all_videos = {}
    for asin, data in search_results.items():
        for video in data['videos']:
            all_videos[video['video_id']] = video

    print(f"="*70)
    print(f"DOWNLOADING & TRANSCRIBING TEARDOWN VIDEOS - FIXED VERSION")
    print(f"="*70)
    print(f"Total videos: {len(all_videos)}")
    print(f"Timeout: 300 seconds (5 minutes)")
    print(f"Retries: 3 attempts per video")
    print(f"="*70)
    print()

    # Load Whisper model ONCE
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    print("Model loaded.\n")

    success_count = 0
    error_count = 0
    already_done = 0

    for i, (video_id, video) in enumerate(all_videos.items(), 1):
        print(f"\n[{i}/{len(all_videos)}] {video['title'][:60]}...")
        print(f"    Video ID: {video_id}")

        audio_path = audio_dir / f"{video_id}.wav"
        transcript_path = transcripts_dir / f"{video_id}.txt"

        # Skip if already transcribed
        if transcript_path.exists():
            print(f"    ✓ Already transcribed")
            already_done += 1
            success_count += 1
            continue

        # Download audio with retries
        print(f"    Downloading audio...")
        if not download_audio(video['url'], audio_path):
            print(f"    ✗ Download failed after 3 attempts")
            error_count += 1
            continue

        # Transcribe
        try:
            print(f"    Transcribing...")
            result = model.transcribe(str(audio_path))

            # Save transcript
            transcript_path.write_text(result['text'])

            print(f"    ✓ Complete ({len(result['text'])} characters)")
            success_count += 1

            # Clean up audio file to save space
            audio_path.unlink()

        except Exception as e:
            print(f"    ✗ Transcription error: {str(e)[:50]}")
            error_count += 1

        # Progress update every 10 videos
        if i % 10 == 0:
            print(f"\n  Progress: {success_count} success ({already_done} existing), {error_count} errors")

    print(f"\n\n{'='*70}")
    print(f"DOWNLOAD & TRANSCRIPTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total: {success_count}/{len(all_videos)} ({100*success_count/len(all_videos):.1f}%)")
    print(f"  Already done: {already_done}")
    print(f"  Newly transcribed: {success_count - already_done}")
    print(f"Errors: {error_count}/{len(all_videos)}")
    print(f"Transcripts saved to: {transcripts_dir}")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
