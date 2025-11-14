#!/usr/bin/env python3
"""
Collect additional 3M Claw YouTube videos with expanded search terms.
Uses broader terms to capture videos that mention 3M Claw but may not have it in title.
Target: 100+ total unique videos.
"""

import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from pathlib import Path

# Bright Data Browser API endpoint
BRIGHTDATA_WSS = "wss://brd-customer-hl_694870e0-zone-category_intelligence_module:lk3i01g4z7u2@brd.superproxy.io:9222"

# Additional search queries (final round to reach 100+)
YOUTUBE_QUERIES = [
    "3M picture hangers",
    "3M drywall products",
    "claw hanger installation",
    "claw vs command",
    "drywall hanger comparison",
    "3M hanging solutions",
    "picture hanging tips",
    "drywall hook test",
    "best picture hangers",
    "3M home improvement",
    "heavy duty picture hanger",
    "picture hanging hack",
]

async def scrape_youtube_search(page, query, max_results=50):
    """Scrape YouTube search results."""
    print(f"\n🎥 YouTube: Searching '{query}' (target: {max_results} videos)")

    try:
        # Go to YouTube search
        await page.goto(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        await page.wait_for_load_state('networkidle')

        # Scroll to load more videos
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
                const descEl = el.querySelector('#description-text');

                if (titleEl && titleEl.href) {
                    const title = titleEl.textContent.trim();
                    const desc = descEl ? descEl.textContent.trim() : '';

                    // Only include if mentions "3M" or "Claw" in title/description
                    if (title.toLowerCase().includes('3m') ||
                        title.toLowerCase().includes('claw') ||
                        desc.toLowerCase().includes('3m claw')) {
                        results.push({
                            video_id: new URL(titleEl.href).searchParams.get('v'),
                            title: title,
                            url: titleEl.href,
                            channel: channelEl ? channelEl.textContent.trim() : '',
                            views: viewsEl ? viewsEl.textContent.trim() : '',
                            thumbnail: thumbnailEl ? thumbnailEl.src : '',
                            description: desc.substring(0, 200),
                            platform: 'youtube'
                        });
                    }
                }
            }
            return results;
        }''')

        print(f"   ✓ Collected {len(videos)} videos (filtered for 3M/Claw mentions)")
        return videos[:max_results]

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return []

async def main():
    """Collect additional 3M Claw YouTube videos."""

    print("="*70)
    print("3M CLAW EXPANDED YOUTUBE COLLECTION")
    print("="*70)
    print(f"Queries: {len(YOUTUBE_QUERIES)} (broader terms)")
    print(f"Filter: Only videos mentioning 3M or Claw")
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
        for i, query in enumerate(YOUTUBE_QUERIES, 1):
            print(f"[{i}/{len(YOUTUBE_QUERIES)}]", end="")
            videos = await scrape_youtube_search(page, query, max_results=50)
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
    print(f"EXPANDED COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total collected: {len(all_videos)} videos")
    print(f"After deduplication: {len(final_videos)} unique new videos")
    print(f"{'='*70}\n")

    # Load previous YouTube results
    output_dir = Path("outputs")
    previous_files = sorted(output_dir.glob("3m_claw_all_videos_*.json"))
    if previous_files:
        latest_file = previous_files[-1]
        print(f"Loading previous results from: {latest_file.name}")
        with open(latest_file, 'r') as f:
            previous_data = json.load(f)
            previous_videos = {v['video_id']: v for v in previous_data['videos']}

        # Combine with new videos
        combined_videos = previous_videos.copy()
        new_count = 0
        for video in final_videos:
            if video['video_id'] not in combined_videos:
                combined_videos[video['video_id']] = video
                new_count += 1

        final_combined = list(combined_videos.values())

        print(f"\nPrevious collection: {len(previous_videos)} videos")
        print(f"New unique videos: {new_count}")
        print(f"Combined total: {len(final_combined)} unique videos")
        print(f"Target met: {'✓ YES' if len(final_combined) >= 100 else f'✗ NO ({len(final_combined)}/100)'}")
    else:
        final_combined = final_videos
        new_count = len(final_videos)

    # Save results
    if final_combined:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"outputs/3m_claw_all_videos_COMBINED_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump({
                'total_count': len(final_combined),
                'youtube_count': len([v for v in final_combined if v['platform'] == 'youtube']),
                'tiktok_count': 0,
                'note': 'Combined from multiple collection runs with expanded search terms',
                'collected_at': timestamp,
                'videos': final_combined
            }, f, indent=2)

        print(f"\n✓ Saved combined results to: {output_file}")
        print(f"  Total unique videos: {len(final_combined)}")

        # Top channels
        channels = {}
        for v in final_combined:
            ch = v.get('channel', 'Unknown')
            if ch:
                channels[ch] = channels.get(ch, 0) + 1

        print(f"\n  Top channels:")
        for ch, count in sorted(channels.items(), key=lambda x: x[1], reverse=True)[:8]:
            print(f"    {ch}: {count} videos")
    else:
        print("\n✗ No videos collected")

if __name__ == "__main__":
    asyncio.run(main())
