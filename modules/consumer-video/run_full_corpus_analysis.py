#!/usr/bin/env python3
"""
Full Corpus Video Analysis
Processes all consumer interview videos from external drive
Generates comprehensive JTBD analysis report
"""

import sys
import json
import time
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict

def collect_all_videos(source_dir: Path) -> List[Path]:
    """
    Recursively find all video files in source directory
    Filters out macOS metadata files and invalid formats
    """
    print("📁 Scanning for video files...")

    valid_extensions = ['.mp4', '.mov', '.MOV', '.webm', '.avi', '.mkv']
    all_videos = []

    for ext in valid_extensions:
        videos = list(source_dir.rglob(f'*{ext}'))
        # Filter out macOS metadata files
        videos = [v for v in videos if not v.name.startswith('._')]
        all_videos.extend(videos)

    # Sort by name for consistent processing order
    all_videos.sort(key=lambda x: x.name)

    print(f"✅ Found {len(all_videos)} video files")
    return all_videos

def categorize_videos(videos: List[Path]) -> Dict[str, List[Path]]:
    """
    Categorize videos by activity type for reporting
    """
    categories = {
        'intro': [],
        'activity_8_pain_points': [],
        'activity_9_improvements': [],
        'activity_5_choices': [],
        'activity_6_walkthrough': [],
        'other_activities': []
    }

    for video in videos:
        name_lower = video.name.lower()

        if 'q1' in name_lower or 'intro' in name_lower:
            categories['intro'].append(video)
        elif 'activity8' in name_lower or 'painpoint' in name_lower:
            categories['activity_8_pain_points'].append(video)
        elif 'activity9' in name_lower or 'improvement' in name_lower or 'future' in name_lower:
            categories['activity_9_improvements'].append(video)
        elif 'activity5' in name_lower or 'choice' in name_lower or 'lighting' in name_lower:
            categories['activity_5_choices'].append(video)
        elif 'activity6' in name_lower or 'walkthrough' in name_lower:
            categories['activity_6_walkthrough'].append(video)
        else:
            categories['other_activities'].append(video)

    return categories

def main():
    """Run full corpus analysis"""

    print("="*70)
    print("🚀 FULL CORPUS VIDEO ANALYSIS")
    print("="*70)
    print()

    # Configuration
    source_dir = Path('/Volumes/DATA/consulting/3m-lighting-consumer-videos/')
    output_base = Path('/Volumes/DATA/consulting/3m-lighting-processed/full_corpus')
    output_base.mkdir(parents=True, exist_ok=True)

    print(f"📂 Source: {source_dir}")
    print(f"💾 Output: {output_base}")
    print()

    # Verify source exists
    if not source_dir.exists():
        print(f"❌ ERROR: Source directory not found: {source_dir}")
        sys.exit(1)

    # Collect all videos
    all_videos = collect_all_videos(source_dir)

    if not all_videos:
        print("❌ No videos found!")
        sys.exit(1)

    # Categorize videos
    categories = categorize_videos(all_videos)

    print()
    print("📊 VIDEO BREAKDOWN BY CATEGORY:")
    print(f"  Intro (Q1): {len(categories['intro'])} videos")
    print(f"  Activity 8 (Pain Points): {len(categories['activity_8_pain_points'])} videos")
    print(f"  Activity 9 (Improvements): {len(categories['activity_9_improvements'])} videos")
    print(f"  Activity 5 (Choices): {len(categories['activity_5_choices'])} videos")
    print(f"  Activity 6 (Walkthrough): {len(categories['activity_6_walkthrough'])} videos")
    print(f"  Other Activities: {len(categories['other_activities'])} videos")
    print(f"  TOTAL: {len(all_videos)} videos")
    print()

    # Save video list for reference
    video_list_file = output_base / 'video_list.json'
    with open(video_list_file, 'w') as f:
        json.dump({
            'total_videos': len(all_videos),
            'categories': {k: [str(v) for v in videos] for k, videos in categories.items()},
            'scan_date': datetime.now().isoformat()
        }, f, indent=2)
    print(f"📝 Video list saved: {video_list_file}")
    print()

    # Create temporary video directory
    temp_video_dir = Path(tempfile.mkdtemp(prefix='full_corpus_'))
    print(f"📁 Temp Directory: {temp_video_dir}")
    print()

    # Stage videos for processing
    print("📦 Staging videos for analysis...")
    video_ids = []
    video_map = {}  # Map video_id to original info

    for i, video_path in enumerate(all_videos, 1):
        video_id = f"video_{i:04d}"
        video_ids.append(video_id)

        video_subdir = temp_video_dir / video_id
        video_subdir.mkdir(parents=True, exist_ok=True)

        # Copy video to expected location
        dest_video = video_subdir / 'video.mp4'
        print(f"  [{i}/{len(all_videos)}] Staging: {video_path.name}")
        shutil.copy2(video_path, dest_video)

        # Store mapping
        video_map[video_id] = {
            'original_path': str(video_path),
            'original_name': video_path.name,
            'size_mb': video_path.stat().st_size / (1024*1024),
            'category': get_category(video_path, categories)
        }

    print(f"✅ {len(video_ids)} videos staged")
    print()

    # Save video map
    video_map_file = output_base / 'video_mapping.json'
    with open(video_map_file, 'w') as f:
        json.dump(video_map, f, indent=2)

    # Initialize analyzer
    print("🔧 Initializing MultiModalAnalyzer...")
    sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
    from consumer_analyzer import MultiModalAnalyzer

    analyzer = MultiModalAnalyzer(
        video_dir=temp_video_dir,
        output_dir=output_base,
        emotion_tier='FREE'
    )

    # Process all videos
    results = []
    start_time = datetime.now()

    print()
    print("⏱️  Processing Started:", start_time.strftime("%Y-%m-%d %H:%M:%S"))
    print("="*70)
    print()

    for i, video_id in enumerate(video_ids, 1):
        video_info = video_map[video_id]
        video_start = time.time()

        print(f"[{i}/{len(video_ids)}] Processing: {video_info['original_name']}")
        print(f"   Category: {video_info['category']}")
        print(f"   Size: {video_info['size_mb']:.1f} MB")
        print(f"   Started: {datetime.now().strftime('%H:%M:%S')}")

        try:
            # Process video
            analysis = analyzer.analyze_video(video_id)

            elapsed = time.time() - video_start
            print(f"   ✅ Complete in {elapsed/60:.1f} min ({elapsed:.0f}s)")

            # Show key metrics
            if analysis:
                jtbd_count = len(analysis.get('jtbd_events', []))
                emotion_count = len(analysis.get('emotion_events', []))
                product_count = len(analysis.get('product_mentions', []))

                print(f"   📊 JTBDs: {jtbd_count} | Emotions: {emotion_count} | Products: {product_count}")

                results.append({
                    'video_id': video_id,
                    'video': video_info['original_name'],
                    'category': video_info['category'],
                    'success': True,
                    'duration_sec': elapsed,
                    'jtbd_count': jtbd_count,
                    'emotion_count': emotion_count,
                    'product_count': product_count
                })

        except Exception as e:
            elapsed = time.time() - video_start
            print(f"   ❌ Failed after {elapsed:.0f}s: {str(e)}")

            results.append({
                'video_id': video_id,
                'video': video_info['original_name'],
                'category': video_info['category'],
                'success': False,
                'duration_sec': elapsed,
                'error': str(e)
            })

        print()

    # Cleanup temp directory
    print(f"🗑️  Cleaning up temp directory: {temp_video_dir}")
    shutil.rmtree(temp_video_dir)
    print()

    # Generate summary
    end_time = datetime.now()
    total_duration = (end_time - start_time).total_seconds()

    print("="*70)
    print("📊 FULL CORPUS ANALYSIS SUMMARY")
    print("="*70)
    print()

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"✅ Successful: {len(successful)}/{len(results)} ({len(successful)/len(results)*100:.1f}%)")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    print(f"⏱️  Total Time: {total_duration/3600:.1f} hours ({total_duration/60:.1f} min)")

    if successful:
        avg_time = sum(r['duration_sec'] for r in successful) / len(successful)
        print(f"⏱️  Avg Time/Video: {avg_time/60:.1f} min ({avg_time:.0f}s)")

        # Aggregate insights
        total_jtbds = sum(r['jtbd_count'] for r in successful)
        total_emotions = sum(r['emotion_count'] for r in successful)
        total_products = sum(r['product_count'] for r in successful)

        print()
        print(f"📊 TOTAL INSIGHTS EXTRACTED:")
        print(f"   JTBD Events: {total_jtbds}")
        print(f"   Emotion Events: {total_emotions}")
        print(f"   Product Mentions: {total_products}")

        # Breakdown by category
        print()
        print(f"📈 INSIGHTS BY CATEGORY:")
        for category in ['activity_8_pain_points', 'activity_9_improvements', 'activity_5_choices', 'intro', 'other_activities']:
            cat_results = [r for r in successful if r['category'] == category]
            if cat_results:
                cat_jtbds = sum(r['jtbd_count'] for r in cat_results)
                cat_name = category.replace('_', ' ').title()
                print(f"   {cat_name}: {cat_jtbds} JTBDs from {len(cat_results)} videos")

    if failed:
        print()
        print("❌ FAILED VIDEOS:")
        for r in failed:
            print(f"   - {r['video']}: {r['error']}")

    # Save results
    results_file = output_base / 'full_corpus_results.json'
    with open(results_file, 'w') as f:
        json.dump({
            'analysis_date': start_time.isoformat(),
            'total_videos': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'total_duration_sec': total_duration,
            'avg_duration_sec': avg_time if successful else 0,
            'total_jtbd_events': total_jtbds if successful else 0,
            'total_emotion_events': total_emotions if successful else 0,
            'total_product_mentions': total_products if successful else 0,
            'results': results
        }, f, indent=2)

    print()
    print(f"💾 Results saved: {results_file}")
    print()

    print("="*70)
    if len(successful) == len(results):
        print("✅ FULL CORPUS ANALYSIS COMPLETE - All videos processed successfully")
    elif len(successful) > len(results) * 0.9:
        print("⚠️  ANALYSIS COMPLETE - Some videos failed (>90% success)")
    else:
        print("❌ ANALYSIS COMPLETE - Multiple failures detected")
    print("="*70)

def get_category(video_path: Path, categories: Dict[str, List[Path]]) -> str:
    """Get category name for a video"""
    for cat_name, videos in categories.items():
        if video_path in videos:
            return cat_name
    return 'unknown'

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
