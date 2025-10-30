#!/usr/bin/env python3
"""
Step 3: Transcribe Audio

Uses Whisper large-v3 (local) to transcribe video audio with timestamps.
No interpretation - just raw transcription with segment timing.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

import torch
import whisper


class VideoTranscriber:
    """Transcribe videos using Whisper large-v3"""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.videos_dir = data_dir / 'videos'

        if not self.videos_dir.exists():
            raise ValueError(f"Videos directory not found: {self.videos_dir}")

        # Load Whisper model
        print("Loading Whisper large-v3...")
        model_path = os.getenv('WHISPER_MODEL_PATH', '/Volumes/TARS/llm-models/whisper/large-v3.pt')

        # Check device
        if torch.backends.mps.is_available():
            print("  Using Metal (MPS) acceleration")
            device = "mps"
        else:
            print("  Using CPU")
            device = "cpu"

        self.model = whisper.load_model(
            "large-v3",
            device=device,
            download_root=str(Path(model_path).parent)
        )
        print("  ✅ Whisper loaded\n")

    def extract_audio(self, video_path: Path, audio_path: Path) -> bool:
        """Extract audio from video using ffmpeg"""
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vn',  # No video
            '-acodec', 'pcm_s16le',
            '-ar', '16000',  # 16kHz
            '-ac', '1',  # Mono
            '-y',  # Overwrite
            str(audio_path)
        ]

        try:
            subprocess.run(cmd, capture_output=True, timeout=60, check=True)
            return audio_path.exists()
        except Exception as e:
            print(f"    ❌ Audio extraction failed: {str(e)[:100]}")
            return False

    def transcribe_video(self, video_dir: Path) -> Optional[Dict]:
        """
        Transcribe single video

        Returns:
            Transcript dict with segments, or None if failed
        """
        video_id = video_dir.name
        video_file = video_dir / 'video.mp4'
        transcript_file = video_dir / 'transcript.json'

        # Check if already transcribed
        if transcript_file.exists():
            print(f"  Skipping (already transcribed): {video_id}")
            return None

        if not video_file.exists():
            print(f"  Error: Video file not found: {video_id}")
            return None

        print(f"  Transcribing: {video_id}")

        # Extract audio
        audio_file = video_dir / 'audio.wav'
        if not audio_file.exists():
            print(f"    Extracting audio...")
            if not self.extract_audio(video_file, audio_file):
                return None

        # Transcribe
        print(f"    Running Whisper...")
        try:
            result = self.model.transcribe(
                str(audio_file),
                language='en',
                task='transcribe',
                verbose=False,
                word_timestamps=False
            )

            # Extract segments
            segments = []
            for seg in result['segments']:
                segments.append({
                    'start': seg['start'],
                    'end': seg['end'],
                    'text': seg['text'].strip()
                })

            transcript = {
                'video_id': video_id,
                'language': result.get('language', 'en'),
                'duration': segments[-1]['end'] if segments else 0,
                'segments': segments,
                'full_text': result['text'],
                'transcribed_at': datetime.now().isoformat()
            }

            # Save transcript
            with open(transcript_file, 'w') as f:
                json.dump(transcript, f, indent=2)

            print(f"    ✅ Transcribed: {len(segments)} segments, {len(result['text'])} chars")

            # Cleanup audio file to save space
            audio_file.unlink()

            return transcript

        except Exception as e:
            print(f"    ❌ Transcription failed: {str(e)[:100]}")
            return None

    def transcribe_all(self) -> Dict:
        """
        Transcribe all downloaded videos

        Returns:
            Summary dict
        """
        print("="*60)
        print("Transcribing Videos")
        print("="*60)

        # Find all video directories
        video_dirs = sorted([d for d in self.videos_dir.iterdir() if d.is_dir()])
        print(f"Found {len(video_dirs)} videos\n")

        success_count = 0
        skip_count = 0
        fail_count = 0

        for i, video_dir in enumerate(video_dirs, 1):
            print(f"\n[{i}/{len(video_dirs)}]")

            # Check if already transcribed
            transcript_file = video_dir / 'transcript.json'
            if transcript_file.exists():
                print(f"  Skipping (already transcribed): {video_dir.name}")
                skip_count += 1
                continue

            # Transcribe
            result = self.transcribe_video(video_dir)
            if result:
                success_count += 1
            else:
                fail_count += 1

        # Summary
        summary = {
            'total_videos': len(video_dirs),
            'transcribed': success_count,
            'skipped': skip_count,
            'failed': fail_count,
            'completed_at': datetime.now().isoformat()
        }

        summary_file = self.data_dir / 'transcription_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print("\n" + "="*60)
        print("Transcription Complete")
        print(f"  Transcribed: {success_count}")
        print(f"  Skipped: {skip_count}")
        print(f"  Failed: {fail_count}")
        print("="*60)

        return summary


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Transcribe videos with Whisper')
    parser.add_argument(
        '--data-dir',
        type=Path,
        help='Data directory containing videos/ folder'
    )

    args = parser.parse_args()

    # Auto-detect data dir
    if not args.data_dir:
        possible_dirs = list(Path('data/processed').glob('*'))
        if not possible_dirs:
            print("Error: No data directories found")
            sys.exit(1)

        # Use most recent
        args.data_dir = max(possible_dirs, key=lambda p: p.stat().st_mtime)
        print(f"Using data directory: {args.data_dir}\n")

    # Transcribe
    transcriber = VideoTranscriber(args.data_dir)
    summary = transcriber.transcribe_all()

    if summary['transcribed'] == 0 and summary['skipped'] == 0:
        print("\nWarning: No videos transcribed!")
        sys.exit(1)

    print(f"\nNext step: python scripts/04_extract_visuals.py")


if __name__ == "__main__":
    main()
