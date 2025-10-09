#!/usr/bin/env python3
"""
Cross-Video Pattern Clusterer
Aggregate JTBD patterns across videos to identify frequency
"""

from typing import Dict, List
from collections import defaultdict

class PatternClusterer:
    """Cluster similar JTBD patterns across multiple videos"""

    def __init__(self):
        # Keyword groups for clustering
        self.keyword_groups = {
            'electrical_knowledge': ['electrician', 'wiring', 'electrical', 'power', 'rewire', 'hardwire'],
            'adhesive_performance': ['tape', 'stick', 'adhesive', 'hold', 'fall', 'fell off', 'came loose'],
            'heat_resistance': ['heat', 'hot', 'arizona', 'temperature', 'warm', 'climate'],
            'installation_difficulty': ['difficult', 'challenging', 'hard to', 'tricky', 'complicated'],
            'rental_constraints': ['landlord', 'lease', 'rental', 'apartment', 'deposit', 'permission'],
            'tool_knowledge': ['don\'t know how', 'not handy', 'never done', 'first time'],
        }

    def cluster_jtbd(self, all_jtbd: List[Dict]) -> Dict:
        """
        Group similar JTBD by keyword matching

        Args:
            all_jtbd: Combined list of JTBD from all videos

        Returns:
            Cluster summary with counts, frequencies, and examples
        """

        if not all_jtbd:
            return {}

        clusters = defaultdict(list)

        # Assign each JTBD to a cluster
        for jtbd in all_jtbd:
            verbatim = jtbd.get('verbatim', '').lower()
            assigned = False

            for cluster_name, keywords in self.keyword_groups.items():
                if any(kw in verbatim for kw in keywords):
                    clusters[cluster_name].append(jtbd)
                    assigned = True
                    break

            # Unclustered (doesn't match any keyword group)
            if not assigned:
                clusters['other'].append(jtbd)

        # Generate summary (only meaningful clusters with >=2 instances)
        cluster_summary = {}

        for name, items in clusters.items():
            if len(items) >= 2:  # Minimum 2 instances for meaningful cluster
                # Get unique video IDs
                video_ids = list(set(item.get('video_id', 'unknown') for item in items))

                cluster_summary[name] = {
                    'count': len(items),
                    'frequency_percent': round((len(items) / len(all_jtbd)) * 100, 1),
                    'video_count': len(video_ids),
                    'video_ids': sorted(video_ids),
                    'sample_verbatim': items[0].get('verbatim', ''),
                    'all_instances': [
                        {
                            'verbatim': item.get('verbatim', ''),
                            'video_id': item.get('video_id', ''),
                            'timestamp': item.get('timestamp', 0),
                            'confidence': item.get('confidence', 0)
                        }
                        for item in items
                    ]
                }

        return cluster_summary

    def generate_frequency_report(self, cluster_summary: Dict, total_videos: int) -> str:
        """
        Generate markdown report of pattern frequencies

        Args:
            cluster_summary: Output from cluster_jtbd()
            total_videos: Total number of videos analyzed

        Returns:
            Formatted markdown report
        """

        if not cluster_summary:
            return "No patterns found with >=2 instances."

        report_lines = []
        report_lines.append("# Cross-Video Pattern Frequency Report")
        report_lines.append("")
        report_lines.append(f"**Total Videos Analyzed:** {total_videos}")
        report_lines.append(f"**Pattern Clusters Found:** {len(cluster_summary)}")
        report_lines.append("")

        # Sort clusters by frequency (highest first)
        sorted_clusters = sorted(
            cluster_summary.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )

        for cluster_name, data in sorted_clusters:
            report_lines.append(f"## {cluster_name.replace('_', ' ').title()}")
            report_lines.append("")
            report_lines.append(f"**Frequency:** {data['count']} instances ({data['frequency_percent']}% of all JTBD)")
            report_lines.append(f"**Affected Videos:** {data['video_count']}/{total_videos} ({', '.join(data['video_ids'])})")
            report_lines.append("")
            report_lines.append(f"**Sample Quote:**")
            report_lines.append(f"> \"{data['sample_verbatim']}\"")
            report_lines.append("")
            report_lines.append(f"**All Instances:**")

            for i, instance in enumerate(data['all_instances'][:5], 1):  # Show first 5
                report_lines.append(f"{i}. `{instance['video_id']}` @ {instance['timestamp']:.1f}s (conf: {instance['confidence']:.2f})")
                report_lines.append(f"   \"{instance['verbatim']}\"")

            if len(data['all_instances']) > 5:
                report_lines.append(f"   _(+{len(data['all_instances']) - 5} more instances)_")

            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

        return "\n".join(report_lines)


def main():
    """Test pattern clustering on batch analysis"""
    import json
    from pathlib import Path

    # Load all JTBD from processed videos
    processed_dir = Path(__file__).parent.parent / 'data' / 'processed'
    all_jtbd = []
    video_ids = []

    for video_dir in sorted(processed_dir.glob('consumer*')):
        if not video_dir.is_dir():
            continue

        analysis_file = video_dir / 'analysis.json'
        if not analysis_file.exists():
            continue

        with open(analysis_file) as f:
            analysis = json.load(f)

        jtbd_list = analysis.get('jtbd', [])
        all_jtbd.extend(jtbd_list)
        video_ids.append(video_dir.name)

    print("=" * 60)
    print("🔗 CROSS-VIDEO PATTERN CLUSTERING TEST")
    print("=" * 60)
    print()
    print(f"Videos analyzed: {len(video_ids)}")
    print(f"Total JTBD instances: {len(all_jtbd)}")
    print()

    if not all_jtbd:
        print("❌ No JTBD data found")
        return

    # Cluster patterns
    clusterer = PatternClusterer()
    cluster_summary = clusterer.cluster_jtbd(all_jtbd)

    print(f"✅ Found {len(cluster_summary)} meaningful patterns (≥2 instances)")
    print()

    # Generate report
    report = clusterer.generate_frequency_report(cluster_summary, len(video_ids))
    print(report)


if __name__ == "__main__":
    main()
