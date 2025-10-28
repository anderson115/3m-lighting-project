import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

async function debugLowes() {
  console.log("Connecting to Bright Data...");
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();

  try {
    console.log("Loading search results...");
    const searchUrl = "https://www.lowes.com/search?searchTerm=garage+organizer";
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 90000 });

    console.log("Page loaded. Taking screenshot...");
    await page.screenshot({ path: 'lowes_search_results.png' });

    // Check for Apollo state
    const hasApollo = await page.evaluate(() => {
      return {
        hasState: typeof window.__APOLLO_STATE__ !== 'undefined',
        stateKeys: window.__APOLLO_STATE__ ? Object.keys(window.__APOLLO_STATE__).slice(0, 10) : [],
        stateSize: window.__APOLLO_STATE__ ? Object.keys(window.__APOLLO_STATE__).length : 0
      };
    });

    console.log("\nApollo State Check:");
    console.log(JSON.stringify(hasApollo, null, 2));

    // Check for SearchProduct entries
    const products = await page.evaluate(() => {
      const state = window.__APOLLO_STATE__;
      if (!state) return [];

      const results = [];
      for (const [key, value] of Object.entries(state)) {
        if (value && typeof value === 'object' && value.__typename === 'SearchProduct') {
          results.push({
            key,
            name: value.name,
            itemNumber: value.itemNumber,
            brand: value.brand,
            priceValue: value.prices?.price?.value,
            priceFormatted: value.prices?.price?.formattedValue,
            pdpUrl: value.pdpUrl
          });
        }
      }
      return results.slice(0, 5); // First 5 for debugging
    });

    console.log("\nFound SearchProduct entries:", products.length);
    console.log(JSON.stringify(products, null, 2));

    // Also check DOM elements
    const domProducts = await page.evaluate(() => {
      const results = [];

      // Try various selectors
      const selectors = [
        '.product-pod',
        '[data-testid="product-pod"]',
        '.plp-pod',
        '[data-nodeid]',
        'article',
        '.sc-product-card'
      ];

      for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
          results.push({
            selector,
            count: elements.length,
            sampleHTML: elements[0]?.outerHTML?.substring(0, 300)
          });
        }
      }

      return results;
    });

    console.log("\nDOM Product Elements:");
    console.log(JSON.stringify(domProducts, null, 2));

    await browser.close();
    console.log("\n✅ Debug complete! Check lowes_search_results.png");

  } catch (error) {
    console.error("Error:", error.message);
    await browser.close();
  }
}

debugLowes();
