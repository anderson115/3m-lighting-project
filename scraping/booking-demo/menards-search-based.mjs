import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// Targeted search queries for garage organization
const SEARCH_QUERIES = [
  "garage organization",
  "garage wall storage",
  "garage shelving",
  "garage cabinets",
  "garage hooks"
];

const MAX_PRODUCTS = 50; // Per search

async function searchAndExtract(page, query) {
  try {
    console.log(`\n🔍 Searching: "${query}"`);

    const searchUrl = `https://www.menards.com/main/search.html?search=${encodeURIComponent(query)}`;
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 120000 });
    await new Promise(resolve => setTimeout(resolve, 6000));

    // Extract product data - Menards typically uses different URL patterns
    const products = await page.evaluate((maxItems) => {
      const results = [];

      // Find product links - Menards uses /p/ in URLs
      const productLinks = Array.from(document.querySelectorAll('a[href*="/p/"]'));

      // Deduplicate
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

        // Try to extract SKU from URL (Menards format varies)
        const skuMatch = url.match(/\/p\/([^/]+)/);
        const sku = skuMatch ? skuMatch[1] : null;

        // Try to get title from link text or nearby elements
        let title = link.textContent?.trim() || '';

        // If title is too short, try to find it in parent container
        if (title.length < 10) {
          const container = link.closest('[class*="product"]') || link.closest('div');
          const titleEl = container?.querySelector('[class*="title"], h2, h3, h4');
          if (titleEl) title = titleEl.textContent?.trim() || '';
        }

        // Last resort: extract from URL
        if (title.length < 10 && skuMatch) {
          title = skuMatch[1].replace(/-/g, ' ');
        }

        // Skip if still no good title
        if (title.length < 10) continue;

        // Clean up title (remove extra whitespace, newlines)
        title = title.replace(/\s+/g, ' ').trim();

        results.push({
          title,
          link: url,
          sku,
          price: null,
          brand: null,
          rating: null,
          reviews: null
        });
      }

      return results;
    }, MAX_PRODUCTS);

    console.log(`   ✓ Found ${products.length} products`);
    return products.map(p => ({ ...p, search_query: query }));

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 100)}`);
    return [];
  }
}

async function main() {
  console.log("=".repeat(70));
  console.log("MENARDS SEARCH-BASED COLLECTION");
  console.log("Garage Organization Products");
  console.log("=".repeat(70));

  const allProducts = [];
  const seenUrls = new Set();

  for (let i = 0; i < SEARCH_QUERIES.length; i++) {
    console.log(`\n[Search ${i + 1}/${SEARCH_QUERIES.length}]`);

    let browser, page;
    try {
      browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
      page = await browser.newPage();

      const products = await searchAndExtract(page, SEARCH_QUERIES[i]);

      // Deduplicate across searches
      let newCount = 0;
      for (const product of products) {
        if (!seenUrls.has(product.link)) {
          seenUrls.add(product.link);
          allProducts.push(product);
          newCount++;
        }
      }

      await page.close();
      await browser.close();

      console.log(`   New unique: ${newCount}, Total unique: ${allProducts.length}`);

      if (i < SEARCH_QUERIES.length - 1) {
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
  console.log(`TOTAL UNIQUE PRODUCTS: ${allProducts.length}`);
  console.log(`${"=".repeat(70)}`);

  if (allProducts.length > 0) {
    const output = {
      retailer: "Menards",
      collected_at: new Date().toISOString(),
      method: "search_based_extraction",
      search_queries: SEARCH_QUERIES,
      product_count: allProducts.length,
      products: allProducts
    };

    fs.writeFileSync('menards_garage_products.json', JSON.stringify(output, null, 2));
    console.log("✓ Saved to menards_garage_products.json");

    // Show sample
    console.log("\n📦 Sample products:");
    const sampleIndices = [0, Math.floor(allProducts.length / 4), Math.floor(allProducts.length / 2), Math.floor(3 * allProducts.length / 4), allProducts.length - 1];
    sampleIndices.forEach((idx) => {
      if (idx < allProducts.length) {
        const p = allProducts[idx];
        console.log(`  • ${p.title.substring(0, 70)}`);
      }
    });
  }

  return allProducts.length;
}

main().then(count => {
  console.log(`\n✅ Complete: ${count} unique products`);
  process.exit(count > 0 ? 0 : 1);
}).catch(err => {
  console.error("❌ Failed:", err.message);
  process.exit(1);
});
