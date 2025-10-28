import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

SEARCH_URL = "https://www.lowes.com/search?searchTerm=garage%20hooks&sortOption=bestSeller"
CHROME_WS = "http://localhost:9224/chromium/address"

async def main():
    stealth = Stealth()
    async with async_playwright() as p:
        # connect to existing Chrome (remote debugging)
        browser = await p.chromium.connect_over_cdp("http://localhost:9224")
        context = browser.contexts[0]
        page = context.pages[0]
        await stealth.apply_stealth_async(page)
        await page.goto(SEARCH_URL, wait_until="networkidle")
        await page.wait_for_timeout(5000)
        state = await page.evaluate("() => window.__APOLLO_STATE__")
        if state:
            print("apollo keys", len(state))
            products = [
                {
                    "title": v.get("name"),
                    "price": v.get("prices", {}).get("price", {}).get("formattedValue"),
                    "url": f"https://www.lowes.com{v.get('pdpUrl')}" if v.get("pdpUrl") else None,
                    "brand": v.get("brand"),
                }
                for v in state.values()
                if isinstance(v, dict) and v.get("__typename") == "SearchProduct"
            ]
            print('found', len(products), 'products')
            for prod in products[:5]:
                print(prod)
        else:
            print("Apollo state missing")
        await browser.close()

asyncio.run(main())
