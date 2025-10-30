#!/usr/bin/env python3
"""
Batch Video Processor
Process videos in batches of 25 with status tracking
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.processors import (
    TranscriptionProcessor,
    VisualAnalysisProcessor,
    AudioFeaturesProcessor,
    MetadataExtractor
)


class StatusTracker:
    """Track processing status for dashboard"""

    def __init__(self, output_dir: Path):
        self.status_file = output_dir / 'status.json'
        self.status = {
            'last_updated': datetime.now().isoformat(),
            'total_videos': 0,
            'stages': {
                'search': {'total': 0, 'complete': 0, 'status': 'pending'},
                'download': {'total': 0, 'complete': 0, 'status': 'pending'},
                'metadata': {'total': 0, 'complete': 0, 'status': 'pending'},
                'transcription': {'total': 0, 'complete': 0, 'status': 'pending'},
                'visual': {'total': 0, 'complete': 0, 'status': 'pending'},
                'audio': {'total': 0, 'complete': 0, 'status': 'pending'},
            },
            'current_batch': 0,
            'total_batches': 0,
            'errors': []
        }
        self.save()

    def update(self, **kwargs):
        """Update status fields"""
        self.status.update(kwargs)
        self.status['last_updated'] = datetime.now().isoformat()
        self.save()

    def update_stage(self, stage: str, **kwargs):
        """Update specific stage"""
        self.status['stages'][stage].update(kwargs)
        self.status['last_updated'] = datetime.now().isoformat()
        self.save()

    def save(self):
        """Save status to JSON"""
        with open(self.status_file, 'w') as f:
            json.dump(self.status, f, indent=2)


class BatchProcessor:
    """Process videos in batches"""

    def __init__(self, config_path: Path, batch_size: int = 25):
        self.config = self._load_config(config_path)
        self.batch_size = batch_size
        self.output_dir = Path(self.config['output']['base_dir'])
        self.videos_dir = self.output_dir / 'videos'

        # Load search results
        search_results_path = self.output_dir / 'search_results.json'
        with open(search_results_path) as f:
            self.search_data = json.load(f)

        self.videos = self.search_data['videos']
        self.tracker = StatusTracker(self.output_dir)

        # Initialize status
        total_batches = (len(self.videos) + batch_size - 1) // batch_size
        self.tracker.update(
            total_videos=len(self.videos),
            total_batches=total_batches
        )

        for stage in ['search', 'download', 'metadata', 'transcription', 'visual', 'audio']:
            self.tracker.update_stage(stage, total=len(self.videos))

        # Mark search complete
        self.tracker.update_stage('search', complete=len(self.videos), status='complete')

    def _load_config(self, config_path: Path) -> Dict:
        """Load YAML configuration"""
        with open(config_path) as f:
            return yaml.safe_load(f)

    def process_video(self, video_data: Dict) -> Dict:
        """Process single video"""
        video_id = video_data['id']
        video_dir = self.videos_dir / video_id
        video_path = video_dir / 'video.mp4'

        if not video_path.exists():
            return {'status': 'error', 'error': 'Video file not found'}

        processors = [
            ('metadata', MetadataExtractor(self.config, video_dir)),
            ('transcription', TranscriptionProcessor(self.config, video_dir)),
            ('visual', VisualAnalysisProcessor(self.config, video_dir)),
            ('audio', AudioFeaturesProcessor(self.config, video_dir)),
        ]

        result = {'status': 'complete', 'stages': {}}

        for stage_name, processor in processors:
            try:
                processor.run(video_path, video_data, force=False)
                result['stages'][stage_name] = 'complete'

                # Update tracker
                current = self.tracker.status['stages'][stage_name]['complete']
                self.tracker.update_stage(stage_name, complete=current + 1)

            except Exception as e:
                result['stages'][stage_name] = f'failed: {str(e)[:100]}'
                result['status'] = 'partial'

        return result

    def process_batch(self, batch_num: int, videos: List[Dict]) -> Dict:
        """Process a batch of videos"""
        print(f"\n{'='*70}")
        print(f"BATCH {batch_num + 1}/{self.tracker.status['total_batches']}")
        print(f"Processing {len(videos)} videos")
        print(f"{'='*70}\n")

        self.tracker.update(current_batch=batch_num + 1)

        for stage in ['metadata', 'transcription', 'visual', 'audio']:
            self.tracker.update_stage(stage, status='processing')

        results = []
        for i, video_data in enumerate(videos, 1):
            print(f"Video {i}/{len(videos)}: {video_data['id']}")
            result = self.process_video(video_data)
            results.append(result)

        # Mark stages as complete if all done
        for stage in ['metadata', 'transcription', 'visual', 'audio']:
            current = self.tracker.status['stages'][stage]['complete']
            total = self.tracker.status['stages'][stage]['total']
            if current >= total:
                self.tracker.update_stage(stage, status='complete')

        return {
            'batch': batch_num,
            'complete': sum(1 for r in results if r['status'] == 'complete'),
            'partial': sum(1 for r in results if r['status'] == 'partial'),
            'failed': sum(1 for r in results if r['status'] == 'error')
        }

    def run(self):
        """Process all videos in batches"""
        print(f"Processing {len(self.videos)} videos in batches of {self.batch_size}")

        # Check which videos are already downloaded
        downloaded = []
        for video_data in self.videos:
            video_dir = self.videos_dir / video_data['id']
            if (video_dir / 'video.mp4').exists():
                downloaded.append(video_data)

        self.tracker.update_stage('download', complete=len(downloaded),
                                 status='complete' if len(downloaded) == len(self.videos) else 'processing')

        # Process in batches
        for batch_num in range(0, len(self.videos), self.batch_size):
            batch = self.videos[batch_num:batch_num + self.batch_size]
            batch_result = self.process_batch(batch_num // self.batch_size, batch)

            print(f"\nBatch {batch_num // self.batch_size + 1} complete:")
            print(f"  Complete: {batch_result['complete']}")
            print(f"  Partial:  {batch_result['partial']}")
            print(f"  Failed:   {batch_result['failed']}")

        print(f"\n{'='*70}")
        print("ALL BATCHES COMPLETE")
        print(f"{'='*70}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Batch process videos')
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('config/examples/garage_organizers_tiktok.yaml'),
        help='Path to collection config YAML'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=25,
        help='Videos per batch'
    )

    args = parser.parse_args()

    if not args.config.exists():
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)

    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not set")
        print("Run with: op run --env-file=../../.env.template -- python batch_processor.py")
        sys.exit(1)

    processor = BatchProcessor(args.config, args.batch_size)
    processor.run()


if __name__ == "__main__":
    main()
