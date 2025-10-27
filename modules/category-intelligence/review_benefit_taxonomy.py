#!/usr/bin/env python3
"""
Review & Social Media Benefit Taxonomy Builder
Extracts benefits, rates importance (frequency) and satisfaction (sentiment)
"""
import json
import sqlite3
from pathlib import Path
from collections import Counter, defaultdict
import re

class BenefitTaxonomyAnalyzer:
    """Analyzes customer feedback to build benefit taxonomy with importance/satisfaction scores."""

    def __init__(self):
        self.benefit_patterns = {
            # Installation & Setup
            'easy_installation': [
                r'\beas(?:y|ier|iest)\s+(?:to\s+)?install',
                r'simple\s+(?:to\s+)?install',
                r'quick\s+(?:to\s+)?install',
                r'install\s+in\s+minutes',
                r'no\s+tools?\s+(?:required|needed)',
                r'tool.free\s+install'
            ],
            'clear_instructions': [
                r'clear\s+instructions',
                r'good\s+instructions',
                r'easy\s+to\s+follow',
                r'well\s+explained'
            ],

            # Durability & Quality
            'durability': [
                r'\bdurable\b',
                r'\bsturdy\b',
                r'\bsolid\b',
                r'\bwell.made\b',
                r'\bheavy.duty\b',
                r'built\s+to\s+last',
                r'quality\s+(?:construction|build)',
                r'\bstrong\b'
            ],
            'weight_capacity': [
                r'holds?\s+(?:a\s+lot|heavy|weight)',
                r'weight\s+capacity',
                r'supports?\s+\d+\s*(?:lbs?|pounds)',
                r'can\s+hold',
                r'heavy\s+(?:duty|load)'
            ],

            # Adhesion & Mounting
            'strong_adhesion': [
                r'sticks?\s+well',
                r'strong\s+adhesive',
                r'stays?\s+(?:in\s+place|put)',
                r'doesn.?t\s+fall',
                r'holds?\s+tight',
                r'secure(?:ly)?\s+(?:attached|mounted)'
            ],
            'no_wall_damage': [
                r'no\s+(?:holes|drilling|damage)',
                r'damage.free',
                r'won.?t\s+damage\s+wall',
                r'renter.friendly',
                r'removable'
            ],

            # Aesthetics
            'appearance': [
                r'looks?\s+(?:good|great|nice|clean)',
                r'aesthetic',
                r'sleek',
                r'professional\s+looking',
                r'low\s+profile',
                r'discreet'
            ],
            'color_options': [
                r'color\s+(?:options|choices)',
                r'comes\s+in\s+\w+\s+colors?',
                r'matches?\s+(?:decor|my\s+\w+)'
            ],

            # Functionality
            'versatility': [
                r'versatile',
                r'multiple\s+uses',
                r'can\s+use\s+for\s+\w+\s+(?:and|or)',
                r'works?\s+(?:great|well)\s+for\s+\w+\s+(?:and|or)'
            ],
            'space_saving': [
                r'saves?\s+space',
                r'space.saving',
                r'free(?:s|d)\s+up\s+(?:space|floor)',
                r'organize(?:s|d)',
                r'declutter'
            ],
            'adjustable': [
                r'adjustable',
                r'can\s+adjust',
                r'customizable',
                r'flexible\s+(?:setup|configuration)'
            ],

            # Value
            'price_value': [
                r'(?:great|good|excellent)\s+value',
                r'worth\s+(?:the\s+)?(?:money|price)',
                r'affordable',
                r'reasonably\s+priced',
                r'good\s+deal'
            ],
            'quantity': [
                r'comes\s+with\s+\d+',
                r'pack\s+of\s+\d+',
                r'includes\s+\d+',
                r'good\s+quantity'
            ],

            # Common Pain Points (negative)
            'falls_off': [
                r'f(?:a|e)ll(?:s|ing)?\s+off',
                r'doesn.?t\s+stick',
                r'adhesive\s+(?:failed|weak)',
                r'came\s+off\s+(?:the\s+)?wall'
            ],
            'poor_quality': [
                r'cheap\s+(?:quality|material)',
                r'broke\s+(?:easily|quickly)',
                r'flimsy',
                r'poor\s+quality',
                r'cheaply\s+made'
            ],
            'difficult_install': [
                r'hard\s+to\s+install',
                r'difficult\s+(?:to\s+)?install',
                r'installation\s+(?:was\s+)?(?:a\s+)?pain',
                r'confusing\s+instructions'
            ]
        }

        # Sentiment keywords
        self.positive_words = {
            'love', 'great', 'excellent', 'perfect', 'amazing', 'awesome',
            'fantastic', 'wonderful', 'best', 'highly recommend', 'impressed',
            'happy', 'satisfied', 'pleased', 'works great', 'exactly what'
        }

        self.negative_words = {
            'disappointing', 'disappointed', 'poor', 'terrible', 'awful',
            'waste', 'don\'t buy', 'regret', 'returning', 'broke', 'failed',
            'useless', 'garbage', 'junk', 'worst', 'horrible'
        }

    def extract_benefits(self, text):
        """Extract benefit mentions from text."""
        text_lower = text.lower()
        found_benefits = {}

        for benefit, patterns in self.benefit_patterns.items():
            matches = []
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    matches.extend(re.findall(pattern, text_lower))

            if matches:
                # Calculate sentiment for this mention
                sentence_window = 100  # characters around match
                context_sentiments = []

                for match in matches:
                    idx = text_lower.find(match)
                    if idx >= 0:
                        context = text_lower[max(0, idx-sentence_window):idx+sentence_window]

                        # Simple sentiment
                        pos_count = sum(1 for word in self.positive_words if word in context)
                        neg_count = sum(1 for word in self.negative_words if word in context)

                        if pos_count > neg_count:
                            context_sentiments.append('positive')
                        elif neg_count > pos_count:
                            context_sentiments.append('negative')
                        else:
                            context_sentiments.append('neutral')

                found_benefits[benefit] = {
                    'count': len(matches),
                    'sentiment': context_sentiments
                }

        return found_benefits

    def analyze_corpus(self, texts, source_name):
        """Analyze a corpus of texts."""
        print(f"\n{'='*70}")
        print(f"ANALYZING: {source_name}")
        print(f"Documents: {len(texts)}")
        print(f"{'='*70}")

        all_benefits = defaultdict(lambda: {'total_mentions': 0, 'positive': 0, 'negative': 0, 'neutral': 0})

        for text in texts:
            if not text or not isinstance(text, str):
                continue

            benefits = self.extract_benefits(text)

            for benefit, data in benefits.items():
                all_benefits[benefit]['total_mentions'] += data['count']
                for sentiment in data['sentiment']:
                    all_benefits[benefit][sentiment] += 1

        # Calculate importance and satisfaction scores
        results = []
        total_docs = len(texts)

        for benefit, stats in all_benefits.items():
            if stats['total_mentions'] == 0:
                continue

            # Importance: % of documents mentioning this benefit
            importance = (stats['total_mentions'] / total_docs) * 100

            # Satisfaction: % of positive mentions vs total
            total_sentiment = stats['positive'] + stats['negative'] + stats['neutral']
            if total_sentiment > 0:
                satisfaction = (stats['positive'] / total_sentiment) * 100
            else:
                satisfaction = 50  # neutral

            results.append({
                'benefit': benefit,
                'importance': round(importance, 2),
                'satisfaction': round(satisfaction, 2),
                'total_mentions': stats['total_mentions'],
                'positive_mentions': stats['positive'],
                'negative_mentions': stats['negative'],
                'neutral_mentions': stats['neutral']
            })

        # Sort by importance
        results.sort(key=lambda x: x['importance'], reverse=True)

        print(f"\nTOP 15 BENEFITS BY IMPORTANCE")
        print(f"{'='*70}")
        print(f"{'Benefit':<25} {'Import%':<10} {'Satisfy%':<10} {'Mentions':<10}")
        print(f"{'-'*70}")

        for item in results[:15]:
            print(f"{item['benefit']:<25} {item['importance']:<10.1f} {item['satisfaction']:<10.1f} {item['total_mentions']:<10}")

        return results

    def create_importance_satisfaction_matrix(self, results, output_path):
        """Create matrix categorization."""

        # Define quadrants
        avg_importance = sum(r['importance'] for r in results) / len(results) if results else 0
        avg_satisfaction = sum(r['satisfaction'] for r in results) / len(results) if results else 0

        quadrants = {
            'maintain': [],      # High importance, high satisfaction
            'improve': [],       # High importance, low satisfaction
            'promote': [],       # Low importance, high satisfaction
            'monitor': []        # Low importance, low satisfaction
        }

        for item in results:
            if item['importance'] >= avg_importance:
                if item['satisfaction'] >= avg_satisfaction:
                    quadrants['maintain'].append(item)
                else:
                    quadrants['improve'].append(item)
            else:
                if item['satisfaction'] >= avg_satisfaction:
                    quadrants['promote'].append(item)
                else:
                    quadrants['monitor'].append(item)

        # Save report
        report = {
            'summary': {
                'total_benefits': len(results),
                'avg_importance': round(avg_importance, 2),
                'avg_satisfaction': round(avg_satisfaction, 2)
            },
            'quadrants': quadrants,
            'all_benefits': results
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n{'='*70}")
        print(f"IMPORTANCE/SATISFACTION MATRIX")
        print(f"{'='*70}")
        print(f"\nMAINTAIN (High Importance, High Satisfaction) - {len(quadrants['maintain'])} benefits")
        print("These are your strengths - keep delivering")
        for item in quadrants['maintain'][:5]:
            print(f"  • {item['benefit']}: {item['importance']:.1f}% importance, {item['satisfaction']:.1f}% satisfaction")

        print(f"\nIMPROVE (High Importance, Low Satisfaction) - {len(quadrants['improve'])} benefits")
        print("Critical gaps - fix these first")
        for item in quadrants['improve'][:5]:
            print(f"  • {item['benefit']}: {item['importance']:.1f}% importance, {item['satisfaction']:.1f}% satisfaction")

        print(f"\nPROMOTE (Low Importance, High Satisfaction) - {len(quadrants['promote'])} benefits")
        print("Hidden strengths - market these better")
        for item in quadrants['promote'][:5]:
            print(f"  • {item['benefit']}: {item['importance']:.1f}% importance, {item['satisfaction']:.1f}% satisfaction")

        print(f"\n{'='*70}")
        print(f"Full report saved to: {output_path}")

        return report


def main():
    analyzer = BenefitTaxonomyAnalyzer()

    all_source_results = []

    # Load Reddit data
    reddit_path = Path("data/reddit_garage_organization.json")
    if reddit_path.exists():
        reddit_data = json.loads(reddit_path.read_text())
        reddit_texts = []
        for post in reddit_data:
            if isinstance(post, dict):
                reddit_texts.append(post.get('selftext', '') or post.get('title', ''))

        reddit_results = analyzer.analyze_corpus(reddit_texts, "Reddit Posts (880)")
        all_source_results.append(reddit_results)

    # Load YouTube transcripts
    youtube_dir = Path("data/youtube_transcripts")
    youtube_texts = []
    if youtube_dir.exists():
        for file in youtube_dir.glob("*.txt"):
            youtube_texts.append(file.read_text())

        youtube_results = analyzer.analyze_corpus(youtube_texts, f"YouTube Transcripts ({len(youtube_texts)})")
        all_source_results.append(youtube_results)

    # Load TikTok transcripts
    tiktok_dir = Path("data/tiktok_transcripts")
    tiktok_texts = []
    if tiktok_dir.exists():
        for file in tiktok_dir.glob("*.txt"):
            tiktok_texts.append(file.read_text())

        tiktok_results = analyzer.analyze_corpus(tiktok_texts, f"TikTok Transcripts ({len(tiktok_texts)})")
        all_source_results.append(tiktok_results)

    # Combine all results
    all_results = defaultdict(lambda: {'importance': 0, 'satisfaction': 0, 'total_mentions': 0,
                                        'positive_mentions': 0, 'negative_mentions': 0, 'sources': 0})

    for results in all_source_results:
        for item in results:
            benefit = item['benefit']
            all_results[benefit]['importance'] += item['importance']
            all_results[benefit]['satisfaction'] += item['satisfaction']
            all_results[benefit]['total_mentions'] += item['total_mentions']
            all_results[benefit]['positive_mentions'] += item['positive_mentions']
            all_results[benefit]['negative_mentions'] += item['negative_mentions']
            all_results[benefit]['sources'] += 1

    # Average across sources
    combined = []
    for benefit, stats in all_results.items():
        combined.append({
            'benefit': benefit,
            'importance': round(stats['importance'] / stats['sources'], 2),
            'satisfaction': round(stats['satisfaction'] / stats['sources'], 2),
            'total_mentions': stats['total_mentions'],
            'positive_mentions': stats['positive_mentions'],
            'negative_mentions': stats['negative_mentions'],
            'sources': stats['sources']
        })

    combined.sort(key=lambda x: x['importance'], reverse=True)

    print(f"\n\n{'='*70}")
    print(f"COMBINED ANALYSIS - ALL SOURCES")
    print(f"{'='*70}")
    print(f"\nTOP 20 BENEFITS (OVERALL)")
    print(f"{'='*70}")
    print(f"{'Benefit':<25} {'Import%':<10} {'Satisfy%':<10} {'Mentions':<10} {'Sources'}")
    print(f"{'-'*70}")

    for item in combined[:20]:
        print(f"{item['benefit']:<25} {item['importance']:<10.1f} {item['satisfaction']:<10.1f} {item['total_mentions']:<10} {item['sources']}")

    # Create matrix
    output_path = Path("outputs/benefit_taxonomy_analysis.json")
    report = analyzer.create_importance_satisfaction_matrix(combined, output_path)

    print(f"\n{'='*70}")
    print(f"ANALYSIS COMPLETE")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
