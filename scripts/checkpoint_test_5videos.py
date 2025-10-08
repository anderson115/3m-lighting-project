#!/usr/bin/env python3
"""
Checkpoint Test: End-to-End 5-Video Analysis
Tests complete pipeline with local-only models (Whisper + LLaVA)
"""
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.multimodal_analyzer import MultiModalAnalyzer

def run_checkpoint_test():
    """Run complete pipeline on 5 test videos"""

    print("\n" + "="*70)
    print("🔬 CHECKPOINT TEST - 5 VIDEO END-TO-END ANALYSIS")
    print("="*70)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖥️  Models: Whisper large-v3 + LLaVA 7B (local only)")
    print("="*70 + "\n")

    # Setup paths
    video_dir = project_root / 'data' / 'checkpoint_test_5videos'
    output_dir = project_root / 'data' / 'checkpoint_test_output'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all video directories
    video_dirs = sorted([d for d in video_dir.iterdir() if d.is_dir() and d.name.startswith('video')])

    if not video_dirs:
        print(f"❌ No video directories found in {video_dir}")
        sys.exit(1)

    print(f"📊 Found {len(video_dirs)} videos to analyze:\n")
    for i, vdir in enumerate(video_dirs, 1):
        video_file = vdir / 'video.mp4'
        if video_file.exists():
            size_mb = video_file.stat().st_size / (1024*1024) if not video_file.is_symlink() else 0
            status = "symlink" if video_file.is_symlink() else f"{size_mb:.1f}MB"
            print(f"   [{i}] {vdir.name}: {status}")

    print()

    # Initialize analyzer
    print("🔧 Initializing multimodal analyzer...\n")
    analyzer = MultiModalAnalyzer(video_dir, output_dir)

    # Track results
    results = []
    start_time = time.time()

    # Process each video
    for i, vdir in enumerate(video_dirs, 1):
        video_id = vdir.name
        video_path = vdir / 'video.mp4'

        if not video_path.exists():
            print(f"⚠️  Skipping {video_id}: video.mp4 not found\n")
            continue

        print(f"\n{'='*70}")
        print(f"[{i}/{len(video_dirs)}] PROCESSING: {video_id}")
        print(f"{'='*70}\n")

        video_start = time.time()

        try:
            # Run full analysis (analyzer expects video_id only, looks for video in video_dir)
            analysis = analyzer.analyze_video(video_id)

            video_duration = time.time() - video_start

            # Save results
            output_file = output_dir / video_id / 'analysis.json'
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)

            results.append({
                'video_id': video_id,
                'success': True,
                'duration_seconds': round(video_duration, 1),
                'pain_points': len(analysis.get('jtbd_insights', {}).get('pain_points', [])),
                'solutions': len(analysis.get('jtbd_insights', {}).get('solutions', [])),
                'frames_analyzed': len(analysis.get('visual_analysis', {}).get('frame_analyses', []))
            })

            print(f"\n✅ {video_id} complete: {video_duration/60:.1f} minutes")
            print(f"   Pain points: {results[-1]['pain_points']}")
            print(f"   Solutions: {results[-1]['solutions']}")
            print(f"   Frames: {results[-1]['frames_analyzed']}")

        except Exception as e:
            print(f"\n❌ {video_id} failed: {str(e)}")
            results.append({
                'video_id': video_id,
                'success': False,
                'error': str(e)
            })

    total_duration = time.time() - start_time

    # Generate summary
    print("\n" + "="*70)
    print("📊 CHECKPOINT TEST SUMMARY")
    print("="*70)

    successful = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]

    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    print(f"⏱️  Total time: {total_duration/60:.1f} minutes")
    if successful:
        print(f"⏱️  Average per video: {total_duration/len(successful)/60:.1f} minutes")

    if successful:
        total_pain_points = sum(r['pain_points'] for r in successful)
        total_solutions = sum(r['solutions'] for r in successful)
        total_frames = sum(r['frames_analyzed'] for r in successful)

        print(f"\n📈 Combined Results:")
        print(f"   Pain points found: {total_pain_points}")
        print(f"   Solutions identified: {total_solutions}")
        print(f"   Frames analyzed: {total_frames}")

    # Save summary
    summary = {
        'test_date': datetime.now().isoformat(),
        'total_videos': len(results),
        'successful': len(successful),
        'failed': len(failed),
        'total_duration_minutes': round(total_duration/60, 1),
        'average_per_video_minutes': round(total_duration/len(successful)/60, 1) if successful else 0,
        'results': results,
        'models': {
            'audio': 'Whisper large-v3',
            'vision': 'LLaVA 7B',
            'mode': 'local-only'
        }
    }

    summary_file = output_dir / 'checkpoint_test_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n💾 Summary saved: {summary_file}")
    print("\n" + "="*70)
    print(f"✅ Checkpoint test complete!")
    print("="*70 + "\n")

    return len(failed) == 0

if __name__ == '__main__':
    success = run_checkpoint_test()
    sys.exit(0 if success else 1)
