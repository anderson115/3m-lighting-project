#!/usr/bin/env python3
"""
JTBD-Emotion Cross-Mapper
Link JTBD instances to emotion events for prioritization
"""

from typing import Dict, List, Optional

class JTBDEmotionMapper:
    """Map JTBD instances to emotion events by timestamp proximity"""

    def __init__(self, time_window: float = 5.0):
        """
        Args:
            time_window: Maximum time difference in seconds for emotion-JTBD link (±5s default)
        """
        self.time_window = time_window

    def map_jtbd_to_emotions(self, analysis: Dict) -> List[Dict]:
        """
        Link JTBD instances to nearby emotion events

        Args:
            analysis: Video analysis with JTBD and emotion_analysis sections

        Returns:
            Enhanced JTBD list with emotion_link field
        """

        jtbd_list = analysis.get('jtbd', [])
        emotion_events = analysis.get('emotion_analysis', {}).get('emotion_events', [])

        if not jtbd_list or not emotion_events:
            return jtbd_list

        enhanced_jtbd = []

        for jtbd in jtbd_list:
            jtbd_timestamp = jtbd.get('timestamp', 0)

            # Find closest emotion within time window
            closest_emotion = self._find_closest_emotion(
                jtbd_timestamp,
                emotion_events,
                self.time_window
            )

            # Add emotion link if found
            if closest_emotion:
                jtbd_enhanced = jtbd.copy()
                jtbd_enhanced['emotion_link'] = {
                    'emotion_type': closest_emotion['emotion'],
                    'confidence': closest_emotion['confidence'],
                    'timestamp_delta': abs(closest_emotion['timestamp'] - jtbd_timestamp)
                }

                # Calculate priority based on emotion type and confidence
                jtbd_enhanced['priority'] = self._calculate_priority(
                    closest_emotion['emotion'],
                    closest_emotion['confidence']
                )

                enhanced_jtbd.append(jtbd_enhanced)
            else:
                # No emotion link found - keep original
                enhanced_jtbd.append(jtbd)

        return enhanced_jtbd

    def _find_closest_emotion(
        self,
        jtbd_timestamp: float,
        emotion_events: List[Dict],
        max_delta: float
    ) -> Optional[Dict]:
        """Find emotion event closest to JTBD timestamp within time window"""

        closest = None
        min_delta = max_delta + 1

        for event in emotion_events:
            event_time = event.get('timestamp', 0)
            delta = abs(event_time - jtbd_timestamp)

            if delta <= max_delta and delta < min_delta:
                min_delta = delta
                closest = event

        return closest

    def _calculate_priority(self, emotion_type: str, confidence: float) -> str:
        """
        Calculate JTBD priority based on linked emotion

        High priority: Negative emotions with high confidence
        Medium priority: Neutral or low-confidence emotions
        Low priority: No emotion link or positive emotions
        """

        # Negative emotions indicate pain points
        negative_emotions = ['frustration', 'stress', 'anxiety', 'disappointment', 'concern']
        positive_emotions = ['satisfaction', 'relief', 'pride', 'excitement', 'happiness']

        if emotion_type.lower() in negative_emotions:
            if confidence >= 0.7:
                return 'high'
            else:
                return 'medium'
        elif emotion_type.lower() in positive_emotions:
            return 'low'
        else:
            return 'medium'

    def generate_priority_report(self, enhanced_jtbd: List[Dict]) -> Dict:
        """
        Generate summary report of JTBD priorities

        Args:
            enhanced_jtbd: JTBD list with emotion_link field

        Returns:
            Priority breakdown with counts and examples
        """

        priority_counts = {'high': 0, 'medium': 0, 'low': 0, 'no_emotion': 0}
        priority_examples = {'high': [], 'medium': [], 'low': []}

        for jtbd in enhanced_jtbd:
            priority = jtbd.get('priority', 'no_emotion')

            if priority in priority_counts:
                priority_counts[priority] += 1

                # Store example for each priority level
                if priority != 'no_emotion' and len(priority_examples[priority]) < 3:
                    priority_examples[priority].append({
                        'verbatim': jtbd.get('verbatim', ''),
                        'emotion': jtbd.get('emotion_link', {}).get('emotion_type', ''),
                        'confidence': jtbd.get('emotion_link', {}).get('confidence', 0)
                    })
            else:
                priority_counts['no_emotion'] += 1

        return {
            'total_jtbd': len(enhanced_jtbd),
            'priority_counts': priority_counts,
            'priority_examples': priority_examples,
            'high_priority_percentage': round(
                (priority_counts['high'] / len(enhanced_jtbd)) * 100, 1
            ) if enhanced_jtbd else 0
        }


def main():
    """Test JTBD-emotion mapping on single video"""
    import json
    from pathlib import Path

    # Load test video (consumer04 has both JTBD and emotions)
    test_file = Path(__file__).parent.parent / 'data' / 'processed' / 'consumer04' / 'analysis.json'

    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return

    with open(test_file) as f:
        analysis = json.load(f)

    print("=" * 60)
    print("🔗 JTBD-EMOTION MAPPING TEST")
    print("=" * 60)
    print()

    mapper = JTBDEmotionMapper(time_window=5.0)

    # Original counts
    jtbd_count = len(analysis.get('jtbd', []))
    emotion_count = len(analysis.get('emotion_analysis', {}).get('emotion_events', []))

    print(f"Input: {jtbd_count} JTBD instances, {emotion_count} emotion events")
    print(f"Time window: ±{mapper.time_window}s")
    print()

    # Map JTBD to emotions
    enhanced_jtbd = mapper.map_jtbd_to_emotions(analysis)

    # Count links
    linked_count = sum(1 for j in enhanced_jtbd if 'emotion_link' in j)

    print(f"✅ Linked: {linked_count}/{jtbd_count} JTBD instances")
    print()

    # Show examples
    print("### LINKED JTBD EXAMPLES")
    print()

    for i, jtbd in enumerate(enhanced_jtbd[:3], 1):
        if 'emotion_link' in jtbd:
            print(f"**JTBD {i}:**")
            print(f"  Verbatim: \"{jtbd.get('verbatim', '')}\"")
            print(f"  Categories: {jtbd.get('categories', [])}")
            print(f"  Timestamp: {jtbd.get('timestamp', 0):.1f}s")
            print(f"  Linked Emotion: {jtbd['emotion_link']['emotion_type']}")
            print(f"  Emotion Confidence: {jtbd['emotion_link']['confidence']:.2f}")
            print(f"  Time Delta: {jtbd['emotion_link']['timestamp_delta']:.1f}s")
            print(f"  Priority: {jtbd.get('priority', 'N/A').upper()}")
            print()

    # Generate priority report
    print("=" * 60)
    print("📊 PRIORITY REPORT")
    print("=" * 60)
    print()

    report = mapper.generate_priority_report(enhanced_jtbd)

    print(f"Total JTBD: {report['total_jtbd']}")
    print(f"High Priority: {report['priority_counts']['high']} ({report['high_priority_percentage']}%)")
    print(f"Medium Priority: {report['priority_counts']['medium']}")
    print(f"Low Priority: {report['priority_counts']['low']}")
    print(f"No Emotion Link: {report['priority_counts']['no_emotion']}")
    print()

    if report['priority_examples']['high']:
        print("### HIGH PRIORITY EXAMPLES")
        for ex in report['priority_examples']['high']:
            print(f"  - \"{ex['verbatim']}\"")
            print(f"    Emotion: {ex['emotion']} ({ex['confidence']:.2f})")
        print()


if __name__ == "__main__":
    main()
