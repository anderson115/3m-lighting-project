#!/usr/bin/env python3
"""
Test script for Pinterest visual scraper.
Demonstrates search, pin analysis, and board analysis capabilities.
"""

import asyncio
import json
from pathlib import Path
from scrapers.pinterest_scraper import PinterestScraper

async def main():
    """Run Pinterest scraper tests."""

    # Initialize scraper
    cache_dir = Path(__file__).parent / "data" / "cache" / "pinterest"
    screenshot_dir = Path(__file__).parent / "data" / "screenshots" / "pinterest"

    print("=" * 80)
    print("🎨 PINTEREST VISUAL SCRAPER TEST")
    print("=" * 80)

    scraper = PinterestScraper(
        cache_dir=cache_dir,
        screenshot_dir=screenshot_dir,
        headless=False  # Set to True for production
    )

    # Test 1: Search and capture visual taxonomy
    print("\n📍 TEST 1: Search for 'LED strip lighting ideas'")
    print("-" * 80)

    search_result = await scraper.search_and_capture(
        query="LED strip lighting ideas",
        limit=20
    )

    print(f"✅ Search complete!")
    print(f"   - Pins found: {len(search_result.get('pins', []))}")
    print(f"   - Related searches: {search_result.get('related_searches', [])[:5]}")
    print(f"   - Screenshots saved: {len(search_result.get('screenshots', {}).get('sections', []))}")
    print(f"\n📸 Full page screenshot: {search_result['screenshots']['full_page']}")

    # Test 2: Analyze individual pin (if we got results)
    if search_result.get('pins') and len(search_result['pins']) > 0:
        first_pin = search_result['pins'][0]
        if first_pin.get('pin_url'):
            print(f"\n📍 TEST 2: Analyzing pin - {first_pin.get('title', 'Untitled')[:50]}")
            print("-" * 80)

            pin_analysis = await scraper.analyze_pin_details(first_pin['pin_url'])

            print(f"✅ Pin analysis complete!")
            print(f"   - Title: {pin_analysis['data'].get('title', 'N/A')[:60]}")
            print(f"   - Save count: {pin_analysis['success_indicators']['save_count']}")
            print(f"   - Comments: {pin_analysis['success_indicators']['comment_count']}")
            print(f"   - Tags: {pin_analysis['data'].get('tags', [])}")
            print(f"   - Has product link: {pin_analysis['success_indicators']['has_product_link']}")

            # Show job indicators
            print(f"\n🎯 Job Indicators:")
            job_indicators = pin_analysis.get('job_indicators', {})
            print(f"   - Keywords found: {job_indicators.get('description_keywords', [])}")

            comment_themes = job_indicators.get('comment_themes', {})
            print(f"   - Questions: {len(comment_themes.get('questions', []))}")
            print(f"   - Praise: {len(comment_themes.get('praise', []))}")
            print(f"   - Concerns: {len(comment_themes.get('concerns', []))}")
            print(f"   - How-to requests: {len(comment_themes.get('how_to', []))}")

            print(f"\n📸 Pin screenshot: {pin_analysis['screenshot']}")

    # Test 3: Board analysis (optional - requires manual board URL)
    # Uncomment and add a real board URL to test
    # print("\n📍 TEST 3: Analyzing board")
    # print("-" * 80)
    # board_result = await scraper.analyze_board("https://www.pinterest.com/username/board-name/")
    # print(f"✅ Board analysis complete!")
    # print(f"   - Total pins: {board_result['visual_taxonomy']['total_pins']}")

    await scraper.close()

    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)
    print(f"\n📁 Data saved to:")
    print(f"   - JSON cache: {cache_dir}")
    print(f"   - Screenshots: {screenshot_dir}")


if __name__ == "__main__":
    asyncio.run(main())
