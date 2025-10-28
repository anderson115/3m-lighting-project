import puppeteer from "puppeteer-core";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";
const URL = "https://www.walmart.com/";
const SEARCH_TERM = "garage tool storage";

async function performSearch(page) {
  // Updated selector - Walmart changed their HTML
  const input = await page.waitForSelector('input[name="q"]', { timeout: 30000 });
  await input.click({ clickCount: 3 });
  await input.type(SEARCH_TERM, { delay: 50 });
  await Promise.all([
    page.keyboard.press('Enter'),
    page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 60000 }),
  ]);
  // Wait for search results to appear
  await page.waitForSelector('[data-automation-id="search-result-gridview-item"], [data-item-id]', { timeout: 30000 });
}

async function extractResults(page) {
  const products = await page.$$eval('[data-automation-id="search-result-gridview-item"]', (cards) => {
    return cards.map((card) => {
      const title = card.querySelector('[data-automation-id="product-title"] span, a[aria-label]')?.textContent?.trim();
      const price = card.querySelector('[data-automation-id="product-price"] span, .price-group')?.textContent?.trim();
      const rating = card.querySelector('[data-automation-id="rating-stars"] span')?.getAttribute('aria-label');
      const reviews = card.querySelector('[data-automation-id="rating-count"] span')?.textContent?.trim();
      const link = card.querySelector('a[href*="/ip/"]')?.href;
      return { title, price, rating, reviews, link };
    }).filter(item => item.title);
  });
  return products;
}

async function run() {
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();
  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await performSearch(page);
  const results = await extractResults(page);
  console.log(JSON.stringify(results, null, 2));
  await browser.close();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  run().catch((err) => {
    console.error('Walmart scraper failed', err);
    process.exit(1);
  });
}
