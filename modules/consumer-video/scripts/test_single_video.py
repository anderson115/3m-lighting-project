#!/usr/bin/env python3
"""
Test consumer analyzer on a single video from checkpoint test data
"""

import sys
from pathlib import Path

# Set up path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from consumer_analyzer import MultiModalAnalyzer

def main():
    """Test on a single checkpoint test video"""

    # Project root is 4 levels up from script
    project_root = Path(__file__).parent.parent.parent.parent

    # Use test input directory
    video_dir = project_root / 'modules' / 'consumer-video' / 'data' / 'test_input'
    output_dir = project_root / 'modules' / 'consumer-video' / 'data' / 'test_output'

    print("="*60)
    print("🧪 CONSUMER VIDEO MODULE - SINGLE VIDEO TEST")
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

    # Test on test video
    video_id = 'testvideo'
    print(f"\n🎯 Testing on {video_id}...")
    analysis = analyzer.analyze_video(video_id)

    if analysis:
        print("\n" + "="*60)
        print("✅ TEST PASSED - Analysis Complete")
        print("="*60)

        # Check emotion analysis
        emotion = analysis.get('emotion_analysis', {})
        if 'timeline' in emotion:
            print(f"\n📊 Emotion Timeline:")
            for event in emotion['timeline'][:5]:  # Show first 5 events
                print(f"   {event['timestamp']:.1f}s: {event['emotion']} (confidence: {event['confidence']:.2f})")

        if 'key_moments' in emotion:
            print(f"\n🎯 Key Emotional Moments: {len(emotion['key_moments'])}")
            for moment in emotion['key_moments'][:3]:  # Show top 3
                print(f"   {moment['timestamp']:.1f}s: {moment['emotion']} (confidence: {moment['confidence']:.2f})")
                print(f"      Quote: {moment['quote'][:80]}...")

        if 'summary' in emotion:
            summary = emotion['summary']
            print(f"\n📈 Emotion Summary:")
            print(f"   Dominant: {summary.get('dominant_emotion', 'N/A')}")
            print(f"   Distribution: {summary.get('emotion_distribution', {})}")

        print(f"\n💾 Full analysis saved to: {output_dir}/{video_id}/analysis.json")
        print("\n✅ Consumer video module emotion analysis working!")

    else:
        print("\n❌ TEST FAILED - Analysis returned None")
        sys.exit(1)

if __name__ == "__main__":
    main()
