import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";
const URL = "https://www.menards.com/main/search.html?search=garage%20hooks";

async function run() {
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();
  await page.goto(URL, { waitUntil: 'networkidle2', timeout: 120000 });
  const html = await page.content();
  fs.writeFileSync('menards_search_dump.html', html);
  const keys = await page.evaluate(() => Object.keys(window));
  fs.writeFileSync('menards_window_keys.json', JSON.stringify(keys, null, 2));
  await browser.close();
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
