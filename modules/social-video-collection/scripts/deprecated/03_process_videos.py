#!/usr/bin/env python3
"""
Step 3: Process Videos - Multimodal Data Extraction
Orchestrates all processors: transcription, visual, audio, metadata
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.processors import (
    TranscriptionProcessor,
    VisualAnalysisProcessor,
    AudioFeaturesProcessor,
    MetadataExtractor
)


class VideoProcessor:
    """Orchestrates all processing modules"""

    def __init__(self, config_path: Path):
        self.config = self._load_config(config_path)
        self.output_dir = Path(self.config['output']['base_dir'])
        self.videos_dir = self.output_dir / 'videos'

        # Load search results
        search_results_path = self.output_dir / 'search_results.json'
        with open(search_results_path) as f:
            self.search_data = json.load(f)

    def _load_config(self, config_path: Path) -> Dict:
        """Load YAML configuration"""
        with open(config_path) as f:
            return yaml.safe_load(f)

    def process_video(self, video_data: Dict, force: bool = False) -> Dict:
        """
        Process single video through all extractors

        Args:
            video_data: Video metadata from search results
            force: Force reprocessing

        Returns:
            Processing status
        """
        video_id = video_data['id']
        video_dir = self.videos_dir / video_id
        video_path = video_dir / 'video.mp4'

        print(f"\nProcessing video {video_id}")
        print(f"  URL: {video_data.get('webVideoUrl', 'N/A')}")

        # Check video exists
        if not video_path.exists():
            print(f"  ✗ Video file not found: {video_path}")
            return {'video_id': video_id, 'status': 'error', 'error': 'Video file not found'}

        status = {
            'video_id': video_id,
            'status': 'processing',
            'processors': {}
        }

        # Initialize processors
        processors = [
            MetadataExtractor(self.config, video_dir),
            TranscriptionProcessor(self.config, video_dir),
            VisualAnalysisProcessor(self.config, video_dir),
            AudioFeaturesProcessor(self.config, video_dir),
        ]

        # Run each processor
        for processor in processors:
            try:
                result = processor.run(video_path, video_data, force=force)
                status['processors'][processor.processor_name] = 'complete'

            except Exception as e:
                print(f"  ✗ {processor.processor_name}: Failed - {str(e)[:100]}")
                status['processors'][processor.processor_name] = f'failed: {str(e)[:100]}'
                # Continue with other processors even if one fails

        # Check overall status
        if all(s == 'complete' for s in status['processors'].values()):
            status['status'] = 'complete'
            print(f"  ✓ Video {video_id}: All processors complete")
        else:
            status['status'] = 'partial'
            print(f"  ⚠ Video {video_id}: Some processors failed")

        return status

    def process_all(self, force: bool = False) -> Dict:
        """
        Process all videos from search results

        Args:
            force: Force reprocessing of all videos

        Returns:
            Summary statistics
        """
        print("="*70)
        print("VIDEO PROCESSING PIPELINE")
        print("="*70)
        print(f"Videos to process: {len(self.search_data['videos'])}")
        print()

        results = []

        for video_data in self.search_data['videos']:
            try:
                result = self.process_video(video_data, force=force)
                results.append(result)

            except Exception as e:
                print(f"  ✗ Unexpected error: {str(e)[:100]}")
                results.append({
                    'video_id': video_data['id'],
                    'status': 'error',
                    'error': str(e)[:200]
                })

        # Summary statistics
        complete = sum(1 for r in results if r['status'] == 'complete')
        partial = sum(1 for r in results if r['status'] == 'partial')
        failed = sum(1 for r in results if r['status'] == 'error')

        print()
        print("="*70)
        print("PROCESSING COMPLETE")
        print("="*70)
        print(f"  Complete:       {complete}/{len(results)}")
        print(f"  Partial:        {partial}/{len(results)}")
        print(f"  Failed:         {failed}/{len(results)}")
        print()

        return {
            'total': len(results),
            'complete': complete,
            'partial': partial,
            'failed': failed,
            'results': results
        }


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Process videos with all extractors')
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('config/examples/garage_organizers_tiktok.yaml'),
        help='Path to collection config YAML'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force reprocessing of all videos'
    )

    args = parser.parse_args()

    if not args.config.exists():
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)

    # Check for required API keys
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not set")
        print("Run with: op run --env-file=../../.env.template -- python 03_process_videos.py")
        sys.exit(1)

    # Run processing
    processor = VideoProcessor(args.config)
    summary = processor.process_all(force=args.force)

    if summary['failed'] > 0:
        print(f"\nWarning: {summary['failed']} videos failed processing")
        sys.exit(1)

    print("Next step: python scripts/04_consolidate_data.py --config", args.config)


if __name__ == "__main__":
    main()
