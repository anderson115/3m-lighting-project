#!/usr/bin/env python3
"""
Optimized video processor for 3M Lighting consumer videos
Uses faster-whisper for 4x speed improvement
Extracts: transcripts, audio, frames (10s intervals)
"""
import os
import json
import sys
from pathlib import Path
from faster_whisper import WhisperModel
import cv2
from datetime import datetime
import time

# Configuration
OUTPUT_BASE = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data/processed")
FRAME_INTERVAL = 10  # seconds (reduced from 5s for speed)
WHISPER_MODEL_PATH = "/Volumes/TARS/llm-models/whisper"

def process_video(video_path):
    """Process single video with optimized pipeline"""
    start_time = time.time()

    video_path = Path(video_path)
    output_dir = OUTPUT_BASE / video_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Processing: {video_path.name}")
    print(f"{'='*60}")

    results = {
        "source_video": {
            "filename": video_path.name,
            "full_path": str(video_path),
            "stem": video_path.stem
        },
        "processed_at": datetime.now().isoformat(),
        "status": {},
        "processing_time": {}
    }

    # 1. Extract audio
    print("→ Extracting audio...")
    step_start = time.time()
    audio_path = output_dir / "audio.wav"
    try:
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps if fps > 0 else 0
        cap.release()

        ffmpeg_bin = "/Users/anderson115/00-interlink/12-work/3m-lighting-project/bin/ffmpeg"
        cmd = f'{ffmpeg_bin} -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}" -y -loglevel error'
        os.system(cmd)

        results["status"]["audio"] = "✓" if audio_path.exists() else "✗"
        results["video_duration_seconds"] = round(duration, 2)
        results["processing_time"]["audio_extraction"] = round(time.time() - step_start, 2)
    except Exception as e:
        results["status"]["audio"] = f"✗ {str(e)}"
        print(f"  Error: {e}")

    # 2. Transcribe with faster-whisper
    print("→ Transcribing (faster-whisper)...")
    step_start = time.time()
    try:
        # Initialize faster-whisper model
        model = WhisperModel(
            "large-v3",
            device="cpu",
            compute_type="int8",
            download_root=WHISPER_MODEL_PATH
        )

        segments, info = model.transcribe(
            str(audio_path),
            language="en",
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        # Convert segments to list
        transcript_segments = []
        full_text = []
        for segment in segments:
            transcript_segments.append({
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip()
            })
            full_text.append(segment.text.strip())

        transcript = {
            "source_video": video_path.name,
            "text": " ".join(full_text),
            "language": info.language,
            "language_probability": round(info.language_probability, 3),
            "duration": round(info.duration, 2),
            "segments": transcript_segments
        }

        with open(output_dir / "transcript.json", "w") as f:
            json.dump(transcript, f, indent=2)

        results["status"]["transcript"] = "✓"
        results["transcript_word_count"] = len(" ".join(full_text).split())
        results["transcript_segment_count"] = len(transcript_segments)
        results["processing_time"]["transcription"] = round(time.time() - step_start, 2)
    except Exception as e:
        results["status"]["transcript"] = f"✗ {str(e)}"
        print(f"  Error: {e}")

    # 3. Extract frames (10s intervals)
    print("→ Extracting frames (10s intervals)...")
    step_start = time.time()
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    try:
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        extracted_frames = []
        last_saved_time = -FRAME_INTERVAL  # Track last saved timestamp

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            current_time_int = int(current_time)

            # Only save if we've passed the next interval
            if current_time_int % FRAME_INTERVAL == 0 and current_time_int > 0 and current_time_int != last_saved_time:
                frame_filename = f"frame_{current_time_int:04d}s.jpg"
                frame_path = frames_dir / frame_filename
                cv2.imwrite(str(frame_path), frame)
                extracted_frames.append({
                    "filename": frame_filename,
                    "timestamp_seconds": current_time_int
                })
                frame_count += 1
                last_saved_time = current_time_int

        cap.release()
        results["status"]["frames"] = "✓"
        results["frames_extracted"] = frame_count
        results["frame_manifest"] = extracted_frames
        results["processing_time"]["frame_extraction"] = round(time.time() - step_start, 2)
    except Exception as e:
        results["status"]["frames"] = f"✗ {str(e)}"
        print(f"  Error: {e}")

    # Save processing summary
    total_time = time.time() - start_time
    results["processing_time"]["total"] = round(total_time, 2)

    with open(output_dir / "processing_summary.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Complete: {video_path.stem}")
    print(f"  Segments: {results.get('transcript_segment_count', 0)}")
    print(f"  Frames: {frame_count}")
    print(f"  Time: {total_time:.1f}s")

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_optimized.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    process_video(video_path)
