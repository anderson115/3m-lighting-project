import fs from "fs";
import puppeteer from "puppeteer-core";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";
const SEARCH_URL = "https://www.etsy.com/search?q=garage%20organizer&explicit=1";

async function run() {
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();
  await page.goto(SEARCH_URL, { waitUntil: "networkidle2", timeout: 120000 });
  const html = await page.content();
  fs.writeFileSync("etsy_search_dump.html", html);
  await browser.close();
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
