#!/usr/bin/env python3
"""
Direct runner for garage organizer analysis - bypasses import issues
"""

import sys
import os
import logging
from pathlib import Path

# Set up paths
MODULE_DIR = Path(__file__).parent
sys.path.insert(0, str(MODULE_DIR))

# Direct imports
import importlib.util

# Import orchestrator module directly
orchestrator_path = MODULE_DIR / "core" / "orchestrator.py"
spec = importlib.util.spec_from_file_location("orchestrator", orchestrator_path)
orchestrator_module = importlib.util.module_from_spec(spec)

# Pre-import dependencies
config_path = MODULE_DIR / "core" / "config.py"
spec = importlib.util.spec_from_file_location("config", config_path)
config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_module)

source_tracker_path = MODULE_DIR / "core" / "source_tracker.py"
spec = importlib.util.spec_from_file_location("source_tracker", source_tracker_path)
st_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st_module)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Import all collectors
collectors = {}
collector_names = ['brand_discovery', 'taxonomy_builder', 'pricing_analyzer',
                  'market_researcher', 'resource_curator', 'consumer_insights']

for name in collector_names:
    path = MODULE_DIR / "collectors" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    collectors[name] = module

# Import HTML reporter
html_reporter_path = MODULE_DIR / "generators" / "html_reporter.py"
spec = importlib.util.spec_from_file_location("html_reporter", html_reporter_path)
html_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(html_module)

# Now load orchestrator
sys.modules['config'] = config_module
sys.modules['source_tracker'] = st_module
sys.modules['html_reporter'] = html_module

# Inject into sys.modules with proper names
sys.modules['collectors.brand_discovery'] = collectors['brand_discovery']
sys.modules['collectors.taxonomy_builder'] = collectors['taxonomy_builder']
sys.modules['collectors.pricing_analyzer'] = collectors['pricing_analyzer']
sys.modules['collectors.market_researcher'] = collectors['market_researcher']
sys.modules['collectors.resource_curator'] = collectors['resource_curator']
sys.modules['collectors.consumer_insights'] = collectors['consumer_insights']

spec.loader.exec_module(orchestrator_module)

CategoryIntelligenceOrchestrator = orchestrator_module.CategoryIntelligenceOrchestrator

def main():
    logger.info("="*60)
    logger.info("GARAGE ORGANIZER MARKET ANALYSIS - US")
    logger.info("="*60)

    try:
        # Initialize orchestrator
        orchestrator = CategoryIntelligenceOrchestrator()

        # Run analysis
        results = orchestrator.analyze_category(
            category_name="garage organizer",
            output_name="Garage_Organizer_US_Market_Analysis"
        )

        logger.info("="*60)
        logger.info("ANALYSIS COMPLETE")
        logger.info("="*60)
        logger.info(f"Status: {results['status']}")

        if results["status"] == "completed":
            logger.info(f"HTML Report: {results.get('html_path')}")
            logger.info(f"Total Sources: {len(orchestrator.source_tracker)}")
            logger.info("✅ Analysis complete! Check outputs directory.")
            return 0
        elif results["status"] == "blocked_fabrication":
            logger.error("❌ Preflight validation failed - insufficient real sources")
            logger.error(f"Error: {results.get('error')}")
            return 1
        else:
            logger.error(f"Analysis failed: {results.get('error')}")
            return 1

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
