#!/usr/bin/env python3
"""
Step 4: Extract Visual Data

Extracts keyframes and generates neutral visual descriptions using LLaVA.
NO interpretation - just objective descriptions of what's visible.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

import ollama


class VisualExtractor:
    """Extract keyframes and visual descriptions"""

    def __init__(self, data_dir: Path, frame_interval: int = 3):
        self.data_dir = data_dir
        self.videos_dir = data_dir / 'videos'
        self.frame_interval = frame_interval

        if not self.videos_dir.exists():
            raise ValueError(f"Videos directory not found: {self.videos_dir}")

        # Set Ollama model path
        ollama_path = os.getenv('OLLAMA_MODELS', '/Volumes/TARS/llm-models/ollama/')
        os.environ['OLLAMA_MODELS'] = ollama_path

        print(f"Visual extraction settings:")
        print(f"  Frame interval: 1 frame every {frame_interval} seconds")
        print(f"  Ollama models: {ollama_path}\n")

    def extract_keyframes(self, video_path: Path, frames_dir: Path) -> List[Path]:
        """
        Extract keyframes using ffmpeg

        Returns:
            List of extracted frame paths
        """
        frames_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', f'fps=1/{self.frame_interval}',
            '-q:v', '2',  # High quality
            '-f', 'image2',
            str(frames_dir / 'frame_%04d.jpg')
        ]

        try:
            subprocess.run(cmd, capture_output=True, timeout=60, check=True)
            frames = sorted(frames_dir.glob('frame_*.jpg'))
            return frames
        except Exception as e:
            print(f"    ❌ Frame extraction failed: {str(e)[:100]}")
            return []

    def describe_frame(self, frame_path: Path, frame_number: int) -> Optional[Dict]:
        """
        Generate neutral visual description using LLaVA

        Prompt emphasizes objective observation, NO interpretation
        """
        prompt = """Describe what you see in this video frame objectively and factually. Focus on:
- Objects visible (products, tools, items)
- Actions being performed
- Environment/setting
- Text visible on screen

Do NOT interpret emotions, quality, or problems. Just describe what is visible."""

        try:
            response = ollama.chat(
                model='llava',
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [str(frame_path)]
                }]
            )

            description = response['message']['content'].strip()
            timestamp = (frame_number - 1) * self.frame_interval

            return {
                'frame_number': frame_number,
                'timestamp': timestamp,
                'frame_path': str(frame_path.name),
                'description': description
            }

        except Exception as e:
            print(f"      Frame {frame_number}: Error - {str(e)[:50]}")
            return None

    def process_video(self, video_dir: Path) -> Optional[Dict]:
        """
        Process single video: extract frames + descriptions

        Returns:
            Visual data dict, or None if failed
        """
        video_id = video_dir.name
        video_file = video_dir / 'video.mp4'
        visual_file = video_dir / 'frames' / 'descriptions.json'

        # Check if already processed
        if visual_file.exists():
            print(f"  Skipping (already processed): {video_id}")
            return None

        if not video_file.exists():
            print(f"  Error: Video file not found: {video_id}")
            return None

        print(f"  Processing: {video_id}")

        # Extract frames
        frames_dir = video_dir / 'frames'
        print(f"    Extracting frames...")
        frames = self.extract_keyframes(video_file, frames_dir)

        if not frames:
            print(f"    ❌ No frames extracted")
            return None

        print(f"    ✅ Extracted {len(frames)} frames")

        # Describe frames
        print(f"    Generating descriptions...")
        frame_descriptions = []

        for i, frame_path in enumerate(frames, 1):
            frame_num = int(frame_path.stem.split('_')[1])
            desc = self.describe_frame(frame_path, frame_num)
            if desc:
                frame_descriptions.append(desc)
                if i % 5 == 0:  # Progress update every 5 frames
                    print(f"      Progress: {i}/{len(frames)} frames")

        # Save descriptions
        visual_data = {
            'video_id': video_id,
            'total_frames': len(frames),
            'frame_interval': self.frame_interval,
            'descriptions': frame_descriptions,
            'processed_at': datetime.now().isoformat()
        }

        with open(visual_file, 'w') as f:
            json.dump(visual_data, f, indent=2)

        print(f"    ✅ Described {len(frame_descriptions)}/{len(frames)} frames")

        return visual_data

    def process_all(self) -> Dict:
        """
        Process all videos

        Returns:
            Summary dict
        """
        print("="*60)
        print("Extracting Visual Data")
        print("="*60)

        video_dirs = sorted([d for d in self.videos_dir.iterdir() if d.is_dir()])
        print(f"Found {len(video_dirs)} videos\n")

        success_count = 0
        skip_count = 0
        fail_count = 0

        for i, video_dir in enumerate(video_dirs, 1):
            print(f"\n[{i}/{len(video_dirs)}]")

            # Check if already processed
            visual_file = video_dir / 'frames' / 'descriptions.json'
            if visual_file.exists():
                print(f"  Skipping (already processed): {video_dir.name}")
                skip_count += 1
                continue

            # Process
            result = self.process_video(video_dir)
            if result:
                success_count += 1
            else:
                fail_count += 1

        # Summary
        summary = {
            'total_videos': len(video_dirs),
            'processed': success_count,
            'skipped': skip_count,
            'failed': fail_count,
            'completed_at': datetime.now().isoformat()
        }

        summary_file = self.data_dir / 'visual_extraction_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print("\n" + "="*60)
        print("Visual Extraction Complete")
        print(f"  Processed: {success_count}")
        print(f"  Skipped: {skip_count}")
        print(f"  Failed: {fail_count}")
        print("="*60)

        return summary


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Extract visual data from videos')
    parser.add_argument(
        '--data-dir',
        type=Path,
        help='Data directory containing videos/ folder'
    )
    parser.add_argument(
        '--frame-interval',
        type=int,
        default=3,
        help='Extract 1 frame every N seconds (default: 3)'
    )

    args = parser.parse_args()

    # Auto-detect data dir
    if not args.data_dir:
        possible_dirs = list(Path('data/processed').glob('*'))
        if not possible_dirs:
            print("Error: No data directories found")
            sys.exit(1)

        args.data_dir = max(possible_dirs, key=lambda p: p.stat().st_mtime)
        print(f"Using data directory: {args.data_dir}\n")

    # Process
    extractor = VisualExtractor(args.data_dir, args.frame_interval)
    summary = extractor.process_all()

    if summary['processed'] == 0 and summary['skipped'] == 0:
        print("\nWarning: No videos processed!")
        sys.exit(1)

    print(f"\nNext step: python scripts/05_audio_features.py")


if __name__ == "__main__":
    main()
