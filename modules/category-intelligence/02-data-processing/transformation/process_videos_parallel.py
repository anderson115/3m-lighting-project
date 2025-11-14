#!/usr/bin/env python3

"""Parallel social-video processing with Whisper medium and keyframe extraction."""
from __future__ import annotations
import os

import argparse
import json
import multiprocessing as mp
import subprocess
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

# Paths

SCRIPT_PATH = Path(__file__).resolve()
MODULE_ROOT = SCRIPT_PATH.parents[1]
PROJECT_ROOT = SCRIPT_PATH.parents[3]
DATA_ROOT = Path(os.environ.get("CATEGORY_INTEL_DATA_ROOT", MODULE_ROOT / "data"))
PROCESSED_BASE = Path(os.environ.get("CATEGORY_INTEL_PROCESSED_ROOT", DATA_ROOT / "processed_videos"))
SOCIAL_VIDEOS_DIR = Path(os.environ.get("CATEGORY_INTEL_SOCIAL_DATA", DATA_ROOT / "social_videos"))

# Output directories
DIRS = {
    "raw_videos": PROCESSED_BASE / "raw_videos",
    "audio": PROCESSED_BASE / "audio",
    "transcripts": PROCESSED_BASE / "transcripts",
    "frames": PROCESSED_BASE / "frames",
    "insights": PROCESSED_BASE / "insights",
    "individual": PROCESSED_BASE / "individual",
    "reports": PROCESSED_BASE / "reports",
}

for path in DIRS.values():
    path.mkdir(parents=True, exist_ok=True)

WHISPER_MODEL = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parallel video processor")
    parser.add_argument(
        "--video-source",
        type=Path,
        default=SOCIAL_VIDEOS_DIR / "youtube_3m_claw_FINAL_20251104_194358.json",
        help="Path to collected videos JSON",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=min(4, mp.cpu_count()),
        help="Maximum parallel workers",
    )
    parser.add_argument(
        "--frame-interval",
        type=int,
        default=5,
        help="Fallback interval (seconds) between keyframes",
    )
    parser.add_argument(
        "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Use TEST_THREE_VIDEOS.json regardless of --video-source",
    )
    return parser.parse_args()


def init_worker(model_name: str) -> None:
    global WHISPER_MODEL
    import ssl
    import whisper

    ssl._create_default_https_context = ssl._create_unverified_context
    WHISPER_MODEL = whisper.load_model(model_name)
    print(f"[{mp.current_process().name}] Whisper {model_name} ready", flush=True)


def run_cmd(cmd: List[str], timeout: int = 180) -> None:
    subprocess.run(cmd, check=True, capture_output=True, timeout=timeout)


def load_transcript(path: Path) -> Optional[Dict]:
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def save_json(path: Path, payload: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as handle:
        json.dump(payload, handle, indent=2)


def derive_keyframe_seconds(transcript: Optional[Dict], fallback_interval: int, duration: Optional[float]) -> List[int]:
    if not transcript:
        if duration:
            return list(range(0, int(duration) + fallback_interval, fallback_interval))
        return []

    segments = transcript.get("segments", [])
    targets: Set[int] = set()
    for segment in segments:
        start = segment.get("start")
        end = segment.get("end")
        if start is None:
            continue
        targets.add(int(start))
        if end is not None and end - start >= 12:
            mid = start + (end - start) / 2
            targets.add(int(mid))
    duration_from_transcript = transcript.get("duration")
    ceiling = int(duration_from_transcript if duration_from_transcript else duration or 0)
    if ceiling:
        for point in range(0, ceiling + fallback_interval, fallback_interval):
            targets.add(point)
    return sorted(targets)


def capture_keyframes(video_path: Path, frames_dir: Path, key_seconds: List[int]) -> int:
    if frames_dir.exists():
        existing = list(frames_dir.glob("*.jpg"))
        if existing:
            return len(existing)
    frames_dir.mkdir(parents=True, exist_ok=True)

    import cv2

    cap = cv2.VideoCapture(str(video_path))
    captured: Set[int] = set()
    total = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            second = int(timestamp)
            if key_seconds and second not in key_seconds:
                continue
            if second in captured:
                continue
            frame_path = frames_dir / f"frame_{second:05d}s.jpg"
            cv2.imwrite(str(frame_path), frame)
            captured.add(second)
            total += 1
    finally:
        cap.release()
    return total


def process_single_video(args: Dict) -> Dict:
    global WHISPER_MODEL

    video = args["video"]
    index = args["index"]
    total = args["total"]
    fallback_interval = args["frame_interval"]

    video_id = video.get("video_id")
    title = video.get("title", "Untitled").strip()
    url = video.get("url", "")

    worker = mp.current_process().name
    result = {
        "index": index,
        "video_id": video_id,
        "title": title,
        "url": url,
        "processed_at": datetime.now().isoformat(),
        "status": {},
        "worker": worker,
    }

    if not video_id:
        result["overall_status"] = "⏭️ SKIPPED: missing video_id"
        return result

    print(f"[{worker}] [{index}/{total}] {title}", flush=True)

    try:
        video_path = DIRS["raw_videos"] / f"{video_id}.mp4"
        audio_path = DIRS["audio"] / f"{video_id}.wav"
        transcript_path = DIRS["transcripts"] / f"{video_id}.json"
        frames_dir = DIRS["frames"] / video_id
        individual_dir = DIRS["individual"] / video_id

        # Step 1: Download video
        if video_path.exists():
            result["status"]["download"] = "cached"
        else:
            cmd = [
                "yt-dlp",
                "-f",
                "best[ext=mp4]",
                "--no-playlist",
                "--no-warnings",
                "-o",
                str(DIRS["raw_videos"] / f"{video_id}.%(ext)s"),
                url,
            ]
            run_cmd(cmd, timeout=240)
            result["status"]["download"] = "fresh"

        # Step 2: Audio extraction
        if audio_path.exists():
            result["status"]["audio"] = "cached"
        else:
            cmd = [
                "ffmpeg",
                "-i",
                str(video_path),
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ar",
                "16000",
                "-ac",
                "1",
                str(audio_path),
                "-y",
            ]
            run_cmd(cmd, timeout=240)
            result["status"]["audio"] = "fresh"

        # Step 3: Transcription
        transcript = load_transcript(transcript_path)
        if transcript:
            result["status"]["transcript"] = "cached"
        else:
            transcript_result = WHISPER_MODEL.transcribe(str(audio_path), language="en")
            transcript = {
                "video_id": video_id,
                "title": title,
                "text": transcript_result.get("text", ""),
                "segments": [
                    {
                        "start": seg.get("start"),
                        "end": seg.get("end"),
                        "text": seg.get("text", ""),
                    }
                    for seg in transcript_result.get("segments", [])
                ],
                "word_count": len(transcript_result.get("text", "").split()),
                "duration": transcript_result.get("segments", [{}])[-1].get("end", 0)
                if transcript_result.get("segments")
                else 0,
            }
            save_json(transcript_path, transcript)
            result["status"]["transcript"] = "fresh"
        result["word_count"] = transcript.get("word_count", 0)
        result["duration"] = transcript.get("duration")

        # Step 4: Keyframes
        key_seconds = derive_keyframe_seconds(transcript, fallback_interval, transcript.get("duration"))
        frame_count = capture_keyframes(video_path, frames_dir, key_seconds)
        result["status"]["frames"] = "cached" if frame_count == 0 else f"{frame_count} frames"
        result["frame_count"] = frame_count if frame_count else len(list(frames_dir.glob("*.jpg")))

        # Persist individual summary for brand alignment
        individual_dir.mkdir(parents=True, exist_ok=True)
        summary_path = individual_dir / "summary.json"
        save_json(
            summary_path,
            {
                "video_id": video_id,
                "title": title,
                "url": url,
                "word_count": result.get("word_count", 0),
                "frame_count": result.get("frame_count", 0),
                "processed_at": result["processed_at"],
            },
        )

        result["overall_status"] = "✓ SUCCESS"
        return result

    except subprocess.CalledProcessError as exc:
        result["overall_status"] = f"✗ FAILED: {exc.cmd[-1]}"  # last token to hint stage
        result["stderr"] = exc.stderr.decode("utf-8", "ignore") if exc.stderr else ""
        return result
    except Exception as exc:  # noqa: BLE001 (we need full trace for logging)
        result["overall_status"] = f"✗ FAILED: {exc}"
        result["traceback"] = traceback.format_exc()
        return result


def main() -> None:
    args = parse_args()
    video_source = SOCIAL_VIDEOS_DIR / "TEST_THREE_VIDEOS.json" if args.test else args.video_source

    if not video_source.exists():
        raise FileNotFoundError(f"Video source not found: {video_source}")

    with open(video_source) as handle:
        payload = json.load(handle)

    videos = payload.get("videos", [])
    if not videos:
        print("No videos found in source; stopping.")
        return

    total = len(videos)
    workers = max(1, min(args.max_workers, mp.cpu_count(), total))

    print("=" * 80)
    print("OPTIMIZED PARALLEL VIDEO PROCESSING")
    print(f"Workers: {workers} | Whisper: {args.model} | Keyframe interval: {args.frame_interval}s")
    print("=" * 80)
    print(f"\n📥 Loading {video_source.name}: {total} videos\n")

    job_args = [
        {
            "video": video,
            "index": idx + 1,
            "total": total,
            "frame_interval": args.frame_interval,
        }
        for idx, video in enumerate(videos)
    ]

    with mp.Pool(processes=workers, initializer=init_worker, initargs=(args.model,)) as pool:
        results = pool.map(process_single_video, job_args)

    successful = [r for r in results if r.get("overall_status") == "✓ SUCCESS"]
    failed = [r for r in results if r.get("overall_status", "").startswith("✗")] 
    skipped = [r for r in results if r.get("overall_status", "").startswith("⏭️")]

    log_payload = {
        "processed_at": datetime.now().isoformat(),
        "video_source": str(video_source.relative_to(PROJECT_ROOT)),
        "total_videos": total,
        "successful": len(successful),
        "failed": len(failed),
        "skipped": len(skipped),
        "model": args.model,
        "frame_interval": args.frame_interval,
        "max_workers": workers,
        "videos": results,
    }
    save_json(PROCESSED_BASE / "processing_log.json", log_payload)

    report_lines = [
        "# Parallel Video Processing Report",
        "",
        f"Generated: {log_payload['processed_at']}",
        "",
        "## Summary",
        "",
        f"- Source: {video_source.name}",
        f"- Total videos: {total}",
        f"- Successful: {len(successful)}",
        f"- Failed: {len(failed)}",
        f"- Skipped: {len(skipped)}",
        f"- Whisper model: {args.model}",
        f"- Workers: {workers}",
        f"- Keyframe interval: {args.frame_interval}s",
        "",
        "## Videos",
        "",
    ]
    for result in results:
        status = result.get("overall_status", "?")
        report_lines.append(f"- `{result.get('video_id', 'n/a')}` — {status}")
    report_path = DIRS["reports"] / f"processing_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path.write_text("\n".join(report_lines))

    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"Successful: {len(successful)}/{total}")
    print(f"Failed: {len(failed)} | Skipped: {len(skipped)}")
    print(f"Log: {PROCESSED_BASE / 'processing_log.json'}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
