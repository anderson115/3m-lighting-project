#!/usr/bin/env python3
"""
Massive 3M Claw video collection across multiple platforms.
Target: 500+ videos total (expecting ~30% relevancy = 150+ relevant videos)
Platforms: YouTube, Instagram Reels, Facebook, Pinterest
"""

import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from pathlib import Path

# Bright Data Browser API endpoint
BRIGHTDATA_WSS = "wss://brd-customer-hl_694870e0-zone-category_intelligence_module:lk3i01g4z7u2@brd.superproxy.io:9222"

# Expanded YouTube search queries (50+ variations)
YOUTUBE_QUERIES = [
    # Direct 3M Claw searches
    "3M Claw hooks", "3M Claw review", "3M Claw drywall hangers", "3M Claw installation",
    "3M Claw picture hanger", "3M Claw garage organization", "3M Claw vs Command hooks",
    "3M Claw how to use", "3M Claw product review", "3M Claw unboxing",
    "3M Claw tutorial", "3M Claw hanging pictures", "3M Claw drywall repair",
    "3M Claw heavy duty", "3M Claw test", "3M Claw fail", "3M Claw success",

    # Brand + category searches
    "3M picture hangers", "3M drywall products", "3M hanging solutions",
    "3M home improvement", "3M DIY products", "3M wall mounting",

    # Claw + variations
    "claw hanger installation", "claw vs command", "claw drywall hanger",
    "claw picture hanger review", "claw hook review", "claw hanger test",

    # Problem/solution searches
    "drywall hanger comparison", "picture hanging tips", "drywall hook test",
    "best picture hangers", "heavy duty picture hanger", "picture hanging hack",
    "no drill picture hanging", "temporary drywall hanger", "removable drywall hook",
    "drywall picture hanger review", "best drywall hangers 2024", "drywall anchor alternative",
    "picture hanging without nails", "garage organization drywall", "picture hanging system drywall",

    # Use case searches
    "hang pictures on drywall", "heavy picture drywall", "garage tool organizer",
    "rental friendly hanging", "apartment picture hanging", "drywall mounting solutions",
    "hang shelves without drilling", "drywall organization", "wall storage no nails",

    # Product comparison
    "picture hanger comparison", "wall hook comparison", "drywall anchor comparison",
    "command vs monkey hook", "picture hanger test", "wall mounting options",
]

# Instagram Reels queries (shorter, hashtag-style)
INSTAGRAM_QUERIES = [
    "3M Claw", "3M Claw hooks", "3M Claw drywall", "claw drywall hanger",
    "drywall picture hanger", "no drill hanging", "rental friendly decor",
    "apartment organization", "garage organization", "picture hanging hack",
]

# Facebook queries (groups and videos)
FACEBOOK_QUERIES = [
    "3M Claw review", "3M Claw drywall hanger", "picture hanging drywall",
    "DIY picture hanging", "garage organization tips", "rental apartment hacks",
]

# Pinterest queries (DIY heavy)
PINTEREST_QUERIES = [
    "3M Claw picture hanger", "drywall hanging solutions", "picture hanging ideas",
    "no drill wall mounting", "rental apartment organization", "garage organization ideas",
]

async def scrape_youtube(page, query, max_results=100):
    """Scrape YouTube search results."""
    print(f"  🎥 YouTube: '{query[:40]}'...", end=" ")
    try:
        await page.goto(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}", timeout=45000)
        await page.wait_for_load_state('networkidle', timeout=45000)

        # Aggressive scrolling for more results
        for _ in range(15):
            await page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            await asyncio.sleep(0.6)

        videos = await page.evaluate('''() => {
            const results = [];
            const videoElements = document.querySelectorAll('ytd-video-renderer');

            for (let el of videoElements) {
                const titleEl = el.querySelector('#video-title');
                const channelEl = el.querySelector('#channel-name a');
                const descEl = el.querySelector('#description-text');

                if (titleEl && titleEl.href) {
                    results.push({
                        video_id: new URL(titleEl.href).searchParams.get('v'),
                        title: titleEl.textContent.trim(),
                        url: titleEl.href,
                        channel: channelEl ? channelEl.textContent.trim() : '',
                        description: descEl ? descEl.textContent.trim().substring(0, 300) : '',
                        platform: 'youtube',
                        search_query: ''
                    });
                }
            }
            return results;
        }''')

        for v in videos:
            v['search_query'] = query

        print(f"✓ {len(videos)}")
        return videos[:max_results]
    except Exception as e:
        print(f"✗ {str(e)[:50]}")
        return []

async def scrape_instagram(page, query, max_results=50):
    """Scrape Instagram Reels search results."""
    print(f"  📸 Instagram: '{query[:40]}'...", end=" ")
    try:
        await page.goto(f"https://www.instagram.com/explore/tags/{query.replace(' ', '').lower()}/", timeout=60000)
        await asyncio.sleep(3)

        # Scroll for more posts
        for _ in range(8):
            await page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            await asyncio.sleep(1)

        videos = await page.evaluate('''() => {
            const results = [];
            const links = document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]');

            for (let link of links) {
                const href = link.href;
                const id = href.split('/')[4];
                if (id && href.includes('instagram.com')) {
                    results.push({
                        video_id: id,
                        title: '',
                        url: href,
                        channel: '',
                        description: '',
                        platform: 'instagram',
                        search_query: ''
                    });
                }
            }
            return results;
        }''')

        for v in videos:
            v['search_query'] = query

        print(f"✓ {len(videos)}")
        return videos[:max_results]
    except Exception as e:
        print(f"✗ {str(e)[:50]}")
        return []

async def scrape_facebook(page, query, max_results=30):
    """Scrape Facebook videos."""
    print(f"  📘 Facebook: '{query[:40]}'...", end=" ")
    try:
        await page.goto(f"https://www.facebook.com/search/videos/?q={query.replace(' ', '%20')}", timeout=60000)
        await asyncio.sleep(4)

        # Scroll for more videos
        for _ in range(5):
            await page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            await asyncio.sleep(1.5)

        videos = await page.evaluate('''() => {
            const results = [];
            const links = document.querySelectorAll('a[href*="/watch/"], a[href*="/videos/"]');

            for (let link of links) {
                const href = link.href;
                const id = href.split('/').pop().split('?')[0];
                if (id && href.includes('facebook.com')) {
                    results.push({
                        video_id: id,
                        title: link.textContent.trim().substring(0, 200),
                        url: href,
                        channel: '',
                        description: '',
                        platform: 'facebook',
                        search_query: ''
                    });
                }
            }
            return results;
        }''')

        for v in videos:
            v['search_query'] = query

        print(f"✓ {len(videos)}")
        return videos[:max_results]
    except Exception as e:
        print(f"✗ {str(e)[:50]}")
        return []

async def scrape_pinterest(page, query, max_results=50):
    """Scrape Pinterest video pins."""
    print(f"  📌 Pinterest: '{query[:40]}'...", end=" ")
    try:
        await page.goto(f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}", timeout=60000)
        await asyncio.sleep(3)

        # Scroll for more pins
        for _ in range(8):
            await page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            await asyncio.sleep(1)

        videos = await page.evaluate('''() => {
            const results = [];
            const links = document.querySelectorAll('a[href*="/pin/"]');

            for (let link of links) {
                const href = link.href;
                const id = href.split('/pin/')[1]?.split('/')[0];
                if (id && href.includes('pinterest.com')) {
                    // Check if it's a video pin
                    const parentDiv = link.closest('div[data-test-id="pin"]');
                    const hasVideo = parentDiv && parentDiv.querySelector('video');

                    results.push({
                        video_id: id,
                        title: link.getAttribute('title') || '',
                        url: href,
                        channel: '',
                        description: '',
                        platform: hasVideo ? 'pinterest_video' : 'pinterest_image',
                        search_query: ''
                    });
                }
            }
            return results;
        }''')

        for v in videos:
            v['search_query'] = query

        print(f"✓ {len(videos)}")
        return videos[:max_results]
    except Exception as e:
        print(f"✗ {str(e)[:50]}")
        return []

async def main():
    """Collect videos from all platforms."""

    print("="*70)
    print("MASSIVE 3M CLAW VIDEO COLLECTION")
    print("="*70)
    print(f"YouTube queries: {len(YOUTUBE_QUERIES)}")
    print(f"Instagram queries: {len(INSTAGRAM_QUERIES)}")
    print(f"Facebook queries: {len(FACEBOOK_QUERIES)}")
    print(f"Pinterest queries: {len(PINTEREST_QUERIES)}")
    print(f"Total queries: {len(YOUTUBE_QUERIES) + len(INSTAGRAM_QUERIES) + len(FACEBOOK_QUERIES) + len(PINTEREST_QUERIES)}")
    print(f"Target: 500+ videos total")
    print("="*70)
    print()

    all_videos = []

    async with async_playwright() as p:
        print("Connecting to Bright Data Browser API...")
        browser = await p.chromium.connect_over_cdp(BRIGHTDATA_WSS)

        if browser.contexts:
            context = browser.contexts[0]
            page = await context.new_page()
        else:
            context = await browser.new_context()
            page = await context.new_page()

        # YouTube collection
        print("\n" + "="*70)
        print("COLLECTING YOUTUBE VIDEOS")
        print("="*70)
        for i, query in enumerate(YOUTUBE_QUERIES, 1):
            print(f"[{i}/{len(YOUTUBE_QUERIES)}]", end=" ")
            videos = await scrape_youtube(page, query, max_results=100)
            all_videos.extend(videos)

        youtube_count = len([v for v in all_videos if v['platform'] == 'youtube'])
        print(f"\nYouTube total: {youtube_count} videos")

        # Instagram collection
        print("\n" + "="*70)
        print("COLLECTING INSTAGRAM REELS")
        print("="*70)
        for i, query in enumerate(INSTAGRAM_QUERIES, 1):
            print(f"[{i}/{len(INSTAGRAM_QUERIES)}]", end=" ")
            videos = await scrape_instagram(page, query, max_results=50)
            all_videos.extend(videos)

        instagram_count = len([v for v in all_videos if v['platform'] == 'instagram'])
        print(f"\nInstagram total: {instagram_count} posts")

        # Facebook collection
        print("\n" + "="*70)
        print("COLLECTING FACEBOOK VIDEOS")
        print("="*70)
        for i, query in enumerate(FACEBOOK_QUERIES, 1):
            print(f"[{i}/{len(FACEBOOK_QUERIES)}]", end=" ")
            videos = await scrape_facebook(page, query, max_results=30)
            all_videos.extend(videos)

        facebook_count = len([v for v in all_videos if v['platform'] == 'facebook'])
        print(f"\nFacebook total: {facebook_count} videos")

        # Pinterest collection
        print("\n" + "="*70)
        print("COLLECTING PINTEREST PINS")
        print("="*70)
        for i, query in enumerate(PINTEREST_QUERIES, 1):
            print(f"[{i}/{len(PINTEREST_QUERIES)}]", end=" ")
            videos = await scrape_pinterest(page, query, max_results=50)
            all_videos.extend(videos)

        pinterest_count = len([v for v in all_videos if v['platform'].startswith('pinterest')])
        print(f"\nPinterest total: {pinterest_count} pins")

        await browser.close()

    # Remove duplicates
    unique_videos = {}
    for video in all_videos:
        key = f"{video['platform']}_{video['video_id']}"
        if video['video_id'] and key not in unique_videos:
            unique_videos[key] = video

    final_videos = list(unique_videos.values())

    # Platform breakdown
    platform_counts = {}
    for v in final_videos:
        platform = v['platform']
        platform_counts[platform] = platform_counts.get(platform, 0) + 1

    print(f"\n{'='*70}")
    print(f"MASSIVE COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total collected: {len(all_videos)} items")
    print(f"After deduplication: {len(final_videos)} unique items")
    print(f"\nPlatform breakdown:")
    for platform, count in sorted(platform_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {platform}: {count}")
    print(f"{'='*70}\n")

    # Save results
    if final_videos:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"outputs/3m_claw_MASSIVE_multiplatform_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump({
                'total_count': len(final_videos),
                'platform_counts': platform_counts,
                'note': 'Multi-platform collection (YouTube, Instagram, Facebook, Pinterest)',
                'collected_at': timestamp,
                'videos': final_videos
            }, f, indent=2)

        print(f"✓ Saved to: {output_file}")
        print(f"  Total unique items: {len(final_videos)}")
    else:
        print("\n✗ No videos collected")

if __name__ == "__main__":
    asyncio.run(main())
