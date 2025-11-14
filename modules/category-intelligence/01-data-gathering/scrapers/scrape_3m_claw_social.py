#!/usr/bin/env python3
"""
Scrape social video content for 3M Claw brand
Sources: YouTube, TikTok, Reddit
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# Bright Data endpoint
BRIGHTDATA_ENDPOINT = "wss://brd-customer-hl_694870e0-zone-category_intelligence_module:lk3i01g4z7u2@brd.superproxy.io:9222"

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "social_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class SocialVideoScraper:
    def __init__(self, use_brightdata=True):
        self.use_brightdata = use_brightdata

    async def scrape_youtube(self, search_queries):
        """Scrape YouTube videos about 3M Claw"""
        print("\n🎥 Scraping YouTube for 3M Claw videos...")

        async with async_playwright() as p:
            if self.use_brightdata:
                browser = await p.chromium.connect_over_cdp(BRIGHTDATA_ENDPOINT)
            else:
                browser = await p.chromium.launch(headless=True)

            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            all_videos = []

            for query in search_queries:
                print(f"  Searching: {query}")

                try:
                    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                    await page.goto(search_url, wait_until="networkidle", timeout=60000)
                    await page.wait_for_timeout(3000)

                    # Scroll to load more
                    for _ in range(3):
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(2000)

                    videos = await page.evaluate("""() => {
                        const items = [];
                        const videoElements = document.querySelectorAll('ytd-video-renderer');

                        videoElements.forEach(video => {
                            try {
                                const titleEl = video.querySelector('#video-title');
                                const channelEl = video.querySelector('#channel-name a');
                                const viewsEl = video.querySelector('#metadata-line span:first-child');
                                const dateEl = video.querySelector('#metadata-line span:nth-child(2)');
                                const durationEl = video.querySelector('ytd-thumbnail-overlay-time-status-renderer span');
                                const linkEl = video.querySelector('#video-title');
                                const thumbnailEl = video.querySelector('img');

                                if (titleEl && linkEl) {
                                    items.push({
                                        title: titleEl.textContent.trim(),
                                        url: 'https://www.youtube.com' + linkEl.getAttribute('href'),
                                        videoId: linkEl.getAttribute('href')?.match(/v=([^&]+)/)?.[1],
                                        channel: channelEl ? channelEl.textContent.trim() : null,
                                        views: viewsEl ? viewsEl.textContent.trim() : null,
                                        publishedDate: dateEl ? dateEl.textContent.trim() : null,
                                        duration: durationEl ? durationEl.textContent.trim() : null,
                                        thumbnail: thumbnailEl ? thumbnailEl.getAttribute('src') : null
                                    });
                                }
                            } catch (e) {}
                        });

                        return items;
                    }""")

                    print(f"    Found {len(videos)} videos")

                    for video in videos:
                        video['search_query'] = query
                        video['platform'] = 'YouTube'
                        video['scraped_at'] = datetime.now().isoformat()

                    all_videos.extend(videos)

                except Exception as e:
                    print(f"    ⚠ Error: {e}")

            await browser.close()

            # Save results
            output_file = OUTPUT_DIR / f"youtube_3m_claw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(all_videos, f, indent=2)

            print(f"\n✓ Saved {len(all_videos)} YouTube videos to {output_file}")
            return all_videos

    async def scrape_reddit(self, subreddits):
        """Scrape Reddit posts about 3M Claw"""
        print("\n📱 Scraping Reddit for 3M Claw discussions...")

        async with async_playwright() as p:
            if self.use_brightdata:
                browser = await p.chromium.connect_over_cdp(BRIGHTDATA_ENDPOINT)
            else:
                browser = await p.chromium.launch(headless=True)

            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            all_posts = []

            search_terms = [
                "3M Claw",
                "3M Claw hooks",
                "3M Claw drywall",
                "3M Claw review"
            ]

            for subreddit in subreddits:
                for term in search_terms:
                    print(f"  Searching r/{subreddit}: {term}")

                    try:
                        # Search within subreddit
                        search_url = f"https://www.reddit.com/r/{subreddit}/search/?q={term.replace(' ', '+')}&restrict_sr=1&sort=relevance"
                        await page.goto(search_url, wait_until="networkidle", timeout=60000)
                        await page.wait_for_timeout(3000)

                        # Scroll to load
                        for _ in range(2):
                            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                            await page.wait_for_timeout(2000)

                        posts = await page.evaluate("""() => {
                            const items = [];
                            const postElements = document.querySelectorAll('[data-testid="post-container"]');

                            postElements.forEach(post => {
                                try {
                                    const titleEl = post.querySelector('h3');
                                    const authorEl = post.querySelector('[data-testid="post_author_link"]');
                                    const scoreEl = post.querySelector('[data-testid="vote-count"]');
                                    const commentsEl = post.querySelector('[data-testid="comment-count"]');
                                    const linkEl = post.querySelector('a[slot="full-post-link"]');
                                    const contentEl = post.querySelector('[data-testid="post-content"]');

                                    if (titleEl) {
                                        items.push({
                                            title: titleEl.textContent.trim(),
                                            url: linkEl ? linkEl.getAttribute('href') : null,
                                            author: authorEl ? authorEl.textContent.trim() : null,
                                            score: scoreEl ? scoreEl.textContent.trim() : null,
                                            comments: commentsEl ? commentsEl.textContent.trim() : null,
                                            content: contentEl ? contentEl.textContent.trim().substring(0, 500) : null
                                        });
                                    }
                                } catch (e) {}
                            });

                            return items;
                        }""")

                        print(f"    Found {len(posts)} posts")

                        for post in posts:
                            post['subreddit'] = subreddit
                            post['search_term'] = term
                            post['platform'] = 'Reddit'
                            post['scraped_at'] = datetime.now().isoformat()

                        all_posts.extend(posts)

                    except Exception as e:
                        print(f"    ⚠ Error: {e}")

            await browser.close()

            # Save
            output_file = OUTPUT_DIR / f"reddit_3m_claw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(all_posts, f, indent=2)

            print(f"\n✓ Saved {len(all_posts)} Reddit posts to {output_file}")
            return all_posts


async def main():
    scraper = SocialVideoScraper(use_brightdata=True)

    print("=" * 80)
    print("3M CLAW BRAND - SOCIAL VIDEO SCRAPING")
    print("=" * 80)

    # YouTube search queries
    youtube_queries = [
        "3M Claw hooks review",
        "3M Claw drywall hooks",
        "3M Claw installation",
        "3M Claw vs Command hooks",
        "3M Claw heavy duty hooks",
        "3M Claw garage organization",
        "3M Claw test",
        "3M Claw unboxing"
    ]

    # Reddit subreddits
    reddit_subreddits = [
        "HomeImprovement",
        "DIY",
        "homeowners",
        "InteriorDesign",
        "organization",
        "GarageStorage",
        "Tools"
    ]

    # Scrape YouTube
    youtube_videos = await scraper.scrape_youtube(youtube_queries)

    # Scrape Reddit
    reddit_posts = await scraper.scrape_reddit(reddit_subreddits)

    print("\n" + "=" * 80)
    print("SOCIAL SCRAPING COMPLETE")
    print("=" * 80)
    print(f"YouTube videos: {len(youtube_videos)}")
    print(f"Reddit posts: {len(reddit_posts)}")
    print(f"Total content: {len(youtube_videos) + len(reddit_posts)}")
    print(f"\nData saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
