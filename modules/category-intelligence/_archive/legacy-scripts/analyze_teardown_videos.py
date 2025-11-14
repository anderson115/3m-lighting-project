#!/usr/bin/env python3
"""
Product Teardown Analysis from Video Transcripts
Extracts technical insights: materials, construction, failure modes, BOM estimates
Written for R&D team from marketing perspective
"""
import json
import re
from pathlib import Path
from collections import defaultdict, Counter

class ProductTeardownAnalyzer:
    """Analyzes video transcripts to extract technical product insights."""

    def __init__(self):
        # Material detection patterns
        self.materials = {
            'metals': {
                'steel': [r'\bsteel\b', r'\bmetal\b', r'\biron\b'],
                'stainless_steel': [r'stainless\s+steel', r'\bss\b'],
                'aluminum': [r'aluminum', r'aluminium'],
                'zinc': [r'\bzinc\b', r'zinc\s+alloy', r'zinc\s+plated'],
                'brass': [r'\bbrass\b']
            },
            'plastics': {
                'abs': [r'\babs\b', r'abs\s+plastic'],
                'pvc': [r'\bpvc\b'],
                'polypropylene': [r'polypropylene', r'\bpp\b plastic'],
                'nylon': [r'\bnylon\b'],
                'generic_plastic': [r'\bplastic\b', r'polymer']
            },
            'adhesives': {
                '3m_tape': [r'3m\s+tape', r'vhb\s+tape', r'command\s+strip'],
                'acrylic_foam': [r'acrylic\s+foam', r'foam\s+tape'],
                'generic_adhesive': [r'\badhesive\b', r'sticky', r'\bglue\b']
            },
            'magnets': {
                'neodymium': [r'neodymium', r'neo\s+magnet', r'\bndfeb\b', r'rare\s+earth'],
                'generic_magnet': [r'\bmagnet\b', r'magnetic']
            },
            'coatings': {
                'powder_coat': [r'powder\s+coat'],
                'vinyl': [r'\bvinyl\b', r'vinyl\s+coat'],
                'rubber': [r'\brubber\b', r'rubber\s+coat', r'non.?slip'],
                'paint': [r'\bpaint\b', r'painted']
            }
        }

        # Construction/manufacturing patterns
        self.construction_methods = {
            'welding': [r'\bweld\b', r'welded', r'spot\s+weld'],
            'stamping': [r'\bstamp\b', r'stamped', r'die\s+cut'],
            'injection_molding': [r'injection\s+mold', r'molded\s+plastic'],
            'extrusion': [r'extrud'],
            'casting': [r'\bcast\b', r'casting', r'die\s+cast'],
            'fasteners': [r'\bscrew\b', r'\bbolt\b', r'rivet', r'fastener'],
            'adhesive_assembly': [r'glued', r'bonded', r'adhered']
        }

        # Quality/failure indicators
        self.quality_indicators = {
            'positive': {
                'well_made': [r'well\s+made', r'quality\s+construction', r'solid\s+build'],
                'thick_material': [r'thick\s+(?:metal|steel|plastic)', r'heavy\s+gauge'],
                'good_finish': [r'good\s+finish', r'smooth\s+finish', r'quality\s+coating'],
                'precision': [r'precise', r'tight\s+tolerance', r'good\s+fit']
            },
            'negative': {
                'thin_material': [r'thin\s+(?:metal|steel|plastic)', r'flimsy', r'cheap\s+feeling'],
                'poor_finish': [r'rough\s+(?:edges|finish)', r'burrs', r'sharp\s+edges'],
                'weak_adhesive': [r'adhesive\s+(?:weak|failed|poor)', r'doesn.?t\s+stick', r'fell\s+off'],
                'bent_easily': [r'bent', r'bends\s+easily', r'not\s+rigid'],
                'broke': [r'\bbroke\b', r'broken', r'snapped', r'cracked']
            }
        }

        # Weight capacity mentions
        self.weight_patterns = [
            r'(\d+)\s*(?:lbs?|pounds?)\s+(?:capacity|hold|support)',
            r'holds?\s+(?:up\s+to\s+)?(\d+)\s*(?:lbs?|pounds?)',
            r'rated\s+(?:for\s+)?(\d+)\s*(?:lbs?|pounds?)'
        ]

        # Price/value mentions
        self.cost_patterns = {
            'cheap': [r'\bcheap\b', r'inexpensive', r'budget'],
            'expensive': [r'expensive', r'pricey', r'costs?\s+a\s+lot'],
            'good_value': [r'good\s+value', r'worth\s+(?:the\s+)?(?:money|price)', r'great\s+deal'],
            'overpriced': [r'overpriced', r'not\s+worth', r'too\s+expensive']
        }

    def extract_materials(self, text):
        """Extract material mentions from text."""
        text_lower = text.lower()
        found_materials = defaultdict(int)

        for category, materials in self.materials.items():
            for material, patterns in materials.items():
                for pattern in patterns:
                    matches = re.findall(pattern, text_lower)
                    if matches:
                        found_materials[f"{category}/{material}"] += len(matches)

        return dict(found_materials)

    def extract_construction(self, text):
        """Extract construction method mentions."""
        text_lower = text.lower()
        found_methods = {}

        for method, patterns in self.construction_methods.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    found_methods[method] = True
                    break

        return found_methods

    def extract_quality_signals(self, text):
        """Extract quality indicators (positive and negative)."""
        text_lower = text.lower()
        signals = {'positive': {}, 'negative': {}}

        for sentiment in ['positive', 'negative']:
            for indicator, patterns in self.quality_indicators[sentiment].items():
                for pattern in patterns:
                    if re.search(pattern, text_lower):
                        signals[sentiment][indicator] = True
                        break

        return signals

    def extract_weight_capacity(self, text):
        """Extract weight capacity mentions."""
        capacities = []

        for pattern in self.weight_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                try:
                    capacities.append(int(match))
                except ValueError:
                    continue

        return capacities

    def extract_cost_sentiment(self, text):
        """Extract cost/value sentiment."""
        text_lower = text.lower()
        sentiment = {}

        for sentiment_type, patterns in self.cost_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    sentiment[sentiment_type] = True

        return sentiment

    def analyze_product_videos(self, product_data, transcripts_dir):
        """Analyze all videos for a single product."""
        product = product_data['product']
        videos = product_data['videos']

        print(f"\n{'='*70}")
        print(f"ANALYZING: {product['brand']} - {product['title'][:50]}...")
        print(f"{'='*70}")
        print(f"Videos to analyze: {len(videos)}")

        # Aggregate findings across all videos
        all_materials = Counter()
        all_construction = Counter()
        all_quality_positive = Counter()
        all_quality_negative = Counter()
        all_weight_capacities = []
        all_cost_sentiments = Counter()

        videos_analyzed = 0

        for video in videos:
            video_id = video['video_id']
            transcript_path = transcripts_dir / f"{video_id}.txt"

            if not transcript_path.exists():
                continue

            transcript = transcript_path.read_text()
            videos_analyzed += 1

            # Extract insights
            materials = self.extract_materials(transcript)
            construction = self.extract_construction(transcript)
            quality = self.extract_quality_signals(transcript)
            capacities = self.extract_weight_capacity(transcript)
            cost_sent = self.extract_cost_sentiment(transcript)

            # Aggregate
            all_materials.update(materials)
            all_construction.update(construction)
            all_quality_positive.update(quality['positive'])
            all_quality_negative.update(quality['negative'])
            all_weight_capacities.extend(capacities)
            all_cost_sentiments.update(cost_sent)

        # Generate product-level report
        report = {
            'product': product,
            'analysis': {
                'videos_analyzed': videos_analyzed,
                'materials': {
                    'primary_materials': dict(all_materials.most_common(5)),
                    'all_materials': dict(all_materials)
                },
                'construction': {
                    'methods_mentioned': dict(all_construction),
                    'primary_method': all_construction.most_common(1)[0][0] if all_construction else None
                },
                'quality_signals': {
                    'positive': dict(all_quality_positive),
                    'negative': dict(all_quality_negative),
                    'overall_sentiment': 'positive' if sum(all_quality_positive.values()) > sum(all_quality_negative.values()) else 'negative'
                },
                'weight_capacity': {
                    'mentioned_capacities_lbs': sorted(set(all_weight_capacities)),
                    'max_mentioned': max(all_weight_capacities) if all_weight_capacities else None,
                    'avg_mentioned': sum(all_weight_capacities) / len(all_weight_capacities) if all_weight_capacities else None
                },
                'value_perception': dict(all_cost_sentiments)
            }
        }

        # Print summary
        print(f"\nVideos analyzed: {videos_analyzed}/{len(videos)}")

        if all_materials:
            print(f"\nPrimary Materials:")
            for mat, count in all_materials.most_common(3):
                print(f"  • {mat}: {count} mentions")

        if all_construction:
            print(f"\nConstruction Methods:")
            for method, count in all_construction.most_common(3):
                print(f"  • {method}: {count} mentions")

        if all_weight_capacities:
            print(f"\nWeight Capacity: {min(all_weight_capacities)}-{max(all_weight_capacities)} lbs (avg: {sum(all_weight_capacities)/len(all_weight_capacities):.0f})")

        quality_score = sum(all_quality_positive.values()) - sum(all_quality_negative.values())
        print(f"\nQuality Score: {'+' if quality_score > 0 else ''}{quality_score} (positive - negative signals)")

        return report


def main():
    analyzer = ProductTeardownAnalyzer()

    # Load search results
    search_results_path = Path("outputs/teardown_videos_search_results.json")
    if not search_results_path.exists():
        print("ERROR: Search results not found. Run search_teardown_videos.py first.")
        return

    search_results = json.loads(search_results_path.read_text())
    transcripts_dir = Path("data/teardown_transcripts")

    if not transcripts_dir.exists():
        print("ERROR: Transcripts directory not found. Download videos first.")
        return

    # Analyze each product
    all_reports = {}

    for asin, product_data in search_results.items():
        try:
            report = analyzer.analyze_product_videos(product_data, transcripts_dir)
            all_reports[asin] = report
        except Exception as e:
            print(f"\nERROR analyzing {asin}: {e}")
            continue

    # Save individual reports
    output_dir = Path("outputs/teardown_reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    for asin, report in all_reports.items():
        report_path = output_dir / f"{asin}_teardown_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

    # Save combined report
    combined_path = Path("outputs/all_teardown_reports.json")
    with open(combined_path, 'w') as f:
        json.dump(all_reports, f, indent=2)

    print(f"\n\n{'='*70}")
    print(f"ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"Products analyzed: {len(all_reports)}")
    print(f"Reports saved to: {output_dir}")
    print(f"Combined report: {combined_path}")


if __name__ == "__main__":
    main()
