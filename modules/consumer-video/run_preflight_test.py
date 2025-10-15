#!/usr/bin/env python3
"""
Preflight Test: 6 Cryptographically Random Videos
Direct processing test with simplified pipeline
"""

import sys
import json
import time
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

def main():
    """Run preflight test on 6 random videos"""

    print("="*70)
    print("🚀 PREFLIGHT TEST - 6 CRYPTOGRAPHICALLY RANDOM VIDEOS")
    print("="*70)
    print()

    # Load randomly selected videos
    with open('/tmp/preflight_videos.txt') as f:
        video_paths = [line.strip() for line in f if line.strip()]

    print(f"📊 Test Sample: {len(video_paths)} videos")
    print()

    # Display selection
    print("🎲 Cryptographically Random Selection:")
    for i, path in enumerate(video_paths, 1):
        name = Path(path).name
        size_mb = Path(path).stat().st_size / (1024*1024)
        print(f"  {i}. {name} ({size_mb:.1f} MB)")
    print()

    # Create output directory on external drive
    output_base = Path('/Volumes/DATA/consulting/3m-lighting-processed/preflight_test')
    output_base.mkdir(parents=True, exist_ok=True)

    print(f"💾 Output Directory: {output_base}")
    print()

    # Create temporary video directory structure
    temp_video_dir = Path(tempfile.mkdtemp(prefix='preflight_videos_'))
    print(f"📁 Temp Video Dir: {temp_video_dir}")
    print()

    # Copy videos to temp structure (expected by analyzer)
    video_ids = []
    video_map = {}  # Map video_id to original name
    for i, video_path in enumerate(video_paths):
        video_id = f"preflight_video_{i+1:02d}"
        video_ids.append(video_id)
        video_map[video_id] = Path(video_path).name

        video_subdir = temp_video_dir / video_id
        video_subdir.mkdir(parents=True, exist_ok=True)

        # Copy video to expected location
        dest_video = video_subdir / 'video.mp4'
        print(f"  Copying {Path(video_path).name} to {video_id}/...")
        shutil.copy2(video_path, dest_video)

    print(f"✅ {len(video_ids)} videos staged for processing")
    print()

    # Now initialize analyzer and process
    sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
    from consumer_analyzer import MultiModalAnalyzer

    print("🔧 Initializing MultiModalAnalyzer...")
    print("  - Whisper: large-v3")
    print("  - Emotion: Librosa FREE tier")
    print("  - JTBD: Evidence-first extraction")
    print()

    analyzer = MultiModalAnalyzer(
        video_dir=temp_video_dir,
        output_dir=output_base,
        emotion_tier='FREE'
    )

    # Process videos
    results = []
    start_time = datetime.now()

    print("⏱️  Processing Started:", start_time.strftime("%Y-%m-%d %H:%M:%S"))
    print("="*70)
    print()

    for i, video_id in enumerate(video_ids, 1):
        # Get original name from video_map
        original_name = video_map[video_id]

        video_start = time.time()

        print(f"[{i}/{len(video_ids)}] Processing: {original_name}")
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
                    'video': original_name,
                    'video_id': video_id,
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
                'video': original_name,
                'video_id': video_id,
                'success': False,
                'duration_sec': elapsed,
                'error': str(e)
            })

        print()

    # Cleanup temp directory
    print(f"🗑️  Cleaning up temp directory: {temp_video_dir}")
    shutil.rmtree(temp_video_dir)
    print()

    # Summary
    end_time = datetime.now()
    total_duration = (end_time - start_time).total_seconds()

    print("="*70)
    print("📊 PREFLIGHT TEST SUMMARY")
    print("="*70)
    print()

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    print(f"⏱️  Total Time: {total_duration/60:.1f} min ({total_duration:.0f}s)")

    if successful:
        avg_time = sum(r['duration_sec'] for r in successful) / len(successful)
        print(f"⏱️  Avg Time/Video: {avg_time/60:.1f} min ({avg_time:.0f}s)")

        total_jtbds = sum(r['jtbd_count'] for r in successful)
        total_emotions = sum(r['emotion_count'] for r in successful)
        total_products = sum(r['product_count'] for r in successful)

        print()
        print(f"📊 Total Insights Extracted:")
        print(f"   JTBDs: {total_jtbds}")
        print(f"   Emotions: {total_emotions}")
        print(f"   Product Mentions: {total_products}")

    if failed:
        print()
        print("❌ Failed Videos:")
        for r in failed:
            print(f"   - {r['video']}: {r['error']}")

    # Save results
    results_file = output_base / 'preflight_results.json'
    with open(results_file, 'w') as f:
        json.dump({
            'test_date': start_time.isoformat(),
            'total_videos': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'total_duration_sec': total_duration,
            'avg_duration_sec': avg_time if successful else 0,
            'results': results
        }, f, indent=2)

    print()
    print(f"💾 Results saved: {results_file}")
    print()

    # Extrapolate to full corpus
    if successful:
        print("="*70)
        print("📈 EXTRAPOLATION TO FULL CORPUS (82 videos)")
        print("="*70)
        print()

        videos_per_hour = 3600 / avg_time
        total_hours = 82 / videos_per_hour
        parallel_4x_hours = total_hours / 4

        print(f"Sequential Processing:")
        print(f"  Time: {total_hours:.1f} hours ({total_hours*60:.0f} min)")
        print()
        print(f"Parallel 4x Processing (RECOMMENDED):")
        print(f"  Time: {parallel_4x_hours:.1f} hours ({parallel_4x_hours*60:.0f} min)")
        print()

        total_jtbds_projected = (total_jtbds / len(successful)) * 82
        print(f"Expected Insights from 82 videos:")
        print(f"  JTBDs: ~{total_jtbds_projected:.0f}")
        print(f"  Emotions: ~{(total_emotions / len(successful)) * 82:.0f}")
        print(f"  Product Mentions: ~{(total_products / len(successful)) * 82:.0f}")

    print()
    print("="*70)

    if len(successful) == len(results):
        print("✅ PREFLIGHT TEST PASSED - System ready for full corpus processing")
    elif len(successful) >= 4:
        print("⚠️  PREFLIGHT TEST PARTIAL - Review failures before proceeding")
    else:
        print("❌ PREFLIGHT TEST FAILED - Fix issues before full processing")

    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
