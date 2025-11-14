#!/usr/bin/env python3
"""
TikTok scraper with manual login
Opens browser, waits for user to log in, then scrapes
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "social_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def scrape_tiktok_with_login():
    """Scrape TikTok after user logs in"""

    print("=" * 80)
    print("TIKTOK VIDEO SCRAPING - With User Login")
    print("=" * 80)
    print("\n🌐 Opening TikTok...")
    print("   Please log in to TikTok when the browser opens.")
    print("   You have 2 minutes to complete the login.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome"
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        # Navigate to TikTok
        await page.goto("https://www.tiktok.com", wait_until="domcontentloaded")

        print("\n✓ Browser opened!")
        print("   1. Log in to TikTok")
        print("   2. You have 2 minutes to complete the login")
        print("   3. Scraping will begin automatically in 2 minutes")

        # Wait for user to log in (2 minutes)
        print("\n⏳ Waiting 120 seconds for you to log in...")
        for remaining in range(120, 0, -10):
            print(f"   {remaining} seconds remaining...")
            await asyncio.sleep(10)
        print("\n✓ Starting scraping now!")

        # Define search queries
        garage_queries = [
            "garage organization",
            "garage storage ideas",
            "garage organization ideas",
            "organize garage",
            "garage hooks",
            "garage shelving"
        ]

        claw_queries = [
            "3M Claw",
            "3M Claw hooks",
            "3M Claw drywall",
            "3M Claw review",
            "3M Claw installation",
            "3M Claw vs Command",
            "3M Claw test",
            "3M Claw hanging"
        ]

        all_garage_videos = []
        all_claw_videos = []

        # PHASE 1: Garage Organization
        print("\n" + "=" * 80)
        print("PHASE 1: GARAGE ORGANIZATION VIDEOS")
        print("=" * 80)

        for query in garage_queries:
            print(f"\n🔍 Searching: {query}")

            search_url = f"https://www.tiktok.com/search?q={query.replace(' ', '%20')}"
            await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(5000)

            # Scroll and collect videos
            videos_collected = 0
            target = 60

            for scroll in range(6):  # 6 scrolls
                # Extract video data
                videos = await page.evaluate("""() => {
                    const items = [];

                    // Try multiple selector approaches
                    let videoElements = document.querySelectorAll('[data-e2e="search_top-item"]');

                    // Fallback: Try finding video links
                    if (videoElements.length === 0) {
                        videoElements = document.querySelectorAll('a[href*="/video/"]');
                    }

                    videoElements.forEach(elem => {
                        try {
                            let url = null;
                            let description = null;
                            let author = null;

                            // Get URL
                            if (elem.href) {
                                url = elem.href;
                            } else {
                                const linkEl = elem.querySelector('a');
                                url = linkEl ? linkEl.href : null;
                            }

                            // Get description from various possible locations
                            const descSelectors = [
                                '[data-e2e="search-card-desc"]',
                                '[data-e2e="video-desc"]',
                                '.video-meta-caption',
                                'h1', 'h2', 'h3'
                            ];

                            for (const sel of descSelectors) {
                                const descEl = elem.querySelector(sel);
                                if (descEl && descEl.textContent.trim()) {
                                    description = descEl.textContent.trim();
                                    break;
                                }
                            }

                            // Get author
                            const authorSelectors = [
                                '[data-e2e="search-card-user-unique-id"]',
                                '[data-e2e="video-author-uniqueid"]',
                                '.author-uniqueId'
                            ];

                            for (const sel of authorSelectors) {
                                const authorEl = elem.querySelector(sel);
                                if (authorEl && authorEl.textContent.trim()) {
                                    author = authorEl.textContent.trim();
                                    break;
                                }
                            }

                            if (url && url.includes('/video/')) {
                                items.push({
                                    url: url,
                                    description: description,
                                    author: author
                                });
                            }
                        } catch (e) {
                            // Skip errors
                        }
                    });

                    return items;
                }""")

                # Add new videos
                new_videos = [v for v in videos if v['url'] not in [av['url'] for av in all_garage_videos]]
                all_garage_videos.extend(new_videos)
                videos_collected += len(new_videos)

                print(f"   Scroll {scroll + 1}/6: +{len(new_videos)} videos (total: {len(all_garage_videos)})")

                if videos_collected >= target:
                    break

                # Scroll down
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(3000)

            # Add metadata
            for v in all_garage_videos[-videos_collected:]:
                v['search_term'] = query
                v['platform'] = 'TikTok'
                v['scraped_at'] = datetime.now().isoformat()

            # Save checkpoint
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            checkpoint_file = OUTPUT_DIR / f"tiktok_garage_checkpoint_{timestamp}.json"
            with open(checkpoint_file, 'w') as f:
                json.dump({
                    'platform': 'TikTok',
                    'category': 'garage_organization',
                    'collected_at': datetime.now().isoformat(),
                    'video_count': len(all_garage_videos),
                    'videos': all_garage_videos
                }, f, indent=2)
            print(f"   💾 Checkpoint: {len(all_garage_videos)} garage videos saved")

        # PHASE 2: 3M Claw
        print("\n" + "=" * 80)
        print("PHASE 2: 3M CLAW VIDEOS")
        print("=" * 80)

        for query in claw_queries:
            print(f"\n🔍 Searching: {query}")

            search_url = f"https://www.tiktok.com/search?q={query.replace(' ', '%20')}"
            await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(5000)

            # Scroll and collect videos
            videos_collected = 0
            target = 50

            for scroll in range(5):  # 5 scrolls
                # Extract video data (same logic as above)
                videos = await page.evaluate("""() => {
                    const items = [];
                    let videoElements = document.querySelectorAll('[data-e2e="search_top-item"]');
                    if (videoElements.length === 0) {
                        videoElements = document.querySelectorAll('a[href*="/video/"]');
                    }

                    videoElements.forEach(elem => {
                        try {
                            let url = null;
                            let description = null;
                            let author = null;

                            if (elem.href) {
                                url = elem.href;
                            } else {
                                const linkEl = elem.querySelector('a');
                                url = linkEl ? linkEl.href : null;
                            }

                            const descSelectors = [
                                '[data-e2e="search-card-desc"]',
                                '[data-e2e="video-desc"]',
                                '.video-meta-caption',
                                'h1', 'h2', 'h3'
                            ];

                            for (const sel of descSelectors) {
                                const descEl = elem.querySelector(sel);
                                if (descEl && descEl.textContent.trim()) {
                                    description = descEl.textContent.trim();
                                    break;
                                }
                            }

                            const authorSelectors = [
                                '[data-e2e="search-card-user-unique-id"]',
                                '[data-e2e="video-author-uniqueid"]',
                                '.author-uniqueId'
                            ];

                            for (const sel of authorSelectors) {
                                const authorEl = elem.querySelector(sel);
                                if (authorEl && authorEl.textContent.trim()) {
                                    author = authorEl.textContent.trim();
                                    break;
                                }
                            }

                            if (url && url.includes('/video/')) {
                                items.push({
                                    url: url,
                                    description: description,
                                    author: author
                                });
                            }
                        } catch (e) {}
                    });

                    return items;
                }""")

                new_videos = [v for v in videos if v['url'] not in [av['url'] for av in all_claw_videos]]
                all_claw_videos.extend(new_videos)
                videos_collected += len(new_videos)

                print(f"   Scroll {scroll + 1}/5: +{len(new_videos)} videos (total: {len(all_claw_videos)})")

                if videos_collected >= target:
                    break

                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(3000)

            # Add metadata
            for v in all_claw_videos[-videos_collected:]:
                v['search_term'] = query
                v['platform'] = 'TikTok'
                v['brand'] = '3M Claw'
                v['scraped_at'] = datetime.now().isoformat()

            # Save checkpoint
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            checkpoint_file = OUTPUT_DIR / f"tiktok_3m_claw_checkpoint_{timestamp}.json"
            with open(checkpoint_file, 'w') as f:
                json.dump({
                    'platform': 'TikTok',
                    'brand': '3M Claw',
                    'collected_at': datetime.now().isoformat(),
                    'video_count': len(all_claw_videos),
                    'videos': all_claw_videos
                }, f, indent=2)
            print(f"   💾 Checkpoint: {len(all_claw_videos)} 3M Claw videos saved")

        await browser.close()

        # Filter relevant 3M Claw videos
        relevant_claw = [
            v for v in all_claw_videos
            if v.get('description') and (
                ('3m' in v['description'].lower() and 'claw' in v['description'].lower()) or
                '3m claw' in v.get('search_term', '').lower()
            )
        ]

        # Save final results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Garage final
        garage_file = OUTPUT_DIR / f"tiktok_garage_organization_FINAL_{timestamp}.json"
        with open(garage_file, 'w') as f:
            json.dump({
                'platform': 'TikTok',
                'category': 'garage_organization',
                'collected_at': datetime.now().isoformat(),
                'search_queries': garage_queries,
                'video_count': len(all_garage_videos),
                'videos': all_garage_videos
            }, f, indent=2)

        # 3M Claw final
        claw_file = OUTPUT_DIR / f"tiktok_3m_claw_FINAL_{timestamp}.json"
        with open(claw_file, 'w') as f:
            json.dump({
                'platform': 'TikTok',
                'brand': '3M Claw',
                'collected_at': datetime.now().isoformat(),
                'search_queries': claw_queries,
                'total_videos': len(all_claw_videos),
                'relevant_videos': len(relevant_claw),
                'videos': all_claw_videos
            }, f, indent=2)

        print("\n" + "=" * 80)
        print("TIKTOK SCRAPING COMPLETE")
        print("=" * 80)
        print(f"\n📊 Results:")
        print(f"  Garage Organization: {len(all_garage_videos)} videos")
        print(f"  3M Claw (all): {len(all_claw_videos)} videos")
        print(f"  3M Claw (relevant): {len(relevant_claw)} videos")
        print(f"\n💾 Files saved:")
        print(f"  {garage_file}")
        print(f"  {claw_file}")


async def main():
    await scrape_tiktok_with_login()


if __name__ == "__main__":
    asyncio.run(main())
