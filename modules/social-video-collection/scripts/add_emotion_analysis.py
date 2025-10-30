#!/usr/bin/env python3
"""
Add Emotion Analysis to All Videos

Processes all existing videos to add high-quality emotion analysis using Claude API.
Requires transcript.json and audio_features.json to already exist.
"""

import sys
import yaml
from pathlib import Path
from processors.emotion_analysis import EmotionAnalysisProcessor


def find_processable_videos(data_dir: Path):
    """Find all videos with transcript + audio features but no emotion analysis"""
    videos_dir = data_dir / "videos"

    processable = []
    skipped = []

    for video_dir in sorted(videos_dir.iterdir()):
        if not video_dir.is_dir() or not video_dir.name.isdigit():
            continue

        has_transcript = (video_dir / "transcript.json").exists()
        has_audio = (video_dir / "audio_features.json").exists()
        has_emotion = (video_dir / "emotion_analysis.json").exists()
        has_video = (video_dir / "video.mp4").exists()

        if has_transcript and has_audio and has_video and not has_emotion:
            processable.append(video_dir)
        elif has_emotion:
            skipped.append(video_dir)

    return processable, skipped


def process_collection(collection_dir: Path, config: dict, force: bool = False):
    """Process all videos in a collection"""

    print(f"\n{'='*70}")
    print(f"Processing: {collection_dir.name}")
    print(f"{'='*70}\n")

    # Find videos to process
    processable, skipped = find_processable_videos(collection_dir)

    if skipped and not force:
        print(f"ℹ️  {len(skipped)} videos already have emotion analysis (skipping)")

    if not processable:
        print(f"✅ All videos in {collection_dir.name} already processed!\n")
        return 0, 0

    print(f"📊 Found {len(processable)} videos to process\n")

    success_count = 0
    failed_count = 0
    failed_videos = []

    for i, video_dir in enumerate(processable, 1):
        video_id = video_dir.name
        video_path = video_dir / "video.mp4"

        print(f"[{i}/{len(processable)}] {video_id}")

        try:
            # Create processor
            processor = EmotionAnalysisProcessor(config, video_dir)

            # Process (metadata not needed for emotion analysis)
            result = processor.run(video_path, {}, force=force)

            print(f"  ✓ Complete - Primary: {result.get('primary_emotion', 'unknown')}, "
                  f"Confidence: {result.get('confidence', 0):.2f}")
            success_count += 1

        except Exception as e:
            print(f"  ✗ Failed: {str(e)[:100]}")
            failed_count += 1
            failed_videos.append((video_id, str(e)))

    # Summary
    print(f"\n{'─'*70}")
    print(f"Collection: {collection_dir.name}")
    print(f"  Success: {success_count}/{len(processable)}")
    print(f"  Failed:  {failed_count}/{len(processable)}")

    if failed_videos:
        print(f"\n⚠️  Failed videos:")
        for vid, error in failed_videos[:10]:
            print(f"  • {vid}: {error[:80]}")

    print()

    return success_count, failed_count


def main():
    """Main entry point"""

    # Default config (minimal - emotion processor doesn't need much)
    config = {
        'emotion_analysis': {
            'model': 'claude-sonnet-4-20250514'
        }
    }

    # Check for force flag
    force = '--force' in sys.argv

    # Find all collections
    processed_dir = Path("data/processed")

    if not processed_dir.exists():
        print("❌ data/processed/ directory not found")
        print("   Run from social-video-collection root directory")
        sys.exit(1)

    collections = [d for d in processed_dir.iterdir()
                  if d.is_dir() and (d / "videos").exists()]

    if not collections:
        print("❌ No collections found in data/processed/")
        sys.exit(1)

    print("\n" + "="*70)
    print("  EMOTION ANALYSIS - ADD TO ALL VIDEOS")
    print("="*70)
    print(f"\nFound {len(collections)} collection(s)")
    print(f"Using Claude API model: {config['emotion_analysis']['model']}")

    if force:
        print("⚠️  FORCE MODE: Will reprocess videos that already have emotion analysis")

    print()

    # Process each collection
    total_success = 0
    total_failed = 0

    for collection in sorted(collections):
        success, failed = process_collection(collection, config, force)
        total_success += success
        total_failed += failed

    # Final summary
    print("="*70)
    print("  FINAL SUMMARY")
    print("="*70)
    print(f"  Total Processed: {total_success}")
    print(f"  Total Failed:    {total_failed}")
    print(f"  Success Rate:    {total_success/(total_success+total_failed)*100:.1f}%"
          if (total_success + total_failed) > 0 else "  N/A")
    print("="*70)
    print()

    if total_failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
