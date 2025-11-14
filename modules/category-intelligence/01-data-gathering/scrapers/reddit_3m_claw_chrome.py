#!/usr/bin/env python3
"""
Reddit scraper for 3M Claw using local Chrome (user logged in)
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "social_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def scrape_reddit_chrome():
    """Use local Chrome to scrape Reddit (user already logged in)"""
    print("\n📱 Scraping Reddit for 3M Claw using local Chrome...")

    async with async_playwright() as p:
        # Connect to existing Chrome instance (user is logged in)
        browser = await p.chromium.launch(
            headless=False,  # Use visible browser
            channel="chrome"
        )

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

        subreddits = [
            "HomeImprovement",
            "DIY",
            "homeowners",
            "organization"
        ]

        for subreddit in subreddits:
            for term in search_terms:
                print(f"  Searching r/{subreddit}: {term}")

                try:
                    # Use Reddit's new interface
                    search_url = f"https://www.reddit.com/r/{subreddit}/search/?q={term.replace(' ', '%20')}&restrict_sr=1&sort=relevance&t=all"

                    await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(3000)

                    # Scroll to load more
                    for _ in range(2):
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(2000)

                    # Extract posts
                    posts = await page.evaluate("""() => {
                        const items = [];

                        // Try new Reddit structure
                        const posts = document.querySelectorAll('[data-testid^="post-container"]');

                        posts.forEach(post => {
                            try {
                                // Title
                                const titleEl = post.querySelector('h3');
                                const title = titleEl ? titleEl.textContent.trim() : null;

                                // Link
                                const linkEl = post.querySelector('a[data-click-id="body"]');
                                const url = linkEl ? linkEl.href : null;

                                // Author
                                const authorEl = post.querySelector('[data-testid="post_author_link"]');
                                const author = authorEl ? authorEl.textContent.trim() : null;

                                // Score
                                const scoreEl = post.querySelector('[id*="vote-arrows"]');
                                const score = scoreEl ? scoreEl.textContent.trim() : null;

                                // Comments
                                const commentsEl = post.querySelector('a[data-click-id="comments"]');
                                const comments = commentsEl ? commentsEl.textContent.trim() : null;

                                // Text content
                                const contentEl = post.querySelector('[data-click-id="text"]');
                                const content = contentEl ? contentEl.textContent.trim().substring(0, 500) : null;

                                if (title) {
                                    items.push({
                                        title: title,
                                        url: url,
                                        author: author,
                                        score: score,
                                        comments: comments,
                                        content: content
                                    });
                                }
                            } catch (e) {
                                console.error('Error parsing post:', e);
                            }
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
                    await page.wait_for_timeout(2000)

                except Exception as e:
                    print(f"    ⚠ Error: {e}")

        await browser.close()

        # Save results
        output_file = OUTPUT_DIR / f"reddit_3m_claw_chrome_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump({
                'platform': 'Reddit',
                'brand': '3M Claw',
                'collected_at': datetime.now().isoformat(),
                'post_count': len(all_posts),
                'posts': all_posts
            }, f, indent=2)

        print(f"\n✓ Saved {len(all_posts)} Reddit posts to {output_file}")
        return all_posts


async def main():
    print("=" * 80)
    print("REDDIT 3M CLAW SCRAPING - Using Local Chrome")
    print("=" * 80)

    posts = await scrape_reddit_chrome()

    print("\n" + "=" * 80)
    print("REDDIT SCRAPING COMPLETE")
    print("=" * 80)
    print(f"Total posts: {len(posts)}")


if __name__ == "__main__":
    asyncio.run(main())
