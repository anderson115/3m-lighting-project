import puppeteer from "puppeteer-core";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-menards:px0askma981v@brd.superproxy.io:9222";
const SEARCH_URL = "https://www.menards.com/main/search.html?search=garage%20hooks";

async function run() {
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();
  await page.goto(SEARCH_URL, { waitUntil: 'networkidle2', timeout: 120000 });
  const html = await page.content();
  console.log(html.slice(0, 500));
  await browser.close();
}

run().catch((err) => {
  console.error('Menards scraper failed', err);
  process.exit(1);
});
