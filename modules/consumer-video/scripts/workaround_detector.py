#!/usr/bin/env python3
"""
Workaround Detector
Identify compensating behaviors that signal product gaps
"""

import re
from typing import Dict, List, Optional

class WorkaroundDetector:
    """Detect workarounds - signals of unmet needs"""

    def __init__(self):
        # Sequences indicating improvisation
        self.workaround_signals = {
            'trial_error': [
                r'\bI tried\b.*\bbut\b',
                r'\bfirst I attempted\b.*\bthen\b',
                r"\bthat didn't work so\b",
                r'\btried.*failed\b',
                r'\btried.*wouldn\'t\b'
            ],
            'substitution': [
                r'\bended up using\b',
                r'\bsettled for\b',
                r'\binstead I\b',
                r'\bhad to use\b.*\bbecause\b',
                r'\bwent with\b.*\binstead\b'
            ],
            'modification': [
                r'\bI had to modify\b',
                r'\bcut it to fit\b',
                r'\brigged up\b',
                r'\bmade it work by\b',
                r'\badded.*to make it\b',
                r'\bimprovis\w+\b'
            ],
            'combination': [
                r'\bused\b.*\balong with\b',
                r'\bcombined\b.*\band\b',
                r'\badded\b.*\bto make it\b',
                r'\bput.*together with\b'
            ]
        }

    def detect_workarounds(self, analysis: Dict) -> List[Dict]:
        """
        Detect workaround patterns

        A workaround has three components:
        1. Original intent (what they were trying to do)
        2. Barrier (what prevented straightforward solution)
        3. Alternative path (what they did instead)

        Args:
            analysis: Video analysis with transcription

        Returns:
            List of workaround instances
        """

        transcript = analysis.get('transcription', {})
        segments = transcript.get('segments', [])
        metadata = analysis.get('metadata', {})

        workarounds = []

        for i, segment in enumerate(segments):
            text = segment.get('text', '').strip()
            if not text:
                continue

            # Check if this segment contains workaround language
            if not self._contains_workaround_pattern(text):
                continue

            # Get extended context for full workaround extraction
            context = self._get_context_window(segments, i, window_sentences=5)

            # Extract three components
            components = self._extract_workaround_components(text, context)

            if not components:
                continue

            # Validate: All three components must be present
            if not all([components.get('intent'), components.get('barrier'), components.get('solution')]):
                continue

            # Calculate confidence
            confidence = self._calculate_confidence(components, text, context)

            # Only keep confident workarounds
            if confidence < 0.4:
                continue

            workaround = {
                'workaround_id': f"{metadata.get('video_id', 'unknown')}_wa_{segment.get('start', 0):.0f}",
                'intent': components['intent'],
                'barrier': components['barrier'],
                'solution': components['solution'],
                'verbatim': text,
                'timestamp': segment.get('start', 0),
                'participant': self._extract_participant(metadata.get('title', '')),
                'video_id': metadata.get('video_id', 'unknown'),
                'confidence': confidence,
                'product_mention': self._extract_product_mention(context),
                'context': context
            }

            workarounds.append(workaround)

        return workarounds

    def _contains_workaround_pattern(self, text: str) -> bool:
        """Check if text contains any workaround signal"""

        text_lower = text.lower()

        for signal_type, patterns in self.workaround_signals.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return True

        return False

    def _get_context_window(self, segments: List[Dict], current_index: int, window_sentences: int = 5) -> str:
        """Get surrounding segments for complete workaround"""

        if not segments or current_index < 0 or current_index >= len(segments):
            return ""

        start_idx = max(0, current_index - window_sentences)
        end_idx = min(len(segments), current_index + window_sentences + 1)

        context_segments = [seg.get('text', '') for seg in segments[start_idx:end_idx]]
        return ' '.join(context_segments)

    def _extract_workaround_components(self, text: str, context: str) -> Optional[Dict]:
        """
        Extract intent, barrier, and solution

        Intent: What they were trying to accomplish
        Barrier: What prevented straightforward approach
        Solution: What they did instead
        """

        components = {}

        # Extract intent
        intent = self._extract_intent(text, context)
        if intent:
            components['intent'] = intent

        # Extract barrier
        barrier = self._extract_barrier(text, context)
        if barrier:
            components['barrier'] = barrier

        # Extract solution
        solution = self._extract_solution(text, context)
        if solution:
            components['solution'] = solution

        return components if len(components) >= 2 else None

    def _extract_intent(self, text: str, context: str) -> Optional[str]:
        """Extract original goal"""

        # Intent markers
        intent_patterns = [
            r'(wanted to|trying to|needed to|attempting to|goal was to)\s+([^.,;!?]+)',
            r'(I was|was)\s+(trying to|attempting to|going to|planning to)\s+([^.,;!?]+)',
            r'(to|for)\s+([a-z]+ing\s+[^.,;!?]+)'
        ]

        for pattern in intent_patterns:
            match = re.search(pattern, context.lower())
            if match:
                # Get full phrase
                intent = match.group(0).strip()
                # Clean up
                intent = intent.replace('i was', '').replace('was', '').strip()
                if len(intent) > 10:  # Meaningful length
                    return intent

        return None

    def _extract_barrier(self, text: str, context: str) -> Optional[str]:
        """Extract what prevented straightforward solution"""

        # Barrier markers
        barrier_patterns = [
            r"(but|because|however|since)\s+([^.,;!?]+?(?:wouldn't|didn't|couldn't|can't|won't)[^.,;!?]+)",
            r"(but|because|however|since)\s+([^.,;!?]+?(?:too|not enough|insufficient)[^.,;!?]+)",
            r"(but|because|however|since)\s+([^.,;!?]+?(?:failed|broke|fell)[^.,;!?]+)"
        ]

        for pattern in barrier_patterns:
            match = re.search(pattern, context.lower())
            if match:
                barrier = match.group(0).strip()
                # Remove leading conjunction
                barrier = re.sub(r'^(but|because|however|since)\s+', '', barrier)
                if len(barrier) > 10:
                    return barrier

        return None

    def _extract_solution(self, text: str, context: str) -> Optional[str]:
        """Extract what they did instead"""

        # Solution markers
        solution_patterns = [
            r'(so I|ended up|instead I|settled for|went with)\s+([^.,;!?]+)',
            r'(had to|decided to|chose to)\s+(use|try|make|build|add)\s+([^.,;!?]+)',
            r'(made it work by|rigged up|improvised)\s+([^.,;!?]+)'
        ]

        for pattern in solution_patterns:
            match = re.search(pattern, context.lower())
            if match:
                solution = match.group(0).strip()
                # Clean up
                solution = re.sub(r'^(so|ended up|instead|settled for)\s+', '', solution)
                if len(solution) > 10:
                    return solution

        return None

    def _calculate_confidence(self, components: Dict, text: str, context: str) -> float:
        """
        Calculate confidence in workaround detection

        High: All three components clearly present
        Medium: Two clear + one implied
        Low: Ambiguous interpretation
        """

        confidence = 0.5

        # Check completeness
        complete_components = sum([
            1 if components.get('intent') else 0,
            1 if components.get('barrier') else 0,
            1 if components.get('solution') else 0
        ])

        if complete_components == 3:
            confidence += 0.3
        elif complete_components == 2:
            confidence += 0.1

        # Check for explicit workaround language
        explicit_markers = ['instead', 'ended up', 'had to', 'rigged', 'improvised']
        if any(marker in context.lower() for marker in explicit_markers):
            confidence += 0.1

        # Check specificity
        if len(context) > 100:  # Detailed description
            confidence += 0.1

        return min(1.0, confidence)

    def _extract_product_mention(self, context: str) -> Optional[str]:
        """Extract any product mentions in workaround context"""

        # Check for common product terms
        product_terms = ['command', 'scotch', 'tape', 'adhesive', 'hook', 'strip']

        for term in product_terms:
            if term in context.lower():
                # Extract phrase around product mention
                pattern = r'([^.,;!?]*\b' + term + r'\b[^.,;!?]*)'
                match = re.search(pattern, context, re.IGNORECASE)
                if match:
                    return match.group(0).strip()

        return None

    def _extract_participant(self, title: str) -> str:
        """Extract participant name from video title"""
        parts = title.split()
        if parts:
            return parts[0]
        return "Unknown"

def main():
    """Test workaround detection on single video"""
    import json
    from pathlib import Path

    # Load test video
    test_file = Path(__file__).parent.parent.parent.parent / 'modules' / 'consumer-video' / 'data' / 'processed' / 'consumer02' / 'analysis.json'

    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return

    with open(test_file) as f:
        analysis = json.load(f)

    print("="*60)
    print("🔧 WORKAROUND DETECTION TEST")
    print("="*60)
    print()

    detector = WorkaroundDetector()
    workarounds = detector.detect_workarounds(analysis)

    print(f"Found {len(workarounds)} workaround instances\n")

    for i, wa in enumerate(workarounds, 1):
        print(f"### Workaround {i}")
        print(f"Confidence: {wa['confidence']:.2f}")
        print(f"Timestamp: {wa['timestamp']:.1f}s")
        print(f"Intent: {wa['intent']}")
        print(f"Barrier: {wa['barrier']}")
        print(f"Solution: {wa['solution']}")
        print(f"Verbatim: \"{wa['verbatim']}\"")
        if wa.get('product_mention'):
            print(f"Product: {wa['product_mention']}")
        print()

if __name__ == "__main__":
    main()
