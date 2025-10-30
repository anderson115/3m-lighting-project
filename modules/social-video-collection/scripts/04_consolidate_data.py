#!/usr/bin/env python3
"""
Step 4: Consolidate Data
Merge all extracted data sources into unified output
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class DataConsolidator:
    """Consolidate all processor outputs into unified format"""

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

    def load_processor_output(self, video_dir: Path, filename: str) -> Dict:
        """Load processor output JSON, return empty dict if not found"""
        output_path = video_dir / filename
        if output_path.exists():
            with open(output_path) as f:
                return json.load(f)
        return {}

    def consolidate_video(self, video_data: Dict) -> Dict:
        """Consolidate all data for single video"""
        video_id = video_data['id']
        video_dir = self.videos_dir / video_id

        # Load all processor outputs
        metadata = self.load_processor_output(video_dir, 'metadata.json')
        transcript = self.load_processor_output(video_dir, 'transcript.json')
        visual = self.load_processor_output(video_dir, 'visual_analysis.json')
        audio = self.load_processor_output(video_dir, 'audio_features.json')

        # Check what's available
        has_transcript = bool(transcript)
        has_visual = bool(visual)
        has_audio = bool(audio)

        # Create consolidated output
        consolidated = {
            'video_id': video_id,
            'url': video_data.get('webVideoUrl', ''),
            'processing_status': {
                'metadata': bool(metadata),
                'transcript': has_transcript,
                'visual_analysis': has_visual,
                'audio_features': has_audio
            },
            'metadata': metadata,
            'transcript': transcript,
            'visual_analysis': visual,
            'audio_features': audio,
            'consolidated_at': datetime.now().isoformat()
        }

        # Save consolidated output
        output_path = video_dir / 'consolidated.json'
        with open(output_path, 'w') as f:
            json.dump(consolidated, f, indent=2)

        return consolidated

    def consolidate_all(self) -> Dict:
        """Consolidate all videos and create collection summary"""
        print("="*70)
        print("DATA CONSOLIDATION")
        print("="*70)
        print(f"Videos to consolidate: {len(self.search_data['videos'])}")
        print()

        consolidated_videos = []
        complete_count = 0

        for video_data in self.search_data['videos']:
            video_id = video_data['id']
            print(f"Consolidating {video_id}...")

            consolidated = self.consolidate_video(video_data)
            consolidated_videos.append(consolidated)

            # Check if fully processed
            if all(consolidated['processing_status'].values()):
                complete_count += 1

        # Create collection-level summary
        collection_summary = {
            'collection_metadata': self.search_data['metadata'],
            'total_videos': len(consolidated_videos),
            'fully_processed': complete_count,
            'videos': consolidated_videos,
            'consolidated_at': datetime.now().isoformat()
        }

        # Save collection summary
        summary_path = self.output_dir / 'collection_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(collection_summary, f, indent=2)

        print()
        print("="*70)
        print("CONSOLIDATION COMPLETE")
        print("="*70)
        print(f"  Total videos:       {len(consolidated_videos)}")
        print(f"  Fully processed:    {complete_count}/{len(consolidated_videos)}")
        print(f"  Output saved to:    {summary_path}")
        print()

        return collection_summary


def main():
    """Main entry point"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Consolidate all extracted data')
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('config/examples/garage_organizers_tiktok.yaml'),
        help='Path to collection config YAML'
    )

    args = parser.parse_args()

    if not args.config.exists():
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)

    # Run consolidation
    consolidator = DataConsolidator(args.config)
    summary = consolidator.consolidate_all()

    print("Data collection pipeline complete!")
    print(f"Fully processed: {summary['fully_processed']}/{summary['total_videos']} videos")


if __name__ == "__main__":
    main()
