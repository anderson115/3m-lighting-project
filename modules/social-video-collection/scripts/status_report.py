#!/usr/bin/env python3
"""Generate status report for video processing pipeline"""

import json
from pathlib import Path

data_dir = Path("data/processed/garage-organizers-tiktok")
videos_dir = data_dir / "videos"

# Load search results
with open(data_dir / "search_results.json") as f:
    search_data = json.load(f)

total_videos = len(search_data["videos"])
video_ids = [v["id"] for v in search_data["videos"]]

# Count pipeline stages
downloaded = 0
transcribed = 0
visual_extracted = 0
audio_features = 0
fully_processed = 0

# Check each video
status_by_video = []

for video_id in video_ids:
    video_dir = videos_dir / video_id

    has_video = (video_dir / "video.mp4").exists()
    has_transcript = (video_dir / "transcript.json").exists()
    has_frames = (video_dir / "frames").exists()
    has_audio = (video_dir / "audio_features.json").exists()

    if has_video:
        downloaded += 1
    if has_transcript:
        transcribed += 1
    if has_frames:
        visual_extracted += 1
    if has_audio:
        audio_features += 1
    if has_video and has_transcript and has_frames and has_audio:
        fully_processed += 1

    # Determine status
    if not has_video:
        status = "❌ Not Downloaded"
    elif has_video and has_transcript and has_frames and has_audio:
        status = "✅ COMPLETE"
    elif has_transcript:
        status = "🎤 Transcribed (pending visual+audio)"
    else:
        status = "📥 Downloaded Only"

    status_by_video.append((video_id, status))

# Print report
print("=" * 70)
print("VIDEO PROCESSING PIPELINE STATUS")
print("=" * 70)
print()
print("📊 OVERALL STATISTICS")
print("-" * 70)
print(f"  Total Videos Collected:        {total_videos}")
print(f"  Downloaded (video.mp4):        {downloaded}/{total_videos}")
print(f"  Transcribed (transcript.json): {transcribed}/{total_videos}")
print(f"  Visual Extracted (frames/):    {visual_extracted}/{total_videos}")
print(f"  Audio Features (audio_features.json): {audio_features}/{total_videos}")
print(f"  Fully Processed (all stages):  {fully_processed}/{total_videos}")
print()

# Calculate percentages
print("📈 PIPELINE COMPLETION")
print("-" * 70)
print(f"  Stage 1 - Search:       100% ({total_videos}/{total_videos})")
print(f"  Stage 2 - Download:     {int(downloaded/total_videos*100)}% ({downloaded}/{total_videos})")
print(f"  Stage 3 - Transcribe:   {int(transcribed/total_videos*100)}% ({transcribed}/{total_videos})")
print(f"  Stage 4 - Visual:       {int(visual_extracted/total_videos*100)}% ({visual_extracted}/{total_videos})")
print(f"  Stage 5 - Audio:        {int(audio_features/total_videos*100)}% ({audio_features}/{total_videos})")
print(f"  Complete Pipeline:      {int(fully_processed/total_videos*100)}% ({fully_processed}/{total_videos})")
print()

# Show failed transcriptions
failed_count = downloaded - transcribed
if failed_count > 0:
    print(f"⚠️  TRANSCRIPTION FAILURES: {failed_count} videos")
    print("-" * 70)
    print(f"  Downloaded but not transcribed: {failed_count} videos")
    print(f"  Error: PyTorch/Whisper version incompatibility")
    print()

# Per-video status (first 10)
print("📹 PER-VIDEO STATUS (First 10)")
print("-" * 70)
for i, (video_id, status) in enumerate(status_by_video[:10], 1):
    # Get URL from search results
    video_data = next(v for v in search_data["videos"] if v["id"] == video_id)
    url = video_data.get("webVideoUrl", "N/A")
    print(f"{i:2}. {video_id}")
    print(f"    Status: {status}")
    print(f"    URL: {url}")

print()
print("=" * 70)
