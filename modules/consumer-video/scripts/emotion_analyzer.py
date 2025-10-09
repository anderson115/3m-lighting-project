#!/usr/bin/env python3
"""
Prosodic/Emotional Analysis for Consumer Videos
Detects: frustration, satisfaction, uncertainty, emphasis
"""

import librosa
import numpy as np
from pathlib import Path
from typing import Dict, List
import os

class EmotionAnalyzer:
    """
    Hybrid emotion analysis: local features + optional API validation
    """

    def __init__(self, tier='FREE'):
        self.tier = tier
        self.use_api = (tier == 'PRO')

    def analyze_video_emotions(self, audio_path: str, transcript_segments: List[Dict]) -> Dict:
        """
        Extract emotional timeline from video

        Args:
            audio_path: Path to extracted audio file
            transcript_segments: Whisper transcript with timestamps

        Returns:
            {
                'segments': [...],      # Per-segment emotions
                'timeline': [...],      # Emotion changes
                'key_moments': [...],   # High-impact emotional events
                'summary': {...}        # Overall emotional arc
            }
        """
        print("   😊 Analyzing emotional tone...")

        # Load audio for acoustic analysis
        y, sr = librosa.load(audio_path, sr=16000)

        emotion_segments = []
        dominant_emotions = []

        for i, segment in enumerate(transcript_segments):
            # Extract segment audio
            start_sample = int(segment['start'] * sr)
            end_sample = int(segment['end'] * sr)
            segment_audio = y[start_sample:end_sample]

            # Analyze this segment
            emotions = self.analyze_segment(
                segment_audio, sr, segment, transcript_segments, i
            )

            emotion_segments.append(emotions)

            if emotions['indicators']:
                dominant_emotions.append(emotions['indicators'][0]['emotion'])

        # Build timeline and summary
        timeline = self.build_emotion_timeline(emotion_segments)
        key_moments = self.extract_key_moments(emotion_segments)
        summary = self.summarize_emotions(emotion_segments, dominant_emotions)

        return {
            'segments': emotion_segments,
            'timeline': timeline,
            'key_moments': key_moments,
            'summary': summary,
            'analysis_tier': self.tier
        }

    def analyze_segment(self, segment_audio, sr, segment, all_segments, index):
        """Analyze single segment for emotions"""

        # Extract acoustic features
        acoustic = self.extract_acoustic_features(segment_audio, sr)

        # Extract Whisper features
        whisper = self.extract_whisper_features(segment, all_segments, index)

        # Classify emotions
        indicators = self.classify_emotions(acoustic, whisper, segment['text'])

        # API validation (PRO tier only)
        if self.use_api and indicators and indicators[0]['confidence'] < 0.7:
            api_result = self.validate_with_api(segment_audio, segment, indicators)
            if api_result:
                indicators = api_result

        return {
            'timestamp': segment['start'],
            'duration': segment['end'] - segment['start'],
            'text': segment['text'],
            'indicators': indicators,
            'acoustic_features': acoustic,
            'confidence': indicators[0]['confidence'] if indicators else 0
        }

    def extract_acoustic_features(self, audio, sr):
        """Extract prosodic features using librosa"""

        if len(audio) < sr * 0.1:  # Too short (<100ms)
            return self.get_default_features()

        # Pitch analysis
        try:
            pitches, magnitudes = librosa.piptrack(y=audio, sr=sr, fmin=50, fmax=400)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)

            pitch_mean = float(np.mean(pitch_values)) if pitch_values else 0
            pitch_variance = float(np.var(pitch_values)) if pitch_values else 0
        except:
            pitch_mean = 0
            pitch_variance = 0

        # Energy/volume
        rms = librosa.feature.rms(y=audio)
        energy = float(np.mean(rms))

        # Speaking rate (words per second)
        # Will be calculated from transcript in whisper features

        # Spectral features (voice quality)
        spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
        spectral_mean = float(np.mean(spectral_centroid))

        # Zero-crossing rate (breathiness, noise)
        zcr = librosa.feature.zero_crossing_rate(audio)
        zcr_mean = float(np.mean(zcr))

        return {
            'pitch_mean': pitch_mean,
            'pitch_variance': pitch_variance,
            'energy': energy,
            'spectral_centroid': spectral_mean,
            'zero_crossing_rate': zcr_mean
        }

    def extract_whisper_features(self, segment, all_segments, index):
        """Extract timing and confidence from Whisper"""

        # Word count for speech rate calculation
        words = segment['text'].split()
        duration = segment['end'] - segment['start']
        speech_rate = len(words) / duration if duration > 0 else 0

        # Detect pauses (gap before this segment)
        pause_before = 0
        if index > 0:
            prev_end = all_segments[index - 1]['end']
            pause_before = segment['start'] - prev_end

        # Filler word detection
        fillers = ['um', 'uh', 'like', 'you know', 'i mean', 'kind of', 'sort of']
        text_lower = segment['text'].lower()
        has_fillers = any(filler in text_lower for filler in fillers)
        filler_count = sum(1 for filler in fillers if filler in text_lower)

        # Confidence (if available from Whisper)
        confidence = segment.get('confidence', 1.0)

        return {
            'speech_rate': speech_rate,
            'pause_before': pause_before,
            'has_fillers': has_fillers,
            'filler_count': filler_count,
            'confidence': confidence,
            'word_count': len(words)
        }

    def classify_emotions(self, acoustic, whisper, text):
        """Rule-based emotion classification"""

        indicators = []

        # FRUSTRATION
        # Markers: irregular pitch + pauses + low confidence OR high energy spike
        frustration_score = 0
        frustration_evidence = []

        if acoustic['pitch_variance'] > 1000:
            frustration_score += 0.3
            frustration_evidence.append(f"Irregular pitch (var: {int(acoustic['pitch_variance'])})")

        if whisper['pause_before'] > 0.5:
            frustration_score += 0.2
            frustration_evidence.append(f"Long pause ({whisper['pause_before']:.1f}s)")

        if whisper['confidence'] < 0.8:
            frustration_score += 0.1
            frustration_evidence.append("Unclear speech")

        if acoustic['energy'] > 0.05:  # Loud
            frustration_score += 0.2
            frustration_evidence.append("High energy (emphasis/frustration)")

        # Check for frustration keywords in text
        frustration_words = ['ugh', 'damn', 'annoying', 'frustrating', 'won\'t', 'doesn\'t']
        if any(word in text.lower() for word in frustration_words):
            frustration_score += 0.3
            frustration_evidence.append("Frustration language detected")

        if frustration_score >= 0.4:
            indicators.append({
                'emotion': 'frustration',
                'confidence': min(frustration_score, 0.9),
                'evidence': frustration_evidence
            })

        # SATISFACTION / RELIEF
        satisfaction_score = 0
        satisfaction_evidence = []

        if acoustic['pitch_variance'] < 500 and acoustic['pitch_mean'] > 0:
            satisfaction_score += 0.3
            satisfaction_evidence.append("Steady, clear pitch")

        if whisper['speech_rate'] > 3.0:  # Fast, fluent
            satisfaction_score += 0.2
            satisfaction_evidence.append(f"Fluent speech ({whisper['speech_rate']:.1f} wps)")

        if whisper['confidence'] > 0.9:
            satisfaction_score += 0.2
            satisfaction_evidence.append("Confident delivery")

        if not whisper['has_fillers']:
            satisfaction_score += 0.1
            satisfaction_evidence.append("No hesitation")

        # Check for satisfaction keywords
        satisfaction_words = ['love', 'perfect', 'great', 'awesome', 'exactly', 'finally', 'works']
        if any(word in text.lower() for word in satisfaction_words):
            satisfaction_score += 0.3
            satisfaction_evidence.append("Positive language detected")

        if satisfaction_score >= 0.5:
            indicators.append({
                'emotion': 'satisfaction',
                'confidence': min(satisfaction_score, 0.9),
                'evidence': satisfaction_evidence
            })

        # UNCERTAINTY / HESITATION
        uncertainty_score = 0
        uncertainty_evidence = []

        if whisper['has_fillers']:
            uncertainty_score += 0.3 * whisper['filler_count']
            uncertainty_evidence.append(f"Filler words ({whisper['filler_count']})")

        if whisper['pause_before'] > 0.3:
            uncertainty_score += 0.2
            uncertainty_evidence.append(f"Pause before ({whisper['pause_before']:.1f}s)")

        if whisper['speech_rate'] < 2.0:  # Slow
            uncertainty_score += 0.2
            uncertainty_evidence.append(f"Slow speech ({whisper['speech_rate']:.1f} wps)")

        if acoustic['energy'] < 0.02:  # Quiet
            uncertainty_score += 0.1
            uncertainty_evidence.append("Low energy (tentative)")

        # Check for uncertainty language
        uncertainty_words = ['maybe', 'i think', 'probably', 'not sure', 'i guess']
        if any(word in text.lower() for word in uncertainty_words):
            uncertainty_score += 0.2
            uncertainty_evidence.append("Uncertain language")

        if uncertainty_score >= 0.4:
            indicators.append({
                'emotion': 'uncertainty',
                'confidence': min(uncertainty_score, 0.9),
                'evidence': uncertainty_evidence
            })

        # EMPHASIS (on key words/phrases)
        if acoustic['energy'] > 0.04 and whisper['speech_rate'] < 2.5:
            indicators.append({
                'emotion': 'emphasis',
                'confidence': 0.7,
                'evidence': ["High energy + deliberate pace"]
            })

        # Sort by confidence
        indicators.sort(key=lambda x: x['confidence'], reverse=True)

        return indicators

    def validate_with_api(self, audio_segment, segment, local_indicators):
        """Use Claude API for validation (PRO tier)"""
        # TODO: Implement API validation
        # For now, return local indicators
        return local_indicators

    def build_emotion_timeline(self, segments):
        """Build timeline of emotion changes"""
        timeline = []
        prev_emotion = None

        for seg in segments:
            if seg['indicators']:
                current_emotion = seg['indicators'][0]['emotion']

                if current_emotion != prev_emotion:
                    timeline.append({
                        'timestamp': seg['timestamp'],
                        'emotion': current_emotion,
                        'confidence': seg['indicators'][0]['confidence']
                    })
                    prev_emotion = current_emotion

        return timeline

    def extract_key_moments(self, segments):
        """Find high-impact emotional moments"""
        key_moments = []

        for seg in segments:
            if seg['indicators'] and seg['confidence'] > 0.75:
                indicator = seg['indicators'][0]

                # Key frustration or satisfaction moments
                if indicator['emotion'] in ['frustration', 'satisfaction']:
                    key_moments.append({
                        'timestamp': seg['timestamp'],
                        'emotion': indicator['emotion'],
                        'confidence': indicator['confidence'],
                        'quote': seg['text'][:100],  # First 100 chars
                        'evidence': indicator['evidence']
                    })

        # Sort by confidence, return top 10
        key_moments.sort(key=lambda x: x['confidence'], reverse=True)
        return key_moments[:10]

    def summarize_emotions(self, segments, dominant_emotions):
        """Overall emotional summary"""
        from collections import Counter

        emotion_counts = Counter(dominant_emotions)

        return {
            'dominant_emotion': emotion_counts.most_common(1)[0][0] if emotion_counts else 'neutral',
            'emotion_distribution': dict(emotion_counts),
            'total_segments_analyzed': len(segments),
            'segments_with_emotions': len([s for s in segments if s['indicators']])
        }

    def get_default_features(self):
        """Return default features for invalid audio"""
        return {
            'pitch_mean': 0,
            'pitch_variance': 0,
            'energy': 0,
            'spectral_centroid': 0,
            'zero_crossing_rate': 0
        }
