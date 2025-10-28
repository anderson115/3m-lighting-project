import puppeteer from "puppeteer-core";
import fs from "fs";

const BROWSER_WS = "wss://brd-customer-hl_694870e0-zone-scraping_api_3m_lighting:hpgmxk27dafu@brd.superproxy.io:9222";

// Targeted workbench searches focusing on premium segment
const RETAILERS = [
  {
    name: "Lowes",
    searches: [
      "garage workbench",
      "work bench garage",
      "tool bench storage",
      "workstation garage",
      "heavy duty workbench",
      "wood workbench",
      "metal workbench garage",
      "adjustable height workbench",
      "workbench cabinet combo",
      "mobile workbench"
    ],
    baseUrl: "https://www.lowes.com/search?searchTerm=",
    urlPattern: "/pd/"
  },
  {
    name: "Home Depot",
    searches: [
      "garage workbench",
      "work bench garage",
      "tool workbench",
      "workstation garage",
      "heavy duty work bench",
      "wood garage workbench",
      "steel workbench",
      "adjustable workbench",
      "workbench with storage",
      "portable workbench garage"
    ],
    baseUrl: "https://www.homedepot.com/s/",
    urlPattern: "/p/"
  },
  {
    name: "Walmart",
    searches: [
      "garage workbench",
      "work bench",
      "tool bench",
      "workstation storage",
      "heavy duty workbench",
      "workbench with drawers",
      "rolling workbench"
    ],
    baseUrl: "https://www.walmart.com/search?q=",
    urlPattern: "/ip/"
  }
];

const MAX_PRODUCTS = 100;

async function extractProducts(page, retailer, query) {
  try {
    console.log(`\n🔍 ${retailer.name}: "${query}"`);

    const searchUrl = `${retailer.baseUrl}${encodeURIComponent(query)}`;
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 120000 });
    await new Promise(resolve => setTimeout(resolve, 6000));

    await page.evaluate(async () => {
      for (let i = 0; i < 3; i++) {
        window.scrollBy(0, window.innerHeight);
        await new Promise(r => setTimeout(r, 1000));
      }
    });
    await new Promise(resolve => setTimeout(resolve, 2000));

    const products = await page.evaluate((urlPattern, maxItems) => {
      const results = [];
      const productLinks = Array.from(document.querySelectorAll(`a[href*="${urlPattern}"]`));

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

        let title = '';
        let sku = '';

        if (urlPattern === '/pd/') {
          const match = url.match(/\/pd\/([^/]+)\/(\d+)/);
          if (match) {
            title = match[1].replace(/-/g, ' ');
            sku = match[2];
          }
        } else if (urlPattern === '/p/') {
          const match = url.match(/\/p\/([^/]+)\/(\d+)/);
          if (match) {
            title = match[1].replace(/-/g, ' ');
            sku = match[2];
          }
        } else if (urlPattern === '/ip/') {
          const match = url.match(/\/ip\/([^/]+)\/(\d+)/);
          if (match) {
            title = match[1].replace(/-/g, ' ');
            sku = match[2];
          }
        }

        if (title.length < 10) continue;

        const titleLower = title.toLowerCase();

        // Must be workbench/work bench/workstation
        if (!titleLower.includes('workbench') &&
            !titleLower.includes('work bench') &&
            !titleLower.includes('work station') &&
            !titleLower.includes('workstation') &&
            !titleLower.includes('tool bench')) {
          continue;
        }

        // Skip non-garage items
        if (titleLower.includes('kids') ||
            titleLower.includes('toy') ||
            titleLower.includes('play') ||
            titleLower.includes('child')) {
          continue;
        }

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
    }, retailer.urlPattern, MAX_PRODUCTS);

    console.log(`   ✓ Found ${products.length} workbench products`);
    return products.map(p => ({ ...p, retailer: retailer.name, search_query: query }));

  } catch (error) {
    console.log(`   ❌ Error: ${error.message.substring(0, 100)}`);
    return [];
  }
}

async function main() {
  console.log("=".repeat(70));
  console.log("WORKBENCH PREMIUM EXPANSION COLLECTION");
  console.log("Target: High-value workbench segment for market entry analysis");
  console.log("=".repeat(70));

  const allProducts = [];
  const seenUrls = new Set();
  let totalSearches = 0;

  for (const retailer of RETAILERS) {
    totalSearches += retailer.searches.length;
  }

  let searchCount = 0;

  for (const retailer of RETAILERS) {
    console.log(`\n${"=".repeat(70)}`);
    console.log(`RETAILER: ${retailer.name.toUpperCase()}`);
    console.log(`${"=".repeat(70)}`);

    for (const query of retailer.searches) {
      searchCount++;
      console.log(`\n[Search ${searchCount}/${totalSearches}]`);

      let browser, page;
      try {
        browser = await puppeteer.connect({ browserWSEndpoint: BROWSER_WS });
        page = await browser.newPage();

        const products = await extractProducts(page, retailer, query);

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

        console.log(`   New unique: ${newCount}, Total: ${allProducts.length}`);

        if (searchCount < totalSearches) {
          console.log(`   Waiting 10 seconds...`);
          await new Promise(resolve => setTimeout(resolve, 10000));
        }

      } catch (error) {
        console.log(`   Session error: ${error.message.substring(0, 100)}`);
        try { if (page) await page.close(); } catch {}
        try { if (browser) await browser.close(); } catch {}
      }
    }
  }

  console.log(`\n${"=".repeat(70)}`);
  console.log(`WORKBENCH EXPANSION COMPLETE`);
  console.log(`${"=".repeat(70)}`);
  console.log(`Total unique workbenches: ${allProducts.length}`);

  if (allProducts.length > 0) {
    const output = {
      category: "Workbenches (Premium Expansion)",
      collected_at: new Date().toISOString(),
      method: "targeted_premium_searches",
      strategic_purpose: "Market entry opportunity analysis",
      retailers: RETAILERS.map(r => r.name),
      product_count: allProducts.length,
      products: allProducts
    };

    fs.writeFileSync('workbenches_premium_expansion.json', JSON.stringify(output, null, 2));
    console.log("\n✓ Saved to workbenches_premium_expansion.json");
  }

  return allProducts.length;
}

main().then(count => {
  console.log(`\n✅ Collection complete: ${count} unique workbench products`);
  process.exit(count > 0 ? 0 : 1);
}).catch(err => {
  console.error("❌ Failed:", err.message);
  process.exit(1);
});
