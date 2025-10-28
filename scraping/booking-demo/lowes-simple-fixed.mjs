import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// Garage organization specific category URLs
const CATEGORY_URLS = [
  { url: "https://www.lowes.com/pl/Garage-organization-Storage-organization/4294612721", name: "Garage Organization" },
  { url: "https://www.lowes.com/pl/Shelving-Storage-organization/4294612733", name: "Shelving" },
  { url: "https://www.lowes.com/pl/Storage-bins-Storage-organization/4294612729", name: "Storage Bins" }
];

const MAX_PRODUCTS = 60; // Per category

async function extractFromCategory(page, categoryInfo) {
  try {
    console.log(`\n🔍 Lowes: ${categoryInfo.name}`);

    await page.goto(categoryInfo.url, { waitUntil: 'networkidle2', timeout: 120000 });
    await new Promise(resolve => setTimeout(resolve, 5000));

    // Extract product URLs and parse names from URLs
    const products = await page.evaluate((maxItems) => {
      const results = [];
      const productLinks = Array.from(document.querySelectorAll('a[href*="/pd/"]'));

      // Deduplicate by href
      const seen = new Set();
      const uniqueLinks = productLinks.filter(link => {
        const href = link.href;
        if (seen.has(href)) return false;
        seen.add(href);
        return true;
      });

      for (let i = 0; i < Math.min(uniqueLinks.length, maxItems); i++) {
        const link = uniqueLinks[i];
        const url = link.href;

        // Parse product name from URL (e.g., /pd/Kobalt-40-in-Fiberglass-Long-handle-Digging-Shovel/1000377397)
        const urlMatch = url.match(/\/pd\/([^/]+)\/(\d+)/);
        if (!urlMatch) continue;

        const nameSlug = urlMatch[1];
        const sku = urlMatch[2];

        // Convert slug to readable name (replace hyphens with spaces, title case)
        const title = nameSlug.replace(/-/g, ' ');

        // Skip if name is too short (likely an error)
        if (title.length < 10) continue;

        results.push({
          title,
          link: url,
          sku,
          price: null, // Will extract if we can find reliable selectors
          brand: null,
          rating: null,
          reviews: null
        });
      }

      return results;
    }, MAX_PRODUCTS);

    console.log(`   ✓ Found ${products.length} products`);
    return products.map(p => ({ ...p, category: categoryInfo.name }));

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 100)}`);
    return [];
  }
}

async function main() {
  console.log("=".repeat(70));
  console.log("LOWES GARAGE ORGANIZATION COLLECTION");
  console.log("Using Bright Data - URL-based product extraction");
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

      console.log(`   Total: ${allProducts.length} products`);

      if (i < CATEGORY_URLS.length - 1) {
        console.log(`   Waiting 10 seconds...`);
        await new Promise(resolve => setTimeout(resolve, 10000));
      }
    } catch (error) {
      console.log(`   Error: ${error.message}`);
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
      method: "url_based_extraction",
      product_count: allProducts.length,
      products: allProducts
    };

    fs.writeFileSync('lowes_garage_products.json', JSON.stringify(output, null, 2));
    console.log("✓ Saved to lowes_garage_products.json");

    // Show sample
    console.log("\n📦 Sample products:");
    allProducts.slice(0, 5).forEach((p, i) => {
      console.log(`  ${i + 1}. ${p.title}`);
      console.log(`     ${p.link.substring(0, 80)}...`);
    });
  }

  return allProducts.length;
}

main().then(count => {
  console.log(`\n✅ Complete: ${count} products`);
  process.exit(count > 0 ? 0 : 1);
}).catch(err => {
  console.error("❌ Failed:", err.message);
  process.exit(1);
});
