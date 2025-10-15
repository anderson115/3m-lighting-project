#!/usr/bin/env python3
"""
Full system test with 50 creators and detailed performance metrics.
Tests error resilience, API usage, timing, and data quality.
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add module to path
module_root = Path(__file__).parent
sys.path.insert(0, str(module_root))

from core.orchestrator import CreatorIntelligenceOrchestrator

def main():
    print("=" * 80)
    print("CREATOR INTELLIGENCE MODULE - 50 CREATOR SYSTEM TEST")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Track metrics
    metrics = {
        'start_time': time.time(),
        'test_config': {
            'target_creators': 50,
            'videos_per_creator': 20,
            'keywords': ["LED lighting", "smart lighting", "home lighting"],
            'platforms': ["youtube"]
        },
        'phases': {}
    }

    try:
        # Initialize orchestrator
        print("📦 Initializing orchestrator...")
        init_start = time.time()
        orchestrator = CreatorIntelligenceOrchestrator()
        metrics['phases']['initialization'] = {
            'duration_seconds': time.time() - init_start,
            'status': 'success'
        }
        print(f"✅ Initialized in {time.time() - init_start:.2f}s\n")

        # Run analysis
        print("🚀 Starting analysis with 50 creator target...")
        analysis_start = time.time()

        results = orchestrator.analyze_creators(
            keywords=metrics['test_config']['keywords'],
            platforms=metrics['test_config']['platforms'],
            limit_per_platform=17  # 17 × 3 keywords = ~51 creators
        )

        analysis_duration = time.time() - analysis_start
        metrics['phases']['analysis'] = {
            'duration_seconds': analysis_duration,
            'duration_minutes': analysis_duration / 60,
            'status': 'success'
        }

        print(f"\n✅ Analysis completed in {analysis_duration:.2f}s ({analysis_duration/60:.2f} min)\n")

        # Collect metrics
        print("=" * 80)
        print("PERFORMANCE METRICS")
        print("=" * 80)

        metrics['results'] = results
        metrics['end_time'] = time.time()
        metrics['total_duration_seconds'] = metrics['end_time'] - metrics['start_time']
        metrics['total_duration_minutes'] = metrics['total_duration_seconds'] / 60

        # Calculate derived metrics
        creators_analyzed = results.get('total_creators_analyzed', 0)
        failed_count = results.get('failed_creators_count', 0)
        total_attempted = creators_analyzed + failed_count

        metrics['performance'] = {
            'total_creators_attempted': total_attempted,
            'creators_successfully_analyzed': creators_analyzed,
            'creators_failed': failed_count,
            'success_rate': results.get('success_rate', '0%'),
            'time_per_creator_seconds': analysis_duration / creators_analyzed if creators_analyzed > 0 else 0,
            'llm_tokens_used': results.get('llm_tokens_used', 0)
        }

        # Get YouTube API quota usage
        if 'youtube' in orchestrator.scrapers:
            youtube_scraper = orchestrator.scrapers['youtube']
            metrics['api_usage'] = {
                'youtube_quota_used': youtube_scraper.quota_used,
                'youtube_quota_limit': 10000,
                'quota_percent_used': (youtube_scraper.quota_used / 10000) * 100
            }

        # Database stats
        if 'database_stats' in results:
            metrics['database'] = results['database_stats']

        # Print metrics
        print(f"\n📊 TIMING METRICS:")
        print(f"   Total Duration: {metrics['total_duration_minutes']:.2f} minutes")
        print(f"   Analysis Phase: {metrics['phases']['analysis']['duration_minutes']:.2f} minutes")
        print(f"   Time per Creator: {metrics['performance']['time_per_creator_seconds']:.2f} seconds")

        print(f"\n📈 THROUGHPUT METRICS:")
        print(f"   Creators Attempted: {metrics['performance']['total_creators_attempted']}")
        print(f"   Creators Successful: {metrics['performance']['creators_successfully_analyzed']}")
        print(f"   Creators Failed: {metrics['performance']['creators_failed']}")
        print(f"   Success Rate: {metrics['performance']['success_rate']}")

        if 'api_usage' in metrics:
            print(f"\n🔌 API USAGE:")
            print(f"   YouTube Quota Used: {metrics['api_usage']['youtube_quota_used']} units")
            print(f"   Quota Limit: {metrics['api_usage']['youtube_quota_limit']} units")
            print(f"   Quota % Used: {metrics['api_usage']['quota_percent_used']:.1f}%")

        print(f"\n🧠 LLM USAGE:")
        print(f"   Tokens Used: {metrics['performance']['llm_tokens_used']:,}")

        if 'database' in metrics:
            print(f"\n💾 DATABASE STATS:")
            print(f"   Total Creators: {metrics['database'].get('total_creators', 0)}")
            print(f"   Total Content: {metrics['database'].get('total_content', 0)}")
            print(f"   Language Phrases: {metrics['database'].get('total_language_phrases', 0)}")

        # Save detailed metrics
        metrics_file = module_root / 'test_metrics_50_creators.json'
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)

        print(f"\n📄 Detailed metrics saved to: {metrics_file}")

        # Analyze bottlenecks
        print("\n" + "=" * 80)
        print("BOTTLENECK ANALYSIS")
        print("=" * 80)

        if creators_analyzed > 0:
            avg_time_per_creator = analysis_duration / creators_analyzed
            expected_time_30 = avg_time_per_creator * 30

            print(f"\n⏱️  ACTUAL PERFORMANCE:")
            print(f"   {creators_analyzed} creators processed in {analysis_duration/60:.2f} minutes")
            print(f"   Average: {avg_time_per_creator:.2f} seconds per creator")

            print(f"\n📐 PROJECTED PERFORMANCE:")
            print(f"   30 creators would take: {expected_time_30/60:.2f} minutes")

            print(f"\n🔍 BOTTLENECK BREAKDOWN:")
            # Estimate where time is spent
            youtube_api_time = metrics['api_usage']['youtube_quota_used'] * 0.5 if 'api_usage' in metrics else 0  # ~0.5s per API call
            llm_estimated_time = (metrics['performance']['llm_tokens_used'] / 1000) * 1.5  # Rough estimate
            database_time = 5  # Estimated
            overhead = analysis_duration - youtube_api_time - llm_estimated_time - database_time

            print(f"   YouTube API calls: ~{youtube_api_time:.1f}s ({youtube_api_time/analysis_duration*100:.1f}%)")
            print(f"   LLM classification: ~{llm_estimated_time:.1f}s ({llm_estimated_time/analysis_duration*100:.1f}%)")
            print(f"   Database operations: ~{database_time:.1f}s ({database_time/analysis_duration*100:.1f}%)")
            print(f"   Other overhead: ~{overhead:.1f}s ({overhead/analysis_duration*100:.1f}%)")

            # Identify optimization opportunities
            print(f"\n💡 OPTIMIZATION OPPORTUNITIES:")
            if youtube_api_time / analysis_duration > 0.3:
                print(f"   ⚠️  YouTube API calls are {youtube_api_time/analysis_duration*100:.0f}% of total time")
                print(f"      → Batch API calls could reduce by ~70%")

            if llm_estimated_time / analysis_duration > 0.4:
                print(f"   ⚠️  LLM calls are {llm_estimated_time/analysis_duration*100:.0f}% of total time")
                print(f"      → Batch LLM classification could reduce by ~60%")

        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Close orchestrator
        orchestrator.close()

        return 0

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

        metrics['error'] = {
            'message': str(e),
            'traceback': traceback.format_exc()
        }

        # Save error metrics
        metrics_file = module_root / 'test_metrics_50_creators_ERROR.json'
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)

        print(f"\nError metrics saved to: {metrics_file}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
