#!/usr/bin/env python3
"""
Category Intelligence Test Runner
Run category analysis with a test category
"""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.category_intelligence.core.orchestrator import CategoryIntelligenceOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Run Category Intelligence Analysis"
    )
    parser.add_argument(
        "--category",
        type=str,
        required=True,
        help="Category to analyze (e.g., 'Smart Home Lighting')"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file name (optional, defaults to category name)"
    )

    args = parser.parse_args()

    logger.info("="*60)
    logger.info("CATEGORY INTELLIGENCE ANALYSIS")
    logger.info("="*60)
    logger.info(f"Category: {args.category}")
    logger.info(f"Output: {args.output or 'auto-generated'}")
    logger.info("="*60)

    # Initialize orchestrator
    orchestrator = CategoryIntelligenceOrchestrator()

    # Run analysis
    try:
        results = orchestrator.analyze_category(
            category_name=args.category,
            output_name=args.output
        )

        logger.info("="*60)
        logger.info("ANALYSIS COMPLETE")
        logger.info("="*60)
        logger.info(f"Status: {results['status']}")

        if results["status"] == "completed":
            logger.info(f"HTML Report: {results.get('html_path')}")
            logger.info(f"Audit Trail: {results.get('audit_path')}")
            logger.info(f"Citations: {results.get('citations_path')}")
            logger.info(f"Total Sources: {len(orchestrator.source_tracker)}")

            # Show validation summary
            validation = results.get("source_validation", {})
            logger.info("\nSource Validation:")
            logger.info(f"  Total Sources: {validation.get('total_sources', 0)}")
            logger.info(f"  High Confidence: {validation.get('by_confidence', {}).get('high', 0)}")
            logger.info(f"  Medium Confidence: {validation.get('by_confidence', {}).get('medium', 0)}")
            logger.info(f"  Low Confidence: {validation.get('by_confidence', {}).get('low', 0)}")

            logger.info("\n✅ Analysis complete! Check outputs directory for results.")

        else:
            logger.error(f"Analysis failed: {results.get('error')}")
            return 1

    except Exception as e:
        logger.error(f"Fatal error during analysis: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
