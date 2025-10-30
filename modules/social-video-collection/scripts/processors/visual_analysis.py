#!/usr/bin/env python3
"""
Visual Analysis Processor
Uses GPT-4 Vision for keyframe analysis and object detection
"""

import os
import base64
from pathlib import Path
from typing import Dict, List
from openai import OpenAI

from .base_processor import BaseProcessor


class VisualAnalysisProcessor(BaseProcessor):
    """Analyze video frames using GPT-4 Vision"""

    @property
    def output_filename(self) -> str:
        return "visual_analysis.json"

    @property
    def processor_name(self) -> str:
        return "Visual Analysis"

    def __init__(self, config: Dict, video_dir: Path):
        super().__init__(config, video_dir)

        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")

        self.client = OpenAI(api_key=api_key)
        self.model = config.get('visual_extraction', {}).get('model', 'gpt-4o')
        self.frame_interval = config.get('visual_extraction', {}).get('frame_interval', 3)

    def extract_keyframes(self, video_path: Path) -> List[Path]:
        """Extract keyframes from video at regular intervals"""
        import subprocess

        frames_dir = self.video_dir / "frames"
        frames_dir.mkdir(exist_ok=True)

        # Extract frames at regular intervals (simpler and more reliable than scene detection)
        # Extract 10 frames evenly distributed throughout the video
        subprocess.run([
            'ffmpeg', '-i', str(video_path),
            '-vf', f'fps=1/{self.frame_interval}',
            '-frames:v', '10',
            '-q:v', '2',  # High quality
            str(frames_dir / 'frame_%03d.jpg'),
            '-y'  # Overwrite existing files
        ], check=True, capture_output=True)

        # Return sorted list of frame paths
        frames = sorted(frames_dir.glob('frame_*.jpg'))
        return frames[:10]  # Limit to 10 frames max to control costs

    def encode_image(self, image_path: Path) -> str:
        """Encode image to base64 for API"""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def analyze_frame(self, frame_path: Path) -> Dict:
        """Analyze single frame with GPT-4 Vision"""
        base64_image = self.encode_image(frame_path)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this video frame and extract:
1. Objects and products visible (focus on garage/organization items)
2. Text/overlays visible (OCR)
3. Visible emotions/facial expressions
4. Actions being performed
5. Problems or failures shown

Respond in JSON format:
{
  "objects": ["item1", "item2"],
  "text_visible": "any text shown",
  "emotions": ["emotion1"],
  "actions": ["action1"],
  "problems": ["problem1"]
}"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )

        # Parse JSON response
        import json
        content = response.choices[0].message.content
        # Extract JSON from markdown code blocks if present
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()

        return json.loads(content)

    def process(self, video_path: Path, metadata: Dict) -> Dict:
        """
        Analyze video frames using GPT-4 Vision

        Returns:
            {
                'frames': [
                    {
                        'timestamp': 3.0,
                        'objects': [...],
                        'text_visible': '...',
                        'emotions': [...],
                        'actions': [...],
                        'problems': [...]
                    }
                ],
                'summary': {
                    'total_frames_analyzed': 5,
                    'objects_detected': [...],
                    'problems_identified': [...]
                }
            }
        """
        # Extract keyframes
        frames = self.extract_keyframes(video_path)

        # Analyze each frame
        frame_analyses = []
        all_objects = set()
        all_problems = set()

        for i, frame_path in enumerate(frames):
            try:
                analysis = self.analyze_frame(frame_path)
                analysis['frame_number'] = i + 1
                analysis['timestamp'] = i * self.frame_interval
                frame_analyses.append(analysis)

                # Aggregate
                all_objects.update(analysis.get('objects', []))
                all_problems.update(analysis.get('problems', []))

            except Exception as e:
                print(f"    Warning: Frame {i+1} analysis failed: {str(e)[:50]}")
                continue

        return {
            'frames': frame_analyses,
            'summary': {
                'total_frames_analyzed': len(frame_analyses),
                'objects_detected': sorted(all_objects),
                'problems_identified': sorted(all_problems)
            }
        }
