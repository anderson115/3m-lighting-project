#!/usr/bin/env python3
"""
Social Video Data Collection - Full Pipeline

Orchestrates complete data collection workflow:
1. Search videos (Apify)
2. Download videos (yt-dlp)
3. Transcribe audio (Whisper)
4. Extract visual data (FFmpeg + LLaVA)
5. Extract audio features (Librosa)

Outputs: Structured raw data ready for agentic analysis
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import argparse


class CollectionOrchestrator:
    """Orchestrate full data collection pipeline"""

    def __init__(self, config_path: Path, test_mode: bool = False):
        self.config_path = config_path
        self.test_mode = test_mode
        self.scripts_dir = Path(__file__).parent

        if not self.config_path.exists():
            raise ValueError(f"Config file not found: {config_path}")

        print("="*60)
        print("Social Video Data Collection Pipeline")
        print("="*60)
        print(f"Config: {config_path}")
        print(f"Mode: {'TEST (10 videos max)' if test_mode else 'FULL COLLECTION'}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

    def run_step(self, step_num: int, script_name: str, description: str, args: list = None) -> bool:
        """
        Run single pipeline step

        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"STEP {step_num}: {description}")
        print(f"{'='*60}")

        script_path = self.scripts_dir / script_name
        cmd = ['python', str(script_path)]

        if args:
            cmd.extend(args)

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=False  # Show output in real-time
            )

            print(f"\n✅ Step {step_num} complete: {description}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"\n❌ Step {step_num} failed: {description}")
            print(f"Error code: {e.returncode}")
            return False

    def run_pipeline(self) -> bool:
        """
        Run complete pipeline

        Returns:
            True if all steps successful
        """
        steps = [
            (1, "01_search_videos.py", "Search & Collect Metadata", [
                '--config', str(self.config_path)
            ]),
            (2, "02_download_videos.py", "Download Videos", []),
            (3, "03_transcribe.py", "Transcribe Audio (Whisper)", []),
            (4, "04_extract_visuals.py", "Extract Visual Data (LLaVA)", [
                '--frame-interval', '3'
            ]),
            (5, "05_audio_features.py", "Extract Audio Features (Librosa)", []),
        ]

        for step_num, script, description, args in steps:
            success = self.run_step(step_num, script, description, args)

            if not success:
                print(f"\n❌ Pipeline failed at step {step_num}")
                return False

        return True

    def print_summary(self, success: bool):
        """Print final summary"""
        print("\n" + "="*60)
        if success:
            print("✅ DATA COLLECTION COMPLETE")
        else:
            print("❌ DATA COLLECTION FAILED")
        print("="*60)

        if success:
            print("\nRaw data collected successfully!")
            print("\nData Location:")
            print(f"  data/processed/{self.config_path.stem}/")
            print("\nNext Steps:")
            print("  1. Review data quality")
            print("  2. Feed to analysis module for insight extraction")
            print("  3. Generate JTBD, pain points, product ideas reports")

        print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Run full social video data collection pipeline'
    )
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('config/examples/garage_organizers_tiktok.yaml'),
        help='Path to collection config YAML'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: collect only 10 videos'
    )

    args = parser.parse_args()

    # Run pipeline
    orchestrator = CollectionOrchestrator(args.config, args.test)
    success = orchestrator.run_pipeline()
    orchestrator.print_summary(success)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
