#!/usr/bin/env python3
"""
Step 5: Extract Audio Features

Extracts prosodic features (pitch, energy, pauses) using Librosa.
NO emotion classification - just raw acoustic measurements.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import librosa


class AudioFeatureExtractor:
    """Extract prosodic features from audio"""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.videos_dir = data_dir / 'videos'

        if not self.videos_dir.exists():
            raise ValueError(f"Videos directory not found: {self.videos_dir}")

        print("Audio Feature Extraction")
        print("  Features: pitch, energy, speech rate, pauses")
        print("  Mode: Raw measurements only (no interpretation)\n")

    def extract_audio(self, video_path: Path, audio_path: Path) -> bool:
        """Extract audio from video"""
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            '-y',
            str(audio_path)
        ]

        try:
            subprocess.run(cmd, capture_output=True, timeout=60, check=True)
            return audio_path.exists()
        except:
            return False

    def extract_features_for_segment(self, audio: np.ndarray, sr: int, segment: Dict) -> Dict:
        """
        Extract prosodic features for single transcript segment

        Returns raw measurements only (no classification)
        """
        # Get segment audio
        start_sample = int(segment['start'] * sr)
        end_sample = int(segment['end'] * sr)
        segment_audio = audio[start_sample:end_sample]

        if len(segment_audio) < sr * 0.1:  # Too short
            return self._get_default_features()

        # Pitch analysis
        try:
            pitches, magnitudes = librosa.piptrack(
                y=segment_audio,
                sr=sr,
                fmin=50,
                fmax=400
            )

            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)

            pitch_mean = float(np.mean(pitch_values)) if pitch_values else 0
            pitch_std = float(np.std(pitch_values)) if pitch_values else 0

        except:
            pitch_mean = 0
            pitch_std = 0

        # Energy
        rms = librosa.feature.rms(y=segment_audio)
        energy = float(np.mean(rms))

        # Speech rate (words per second)
        words = segment['text'].split()
        duration = segment['end'] - segment['start']
        speech_rate = len(words) / duration if duration > 0 else 0

        # Spectral features
        spectral_centroid = librosa.feature.spectral_centroid(y=segment_audio, sr=sr)
        spectral_mean = float(np.mean(spectral_centroid))

        # Zero-crossing rate
        zcr = librosa.feature.zero_crossing_rate(segment_audio)
        zcr_mean = float(np.mean(zcr))

        return {
            'pitch_mean': round(pitch_mean, 2),
            'pitch_std': round(pitch_std, 2),
            'energy': round(energy, 4),
            'speech_rate': round(speech_rate, 2),
            'spectral_centroid': round(spectral_mean, 2),
            'zero_crossing_rate': round(zcr_mean, 4)
        }

    def _get_default_features(self) -> Dict:
        """Default features for invalid segments"""
        return {
            'pitch_mean': 0,
            'pitch_std': 0,
            'energy': 0,
            'speech_rate': 0,
            'spectral_centroid': 0,
            'zero_crossing_rate': 0
        }

    def process_video(self, video_dir: Path) -> Optional[Dict]:
        """
        Extract audio features for single video

        Returns:
            Audio features dict, or None if failed
        """
        video_id = video_dir.name
        video_file = video_dir / 'video.mp4'
        transcript_file = video_dir / 'transcript.json'
        features_file = video_dir / 'audio_features.json'

        # Check if already processed
        if features_file.exists():
            print(f"  Skipping (already processed): {video_id}")
            return None

        if not video_file.exists():
            print(f"  Error: Video file not found: {video_id}")
            return None

        if not transcript_file.exists():
            print(f"  Error: Transcript not found: {video_id}")
            return None

        print(f"  Processing: {video_id}")

        # Load transcript
        with open(transcript_file) as f:
            transcript = json.load(f)
            segments = transcript.get('segments', [])

        if not segments:
            print(f"    ❌ No transcript segments")
            return None

        # Extract audio
        audio_file = video_dir / 'audio.wav'
        if not audio_file.exists():
            print(f"    Extracting audio...")
            if not self.extract_audio(video_file, audio_file):
                print(f"    ❌ Audio extraction failed")
                return None

        # Load audio
        print(f"    Analyzing {len(segments)} segments...")
        try:
            y, sr = librosa.load(str(audio_file), sr=16000)
        except Exception as e:
            print(f"    ❌ Failed to load audio: {str(e)[:100]}")
            return None

        # Extract features for each segment
        segment_features = []

        for i, segment in enumerate(segments):
            features = self.extract_features_for_segment(y, sr, segment)

            segment_data = {
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'],
                'features': features
            }

            segment_features.append(segment_data)

        # Save features
        audio_features = {
            'video_id': video_id,
            'total_segments': len(segments),
            'segments': segment_features,
            'processed_at': datetime.now().isoformat()
        }

        with open(features_file, 'w') as f:
            json.dump(audio_features, f, indent=2)

        print(f"    ✅ Extracted features for {len(segment_features)} segments")

        # Cleanup audio file
        audio_file.unlink()

        return audio_features

    def process_all(self) -> Dict:
        """
        Process all videos

        Returns:
            Summary dict
        """
        print("="*60)
        print("Extracting Audio Features")
        print("="*60)

        video_dirs = sorted([d for d in self.videos_dir.iterdir() if d.is_dir()])
        print(f"Found {len(video_dirs)} videos\n")

        success_count = 0
        skip_count = 0
        fail_count = 0

        for i, video_dir in enumerate(video_dirs, 1):
            print(f"\n[{i}/{len(video_dirs)}]")

            # Check if already processed
            features_file = video_dir / 'audio_features.json'
            if features_file.exists():
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

        summary_file = self.data_dir / 'audio_features_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print("\n" + "="*60)
        print("Audio Feature Extraction Complete")
        print(f"  Processed: {success_count}")
        print(f"  Skipped: {skip_count}")
        print(f"  Failed: {fail_count}")
        print("="*60)

        return summary


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Extract audio features from videos')
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

        args.data_dir = max(possible_dirs, key=lambda p: p.stat().st_mtime)
        print(f"Using data directory: {args.data_dir}\n")

    # Process
    extractor = AudioFeatureExtractor(args.data_dir)
    summary = extractor.process_all()

    if summary['processed'] == 0 and summary['skipped'] == 0:
        print("\nWarning: No videos processed!")
        sys.exit(1)

    print(f"\nData collection complete! All raw data saved to: {args.data_dir}")
    print("\nNext: Feed data to analysis module for insight extraction")


if __name__ == "__main__":
    main()
