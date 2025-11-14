#!/usr/bin/env python3
"""
Multi-Modal Video Analysis Pipeline
Analyzes downloaded videos using Whisper and LLaVA vision models

Input: data/videos/{video_id}/video.mp4
Output: data/analysis/{video_id}/analysis.json
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import yaml

import torch
import whisper
import ollama

# Load environment
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import EmotionAnalyzer (local import)
from emotion_analyzer import EmotionAnalyzer
from jtbd_extractor import JTBDExtractor
from product_tracker import ProductTracker
from workaround_detector import WorkaroundDetector

# Load model configuration
with open(project_root / 'config' / 'model_paths.yaml') as f:
    config = yaml.safe_load(f)

# Environment variables for model paths
os.environ['OLLAMA_MODELS'] = config['models']['ollama']['base_path']
os.environ['XDG_CACHE_HOME'] = config['models']['whisper']['cache_dir']

# Analysis configuration
FRAME_EXTRACTION_INTERVAL = 30  # Extract keyframe every 30 seconds

class MultiModalAnalyzer:
    """Multi-modal video analysis using ML stack"""

    def __init__(self, video_dir: Path, output_dir: Path, emotion_tier='FREE'):
        self.video_dir = video_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Model instances
        self.whisper_model = None
        self.emotion_analyzer = EmotionAnalyzer(tier=emotion_tier)

        # Enhancement extractors
        self.jtbd_extractor = JTBDExtractor()
        self.product_tracker = ProductTracker()
        self.workaround_detector = WorkaroundDetector()

        print("🔧 Initializing ML models...")
        self._initialize_models()

    def _initialize_models(self):
        """Load ML models"""

        # Check MPS availability
        if torch.backends.mps.is_available():
            print(f"✅ Metal acceleration enabled (MPS)")
        else:
            print(f"⚠️  Using CPU (MPS not available)")

        # Load Whisper
        print("   Loading Whisper large-v3...")
        try:
            self.whisper_model = whisper.load_model(
                config['models']['whisper']['model_size'],
                download_root=config['models']['whisper']['cache_dir']
            )
            print("   ✅ Whisper loaded")
        except Exception as e:
            print(f"   ❌ Whisper failed: {str(e)[:100]}")

        print("✅ Model initialization complete\n")

    def extract_audio(self, video_path: Path, audio_path: Path) -> bool:
        """Extract audio from video using ffmpeg"""
        try:
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-vn',  # No video
                '-acodec', 'pcm_s16le',  # WAV format
                '-ar', '16000',  # 16kHz sample rate (Whisper requirement)
                '-ac', '1',  # Mono
                '-y',  # Overwrite
                str(audio_path)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=300
            )

            return result.returncode == 0

        except Exception as e:
            print(f"   ❌ Audio extraction failed: {str(e)[:100]}")
            return False

    def extract_keyframes(self, video_path: Path, frames_dir: Path, interval: int = 30) -> List[Path]:
        """
        Extract keyframes from video using ffmpeg

        Args:
            video_path: Path to video file
            frames_dir: Output directory for frames
            interval: Extract frame every N seconds

        Returns:
            List of frame file paths
        """
        frames_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Extract frames at interval
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-vf', f'fps=1/{interval}',  # 1 frame per interval seconds
                '-q:v', '2',  # High quality
                '-f', 'image2',
                str(frames_dir / 'frame_%04d.jpg')
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=300
            )

            if result.returncode == 0:
                frames = sorted(frames_dir.glob('frame_*.jpg'))
                return frames
            else:
                return []

        except Exception as e:
            print(f"   ❌ Frame extraction failed: {str(e)[:100]}")
            return []

    def transcribe_audio(self, audio_path: Path) -> Dict:
        """
        Transcribe audio using Whisper

        Returns:
            Dict with full_text, segments, and language
        """
        if not self.whisper_model:
            return {'error': 'Whisper model not loaded'}

        print("   🎤 Transcribing audio...")

        try:
            result = self.whisper_model.transcribe(
                str(audio_path),
                language='en',
                task='transcribe',
                verbose=False
            )

            # Extract key segments with timestamps
            segments = []
            for seg in result['segments']:
                segments.append({
                    'start': seg['start'],
                    'end': seg['end'],
                    'text': seg['text'].strip()
                })

            print(f"   ✅ Transcribed: {len(result['text'])} chars, {len(segments)} segments")

            return {
                'full_text': result['text'],
                'segments': segments,
                'language': result.get('language', 'en')
            }

        except Exception as e:
            print(f"   ❌ Transcription failed: {str(e)[:100]}")
            return {'error': str(e)}

    def analyze_emotion(self, audio_path: Path, transcript_segments: List[Dict]) -> Dict:
        """
        Emotion analysis using EmotionAnalyzer

        Args:
            audio_path: Path to audio file
            transcript_segments: Whisper transcript segments with timestamps

        Returns:
            Dict with emotion timeline, key moments, and summary
        """
        return self.emotion_analyzer.analyze_video_emotions(
            str(audio_path),
            transcript_segments
        )

    def analyze_visual_content(self, frames: List[Path]) -> List[Dict]:
        """
        Analyze video frames using LLaVA vision model via Ollama

        Returns:
            List of frame analyses with timestamps and insights
        """
        print(f"   👁️  Analyzing {len(frames)} frames with LLaVA...")

        frame_analyses = []

        # Lighting analysis prompt
        prompt = """Analyze this video frame focusing on lighting aspects:
1. What lighting problems or challenges are visible?
2. What lighting solutions or techniques are being demonstrated?
3. Are there any specific lighting products mentioned or shown?
4. What is the lighting context (room type, task, mood)?

Provide a concise analysis focusing on pain points and solutions."""

        for i, frame_path in enumerate(frames):
            try:
                # Calculate timestamp from frame number
                frame_num = int(frame_path.stem.split('_')[1])
                timestamp = (frame_num - 1) * FRAME_EXTRACTION_INTERVAL

                # Call LLaVA via Ollama Python API
                # Set OLLAMA_MODELS env before API call
                os.environ['OLLAMA_MODELS'] = config['models']['ollama']['base_path']

                response = ollama.chat(
                    model=config['models']['ollama']['vision_model'],
                    messages=[{
                        'role': 'user',
                        'content': prompt,
                        'images': [str(frame_path)]
                    }]
                )

                analysis = response['message']['content'].strip()
                frame_analyses.append({
                    'frame_number': frame_num,
                    'timestamp': timestamp,
                    'frame_path': str(frame_path),
                    'analysis': analysis
                })
                print(f"      Frame {i+1}/{len(frames)}: {len(analysis)} chars")

            except Exception as e:
                print(f"      Frame {i+1}/{len(frames)}: Error - {str(e)[:50]}")

        print(f"   ✅ Analyzed {len(frame_analyses)}/{len(frames)} frames")
        return frame_analyses

    def extract_insights(self, transcription: Dict, visual_analyses: List[Dict]) -> Dict:
        """
        Extract JTBD insights from combined analysis

        Returns:
            Dict with pain_points, solutions, and verbatim quotes
        """
        print("   💡 Extracting JTBD insights...")

        insights = {
            'pain_points': [],
            'solutions': [],
            'verbatims': [],
            'lighting_contexts': []
        }

        # Extract from transcription
        if 'full_text' in transcription:
            text = transcription['full_text'].lower()

            # Common pain point keywords
            pain_keywords = [
                'problem', 'issue', 'struggle', 'difficult', 'hard',
                'dark', 'dim', 'glare', 'shadow', 'uneven',
                'expensive', 'complicated', 'frustrating'
            ]

            # Common solution keywords
            solution_keywords = [
                'solution', 'fix', 'install', 'add', 'replace',
                'LED', 'strip light', 'dimmer', 'smart light',
                'diffuser', 'reflector', 'fixture'
            ]

            # Simple keyword extraction (would be enhanced with NLP)
            for segment in transcription.get('segments', []):
                seg_text = segment['text'].lower()

                # Check for pain points
                if any(keyword in seg_text for keyword in pain_keywords):
                    insights['pain_points'].append({
                        'timestamp': segment['start'],
                        'text': segment['text'],
                        'type': 'pain_point'
                    })

                # Check for solutions
                if any(keyword in seg_text for keyword in solution_keywords):
                    insights['solutions'].append({
                        'timestamp': segment['start'],
                        'text': segment['text'],
                        'type': 'solution'
                    })

        # Extract from visual analysis
        for frame_analysis in visual_analyses:
            analysis_text = frame_analysis['analysis'].lower()

            # Extract lighting contexts
            if 'room' in analysis_text or 'kitchen' in analysis_text or 'bedroom' in analysis_text:
                insights['lighting_contexts'].append({
                    'timestamp': frame_analysis['timestamp'],
                    'context': frame_analysis['analysis'][:200]
                })

        # Extract verbatim quotes (top pain points)
        insights['verbatims'] = [
            p['text'] for p in insights['pain_points'][:5]
        ]

        print(f"   ✅ Found: {len(insights['pain_points'])} pain points, {len(insights['solutions'])} solutions")

        return insights

    def analyze_video(self, video_id: str) -> Optional[Dict]:
        """
        Complete multi-modal analysis pipeline for single video

        Returns:
            Complete analysis dict or None if failed
        """
        print(f"\n{'='*60}")
        print(f"🎬 ANALYZING VIDEO: {video_id}")
        print(f"{'='*60}")

        video_path = self.video_dir / video_id / 'video.mp4'
        metadata_path = self.video_dir / video_id / 'metadata.json'

        if not video_path.exists():
            print(f"❌ Video not found: {video_path}")
            return None

        # Load metadata (optional for consumer videos)
        metadata = {}
        if metadata_path.exists():
            with open(metadata_path) as f:
                metadata = json.load(f)

            print(f"Title: {metadata.get('title', 'N/A')}")
            print(f"Channel: {metadata.get('channel', 'N/A')}")
            if 'duration' in metadata:
                print(f"Duration: {metadata['duration']//60}m {metadata['duration']%60}s")
        else:
            print(f"Video ID: {video_id}")
            print(f"Source: {video_path.name}")
            print("Note: Processing raw consumer video without metadata")

        # Create working directories
        work_dir = self.output_dir / video_id
        work_dir.mkdir(parents=True, exist_ok=True)

        audio_path = work_dir / 'audio.wav'
        frames_dir = work_dir / 'frames'

        # Step 1: Extract audio
        print("\n1️⃣  Extracting audio...")
        if not self.extract_audio(video_path, audio_path):
            print("❌ Audio extraction failed")
            return None
        print(f"   ✅ Audio saved: {audio_path.stat().st_size / (1024*1024):.1f} MB")

        # Step 2: Extract keyframes
        print("\n2️⃣  Extracting keyframes...")
        frames = self.extract_keyframes(video_path, frames_dir, FRAME_EXTRACTION_INTERVAL)
        if not frames:
            print("❌ Frame extraction failed")
            return None
        print(f"   ✅ Extracted {len(frames)} frames")

        # Step 3: Transcribe audio
        print("\n3️⃣  Transcribing audio (Whisper)...")
        transcription = self.transcribe_audio(audio_path)

        # Explicit cleanup: Release Whisper resources
        import gc
        gc.collect()

        # Step 4: Analyze emotion (librosa + hybrid)
        print("\n4️⃣  Analyzing emotion (librosa + hybrid)...")
        emotion = self.analyze_emotion(audio_path, transcription.get('segments', []))

        # Step 5: Analyze visual content
        print("\n5️⃣  Analyzing visual content (LLaVA)...")
        visual_analyses = self.analyze_visual_content(frames)

        # Step 6: Extract insights
        print("\n6️⃣  Extracting JTBD insights...")
        insights = self.extract_insights(transcription, visual_analyses)

        # Compile complete analysis
        analysis = {
            'metadata': {
                'video_id': video_id,
                'title': metadata.get('title', video_path.name),
                'channel': metadata.get('channel', 'Consumer Interview'),
                'duration': metadata.get('duration', 0),
                'analyzed_at': datetime.now().isoformat()
            },
            'transcription': transcription,
            'emotion_analysis': emotion,
            'visual_analysis': {
                'total_frames': len(frames),
                'analyzed_frames': len(visual_analyses),
                'frame_interval': FRAME_EXTRACTION_INTERVAL,
                'frames': visual_analyses
            },
            'insights': insights
        }

        # Enhancement layers
        print("\n7️⃣  Extracting JTBD patterns...")
        print("   💡 Analyzing jobs-to-be-done...")
        jtbd_findings = self.jtbd_extractor.extract_jtbd_from_video(analysis)
        print(f"   ✅ Found: {len(jtbd_findings)} JTBD instances")
        analysis['jtbd'] = jtbd_findings

        print("\n8️⃣  Tracking product mentions...")
        print("   📦 Detecting 3M products...")
        product_mentions = self.product_tracker.extract_product_mentions(analysis)
        print(f"   ✅ Found: {len(product_mentions)} product mentions")
        analysis['products_3m'] = product_mentions

        print("\n9️⃣  Detecting workarounds...")
        print("   🔧 Identifying compensating behaviors...")
        workarounds = self.workaround_detector.detect_workarounds(analysis)
        print(f"   ✅ Found: {len(workarounds)} workarounds")
        analysis['workarounds'] = workarounds

        # Save analysis
        analysis_path = work_dir / 'analysis.json'
        with open(analysis_path, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"\n💾 Analysis saved: {analysis_path}")
        return analysis

    def analyze_all_videos(self) -> List[Dict]:
        """
        Analyze all videos in video directory

        Returns:
            List of all analyses
        """
        # Find all videos
        video_dirs = [d for d in self.video_dir.iterdir() if d.is_dir()]

        print(f"\n🎯 Found {len(video_dirs)} videos to analyze")

        all_analyses = []

        for i, video_dir in enumerate(video_dirs, 1):
            video_id = video_dir.name

            # Skip if already analyzed
            analysis_path = self.output_dir / video_id / 'analysis.json'
            if analysis_path.exists():
                print(f"\n[{i}/{len(video_dirs)}] {video_id}: Already analyzed ✓")
                with open(analysis_path) as f:
                    all_analyses.append(json.load(f))
                continue

            print(f"\n[{i}/{len(video_dirs)}] {video_id}")
            analysis = self.analyze_video(video_id)

            if analysis:
                all_analyses.append(analysis)
            else:
                print(f"   ⚠️  Analysis failed for {video_id}")

        return all_analyses

    def generate_summary_report(self, all_analyses: List[Dict]):
        """Generate summary report across all videos"""

        summary_path = self.output_dir / 'summary_report.json'

        # Aggregate insights
        total_pain_points = 0
        total_solutions = 0
        total_verbatims = 0

        all_pain_points = []
        all_solutions = []
        all_verbatims = []

        for analysis in all_analyses:
            insights = analysis.get('insights', {})
            pain_points = insights.get('pain_points', [])
            solutions = insights.get('solutions', [])
            verbatims = insights.get('verbatims', [])

            total_pain_points += len(pain_points)
            total_solutions += len(solutions)
            total_verbatims += len(verbatims)

            all_pain_points.extend(pain_points)
            all_solutions.extend(solutions)
            all_verbatims.extend(verbatims)

        summary = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_videos_analyzed': len(all_analyses)
            },
            'aggregate_stats': {
                'total_pain_points': total_pain_points,
                'total_solutions': total_solutions,
                'total_verbatims': total_verbatims
            },
            'top_pain_points': all_pain_points[:20],  # Top 20
            'top_solutions': all_solutions[:20],
            'sample_verbatims': all_verbatims[:10]
        }

        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"\n📊 Summary report saved: {summary_path}")

        # Print summary
        print("\n" + "=" * 60)
        print("📊 ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"Videos analyzed: {len(all_analyses)}")
        print(f"Pain points found: {total_pain_points}")
        print(f"Solutions identified: {total_solutions}")
        print(f"Verbatim quotes: {total_verbatims}")


def check_dependencies():
    """Check required dependencies"""
    print("🔍 Checking dependencies...")

    dependencies = {
        'ffmpeg': ['ffmpeg', '-version'],
        'ollama': ['ollama', '--version']
    }

    all_ok = True
    for name, cmd in dependencies.items():
        try:
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                print(f"   ✅ {name}")
            else:
                print(f"   ❌ {name} not working")
                all_ok = False
        except FileNotFoundError:
            print(f"   ❌ {name} not installed")
            all_ok = False

    return all_ok


def main():
    """Main entry point"""

    # Check dependencies
    if not check_dependencies():
        print("\n❌ Missing dependencies - cannot proceed")
        sys.exit(1)

    # Paths
    video_dir = project_root / 'data' / 'videos'
    output_dir = project_root / 'data' / 'analysis'

    if not video_dir.exists():
        print(f"❌ Video directory not found: {video_dir}")
        print("   Run: python scripts/video_downloader.py")
        sys.exit(1)

    # Run analyzer
    analyzer = MultiModalAnalyzer(video_dir, output_dir)
    all_analyses = analyzer.analyze_all_videos()

    if all_analyses:
        analyzer.generate_summary_report(all_analyses)
        print("\n✅ Multi-modal analysis complete!")
        print(f"   Next: python scripts/generate_jtbd_report.py")
    else:
        print("\n⚠️  No videos analyzed")
        sys.exit(1)


if __name__ == "__main__":
    main()
