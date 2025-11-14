#!/usr/bin/env python3
"""
TikTok scraper for garage organization and 3M Claw videos
Uses Playwright with visible browser
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

async def scrape_tiktok_search(search_term, max_videos=50):
    """Scrape TikTok search results"""

    print(f"\n🔍 Searching TikTok: {search_term}")
    print(f"   Target: {max_videos} videos")
    print(f"   Opening browser in 5 seconds...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome"
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        # Navigate to TikTok search
        search_url = f"https://www.tiktok.com/search?q={search_term.replace(' ', '%20')}"
        await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)

        print(f"\n✓ Page loaded. Waiting 10 seconds for initial content...")
        await page.wait_for_timeout(10000)

        all_videos = []
        scroll_count = 0
        max_scrolls = max_videos // 10  # ~10 videos per screen

        print(f"\n📜 Scrolling to load ~{max_videos} videos...")

        for scroll in range(max_scrolls):
            # Extract videos
            videos = await page.evaluate("""() => {
                const items = [];

                // TikTok uses different selectors, try multiple approaches
                const videoCards = document.querySelectorAll('[data-e2e="search_top-item"]');

                videoCards.forEach((card, idx) => {
                    try {
                        // Get video link
                        const link = card.querySelector('a');
                        const url = link ? link.href : null;

                        // Get description/caption
                        const descEl = card.querySelector('[data-e2e="search-card-desc"]');
                        const desc = descEl ? descEl.textContent.trim() : null;

                        // Get author
                        const authorEl = card.querySelector('[data-e2e="search-card-user-unique-id"]');
                        const author = authorEl ? authorEl.textContent.trim() : null;

                        // Get stats (likes, views, etc)
                        const statsEls = card.querySelectorAll('[data-e2e="search-card-like-container"]');
                        let likes = null;
                        if (statsEls.length > 0) {
                            const likesText = statsEls[0].textContent;
                            likes = likesText;
                        }

                        if (url) {
                            items.push({
                                url: url,
                                description: desc,
                                author: author,
                                likes: likes,
                                scraped_at: new Date().toISOString()
                            });
                        }
                    } catch (e) {
                        console.error('Error parsing video:', e);
                    }
                });

                return items;
            }""")

            new_videos = [v for v in videos if v['url'] not in [av['url'] for av in all_videos]]
            all_videos.extend(new_videos)

            print(f"   Scroll {scroll + 1}/{max_scrolls}: Found {len(new_videos)} new videos (total: {len(all_videos)})")

            if len(all_videos) >= max_videos:
                break

            # Scroll down
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            scroll_count += 1

        await browser.close()

        print(f"\n✓ Collected {len(all_videos)} videos for '{search_term}'")

        # Add metadata
        for v in all_videos:
            v['search_term'] = search_term
            v['platform'] = 'TikTok'

        return all_videos


async def main():
    print("=" * 80)
    print("TIKTOK VIDEO SCRAPING")
    print("=" * 80)

    # Search queries
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

    # Collect garage organization videos
    print("\n" + "=" * 80)
    print("PHASE 1: GARAGE ORGANIZATION VIDEOS")
    print("=" * 80)
    print("Target: 300+ videos")

    garage_videos = []
    videos_per_query = 60  # 6 queries × 60 = 360 videos

    for query in garage_queries:
        videos = await scrape_tiktok_search(query, max_videos=videos_per_query)
        garage_videos.extend(videos)

        # Save checkpoint
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        checkpoint_file = OUTPUT_DIR / f"tiktok_garage_checkpoint_{timestamp}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump({
                'platform': 'TikTok',
                'category': 'garage_organization',
                'collected_at': datetime.now().isoformat(),
                'video_count': len(garage_videos),
                'videos': garage_videos
            }, f, indent=2)
        print(f"\n💾 Checkpoint: {len(garage_videos)} garage videos saved")

    # Deduplicate garage videos
    unique_garage = {v['url']: v for v in garage_videos}
    garage_videos = list(unique_garage.values())

    print(f"\n✓ Total unique garage videos: {len(garage_videos)}")

    # Collect 3M Claw videos
    print("\n" + "=" * 80)
    print("PHASE 2: 3M CLAW VIDEOS")
    print("=" * 80)
    print("Target: 400 videos (to filter to ~100 relevant)")

    claw_videos = []
    videos_per_query = 50  # 8 queries × 50 = 400 videos

    for query in claw_queries:
        videos = await scrape_tiktok_search(query, max_videos=videos_per_query)
        claw_videos.extend(videos)

        # Save checkpoint
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        checkpoint_file = OUTPUT_DIR / f"tiktok_3m_claw_checkpoint_{timestamp}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump({
                'platform': 'TikTok',
                'brand': '3M Claw',
                'collected_at': datetime.now().isoformat(),
                'video_count': len(claw_videos),
                'videos': claw_videos
            }, f, indent=2)
        print(f"\n💾 Checkpoint: {len(claw_videos)} 3M Claw videos saved")

    # Deduplicate 3M Claw videos
    unique_claw = {v['url']: v for v in claw_videos}
    claw_videos = list(unique_claw.values())

    # Filter for relevant 3M Claw content
    relevant_claw = [
        v for v in claw_videos
        if v.get('description') and (
            '3m' in v['description'].lower() and 'claw' in v['description'].lower()
        ) or '3m claw' in v.get('search_term', '').lower()
    ]

    print(f"\n✓ Total unique 3M Claw videos: {len(claw_videos)}")
    print(f"✓ Relevant 3M Claw videos: {len(relevant_claw)}")

    # Save final results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Garage organization final
    garage_file = OUTPUT_DIR / f"tiktok_garage_organization_{timestamp}.json"
    with open(garage_file, 'w') as f:
        json.dump({
            'platform': 'TikTok',
            'category': 'garage_organization',
            'collected_at': datetime.now().isoformat(),
            'search_queries': garage_queries,
            'video_count': len(garage_videos),
            'videos': garage_videos
        }, f, indent=2)

    # 3M Claw final
    claw_file = OUTPUT_DIR / f"tiktok_3m_claw_{timestamp}.json"
    with open(claw_file, 'w') as f:
        json.dump({
            'platform': 'TikTok',
            'brand': '3M Claw',
            'collected_at': datetime.now().isoformat(),
            'search_queries': claw_queries,
            'total_videos': len(claw_videos),
            'relevant_videos': len(relevant_claw),
            'videos': claw_videos
        }, f, indent=2)

    print("\n" + "=" * 80)
    print("TIKTOK SCRAPING COMPLETE")
    print("=" * 80)
    print(f"\n📊 Results:")
    print(f"  Garage Organization: {len(garage_videos)} videos")
    print(f"  3M Claw (all): {len(claw_videos)} videos")
    print(f"  3M Claw (relevant): {len(relevant_claw)} videos")
    print(f"\n💾 Files saved:")
    print(f"  {garage_file}")
    print(f"  {claw_file}")


if __name__ == "__main__":
    asyncio.run(main())
