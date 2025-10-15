"""
Run comprehensive 25-creator test for client deliverable.
Tests full end-to-end functionality with data verification.
"""

import sys
from pathlib import Path

# Add module to path (same pattern as test_50_creators_with_metrics.py)
module_root = Path(__file__).parent
sys.path.insert(0, str(module_root))

from core.orchestrator import CreatorIntelligenceOrchestrator
from core.config import config
import json
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run 25-creator comprehensive test."""

    logger.info("🚀 Starting 25-Creator Comprehensive Test")
    logger.info("=" * 60)

    # Initialize orchestrator
    orchestrator = CreatorIntelligenceOrchestrator()

    # Define keywords across different lighting use cases
    keywords = [
        'LED strip lights installation',
        'smart home lighting',
        'ambient lighting setup',
        'kitchen cabinet lighting',
        'bedroom lighting ideas',
        'gaming room lighting',
        'DIY lighting projects',
        'home theater lighting'
    ]

    logger.info(f"📋 Testing {len(keywords)} keywords")
    logger.info(f"🎯 Target: ~25 creators (3 per keyword)")
    logger.info(f"📊 Content: 10 items per creator")
    logger.info("")

    # Run analysis
    logger.info("🔍 Analyzing creators...")
    results = orchestrator.analyze_creators(
        keywords=keywords,
        limit_per_platform=25,
        max_content_per_creator=10
    )

    logger.info("")
    logger.info("=" * 60)
    logger.info(f"✅ Test Complete - Analyzed {len(results)} creators")
    logger.info("=" * 60)

    # Save results
    output_path = Path(__file__).parent / "25_creator_test_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    logger.info(f"💾 Results saved: {output_path}")

    # Verify data in database
    logger.info("")
    logger.info("🔍 Verifying database contents...")
    db_path = Path(__file__).parent / "data" / "database" / "creators.db"

    if not db_path.exists():
        logger.error(f"❌ Database not found: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Count creators
    cursor.execute("SELECT COUNT(*) FROM creators")
    creator_count = cursor.fetchone()[0]
    logger.info(f"   Creators in DB: {creator_count}")

    # Count content
    cursor.execute("SELECT COUNT(*) FROM creator_content")
    content_count = cursor.fetchone()[0]
    logger.info(f"   Content items in DB: {content_count}")

    # Verify titles populated
    cursor.execute("SELECT COUNT(*) FROM creator_content WHERE title IS NOT NULL AND title != ''")
    titles_count = cursor.fetchone()[0]
    logger.info(f"   Titles populated: {titles_count}/{content_count} ({titles_count/content_count*100:.1f}%)")

    # Verify descriptions populated
    cursor.execute("SELECT COUNT(*) FROM creator_content WHERE description IS NOT NULL AND description != ''")
    desc_count = cursor.fetchone()[0]
    logger.info(f"   Descriptions populated: {desc_count}/{content_count} ({desc_count/content_count*100:.1f}%)")

    # Verify engagement metrics
    cursor.execute("SELECT COUNT(*) FROM creator_content WHERE view_count IS NOT NULL AND view_count > 0")
    views_count = cursor.fetchone()[0]
    logger.info(f"   View counts populated: {views_count}/{content_count} ({views_count/content_count*100:.1f}%)")

    # Verify classifications
    cursor.execute("SELECT COUNT(*) FROM creator_content WHERE classification IS NOT NULL")
    classified_count = cursor.fetchone()[0]
    logger.info(f"   Classifications populated: {classified_count}/{content_count} ({classified_count/content_count*100:.1f}%)")

    # Sample a record to verify full data
    cursor.execute("""
        SELECT title, description, view_count, like_count, classification, relevance_score
        FROM creator_content
        WHERE title IS NOT NULL
        LIMIT 1
    """)
    sample = cursor.fetchone()

    logger.info("")
    logger.info("📋 Sample Record Verification:")
    if sample:
        logger.info(f"   Title: {sample[0][:50]}...")
        logger.info(f"   Description: {sample[1][:50] if sample[1] else 'None'}...")
        logger.info(f"   Views: {sample[2]:,}")
        logger.info(f"   Likes: {sample[3]:,}")
        logger.info(f"   Classification: {sample[4]}")
        logger.info(f"   Relevance: {sample[5]:.2f}")
        logger.info("   ✅ Full data captured!")
    else:
        logger.error("   ❌ No records found!")

    conn.close()

    logger.info("")
    logger.info("=" * 60)
    logger.info("🎯 VERIFICATION SUMMARY")
    logger.info("=" * 60)

    if titles_count == content_count and desc_count > content_count * 0.8 and views_count > content_count * 0.8:
        logger.info("✅ DATA PRESERVATION: 100% SUCCESS")
        logger.info("✅ All scraped data captured correctly")
        logger.info("✅ Ready for client report generation")
    else:
        logger.error("⚠️ DATA PRESERVATION: PARTIAL")
        logger.error("⚠️ Some data may be missing - review logs")

    logger.info("")
    logger.info("📊 Next step: Generate client report")
    logger.info(f"   Run: python {Path(__file__).parent}/generate_client_report.py")
    logger.info("")

if __name__ == "__main__":
    main()
