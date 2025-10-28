import puppeteer from "puppeteer-core";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";
const URL = "https://www.homedepot.com/";
const SEARCH_TERM = "garage cabinets";

async function dismissPopups(page) {
  try {
    const closeBtn = await page.waitForSelector('button[aria-label="Close"]', { timeout: 5000 });
    await closeBtn.click();
  } catch (_) {}
}

async function performSearch(page) {
  const input = await page.waitForSelector('input[data-testid="search-bar-input"]', { timeout: 30000 });
  await input.click({ clickCount: 3 });
  await input.type(SEARCH_TERM, { delay: 50 });
  await Promise.all([
    page.keyboard.press('Enter'),
    page.waitForNavigation({ waitUntil: 'domcontentloaded' }),
  ]);
}

async function extractResults(page) {
  const products = await page.$$eval('[data-testid="product-card"]', (cards) => {
    return cards.map((card) => {
      const title = card.querySelector('[data-testid="product-card-title"]')?.textContent?.trim();
      const price = card.querySelector('[data-testid="product-price"] span, [data-testid="each-price"]')?.textContent?.trim();
      const rating = card.querySelector('[data-testid="star-rating"]')?.getAttribute('aria-label');
      const reviews = card.querySelector('[data-testid="review-count"]')?.textContent?.trim();
      const link = card.querySelector('a[data-testid="product-card-title"]')?.href;
      return { title, price, rating, reviews, link };
    }).filter(item => item.title);
  });
  return products;
}

async function run() {
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();
  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await dismissPopups(page);
  await performSearch(page);
  const results = await extractResults(page);
  console.log(JSON.stringify(results, null, 2));
  await browser.close();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  run().catch((err) => {
    console.error('Home Depot scraper failed', err);
    process.exit(1);
  });
}
