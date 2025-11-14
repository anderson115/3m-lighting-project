#!/usr/bin/env python3
"""
Collect 3M Claw discussions and video links from Reddit.
Searches DIY, home improvement, apartment living subreddits.
"""

import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Bright Data Browser API endpoint
BRIGHTDATA_WSS = "wss://brd-customer-hl_694870e0-zone-category_intelligence_module:lk3i01g4z7u2@brd.superproxy.io:9222"

# Reddit search queries
REDDIT_SEARCHES = [
    "3M Claw",
    "3M Claw hooks",
    "3M Claw review",
    "3M drywall hangers",
    "claw drywall hanger",
    "picture hanging drywall",
    "drywall hanger review",
]

# Subreddits to search
SUBREDDITS = [
    "DIY",
    "HomeImprovement",
    "ApartmentHacks",
    "OrganizationPorn",
    "HomeOrganization",
    "GarageStorage",
    "Frugal",
    "BuyItForLife",
]

async def scrape_reddit_search(page, query, subreddit=None):
    """Scrape Reddit search results."""
    if subreddit:
        search_url = f"https://www.reddit.com/r/{subreddit}/search/?q={query.replace(' ', '+')}&restrict_sr=1"
        print(f"  🔍 r/{subreddit}: '{query[:30]}'...", end=" ")
    else:
        search_url = f"https://www.reddit.com/search/?q={query.replace(' ', '+')}"
        print(f"  🔍 All Reddit: '{query[:30]}'...", end=" ")

    try:
        await page.goto(search_url, timeout=45000)
        await page.wait_for_load_state('networkidle', timeout=45000)
        await asyncio.sleep(2)

        # Scroll to load more posts
        for _ in range(3):
            await page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            await asyncio.sleep(1)

        posts = await page.evaluate('''() => {
            const results = [];
            const postElements = document.querySelectorAll('[data-testid="post-container"]');

            for (let el of postElements) {
                const titleEl = el.querySelector('a[slot="full-post-link"], a[data-click-id="body"]');
                const subredditEl = el.querySelector('a[data-testid="subreddit-name"]');
                const authorEl = el.querySelector('a[href^="/user/"]');
                const scoreEl = el.querySelector('[id^="vote-arrows-"]');
                const timeEl = el.querySelector('faceplate-timeago');

                if (titleEl) {
                    const title = titleEl.textContent.trim();
                    const url = titleEl.href;
                    const postId = url.split('/comments/')[1]?.split('/')[0] || '';

                    // Check if mentions 3M or Claw
                    const text = el.textContent.toLowerCase();
                    if (text.includes('3m') || text.includes('claw')) {
                        results.push({
                            post_id: postId,
                            title: title,
                            url: url,
                            subreddit: subredditEl ? subredditEl.textContent.trim() : '',
                            author: authorEl ? authorEl.textContent.trim() : '',
                            score: scoreEl ? scoreEl.textContent.trim() : '',
                            timestamp: timeEl ? timeEl.getAttribute('ts') : '',
                            platform: 'reddit',
                            type: 'discussion'
                        });
                    }
                }
            }
            return results;
        }''')

        print(f"✓ {len(posts)}")
        return posts

    except Exception as e:
        print(f"✗ {str(e)[:50]}")
        return []

async def main():
    """Collect Reddit posts about 3M Claw."""

    print("="*70)
    print("3M CLAW REDDIT COLLECTION")
    print("="*70)
    print(f"Search queries: {len(REDDIT_SEARCHES)}")
    print(f"Subreddits: {len(SUBREDDITS)}")
    print(f"Total searches: {len(REDDIT_SEARCHES) * (len(SUBREDDITS) + 1)}")
    print()

    all_posts = []

    async with async_playwright() as p:
        print("Connecting to Bright Data Browser API...")
        browser = await p.chromium.connect_over_cdp(BRIGHTDATA_WSS)

        if browser.contexts:
            context = browser.contexts[0]
            page = await context.new_page()
        else:
            context = await browser.new_context()
            page = await context.new_page()

        # Search all Reddit
        print("\n" + "="*70)
        print("SEARCHING ALL REDDIT")
        print("="*70)
        for i, query in enumerate(REDDIT_SEARCHES, 1):
            print(f"[{i}/{len(REDDIT_SEARCHES)}]", end=" ")
            posts = await scrape_reddit_search(page, query)
            for p in posts:
                p['search_query'] = query
            all_posts.extend(posts)

        # Search specific subreddits
        print("\n" + "="*70)
        print("SEARCHING SPECIFIC SUBREDDITS")
        print("="*70)
        for i, subreddit in enumerate(SUBREDDITS, 1):
            print(f"\n[{i}/{len(SUBREDDITS)}] r/{subreddit}:")
            for query in REDDIT_SEARCHES:
                posts = await scrape_reddit_search(page, query, subreddit)
                for p in posts:
                    p['search_query'] = f"{subreddit}:{query}"
                all_posts.extend(posts)

        await browser.close()

    # Remove duplicates
    unique_posts = {}
    for post in all_posts:
        post_id = post.get('post_id')
        if post_id and post_id not in unique_posts:
            unique_posts[post_id] = post

    final_posts = list(unique_posts.values())

    print(f"\n{'='*70}")
    print(f"REDDIT COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total collected: {len(all_posts)} posts")
    print(f"After deduplication: {len(final_posts)} unique posts")
    print(f"{'='*70}\n")

    # Save results
    if final_posts:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"outputs/3m_claw_reddit_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump({
                'total_count': len(final_posts),
                'platform': 'reddit',
                'collected_at': timestamp,
                'posts': final_posts
            }, f, indent=2)

        print(f"✓ Saved to: {output_file}")
        print(f"  Total posts: {len(final_posts)}")

        # Top subreddits
        subreddits = {}
        for p in final_posts:
            sub = p.get('subreddit', 'Unknown')
            if sub:
                subreddits[sub] = subreddits.get(sub, 0) + 1

        print(f"\n  Top subreddits:")
        for sub, count in sorted(subreddits.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"    {sub}: {count} posts")
    else:
        print("\n✗ No posts collected")

if __name__ == "__main__":
    asyncio.run(main())
