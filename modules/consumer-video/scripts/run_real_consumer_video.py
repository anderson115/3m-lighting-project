#!/usr/bin/env python3
"""
Run analysis on real consumer video
"""

import sys
from pathlib import Path

# Set up path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from consumer_analyzer import MultiModalAnalyzer

def main():
    """Run analysis on first real consumer video"""

    # Project root is 4 levels up from script
    project_root = Path(__file__).parent.parent.parent.parent

    # Use raw_videos directory (real consumer videos)
    video_dir = project_root / 'modules' / 'consumer-video' / 'data' / 'raw_videos'
    output_dir = project_root / 'modules' / 'consumer-video' / 'data' / 'processed'

    print("="*60)
    print("🎬 REAL CONSUMER VIDEO - FIRST ANALYSIS")
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

    # Run on consumer01
    video_id = 'consumer01'
    print(f"\n🎯 Analyzing {video_id} (AlanG Q1 Interview - 43s)...")
    analysis = analyzer.analyze_video(video_id)

    if analysis:
        print("\n" + "="*60)
        print("✅ REAL CONSUMER VIDEO ANALYSIS COMPLETE")
        print("="*60)

        # Check emotion analysis
        emotion = analysis.get('emotion_analysis', {})
        if 'timeline' in emotion:
            print(f"\n📊 Emotion Timeline: {len(emotion['timeline'])} events")
            for event in emotion['timeline'][:5]:
                print(f"   {event['timestamp']:.1f}s: {event['emotion']} (confidence: {event['confidence']:.2f})")

        if 'key_moments' in emotion:
            print(f"\n🎯 Key Emotional Moments: {len(emotion['key_moments'])}")
            for moment in emotion['key_moments'][:3]:
                print(f"   {moment['timestamp']:.1f}s: {moment['emotion']} ({moment['confidence']:.2f})")
                print(f"      \"{moment['quote'][:80]}...\"")

        if 'summary' in emotion:
            summary = emotion['summary']
            print(f"\n📈 Emotion Summary:")
            print(f"   Dominant: {summary.get('dominant_emotion', 'N/A')}")
            print(f"   Distribution: {summary.get('emotion_distribution', {})}")

        # JTBD insights
        insights = analysis.get('insights', {})
        print(f"\n💡 JTBD Insights:")
        print(f"   Pain points: {len(insights.get('pain_points', []))}")
        print(f"   Solutions: {len(insights.get('solutions', []))}")

        print(f"\n💾 Full analysis saved to: {output_dir}/{video_id}/analysis.json")
        print("\n✅ Real consumer video pipeline working!")

    else:
        print("\n❌ ANALYSIS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
