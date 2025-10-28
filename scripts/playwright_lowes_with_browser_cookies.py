import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import browser_cookie3

SEARCH_URL = "https://www.lowes.com/search?searchTerm=garage%20hooks&sortOption=bestSeller"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
EXTRA_HEADERS = {
    "sec-ch-ua": '"Google Chrome";v="141", "Chromium";v="141", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-language": "en-US,en;q=0.9",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "upgrade-insecure-requests": "1",
    "referer": "https://www.lowes.com/"
}

async def main():
    cookies_jar = browser_cookie3.chrome(domain_name='.lowes.com')
    cookies = []
    for cookie in cookies_jar:
        cookies.append({
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain,
            "path": cookie.path,
            "expires": cookie.expires if cookie.expires is not None else -1,
            "httpOnly": cookie.has_nonstandard_attr('HttpOnly'),
            "secure": bool(cookie.secure),
        })
    print(f"Loaded {len(cookies)} cookies from Chrome")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent=USER_AGENT,
            locale="en-US",
            viewport={"width": 1280, "height": 720},
        )
        await context.set_extra_http_headers(EXTRA_HEADERS)
        await context.add_cookies(cookies)
        page = await context.new_page()
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        await page.goto(SEARCH_URL, wait_until='networkidle')
        await page.wait_for_timeout(5000)
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
