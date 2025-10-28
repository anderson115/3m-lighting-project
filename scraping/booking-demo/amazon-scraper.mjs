import puppeteer from "puppeteer-core";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";
const URL = "https://www.amazon.com/";
const SEARCH_TERM = "garage shelving";

async function dismissPopups(page) {
  try {
    const denyBtn = await page.waitForSelector('#sp-cc-accept', { timeout: 5000 });
    await denyBtn.click();
  } catch (_) {}
  try {
    const closeBtn = await page.waitForSelector('[data-action="a-popover-close"]', { timeout: 5000 });
    await closeBtn.click();
  } catch (_) {}
}

async function performSearch(page) {
  const selector = 'input#twotabsearchtextbox, input[name="field-keywords"]';
  await page.waitForSelector(selector, { timeout: 45000 });
  await page.focus(selector);
  await page.keyboard.down('Control');
  await page.keyboard.press('A');
  await page.keyboard.up('Control');
  await page.keyboard.type(SEARCH_TERM, { delay: 50 });
  await page.keyboard.press('Enter');
  await page.waitForSelector('div.s-main-slot', { timeout: 90000 });
}

async function extractResults(page) {
  const results = await page.$$eval('div.s-result-item[data-component-type="s-search-result"]', (els) => {
    return els.map((el) => {
      const title = el.querySelector('h2 a span')?.textContent?.trim();
      const priceWhole = el.querySelector('.a-price > .a-offscreen')?.textContent?.trim();
      const rating = el.querySelector('[data-component-type="s-search-result"] span[aria-label*="out of 5 stars"]')?.getAttribute('aria-label');
      const reviews = el.querySelector('span[aria-label*="ratings"]')?.getAttribute('aria-label') ||
        el.querySelector('span[aria-label*="rating"]')?.getAttribute('aria-label');
      const link = el.querySelector('h2 a')?.href;
      return { title, price: priceWhole, rating, reviews, link };
    }).filter(item => item.title);
  });
  return results;
}

async function run() {
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();
  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await dismissPopups(page);
  await performSearch(page);
  const data = await extractResults(page);
  console.log(JSON.stringify(data, null, 2));
  await browser.close();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  run().catch((err) => {
    console.error('Amazon scraper failed', err);
    process.exit(1);
  });
}
