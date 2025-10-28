import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// Targeted queries for missing categories + general organizer term
const QUERIES = [
  "garage organizer",
  "garage shelving",
  "garage cabinets",
  "garage storage bins",
  "garage workbench"
];

const MAX_PRODUCTS_PER_QUERY = 40; // Control costs

async function searchAndExtract(browser, query) {
  const page = await browser.newPage();

  try {
    console.log(`\n🔍 Searching Lowes: "${query}"`);

    const searchUrl = `https://www.lowes.com/search?searchTerm=${encodeURIComponent(query)}`;
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 90000 });

    // Wait for Apollo state (Lowes uses GraphQL)
    await page.waitForFunction(() => window.__APOLLO_STATE__ !== undefined, { timeout: 60000 });

    const products = await page.evaluate(() => {
      const state = window.__APOLLO_STATE__;
      if (!state) return [];

      const results = [];
      for (const [key, value] of Object.entries(state)) {
        if (value && typeof value === 'object' && value.__typename === 'SearchProduct') {
          results.push({
            title: value.name,
            price: value.prices?.price?.formattedValue || value.prices?.price?.value,
            rating: value.ratingsAndReviews?.averageRating,
            reviews: value.ratingsAndReviews?.reviewCount,
            link: value.pdpUrl ? `https://www.lowes.com${value.pdpUrl}` : null,
            sku: value.itemNumber,
            brand: value.brand,
            query: undefined // Will be set below
          });
        }
      }
      return results;
    });

    // Add query context and limit results
    const limited = products.slice(0, MAX_PRODUCTS_PER_QUERY).map(p => ({
      ...p,
      query
    }));

    console.log(`   ✓ Found ${limited.length} products`);
    await page.close();
    return limited;

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 100)}`);
    await page.close();
    return [];
  }
}

async function main() {
  console.log("="*60);
  console.log("LOWES TARGETED COLLECTION (Bright Data)");
  console.log("="*60);
  console.log(`Queries: ${QUERIES.length}`);
  console.log(`Max per query: ${MAX_PRODUCTS_PER_QUERY}`);
  console.log(`Estimated max: ${QUERIES.length * MAX_PRODUCTS_PER_QUERY} products`);

  const browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });

  const allProducts = [];

  for (const query of QUERIES) {
    const products = await searchAndExtract(browser, query);
    allProducts.push(...products);

    // Rate limiting
    await new Promise(resolve => setTimeout(resolve, 3000));
  }

  await browser.close();

  console.log(`\n${"=".repeat(60)}`);
  console.log(`TOTAL COLLECTED: ${allProducts.length} products`);
  console.log(`${"=".repeat(60)}`);

  // Save results
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
  console.log(`\n✅ Collection complete: ${count} products`);
  process.exit(0);
}).catch(err => {
  console.error("❌ Collection failed:", err.message);
  process.exit(1);
});
