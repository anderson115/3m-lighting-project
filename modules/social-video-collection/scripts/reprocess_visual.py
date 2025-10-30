#!/usr/bin/env python3
"""
Reprocess failed visual analysis videos
"""

import sys
import json
from pathlib import Path

# Add parent directory to path to import processors
sys.path.insert(0, str(Path(__file__).parent))

from processors.visual_analysis import VisualAnalysisProcessor


def main():
    # Read config
    config_path = Path("config/examples/garage_organizers_tiktok.yaml")
    import yaml
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Read failed videos list
    failed_videos_file = Path("/tmp/failed_videos.txt")
    with open(failed_videos_file) as f:
        failed_video_ids = [line.strip() for line in f if line.strip()]

    print(f"Reprocessing {len(failed_video_ids)} videos with failed visual analysis\n")

    videos_dir = Path(config['output']['base_dir']) / 'videos'

    success_count = 0
    failed_count = 0

    for i, video_id in enumerate(failed_video_ids, 1):
        video_dir = videos_dir / video_id
        video_path = video_dir / 'video.mp4'

        if not video_path.exists():
            print(f"{i}/{len(failed_video_ids)} - {video_id}: Video file not found, skipping")
            failed_count += 1
            continue

        print(f"{i}/{len(failed_video_ids)} - {video_id}: Processing...", end=" ")

        try:
            # Create processor
            processor = VisualAnalysisProcessor(config, video_dir)

            # Load metadata
            metadata_path = video_dir / 'metadata.json'
            metadata = {}
            if metadata_path.exists():
                with open(metadata_path) as f:
                    metadata = json.load(f)

            # Process video (force=True to overwrite)
            result = processor.run(video_path, metadata, force=True)

            print("✓ Success")
            success_count += 1

        except Exception as e:
            print(f"✗ Failed: {str(e)[:100]}")
            failed_count += 1

    print(f"\n" + "="*60)
    print(f"Reprocessing complete:")
    print(f"  Success: {success_count}/{len(failed_video_ids)}")
    print(f"  Failed:  {failed_count}/{len(failed_video_ids)}")
    print(f"="*60)


if __name__ == '__main__':
    main()
