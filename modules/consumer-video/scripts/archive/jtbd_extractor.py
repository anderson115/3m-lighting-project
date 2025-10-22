#!/usr/bin/env python3
"""
Jobs-to-Be-Done (JTBD) Extractor
Evidence-first extraction of functional, social, and emotional jobs
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class JTBDExtraction:
    """Structured JTBD finding"""
    jtbd_id: str
    categories: List[str]
    confidence: float
    verbatim: str
    timestamp: float
    participant: str
    evidence: Dict[str, str]
    video_id: str
    context: str

class JTBDExtractor:
    """Extract JTBD patterns from transcript without confirmation bias"""

    def __init__(self):
        # Semantic patterns - BROAD, not narrow keywords
        self.functional_signals = {
            'intent': [
                r'\btrying to\b', r'\battempting to\b', r'\bgoal was\b',
                r'\bwanted to\b', r'\bneeded to\b', r'\bhad to\b',
                r'\blooking to\b', r'\bplanning to\b'
            ],
            'constraint': [
                r"\bcan't\b", r"\bcouldn't\b", r"\bwon't let\b",
                r"\bnot allowed\b", r"\brestriction\b", r"\bdidn't work\b"
            ],
            'outcome': [
                r'\bso that\b', r'\bin order to\b', r'\bbecause I need\b',
                r'\bto achieve\b', r'\bto get\b', r'\bfor\b.*\bing\b'
            ]
        }

        self.social_signals = {
            'stakeholders': [
                r'\blandlord\b', r'\broommate\b', r'\bspouse\b', r'\bfamily\b',
                r'\bguests\b', r'\bwife\b', r'\bhusband\b', r'\bpartner\b',
                r'\bbuilding\b', r'\bapartment\b'
            ],
            'constraints': [
                r'\blease\b', r'\brental\b', r'\bapartment rules\b',
                r'\bbuilding codes\b', r'\brenting\b', r'\brent\b'
            ],
            'approval': [
                r'\bpermission\b', r'\ballowed\b', r'\bapproved\b',
                r'\bacceptable to\b', r'\binspects\b', r'\bdeposit\b'
            ],
            'impression': [
                r'\blooks professional\b', r'\bguests notice\b',
                r'\bembarrassed\b', r'\bproud to show\b', r'\bappearance\b'
            ]
        }

        self.emotional_signals = {
            'relief': [
                r'\bfinally\b', r'\bno more\b', r"\bdoesn't worry\b",
                r'\bpeace of mind\b', r'\brelief\b'
            ],
            'pride': [
                r'\bproud\b', r'\baccomplished\b', r'\bdid it myself\b',
                r'\bturned out great\b', r'\blove\b'
            ],
            'comfort': [
                r'\bcozy\b', r'\brelaxing\b', r'\bfeels like home\b',
                r'\bwelcoming\b', r'\bcomfortable\b'
            ],
            'stress': [
                r'\bfrustrat\w+\b', r'\banxious\b', r'\bworried\b',
                r'\bstressful\b', r'\bexhausting\b', r'\bannoying\b'
            ]
        }

        # Rejection patterns - filter out noise
        self.reject_patterns = [
            r'\bI think\b.*\bin general\b',
            r'\bpeople should\b',
            r'\bif I were\b',
            r'\bmy friend\b',
            r'\bsomeone else\b',
            r'\bhypothetically\b'
        ]

    def extract_jtbd_from_video(self, analysis: Dict) -> List[Dict]:
        """
        Extract JTBD patterns from video analysis

        Args:
            analysis: Video analysis dict with transcription and metadata

        Returns:
            List of JTBD extractions with confidence scores
        """

        transcript = analysis.get('transcription', {})
        segments = transcript.get('segments', [])
        metadata = analysis.get('metadata', {})

        extractions = []

        for segment in segments:
            text = segment.get('text', '').strip()
            if not text:
                continue

            # Get context window (this segment + neighbors)
            context = self._get_context_window(segments, segment)

            # Check if lighting-related and personal experience
            if not self._is_valid_extraction(text, context):
                continue

            # Detect JTBD categories
            categories = self._detect_categories(text, context)

            if not categories:
                continue

            # Calculate confidence
            confidence = self._calculate_confidence(text, context, categories)

            # Only keep high enough confidence
            if confidence < 0.4:
                continue

            # Extract evidence
            evidence = self._extract_evidence(text, context, categories)

            # Create extraction
            extraction = {
                'jtbd_id': f"{metadata.get('video_id', 'unknown')}_{segment.get('start', 0):.0f}",
                'categories': categories,
                'confidence': confidence,
                'verbatim': text,
                'timestamp': segment.get('start', 0),
                'participant': self._extract_participant(metadata.get('title', '')),
                'evidence': evidence,
                'video_id': metadata.get('video_id', 'unknown'),
                'context': context
            }

            extractions.append(extraction)

        return extractions

    def _get_context_window(self, segments: List[Dict], current: Dict, window_seconds: int = 30) -> str:
        """Get surrounding context for validation"""

        current_time = current.get('start', 0)

        context_segments = []
        for seg in segments:
            seg_time = seg.get('start', 0)
            if abs(seg_time - current_time) <= window_seconds:
                context_segments.append(seg.get('text', ''))

        return ' '.join(context_segments)

    def _is_valid_extraction(self, text: str, context: str) -> bool:
        """
        Validate this is worth extracting

        Reject if:
        - General opinion not about personal experience
        - Hypothetical scenario
        - About someone else
        - Off-topic (not lighting related)
        """

        text_lower = text.lower()
        context_lower = context.lower()

        # Check rejection patterns
        for pattern in self.reject_patterns:
            if re.search(pattern, text_lower):
                return False

        # Require lighting context
        lighting_terms = ['light', 'lighting', 'lamp', 'illuminat', 'bright', 'dark', 'glow']
        if not any(term in context_lower for term in lighting_terms):
            return False

        # Require first-person personal experience
        personal_indicators = ['i ', 'my ', 'me ', "i'm", "i've", "i'd"]
        if not any(indicator in text_lower for indicator in personal_indicators):
            return False

        return True

    def _detect_categories(self, text: str, context: str) -> List[str]:
        """Detect which JTBD categories present"""

        categories = []
        text_lower = text.lower()
        context_lower = context.lower()

        # Check functional signals
        functional_score = 0
        for signal_type, patterns in self.functional_signals.items():
            for pattern in patterns:
                if re.search(pattern, text_lower) or re.search(pattern, context_lower):
                    functional_score += 1
                    break

        if functional_score >= 1:
            categories.append('functional')

        # Check social signals
        social_score = 0
        for signal_type, patterns in self.social_signals.items():
            for pattern in patterns:
                if re.search(pattern, text_lower) or re.search(pattern, context_lower):
                    social_score += 1
                    break

        if social_score >= 1:
            categories.append('social')

        # Check emotional signals
        emotional_score = 0
        for signal_type, patterns in self.emotional_signals.items():
            for pattern in patterns:
                if re.search(pattern, text_lower) or re.search(pattern, context_lower):
                    emotional_score += 1
                    break

        if emotional_score >= 1:
            categories.append('emotional')

        return categories

    def _calculate_confidence(self, text: str, context: str, categories: List[str]) -> float:
        """
        Calculate confidence score

        High (0.8-1.0): Explicit language with clear intent
        Medium (0.6-0.79): Implied but clear from context
        Low (0.4-0.59): Ambiguous interpretation
        Reject (<0.4): Insufficient evidence
        """

        text_lower = text.lower()

        # Base confidence
        confidence = 0.5

        # Boost for explicit language
        explicit_markers = ['because', 'so that', 'in order to', 'needed to', 'trying to']
        if any(marker in text_lower for marker in explicit_markers):
            confidence += 0.2

        # Boost for specificity
        specific_markers = ['the', 'this', 'that', 'my', 'specific']
        if len([m for m in specific_markers if m in text_lower]) >= 2:
            confidence += 0.1

        # Boost for multiple category signals
        if len(categories) >= 2:
            confidence += 0.1

        # Penalty for vagueness
        vague_markers = ['maybe', 'probably', 'i think', 'kind of', 'sort of']
        if any(marker in text_lower for marker in vague_markers):
            confidence -= 0.2

        # Penalty for short statements (likely incomplete)
        if len(text.split()) < 8:
            confidence -= 0.1

        return max(0.0, min(1.0, confidence))

    def _extract_evidence(self, text: str, context: str, categories: List[str]) -> Dict[str, str]:
        """Extract key phrases that justify categorization"""

        evidence = {}
        text_lower = text.lower()

        if 'functional' in categories:
            # Find the clearest functional signal
            for signal_type, patterns in self.functional_signals.items():
                for pattern in patterns:
                    match = re.search(pattern, text_lower)
                    if match:
                        evidence['functional_signal'] = match.group(0)
                        break
                if 'functional_signal' in evidence:
                    break

        if 'social' in categories:
            for signal_type, patterns in self.social_signals.items():
                for pattern in patterns:
                    match = re.search(pattern, text_lower)
                    if match:
                        evidence['social_signal'] = match.group(0)
                        break
                if 'social_signal' in evidence:
                    break

        if 'emotional' in categories:
            for signal_type, patterns in self.emotional_signals.items():
                for pattern in patterns:
                    match = re.search(pattern, text_lower)
                    if match:
                        evidence['emotional_signal'] = match.group(0)
                        break
                if 'emotional_signal' in evidence:
                    break

        return evidence

    def _extract_participant(self, title: str) -> str:
        """Extract participant name from video title"""
        parts = title.split()
        if parts:
            return parts[0]
        return "Unknown"

def main():
    """Test extraction on single video"""
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
    print("🎯 JTBD EXTRACTION TEST")
    print("="*60)
    print()

    extractor = JTBDExtractor()
    extractions = extractor.extract_jtbd_from_video(analysis)

    print(f"Found {len(extractions)} JTBD instances\n")

    for i, extraction in enumerate(extractions[:5], 1):
        print(f"### JTBD {i}")
        print(f"Categories: {', '.join(extraction['categories'])}")
        print(f"Confidence: {extraction['confidence']:.2f}")
        print(f"Timestamp: {extraction['timestamp']:.1f}s")
        print(f"Verbatim: \"{extraction['verbatim']}\"")
        print(f"Evidence: {extraction['evidence']}")
        print()

if __name__ == "__main__":
    main()
