import asyncio
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

SEARCH_URL = "https://www.lowes.com/search?searchTerm=garage%20hooks&sortOption=bestSeller"
COOKIES_PATH = "cookies/lowes_min.json"

async def main():
    stealth = Stealth()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        with open(COOKIES_PATH, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)
        print(f"Loaded {len(cookies)} cookies")
        page = await context.new_page()
        await stealth.apply_stealth_async(page)
        await page.goto(SEARCH_URL, wait_until="networkidle")
        await page.wait_for_timeout(7000)
        html = await page.content()
        print(html[:200])
        state = await page.evaluate("() => window.__APOLLO_STATE__")
        if state:
            products = [
                {
                    "title": v.get("name"),
                    "price": v.get("prices", {}).get("price", {}).get("formattedValue"),
                    "url": f"https://www.lowes.com{v.get('pdpUrl')}" if v.get("pdpUrl") else None,
                    "brand": v.get("brand"),
                    "itemNumber": v.get("itemNumber"),
                }
                for v in state.values()
                if isinstance(v, dict) and v.get("__typename") == "SearchProduct"
            ]
            print(f"Found {len(products)} products")
            for prod in products[:5]:
                print(prod)
        else:
            print("__APOLLO_STATE__ not found")
        await browser.close()

asyncio.run(main())
