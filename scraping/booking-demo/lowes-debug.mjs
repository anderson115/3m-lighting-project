import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";
const URL = "https://www.lowes.com/";
const SEARCH_TERM = "garage hooks";

async function run() {
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();
  page.on('response', async (response) => {
    try {
      const url = response.url();
      if (url.includes('/api/') || url.includes('graphql') || url.includes('search')) {
        const text = await response.text();
        if (text && text.includes('SearchProduct')) {
          fs.writeFileSync('lowes_response.json', text);
        }
      }
    } catch (err) {
      // ignore
    }
  });
  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForSelector('input[id="search-query"]', { timeout: 30000 });
  await page.type('input[id="search-query"]', SEARCH_TERM, { delay: 50 });
 await Promise.all([
    page.keyboard.press('Enter'),
    page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 90000 }),
  ]);
  await new Promise((resolve) => setTimeout(resolve, 5000));
  const html = await page.content();
  fs.writeFileSync('lowes_search_dump.html', html);
  const keys = await page.evaluate(() => Object.keys(window));
  fs.writeFileSync('lowes_window_keys.json', JSON.stringify(keys, null, 2));
  const apolloState = await page.evaluate(() => window.__APOLLO_STATE__);
  fs.writeFileSync('lowes_apollo_state.json', JSON.stringify(apolloState, null, 2));
  await browser.close();
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
