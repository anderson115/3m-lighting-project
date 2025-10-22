#!/usr/bin/env python3
"""
3M Product Tracker
Evidence-first detection of Command, Scotch, and generic adhesive mentions
"""

import re
from typing import Dict, List, Optional

class ProductTracker:
    """Track 3M product mentions and usage patterns without forcing findings"""

    def __init__(self):
        # LOOSE matching - catch variations
        self.product_patterns = {
            'command': [
                r'\bcommand\b', r'\bCommand\b', r'\bCOMMAND\b',
                r'\bcommand hook\w*\b', r'\bcommand strip\w*\b'
            ],
            'scotch': [
                r'\bscotch\b', r'\bScotch\b', r'\bSCOTCH\b',
                r'\bscotch tape\b'
            ],
            '3m': [
                r'\b3M\b', r'\bthree M\b', r'\b3-M\b', r'\bThree M\b'
            ],
            'generic_adhesive': [
                r'\badhesive\b', r'\bsticky\b', r'\btape\b',
                r'\bmounting tape\b', r'\bdouble[- ]sided\b',
                r'\bstick\w*\b.*\btape\b'
            ]
        }

        # Success indicators - require explicit statement
        self.success_indicators = [
            r'\bworked well\b', r'\bheld up\b', r'\bstill holding\b',
            r'\bno issues\b', r'\bwould use again\b', r'\brecommend\b',
            r'\bgreat\b', r'\bperfect\b', r'\blove it\b'
        ]

        # Failure indicators - must be explicit
        self.failure_indicators = [
            r'\bfell off\b', r"\bdidn't stick\b", r'\bcame loose\b',
            r'\bfailed\b', r'\bhad to redo\b', r"\bwouldn't hold\b",
            r'\btried but\b', r'\bgave up\b', r"\bwon't stay\b",
            r"\bcan't get.*to stick\b"
        ]

        # Wishlist patterns - what consumer wants that doesn't exist
        self.wishlist_patterns = [
            r'\bI wish there was\b', r'\bIt would be great if\b',
            r'\bIf only they made\b', r"\bI couldn't find anything that\b",
            r'\bI was looking for something that could\b',
            r'\bwould be nice if\b', r'\bshould make\b'
        ]

    def extract_product_mentions(self, analysis: Dict) -> List[Dict]:
        """
        Extract product mentions with usage context

        Args:
            analysis: Video analysis with transcription

        Returns:
            List of product mention instances with context
        """

        transcript = analysis.get('transcription', {})
        segments = transcript.get('segments', [])
        metadata = analysis.get('metadata', {})

        mentions = []

        for i, segment in enumerate(segments):
            text = segment.get('text', '').strip()
            if not text:
                continue

            # Check for product mentions
            detected_products = self._detect_products(text)

            if not detected_products:
                continue

            # Get extended context (±45 seconds)
            context = self._get_extended_context(segments, i, window_seconds=45)

            # Extract usage pattern
            for product_type, product_name in detected_products:
                usage = self._extract_usage_context(text, context, product_type)

                if not usage:
                    continue

                mention = {
                    'product_id': f"{metadata.get('video_id', 'unknown')}_{product_type}_{segment.get('start', 0):.0f}",
                    'product_type': product_type,
                    'product_name': product_name,
                    'mention_verbatim': text,
                    'timestamp': segment.get('start', 0),
                    'participant': self._extract_participant(metadata.get('title', '')),
                    'video_id': metadata.get('video_id', 'unknown'),
                    'application': usage.get('application'),
                    'outcome': usage.get('outcome'),
                    'outcome_confidence': usage.get('outcome_confidence'),
                    'alternative_considered': usage.get('alternative'),
                    'wish_statement': usage.get('wish'),
                    'context': context
                }

                mentions.append(mention)

        return mentions

    def _detect_products(self, text: str) -> List[tuple]:
        """Detect which products mentioned in text"""

        detected = []
        text_lower = text.lower()

        for product_type, patterns in self.product_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    detected.append((product_type, match.group(0)))
                    break

        return detected

    def _get_extended_context(self, segments: List[Dict], current_index: int, window_seconds: int = 45) -> str:
        """Get ±45 seconds context around mention"""

        if not segments or current_index < 0 or current_index >= len(segments):
            return ""

        current_time = segments[current_index].get('start', 0)

        context_segments = []
        for seg in segments:
            seg_time = seg.get('start', 0)
            if abs(seg_time - current_time) <= window_seconds:
                context_segments.append(seg.get('text', ''))

        return ' '.join(context_segments)

    def _extract_usage_context(self, text: str, context: str, product_type: str) -> Optional[Dict]:
        """
        Extract how product was used

        Returns:
            {
                'application': What they used it for,
                'outcome': 'success' | 'failure' | 'unclear',
                'outcome_confidence': 0.0-1.0,
                'alternative': What else they considered,
                'wish': What they wish existed
            }
        """

        context_lower = context.lower()

        # Extract application (what for)
        application = self._extract_application(text, context)

        # Determine outcome
        outcome, confidence = self._determine_outcome(context_lower)

        # Extract alternatives considered
        alternative = self._extract_alternative(context_lower)

        # Extract wishlist
        wish = self._extract_wish(context_lower)

        # Only return if we have meaningful information
        if not any([application, outcome != 'unclear', alternative, wish]):
            return None

        return {
            'application': application,
            'outcome': outcome,
            'outcome_confidence': confidence,
            'alternative': alternative,
            'wish': wish
        }

    def _extract_application(self, text: str, context: str) -> Optional[str]:
        """Extract what they were trying to do with the product"""

        # Look for intent markers
        intent_patterns = [
            r'(trying to|attempting to|wanted to|needed to|used.*to)\s+([^.!?]+)',
            r'(to|for)\s+([a-z]+ing\s+[^.!?]+)',
            r'(mount|hang|attach|stick|install)\s+([^.!?]+)'
        ]

        for pattern in intent_patterns:
            match = re.search(pattern, context.lower())
            if match:
                return match.group(0).strip()

        return None

    def _determine_outcome(self, context: str) -> tuple:
        """
        Determine if product usage succeeded or failed

        Returns:
            ('success' | 'failure' | 'unclear', confidence)
        """

        # Count success indicators
        success_count = 0
        for pattern in self.success_indicators:
            if re.search(pattern, context, re.IGNORECASE):
                success_count += 1

        # Count failure indicators
        failure_count = 0
        for pattern in self.failure_indicators:
            if re.search(pattern, context, re.IGNORECASE):
                failure_count += 1

        # Determine outcome
        if failure_count > success_count and failure_count > 0:
            confidence = min(0.9, 0.6 + (failure_count * 0.1))
            return ('failure', confidence)
        elif success_count > failure_count and success_count > 0:
            confidence = min(0.9, 0.6 + (success_count * 0.1))
            return ('success', confidence)
        else:
            return ('unclear', 0.3)

    def _extract_alternative(self, context: str) -> Optional[str]:
        """Extract what alternative they considered or used instead"""

        alternative_patterns = [
            r'instead\s+(I\s+)?([^.!?]+)',
            r'ended up\s+(using\s+)?([^.!?]+)',
            r'settled for\s+([^.!?]+)',
            r'(switched to|went with|chose)\s+([^.!?]+)'
        ]

        for pattern in alternative_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                return match.group(0).strip()

        return None

    def _extract_wish(self, context: str) -> Optional[str]:
        """Extract wishlist statement - what consumer wishes existed"""

        for pattern in self.wishlist_patterns:
            match = re.search(pattern + r'\s*([^.!?]+)', context, re.IGNORECASE)
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
    """Test product tracking on single video"""
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
    print("📦 PRODUCT TRACKING TEST")
    print("="*60)
    print()

    tracker = ProductTracker()
    mentions = tracker.extract_product_mentions(analysis)

    print(f"Found {len(mentions)} product mentions\n")

    for i, mention in enumerate(mentions, 1):
        print(f"### Product Mention {i}")
        print(f"Product: {mention['product_name']} ({mention['product_type']})")
        print(f"Timestamp: {mention['timestamp']:.1f}s")
        print(f"Verbatim: \"{mention['mention_verbatim']}\"")
        if mention.get('application'):
            print(f"Application: {mention['application']}")
        if mention.get('outcome') != 'unclear':
            print(f"Outcome: {mention['outcome']} (confidence: {mention['outcome_confidence']:.2f})")
        if mention.get('alternative_considered'):
            print(f"Alternative: {mention['alternative_considered']}")
        if mention.get('wish_statement'):
            print(f"Wish: {mention['wish_statement']}")
        print()

if __name__ == "__main__":
    main()
