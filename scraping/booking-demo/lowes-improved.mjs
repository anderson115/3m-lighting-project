import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// More specific garage organization category URLs
const CATEGORY_URLS = [
  { url: "https://www.lowes.com/pl/Garage-organization-Storage-organization/4294612721", name: "Garage Organization" },
  { url: "https://www.lowes.com/pl/Wall-mounted-garage-storage-Garage-organization-Storage-organization/4294612722", name: "Wall Mounted Storage" },
  { url: "https://www.lowes.com/pl/Garage-shelving-units-Garage-organization-Storage-organization/4294612723", name: "Garage Shelving Units" },
  { url: "https://www.lowes.com/pl/Garage-cabinets-Garage-organization-Storage-organization/4294612724", name: "Garage Cabinets" }
];

const MAX_PRODUCTS = 100; // Increase limit

async function extractFromCategory(page, categoryInfo) {
  try {
    console.log(`\n🔍 Lowes: ${categoryInfo.name}`);
    console.log(`   URL: ${categoryInfo.url}`);

    await page.goto(categoryInfo.url, { waitUntil: 'domcontentloaded', timeout: 120000 });

    // Wait for product grid to load
    await new Promise(resolve => setTimeout(resolve, 6000));

    // Scroll to load more products
    await page.evaluate(async () => {
      for (let i = 0; i < 3; i++) {
        window.scrollBy(0, window.innerHeight);
        await new Promise(r => setTimeout(r, 1000));
      }
    });

    await new Promise(resolve => setTimeout(resolve, 2000));

    // Extract product data with improved selectors
    const products = await page.evaluate((maxItems) => {
      const results = [];

      // Find all product links first
      const productLinks = Array.from(document.querySelectorAll('a[href*="/pd/"]'));

      // Group by unique URLs
      const uniqueProducts = new Map();
      productLinks.forEach(link => {
        const url = link.href;
        if (!uniqueProducts.has(url)) {
          uniqueProducts.set(url, link);
        }
      });

      let count = 0;
      for (const [url, link] of uniqueProducts) {
        if (count >= maxItems) break;

        try {
          // Find the product card container
          let card = link.closest('div[data-nodeid]') ||
                    link.closest('article') ||
                    link.closest('[class*="ProductCard"]') ||
                    link.closest('div[class*="product"]');

          if (!card) card = link;

          // Extract product name from URL as fallback
          const urlMatch = url.match(/\/pd\/([^/]+)\//);
          const nameFromUrl = urlMatch ? decodeURIComponent(urlMatch[1]).replace(/-/g, ' ') : '';

          // Try multiple methods to find title
          let title = null;

          // Method 1: Look for heading tags
          const h2 = card.querySelector('h2, h3, h4');
          if (h2) title = h2.textContent.trim();

          // Method 2: Look for product title classes/attributes
          if (!title || title.length < 5) {
            const titleEl = card.querySelector('[class*="title"]') ||
                           card.querySelector('[class*="ProductTitle"]') ||
                           card.querySelector('[class*="name"]');
            if (titleEl) title = titleEl.textContent.trim();
          }

          // Method 3: Use link text
          if (!title || title.length < 5) {
            title = link.textContent.trim();
          }

          // Method 4: Use URL as last resort
          if (!title || title.length < 5) {
            title = nameFromUrl;
          }

          // Skip if still no good title
          if (!title || title.length < 5 ||
              title.includes('Pickup Today') ||
              title.includes('YOU MAY ALSO') ||
              title.includes('Add to Cart')) {
            return; // Skip this product
          }

          // Extract price
          let price = null;
          const priceElements = card.querySelectorAll('[class*="price"], [class*="Price"]');
          for (const priceEl of priceElements) {
            const priceText = priceEl.textContent.trim();
            if (priceText.match(/\$\s*\d+/)) {
              // Clean up price - just get the number
              const match = priceText.match(/\$\s*(\d+(?:\.\d{2})?)/);
              if (match) {
                price = `$${match[1]}`;
                break;
              }
            }
          }

          // Extract brand
          let brand = null;
          const brandEl = card.querySelector('[class*="brand"], [class*="Brand"]');
          if (brandEl) {
            brand = brandEl.textContent.trim();
          }

          // Extract SKU/model from URL
          const skuMatch = url.match(/\/(\d+)$/);
          const sku = skuMatch ? skuMatch[1] : null;

          // Extract rating
          let rating = null;
          const ratingEl = card.querySelector('[aria-label*="star"]');
          if (ratingEl) {
            const ratingMatch = ratingEl.getAttribute('aria-label').match(/(\d+\.?\d*)/);
            if (ratingMatch) rating = parseFloat(ratingMatch[1]);
          }

          results.push({
            title,
            link: url,
            price,
            brand,
            sku,
            rating,
            reviews: null
          });

          count++;
        } catch (err) {
          // Skip problematic products
        }
      }

      return results;
    }, MAX_PRODUCTS);

    console.log(`   ✓ Extracted ${products.length} products`);
    return products.map(p => ({ ...p, category: categoryInfo.name }));

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 150)}`);
    return [];
  }
}

async function main() {
  console.log("=".repeat(70));
  console.log("LOWES IMPROVED COLLECTION");
  console.log("Using Bright Data - Separate sessions per category");
  console.log("=".repeat(70));

  const allProducts = [];

  for (let i = 0; i < CATEGORY_URLS.length; i++) {
    console.log(`\n[Category ${i + 1}/${CATEGORY_URLS.length}]`);

    let browser, page;
    try {
      browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
      page = await browser.newPage();

      const products = await extractFromCategory(page, CATEGORY_URLS[i]);
      allProducts.push(...products);

      await page.close();
      await browser.close();

      console.log(`   Session closed. Running total: ${allProducts.length} products`);

      // Rate limiting
      if (i < CATEGORY_URLS.length - 1) {
        console.log(`   Waiting 8 seconds...`);
        await new Promise(resolve => setTimeout(resolve, 8000));
      }
    } catch (error) {
      console.log(`   Session error: ${error.message}`);
      try { if (page) await page.close(); } catch {}
      try { if (browser) await browser.close(); } catch {}
    }
  }

  console.log(`\n${"=".repeat(70)}`);
  console.log(`TOTAL COLLECTED: ${allProducts.length} products`);
  console.log(`${"=".repeat(70)}`);

  if (allProducts.length > 0) {
    const output = {
      retailer: "Lowes",
      collected_at: new Date().toISOString(),
      method: "improved_category_extraction",
      product_count: allProducts.length,
      products: allProducts
    };

    fs.writeFileSync('lowes_garage_collection.json', JSON.stringify(output, null, 2));
    console.log("✓ Saved to lowes_garage_collection.json");

    // Print sample
    if (allProducts.length > 0) {
      console.log("\nSample products:");
      allProducts.slice(0, 3).forEach((p, i) => {
        console.log(`  ${i + 1}. ${p.title} - ${p.price || 'N/A'}`);
      });
    }
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
