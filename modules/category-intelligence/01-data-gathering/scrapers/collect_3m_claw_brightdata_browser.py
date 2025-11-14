#!/usr/bin/env python3
"""
Collect 3M Claw YouTube and TikTok videos using Bright Data Browser API.
Uses browser automation through Bright Data's proxy.
Target: 100+ videos combined.
"""

import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Bright Data Browser API endpoint
BRIGHTDATA_WSS = "wss://brd-customer-hl_694870e0-zone-category_intelligence_module:lk3i01g4z7u2@brd.superproxy.io:9222"

# YouTube search queries for 3M Claw (expanded for 100+ videos)
YOUTUBE_QUERIES = [
    "3M Claw hooks",
    "3M Claw review",
    "3M Claw drywall hangers",
    "3M Claw installation",
    "3M Claw picture hanger",
    "3M Claw garage organization",
    "3M Claw vs Command hooks",
    "3M Claw how to use",
    "3M Claw product review",
    "3M Claw unboxing",
    "3M Claw tutorial",
    "3M Claw hanging pictures",
    "3M Claw drywall repair",
    "3M Claw heavy duty",
]

# TikTok search queries for 3M Claw
TIKTOK_QUERIES = [
    "3M Claw",
    "3M Claw hooks",
    "3M Claw review",
]

async def scrape_youtube_search(page, query, max_results=50):
    """Scrape YouTube search results."""
    print(f"\n🎥 YouTube: Searching '{query}' (target: {max_results} videos)")

    try:
        # Go to YouTube search
        await page.goto(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        await page.wait_for_load_state('networkidle')

        # Scroll to load more videos (increased scrolling for more results)
        for _ in range(10):
            await page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            await asyncio.sleep(0.8)

        # Extract video data
        videos = await page.evaluate('''() => {
            const results = [];
            const videoElements = document.querySelectorAll('ytd-video-renderer');

            for (let i = 0; i < videoElements.length; i++) {
                const el = videoElements[i];
                const titleEl = el.querySelector('#video-title');
                const channelEl = el.querySelector('#channel-name a');
                const viewsEl = el.querySelector('#metadata-line span:first-child');
                const thumbnailEl = el.querySelector('img');

                if (titleEl && titleEl.href) {
                    results.push({
                        video_id: new URL(titleEl.href).searchParams.get('v'),
                        title: titleEl.textContent.trim(),
                        url: titleEl.href,
                        channel: channelEl ? channelEl.textContent.trim() : '',
                        views: viewsEl ? viewsEl.textContent.trim() : '',
                        thumbnail: thumbnailEl ? thumbnailEl.src : '',
                        platform: 'youtube'
                    });
                }
            }
            return results;
        }''')

        print(f"   ✓ Collected {len(videos)} videos")
        return videos[:max_results]

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return []

async def scrape_tiktok_search(page, query, max_results=20):
    """Scrape TikTok search results."""
    print(f"\n📱 TikTok: Searching '{query}' (target: {max_results} videos)")

    try:
        # Go to TikTok search
        await page.goto(f"https://www.tiktok.com/search?q={query.replace(' ', '%20')}")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)

        # Scroll to load more videos
        for _ in range(5):
            await page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            await asyncio.sleep(1)

        # Extract video data
        videos = await page.evaluate('''() => {
            const results = [];
            const videoElements = document.querySelectorAll('[data-e2e="search_top-item"]');

            for (let i = 0; i < videoElements.length; i++) {
                const el = videoElements[i];
                const linkEl = el.querySelector('a[href*="/video/"]');
                const titleEl = el.querySelector('[data-e2e="search-card-desc"]');
                const authorEl = el.querySelector('[data-e2e="search-card-user-unique-id"]');
                const viewsEl = el.querySelector('[data-e2e="search-card-like-container"]');

                if (linkEl) {
                    results.push({
                        video_id: linkEl.href.split('/video/')[1]?.split('?')[0] || '',
                        title: titleEl ? titleEl.textContent.trim() : '',
                        url: linkEl.href,
                        channel: authorEl ? authorEl.textContent.trim() : '',
                        views: viewsEl ? viewsEl.textContent.trim() : '',
                        platform: 'tiktok'
                    });
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
    """Collect 3M Claw videos from YouTube and TikTok."""

    print("="*70)
    print("3M CLAW VIDEO COLLECTION (BRIGHT DATA BROWSER API)")
    print("="*70)
    print(f"YouTube queries: {len(YOUTUBE_QUERIES)}")
    print(f"TikTok queries: {len(TIKTOK_QUERIES)}")
    print(f"Target: 100+ videos combined")
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

        # Collect YouTube videos
        print("\n" + "="*70)
        print("COLLECTING YOUTUBE VIDEOS")
        print("="*70)

        for i, query in enumerate(YOUTUBE_QUERIES, 1):
            print(f"[{i}/{len(YOUTUBE_QUERIES)}]", end="")
            videos = await scrape_youtube_search(page, query, max_results=50)
            for v in videos:
                v['search_query'] = query
            all_videos.extend(videos)

        youtube_count = len([v for v in all_videos if v['platform'] == 'youtube'])
        print(f"\n{'='*70}")
        print(f"YouTube total: {youtube_count} videos")
        print(f"{'='*70}")

        # Skip TikTok (navigation limit reached, focus on YouTube first)
        tiktok_count = 0
        print(f"\n{'='*70}")
        print(f"SKIPPING TIKTOK (Navigation limit - will run separate session)")
        print(f"{'='*70}")

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
    print(f"YouTube: {len([v for v in final_videos if v['platform'] == 'youtube'])}")
    print(f"TikTok: {len([v for v in final_videos if v['platform'] == 'tiktok'])}")
    print(f"Target met: {'✓ YES' if len(final_videos) >= 100 else f'✗ NO ({len(final_videos)}/100)'}")
    print(f"{'='*70}\n")

    # Save results
    if final_videos:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save combined
        output_file = f"outputs/3m_claw_all_videos_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump({
                'total_count': len(final_videos),
                'youtube_count': len([v for v in final_videos if v['platform'] == 'youtube']),
                'tiktok_count': len([v for v in final_videos if v['platform'] == 'tiktok']),
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
