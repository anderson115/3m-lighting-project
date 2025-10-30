#!/usr/bin/env python3
"""
Transcription Processor
Uses OpenAI Whisper API for accurate audio transcription
"""

import os
from pathlib import Path
from typing import Dict
from openai import OpenAI

from .base_processor import BaseProcessor


class TranscriptionProcessor(BaseProcessor):
    """Transcribe audio using OpenAI Whisper API"""

    @property
    def output_filename(self) -> str:
        return "transcript.json"

    @property
    def processor_name(self) -> str:
        return "Audio Transcription"

    def __init__(self, config: Dict, video_dir: Path):
        super().__init__(config, video_dir)

        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")

        self.client = OpenAI(api_key=api_key)
        self.model = config.get('transcription', {}).get('model', 'whisper-1')

    def extract_audio(self, video_path: Path) -> Path:
        """Extract audio from video to temporary file"""
        import subprocess

        audio_path = self.video_dir / "audio.mp3"

        # Use FFmpeg to extract audio
        subprocess.run([
            'ffmpeg', '-i', str(video_path),
            '-vn',  # No video
            '-acodec', 'libmp3lame',
            '-q:a', '2',  # High quality
            '-y',  # Overwrite
            str(audio_path)
        ], check=True, capture_output=True)

        return audio_path

    def process(self, video_path: Path, metadata: Dict) -> Dict:
        """
        Transcribe video audio using Whisper API

        Returns:
            {
                'text': 'full transcript',
                'segments': [{'start': 0.0, 'end': 1.5, 'text': '...'}],
                'language': 'en',
                'duration': 30.5
            }
        """
        # Extract audio to temporary file
        audio_path = self.extract_audio(video_path)

        try:
            # Call Whisper API with verbose output for timestamps
            with open(audio_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )

            # Convert response to dict
            result = {
                'text': transcript.text,
                'language': transcript.language,
                'duration': transcript.duration,
                'segments': [
                    {
                        'start': seg.start,
                        'end': seg.end,
                        'text': seg.text
                    }
                    for seg in transcript.segments
                ]
            }

            return result

        finally:
            # Cleanup temporary audio file
            if audio_path.exists():
                audio_path.unlink()
