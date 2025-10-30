#!/usr/bin/env python3
"""
Social Video Collection - Status Report Generator

Auto-detects all collections and generates standardized status reports.
Works across all category intelligence projects.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class StatusReporter:
    def __init__(self, project_root: Path = None):
        """Initialize reporter with auto-detection of project root"""
        if project_root:
            self.project_root = project_root
        else:
            # Auto-detect: look for data/processed/ directory
            current = Path.cwd()
            while current != current.parent:
                if (current / "data" / "processed").exists():
                    self.project_root = current
                    break
                current = current.parent
            else:
                raise FileNotFoundError(
                    "Could not find project root (no data/processed/ directory). "
                    "Run from within a social-video-collection project."
                )

        self.processed_dir = self.project_root / "data" / "processed"

    def find_collections(self) -> List[Path]:
        """Find all collections in data/processed/"""
        if not self.processed_dir.exists():
            return []

        collections = []
        for item in self.processed_dir.iterdir():
            if item.is_dir() and (item / "videos").exists():
                collections.append(item)

        return sorted(collections)

    def get_collection_stats(self, collection_dir: Path) -> Dict:
        """Get statistics for a single collection"""
        videos_dir = collection_dir / "videos"

        # Find all video directories
        video_dirs = [d for d in videos_dir.iterdir()
                     if d.is_dir() and d.name.isdigit()]

        total = len(video_dirs)

        # Count each stage
        counts = {
            'total': total,
            'metadata': 0,
            'transcript': 0,
            'visual': 0,
            'audio': 0,
            'complete': 0
        }

        failed_videos = []

        for video_dir in video_dirs:
            has_metadata = (video_dir / "metadata.json").exists()
            has_transcript = (video_dir / "transcript.json").exists()
            has_visual = (video_dir / "visual_analysis.json").exists()
            has_audio = (video_dir / "audio_features.json").exists()

            if has_metadata:
                counts['metadata'] += 1
            if has_transcript:
                counts['transcript'] += 1
            if has_visual:
                counts['visual'] += 1
            if has_audio:
                counts['audio'] += 1

            if all([has_metadata, has_transcript, has_visual, has_audio]):
                counts['complete'] += 1
            else:
                # Track failures for potential retry
                missing = []
                if not has_metadata:
                    missing.append('metadata')
                if not has_transcript:
                    missing.append('transcript')
                if not has_visual:
                    missing.append('visual')
                if not has_audio:
                    missing.append('audio')

                failed_videos.append((video_dir.name, missing))

        return {
            'counts': counts,
            'failed_videos': failed_videos,
            'is_complete': counts['complete'] == total,
            'completion_rate': (counts['complete'] / total * 100) if total > 0 else 0
        }

    def print_collection_status(self, collection_dir: Path, stats: Dict):
        """Print formatted status for a single collection"""
        name = collection_dir.name
        counts = stats['counts']
        total = counts['total']

        # Determine status emoji
        if stats['is_complete']:
            status_emoji = "✅"
        elif counts['complete'] > 0:
            status_emoji = "🔄"
        else:
            status_emoji = "⏳"

        print(f"\n{status_emoji} {name.upper().replace('-', ' ')}")
        print(f"   Total: {total} videos")
        print(f"   ├─ Metadata:    {counts['metadata']:3}/{total} {'✅' if counts['metadata'] == total else '🔄'}")
        print(f"   ├─ Transcripts: {counts['transcript']:3}/{total} {'✅' if counts['transcript'] == total else '🔄'}")
        print(f"   ├─ Visual:      {counts['visual']:3}/{total} {'✅' if counts['visual'] == total else '🔄'}")
        print(f"   └─ Audio:       {counts['audio']:3}/{total} {'✅' if counts['audio'] == total else '🔄'}")
        print(f"   ")
        print(f"   Fully Complete: {counts['complete']}/{total} ({stats['completion_rate']:.1f}%)")

        # Show failed videos if any
        if stats['failed_videos'] and len(stats['failed_videos']) <= 10:
            print(f"   ")
            print(f"   ⚠️  Failed/Incomplete Videos:")
            for video_id, missing in stats['failed_videos'][:10]:
                print(f"      • {video_id}: missing {', '.join(missing)}")
        elif len(stats['failed_videos']) > 10:
            print(f"   ")
            print(f"   ⚠️  {len(stats['failed_videos'])} videos incomplete/failed")

    def generate_report(self, collection_name: str = None):
        """Generate comprehensive status report"""
        collections = self.find_collections()

        if not collections:
            print("❌ No collections found in data/processed/")
            print(f"   Searched in: {self.processed_dir}")
            return

        # Filter by name if specified
        if collection_name:
            collections = [c for c in collections if collection_name in c.name]
            if not collections:
                print(f"❌ No collection matching '{collection_name}' found")
                return

        # Header
        print("\n" + "═" * 70)
        print("       SOCIAL VIDEO COLLECTION - STATUS REPORT")
        print("═" * 70)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Project:   {self.project_root.name}")

        # Process each collection
        all_stats = {}
        for collection in collections:
            try:
                stats = self.get_collection_stats(collection)
                all_stats[collection.name] = stats
                self.print_collection_status(collection, stats)
            except Exception as e:
                print(f"\n❌ Error processing {collection.name}: {e}")

        # Combined summary if multiple collections
        if len(all_stats) > 1:
            total_videos = sum(s['counts']['total'] for s in all_stats.values())
            total_complete = sum(s['counts']['complete'] for s in all_stats.values())
            overall_rate = (total_complete / total_videos * 100) if total_videos > 0 else 0

            print("\n" + "─" * 70)
            print("📊 COMBINED SUMMARY")
            print(f"   Total Collections: {len(all_stats)}")
            print(f"   Total Videos: {total_videos}")
            print(f"   Fully Processed: {total_complete}/{total_videos} ({overall_rate:.1f}%)")

        # Check if all processing complete
        all_complete = all(s['is_complete'] for s in all_stats.values())
        if all_complete:
            print("\n" + "─" * 70)
            print("🎉 ALL PROCESSING COMPLETE!")
            print("   Ready for consolidation and analysis")
            print(f"   Next step: Run consolidation script")

        print("\n" + "═" * 70)


def main():
    """Main entry point"""
    try:
        # Parse arguments
        collection_name = sys.argv[1] if len(sys.argv) > 1 else None

        # Generate report
        reporter = StatusReporter()
        reporter.generate_report(collection_name)

    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("\n💡 Make sure you're running from within a social-video-collection project")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
