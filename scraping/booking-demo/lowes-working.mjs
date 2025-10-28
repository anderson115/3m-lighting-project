import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

const QUERIES = [
  "garage organizer",
  "garage shelving",
  "garage cabinets",
  "garage storage bins",
  "garage workbench"
];

const MAX_PER_QUERY = 40;

async function searchAndExtract(browser, query) {
  const page = await browser.newPage();

  try {
    console.log(`\n🔍 Searching Lowes: "${query}"`);

    const searchUrl = `https://www.lowes.com/search?searchTerm=${encodeURIComponent(query)}`;
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 90000 });

    // Wait for dynamic content to load
    await new Promise(resolve => setTimeout(resolve, 5000));

    // Try to extract from page content directly
    const products = await page.evaluate((maxItems) => {
      const results = [];

      // Look for product cards - Lowes uses various structures
      const productSelectors = [
        'article[data-testid="hybrid-component"]',
        '.product-pod',
        '[data-itemid]',
        'a[href*="/pd/"]'
      ];

      let productElements = [];
      for (const selector of productSelectors) {
        productElements = Array.from(document.querySelectorAll(selector));
        if (productElements.length > 0) break;
      }

      // Extract from each product element
      for (let i = 0; i < Math.min(productElements.length, maxItems); i++) {
        const el = productElements[i];

        // Find product link
        const link = el.querySelector('a[href*="/pd/"]') || el.closest('a[href*="/pd/"]');
        if (!link) continue;

        const url = link.href;

        // Extract title - try multiple selectors
        const title = el.querySelector('h3')?.textContent?.trim() ||
                     el.querySelector('[data-testid="product-title"]')?.textContent?.trim() ||
                     el.querySelector('.product-title')?.textContent?.trim() ||
                     link.getAttribute('aria-label') ||
                     '';

        if (!title) continue;

        // Extract price
        const priceEl = el.querySelector('[data-testid="price"]') ||
                       el.querySelector('.price') ||
                       el.querySelector('[class*="price"]');
        const price = priceEl?.textContent?.trim() || null;

        // Extract other details
        const brand = el.querySelector('[data-testid="brand"]')?.textContent?.trim() ||
                     el.querySelector('.brand')?.textContent?.trim() ||
                     null;

        results.push({
          title,
          link: url,
          price,
          brand,
          rating: null,
          reviews: null,
          sku: null
        });
      }

      return results;
    }, MAX_PER_QUERY);

    console.log(`   ✓ Found ${products.length} products`);
    await page.close();
    return products.map(p => ({ ...p, query }));

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 100)}`);
    await page.close();
    return [];
  }
}

async function main() {
  console.log("=".repeat(60));
  console.log("LOWES COLLECTION (Bright Data)");
  console.log("=".repeat(60));

  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
  const allProducts = [];

  for (const query of QUERIES) {
    const products = await searchAndExtract(browser, query);
    allProducts.push(...products);
    await new Promise(resolve => setTimeout(resolve, 3000));
  }

  await browser.close();

  console.log(`\n${"=".repeat(60)}`);
  console.log(`TOTAL: ${allProducts.length} products`);
  console.log(`${"=".repeat(60)}`);

  const output = {
    retailer: "Lowes",
    collected_at: new Date().toISOString(),
    queries: QUERIES,
    product_count: allProducts.length,
    products: allProducts
  };

  fs.writeFileSync('lowes_garage_collection.json', JSON.stringify(output, null, 2));
  console.log("✓ Saved to lowes_garage_collection.json");

  return allProducts.length;
}

main().then(count => {
  console.log(`\n✅ Complete: ${count} products`);
  process.exit(0);
}).catch(err => {
  console.error("❌ Failed:", err.message);
  process.exit(1);
});
