import puppeteer from "puppeteer-core";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";
const URL = "https://www.lowes.com/";
const SEARCH_TERM = "garage cabinets";

async function performSearch(page) {
  const searchContainer = await page.waitForSelector('input[id="search-query"]', { timeout: 30000 });
  await searchContainer.click({ clickCount: 3 });
  await searchContainer.type(SEARCH_TERM, { delay: 50 });
  await Promise.all([
    page.keyboard.press('Enter'),
    page.waitForNavigation({ waitUntil: 'domcontentloaded' }),
  ]);
  await page.waitForFunction(() => window.__APOLLO_STATE__ !== undefined, { timeout: 60000 });
}

async function extractResults(page) {
  const state = await page.evaluate(() => window.__APOLLO_STATE__);
  if (!state) {
    return [];
  }
  const products = [];
  for (const value of Object.values(state)) {
    if (value && typeof value === 'object' && value.__typename === 'SearchProduct') {
      products.push({
        title: value.name,
        price: value.prices?.price?.formattedValue || value.prices?.price?.value,
        rating: value.ratingsAndReviews?.averageRating,
        reviews: value.ratingsAndReviews?.reviewCount,
        link: value.pdpUrl ? `https://www.lowes.com${value.pdpUrl}` : null,
        sku: value.itemNumber,
        brand: value.brand,
      });
    }
  }
  return products;
}

async function run() {
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();
  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await performSearch(page);
  const data = await extractResults(page);
  console.log(JSON.stringify(data, null, 2));
  await browser.close();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  run().catch((err) => {
    console.error('Lowe\'s scraper failed', err);
    process.exit(1);
  });
}
