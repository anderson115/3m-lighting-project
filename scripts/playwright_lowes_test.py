import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

SEARCH_URL = "https://www.lowes.com/search?searchTerm=garage%20hooks&sortOption=bestSeller"

async def main():
    stealth = Stealth()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth.apply_stealth_async(page)
        await page.goto(SEARCH_URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        content = await page.content()
        print(content[:1000])
        state = await page.evaluate("() => window.__APOLLO_STATE__")
        print("state keys", len(state) if state else None)
        await browser.close()

asyncio.run(main())
