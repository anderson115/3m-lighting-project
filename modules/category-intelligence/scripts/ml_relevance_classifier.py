#!/usr/bin/env python3
"""
ML-Enhanced Relevance Classifier for YouTube Video Collection
Trains on existing data to predict relevance and optimize search queries
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
import math

BASE_PATH = Path("/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/category-intelligence")
CONSOLIDATED = BASE_PATH / "data" / "consolidated"

class MLRelevanceClassifier:
    def __init__(self):
        self.features = {
            "title_keywords": {},
            "channel_patterns": {},
            "query_performance": {},
            "bigrams": {},
            "trigrams": {}
        }
        self.relevance_scores = {}
        self.training_data = []

    def extract_features(self, video):
        """Extract features from video metadata for ML training"""
        features = {}

        title = video.get("title", "").lower()
        channel = video.get("channel", "").lower()
        search_query = video.get("search_query", "").lower()

        # Title features
        features["title_length"] = len(title)
        features["title_word_count"] = len(title.split())
        features["has_3m"] = int("3m" in title)
        features["has_claw"] = int("claw" in title)
        features["has_garage"] = int("garage" in title)
        features["has_organization"] = int("organization" in title or "organize" in title)
        features["has_storage"] = int("storage" in title)
        features["has_hook"] = int("hook" in title or "hanger" in title)
        features["has_diy"] = int("diy" in title)
        features["has_review"] = int("review" in title)
        features["has_installation"] = int("install" in title)
        features["has_transformation"] = int("transformation" in title or "makeover" in title)

        # Query-title alignment
        query_words = set(search_query.split())
        title_words = set(title.split())
        features["query_title_overlap"] = len(query_words.intersection(title_words))
        features["query_title_ratio"] = len(query_words.intersection(title_words)) / max(len(query_words), 1)

        # Title quality indicators
        features["has_numbers"] = int(bool(re.search(r'\d+', title)))
        features["has_year"] = int(bool(re.search(r'20\d{2}', title)))
        features["has_hashtags"] = int('#' in title)
        features["has_emoji"] = int(bool(re.search(r'[^\x00-\x7F]+', title)))
        features["all_caps_ratio"] = sum(1 for c in title if c.isupper()) / max(len(title), 1)

        # Channel features
        features["channel_length"] = len(channel)
        features["channel_is_brand"] = int(any(brand in channel for brand in ["3m", "command", "rubbermaid", "gladiator"]))

        # Search query features
        features["query_specificity"] = len(search_query.split())
        features["query_has_brand"] = int("3m" in search_query or "claw" in search_query)
        features["query_is_category"] = int("garage" in search_query and "organization" in search_query)

        return features

    def extract_ngrams(self, text, n=2):
        """Extract n-grams from text"""
        words = text.lower().split()
        ngrams = []
        for i in range(len(words) - n + 1):
            ngrams.append(' '.join(words[i:i+n]))
        return ngrams

    def train_from_existing_data(self):
        """Train classifier from existing labeled video data"""
        print("="*100)
        print("TRAINING ML RELEVANCE CLASSIFIER")
        print("="*100)

        # Load 3M Claw videos (high relevance)
        with open(CONSOLIDATED / "3m-claw-videos-youtube.json") as f:
            claw_data = json.load(f)

        # Load category videos (mixed relevance)
        with open(CONSOLIDATED / "garage-organizer-category-videos-youtube.json") as f:
            category_data = json.load(f)

        # Label training data
        # 3M Claw videos = highly relevant (label: 1.0)
        # Category videos with 3M/Claw in title = relevant (label: 0.8)
        # Category videos without 3M/Claw = somewhat relevant (label: 0.6)

        print(f"\n📚 Training Dataset:")
        print(f"  3M Claw videos: {len(claw_data.get('videos', []))}")
        print(f"  Category videos: {len(category_data.get('videos', []))}")

        # Process 3M Claw videos (highly relevant)
        for video in claw_data.get("videos", []):
            features = self.extract_features(video)
            self.training_data.append({
                "features": features,
                "label": 1.0,  # Highly relevant
                "video": video
            })

        # Process category videos (label based on content)
        for video in category_data.get("videos", []):
            title = video.get("title", "").lower()

            # Determine relevance label
            if "3m" in title or "claw" in title:
                label = 0.9  # High relevance (3M related)
            elif any(kw in title for kw in ["garage organization", "storage system", "hooks", "pegboard"]):
                label = 0.7  # Medium-high relevance
            elif any(kw in title for kw in ["garage makeover", "garage transformation"]):
                label = 0.6  # Medium relevance
            else:
                label = 0.5  # Lower relevance

            features = self.extract_features(video)
            self.training_data.append({
                "features": features,
                "label": label,
                "video": video
            })

        print(f"\n  Total training examples: {len(self.training_data)}")

        # Calculate feature importance
        self._calculate_feature_importance()

        # Train query performance model
        self._train_query_model()

        # Extract keyword patterns
        self._extract_keyword_patterns()

        print(f"\n✅ Training complete")

    def _calculate_feature_importance(self):
        """Calculate correlation between features and relevance"""
        print(f"\n🧮 Calculating feature importance...")

        feature_names = list(self.training_data[0]["features"].keys())
        feature_importances = {}

        for feature_name in feature_names:
            # Calculate correlation with label
            feature_values = [ex["features"][feature_name] for ex in self.training_data]
            labels = [ex["label"] for ex in self.training_data]

            # Simple correlation coefficient
            mean_feature = sum(feature_values) / len(feature_values)
            mean_label = sum(labels) / len(labels)

            numerator = sum((f - mean_feature) * (l - mean_label) for f, l in zip(feature_values, labels))
            denom_f = math.sqrt(sum((f - mean_feature) ** 2 for f in feature_values))
            denom_l = math.sqrt(sum((l - mean_label) ** 2 for l in labels))

            correlation = numerator / (denom_f * denom_l + 0.0001)
            feature_importances[feature_name] = abs(correlation)

        # Store and display top features
        self.feature_importance = dict(sorted(feature_importances.items(), key=lambda x: x[1], reverse=True))

        print(f"\n  Top 10 Most Important Features:")
        for i, (feature, importance) in enumerate(list(self.feature_importance.items())[:10], 1):
            print(f"    {i:2d}. {feature:30s} {importance:.4f}")

    def _train_query_model(self):
        """Train query performance prediction model"""
        print(f"\n🔍 Training query performance model...")

        query_stats = defaultdict(lambda: {"count": 0, "avg_relevance": 0, "total_relevance": 0})

        for example in self.training_data:
            query = example["video"].get("search_query", "")
            label = example["label"]

            query_stats[query]["count"] += 1
            query_stats[query]["total_relevance"] += label

        # Calculate average relevance per query
        for query, stats in query_stats.items():
            stats["avg_relevance"] = stats["total_relevance"] / stats["count"]
            stats["hit_rate"] = stats["avg_relevance"]

        self.query_performance = dict(query_stats)

        # Display top queries
        sorted_queries = sorted(self.query_performance.items(),
                               key=lambda x: (x[1]["avg_relevance"], x[1]["count"]),
                               reverse=True)

        print(f"\n  Top 15 Highest Performing Queries:")
        for i, (query, stats) in enumerate(sorted_queries[:15], 1):
            print(f"    {i:2d}. \"{query:40s}\" | Avg: {stats['avg_relevance']:.2f} | Count: {stats['count']:>3d}")

    def _extract_keyword_patterns(self):
        """Extract high-value keywords and patterns"""
        print(f"\n🔑 Extracting keyword patterns...")

        # Extract keywords from high-relevance videos
        high_relevance_titles = []
        for example in self.training_data:
            if example["label"] >= 0.8:
                high_relevance_titles.append(example["video"].get("title", ""))

        # Count bigrams and trigrams
        all_bigrams = []
        all_trigrams = []

        for title in high_relevance_titles:
            all_bigrams.extend(self.extract_ngrams(title, n=2))
            all_trigrams.extend(self.extract_ngrams(title, n=3))

        bigram_counts = Counter(all_bigrams)
        trigram_counts = Counter(all_trigrams)

        print(f"\n  Top 10 Bigrams (2-word patterns):")
        for i, (bigram, count) in enumerate(bigram_counts.most_common(10), 1):
            print(f"    {i:2d}. \"{bigram:30s}\" ({count} occurrences)")

        print(f"\n  Top 10 Trigrams (3-word patterns):")
        for i, (trigram, count) in enumerate(trigram_counts.most_common(10), 1):
            print(f"    {i:2d}. \"{trigram:35s}\" ({count} occurrences)")

        self.bigram_patterns = bigram_counts
        self.trigram_patterns = trigram_counts

    def predict_relevance(self, video):
        """Predict relevance score for a new video"""
        features = self.extract_features(video)

        # Weighted feature scoring
        score = 0.0
        weight_sum = 0.0

        for feature_name, feature_value in features.items():
            if feature_name in self.feature_importance:
                importance = self.feature_importance[feature_name]
                score += feature_value * importance
                weight_sum += importance

        # Normalize
        if weight_sum > 0:
            score = score / weight_sum

        # Boost score based on query performance
        query = video.get("search_query", "")
        if query in self.query_performance:
            query_boost = self.query_performance[query]["avg_relevance"] * 0.3
            score = score * 0.7 + query_boost

        return min(1.0, max(0.0, score))

    def generate_optimized_queries(self, n=20):
        """Generate optimized search queries based on learned patterns"""
        print(f"\n{'='*100}")
        print("GENERATING OPTIMIZED SEARCH QUERIES")
        print("="*100)

        # Start with top performing existing queries
        base_queries = sorted(self.query_performance.items(),
                             key=lambda x: x[1]["avg_relevance"],
                             reverse=True)[:10]

        optimized_queries = []

        # Add proven high performers
        for query, stats in base_queries:
            optimized_queries.append({
                "query": query,
                "expected_hit_rate": stats["avg_relevance"],
                "confidence": "HIGH (proven)",
                "evidence": f"{stats['count']} videos, {stats['avg_relevance']:.2f} avg relevance"
            })

        # Generate new queries using high-value patterns
        new_queries = [
            # 3M Claw specific
            "3M Claw vs drywall anchors",
            "3M Claw weight capacity test",
            "3M Claw damage free hanging",
            "best 3M Claw alternatives",

            # Category + brand combinations
            "garage organization 3M Claw",
            "3M Claw garage tool storage",
            "heavy duty garage hooks 3M",

            # High-performing category patterns
            "garage organization ideas 2025",
            "best garage storage solutions 2024",
            "DIY garage organization system",
            "professional garage organization tips"
        ]

        # Predict performance for new queries
        for query in new_queries:
            # Create synthetic video to test query
            synthetic_video = {
                "title": query,
                "search_query": query,
                "channel": "test"
            }

            predicted_score = self.predict_relevance(synthetic_video)

            optimized_queries.append({
                "query": query,
                "expected_hit_rate": predicted_score,
                "confidence": "PREDICTED (ML)",
                "evidence": f"ML model prediction based on feature patterns"
            })

        # Sort by expected hit rate
        optimized_queries.sort(key=lambda x: x["expected_hit_rate"], reverse=True)

        print(f"\n📊 Top {n} Optimized Search Queries:\n")
        for i, q in enumerate(optimized_queries[:n], 1):
            print(f"  {i:2d}. \"{q['query']:50s}\"")
            print(f"      Expected Hit Rate: {q['expected_hit_rate']:.1%}")
            print(f"      Confidence: {q['confidence']}")
            print(f"      Evidence: {q['evidence']}\n")

        return optimized_queries[:n]

    def calculate_improved_hit_rate(self, optimized_queries):
        """Calculate expected improvement in hit rate"""
        print(f"\n{'='*100}")
        print("HIT RATE IMPROVEMENT ANALYSIS")
        print("="*100)

        # Current average hit rate
        current_avg = sum(q["expected_hit_rate"] for q in optimized_queries[:10]) / 10

        # Baseline (existing queries)
        baseline_queries = sorted(self.query_performance.items(),
                                 key=lambda x: x[1]["avg_relevance"],
                                 reverse=True)[:10]
        baseline_avg = sum(q[1]["avg_relevance"] for q in baseline_queries) / 10

        print(f"\n📈 Performance Comparison:")
        print(f"  Baseline (existing queries):     {baseline_avg:.2%}")
        print(f"  Optimized (ML-enhanced queries): {current_avg:.2%}")
        print(f"  Improvement:                     {(current_avg - baseline_avg):.2%}")
        print(f"  Relative gain:                   {((current_avg / baseline_avg) - 1) * 100:.1f}%")

        # Calculate videos needed for targets
        targets = [10, 25, 50, 100]

        print(f"\n📊 Videos Required to Collect N Relevant Videos:")
        print(f"\n{'Target':>10s} | {'Baseline':>15s} | {'Optimized':>15s} | {'Savings':>12s}")
        print("-" * 60)

        for target in targets:
            baseline_needed = int(target / baseline_avg)
            optimized_needed = int(target / current_avg)
            savings = baseline_needed - optimized_needed
            savings_pct = (savings / baseline_needed) * 100

            print(f"{target:>10d} | {baseline_needed:>15d} | {optimized_needed:>15d} | {savings:>6d} ({savings_pct:>4.1f}%)")

        return {
            "baseline_hit_rate": baseline_avg,
            "optimized_hit_rate": current_avg,
            "improvement": current_avg - baseline_avg,
            "relative_gain_pct": ((current_avg / baseline_avg) - 1) * 100
        }

    def save_model(self):
        """Save trained model for future use"""
        model_data = {
            "feature_importance": self.feature_importance,
            "query_performance": self.query_performance,
            "bigram_patterns": dict(self.bigram_patterns.most_common(50)),
            "trigram_patterns": dict(self.trigram_patterns.most_common(50)),
            "training_size": len(self.training_data),
            "model_version": "1.0"
        }

        output_file = CONSOLIDATED / "ml_relevance_model.json"
        with open(output_file, 'w') as f:
            json.dump(model_data, f, indent=2)

        print(f"\n💾 Model saved to: {output_file}")

        return output_file

def main():
    print("="*100)
    print("ML-ENHANCED RELEVANCE CLASSIFIER FOR VIDEO COLLECTION")
    print("="*100)

    classifier = MLRelevanceClassifier()

    # Train from existing data
    classifier.train_from_existing_data()

    # Generate optimized queries
    optimized_queries = classifier.generate_optimized_queries(n=20)

    # Calculate improvement
    improvement = classifier.calculate_improved_hit_rate(optimized_queries)

    # Save model
    model_file = classifier.save_model()

    # Generate summary report
    print(f"\n{'='*100}")
    print("FINAL SUMMARY")
    print("="*100)

    print(f"\n✅ ML Model Training Complete")
    print(f"  Training examples: {len(classifier.training_data)}")
    print(f"  Features analyzed: {len(classifier.feature_importance)}")
    print(f"  Query patterns learned: {len(classifier.query_performance)}")

    print(f"\n📈 Expected Performance Gains:")
    print(f"  Baseline hit rate: {improvement['baseline_hit_rate']:.2%}")
    print(f"  Optimized hit rate: {improvement['optimized_hit_rate']:.2%}")
    print(f"  Improvement: +{improvement['improvement']:.2%}")
    print(f"  Relative gain: {improvement['relative_gain_pct']:.1f}%")

    print(f"\n💡 To collect 25 relevant videos:")
    baseline_needed = int(25 / improvement['baseline_hit_rate'])
    optimized_needed = int(25 / improvement['optimized_hit_rate'])
    print(f"  Before optimization: {baseline_needed} videos needed")
    print(f"  After optimization:  {optimized_needed} videos needed")
    print(f"  Savings: {baseline_needed - optimized_needed} fewer videos ({((baseline_needed - optimized_needed) / baseline_needed * 100):.1f}% reduction)")

    print(f"\n🎯 Next Steps:")
    print(f"  1. Use optimized queries from ml_relevance_model.json")
    print(f"  2. Collect videos using top 10-15 queries")
    print(f"  3. Filter results using ML prediction scores")
    print(f"  4. Retrain model periodically with new data")

    return 0

if __name__ == "__main__":
    exit(main())
