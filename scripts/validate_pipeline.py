#!/usr/bin/env python3
"""
Pipeline Validation Checkpoint
Tests the complete multimodal analysis pipeline on a 60-second video clip
before running full batch analysis.

Usage:
    python scripts/validate_pipeline.py [video_path]

Output:
    data/preflight/validation_report.json
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.multimodal_analyzer import MultiModalAnalyzer

# Validation thresholds
MIN_TRANSCRIPT_WORDS = 10
MIN_FRAMES_ANALYZED = 1  # At least 1 frame should succeed
MIN_EMOTION_SEGMENTS = 1
MIN_TRANSCRIPT_LENGTH = 50  # characters


class PipelineValidator:
    """Validates the complete multimodal analysis pipeline"""

    def __init__(self, video_path: Path):
        self.video_path = video_path
        self.test_dir = project_root / 'data' / 'validation_test'
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.results = {
            'status': 'UNKNOWN',
            'timestamp': datetime.now().isoformat(),
            'video_tested': str(video_path),
            'checks': {}
        }

    def extract_60s_clip(self) -> Path:
        """Extract first 90 seconds of video for testing (need ≥3 frames at 30s interval)"""
        print("📹 Extracting 90-second test clip...")

        clip_path = self.test_dir / 'test_clip.mp4'

        cmd = [
            'ffmpeg', '-y',
            '-i', str(self.video_path),
            '-t', '90',  # First 90 seconds (ensures 3 frames at 30s intervals)
            '-c', 'copy',  # Copy codec (fast)
            str(clip_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0 or not clip_path.exists():
            raise Exception(f"Failed to extract clip: {result.stderr}")

        print(f"   ✅ Test clip created: {clip_path.stat().st_size / 1024 / 1024:.1f} MB")
        return clip_path

    def setup_test_structure(self, clip_path: Path) -> Path:
        """Create expected directory structure for analyzer"""
        video_id = 'validation_test'
        video_dir = self.test_dir / video_id
        video_dir.mkdir(parents=True, exist_ok=True)

        # Copy clip to expected location
        dest_video = video_dir / 'video.mp4'
        shutil.copy(clip_path, dest_video)

        # Create minimal metadata
        metadata = {
            'video_id': video_id,
            'title': 'Validation Test Clip',
            'channel': 'Test',
            'duration': 90
        }

        with open(video_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)

        return video_dir

    def run_analysis(self, video_dir: Path) -> dict:
        """Run multimodal analysis on test clip"""
        print("\n🔬 Running pipeline analysis...")

        analysis_output_dir = project_root / 'data' / 'validation_analysis'
        analysis_output_dir.mkdir(parents=True, exist_ok=True)

        analyzer = MultiModalAnalyzer(
            video_dir=self.test_dir,
            output_dir=analysis_output_dir
        )

        analyses = analyzer.analyze_all_videos()

        if not analyses or len(analyses) == 0:
            raise Exception("No analysis results returned")

        return analyses[0]

    def validate_whisper(self, analysis: dict) -> dict:
        """Validate Whisper transcription output"""
        print("   🎤 Checking Whisper transcription...")

        check = {'pass': False, 'reason': ''}

        try:
            transcript = analysis.get('transcription', {})

            if not transcript:
                check['reason'] = "No transcription data found"
                return check

            full_text = transcript.get('full_text', '')
            segments = transcript.get('segments', [])

            # Check transcript length
            if len(full_text) < MIN_TRANSCRIPT_LENGTH:
                check['reason'] = f"Transcript too short: {len(full_text)} chars (min {MIN_TRANSCRIPT_LENGTH})"
                return check

            # Check word count
            word_count = len(full_text.split())
            if word_count < MIN_TRANSCRIPT_WORDS:
                check['reason'] = f"Too few words: {word_count} (min {MIN_TRANSCRIPT_WORDS})"
                return check

            # Check segments exist
            if len(segments) == 0:
                check['reason'] = "No transcript segments found"
                return check

            # Check timestamps are reasonable
            first_segment = segments[0]
            if 'start' not in first_segment or 'end' not in first_segment:
                check['reason'] = "Missing timestamps in segments"
                return check

            # All checks passed
            check['pass'] = True
            check['reason'] = f"OK: {word_count} words, {len(segments)} segments"
            check['details'] = {
                'word_count': word_count,
                'segment_count': len(segments),
                'duration': first_segment.get('end', 0)
            }

        except Exception as e:
            check['reason'] = f"Exception: {str(e)}"

        return check

    def validate_llava(self, analysis: dict) -> dict:
        """Validate LLaVA visual analysis output"""
        print("   👁️  Checking LLaVA visual analysis...")

        check = {'pass': False, 'reason': ''}

        try:
            visual_container = analysis.get('visual_analysis', {})

            if not visual_container:
                check['reason'] = "No visual analysis data found"
                return check

            # Handle both dict (new format) and list (old format)
            if isinstance(visual_container, dict):
                visual_data = visual_container.get('frames', [])
                total_frames = visual_container.get('total_frames', len(visual_data))
            else:
                visual_data = visual_container
                total_frames = len(visual_data)

            if not visual_data:
                check['reason'] = "No frames in visual analysis"
                return check

            # Count successful analyses
            successful = [v for v in visual_data if v.get('analysis') and len(v.get('analysis', '')) > 0]

            if len(successful) < MIN_FRAMES_ANALYZED:
                check['reason'] = f"Only {len(successful)}/{len(visual_data)} frames analyzed (min {MIN_FRAMES_ANALYZED})"
                return check

            # CRITICAL: For validation checkpoint, require at least 3 frames
            # This ensures LLaVA is actually processing images, not just returning empty results
            if len(successful) < 3:
                check['reason'] = f"Insufficient frames analyzed: {len(successful)}/{ len(visual_data)} (need ≥3 for validation)"
                return check

            # Check quality of analysis (not just error messages)
            sample_analysis = successful[0].get('analysis', '')

            # Check for common error patterns
            error_patterns = ['error', 'failed', 'unknown flag', 'Exception', 'status code']
            if any(pattern.lower() in sample_analysis.lower() for pattern in error_patterns):
                check['reason'] = f"Analysis contains error text: {sample_analysis[:100]}"
                return check

            # Check analysis is substantive (>100 chars for quality)
            # LLaVA should produce detailed descriptions, not brief responses
            if len(sample_analysis) < 100:
                check['reason'] = f"Analysis too brief: {len(sample_analysis)} chars (need ≥100 for quality)"
                return check

            # Calculate average description length across all successful frames
            avg_length = sum(len(v.get('analysis', '')) for v in successful) / len(successful)
            if avg_length < 100:
                check['reason'] = f"Descriptions too brief (avg {avg_length:.0f} chars, need ≥100)"
                return check

            # All checks passed
            check['pass'] = True
            check['reason'] = f"OK: {len(successful)}/{total_frames} frames analyzed (avg {avg_length:.0f} chars)"
            check['details'] = {
                'frames_total': total_frames,
                'frames_successful': len(successful),
                'sample_analysis_length': len(sample_analysis),
                'avg_analysis_length': round(avg_length, 1)
            }

        except Exception as e:
            check['reason'] = f"Exception: {str(e)}"

        return check

    def validate_hubert(self, analysis: dict) -> dict:
        """Validate HuBERT emotion detection output"""
        print("   😊 Checking HuBERT emotion analysis...")

        check = {'pass': False, 'reason': ''}

        try:
            emotion_data = analysis.get('emotion_analysis', {})

            if not emotion_data:
                check['reason'] = "No emotion analysis data found"
                return check

            # Check if model is ready (for preflight, this is acceptable)
            model_ready = emotion_data.get('model_ready', False)

            # Check for emotion scores
            if 'segments' in emotion_data or 'emotions' in emotion_data:
                # Get emotion segments (structure may vary)
                segments = emotion_data.get('segments', emotion_data.get('emotions', []))

                if len(segments) < MIN_EMOTION_SEGMENTS:
                    check['reason'] = f"Too few emotion segments: {len(segments)} (min {MIN_EMOTION_SEGMENTS})"
                    return check

                # All checks passed
                check['pass'] = True
                check['reason'] = f"OK: {len(segments)} emotion segments detected"
                check['details'] = {
                    'segment_count': len(segments)
                }
            elif model_ready and 'emotion_classes' in emotion_data:
                # Model loaded but not yet running (acceptable for preflight)
                check['pass'] = True
                check['reason'] = f"OK: Model ready, classes: {', '.join(emotion_data.get('emotion_classes', []))}"
                check['details'] = {
                    'model_ready': True,
                    'note': emotion_data.get('note', 'Emotion model loaded')
                }
            else:
                check['reason'] = "Missing emotion segments/scores and model not ready"
                return check

        except Exception as e:
            check['reason'] = f"Exception: {str(e)}"

        return check

    def validate_files(self) -> dict:
        """Validate all expected output files were created"""
        print("   📁 Checking output files...")

        check = {'pass': False, 'reason': ''}

        try:
            analysis_dir = project_root / 'data' / 'validation_analysis' / 'validation_test'

            if not analysis_dir.exists():
                check['reason'] = "Analysis output directory not found"
                return check

            expected_files = [
                'analysis.json',
                'audio.wav'
            ]

            missing = []
            zero_byte = []

            for filename in expected_files:
                filepath = analysis_dir / filename

                if not filepath.exists():
                    missing.append(filename)
                elif filepath.stat().st_size == 0:
                    zero_byte.append(filename)

            if missing:
                check['reason'] = f"Missing files: {', '.join(missing)}"
                return check

            if zero_byte:
                check['reason'] = f"Zero-byte files: {', '.join(zero_byte)}"
                return check

            # Check frames directory
            frames_dir = analysis_dir / 'frames'
            if not frames_dir.exists() or len(list(frames_dir.glob('*.jpg'))) == 0:
                check['reason'] = "No frame images found"
                return check

            # All checks passed
            check['pass'] = True
            check['reason'] = f"OK: All files created, {len(list(frames_dir.glob('*.jpg')))} frames extracted"
            check['details'] = {
                'frames_extracted': len(list(frames_dir.glob('*.jpg')))
            }

        except Exception as e:
            check['reason'] = f"Exception: {str(e)}"

        return check

    def validate_integration(self, analysis: dict) -> dict:
        """Validate data integration across components"""
        print("   🔗 Checking component integration...")

        check = {'pass': False, 'reason': ''}

        try:
            # Check that insights were extracted
            insights = analysis.get('insights', {})

            if not insights:
                check['reason'] = "No insights data found"
                return check

            # Check for JTBD components
            pain_points = insights.get('pain_points', [])
            solutions = insights.get('solutions', [])
            verbatims = insights.get('verbatims', [])

            # At least some insights should exist
            total_insights = len(pain_points) + len(solutions) + len(verbatims)

            if total_insights == 0:
                check['reason'] = "No JTBD insights extracted"
                return check

            # All checks passed
            check['pass'] = True
            check['reason'] = f"OK: {len(pain_points)} pain points, {len(solutions)} solutions, {len(verbatims)} verbatims"
            check['details'] = {
                'pain_points': len(pain_points),
                'solutions': len(solutions),
                'verbatims': len(verbatims)
            }

        except Exception as e:
            check['reason'] = f"Exception: {str(e)}"

        return check

    def run_validation(self) -> dict:
        """Run complete validation sequence"""
        print("\n" + "="*60)
        print("🔬 PIPELINE VALIDATION CHECKPOINT")
        print("="*60)

        try:
            # Step 1: Extract test clip
            clip_path = self.extract_60s_clip()

            # Step 2: Setup test structure
            video_dir = self.setup_test_structure(clip_path)

            # Step 3: Run analysis
            analysis = self.run_analysis(video_dir)

            # Step 4: Run validation checks
            print("\n🔍 Running validation checks...\n")

            self.results['checks']['whisper'] = self.validate_whisper(analysis)
            self.results['checks']['llava'] = self.validate_llava(analysis)
            self.results['checks']['hubert'] = self.validate_hubert(analysis)
            self.results['checks']['files'] = self.validate_files()
            self.results['checks']['integration'] = self.validate_integration(analysis)

            # Determine overall status
            all_passed = all(check['pass'] for check in self.results['checks'].values())

            if all_passed:
                self.results['status'] = 'PASS'
                self.results['recommendation'] = 'PROCEED'
            else:
                self.results['status'] = 'FAIL'
                self.results['recommendation'] = 'FIX_AND_RETRY'

        except Exception as e:
            self.results['status'] = 'ERROR'
            self.results['recommendation'] = 'FIX_AND_RETRY'
            self.results['error'] = str(e)
            print(f"\n❌ Validation error: {str(e)}")

        return self.results

    def save_report(self):
        """Save validation report to JSON"""
        report_path = project_root / 'data' / 'preflight' / 'validation_report.json'
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n💾 Validation report saved: {report_path}")
        return report_path

    def print_summary(self):
        """Print validation summary"""
        print("\n" + "="*60)
        print("📊 VALIDATION SUMMARY")
        print("="*60)

        status_icon = "✅" if self.results['status'] == 'PASS' else "❌"
        print(f"\n{status_icon} Overall Status: {self.results['status']}")
        print(f"📋 Recommendation: {self.results.get('recommendation', 'UNKNOWN')}")

        print("\n📋 Component Checks:")
        for component, check in self.results['checks'].items():
            icon = "✅" if check['pass'] else "❌"
            print(f"   {icon} {component.upper()}: {check['reason']}")

        if self.results.get('error'):
            print(f"\n⚠️  Error: {self.results['error']}")

        print("\n" + "="*60)


def main():
    """Main validation entry point"""

    # Default to first preflight video
    if len(sys.argv) > 1:
        video_path = Path(sys.argv[1])
    else:
        video_path = project_root / 'data' / 'preflight' / 'beginner' / '6YlrdMaM0dw.mp4'

    if not video_path.exists():
        print(f"❌ Video not found: {video_path}")
        sys.exit(1)

    # Run validation
    validator = PipelineValidator(video_path)
    results = validator.run_validation()
    validator.save_report()
    validator.print_summary()

    # Exit with appropriate code
    sys.exit(0 if results['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
