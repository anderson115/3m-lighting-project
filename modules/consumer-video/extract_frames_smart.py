#!/usr/bin/env python3
"""
Smart on-demand frame extractor
Extracts frames at intelligently chosen timestamps based on:
- Transcript segment boundaries
- Key moments (detected from transcript content)
- Uniform sampling for visual continuity
"""

from config import PATHS
import json
import sys
import cv2
from pathlib import Path
import re

OUTPUT_BASE = Path(PATHS["processed"])

def extract_frames_smart(video_stem, mode="segment_boundaries", custom_timestamps=None):
    """
    Extract frames intelligently

    Modes:
    - segment_boundaries: Extract at start/end of each transcript segment
    - uniform_10s: Extract every 10 seconds
    - uniform_5s: Extract every 5 seconds
    - key_moments: Extract at detected key moments from transcript
    - custom: Extract at specific timestamps (provide custom_timestamps list)
    """

    processed_dir = OUTPUT_BASE / video_stem
    if not processed_dir.exists():
        print(f"Error: {video_stem} not processed yet")
        return None

    # Load transcript
    transcript_path = processed_dir / "transcript.json"
    if not transcript_path.exists():
        print(f"Error: No transcript found for {video_stem}")
        return None

    with open(transcript_path) as f:
        transcript = json.load(f)

    # Load processing summary to get video path
    summary_path = processed_dir / "processing_summary.json"
    with open(summary_path) as f:
        summary = json.load(f)

    video_path = summary["source_video"]["full_path"]

    # Determine timestamps to extract
    timestamps = []

    if mode == "segment_boundaries":
        # Extract at start and end of each segment
        for seg in transcript["segments"]:
            timestamps.append(seg["start"])
            timestamps.append(seg["end"])

    elif mode == "uniform_10s":
        duration = summary["video_metadata"]["duration_seconds"]
        timestamps = list(range(10, int(duration), 10))

    elif mode == "uniform_5s":
        duration = summary["video_metadata"]["duration_seconds"]
        timestamps = list(range(5, int(duration), 5))

    elif mode == "key_moments":
        # Extract frames at segments containing action words or emotional language
        key_patterns = [
            r'\b(look|see|here|this|show|light|problem|issue|great|love|hate|difficult|easy)\b',
            r'\b(because|why|how|when|where)\b'
        ]
        for seg in transcript["segments"]:
            text_lower = seg["text"].lower()
            for pattern in key_patterns:
                if re.search(pattern, text_lower):
                    # Extract middle of segment
                    mid_time = (seg["start"] + seg["end"]) / 2
                    timestamps.append(mid_time)
                    break

    elif mode == "custom" and custom_timestamps:
        timestamps = custom_timestamps

    else:
        print(f"Unknown mode: {mode}")
        return None

    # Remove duplicates and sort
    timestamps = sorted(set([round(t, 1) for t in timestamps]))

    print(f"Extracting {len(timestamps)} frames from {video_stem} (mode: {mode})")

    # Extract frames
    frames_dir = processed_dir / "frames"
    frames_dir.mkdir(exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    extracted = []
    for timestamp in timestamps:
        frame_number = int(timestamp * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if ret:
            frame_filename = f"frame_{timestamp:07.1f}s.jpg"
            frame_path = frames_dir / frame_filename
            cv2.imwrite(str(frame_path), frame)
            extracted.append({
                "filename": frame_filename,
                "timestamp_seconds": timestamp
            })

    cap.release()

    # Update processing summary
    summary["frames_extracted"] = len(extracted)
    summary["frame_extraction_mode"] = mode
    summary["frame_manifest"] = extracted
    summary["status"]["frames"] = "✓"

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"✓ Extracted {len(extracted)} frames")
    return extracted

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_frames_smart.py <video_stem> [mode]")
        print("Modes: segment_boundaries, uniform_10s, uniform_5s, key_moments")
        sys.exit(1)

    video_stem = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "segment_boundaries"

    extract_frames_smart(video_stem, mode)
