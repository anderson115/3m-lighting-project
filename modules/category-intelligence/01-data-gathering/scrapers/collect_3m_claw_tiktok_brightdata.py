#!/usr/bin/env python3
"""Collect 3M Claw TikTok videos via Bright Data Browser API."""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

BRIGHTDATA_WSS = "wss://brd-customer-hl_694870e0-zone-category_intelligence_module:lk3i01g4z7u2@brd.superproxy.io:9222"
TIKTOK_QUERIES = [
    "3M Claw",
    "3M Claw hooks",
    "3M Claw review",
    "3M Claw installation",
    "3M Claw picture hanger"
]

async def scrape_tiktok(page, query: str, max_results: int = 60):
    print(f"\n📱 TikTok: {query}")
    await page.goto(f"https://www.tiktok.com/search?q={query.replace(' ', '%20')}")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(3)
    for _ in range(8):
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(1.2)
    results = await page.evaluate('''() => {
        const rows = [];
        const items = document.querySelectorAll('[data-e2e="search_top-item"]');
        for (const el of items) {
            const anchor = el.querySelector('a[href*="/video/"]');
            if (!anchor) { continue; }
            const vid = anchor.href.split('/video/')[1]?.split('?')[0] || '';
            if (!vid) { continue; }
            rows.push({
                video_id: vid,
                url: anchor.href,
                title: (el.querySelector('[data-e2e="search-card-desc"]')?.textContent || '').trim(),
                channel: (el.querySelector('[data-e2e="search-card-user-unique-id"]')?.textContent || '').trim(),
                views: (el.querySelector('[data-e2e="search-card-view-count"]')?.textContent || '').trim(),
                platform: 'tiktok',
                search_query: query
            });
        }
        return rows;
    }''')
    print(f"   ✓ {len(results)} items")
    return results[:max_results]

async def main():
    print("Connecting to Bright Data Browser API for TikTok scrape...")
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(BRIGHTDATA_WSS)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()
        collected = []
        for idx, query in enumerate(TIKTOK_QUERIES, 1):
            print(f"[{idx}/{len(TIKTOK_QUERIES)}]", end="")
            results = await scrape_tiktok(page, query)
            collected.extend(results)
        await browser.close()

    dedup = {}
    for row in collected:
        vid = row.get('video_id')
        if vid and vid not in dedup:
            dedup[vid] = row
    final = list(dedup.values())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    out_path = output_dir / f"3m_claw_tiktok_{timestamp}.json"
    out_path.write_text(json.dumps({
        "total": len(final),
        "collected_at": timestamp,
        "videos": final
    }, indent=2))
    print(f"\nSaved {len(final)} unique TikTok videos -> {out_path}")

if __name__ == "__main__":
    asyncio.run(main())
