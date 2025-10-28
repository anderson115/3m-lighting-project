import puppeteer from "puppeteer-core";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";
const SEARCH_URL = "https://www.etsy.com/search?q=garage%20organizer&explicit=1";

async function run() {
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();
  try {
    await page.goto(SEARCH_URL, { waitUntil: "domcontentloaded", timeout: 120000 });
    await page.waitForSelector("ul.responsive-listing-grid li", { timeout: 120000 });
    const listings = await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll("ul.responsive-listing-grid li"));
      return items.slice(0, 6).map((item) => {
        const titleEl = item.querySelector("h3");
        const title = titleEl ? titleEl.textContent.trim().replace(/\s+/g, " ") : null;
        const linkEl = item.querySelector("a.listing-link");
        const url = linkEl ? linkEl.href : null;
        const priceEl = item.querySelector("span.currency-value");
        const price = priceEl ? priceEl.textContent.trim() : null;
        const shopEl = item.querySelector("p.text-body-smaller");
        const shop = shopEl ? shopEl.textContent.trim().replace(/\s+/g, " ") : null;
        const badgeEl = item.querySelector("p[data-region=badge]");
        const badge = badgeEl ? badgeEl.textContent.trim().replace(/\s+/g, " ") : null;
        const salesEl = item.querySelector("span[data-qa=listing-card-info]");
        const sales = salesEl ? salesEl.textContent.trim().replace(/\s+/g, " ") : null;
        return { title, url, price, shop, badge, sales };
      }).filter(item => item.title && item.url);
    });
    console.log(JSON.stringify(listings, null, 2));
  } finally {
    await page.close();
    await browser.close();
  }
}

run().catch((err) => {
  console.error("Etsy test scrape failed", err);
  process.exit(1);
});
