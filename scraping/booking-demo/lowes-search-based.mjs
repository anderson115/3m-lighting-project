import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// Targeted search queries for garage organization
const SEARCH_QUERIES = [
  "garage organization system",
  "garage wall organizer",
  "garage shelving unit",
  "garage storage cabinet",
  "garage hooks and hangers"
];

const MAX_PRODUCTS = 50; // Per search

async function searchAndExtract(page, query) {
  try {
    console.log(`\n🔍 Searching: "${query}"`);

    const searchUrl = `https://www.lowes.com/search?searchTerm=${encodeURIComponent(query)}`;
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 120000 });
    await new Promise(resolve => setTimeout(resolve, 6000));

    // Extract product URLs
    const products = await page.evaluate((maxItems) => {
      const results = [];
      const productLinks = Array.from(document.querySelectorAll('a[href*="/pd/"]'));

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

        // Parse from URL
        const urlMatch = url.match(/\/pd\/([^/]+)\/(\d+)/);
        if (!urlMatch) continue;

        const nameSlug = urlMatch[1];
        const sku = urlMatch[2];
        const title = nameSlug.replace(/-/g, ' ');

        if (title.length < 10) continue;

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
  console.log("LOWES SEARCH-BASED COLLECTION");
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
      retailer: "Lowes",
      collected_at: new Date().toISOString(),
      method: "search_based_extraction",
      search_queries: SEARCH_QUERIES,
      product_count: allProducts.length,
      products: allProducts
    };

    fs.writeFileSync('lowes_garage_products.json', JSON.stringify(output, null, 2));
    console.log("✓ Saved to lowes_garage_products.json");

    // Show diverse sample
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
