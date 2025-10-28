import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// Targeted queries for missing categories
const QUERIES = [
  "garage organizer",
  "garage shelving",
  "garage cabinets",
  "garage storage bins",
  "garage workbench"
];

const MAX_PRODUCTS_PER_QUERY = 40;

async function searchAndExtract(browser, query) {
  const page = await browser.newPage();

  try {
    console.log(`\n🔍 Searching Menards: "${query}"`);

    const searchUrl = `https://www.menards.com/main/search.html?search=${encodeURIComponent(query)}`;
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 90000 });

    // Wait for product grid
    await page.waitForSelector('.plp-pod, [data-testid="product-pod"], .product-card', { timeout: 30000 });

    const products = await page.$$eval('.plp-pod, [data-testid="product-pod"], .product-card', (cards) => {
      return cards.slice(0, 40).map(card => {
        const title = card.querySelector('.plp-pod__description-name, [data-testid="product-title"], .product-title')?.textContent?.trim();
        const priceEl = card.querySelector('.plp-pod__description-price, [data-testid="price"], .price');
        const price = priceEl?.textContent?.trim();
        const link = card.querySelector('a')?.href;
        const brand = card.querySelector('.brand, [data-testid="brand"]')?.textContent?.trim();
        const sku = card.querySelector('[data-product-id], [data-sku]')?.getAttribute('data-product-id') ||
                    card.querySelector('[data-product-id], [data-sku]')?.getAttribute('data-sku');

        return {
          title,
          price,
          link,
          brand,
          sku,
          rating: null,
          reviews: null
        };
      }).filter(p => p.title && p.link);
    });

    const withQuery = products.map(p => ({ ...p, query }));

    console.log(`   ✓ Found ${withQuery.length} products`);
    await page.close();
    return withQuery;

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 100)}`);
    await page.close();
    return [];
  }
}

async function main() {
  console.log("="*60);
  console.log("MENARDS TARGETED COLLECTION (Bright Data)");
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
    retailer: "Menards",
    collected_at: new Date().toISOString(),
    queries: QUERIES,
    product_count: allProducts.length,
    products: allProducts
  };

  fs.writeFileSync('menards_garage_collection.json', JSON.stringify(output, null, 2));
  console.log("✓ Saved to menards_garage_collection.json");

  return allProducts.length;
}

main().then(count => {
  console.log(`\n✅ Collection complete: ${count} products`);
  process.exit(0);
}).catch(err => {
  console.error("❌ Collection failed:", err.message);
  process.exit(1);
});
