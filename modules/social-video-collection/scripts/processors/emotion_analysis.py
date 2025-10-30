#!/usr/bin/env python3
"""
Emotion Analysis Processor
Uses Claude API for high-quality, nuanced emotion detection from transcript + audio features
"""

import os
import json
from pathlib import Path
from typing import Dict
from anthropic import Anthropic

from .base_processor import BaseProcessor


class EmotionAnalysisProcessor(BaseProcessor):
    """Analyze emotions using Claude API with transcript + prosodic features"""

    @property
    def output_filename(self) -> str:
        return "emotion_analysis.json"

    @property
    def processor_name(self) -> str:
        return "Emotion Analysis"

    def __init__(self, config: Dict, video_dir: Path):
        super().__init__(config, video_dir)

        # Initialize Claude client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        self.client = Anthropic(api_key=api_key)
        self.model = config.get('emotion_analysis', {}).get('model', 'claude-sonnet-4-20250514')

    def load_transcript(self) -> Dict:
        """Load transcript from transcript.json"""
        transcript_path = self.video_dir / "transcript.json"
        if not transcript_path.exists():
            raise FileNotFoundError(f"Transcript not found: {transcript_path}")

        with open(transcript_path) as f:
            return json.load(f)

    def load_audio_features(self) -> Dict:
        """Load prosodic features from audio_features.json"""
        audio_path = self.video_dir / "audio_features.json"
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio features not found: {audio_path}")

        with open(audio_path) as f:
            return json.load(f)

    def analyze_emotion(self, transcript: Dict, audio_features: Dict) -> Dict:
        """
        Use Claude to analyze emotions from transcript + prosodic features

        Returns detailed emotion analysis with high nuance
        """
        # Extract text from transcript
        full_text = transcript.get('text', '')
        segments = transcript.get('segments', [])

        # Extract prosodic features
        prosodic = audio_features.get('prosodic_features', {})
        duration = audio_features.get('duration', 0)

        # Build analysis prompt
        prompt = f"""Analyze the emotional content of this TikTok video about garage organization problems.

VIDEO TRANSCRIPT:
{full_text}

AUDIO PROSODIC FEATURES:
- Duration: {duration:.1f} seconds
- Pitch: mean={prosodic.get('pitch', {}).get('mean', 0):.1f}Hz, std={prosodic.get('pitch', {}).get('std', 0):.1f}Hz, range={prosodic.get('pitch', {}).get('min', 0):.1f}-{prosodic.get('pitch', {}).get('max', 0):.1f}Hz
- Energy: mean={prosodic.get('energy', {}).get('mean', 0):.3f}, std={prosodic.get('energy', {}).get('std', 0):.3f}
- Tempo: {prosodic.get('tempo', 0):.1f} BPM
- Speech characteristics: ZCR={prosodic.get('speech_characteristics', {}).get('zero_crossing_rate_mean', 0):.4f}, Spectral Centroid={prosodic.get('speech_characteristics', {}).get('spectral_centroid_mean', 0):.1f}Hz

Provide a detailed emotional analysis in JSON format:

{{
  "primary_emotion": "the main emotion (frustrated/excited/overwhelmed/satisfied/proud/annoyed/stressed/relieved/etc)",
  "secondary_emotions": ["list", "of", "other", "present", "emotions"],
  "intensity": 0.0-1.0 (how intense the emotions are),
  "emotional_arc": "brief description of how emotions change throughout the video",
  "sentiment": "positive/negative/mixed/neutral",
  "tone": "casual/professional/humorous/serious/sarcastic/etc",
  "pain_points": ["specific", "problems", "or", "frustrations", "mentioned"],
  "voice_indicators": "what the pitch, energy, and tempo patterns suggest about emotional state",
  "text_indicators": "what the word choice, phrasing, and content reveal about emotions",
  "confidence": 0.0-1.0 (how confident you are in this analysis)
}}

Be highly nuanced and detailed. Consider:
- Mixed emotions (people often feel multiple things simultaneously)
- Sarcasm, humor, or exaggeration
- Cultural context of TikTok content creation
- Whether this is genuine frustration or performative/entertaining
- Emotional intensity variations throughout the video
"""

        # Call Claude API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Parse response
        response_text = response.content[0].text

        # Extract JSON from response (Claude might wrap it in markdown)
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        elif '```' in response_text:
            json_start = response_text.find('```') + 3
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()

        emotion_data = json.loads(response_text)

        # Add metadata
        emotion_data['model'] = self.model
        emotion_data['analysis_version'] = '1.0'

        return emotion_data

    def process(self, video_path: Path, metadata: Dict) -> Dict:
        """
        Analyze emotions from transcript and audio features

        Returns:
            {
                'primary_emotion': str,
                'secondary_emotions': [str],
                'intensity': float,
                'emotional_arc': str,
                'sentiment': str,
                'tone': str,
                'pain_points': [str],
                'voice_indicators': str,
                'text_indicators': str,
                'confidence': float,
                'model': str,
                'analysis_version': str
            }
        """
        # Load required data
        transcript = self.load_transcript()
        audio_features = self.load_audio_features()

        # Analyze emotions
        emotion_data = self.analyze_emotion(transcript, audio_features)

        return emotion_data
