import puppeteer from "puppeteer-core";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";
const URL = "https://www.acehardware.com/";
const SEARCH_TERM = "garage organizers";

async function dismissPopups(page) {
  try {
    const closeBtn = await page.waitForSelector('button[aria-label="Close"]', { timeout: 8000 });
    await closeBtn.click();
  } catch (_) {}
}

async function performSearch(page) {
  const input = await page.waitForSelector('input#headerSearch', { timeout: 30000 });
  await input.click({ clickCount: 3 });
  await input.type(SEARCH_TERM, { delay: 50 });
  await Promise.all([
    page.keyboard.press('Enter'),
    page.waitForNavigation({ waitUntil: 'domcontentloaded' }),
  ]);
}

async function extractResults(page) {
  const products = await page.$$eval('li.product-grid__item', (items) => {
    return items.map((item) => {
      const title = item.querySelector('h3 a')?.textContent?.trim();
      const price = item.querySelector('.product-card__price, [data-test="product-price"]')?.textContent?.trim();
      const rating = item.querySelector('span[aria-label*="out of 5"]')?.getAttribute('aria-label');
      const reviews = item.querySelector('.product-card__reviews-count')?.textContent?.trim();
      const link = item.querySelector('h3 a')?.href;
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
    console.error('Ace Hardware scraper failed', err);
    process.exit(1);
  });
}
