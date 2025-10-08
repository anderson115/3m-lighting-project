"""
Perception Pipeline Module
Whisper transcription + LLaVA frame analysis
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import json


class WhisperTranscriber:
    """Audio transcription using Whisper"""

    def __init__(self, model_name: str = 'tiny'):
        """
        Initialize Whisper transcriber

        Args:
            model_name: Whisper model (tiny, base, small, medium, large, large-v3)
        """
        self.model_name = model_name

    def transcribe(
        self,
        audio_path: Path,
        output_format: str = 'json'
    ) -> Dict:
        """
        Transcribe audio file using Whisper

        Args:
            audio_path: Path to WAV audio file
            output_format: Output format (json, txt, vtt, srt)

        Returns:
            Dictionary with transcription data
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        output_dir = audio_path.parent / 'transcripts'
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / f"{audio_path.stem}.json"

        try:
            # Run Whisper command
            cmd = [
                'whisper',
                str(audio_path),
                '--model', self.model_name,
                '--output_format', output_format,
                '--output_dir', str(output_dir),
                '--language', 'en'
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            # Load JSON result
            with open(output_file, 'r') as f:
                transcript_data = json.load(f)

            return {
                'text': transcript_data['text'],
                'segments': transcript_data.get('segments', []),
                'language': transcript_data.get('language', 'en'),
                'duration': transcript_data.get('duration', 0),
                'output_file': str(output_file)
            }

        except subprocess.CalledProcessError as e:
            raise Exception(f"Whisper error: {e.stderr}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON parsing error: {e}")


# Checkpoint test function
def test_whisper_transcription(audio_path: str):
    """Test Whisper transcription (CHECKPOINT 6)"""
    print(f"\n🎤 CHECKPOINT 6: Testing Whisper transcription...")
    print(f"Audio: {Path(audio_path).name}")
    print(f"Model: tiny (fast test)")

    transcriber = WhisperTranscriber(model_name='tiny')
    result = transcriber.transcribe(Path(audio_path))

    print(f"\n✅ Transcription complete:")
    print(f"   Text length: {len(result['text'])} characters")
    print(f"   Segments: {len(result['segments'])}")
    print(f"   Duration: {result['duration']:.1f}s")
    print(f"   Output: {result['output_file']}")
    print(f"\n📝 First 200 chars:")
    print(f"   {result['text'][:200]}...")

    return result


class LLaVAAnalyzer:
    """Visual frame analysis using LLaVA"""

    def __init__(self, model_name: str = 'llava:7b'):
        """
        Initialize LLaVA analyzer

        Args:
            model_name: LLaVA model via Ollama (llava:7b, llava:13b, llava:34b)
        """
        self.model_name = model_name

    def extract_frames_intelligent(
        self,
        video_path: Path,
        transcript_data: Optional[Dict] = None,
        scene_threshold: float = 0.4,
        min_frames: int = 10,
        max_frames: int = 50,
        output_dir: Optional[Path] = None
    ) -> List[Dict]:
        """
        Intelligent frame extraction using scene changes and transcript correlation

        Args:
            video_path: Path to video file
            transcript_data: Whisper transcript with segments/timestamps
            scene_threshold: Scene change detection sensitivity (0.3-0.5)
            min_frames: Minimum frames to extract
            max_frames: Maximum frames to extract
            output_dir: Directory to save frames

        Returns:
            List of dicts with frame path, timestamp, reason, transcript_segment
        """
        video_path = Path(video_path)
        if output_dir is None:
            output_dir = video_path.parent / 'frames' / video_path.stem

        output_dir.mkdir(parents=True, exist_ok=True)

        # Step 1: Scene change detection with ffmpeg
        scene_file = output_dir / 'scenes.txt'
        scene_cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', f'select=gt(scene\\,{scene_threshold}),showinfo',
            '-f', 'null',
            '-'
        ]

        result = subprocess.run(scene_cmd, capture_output=True, text=True)

        # Parse scene timestamps from stderr
        scene_timestamps = []
        for line in result.stderr.split('\n'):
            if 'pts_time:' in line:
                try:
                    timestamp = float(line.split('pts_time:')[1].split()[0])
                    scene_timestamps.append(timestamp)
                except (IndexError, ValueError):
                    continue

        # Step 2: Get video duration
        duration_cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(video_path)
        ]
        result = subprocess.run(duration_cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())

        # Step 3: Identify keyword-rich segments from transcript
        keyword_timestamps = []
        if transcript_data and 'segments' in transcript_data:
            keywords = [
                'flickering', 'flicker', 'dimmer', 'bulb', 'light', 'switch',
                'fixture', 'wire', 'wiring', 'electrical', 'problem', 'issue',
                'fix', 'repair', 'install', 'replace', 'show', 'showing',
                'here', 'this', 'see', 'look', 'demonstration'
            ]

            for segment in transcript_data['segments']:
                text_lower = segment['text'].lower()
                if any(kw in text_lower for kw in keywords):
                    keyword_timestamps.append({
                        'time': segment['start'],
                        'text': segment['text'],
                        'keywords': [kw for kw in keywords if kw in text_lower]
                    })

        # Step 4: Combine and prioritize timestamps
        frame_candidates = []

        # Add scene changes
        for ts in scene_timestamps[:max_frames//2]:  # Limit scene changes
            frame_candidates.append({
                'timestamp': ts,
                'reason': 'scene_change',
                'priority': 2
            })

        # Add keyword moments
        for kw_data in keyword_timestamps:
            frame_candidates.append({
                'timestamp': kw_data['time'],
                'reason': f"keyword: {', '.join(kw_data['keywords'][:3])}",
                'priority': 3,
                'transcript': kw_data['text']
            })

        # Add evenly spaced fallback frames
        interval = duration / (min_frames + 1)
        for i in range(1, min_frames + 1):
            frame_candidates.append({
                'timestamp': i * interval,
                'reason': 'even_spacing',
                'priority': 1
            })

        # Step 5: Deduplicate (keep frames at least 2s apart)
        frame_candidates.sort(key=lambda x: (x['priority'], x['timestamp']), reverse=True)
        selected_frames = []

        for candidate in frame_candidates:
            if len(selected_frames) >= max_frames:
                break

            # Check if too close to existing frame
            too_close = any(abs(candidate['timestamp'] - f['timestamp']) < 2.0
                          for f in selected_frames)
            if not too_close and candidate['timestamp'] < duration:
                selected_frames.append(candidate)

        # Ensure minimum frames
        if len(selected_frames) < min_frames:
            for i in range(len(selected_frames), min_frames):
                ts = (i + 1) * (duration / (min_frames + 1))
                if ts < duration:
                    selected_frames.append({
                        'timestamp': ts,
                        'reason': 'minimum_coverage',
                        'priority': 1
                    })

        # Step 6: Extract frames
        selected_frames.sort(key=lambda x: x['timestamp'])
        frame_data = []

        for i, frame_info in enumerate(selected_frames, 1):
            frame_path = output_dir / f"frame_{i:03d}_{frame_info['reason'].split(':')[0].replace(' ', '_')}.jpg"

            cmd = [
                'ffmpeg',
                '-ss', str(frame_info['timestamp']),
                '-i', str(video_path),
                '-vframes', '1',
                '-q:v', '2',
                '-y',
                str(frame_path)
            ]

            subprocess.run(cmd, capture_output=True, check=True)

            frame_data.append({
                'path': frame_path,
                'timestamp': frame_info['timestamp'],
                'reason': frame_info['reason'],
                'transcript': frame_info.get('transcript', ''),
                'priority': frame_info['priority']
            })

        return frame_data

    def analyze_frame(self, frame_path: Path, prompt: str) -> str:
        """
        Analyze single frame with LLaVA

        Args:
            frame_path: Path to frame image
            prompt: Analysis prompt

        Returns:
            LLaVA response text
        """
        cmd = [
            'ollama',
            'run',
            self.model_name,
            prompt,
            str(frame_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()


def test_llava_analysis(video_path: str, num_frames: int = 3):
    """Test LLaVA frame analysis (CHECKPOINT 7)"""
    print(f"\n🖼️  CHECKPOINT 7: Testing LLaVA frame analysis...")
    print(f"Video: {Path(video_path).name}")
    print(f"Frames to extract: {num_frames}")

    analyzer = LLaVAAnalyzer(model_name='llava:latest')

    # Extract frames
    print(f"\n📸 Extracting frames...")
    frames = analyzer.extract_frames(Path(video_path), num_frames=num_frames)
    print(f"✅ Extracted {len(frames)} frames")

    # Analyze first frame
    print(f"\n🔍 Analyzing frame 1...")
    prompt = "Describe what you see in this image related to lighting or home electrical issues. Be specific about any visible problems, products, or solutions shown."
    analysis = analyzer.analyze_frame(frames[0], prompt)

    print(f"✅ Analysis complete:")
    print(f"   Frame: {frames[0].name}")
    print(f"   Response length: {len(analysis)} chars")
    print(f"\n📝 LLaVA output:")
    print(f"   {analysis[:300]}...")

    return frames, analysis


if __name__ == "__main__":
    # Test with first downloaded audio file
    test_audio = "/tmp/youtube_live_test/-qYonWEwPko.wav"
    test_whisper_transcription(test_audio)
