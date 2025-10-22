#!/usr/bin/env python3
"""
Run batch analysis on 5 consumer videos
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Set up path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from consumer_analyzer import MultiModalAnalyzer

def main():
    """Run analysis on 5 consumer videos"""

    # Project root is 4 levels up from script
    project_root = Path(__file__).parent.parent.parent.parent

    # Use raw_videos directory (real consumer videos)
    video_dir = project_root / 'modules' / 'consumer-video' / 'data' / 'raw_videos'
    output_dir = project_root / 'modules' / 'consumer-video' / 'data' / 'processed'

    print("="*60)
    print("🎬 BATCH ANALYSIS - 5 CONSUMER VIDEOS")
    print("="*60)
    print(f"Video dir: {video_dir}")
    print(f"Output dir: {output_dir}")
    print()

    # Initialize analyzer with FREE tier emotion analysis
    analyzer = MultiModalAnalyzer(
        video_dir=video_dir,
        output_dir=output_dir,
        emotion_tier='FREE'
    )

    # Define 5 videos
    video_ids = ['consumer01', 'consumer02', 'consumer03', 'consumer04', 'consumer05']

    results = []
    start_time = datetime.now()

    for i, video_id in enumerate(video_ids, 1):
        # Read metadata
        metadata_path = video_dir / video_id / 'metadata.json'
        with open(metadata_path) as f:
            metadata = json.load(f)

        print(f"\n{'='*60}")
        print(f"🎯 [{i}/5] Analyzing {video_id}")
        print(f"{'='*60}")
        print(f"Title: {metadata['title']}")
        print(f"Duration: {metadata['duration']}s")
        print()

        video_start = datetime.now()
        analysis = analyzer.analyze_video(video_id)
        video_duration = (datetime.now() - video_start).total_seconds()

        if analysis:
            # Store result
            result = {
                'video_id': video_id,
                'title': metadata['title'],
                'duration': metadata['duration'],
                'processing_time': video_duration,
                'success': True
            }

            # Count insights
            emotion = analysis.get('emotion_analysis', {})
            insights = analysis.get('insights', {})

            result['emotion_events'] = len(emotion.get('timeline', []))
            result['pain_points'] = len(insights.get('pain_points', []))
            result['solutions'] = len(insights.get('solutions', []))

            results.append(result)

            print(f"\n✅ {video_id} complete:")
            print(f"   Processing time: {video_duration:.1f}s")
            print(f"   Emotion events: {result['emotion_events']}")
            print(f"   Pain points: {result['pain_points']}")
            print(f"   Solutions: {result['solutions']}")
        else:
            print(f"\n❌ {video_id} FAILED")
            results.append({
                'video_id': video_id,
                'success': False
            })

    # Final summary
    total_duration = (datetime.now() - start_time).total_seconds()
    successful = sum(1 for r in results if r['success'])

    print("\n" + "="*60)
    print("✅ BATCH ANALYSIS COMPLETE")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   Videos processed: {successful}/{len(video_ids)}")
    print(f"   Total processing time: {total_duration/60:.1f} minutes")
    print(f"   Average per video: {total_duration/len(video_ids):.1f}s")

    total_emotion = sum(r.get('emotion_events', 0) for r in results)
    total_pain = sum(r.get('pain_points', 0) for r in results)
    total_solutions = sum(r.get('solutions', 0) for r in results)

    print(f"\n💡 Total Insights Extracted:")
    print(f"   Emotion events: {total_emotion}")
    print(f"   Pain points: {total_pain}")
    print(f"   Solutions: {total_solutions}")

    print(f"\n💾 Individual analyses saved to:")
    for video_id in video_ids:
        print(f"   - {output_dir}/{video_id}/analysis.json")

    # Save batch summary
    summary_path = output_dir / 'batch_summary.json'
    with open(summary_path, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_videos': len(video_ids),
            'successful': successful,
            'total_processing_time': total_duration,
            'results': results
        }, f, indent=2)

    print(f"\n💾 Batch summary: {summary_path}")

if __name__ == "__main__":
    main()
