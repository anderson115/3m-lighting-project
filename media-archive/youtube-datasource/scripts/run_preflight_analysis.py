#!/usr/bin/env python3
"""
Preflight Analysis Runner
Runs multimodal analysis on preflight videos in data/preflight/

Works with the 3-level directory structure:
data/preflight/beginner/
data/preflight/intermediate/
data/preflight/advanced/
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the multimodal analyzer
from scripts.multimodal_analyzer import MultiModalAnalyzer

def find_preflight_videos(preflight_dir: Path) -> dict:
    """Find all preflight videos organized by level"""

    videos = {}

    for level in ['beginner', 'intermediate', 'advanced']:
        level_dir = preflight_dir / level

        if not level_dir.exists():
            continue

        # Find .mp4 files
        mp4_files = list(level_dir.glob('*.mp4'))

        if mp4_files:
            video_file = mp4_files[0]  # Take first .mp4

            # Look for metadata
            metadata_file = level_dir / f"{video_file.stem}_metadata.json"
            metadata = {}
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)

            videos[level] = {
                'level': level,
                'video_id': video_file.stem,
                'video_path': video_file,
                'metadata': metadata
            }

    return videos

def analyze_preflight_videos():
    """Main preflight analysis workflow"""

    print("\n" + "="*60)
    print("🔬 PREFLIGHT ANALYSIS - 3M LIGHTING PROJECT")
    print("="*60)

    # Locate preflight videos
    preflight_dir = project_root / 'data' / 'preflight'

    if not preflight_dir.exists():
        print(f"❌ Preflight directory not found: {preflight_dir}")
        print("   Run: python scripts/preflight_video_selector.py")
        sys.exit(1)

    videos = find_preflight_videos(preflight_dir)

    if not videos:
        print(f"❌ No preflight videos found in {preflight_dir}")
        print("   Expected structure:")
        print("   data/preflight/beginner/*.mp4")
        print("   data/preflight/intermediate/*.mp4")
        print("   data/preflight/advanced/*.mp4")
        sys.exit(1)

    print(f"\n📊 Found {len(videos)} preflight videos:")
    for level, video in videos.items():
        print(f"   {level}: {video['video_path'].name}")

    # Create output directory
    analysis_output_dir = project_root / 'data' / 'preflight_analysis'
    analysis_output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize analyzer
    print("\n🔧 Initializing multimodal analyzer...")

    # Create video directory structure for analyzer (in-place)
    videos_dir = project_root / 'data' / 'preflight_videos'
    videos_dir.mkdir(parents=True, exist_ok=True)

    # Prepare video metadata for analyzer
    for level, video in videos.items():
        video_id = video['video_id']
        video_dir = videos_dir / video_id
        video_dir.mkdir(parents=True, exist_ok=True)

        # Symlink video (avoids copying large files)
        dest_video = video_dir / 'video.mp4'
        if not dest_video.exists():
            dest_video.symlink_to(video['video_path'].resolve())

        # Write metadata with format conversion
        if video['metadata']:
            metadata = video['metadata'].copy()

            # Convert duration_minutes to duration (seconds)
            if 'duration_minutes' in metadata:
                metadata['duration'] = int(metadata['duration_minutes'] * 60)

            # Ensure required fields
            if 'channel' not in metadata and 'channel_title' in metadata:
                metadata['channel'] = metadata['channel_title']

            metadata_path = video_dir / 'metadata.json'
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)

    # Run analyzer
    analyzer = MultiModalAnalyzer(videos_dir, analysis_output_dir)

    start_time = time.time()
    all_analyses = analyzer.analyze_all_videos()
    end_time = time.time()

    total_time = end_time - start_time

    if all_analyses:
        analyzer.generate_summary_report(all_analyses)

        # Generate preflight-specific metrics
        print(f"\n" + "="*60)
        print("📊 PREFLIGHT PERFORMANCE METRICS")
        print("="*60)
        print(f"Total videos analyzed: {len(all_analyses)}")
        print(f"Total processing time: {total_time/60:.1f} minutes")
        print(f"Average time per video: {total_time/len(all_analyses)/60:.1f} minutes")

        # Map analyses back to levels
        level_analyses = {}
        for level, video in videos.items():
            video_id = video['video_id']
            for analysis in all_analyses:
                if analysis['metadata']['video_id'] == video_id:
                    level_analyses[level] = analysis
                    break

        # Print level-specific results
        print(f"\n" + "="*60)
        print("🎯 RESULTS BY LEVEL")
        print("="*60)

        for level in ['beginner', 'intermediate', 'advanced']:
            if level in level_analyses:
                analysis = level_analyses[level]
                insights = analysis.get('insights', {})

                print(f"\n{level.upper()}:")
                print(f"   Title: {analysis['metadata']['title'][:50]}...")
                print(f"   Duration: {analysis['metadata']['duration']//60}m {analysis['metadata']['duration']%60}s")
                print(f"   Pain points found: {len(insights.get('pain_points', []))}")
                print(f"   Solutions found: {len(insights.get('solutions', []))}")
                print(f"   Verbatims extracted: {len(insights.get('verbatims', []))}")

                # Show top pain point
                if insights.get('pain_points'):
                    top_pain = insights['pain_points'][0]
                    print(f"   Top pain point: \"{top_pain['text'][:60]}...\"")

        # Save preflight summary
        preflight_summary = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_videos': len(all_analyses),
                'processing_time_minutes': total_time / 60,
                'avg_time_per_video_minutes': total_time / len(all_analyses) / 60
            },
            'level_results': {}
        }

        for level in ['beginner', 'intermediate', 'advanced']:
            if level in level_analyses:
                analysis = level_analyses[level]
                insights = analysis.get('insights', {})

                preflight_summary['level_results'][level] = {
                    'video_id': analysis['metadata']['video_id'],
                    'title': analysis['metadata']['title'],
                    'duration': analysis['metadata']['duration'],
                    'pain_points_count': len(insights.get('pain_points', [])),
                    'solutions_count': len(insights.get('solutions', [])),
                    'verbatims_count': len(insights.get('verbatims', []))
                }

        summary_path = analysis_output_dir / 'preflight_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(preflight_summary, f, indent=2)

        print(f"\n💾 Preflight summary saved: {summary_path}")

        print("\n✅ Preflight analysis complete!")
        print(f"   Next: python scripts/generate_preflight_report.py")

        return True
    else:
        print("\n⚠️  No videos analyzed successfully")
        return False


if __name__ == "__main__":
    success = analyze_preflight_videos()
    sys.exit(0 if success else 1)
