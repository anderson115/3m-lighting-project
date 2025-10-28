import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

async function debugWalmart() {
  console.log("Connecting to Bright Data browser...");
  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const page = await browser.newPage();

  console.log("Loading Walmart.com...");
  await page.goto("https://www.walmart.com/", { waitUntil: 'networkidle2', timeout: 60000 });

  console.log("Page loaded. Taking screenshot...");
  await page.screenshot({ path: 'walmart_homepage.png', fullPage: false });

  console.log("Finding search inputs...");
  const inputs = await page.$$eval('input', (elements) => {
    return elements.map((el, i) => ({
      index: i,
      type: el.type,
      id: el.id,
      name: el.name,
      placeholder: el.placeholder,
      ariaLabel: el.getAttribute('aria-label'),
      className: el.className,
      visible: el.offsetParent !== null
    }));
  });

  console.log("\nFound inputs:");
  inputs.filter(i => i.visible).forEach(input => {
    console.log(JSON.stringify(input, null, 2));
  });

  // Try to find search-related elements
  console.log("\n\nSearching for elements with 'search' in attributes...");
  const searchElements = await page.evaluate(() => {
    const results = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);

    while (walker.nextNode()) {
      const el = walker.currentNode;
      const attrs = Array.from(el.attributes || []);
      const hasSearch = attrs.some(attr =>
        attr.value?.toLowerCase().includes('search') ||
        attr.name?.toLowerCase().includes('search')
      );

      if (hasSearch && (el.tagName === 'INPUT' || el.tagName === 'BUTTON')) {
        results.push({
          tag: el.tagName,
          id: el.id,
          class: el.className,
          type: el.type,
          placeholder: el.placeholder,
          ariaLabel: el.getAttribute('aria-label'),
          dataTestId: el.getAttribute('data-testid'),
          outerHTML: el.outerHTML.substring(0, 200)
        });
      }
    }
    return results;
  });

  console.log(JSON.stringify(searchElements, null, 2));

  await browser.close();
  console.log("\nDebug complete!");
}

debugWalmart().catch(console.error);
