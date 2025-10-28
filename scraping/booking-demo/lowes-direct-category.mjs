import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// Direct category URLs instead of search
const CATEGORY_URLS = [
  "https://www.lowes.com/pl/Garage-organization-Storage-organization/4294612721",
  "https://www.lowes.com/pl/Shelving-Storage-organization/4294612733",
  "https://www.lowes.com/pl/Storage-bins-Storage-organization/4294612729",
  "https://www.lowes.com/pl/Cabinets-cabinet-hardware/4294709874"
];

const MAX_PRODUCTS = 50; // Per category

async function extractFromCategory(page, url, categoryName) {
  try {
    console.log(`\n🔍 Lowes Category: ${categoryName}`);
    console.log(`   URL: ${url}`);

    await page.goto(url, { waitUntil: 'networkidle2', timeout: 90000 });

    // Wait for content to fully render
    await new Promise(resolve => setTimeout(resolve, 5000));

    // Extract product data
    const products = await page.evaluate((maxItems) => {
      const results = [];

      // Try multiple selectors for product cards
      let productLinks = Array.from(document.querySelectorAll('a[href*="/pd/"]'));

      // Deduplicate by href
      const seen = new Set();
      productLinks = productLinks.filter(link => {
        const href = link.href;
        if (seen.has(href)) return false;
        seen.add(href);
        return true;
      });

      for (let i = 0; i < Math.min(productLinks.length, maxItems); i++) {
        const link = productLinks[i];

        // Get the parent container that has product info
        let container = link.closest('[data-selector="product-card"]') ||
                       link.closest('article') ||
                       link.closest('[data-nodeid]') ||
                       link;

        // Extract title
        const title = container.querySelector('[data-selector="product-title"]')?.textContent?.trim() ||
                     container.querySelector('h3')?.textContent?.trim() ||
                     link.textContent?.trim() ||
                     '';

        if (!title || title.length < 3) continue;

        // Extract price
        const priceEl = container.querySelector('[data-selector="product-price"]') ||
                       container.querySelector('[class*="price"]');
        const price = priceEl?.textContent?.trim() || null;

        // Extract brand
        const brand = container.querySelector('[data-selector="brand"]')?.textContent?.trim() ||
                     container.querySelector('.brand')?.textContent?.trim() ||
                     null;

        // Extract model/SKU
        const model = container.querySelector('[data-selector="model"]')?.textContent?.trim() ||
                     null;

        // Extract rating
        const ratingEl = container.querySelector('[aria-label*="star"]');
        const rating = ratingEl?.getAttribute('aria-label')?.match(/(\d+\.?\d*)/)?.[1] || null;

        results.push({
          title,
          link: link.href,
          price,
          brand,
          sku: model,
          rating,
          reviews: null
        });
      }

      return results;
    }, MAX_PRODUCTS);

    console.log(`   ✓ Found ${products.length} products`);
    return products.map(p => ({ ...p, category: categoryName }));

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 150)}`);
    return [];
  }
}

async function main() {
  console.log("=".repeat(70));
  console.log("LOWES DIRECT CATEGORY COLLECTION");
  console.log("Using Bright Data with $50 credit");
  console.log("Note: Using separate browser sessions per category");
  console.log("=".repeat(70));

  const allProducts = [];

  const categories = [
    "Garage Organization",
    "Shelving",
    "Storage Bins",
    "Cabinets"
  ];

  // Process each category with its own browser session to avoid navigation limits
  for (let i = 0; i < CATEGORY_URLS.length; i++) {
    console.log(`\n[Category ${i + 1}/${CATEGORY_URLS.length}] Starting new browser session...`);

    const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
    const page = await browser.newPage();

    const products = await extractFromCategory(page, CATEGORY_URLS[i], categories[i]);
    allProducts.push(...products);

    await page.close();
    await browser.close();

    console.log(`   Browser session closed. Running total: ${allProducts.length} products`);

    // Rate limiting between categories (allow Bright Data to reset)
    if (i < CATEGORY_URLS.length - 1) {
      console.log(`   Waiting 10 seconds before next category...`);
      await new Promise(resolve => setTimeout(resolve, 10000));
    }
  }

  console.log(`\n${"=".repeat(70)}`);
  console.log(`TOTAL COLLECTED: ${allProducts.length} products`);
  console.log(`${"=".repeat(70)}`);

  if (allProducts.length > 0) {
    const output = {
      retailer: "Lowes",
      collected_at: new Date().toISOString(),
      method: "direct_category_urls",
      product_count: allProducts.length,
      products: allProducts
    };

    fs.writeFileSync('lowes_garage_collection.json', JSON.stringify(output, null, 2));
    console.log("✓ Saved to lowes_garage_collection.json");
  }

  return allProducts.length;
}

main().then(count => {
  console.log(`\n✅ Collection complete: ${count} products`);
  process.exit(count > 0 ? 0 : 1);
}).catch(err => {
  console.error("❌ Collection failed:", err.message);
  process.exit(1);
});
