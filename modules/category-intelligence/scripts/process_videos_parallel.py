#!/usr/bin/env python3
"""
Optimized parallel video processing: 4 workers, medium Whisper model, keyframe extraction
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import subprocess
import multiprocessing as mp
from functools import partial
import traceback

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
CATEGORY_INTEL_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "core"))

print("=" * 80)
print("OPTIMIZED PARALLEL VIDEO PROCESSING")
print("4 Workers | Whisper Medium | Smart Keyframes")
print("=" * 80)

# Configuration
VIDEO_SOURCE = CATEGORY_INTEL_ROOT / "data" / "social_videos" / "TEST_THREE_VIDEOS.json"  # TEST MODE
OUTPUT_BASE = CATEGORY_INTEL_ROOT / "data" / "processed_videos"
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

# Create organized output structure
DIRS = {
    "raw_videos": OUTPUT_BASE / "raw_videos",
    "audio": OUTPUT_BASE / "audio",
    "transcripts": OUTPUT_BASE / "transcripts",
    "frames": OUTPUT_BASE / "frames",
    "insights": OUTPUT_BASE / "insights",
    "reports": OUTPUT_BASE / "reports"
}

for dir_path in DIRS.values():
    dir_path.mkdir(parents=True, exist_ok=True)

# Load Whisper once per worker (not per video)
WHISPER_MODEL = None

def init_worker():
    """Initialize Whisper model once per worker process"""
    global WHISPER_MODEL
    import whisper
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    print(f"[Worker {mp.current_process().name}] Loading Whisper medium model...")
    WHISPER_MODEL = whisper.load_model("medium")  # 3x faster than large-v3
    print(f"[Worker {mp.current_process().name}] Model loaded")

def process_single_video(video_data):
    """Process a single video (called by worker)"""
    global WHISPER_MODEL

    video = video_data["video"]
    index = video_data["index"]
    total = video_data["total"]

    video_id = video.get('video_id')
    title = video.get('title', 'Unknown')[:60]
    url = video.get('url', '')

    worker_name = mp.current_process().name

    # Skip videos with no video_id
    if not video_id:
        return {
            "video_id": None,
            "title": title,
            "url": url,
            "processed_at": datetime.now().isoformat(),
            "overall_status": "⏭️  SKIPPED: No video_id",
            "worker": worker_name
        }

    print(f"\n[{worker_name}] [{index}/{total}] {title}")
    print(f"[{worker_name}] Video ID: {video_id}")

    result = {
        "video_id": video_id,
        "title": title,
        "url": url,
        "processed_at": datetime.now().isoformat(),
        "status": {},
        "worker": worker_name
    }

    try:
        # Step 1: Download video
        print(f"[{worker_name}] [1/4] 📥 Downloading...")
        video_path = DIRS["raw_videos"] / f"{video_id}.mp4"

        if video_path.exists():
            print(f"[{worker_name}]    ⏭️  Cached")
            result["status"]["download"] = "✓ (cached)"
        else:
            ytdlp_cmd = [
                "yt-dlp",
                "-f", "best[ext=mp4]",
                "--no-playlist",
                "--no-warnings",
                "-o", str(DIRS["raw_videos"] / f"{video_id}.%(ext)s"),
                url
            ]
            subprocess.run(ytdlp_cmd, capture_output=True, check=True, timeout=120)

            if video_path.exists():
                print(f"[{worker_name}]    ✓ Downloaded")
                result["status"]["download"] = "✓"
            else:
                raise Exception("Download failed")

        # Step 2: Extract audio
        print(f"[{worker_name}] [2/4] 🎵 Extracting audio...")
        audio_path = DIRS["audio"] / f"{video_id}.wav"

        if audio_path.exists():
            print(f"[{worker_name}]    ⏭️  Cached")
            result["status"]["audio"] = "✓ (cached)"
        else:
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", str(video_path),
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1",
                str(audio_path),
                "-y"
            ]
            subprocess.run(ffmpeg_cmd, capture_output=True, check=True, timeout=120)

            if audio_path.exists():
                print(f"[{worker_name}]    ✓ Extracted")
                result["status"]["audio"] = "✓"
            else:
                raise Exception("Audio extraction failed")

        # Step 3: Transcribe with Whisper medium
        print(f"[{worker_name}] [3/4] 📝 Transcribing (medium)...")
        transcript_path = DIRS["transcripts"] / f"{video_id}.json"

        if transcript_path.exists():
            print(f"[{worker_name}]    ⏭️  Cached")
            result["status"]["transcript"] = "✓ (cached)"
            # Load word count from existing transcript
            with open(transcript_path) as f:
                existing = json.load(f)
                result["word_count"] = existing.get("word_count", 0)
        else:
            # Use pre-loaded model
            transcript_result = WHISPER_MODEL.transcribe(str(audio_path), language="en")

            transcript_data = {
                "video_id": video_id,
                "title": title,
                "text": transcript_result["text"],
                "segments": [{
                    "start": s["start"],
                    "end": s["end"],
                    "text": s["text"]
                } for s in transcript_result["segments"]],
                "word_count": len(transcript_result["text"].split()),
                "duration": transcript_result["segments"][-1]["end"] if transcript_result["segments"] else 0
            }

            with open(transcript_path, 'w') as f:
                json.dump(transcript_data, f, indent=2)

            print(f"[{worker_name}]    ✓ {len(transcript_data['segments'])} segments, {transcript_data['word_count']} words")
            result["status"]["transcript"] = "✓"
            result["word_count"] = transcript_data['word_count']

        # Step 4: Extract keyframes (every 5 seconds)
        print(f"[{worker_name}] [4/4] 🖼️  Extracting frames...")
        frames_dir = DIRS["frames"] / video_id
        frames_dir.mkdir(exist_ok=True)

        existing_frames = list(frames_dir.glob("*.jpg"))
        if len(existing_frames) > 0:
            print(f"[{worker_name}]    ⏭️  Cached ({len(existing_frames)} frames)")
            result["status"]["frames"] = f"✓ (cached, {len(existing_frames)} frames)"
            result["frame_count"] = len(existing_frames)
        else:
            import cv2
            cap = cv2.VideoCapture(str(video_path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = 5  # Extract every 5 seconds

            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                if int(current_time) % frame_interval == 0:
                    frame_path = frames_dir / f"frame_{int(current_time):04d}s.jpg"
                    if not frame_path.exists():  # Avoid duplicates
                        cv2.imwrite(str(frame_path), frame)
                        frame_count += 1

            cap.release()
            print(f"[{worker_name}]    ✓ {frame_count} frames")
            result["status"]["frames"] = f"✓ {frame_count} frames"
            result["frame_count"] = frame_count

        # Success
        result["overall_status"] = "✓ SUCCESS"
        print(f"[{worker_name}] ✅ Complete")
        return result

    except Exception as e:
        result["overall_status"] = f"✗ FAILED: {str(e)}"
        result["error"] = str(e)
        result["traceback"] = traceback.format_exc()
        print(f"[{worker_name}] ❌ Error: {str(e)}")
        return result

def main():
    # Load collected videos
    print(f"\n📥 Loading: {VIDEO_SOURCE.name}")

    with open(VIDEO_SOURCE) as f:
        data = json.load(f)

    videos = data['videos']
    print(f"✓ Found {len(videos)} videos")

    # Prepare video data with indices
    video_data_list = [
        {"video": video, "index": i+1, "total": len(videos)}
        for i, video in enumerate(videos)
    ]

    # Determine number of workers
    num_workers = min(4, mp.cpu_count(), len(videos))
    print(f"\n🚀 Starting {num_workers} parallel workers...")
    print(f"⏱️  Estimated time: ~{len(videos) * 3 / num_workers:.0f} minutes")
    print(f"📦 Model: Whisper medium (3x faster)")
    print(f"🖼️  Frames: Every 5 seconds\n")

    # Process videos in parallel
    with mp.Pool(processes=num_workers, initializer=init_worker) as pool:
        results = pool.map(process_single_video, video_data_list)

    # Calculate stats
    successful = sum(1 for r in results if r["overall_status"] == "✓ SUCCESS")
    failed = sum(1 for r in results if "FAILED" in r["overall_status"])
    skipped = sum(1 for r in results if "SKIPPED" in r["overall_status"])

    # Save results
    progress_file = OUTPUT_BASE / "processing_log.json"
    with open(progress_file, 'w') as f:
        json.dump({
            "processed_at": datetime.now().isoformat(),
            "total_videos": len(videos),
            "successful": successful,
            "failed": failed,
            "skipped": skipped,
            "num_workers": num_workers,
            "model": "whisper-medium",
            "videos": results
        }, f, indent=2)

    # Final summary
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"\n📊 Results:")
    print(f"   ✓ Successful: {successful}/{len(videos)}")
    print(f"   ✗ Failed: {failed}/{len(videos)}")
    print(f"   ⏭️  Skipped: {skipped}/{len(videos)}")
    print(f"\n📁 Output: {OUTPUT_BASE}")
    print(f"📄 Log: {progress_file}")

    # Generate summary report
    report_path = DIRS["reports"] / f"processing_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, 'w') as f:
        f.write(f"# Parallel Video Processing Report\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
        f.write(f"## Configuration\n\n")
        f.write(f"- Workers: {num_workers}\n")
        f.write(f"- Model: Whisper medium\n")
        f.write(f"- Frame interval: 5 seconds\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- Total videos: {len(videos)}\n")
        f.write(f"- Successful: {successful}\n")
        f.write(f"- Failed: {failed}\n")
        f.write(f"- Skipped: {skipped}\n")
        f.write(f"- Success rate: {successful/len(videos)*100:.1f}%\n\n")
        f.write(f"## Processed Videos\n\n")
        for result in results:
            status_emoji = "✅" if result["overall_status"] == "✓ SUCCESS" else "❌" if "FAILED" in result["overall_status"] else "⏭️"
            f.write(f"### {status_emoji} {result['title']}\n\n")
            f.write(f"- Video ID: `{result['video_id']}`\n")
            f.write(f"- Worker: {result.get('worker', 'unknown')}\n")
            f.write(f"- Status: {result['overall_status']}\n")
            if result.get('word_count'):
                f.write(f"- Word count: {result['word_count']}\n")
            if result.get('frame_count'):
                f.write(f"- Frames: {result['frame_count']}\n")
            f.write(f"\n")

    print(f"📄 Report: {report_path}\n")
    print("✓ Done!")

if __name__ == "__main__":
    main()
