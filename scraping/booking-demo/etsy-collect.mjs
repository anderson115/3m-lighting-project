import puppeteer from "puppeteer-core";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

const QUERIES = [
  "garage organizer",
  "slatwall storage",
  "french cleat shelf",
  "garage hook",
];

async function extractListings(page) {
  await page.waitForSelector('div.js-merch-stash-check-listing', { timeout: 120000 });
  return await page.$$eval('div.js-merch-stash-check-listing', (cards) => {
    return cards.slice(0, 40).map((card, index) => {
      const titleAnchor = card.querySelector('a.listing-link[data-listing-id]');
      const title = titleAnchor?.querySelector('h3')?.textContent?.trim();
      const url = titleAnchor?.href || null;
      const priceEl = card.querySelector('.currency-value');
      const currencyEl = card.querySelector('.currency-symbol');
      const shopEl = card.querySelector('span.clickable-shop-name');
      const badgeEl = card.querySelector('p[data-region="badge"]');
      const ratingEl = card.querySelector('[role="img"][aria-label*="star rating"]');
      const reviewsEl = card.querySelector('p wt-text-body-smaller');
      const listingTypeEl = card.querySelector('div.wt-display-flex-xs svg + p');
      const imageEl = card.querySelector('img[data-listing-card-listing-image]');
      return {
        title,
        url,
        price: priceEl?.textContent?.trim() || null,
        currency: currencyEl?.textContent?.trim() || null,
        shop: shopEl?.textContent?.trim() || null,
        badge: badgeEl?.textContent?.trim() || null,
        rating: ratingEl?.getAttribute('aria-label') || null,
        listing_type: listingTypeEl?.textContent?.trim() || null,
        image: imageEl?.src || null,
        index
      };
    }).filter(item => item.title && item.url);
  });
}

async function collectQuery(browser, query) {
  const page = await browser.newPage();
  try {
    const searchUrl = `https://www.etsy.com/search?q=${encodeURIComponent(query)}&explicit=1`;
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 120000 });
    const listings = await extractListings(page);
    return listings.map(item => ({ ...item, query }));
  } finally {
    await page.close();
  }
}

async function run() {
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const results = [];
  for (const query of QUERIES) {
    const listings = await collectQuery(browser, query);
    console.error(`Query "${query}" returned ${listings.length} listings.`);
    results.push(...listings);
  }
  await browser.close();
  const __dirname = path.dirname(fileURLToPath(import.meta.url));
  const outputPath = path.resolve(__dirname, '../../modules/category-intelligence/data/etsy_listings.json');
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`Saved ${results.length} records to ${outputPath}`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  run().catch((err) => {
    console.error('Etsy collection failed', err);
    process.exit(1);
  });
}
