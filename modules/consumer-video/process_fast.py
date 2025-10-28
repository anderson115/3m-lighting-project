#!/usr/bin/env python3
"""
Fast video processor - transcripts + audio only
Frame extraction on-demand via separate tool
"""
import os
import json
import sys
from pathlib import Path
from faster_whisper import WhisperModel
import cv2
from datetime import datetime
import time

OUTPUT_BASE = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data/processed")
WHISPER_MODEL_PATH = "/Volumes/TARS/llm-models/whisper"

def process_video(video_path):
    """Process single video - transcripts + audio only"""
    start_time = time.time()

    video_path = Path(video_path)
    output_dir = OUTPUT_BASE / video_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

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

    # 1. Extract audio + get video metadata
    step_start = time.time()
    audio_path = output_dir / "audio.wav"
    try:
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = total_frames / fps if fps > 0 else 0
        cap.release()

        ffmpeg_bin = "/Users/anderson115/00-interlink/12-work/3m-lighting-project/bin/ffmpeg"
        cmd = f'{ffmpeg_bin} -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}" -y -loglevel error'
        os.system(cmd)

        results["status"]["audio"] = "✓" if audio_path.exists() else "✗"
        results["video_metadata"] = {
            "duration_seconds": round(duration, 2),
            "fps": round(fps, 2),
            "total_frames": int(total_frames)
        }
        results["processing_time"]["audio_extraction"] = round(time.time() - step_start, 2)
    except Exception as e:
        results["status"]["audio"] = f"✗ {str(e)}"
        print(f"  Audio error: {e}")

    # 2. Transcribe with faster-whisper
    step_start = time.time()
    try:
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
        print(f"  Transcript error: {e}")

    # Save processing summary
    total_time = time.time() - start_time
    results["processing_time"]["total"] = round(total_time, 2)
    results["status"]["frames"] = "on_demand"  # Frames extractable via separate tool

    with open(output_dir / "processing_summary.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"✓ {video_path.stem[:30]:<30} | {results.get('transcript_segment_count', 0):2d} segments | {total_time:5.1f}s")

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_fast.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    process_video(video_path)
