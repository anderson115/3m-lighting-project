#!/usr/bin/env python3
"""
Audio Features Processor
Extract prosodic features and emotion from audio
"""

import os
import numpy as np
from pathlib import Path
from typing import Dict
import subprocess

from .base_processor import BaseProcessor


class AudioFeaturesProcessor(BaseProcessor):
    """Extract audio features using Librosa and Pyannote"""

    @property
    def output_filename(self) -> str:
        return "audio_features.json"

    @property
    def processor_name(self) -> str:
        return "Audio Features"

    def __init__(self, config: Dict, video_dir: Path):
        super().__init__(config, video_dir)
        self.sample_rate = config.get('audio_features', {}).get('sample_rate', 16000)

        # Check for Hugging Face token for Pyannote
        self.hf_token = os.getenv('HF_TOKEN')

    def extract_audio_wav(self, video_path: Path) -> Path:
        """Extract audio to WAV for analysis"""
        audio_path = self.video_dir / "audio.wav"

        subprocess.run([
            'ffmpeg', '-i', str(video_path),
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', str(self.sample_rate),
            '-ac', '1',  # Mono
            '-y',
            str(audio_path)
        ], check=True, capture_output=True)

        return audio_path

    def extract_prosodic_features(self, audio_path: Path) -> Dict:
        """Extract pitch, energy, speech rate using Librosa"""
        import librosa

        # Load audio
        y, sr = librosa.load(audio_path, sr=self.sample_rate)

        # Pitch (fundamental frequency)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(float(pitch))

        # Energy (RMS)
        rms = librosa.feature.rms(y=y)[0]

        # Tempo/speech rate
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Zero crossing rate (indicator of speech vs silence)
        zcr = librosa.feature.zero_crossing_rate(y)[0]

        # Spectral centroid (brightness of sound)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

        return {
            'pitch': {
                'mean': float(np.mean(pitch_values)) if pitch_values else 0.0,
                'std': float(np.std(pitch_values)) if pitch_values else 0.0,
                'min': float(np.min(pitch_values)) if pitch_values else 0.0,
                'max': float(np.max(pitch_values)) if pitch_values else 0.0
            },
            'energy': {
                'mean': float(np.mean(rms)),
                'std': float(np.std(rms)),
                'max': float(np.max(rms))
            },
            'tempo': float(tempo),
            'speech_characteristics': {
                'zero_crossing_rate_mean': float(np.mean(zcr)),
                'spectral_centroid_mean': float(np.mean(spectral_centroid))
            }
        }

    def detect_emotion(self, audio_path: Path) -> Dict:
        """Detect emotion using Pyannote audio"""
        if not self.hf_token:
            print("    Warning: HF_TOKEN not set, skipping emotion detection")
            return {'emotions': [], 'confidence': 0.0}

        try:
            from pyannote.audio import Inference

            # Load emotion detection model
            inference = Inference(
                "pyannote/wespeaker-voxceleb-resnet34-LM",
                use_auth_token=self.hf_token
            )

            # Get embedding (can be used for emotion classification)
            embedding = inference(str(audio_path))

            # Simple heuristic: high energy + high pitch = excitement/frustration
            # Low energy = calm/sad
            # This is simplified - in production, use trained emotion classifier

            return {
                'embedding_available': True,
                'note': 'Emotion classification requires additional model'
            }

        except Exception as e:
            print(f"    Warning: Emotion detection failed: {str(e)[:50]}")
            return {'emotions': [], 'error': str(e)[:100]}

    def process(self, video_path: Path, metadata: Dict) -> Dict:
        """
        Extract audio features

        Returns:
            {
                'prosodic_features': {...},
                'emotion': {...},
                'duration': 30.5
            }
        """
        # Extract audio
        audio_path = self.extract_audio_wav(video_path)

        try:
            # Get duration
            import librosa
            duration = librosa.get_duration(path=audio_path)

            # Extract features
            prosodic = self.extract_prosodic_features(audio_path)
            emotion = self.detect_emotion(audio_path)

            return {
                'duration': float(duration),
                'prosodic_features': prosodic,
                'emotion': emotion
            }

        finally:
            # Cleanup
            if audio_path.exists():
                audio_path.unlink()
