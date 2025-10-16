#!/usr/bin/env python3
"""
Readiness Checker - Validate Environment Before Running Analysis

Command-line tool to check if all required data sources are configured.
Provides actionable guidance on what's missing and how to fix it.

Usage:
    python3 check_readiness.py
    python3 check_readiness.py --verbose
    python3 check_readiness.py --json
"""

import sys
import json
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.environment_checker import EnvironmentChecker


def main():
    parser = argparse.ArgumentParser(
        description="Check if environment is ready for category intelligence analysis"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed information for all sources"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of formatted report"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only output errors (exit code 0=ready, 1=not ready)"
    )

    args = parser.parse_args()

    # Check environment
    checker = EnvironmentChecker()
    ready, checks = checker.check_all_sources()

    if args.json:
        # Output JSON format
        output = {
            "ready": ready,
            "checks": [
                {
                    "name": check.name,
                    "status": check.status.value,
                    "message": check.message,
                    "priority": check.priority,
                    "setup_instructions": check.setup_instructions
                }
                for check in checks
            ],
            "missing": checker.get_missing_requirements()
        }
        print(json.dumps(output, indent=2))

    elif args.quiet:
        # Quiet mode - only exit code matters
        if not ready:
            print("Not ready", file=sys.stderr)

    else:
        # Human-readable report
        report = checker.generate_readiness_report()
        print(report)

        if args.verbose:
            print("\n\nDETAILED CHECK RESULTS:")
            print("=" * 80)
            for check in checks:
                print(f"\n{check.name}:")
                print(f"  Status: {check.status.value}")
                print(f"  Priority: {check.priority}")
                print(f"  Message: {check.message}")
                if args.verbose:
                    print(f"  Setup:")
                    for line in check.setup_instructions.split("\n"):
                        print(f"    {line}")

    # Exit with appropriate code
    sys.exit(0 if ready else 1)


if __name__ == "__main__":
    main()
