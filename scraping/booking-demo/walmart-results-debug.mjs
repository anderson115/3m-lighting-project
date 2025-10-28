import puppeteer from "puppeteer-core";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";
const SEARCH_TERM = "garage cabinets";

async function debugResults() {
  console.log("Connecting to Bright Data browser...");
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();

  console.log("Loading Walmart and searching...");
  await page.goto("https://www.walmart.com/", { waitUntil: 'network idle2', timeout: 60000 });

  const input = await page.waitForSelector('input[name="q"]', { timeout: 30000 });
  await input.click({ clickCount: 3 });
  await input.type(SEARCH_TERM, { delay: 50 });
  await Promise.all([
    page.keyboard.press('Enter'),
    page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 60000 }),
  ]);

  console.log("Waiting for results...");
  await page.waitForSelector('[data-automation-id="search-result-gridview-item"], [data-item-id], [data-testid="list-view"]', { timeout: 30000 });

  console.log("Taking screenshot...");
  await page.screenshot({ path: 'walmart_results.png', fullPage: true });

  console.log("Analyzing page structure...");

  // Check for various possible selectors
  const analysis = await page.evaluate(() => {
    const results = {
      automationId: document.querySelectorAll('[data-automation-id="search-result-gridview-item"]').length,
      itemId: document.querySelectorAll('[data-item-id]').length,
      testId: document.querySelectorAll('[data-testid*="item"]').length,
      productCards: document.querySelectorAll('[data-testid="list-view"] > div').length,
    };

    // Get sample product card HTML
    const firstCard = document.querySelector('[data-item-id]') ||
                     document.querySelector('[data-testid="list-view"] > div') ||
                     document.querySelector('[data-automation-id="search-result-gridview-item"]');

    if (firstCard) {
      results.sampleHTML = firstCard.outerHTML.substring(0, 1000);

      // Try to extract data from first card
      results.sampleData = {
        title: firstCard.querySelector('[data-automation-id="product-title"]')?.textContent ||
               firstCard.querySelector('[data-testid="product-title"]')?.textContent ||
               firstCard.querySelector('span[class*="product-title"]')?.textContent ||
               firstCard.querySelector('a span')?.textContent,
        price: firstCard.querySelector('[data-automation-id="product-price"]')?.textContent ||
               firstCard.querySelector('[data-testid="price"]')?.textContent ||
               firstCard.querySelector('[class*="price"]')?.textContent,
        link: firstCard.querySelector('a')?.href
      };
    }

    return results;
  });

  console.log("\nPage Analysis:");
  console.log(JSON.stringify(analysis, null, 2));

  await browser.close();
  console.log("\nDebug complete! Check walmart_results.png");
}

debugResults().catch(console.error);
