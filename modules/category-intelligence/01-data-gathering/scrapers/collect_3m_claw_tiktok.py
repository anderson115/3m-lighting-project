#!/usr/bin/env python3
"""
Collect 3M Claw TikTok videos using Bright Data Browser API.
Separate session to avoid navigation limits.
Target: 30+ TikTok videos to combine with YouTube results.
"""

import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Bright Data Browser API endpoint
BRIGHTDATA_WSS = "wss://brd-customer-hl_694870e0-zone-category_intelligence_module:lk3i01g4z7u2@brd.superproxy.io:9222"

# TikTok search queries for 3M Claw
TIKTOK_QUERIES = [
    "3M Claw",
    "3M Claw hooks",
    "3M Claw review",
    "3M Claw drywall",
    "3M Claw picture hanger",
    "3M Claw tutorial",
]

async def scrape_tiktok_search(page, query, max_results=20):
    """Scrape TikTok search results."""
    print(f"\n📱 TikTok: Searching '{query}' (target: {max_results} videos)")

    try:
        # Go to TikTok search
        await page.goto(f"https://www.tiktok.com/search?q={query.replace(' ', '%20')}", timeout=60000)
        await page.wait_for_load_state('networkidle', timeout=60000)
        await asyncio.sleep(5)

        # Scroll to load more videos
        for _ in range(8):
            await page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            await asyncio.sleep(1.5)

        # Extract video data
        videos = await page.evaluate('''() => {
            const results = [];

            // Try multiple selectors for TikTok video elements
            const selectors = [
                '[data-e2e="search_top-item"]',
                '[data-e2e="search-card-item"]',
                'div[data-e2e*="search"]',
                'a[href*="/video/"]'
            ];

            let videoElements = [];
            for (const selector of selectors) {
                const elements = document.querySelectorAll(selector);
                if (elements.length > 0) {
                    videoElements = elements;
                    break;
                }
            }

            for (let i = 0; i < videoElements.length; i++) {
                const el = videoElements[i];
                const linkEl = el.querySelector('a[href*="/video/"]') || (el.tagName === 'A' ? el : null);
                const titleEl = el.querySelector('[data-e2e="search-card-desc"]') || el.querySelector('div[class*="desc"]');
                const authorEl = el.querySelector('[data-e2e="search-card-user-unique-id"]') || el.querySelector('a[class*="author"]');

                if (linkEl && linkEl.href) {
                    const videoId = linkEl.href.split('/video/')[1]?.split('?')[0] || '';
                    if (videoId) {
                        results.push({
                            video_id: videoId,
                            title: titleEl ? titleEl.textContent.trim() : '',
                            url: linkEl.href,
                            channel: authorEl ? authorEl.textContent.trim() : '',
                            views: '',
                            platform: 'tiktok'
                        });
                    }
                }
            }
            return results;
        }''')

        print(f"   ✓ Collected {len(videos)} videos")
        return videos[:max_results]

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return []

async def main():
    """Collect 3M Claw TikTok videos."""

    print("="*70)
    print("3M CLAW TIKTOK COLLECTION (BRIGHT DATA BROWSER API)")
    print("="*70)
    print(f"TikTok queries: {len(TIKTOK_QUERIES)}")
    print(f"Target: 30+ videos")
    print()

    all_videos = []

    async with async_playwright() as p:
        print("Connecting to Bright Data Browser API...")
        browser = await p.chromium.connect_over_cdp(BRIGHTDATA_WSS)

        # Create new context and page
        if browser.contexts:
            context = browser.contexts[0]
            page = await context.new_page()
        else:
            context = await browser.new_context()
            page = await context.new_page()

        # Collect TikTok videos
        print("\n" + "="*70)
        print("COLLECTING TIKTOK VIDEOS")
        print("="*70)

        for i, query in enumerate(TIKTOK_QUERIES, 1):
            print(f"[{i}/{len(TIKTOK_QUERIES)}]", end="")
            videos = await scrape_tiktok_search(page, query, max_results=20)
            for v in videos:
                v['search_query'] = query
            all_videos.extend(videos)

        await browser.close()

    # Remove duplicates by video_id
    unique_videos = {}
    for video in all_videos:
        vid_id = video.get('video_id')
        if vid_id and vid_id not in unique_videos:
            unique_videos[vid_id] = video

    final_videos = list(unique_videos.values())

    print(f"\n{'='*70}")
    print(f"COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total collected: {len(all_videos)} videos")
    print(f"After deduplication: {len(final_videos)} unique videos")
    print(f"{'='*70}\n")

    # Save results
    if final_videos:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"outputs/3m_claw_tiktok_videos_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump({
                'total_count': len(final_videos),
                'platform': 'tiktok',
                'collected_at': timestamp,
                'videos': final_videos
            }, f, indent=2)

        print(f"✓ Saved to: {output_file}")
        print(f"  Total videos: {len(final_videos)}")

        # Top channels
        channels = {}
        for v in final_videos:
            ch = v.get('channel', 'Unknown')
            if ch:
                channels[ch] = channels.get(ch, 0) + 1

        print(f"\n  Top channels:")
        for ch, count in sorted(channels.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"    {ch}: {count} videos")
    else:
        print("\n✗ No videos collected")

if __name__ == "__main__":
    asyncio.run(main())
